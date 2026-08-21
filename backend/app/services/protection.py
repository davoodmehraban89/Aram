from sqlalchemy.orm import Session
from backend.app.models.entities import FiscalYear, FiscalYearStatus


class LockedFiscalYearError(Exception):
    """Raised when attempting to modify data associated with an Approved or Locked fiscal year."""
    def __init__(self, year: int, status: FiscalYearStatus):
        self.year = year
        self.status = status
        super().__init__(
            f"Cannot modify data for fiscal year {year} because its status is '{status.value}'. "
            "Data in Approved or Locked fiscal years is immutable."
        )


def check_fiscal_year_mutable(db: Session, year_id: int) -> FiscalYear:
    """
    Verifies if a fiscal year is mutable (i.e. status is Draft).
    If status is Approved or Locked, raises LockedFiscalYearError.
    """
    fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == year_id).first()
    if not fiscal_year:
        raise ValueError(f"FiscalYear with id {year_id} not found.")

    if fiscal_year.status in (FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED):
        raise LockedFiscalYearError(year=fiscal_year.year, status=fiscal_year.status)

    return fiscal_year
