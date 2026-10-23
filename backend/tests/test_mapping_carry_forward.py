import pytest
from sqlalchemy import select

from aram_backend.mapping_carry_forward import preview_mapping_carry_forward
from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import (
    AccountVersion, Company, FiscalYear, FiscalYearStatus, MappingRule, NoteDefinition,
)


def make_year(session, company, year, accounts=("001",), note_numbers=("1",)):
    fiscal = FiscalYear(company=company, year=year)
    session.add(fiscal)
    session.flush()
    for code in accounts:
        session.add(AccountVersion(year_id=fiscal.id, account_code=code, account_name=code, version=1))
    notes = []
    for number in note_numbers:
        note = NoteDefinition(year_id=fiscal.id, note_number=number, title=number, version=1)
        session.add(note)
        notes.append(note)
    session.flush()
    return fiscal, notes


def fixture_years(session, target_accounts=("001",), target_notes=("1",)):
    company = Company(code="CF-A", name="Carry forward")
    source, old_notes = make_year(session, company, 1403)
    target, new_notes = make_year(session, company, 1404, target_accounts, target_notes)
    session.add(MappingRule(year_id=source.id, rule_key="cash", account_code="001",
                            target_note_id=old_notes[0].id, mapping_type="direct", version=1))
    session.commit()
    return source, target, old_notes, new_notes


def test_valid_preview_is_read_only(session):
    source, target, _, notes = fixture_years(session)
    before = session.scalars(select(MappingRule)).all()
    result = preview_mapping_carry_forward(session, source_year_id=source.id, target_year_id=target.id)
    assert len(result.candidates) == 1
    assert result.candidates[0].target_note_id == notes[0].id
    assert result.candidates[0].source_note_number == "1"
    assert result.skipped == ()
    assert session.scalars(select(MappingRule)).all() == before


@pytest.mark.parametrize("accounts,notes,reason", [
    ((), ("1",), "target_account_missing"),
    (("001",), ("2",), "target_note_missing"),
])
def test_missing_reference_skipped(session, accounts, notes, reason):
    source, target, _, _ = fixture_years(session, accounts, notes)
    result = preview_mapping_carry_forward(session, source_year_id=source.id, target_year_id=target.id)
    assert result.candidates == ()
    assert result.skipped == (("cash", reason),)


def test_existing_target_rule_is_not_overwritten(session):
    source, target, _, notes = fixture_years(session)
    session.add(MappingRule(year_id=target.id, rule_key="cash", account_code="001",
                            target_note_id=notes[0].id, mapping_type="manual", version=1))
    session.commit()
    result = preview_mapping_carry_forward(session, source_year_id=source.id, target_year_id=target.id)
    assert result.skipped == (("cash", "target_rule_exists"),)


def test_latest_source_rule_and_target_note_versions(session):
    source, target, old_notes, new_notes = fixture_years(session)
    session.add(NoteDefinition(year_id=target.id, note_number="1", title="Updated", version=2))
    session.add(MappingRule(year_id=source.id, rule_key="cash", account_code="001",
                            target_note_id=old_notes[0].id, mapping_type="manual", version=2))
    session.commit()
    result = preview_mapping_carry_forward(session, source_year_id=source.id, target_year_id=target.id)
    assert result.candidates[0].source_version == 2
    assert result.candidates[0].mapping_type == "manual"
    assert result.candidates[0].target_note_id != new_notes[0].id


def test_protected_target_rejected(session):
    source, target, _, _ = fixture_years(session)
    target.status = FiscalYearStatus.APPROVED
    session.commit()
    with pytest.raises(MappingValidationError, match="Draft"):
        preview_mapping_carry_forward(session, source_year_id=source.id, target_year_id=target.id)


def test_different_company_rejected(session):
    source, target, _, _ = fixture_years(session)
    other = Company(code="CF-B", name="Other")
    other_year, _ = make_year(session, other, 1405)
    session.commit()
    with pytest.raises(MappingValidationError, match="same company"):
        preview_mapping_carry_forward(session, source_year_id=source.id, target_year_id=other_year.id)


@pytest.mark.parametrize("source_id,target_id", [(0, 1), (True, 1), (1, False), ("1", 2), (1, 1), (99999, 100000)])
def test_invalid_year_inputs_rejected(session, source_id, target_id):
    with pytest.raises(MappingValidationError):
        preview_mapping_carry_forward(session, source_year_id=source_id, target_year_id=target_id)


def test_reverse_year_order_rejected(session):
    source, target, _, _ = fixture_years(session)
    with pytest.raises(MappingValidationError, match="later"):
        preview_mapping_carry_forward(session, source_year_id=target.id, target_year_id=source.id)


def test_preview_does_not_autoflush_unrelated_changes(session):
    source, target, _, _ = fixture_years(session)
    pending = AccountVersion(year_id=target.id, account_code="NEW", account_name="Pending", version=1)
    session.add(pending)
    preview_mapping_carry_forward(session, source_year_id=source.id, target_year_id=target.id)
    assert pending in session.new
    assert pending.id is None
