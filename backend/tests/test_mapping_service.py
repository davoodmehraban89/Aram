import pytest
from aram_backend.models import (
    MappingStatus, MappingRule, NoteDefinition, Company, FiscalYear, AccountVersion, FiscalYearStatus
)
from aram_backend.mapping import create_mapping_rule, MappingValidationError

def make_year(session, year=1404):
    company = Company(code=f"CO-{year}", name="Test Company")
    fiscal_year = FiscalYear(company=company, year=year)
    session.add(company)
    session.commit()
    return fiscal_year

def setup_basic_mapping_data(session):
    year = make_year(session)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Assets", version=1)
    account = AccountVersion(year_id=year.id, account_code="1000", account_name="Cash", version=1)
    session.add_all([note, account])
    session.commit()
    return year, note, account

def test_create_mapping_rule_valid(session):
    year, note, account = setup_basic_mapping_data(session)

    mapping = create_mapping_rule(
        session,
        year_id=year.id,
        rule_key="rule-1",
        account_code="1000",
        target_note_id=note.id,
        mapping_type="O"
    )

    assert mapping.id is not None
    assert mapping.rule_key == "rule-1"
    assert mapping.account_code == "1000"
    assert mapping.status == MappingStatus.DRAFT

def test_create_mapping_rule_invalid_year(session):
    year, note, account = setup_basic_mapping_data(session)

    with pytest.raises(MappingValidationError, match="Fiscal year 9999 does not exist"):
        create_mapping_rule(
            session,
            year_id=9999,
            rule_key="rule-1",
            account_code="1000",
            target_note_id=note.id,
            mapping_type="O"
        )

def test_create_mapping_rule_invalid_account(session):
    year, note, account = setup_basic_mapping_data(session)

    with pytest.raises(MappingValidationError, match="Account 9999 does not exist"):
        create_mapping_rule(
            session,
            year_id=year.id,
            rule_key="rule-1",
            account_code="9999",
            target_note_id=note.id,
            mapping_type="O"
        )

def test_create_mapping_rule_invalid_note(session):
    year, note, account = setup_basic_mapping_data(session)

    with pytest.raises(MappingValidationError, match="Target note 9999 is invalid"):
        create_mapping_rule(
            session,
            year_id=year.id,
            rule_key="rule-1",
            account_code="1000",
            target_note_id=9999,
            mapping_type="O"
        )

def test_create_mapping_rule_duplicate(session):
    year, note, account = setup_basic_mapping_data(session)

    create_mapping_rule(
        session,
        year_id=year.id,
        rule_key="rule-1",
        account_code="1000",
        target_note_id=note.id,
        mapping_type="O"
    )

    with pytest.raises(MappingValidationError, match="Mapping rule rule-1 version 1 already exists"):
        create_mapping_rule(
            session,
            year_id=year.id,
            rule_key="rule-1",
            account_code="1000",
            target_note_id=note.id,
            mapping_type="O"
        )

def test_create_mapping_rule_locked_year(session):
    year, note, account = setup_basic_mapping_data(session)

    year.status = FiscalYearStatus.APPROVED
    session.commit()

    with pytest.raises(MappingValidationError, match="is approved and cannot accept mapping changes"):
        create_mapping_rule(
            session,
            year_id=year.id,
            rule_key="rule-1",
            account_code="1000",
            target_note_id=note.id,
            mapping_type="O"
        )
