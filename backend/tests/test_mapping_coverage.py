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


def test_diagnostic_does_not_flush_pending_unrelated_writes(session):
    year, _ = year_with_accounts(session, "COVER-I", ("001",))
    pending = AccountVersion(year_id=year.id, account_code="PENDING", account_name="Pending", version=1)
    session.add(pending)
    coverage = inspect_mapping_coverage(session, year_id=year.id)
    assert pending in session.new
    assert pending.id is None
    assert coverage.total_accounts == 1
    assert coverage.unmapped_accounts == ("001",)


def test_stale_same_year_note_is_not_counted_as_mapped(session):
    year, notes = year_with_accounts(session, "STALE-A", ("001",))
    rule(session, year, "old_note", "001", notes[0].id)
    session.add(NoteDefinition(
        year_id=year.id, note_number=notes[0].note_number,
        title="Current version", version=2,
    ))
    session.commit()

    result = inspect_mapping_coverage(session, year_id=year.id)

    assert result.mapped_accounts == ()
    assert result.unmapped_accounts == ("001",)
    assert result.invalid_target_rules == (("old_note", "001", "target_note_stale"),)


def test_cross_year_note_target_is_not_counted_as_mapped(session):
    from sqlalchemy import update

    year, notes = year_with_accounts(session, "FOREIGN-A", ("001",))
    foreign, foreign_notes = year_with_accounts(session, "FOREIGN-B", ("001",))
    rule(session, year, "foreign", "001", notes[0].id)
    session.commit()
    # This is intentionally an ORM event bypass via SQLAlchemy Core SQL.
    session.execute(
        update(MappingRule)
        .where(MappingRule.year_id == year.id, MappingRule.rule_key == "foreign")
        .values(target_note_id=foreign_notes[0].id)
    )
    session.commit()
    session.expire_all()

    result = inspect_mapping_coverage(session, year_id=year.id)

    assert result.mapped_accounts == ()
    assert result.unmapped_accounts == ("001",)
    assert result.invalid_target_rules == (("foreign", "001", "target_note_wrong_year"),)


def test_one_valid_and_one_stale_rule_does_not_count_as_clean_mapping(session):
    year, notes = year_with_accounts(session, "MIXED-A", ("001",))
    rule(session, year, "valid", "001", notes[1].id)
    rule(session, year, "stale", "001", notes[0].id)
    session.add(NoteDefinition(
        year_id=year.id, note_number=notes[0].note_number,
        title="Current version", version=2,
    ))
    session.commit()

    result = inspect_mapping_coverage(session, year_id=year.id)

    assert result.mapped_accounts == ()
    assert result.unmapped_accounts == ("001",)
    assert result.ambiguous_accounts == ()
    assert result.invalid_target_rules == (("stale", "001", "target_note_stale"),)


def test_latest_note_version_target_is_clean_and_read_only(session):
    year, notes = year_with_accounts(session, "LATEST-A", ("001",))
    current = NoteDefinition(year_id=year.id, note_number=notes[0].note_number, title="Current", version=2)
    session.add(current)
    session.flush()
    rule(session, year, "ok", "001", current.id)
    session.commit()

    pending = AccountVersion(year_id=year.id, account_code="X", account_name="Pending", version=1)
    session.add(pending)
    result = inspect_mapping_coverage(session, year_id=year.id)

    assert result.mapped_accounts == ("001",)
    assert result.invalid_target_rules == ()
    assert pending in session.new
    assert pending.id is None
