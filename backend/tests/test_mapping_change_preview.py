"""Synthetic read-only Mapping decision previews; NOT an approval workflow."""
from dataclasses import replace

import pytest
from sqlalchemy import select

from aram_backend.mapping_change_preview import (
    MappingChangePreview, preview_mapping_change, verify_mapping_change_preview_current,
)
from aram_backend.mapping_service import MappingValidationError, save_mapping_rule
from aram_backend.models import (
    AccountVersion, Company, FiscalYear, FiscalYearStatus, MappingRule, NoteDefinition,
)


def setup_year(session, company_code="PREVIEW-A", year_number=1404):
    company = Company(code=company_code, name="Synthetic accounting")
    year = FiscalYear(company=company, year=year_number)
    session.add(year)
    session.flush()
    old_note = NoteDefinition(year_id=year.id, note_number="1", title="Cash", version=1)
    other_note = NoteDefinition(year_id=year.id, note_number="2", title="Receivables", version=1)
    account = AccountVersion(year_id=year.id, account_code="001", account_name="Cash", version=1)
    session.add_all([old_note, other_note, account])
    session.commit()
    return year, old_note, other_note


def preview(session, year, note, **kw):
    data = dict(
        year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=note.id, mapping_type="direct", expected_base_version=0,
    )
    data.update(kw)
    return preview_mapping_change(session, **data)


def test_new_rule_preview_shows_version_one_without_persisting(session):
    year, note, _ = setup_year(session)
    before = session.scalars(select(MappingRule)).all()
    result = preview(session, year, note)

    assert isinstance(result, MappingChangePreview)
    assert result.before is None
    assert result.expected_base_version == 0
    assert result.proposed.version == 1
    assert result.proposed.target_note_id == note.id
    assert result.company_id == year.company_id
    assert result.fiscal_year_number == year.year
    assert len(result.fingerprint) == 64
    assert session.scalars(select(MappingRule)).all() == before == []
    verify_mapping_change_preview_current(session, result)


def test_change_preview_shows_explicit_old_new_and_is_deterministic(session):
    year, old_note, new_note = setup_year(session, "PREVIEW-B")
    saved = save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=old_note.id, mapping_type="direct", version=1,
    )
    session.commit()

    result = preview(
        session, year, new_note, mapping_type="manual", expected_base_version=1,
    )
    again = preview(
        session, year, new_note, mapping_type="manual", expected_base_version=1,
    )
    assert result == again
    assert result.before is not None
    assert result.before.id == saved.id
    assert result.before.version == 1
    assert result.before.target_note_id == old_note.id
    assert result.proposed.version == 2
    assert result.proposed.target_note_id == new_note.id
    assert result.proposed.mapping_type == "manual"
    assert session.scalars(select(MappingRule)).all() == [saved]
    verify_mapping_change_preview_current(session, result)


def test_reject_noop_reconfirmation_instead_of_faking_review(session):
    year, note, _ = setup_year(session, "PREVIEW-C")
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=note.id, mapping_type="direct",
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="no mapping change"):
        preview(session, year, note, expected_base_version=1)


def test_stale_precondition_rejected_even_if_target_is_valid(session):
    year, note, other_note = setup_year(session, "PREVIEW-D")
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=note.id, mapping_type="direct",
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="stale base"):
        preview(session, year, other_note, expected_base_version=0)
    with pytest.raises(MappingValidationError, match="stale base"):
        preview(session, year, other_note, expected_base_version=2)


def test_verify_rejects_later_mapping_version_without_mutation(session):
    year, note, other = setup_year(session, "PREVIEW-E")
    current = preview(session, year, note)
    save_mapping_rule(
        session, year_id=year.id, rule_key="cash", account_code="001",
        target_note_id=other.id, mapping_type="manual",
    )
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_change_preview_current(session, current)
    assert session.scalar(select(MappingRule)).target_note_id == other.id


def test_verify_rejects_later_note_version(session):
    year, note, _ = setup_year(session, "PREVIEW-F")
    current = preview(session, year, note)
    session.add(NoteDefinition(
        year_id=year.id, note_number="1", title="Revised", version=2,
    ))
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_change_preview_current(session, current)
    assert session.scalars(select(MappingRule)).all() == []


def test_verify_rejects_updated_account_version_even_when_code_is_unchanged(session):
    year, note, _ = setup_year(session, "PREVIEW-G")
    current = preview(session, year, note)
    session.add(AccountVersion(
        year_id=year.id, account_code="001", account_name="Updated", version=2,
    ))
    session.commit()
    with pytest.raises(MappingValidationError, match="stale"):
        verify_mapping_change_preview_current(session, current)
    assert session.scalars(select(MappingRule)).all() == []


@pytest.mark.parametrize("changed", [
    ("mapping_type", "manual"),
    ("fingerprint", "0" * 64),
    ("company_id", 1000000),
    ("expected_base_version", 1),
])
def test_verify_rejects_forged_or_modified_preview(session, changed):
    year, note, _ = setup_year(session, "PREVIEW-FORGE")
    original = preview(session, year, note)
    key, value = changed
    if key == "mapping_type":
        altered = replace(original, proposed=replace(original.proposed, mapping_type=value))
    else:
        altered = replace(original, **{key: value})
    with pytest.raises(MappingValidationError, match="stale|altered"):
        verify_mapping_change_preview_current(session, altered)


def test_fiscal_year_protection_and_foreign_year_note(session):
    year, note, _ = setup_year(session, "PREVIEW-H")
    other_year, foreign_note, _ = setup_year(session, "PREVIEW-I")
    with pytest.raises(MappingValidationError, match="same fiscal year"):
        preview(session, year, foreign_note)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    with pytest.raises(MappingValidationError, match="Draft"):
        preview(session, year, note)


@pytest.mark.parametrize("override", [
    {"year_id": 0}, {"year_id": True}, {"rule_key": ""}, {"rule_key": "x "},
    {"account_code": 10}, {"account_code": "missing"},
    {"target_note_id": True}, {"target_note_id": -1},
    {"mapping_type": ""}, {"mapping_type": "x" * 33},
    {"expected_base_version": -1}, {"expected_base_version": False},
])
def test_preview_rejects_invalid_input(session, override):
    year, note, _ = setup_year(session, "PREVIEW-INPUT")
    with pytest.raises(MappingValidationError):
        preview(session, year, note, **override)


def test_pending_related_edits_fail_closed_without_autoflush(session):
    year, note, _ = setup_year(session, "PREVIEW-PENDING")
    pending = AccountVersion(
        year_id=year.id, account_code="PENDING", account_name="Uncommitted", version=1,
    )
    session.add(pending)
    with pytest.raises(MappingValidationError, match="clean Session"):
        preview(session, year, note)
    assert pending in session.new
    assert pending.id is None


def test_unrelated_pending_company_is_not_flushed(session):
    year, note, _ = setup_year(session, "PREVIEW-UNRELATED")
    unrelated = Company(code="UNCOMMITTED", name="Uncommitted company")
    session.add(unrelated)
    result = preview(session, year, note)
    assert result.proposed.version == 1
    assert unrelated in session.new
    assert unrelated.id is None
    verify_mapping_change_preview_current(session, result)


def test_preview_never_commits_even_when_explicitly_verified(session):
    year, note, _ = setup_year(session, "PREVIEW-READONLY")
    original = preview(session, year, note)
    verify_mapping_change_preview_current(session, original)
    session.rollback()
    assert session.scalars(select(MappingRule)).all() == []
