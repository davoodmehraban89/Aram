"""Synthetic DB-backed *unreviewed* proposal persistence; not approval or apply."""
import pytest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from aram_backend.mapping_batch_review import ProposedMappingRow, preview_mapping_batch
from aram_backend.mapping_draft_store import (
    mapping_review_drafts, save_unreviewed_batch,
    get_unreviewed_batch, validate_unreviewed_batch_current,
)
from aram_backend.mapping_service import MappingValidationError, save_mapping_rule
from aram_backend.models import (
    Company, FiscalYear, FiscalYearStatus, NoteDefinition, AccountVersion, MappingRule,
)


@pytest.fixture
def setup(session):
    # Deliberately NOT part of Base.metadata. Migration creates this table
    # after initial metadata-driven migration to prevent double-create.
    mapping_review_drafts.create(session.get_bind())
    company = Company(code="DRAFT-STORE", name="Synthetic")
    year = FiscalYear(company=company, year=1404)
    session.add(year)
    session.flush()
    note1 = NoteDefinition(year_id=year.id, note_number="1", title="Cash", version=1)
    note2 = NoteDefinition(year_id=year.id, note_number="2", title="Receivables", version=1)
    account = AccountVersion(
        year_id=year.id, account_code="001", account_name="Cash", version=1,
    )
    session.add_all([note1, note2, account])
    session.commit()
    return session, year, note1, note2


def proposal(session, year, note, key="cash"):
    return preview_mapping_batch(session, year_id=year.id, rows=(
        ProposedMappingRow(
            source_locator="Mapping!2", rule_key=key, account_code="001",
            target_note_id=note.id, mapping_type="manual", expected_base_version=0,
        ),
    ))


def test_save_unreviewed_draft_persists_exact_original_without_mapping_write(setup):
    session, year, note, _ = setup
    draft = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="request-0001",
    )
    assert draft.id > 0
    assert draft.year_id == year.id
    assert draft.state == "Unreviewed"
    assert draft.checksum
    assert session.scalars(select(MappingRule)).all() == []
    session.commit()
    other = get_unreviewed_batch(session, draft_id=draft.id, year_id=year.id)
    assert other == draft
    assert validate_unreviewed_batch_current(
        session, draft_id=draft.id, year_id=year.id
    ) is None
    assert session.scalars(select(MappingRule)).all() == []


def test_exact_idempotent_retry_never_creates_second_draft(setup):
    session, year, note, _ = setup
    snapshot = proposal(session, year, note)
    first = save_unreviewed_batch(session, snapshot, request_key="request-0002")
    session.commit()
    again = save_unreviewed_batch(session, snapshot, request_key="request-0002")
    session.commit()
    assert first == again
    assert len(session.execute(select(mapping_review_drafts)).all()) == 1


def test_idempotency_key_cannot_represent_different_proposal(setup):
    session, year, cash, other = setup
    save_unreviewed_batch(session, proposal(session, year, cash), request_key="request-0003")
    session.commit()
    with pytest.raises(MappingValidationError, match="idempotency|request key"):
        save_unreviewed_batch(session, proposal(session, year, other), request_key="request-0003")
    assert len(session.execute(select(mapping_review_drafts)).all()) == 1


def test_rollback_removes_staged_draft_without_touching_mapping(setup):
    session, year, note, _ = setup
    draft = save_unreviewed_batch(session, proposal(session, year, note), request_key="request-0004")
    assert draft.id > 0
    session.rollback()
    assert session.execute(select(mapping_review_drafts)).all() == []
    assert session.scalars(select(MappingRule)).all() == []


def test_original_draft_is_stale_after_newer_note_version(setup):
    session, year, note, _ = setup
    draft = save_unreviewed_batch(session, proposal(session, year, note), request_key="request-0005")
    session.commit()
    session.add(NoteDefinition(year_id=year.id, note_number="1", title="Revised", version=2))
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        validate_unreviewed_batch_current(session, draft_id=draft.id, year_id=year.id)
    assert get_unreviewed_batch(session, draft_id=draft.id, year_id=year.id).state == "Unreviewed"


def test_original_draft_stale_after_rule_change(setup):
    session, year, note, other = setup
    draft = save_unreviewed_batch(session, proposal(session, year, note), request_key="request-0006")
    session.commit()
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=other.id, mapping_type="manual", version=1,
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        validate_unreviewed_batch_current(session, draft_id=draft.id, year_id=year.id)


def test_staged_draft_is_invalid_after_approved_year(setup):
    session, year, note, _ = setup
    draft = save_unreviewed_batch(session, proposal(session, year, note), request_key="request-0007")
    session.commit()
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        validate_unreviewed_batch_current(session, draft_id=draft.id, year_id=year.id)


def test_wrong_year_cannot_access_draft_even_with_known_id(setup):
    session, year, note, _ = setup
    draft = save_unreviewed_batch(session, proposal(session, year, note), request_key="request-0008")
    session.commit()
    with pytest.raises(MappingValidationError, match="not found"):
        get_unreviewed_batch(session, draft_id=draft.id, year_id=year.id + 1)
    with pytest.raises(MappingValidationError, match="not found"):
        validate_unreviewed_batch_current(session, draft_id=draft.id, year_id=year.id + 1)


@pytest.mark.parametrize("bad", ["", " spaces ", "a" * 65, "\n", "contains\x00nul", False, 123])
def test_invalid_request_keys_are_rejected_without_sql_inserts(setup, bad):
    session, year, note, _ = setup
    with pytest.raises(MappingValidationError, match="request key"):
        save_unreviewed_batch(session, proposal(session, year, note), request_key=bad)
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_conflicted_batch_cannot_be_stored(setup):
    session, year, cash, other = setup
    first = ProposedMappingRow("M!2", "cash", "001", cash.id, "manual", 0)
    second = ProposedMappingRow("M!3", "cash", "001", other.id, "manual", 0)
    rejected = preview_mapping_batch(session, year_id=year.id, rows=[first, second])
    assert not rejected.ready_for_review
    with pytest.raises(MappingValidationError, match="not ready"):
        save_unreviewed_batch(session, rejected, request_key="request-0009")
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_modified_snapshot_cannot_be_stored(setup):
    from dataclasses import replace
    session, year, note, _ = setup
    original = proposal(session, year, note)
    tampered = replace(original, fingerprint="a" * 64)
    with pytest.raises(MappingValidationError, match="stale"):
        save_unreviewed_batch(session, tampered, request_key="request-0010")
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_db_check_constraint_rejects_synthetic_approved_state(setup):
    session, year, note, _ = setup
    draft = save_unreviewed_batch(session, proposal(session, year, note), request_key="request-0011")
    session.commit()
    with pytest.raises(IntegrityError):
        session.execute(
            update(mapping_review_drafts)
            .where(mapping_review_drafts.c.id == draft.id)
            .values(state="Approved")
        )
        session.commit()
    session.rollback()
    assert get_unreviewed_batch(session, draft_id=draft.id, year_id=year.id).state == "Unreviewed"


def test_cannot_store_draft_with_pending_related_financial_changes(setup):
    session, year, note, _ = setup
    snap = proposal(session, year, note)
    session.add(AccountVersion(
        year_id=year.id, account_code="SHADOW", account_name="Pending", version=1,
    ))
    with pytest.raises(MappingValidationError, match="clean Session"):
        save_unreviewed_batch(session, snap, request_key="request-0012")
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_draft_state_is_unreviewed_not_authenticated_approval(setup):
    session, year, note, _ = setup
    draft = save_unreviewed_batch(session, proposal(session, year, note), request_key="request-0013")
    assert not hasattr(draft, "approver_id")
    assert not hasattr(draft, "approved_at")
    assert not hasattr(draft, "apply")
    assert draft.state == "Unreviewed"
