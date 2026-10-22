import pytest

from aram_backend.mapping_coverage import inspect_mapping_coverage
from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import (
    AccountVersion, Company, FiscalYear, MappingRule, NoteDefinition,
)


def year_with_accounts(session, code, codes=("001", "002", "003")):
    company = Company(code=code, name="Coverage test")
    year = FiscalYear(company=company, year=1404)
    session.add(year)
    session.flush()
    for account_code in codes:
        session.add(AccountVersion(year_id=year.id, account_code=account_code,
                                   account_name=account_code, version=1))
    notes = [NoteDefinition(year_id=year.id, note_number=str(i), title=str(i), version=1)
             for i in (1, 2)]
    session.add_all(notes)
    session.commit()
    return year, notes


def rule(session, year, key, code, note_id, version=1):
    session.add(MappingRule(year_id=year.id, rule_key=key, account_code=code,
                            target_note_id=note_id, mapping_type="direct", version=version))


def test_empty_queue_without_mappings(session):
    year, _ = year_with_accounts(session, "COVER-A")
    coverage = inspect_mapping_coverage(session, year_id=year.id)
    assert coverage.total_accounts == 3
    assert coverage.mapped_accounts == ()
    assert coverage.unmapped_accounts == ("001", "002", "003")
    assert coverage.ambiguous_accounts == ()


def test_mapped_and_ambiguous_queues(session):
    year, notes = year_with_accounts(session, "COVER-B")
    rule(session, year, "a", "001", notes[0].id)
    rule(session, year, "b", "002", notes[0].id)
    rule(session, year, "c", "002", notes[1].id)
    session.commit()
    coverage = inspect_mapping_coverage(session, year_id=year.id)
    assert coverage.mapped_accounts == ("001",)
    assert coverage.ambiguous_accounts == ("002",)
    assert coverage.unmapped_accounts == ("003",)
    assert coverage.total_accounts == 3


def test_multiple_rules_same_note_are_not_ambiguous(session):
    year, notes = year_with_accounts(session, "COVER-C", ("001",))
    rule(session, year, "a", "001", notes[0].id)
    rule(session, year, "b", "001", notes[0].id)
    session.commit()
    assert inspect_mapping_coverage(session, year_id=year.id).mapped_accounts == ("001",)


def test_latest_rule_version_supersedes_prior_version(session):
    year, notes = year_with_accounts(session, "COVER-D", ("001",))
    rule(session, year, "a", "001", notes[0].id, version=1)
    rule(session, year, "a", "001", notes[1].id, version=2)
    session.commit()
    coverage = inspect_mapping_coverage(session, year_id=year.id)
    assert coverage.mapped_accounts == ("001",)
    assert coverage.ambiguous_accounts == ()


def test_latest_account_version_counted_once(session):
    year, _ = year_with_accounts(session, "COVER-E", ("001",))
    session.add(AccountVersion(year_id=year.id, account_code="001", account_name="Updated", version=2))
    session.commit()
    coverage = inspect_mapping_coverage(session, year_id=year.id)
    assert coverage.total_accounts == 1
    assert coverage.unmapped_accounts == ("001",)


def test_orphan_rule_and_cross_year_isolation(session):
    year, notes = year_with_accounts(session, "COVER-F", ("001",))
    other, other_notes = year_with_accounts(session, "COVER-G", ("001",))
    rule(session, year, "orphan", "999", notes[0].id)
    rule(session, other, "other", "001", other_notes[0].id)
    session.commit()
    coverage = inspect_mapping_coverage(session, year_id=year.id)
    assert coverage.orphan_rule_keys == ("orphan",)
    assert coverage.unmapped_accounts == ("001",)
    assert coverage.mapped_accounts == ()


@pytest.mark.parametrize("year_id", [0, -1, True, "1", None, 99999])
def test_invalid_or_unknown_year_rejected(session, year_id):
    with pytest.raises(MappingValidationError):
        inspect_mapping_coverage(session, year_id=year_id)


def test_coverage_does_not_change_rows(session):
    year, notes = year_with_accounts(session, "COVER-H")
    rule(session, year, "a", "001", notes[0].id)
    session.commit()
    before = session.query(MappingRule).count()
    inspect_mapping_coverage(session, year_id=year.id)
    assert session.query(MappingRule).count() == before
