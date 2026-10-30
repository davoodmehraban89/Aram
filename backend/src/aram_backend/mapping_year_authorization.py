"""Company/year/role authorization preflight for signed Mapping JWT scopes.

An issuer-signed identity is not enough: permission is the intersection of a
specific signed grant with the current FiscalYear/Company database boundary.
This is read-only and NOT finance approval, an actor-directory authorization
replacement, or a race-free apply permission.
"""
from __future__ import annotations

from time import time

from fastapi import HTTPException
from sqlalchemy.orm import Session

from aram_backend.authenticated_identity import (
    SignedYearScope, TRUSTED_ROLES, VerifiedPrincipal,
)
from aram_backend.models import Company, FiscalYear, FiscalYearStatus


def _deny() -> None:
    # Keep foreign-company/year and missing-year responses indistinguishable.
    raise HTTPException(status_code=403, detail="Mapping year access denied")


def require_year_access(
    session: Session, *, principal: VerifiedPrincipal, year_id: int,
    required_role: str,
) -> SignedYearScope:
    """Require a matching signed grant for the *currently Draft* year.

    Call only after FastAPI's verified RSA-bearer dependency. A caller-created
    Python VerifiedPrincipal object is NOT an authentication mechanism.
    Every eventual staging/approval API must enforce this preflight inside
    its trusted request handler AND repeat checks in its write transaction.
    """
    if (
        not isinstance(principal, VerifiedPrincipal)
        or type(year_id) is not int or year_id <= 0
        or type(required_role) is not str or required_role not in TRUSTED_ROLES
        or required_role not in principal.roles
        or type(principal.expires_at) is not int
        or principal.expires_at <= int(time())
    ):
        _deny()

    with session.no_autoflush:
        # Related pending edits might describe a different fiscal boundary.
        if any(
            isinstance(item, (FiscalYear, Company))
            for item in session.new | session.dirty | session.deleted
        ):
            _deny()
        year = session.get(FiscalYear, year_id, populate_existing=True)
        if year is None or year.status is not FiscalYearStatus.DRAFT:
            _deny()
        company = session.get(Company, year.company_id, populate_existing=True)
        if company is None:
            _deny()
        allowed = SignedYearScope(
            company_code=company.code, fiscal_year=year.year,
            role=required_role,
        )
        if allowed not in principal.year_scopes:
            _deny()
        return allowed
