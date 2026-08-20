import pytest
from sqlalchemy.exc import IntegrityError

from aram_backend.models import (
    AccountVersion,
    Company,
    FinancialStatement,
    FiscalYear,
    FiscalYearStatus,
    MappingRule,
    NoteDefinition,
    NoteRow,
    SourceDocument,
    StatementLine,
    StatementType,
)


def make_year(session, year=1404):
    company = Company(code=f"CO-{year}", name="Test Company")
    fiscal_year = FiscalYear(company=company, year=year)
    session.add(company)
    session.commit()
    return fiscal_year


def test_model_relationships(session):
    year = make_year(session)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Assets", version=1)
    note.rows.append(NoteRow(row_order=0, label="Tangible assets"))
    statement = FinancialStatement(year_id=year.id, statement_type=StatementType.BALANCE_SHEET)
    statement.lines.append(StatementLine(line_order=0, line_label="Assets", target_note=note))
    session.add_all([note, statement])
    session.commit()
    assert note.rows[0].note_id == note.id
    assert statement.lines[0].target_note_id == note.id


def test_version_uniqueness(session):
    year = make_year(session)
    session.add(AccountVersion(year_id=year.id, account_code="1000", account_name="Cash", version=1))
    session.commit()
    session.add(AccountVersion(year_id=year.id, account_code="1000", account_name="Cash duplicate", version=1))
    with pytest.raises(IntegrityError):
        session.commit()


def test_source_document_hash_unique_within_year(session):
    year = make_year(session)
    session.add(SourceDocument(year_id=year.id, filename="a.xlsx", file_hash="abc", document_type="ledger"))
    session.commit()
    session.add(SourceDocument(year_id=year.id, filename="b.xlsx", file_hash="abc", document_type="ledger"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_fiscal_year_isolation_for_mapping(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Assets")
    session.add(note)
    session.commit()
    session.add(MappingRule(
        year_id=second.id, rule_key="rule-1", account_code="1000",
        target_note=note, mapping_type="O"
    ))
    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()


def test_locked_year_blocks_mutation(session):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    year.status = FiscalYearStatus.LOCKED
    session.commit()
    session.add(AccountVersion(year_id=year.id, account_code="1000", account_name="Cash"))
    with pytest.raises(ValueError, match="locked"):
        session.commit()


def test_approved_year_blocks_silent_overwrite(session):
    year = make_year(session)
    account = AccountVersion(
        year_id=year.id, account_code="1000", account_name="Cash"
    )
    session.add(account)
    session.commit()
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    account.account_name = "Silently changed cash"
    with pytest.raises(ValueError, match="approved"):
        session.commit()


def test_locked_year_cannot_be_reopened(session):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    year.status = FiscalYearStatus.LOCKED
    session.commit()
    year.status = FiscalYearStatus.DRAFT
    with pytest.raises(ValueError, match="Invalid fiscal-year transition"):
        session.commit()


def test_invalid_status_skip_is_rejected(session):
    year = make_year(session)
    year.status = FiscalYearStatus.LOCKED
    with pytest.raises(ValueError, match="Invalid fiscal-year transition"):
        session.commit()
