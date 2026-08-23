from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models.entities import StatementSnapshot, ReviewStatus
from backend.app.services.protection import check_fiscal_year_mutable
from backend.app.accounting.service import generate_financial_statements
from backend.app.accounting.rules import AccountingRuleConfig


def create_statement_snapshot(
    db: Session,
    year_id: int,
    notes: Optional[str] = None,
    created_by: Optional[str] = None,
    rule_config: Optional[AccountingRuleConfig] = None,
) -> StatementSnapshot:
    """
    Generates financial statement calculations from normalized records,
    determines next version number for year_id, and persists a StatementSnapshot.
    Enforces fiscal year mutability protection.
    """
    check_fiscal_year_mutable(db, year_id)

    # Compute latest version number for year_id
    max_ver = (
        db.query(func.max(StatementSnapshot.version))
        .filter(StatementSnapshot.year_id == year_id)
        .scalar()
    )
    next_ver = (max_ver or 0) + 1

    # Generate frozen financial calculation snapshot data
    calc_data = generate_financial_statements(db, year_id, rule_config)

    snapshot = StatementSnapshot(
        year_id=year_id,
        version=next_ver,
        status=ReviewStatus.DRAFT,
        snapshot_data=calc_data,
        created_by=created_by,
        notes=notes,
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


def get_snapshots_for_year(db: Session, year_id: int) -> List[StatementSnapshot]:
    """Retrieves all statement snapshots for a given fiscal year ordered by version desc."""
    return (
        db.query(StatementSnapshot)
        .filter(StatementSnapshot.year_id == year_id)
        .order_by(StatementSnapshot.version.desc())
        .all()
    )


def update_snapshot_review_status(
    db: Session,
    snapshot_id: int,
    new_status: ReviewStatus,
    notes: Optional[str] = None,
) -> StatementSnapshot:
    """
    Updates review status (DRAFT, UNDER_REVIEW, APPROVED, REJECTED) for a snapshot.
    Enforces fiscal year mutability protection.
    """
    snapshot = db.query(StatementSnapshot).filter(StatementSnapshot.id == snapshot_id).first()
    if not snapshot:
        raise ValueError(f"StatementSnapshot with id {snapshot_id} not found.")

    check_fiscal_year_mutable(db, snapshot.year_id)

    snapshot.status = new_status
    if notes:
        snapshot.notes = f"{snapshot.notes or ''}\n[Status Change to {new_status.value}]: {notes}".strip()

    db.commit()
    db.refresh(snapshot)
    return snapshot
