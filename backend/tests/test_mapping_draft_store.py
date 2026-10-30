"""Synthetic DB-backed *unreviewed* proposal persistence; not approval or apply."""
import pytest
from sqlalchemy import select, update, insert, inspect
from sqlalchemy.exc import IntegrityError

from aram_backend.mapping_batch_review import ProposedMappingRow, preview_mapping_batch
from aram_backend.mapping_draft_store import (
    mapping_review_drafts, save_unreviewed_batch,
    get_unreviewed_batch, validate_unreviewed_batch_current,
)
from aram_backend.mapping_service import MappingValidationError, save_mapping_rule
from aram_backend.mapping_draft_audit import mapping_draft_events, verify_draft_staging_event
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
    try:
        yield session, year, note1, note2
    finally:
        # This table deliberately lives outside Base.metadata. It MUST be
        # removed before the outer session fixture drops FiscalYear tables.
        session.rollback()
        mapping_review_drafts.drop(session.get_bind())


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


def test_stored_proposal_checksum_detects_direct_sql_payload_change(setup):
    session, year, note, _ = setup
    saved = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="request-0014",
    )
    session.commit()
    session.execute(
        update(mapping_review_drafts)
        .where(mapping_review_drafts.c.id == saved.id)
        .values(payload_json={"batch": {"source_rows": []}})
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="corrupted"):
        get_unreviewed_batch(session, draft_id=saved.id, year_id=year.id)
    with pytest.raises(MappingValidationError, match="corrupted"):
        validate_unreviewed_batch_current(session, draft_id=saved.id, year_id=year.id)


def test_database_unique_constraint_rejects_duplicate_request_identity(setup):
    session, year, note, _ = setup
    first = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="request-0015",
    )
    session.commit()
    existing = session.execute(
        select(mapping_review_drafts).where(mapping_review_drafts.c.id == first.id)
    ).mappings().one()
    with pytest.raises(IntegrityError):
        session.execute(
            insert(mapping_review_drafts).values(
                year_id=year.id, request_key=first.request_key,
                payload_json=existing["payload_json"],
                payload_hash=existing["payload_hash"], state="Unreviewed",
            )
        )
        session.commit()
    session.rollback()
    assert len(session.execute(select(mapping_review_drafts)).all()) == 1


def test_proposal_table_has_independent_metadata_and_fk(setup):
    from aram_backend.database import Base
    session, year, note, _ = setup
    assert "mapping_review_drafts" not in Base.metadata.tables
    assert "mapping_review_drafts" in inspect(session.get_bind()).get_table_names()
    names = {fk["referred_table"] for fk in inspect(session.get_bind()).get_foreign_keys("mapping_review_drafts")}
    assert "fiscal_years" in names


def test_staging_has_exactly_one_atomic_system_audit_event(setup):
    session, year, note, _ = setup
    staged = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="audit-01",
    )
    events = session.execute(
        select(mapping_draft_events).where(mapping_draft_events.c.draft_id == staged.id)
    ).mappings().all()
    assert len(events) == 1
    assert events[0]["event_type"] == "DraftStaged"
    assert events[0]["year_id"] == year.id
    assert events[0]["payload_hash"] == staged.checksum
    assert verify_draft_staging_event(session, draft_id=staged.id, year_id=year.id) is None
    assert session.scalars(select(MappingRule)).all() == []
    session.commit()
    assert verify_draft_staging_event(session, draft_id=staged.id, year_id=year.id) is None


def test_staged_draft_rollback_discards_audit_and_proposal_together(setup):
    session, year, note, _ = setup
    save_unreviewed_batch(session, proposal(session, year, note), request_key="audit-02")
    assert len(session.execute(select(mapping_draft_events)).all()) == 1
    session.rollback()
    assert session.execute(select(mapping_draft_events)).all() == []
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_idempotent_replay_does_not_append_another_audit_event(setup):
    session, year, note, _ = setup
    snapshot = proposal(session, year, note)
    initial = save_unreviewed_batch(session, snapshot, request_key="audit-03")
    session.commit()
    repeated = save_unreviewed_batch(session, snapshot, request_key="audit-03")
    session.commit()
    assert initial == repeated
    assert len(session.execute(select(mapping_draft_events)).all()) == 1


def test_sqlite_event_audit_update_and_delete_are_denied_by_triggers(setup):
    session, year, note, _ = setup
    saved = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="audit-04",
    )
    session.commit()
    with pytest.raises(IntegrityError):
        session.execute(
            update(mapping_draft_events)
            .where(mapping_draft_events.c.draft_id == saved.id)
            .values(payload_hash="0" * 64)
        )
    session.rollback()
    from sqlalchemy import delete
    with pytest.raises(IntegrityError):
        session.execute(
            delete(mapping_draft_events)
            .where(mapping_draft_events.c.draft_id == saved.id)
        )
    session.rollback()
    assert verify_draft_staging_event(session, draft_id=saved.id, year_id=year.id) is None


def test_draft_read_rejects_modified_payload_even_if_draft_hash_is_recomputed(setup):
    session, year, note, _ = setup
    saved = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="audit-05",
    )
    session.commit()
    from hashlib import sha256
    import json
    corrupted = {"batch": {"source_rows": []}}
    replacement_hash = sha256(json.dumps(
        corrupted, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")).hexdigest()
    session.execute(
        update(mapping_review_drafts)
        .where(mapping_review_drafts.c.id == saved.id)
        .values(payload_json=corrupted, payload_hash=replacement_hash)
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="audit|tamper|corrupt"):
        get_unreviewed_batch(session, draft_id=saved.id, year_id=year.id)


def test_draft_event_foreign_year_is_not_readable(setup):
    session, year, note, _ = setup
    saved = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="audit-06",
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="not found"):
        verify_draft_staging_event(session, draft_id=saved.id, year_id=year.id + 1)


def test_raw_sql_cannot_insert_second_event_for_same_draft(setup):
    session, year, note, _ = setup
    saved = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="audit-07",
    )
    session.commit()
    event = session.execute(select(mapping_draft_events)).mappings().one()
    with pytest.raises(IntegrityError):
        session.execute(
            insert(mapping_draft_events).values(
                draft_id=saved.id, year_id=year.id,
                event_type="DraftStaged",
                payload_hash=event["payload_hash"],
                event_hash=event["event_hash"],
            )
        )
    session.rollback()
    assert len(session.execute(select(mapping_draft_events)).all()) == 1


def test_draft_event_is_system_staging_not_user_approval(setup):
    session, year, note, _ = setup
    saved = save_unreviewed_batch(
        session, proposal(session, year, note), request_key="audit-08",
    )
    event = session.execute(select(mapping_draft_events)).mappings().one()
    assert event["event_type"] == "DraftStaged"
    assert "approved_by" not in mapping_draft_events.c
    assert "reviewer_id" not in mapping_draft_events.c
    assert not hasattr(saved, "approve")
    assert session.scalars(select(MappingRule)).all() == []
