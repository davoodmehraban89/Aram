import pytest
from sqlalchemy import select

from aram_backend.mapping_service import MappingValidationError, save_mapping_rule
from aram_backend.models import (
    AccountVersion, Company, FiscalYear, FiscalYearStatus, MappingRule, NoteDefinition,
)


def setup_year(session, company_code, year_number=1404):
    company = Company(code=company_code, name="Test")
    year = FiscalYear(company=company, year=year_number)
    session.add(company)
    session.flush()
    account = AccountVersion(year_id=year.id, account_code="001", account_name="Cash", version=1)
    note = NoteDefinition(year_id=year.id, note_number="1", title="Cash", version=1)
    session.add_all([account, note])
    session.commit()
    return year, note


def arguments(year, note):
    return dict(year_id=year.id, rule_key="cash-note", account_code="001",
                target_note_id=note.id, mapping_type="direct", version=1)


def test_create_and_idempotent_replay(session):
    year, note = setup_year(session, "MAP-A")
    first = save_mapping_rule(session, **arguments(year, note))
    session.commit()
    second = save_mapping_rule(session, **arguments(year, note))
    assert first.id == second.id
    assert len(session.scalars(select(MappingRule)).all()) == 1


def test_conflicting_version_is_rejected_without_new_rows(session):
    year, note = setup_year(session, "MAP-B")
    save_mapping_rule(session, **arguments(year, note))
    session.commit()
    with pytest.raises(MappingValidationError, match="conflicts"):
        save_mapping_rule(session, **(arguments(year, note) | {"mapping_type": "manual"}))
    assert len(session.scalars(select(MappingRule)).all()) == 1


def test_different_version_can_be_recorded(session):
    year, note = setup_year(session, "MAP-C")
    save_mapping_rule(session, **arguments(year, note))
    save_mapping_rule(session, **(arguments(year, note) | {"version": 2}))
    session.commit()
    assert len(session.scalars(select(MappingRule)).all()) == 2


def test_reject_cross_year_note_and_unknown_account(session):
    year, note = setup_year(session, "MAP-D")
    other_year, other_note = setup_year(session, "MAP-E")
    with pytest.raises(MappingValidationError, match="same fiscal year"):
        save_mapping_rule(session, **(arguments(year, note) | {"target_note_id": other_note.id}))
    with pytest.raises(MappingValidationError, match="account code"):
        save_mapping_rule(session, **(arguments(year, note) | {"account_code": "999"}))
    assert session.scalars(select(MappingRule)).all() == []


@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
def test_protected_year_rejected(session, status):
    year, note = setup_year(session, "MAP-" + status.value)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        year.status = FiscalYearStatus.LOCKED
        session.commit()
    with pytest.raises(MappingValidationError, match="Draft"):
        save_mapping_rule(session, **arguments(year, note))


@pytest.mark.parametrize("override", [
    {"year_id": 0}, {"year_id": True}, {"version": 0}, {"version": True},
    {"rule_key": ""}, {"rule_key": " leading"}, {"rule_key": "x" * 129},
    {"account_code": " "}, {"account_code": "x" * 65},
    {"mapping_type": ""}, {"mapping_type": "x" * 33},
    {"target_note_id": -1}, {"target_note_id": True},
])
def test_reject_invalid_input(session, override):
    year, note = setup_year(session, "MAP-VALIDATION")
    with pytest.raises(MappingValidationError):
        save_mapping_rule(session, **(arguments(year, note) | override))
    assert session.scalars(select(MappingRule)).all() == []


def test_caller_controls_commit_and_rollback(session):
    year, note = setup_year(session, "MAP-ROLLBACK")
    save_mapping_rule(session, **arguments(year, note))
    session.rollback()
    assert session.scalars(select(MappingRule)).all() == []
