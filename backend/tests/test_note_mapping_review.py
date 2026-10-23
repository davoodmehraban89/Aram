import pytest

from aram_backend.note_mapping_review import review_note_mappings
from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import AccountVersion, Company, FiscalYear, MappingRule, NoteDefinition


def setup(session):
    company = Company(code="NOTE", name="Test")
    year = FiscalYear(company=company, year=1404)
    session.add(company)
    session.flush()
    account = AccountVersion(year_id=year.id, account_code="001", account_name="Cash", version=1)
    notes = [NoteDefinition(year_id=year.id, note_number=str(n), title=str(n), version=1) for n in (1, 2)]
    session.add_all([account, *notes])
    session.commit()
    return year, account, notes


def rule(session, year, note, key="cash", version=1):
    session.add(MappingRule(year_id=year.id, rule_key=key, version=version,
                            account_code="001", target_note_id=note.id, mapping_type="direct"))


def test_unmapped_and_mapped(session):
    year, _, notes = setup(session)
    assert review_note_mappings(session, year_id=year.id).unmapped_account_codes == ("001",)
    rule(session, year, notes[0])
    session.commit()
    result = review_note_mappings(session, year_id=year.id)
    assert result.notes[0].account_codes == ("001",)
    assert result.unmapped_account_codes == ()


def test_ambiguity(session):
    year, _, notes = setup(session)
    rule(session, year, notes[0], "a")
    rule(session, year, notes[1], "b")
    session.commit()
    result = review_note_mappings(session, year_id=year.id)
    assert all(note.ambiguous_account_codes == ("001",) for note in result.notes)
    assert all(not note.account_codes for note in result.notes)


def test_latest_rule_version(session):
    year, _, notes = setup(session)
    rule(session, year, notes[0], version=1)
    rule(session, year, notes[1], version=2)
    session.commit()
    result = review_note_mappings(session, year_id=year.id)
    assert result.notes[1].account_codes == ("001",)


def test_stale_note_version(session):
    year, _, notes = setup(session)
    rule(session, year, notes[0])
    session.add(NoteDefinition(year_id=year.id, note_number="1", title="Updated", version=2))
    session.commit()
    result = review_note_mappings(session, year_id=year.id)
    assert result.stale_note_rule_keys == ("cash",)
    assert result.unmapped_account_codes == ("001",)


@pytest.mark.parametrize("value", [0, -1, True, False, "1", 99999])
def test_invalid_year(session, value):
    with pytest.raises(MappingValidationError):
        review_note_mappings(session, year_id=value)


def test_does_not_autoflush(session):
    year, _, _ = setup(session)
    pending = AccountVersion(year_id=year.id, account_code="002", account_name="Pending", version=1)
    session.add(pending)
    review_note_mappings(session, year_id=year.id)
    assert pending in session.new and pending.id is None
