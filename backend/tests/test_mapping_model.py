import pytest
from aram_backend.models import MappingStatus, MappingRule, NoteDefinition, Company, FiscalYear

def make_year(session, year=1404):
    company = Company(code=f"CO-{year}", name="Test Company")
    fiscal_year = FiscalYear(company=company, year=year)
    session.add(company)
    session.commit()
    return fiscal_year

def test_mapping_status_default(session):
    year = make_year(session)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Assets", version=1)
    session.add(note)
    session.commit()

    mapping = MappingRule(
        year_id=year.id,
        rule_key="rule-1",
        account_code="1000",
        target_note_id=note.id,
        mapping_type="O"
    )
    session.add(mapping)
    session.commit()

    assert mapping.status == MappingStatus.DRAFT

def test_mapping_lifecycle_valid_transitions(session):
    year = make_year(session)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Assets", version=1)
    session.add(note)
    session.commit()

    mapping = MappingRule(
        year_id=year.id,
        rule_key="rule-1",
        account_code="1000",
        target_note_id=note.id,
        mapping_type="O"
    )
    session.add(mapping)
    session.commit()

    # Draft -> Proposed
    mapping.status = MappingStatus.PROPOSED
    session.commit()
    assert mapping.status == MappingStatus.PROPOSED

    # Proposed -> Active
    mapping.status = MappingStatus.ACTIVE
    session.commit()
    assert mapping.status == MappingStatus.ACTIVE

    # Active -> Retired
    mapping.status = MappingStatus.RETIRED
    session.commit()
    assert mapping.status == MappingStatus.RETIRED

def test_mapping_lifecycle_invalid_transition(session):
    year = make_year(session)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Assets", version=1)
    session.add(note)
    session.commit()

    mapping = MappingRule(
        year_id=year.id,
        rule_key="rule-1",
        account_code="1000",
        target_note_id=note.id,
        mapping_type="O"
    )
    session.add(mapping)
    session.commit()

    # Draft -> Active (invalid)
    mapping.status = MappingStatus.ACTIVE
    with pytest.raises(ValueError, match="Invalid mapping transition"):
        session.commit()
