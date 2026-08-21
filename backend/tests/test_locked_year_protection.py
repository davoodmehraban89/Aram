import pytest
from backend.app.models import Company, FiscalYear, FiscalYearStatus
from backend.app.services.protection import check_fiscal_year_mutable, LockedFiscalYearError


def test_draft_fiscal_year_is_mutable(db_session):
    company = Company(code="C_MUTE", name="Mutable Test Corp")
    db_session.add(company)
    db_session.commit()

    fy = FiscalYear(company_id=company.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    # Checking mutability should succeed and return the fiscal year object
    verified_fy = check_fiscal_year_mutable(db_session, fy.id)
    assert verified_fy.id == fy.id
    assert verified_fy.status == FiscalYearStatus.DRAFT


def test_approved_fiscal_year_raises_error(db_session):
    company = Company(code="C_APP", name="Approved Test Corp")
    db_session.add(company)
    db_session.commit()

    fy = FiscalYear(company_id=company.id, year=1402, status=FiscalYearStatus.APPROVED)
    db_session.add(fy)
    db_session.commit()

    with pytest.raises(LockedFiscalYearError) as exc_info:
        check_fiscal_year_mutable(db_session, fy.id)

    assert "1402" in str(exc_info.value)
    assert "Approved" in str(exc_info.value)


def test_locked_fiscal_year_raises_error(db_session):
    company = Company(code="C_LOCK", name="Locked Test Corp")
    db_session.add(company)
    db_session.commit()

    fy = FiscalYear(company_id=company.id, year=1402, status=FiscalYearStatus.LOCKED)
    db_session.add(fy)
    db_session.commit()

    with pytest.raises(LockedFiscalYearError) as exc_info:
        check_fiscal_year_mutable(db_session, fy.id)

    assert "1402" in str(exc_info.value)
    assert "Locked" in str(exc_info.value)
