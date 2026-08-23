from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app import models, schemas
from backend.app.api.auth import (
    get_current_user,
    require_role,
    hash_password,
    verify_password,
    create_access_token,
)
from backend.app.services.audit import log_audit_event
from backend.app.accounting.service import generate_financial_statements
from backend.app.accounting.snapshot import (
    create_statement_snapshot,
    get_snapshots_for_year,
    update_snapshot_review_status,
)


router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint to verify backend service status."""
    return {"status": "ok", "service": "financial-reporting-platform"}


# --- Authentication & User Endpoints ---

@router.post("/auth/login", response_model=schemas.Token)
def login_endpoint(
    login_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Authenticates user credentials and returns JWT access token."""
    user = db.query(models.User).filter(models.User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )

    token = create_access_token({"sub": user.username, "role": user.role.value})
    log_audit_event(
        db,
        user_id=user.id,
        user_action=f"User '{user.username}' logged in successfully.",
        entity_affected="User",
        action_type="LOGIN",
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role,
    }


@router.get("/auth/me", response_model=Dict[str, Any])
def get_current_user_me(user: Dict[str, Any] = Depends(get_current_user)):
    """Returns current authenticated user context."""
    return user


@router.get("/audit-logs", response_model=List[schemas.AuditLogRead])
def list_audit_logs(
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Lists audit logs for security and compliance review."""
    return db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).all()


# --- Core Read-Only Schema Endpoints ---

@router.get("/companies", response_model=List[schemas.CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    """Read-only schema endpoint listing companies."""
    return db.query(models.Company).all()


@router.get("/fiscal-years", response_model=List[schemas.FiscalYearRead])
def list_fiscal_years(
    company_id: Optional[int] = Query(None, description="Filter by company ID"),
    db: Session = Depends(get_db)
):
    """Read-only schema endpoint listing fiscal years."""
    query = db.query(models.FiscalYear)
    if company_id is not None:
        query = query.filter(models.FiscalYear.company_id == company_id)
    return query.all()


@router.get("/notes", response_model=List[schemas.NoteDefinitionRead])
def list_note_definitions(
    year_id: Optional[int] = Query(None, description="Filter by fiscal year ID"),
    db: Session = Depends(get_db)
):
    """Read-only schema endpoint listing note definitions."""
    query = db.query(models.NoteDefinition)
    if year_id is not None:
        query = query.filter(models.NoteDefinition.year_id == year_id)
    return query.all()


@router.get("/statements", response_model=List[schemas.FinancialStatementRead])
def list_financial_statements(
    year_id: Optional[int] = Query(None, description="Filter by fiscal year ID"),
    db: Session = Depends(get_db)
):
    """Read-only schema endpoint listing financial statements."""
    query = db.query(models.FinancialStatement)
    if year_id is not None:
        query = query.filter(models.FinancialStatement.year_id == year_id)
    return query.all()


# --- Financial Reporting API Endpoints ---

@router.get("/reporting/trial-balance")
def get_trial_balance_report(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Returns calculated Trial Balance for specified fiscal year."""
    statements = generate_financial_statements(db, year_id=year_id)
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Queried Trial Balance for FiscalYear {year_id}.",
        entity_affected="NormalizedFinancialRecord",
        action_type="READ",
    )
    return statements["trial_balance"]


@router.get("/reporting/balance-sheet")
def get_balance_sheet_report(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Returns calculated Balance Sheet foundation for specified fiscal year."""
    statements = generate_financial_statements(db, year_id=year_id)
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Queried Balance Sheet for FiscalYear {year_id}.",
        entity_affected="NormalizedFinancialRecord",
        action_type="READ",
    )
    return statements["balance_sheet"]


@router.get("/reporting/income-statement")
def get_income_statement_report(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Returns calculated Income Statement foundation for specified fiscal year."""
    statements = generate_financial_statements(db, year_id=year_id)
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Queried Income Statement for FiscalYear {year_id}.",
        entity_affected="NormalizedFinancialRecord",
        action_type="READ",
    )
    return statements["income_statement"]


# --- Statement Snapshot & Review Endpoints ---

@router.get("/snapshots", response_model=List[schemas.StatementSnapshotRead])
def list_snapshots(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Lists versioned statement snapshots for a fiscal year."""
    return get_snapshots_for_year(db, year_id=year_id)


@router.post("/snapshots", response_model=schemas.StatementSnapshotRead)
def create_snapshot_endpoint(
    year_id: int = Query(..., description="Fiscal Year ID"),
    notes: Optional[str] = Query(None, description="Snapshot notes"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Generates and persists a new StatementSnapshot for a fiscal year."""
    snapshot = create_statement_snapshot(
        db,
        year_id=year_id,
        notes=notes,
        created_by=user.get("username"),
    )
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Created StatementSnapshot v{snapshot.version} for FiscalYear {year_id}.",
        entity_affected="StatementSnapshot",
        action_type="CREATE",
    )
    return snapshot


@router.patch("/snapshots/{snapshot_id}/status", response_model=schemas.StatementSnapshotRead)
def update_snapshot_status_endpoint(
    snapshot_id: int,
    new_status: models.ReviewStatus = Query(..., description="New review status"),
    notes: Optional[str] = Query(None, description="Status update notes"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Updates review status for a statement snapshot (DRAFT, UNDER_REVIEW, APPROVED, REJECTED)."""
    snapshot = update_snapshot_review_status(
        db,
        snapshot_id=snapshot_id,
        new_status=new_status,
        notes=notes,
    )
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Updated StatementSnapshot {snapshot_id} status to '{new_status.value}'.",
        entity_affected="StatementSnapshot",
        action_type="UPDATE",
    )
    return snapshot


@router.get("/snapshots/{snapshot_id}", response_model=schemas.StatementSnapshotRead)
def get_snapshot_by_id(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Retrieves a specific statement snapshot (preserving read-only access)."""
    snapshot = db.query(models.StatementSnapshot).filter(models.StatementSnapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"StatementSnapshot with id {snapshot_id} not found."
        )
    return snapshot
