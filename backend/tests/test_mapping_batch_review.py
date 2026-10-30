"""Synthetic evidence-only batch Mapping review: never apply proposals."""
from dataclasses import replace

import pytest
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from aram_backend.mapping_batch_review import (
    ProposedMappingRow, preview_mapping_batch, verify_mapping_batch_current,
)
from aram_backend.mapping_service import MappingValidationError, save_mapping_rule
from aram_backend.models import (
    AccountVersion, Company, FiscalYear, FiscalYearStatus, MappingRule, NoteDefinition,
)


def setup_year(session, code="BATCH-A"):
    company = Company(code=code, name="Synthetic Batch")
    year = FiscalYear(company=company, year=1404)
    session.add(year)
    session.flush()
    cash = NoteDefinition(year_id=year.id, note_number="1", title="Cash", version=1)
    receivables = NoteDefinition(year_id=year.id, note_number="2", title="Receivables", version=1)
    session.add_all([cash, receivables])
    for account in ("001", "002"):
        session.add(AccountVersion(
            year_id=year.id, account_code=account, account_name=account, version=1,
        ))
    session.commit()
    return year, cash, receivables


def row(locator, rule_key, note, **override):
    payload = dict(
        source_locator=locator, rule_key=rule_key, account_code="001",
        target_note_id=note.id, mapping_type="manual", expected_base_version=0,
    )
    payload.update(override)
    return ProposedMappingRow(**payload)


def test_unique_new_rows_are_previewed_but_never_saved(session):
    year, cash, note2 = setup_year(session)
    before = session.scalars(select(MappingRule)).all()
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("Mapping!2", "cash", cash),
        row("Mapping!3", "ar", note2, account_code="002"),
    ])
    assert result.counts == {"new": 2}
    assert result.ready_for_review is True
    assert result.has_changes is True
    assert len(result.fingerprint) == 64
    assert all(item.preview is not None for item in result.rows)
    assert [item.preview.proposed.version for item in result.rows] == [1, 1]
    assert session.scalars(select(MappingRule)).all() == before == []


def test_identical_source_duplicates_are_coalesced_not_applied_twice(session):
    year, cash, _ = setup_year(session, "BATCH-DUP")
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("Mapping!2", "cash", cash),
        row("Mapping!3", "cash", cash),
    ])
    assert [x.status for x in result.rows] == ["new", "coalesced"]
    assert result.rows[1].duplicate_of == "Mapping!2"
    assert result.counts == {"new": 1, "coalesced": 1}
    assert result.ready_for_review is True
    assert session.scalars(select(MappingRule)).all() == []


def test_conflicting_duplicates_poison_all_rows_without_first_wins(session):
    year, cash, other = setup_year(session, "BATCH-CONFLICT")
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("Mapping!2", "cash", cash),
        row("Mapping!9", "cash", other),
        row("Mapping!10", "cash", cash),
    ])
    assert [x.status for x in result.rows] == ["conflict"] * 3
    assert result.counts == {"conflict": 3}
    assert result.ready_for_review is False
    assert result.has_changes is False
    assert all(x.preview is None for x in result.rows)
    assert session.scalars(select(MappingRule)).all() == []


def test_existing_unchanged_and_changed_show_old_and_new(session):
    year, cash, other = setup_year(session, "BATCH-DIFF")
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    save_mapping_rule(
        session, year_id=year.id, rule_key="ar", account_code="002",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.commit()
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("Mapping!2", "cash", cash, expected_base_version=1),
        row("Mapping!3", "ar", other, account_code="002", expected_base_version=1),
    ])
    assert [x.status for x in result.rows] == ["unchanged", "changed"]
    assert result.rows[0].preview is None
    assert result.rows[1].preview.before.target_note_id == cash.id
    assert result.rows[1].preview.proposed.target_note_id == other.id
    assert result.rows[1].preview.proposed.version == 2
    assert result.ready_for_review is True
    assert len(session.scalars(select(MappingRule)).all()) == 2


def test_stale_base_version_is_invalid_and_blocks_entire_batch(session):
    year, cash, _ = setup_year(session, "BATCH-STALE")
    save_mapping_rule(
        session, year_id=year.id, rule_key="old", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.commit()
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("Mapping!2", "valid", cash),
        row("Mapping!3", "old", cash, expected_base_version=0),
    ])
    assert [x.status for x in result.rows] == ["new", "invalid"]
    assert "stale base" in result.rows[1].reason
    assert result.ready_for_review is False
    assert result.has_changes is True
    assert len(session.scalars(select(MappingRule)).all()) == 1


def test_cross_year_note_and_unknown_account_are_invalid(session):
    year, cash, _ = setup_year(session, "BATCH-OWNER")
    _, foreign, _ = setup_year(session, "BATCH-FOREIGN")
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("Mapping!2", "foreign", foreign),
        row("Mapping!3", "unknown", cash, account_code="404"),
    ])
    assert result.counts == {"invalid": 2}
    assert "same fiscal year" in result.rows[0].reason
    assert "account code" in result.rows[1].reason
    assert result.ready_for_review is False


def test_stale_same_year_note_is_invalid_before_import(session):
    year, old_note, _ = setup_year(session, "BATCH-OLDNOTE")
    session.add(NoteDefinition(year_id=year.id, note_number="1", title="New", version=2))
    session.commit()
    result = preview_mapping_batch(session, year_id=year.id, rows=[row("M!2", "x", old_note)])
    assert result.rows[0].status == "invalid"
    assert "latest note" in result.rows[0].reason
    assert result.ready_for_review is False


def test_all_noop_is_not_an_approvable_delta(session):
    year, cash, _ = setup_year(session, "BATCH-NOOP")
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.commit()
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("M!2", "cash", cash, expected_base_version=1),
    ])
    assert result.counts == {"unchanged": 1}
    assert result.has_changes is False
    assert result.ready_for_review is False


def test_deterministic_snapshot_and_no_autoflush_of_unrelated_company(session):
    year, cash, _ = setup_year(session, "BATCH-DETERM")
    unrelated = Company(code="UNCOMMITTED-BATCH", name="Uncommitted")
    session.add(unrelated)
    rows = (row("M!2", "cash", cash),)
    first = preview_mapping_batch(session, year_id=year.id, rows=rows)
    second = preview_mapping_batch(session, year_id=year.id, rows=rows)
    assert first == second
    assert unrelated in session.new
    assert unrelated.id is None


def test_pending_mapping_changes_are_rejected_without_autoflush(session):
    year, cash, _ = setup_year(session, "BATCH-PENDING")
    pending = MappingRule(
        year_id=year.id, rule_key="pending", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.add(pending)
    with pytest.raises(MappingValidationError, match="clean Session"):
        preview_mapping_batch(session, year_id=year.id, rows=[row("M!2", "cash", cash)])
    assert pending in session.new and pending.id is None


@pytest.mark.parametrize("bad", [
    (), None, "not rows", [123], [row("M!2", "x", type("N", (), {"id": 1})())] * 10_001,
])
def test_unusable_or_oversized_batch_rejected(session, bad):
    year, _, _ = setup_year(session, "BATCH-BAD")
    with pytest.raises(MappingValidationError):
        preview_mapping_batch(session, year_id=year.id, rows=bad)


def test_duplicate_source_locator_rejected(session):
    year, cash, _ = setup_year(session, "BATCH-LOCATOR")
    with pytest.raises(MappingValidationError, match="source locator"):
        preview_mapping_batch(session, year_id=year.id, rows=[
            row("M!2", "a", cash), row("M!2", "b", cash),
        ])


@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
def test_protected_year_batch_is_rejected(session, status):
    year, cash, _ = setup_year(session, "BATCH-" + status.value)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        year.status = status
        session.commit()
    with pytest.raises(MappingValidationError, match="Draft"):
        preview_mapping_batch(session, year_id=year.id, rows=[row("M!2", "cash", cash)])


def test_malformed_row_is_diagnostic_not_parser_crash(session):
    year, cash, _ = setup_year(session, "BATCH-MALFORMED")
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("M!2", "bad", cash, target_note_id=True),
        row("M!3", "good", cash),
    ])
    assert result.counts == {"invalid": 1, "new": 1}
    assert result.ready_for_review is False


def test_bool_target_id_cannot_coalesce_with_integer_id(session):
    year, cash, _ = setup_year(session, "BATCH-TYPE-ID")
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("M!2", "cash", cash),
        row("M!3", "cash", cash, target_note_id=True),
    ])
    assert [item.status for item in result.rows] == ["conflict", "conflict"]
    assert result.ready_for_review is False
    assert session.scalars(select(MappingRule)).all() == []


def test_bool_base_version_cannot_coalesce_with_integer_version(session):
    year, cash, other = setup_year(session, "BATCH-TYPE-VERSION")
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.commit()
    result = preview_mapping_batch(session, year_id=year.id, rows=[
        row("M!2", "cash", other, expected_base_version=1),
        row("M!3", "cash", other, expected_base_version=True),
    ])
    assert [item.status for item in result.rows] == ["conflict", "conflict"]
    assert result.ready_for_review is False


@pytest.mark.parametrize("locator", ["M!2\nM!3", "M!2\rM!3", "M!2\tsecret", "M!2\x00hidden"])
def test_control_characters_in_source_locator_are_rejected(session, locator):
    year, cash, _ = setup_year(session, "BATCH-CTRL")
    with pytest.raises(MappingValidationError, match="source locator"):
        preview_mapping_batch(session, year_id=year.id, rows=[
            row(locator, "cash", cash),
        ])


def test_verify_fresh_two_rule_batch_without_db_writes(session):
    year, cash, other = setup_year(session, "VERIFY-BASE")
    rows = (row("M!2", "cash", cash), row("M!3", "ar", other, account_code="002"))
    result = preview_mapping_batch(session, year_id=year.id, rows=rows)
    assert result.ready_for_review
    assert result.source_rows == rows
    assert verify_mapping_batch_current(session, result) is None
    assert session.scalars(select(MappingRule)).all() == []


def test_verify_rejects_version_change_after_initial_batch(session):
    year, cash, other = setup_year(session, "VERIFY-VERSION")
    rows = (row("M!2", "cash", cash),)
    original = preview_mapping_batch(session, year_id=year.id, rows=rows)
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=other.id, mapping_type="manual", version=1,
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_batch_current(session, original)


def test_verify_rejects_external_same_version_rule_update(session):
    year, cash, other = setup_year(session, "VERIFY-EXTERNAL-RULE")
    saved = save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.commit()
    original = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "cash", other, expected_base_version=1),
    ))
    with Session(session.get_bind(), expire_on_commit=False) as remote:
        remote.execute(update(MappingRule).where(MappingRule.id == saved.id).values(mapping_type="external"))
        remote.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_batch_current(session, original)


def test_verify_rejects_year_approval_after_batch(session):
    year, cash, _ = setup_year(session, "VERIFY-YEAR")
    original = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "cash", cash),
    ))
    with Session(session.get_bind(), expire_on_commit=False) as remote:
        remote.execute(update(FiscalYear).where(FiscalYear.id == year.id).values(
            status=FiscalYearStatus.APPROVED,
        ))
        remote.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_batch_current(session, original)


def test_verify_rejects_catalog_change_to_latest_note(session):
    year, cash, _ = setup_year(session, "VERIFY-NOTE")
    original = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "cash", cash),
    ))
    session.add(NoteDefinition(year_id=year.id, note_number="1", title="Updated", version=2))
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_batch_current(session, original)


def test_verify_rejects_changed_latest_account_even_for_noop_row(session):
    year, cash, other = setup_year(session, "VERIFY-NOOP-ACCOUNT")
    save_mapping_rule(
        session, year_id=year.id, rule_key="existing", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.commit()
    original = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "existing", cash, expected_base_version=1),
        row("M!3", "new", other),
    ))
    assert [item.status for item in original.rows] == ["unchanged", "new"]
    session.add(AccountVersion(
        year_id=year.id, account_code="001", account_name="Updated", version=2,
    ))
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_batch_current(session, original)


@pytest.mark.parametrize("tamper", ["source", "result", "fingerprint", "status", "year"])
def test_verify_rejects_modified_batch_evidence(session, tamper):
    year, cash, other = setup_year(session, "VERIFY-TAMPER")
    original = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "cash", cash),
    ))
    if tamper == "source":
        altered = replace(original, source_rows=(row("M!2", "cash", other),))
    elif tamper == "result":
        altered = replace(
            original, rows=(replace(original.rows[0], source_locator="M!999"),)
        )
    elif tamper == "fingerprint":
        altered = replace(original, fingerprint="0" * 64)
    elif tamper == "status":
        altered = replace(
            original, rows=(replace(original.rows[0], status="changed"),)
        )
    else:
        altered = replace(original, year_id=year.id + 1)
    with pytest.raises(MappingValidationError, match="stale|invalid"):
        verify_mapping_batch_current(session, altered)


def test_verify_refuses_conflicted_batch_even_when_snapshot_unchanged(session):
    year, cash, other = setup_year(session, "VERIFY-CONFLICT")
    snapshot = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "cash", cash), row("M!3", "cash", other),
    ))
    assert not snapshot.ready_for_review
    with pytest.raises(MappingValidationError, match="not ready"):
        verify_mapping_batch_current(session, snapshot)


def test_verify_refuses_all_noop_batch(session):
    year, cash, _ = setup_year(session, "VERIFY-NOOP")
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=cash.id, mapping_type="manual", version=1,
    )
    session.commit()
    original = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "cash", cash, expected_base_version=1),
    ))
    assert not original.ready_for_review
    with pytest.raises(MappingValidationError, match="not ready"):
        verify_mapping_batch_current(session, original)


def test_verify_does_not_autoflush_unrelated_pending_company(session):
    year, cash, _ = setup_year(session, "VERIFY-NOFLUSH")
    original = preview_mapping_batch(session, year_id=year.id, rows=(
        row("M!2", "cash", cash),
    ))
    company = Company(code="PENDING-RECHECK", name="Pending")
    session.add(company)
    verify_mapping_batch_current(session, original)
    assert company in session.new and company.id is None


def test_verify_rejects_non_batch_object(session):
    with pytest.raises(MappingValidationError, match="invalid"):
        verify_mapping_batch_current(session, {"year_id": 1})
