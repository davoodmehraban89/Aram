import pytest
from sqlalchemy.exc import IntegrityError
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    AccountVersion,
    NoteDefinition,
    FinancialStatement,
    StatementType,
    SourceDocument,
)


def test_unique_company_code(db_session):
    c1 = Company(code="C1", name="Company One")
    db_session.add(c1)
    db_session.commit()

    c2 = Company(code="C1", name="Company Two")
    db_session.add(c2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_unique_company_fiscal_year(db_session):
    c = Company(code="C1", name="Company One")
    db_session.add(c)
    db_session.commit()

    fy1 = FiscalYear(company_id=c.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy1)
    db_session.commit()

    fy2 = FiscalYear(company_id=c.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_unique_year_account_code(db_session):
    c = Company(code="C1", name="Company One")
    db_session.add(c)
    db_session.commit()

    fy = FiscalYear(company_id=c.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    a1 = AccountVersion(year_id=fy.id, account_code="1001", account_name="Acc 1")
    a2 = AccountVersion(year_id=fy.id, account_code="1001", account_name="Acc 2")
    db_session.add_all([a1, a2])
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_fiscal_year_isolation(db_session):
    c = Company(code="C1", name="Company One")
    db_session.add(c)
    db_session.commit()

    fy1402 = FiscalYear(company_id=c.id, year=1402, status=FiscalYearStatus.LOCKED)
    fy1403 = FiscalYear(company_id=c.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    # Accounts with same code in different fiscal years should be allowed
    a1402 = AccountVersion(year_id=fy1402.id, account_code="1001", account_name="1402 Cash")
    a1403 = AccountVersion(year_id=fy1403.id, account_code="1001", account_name="1403 Cash")
    db_session.add_all([a1402, a1403])
    db_session.commit()

    assert a1402.year_id != a1403.year_id


def test_foreign_key_constraint(db_session):
    # Attempt to insert SourceDocument for non-existent year_id
    doc = SourceDocument(
        year_id=99999,
        filename="non_existent.xlsx",
        file_hash="dummy",
        doc_type="ledger",
    )
    db_session.add(doc)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
