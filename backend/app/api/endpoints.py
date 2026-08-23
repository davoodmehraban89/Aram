from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
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
from backend.app.services.feedback import (
    record_pilot_feedback,
    log_pilot_validation_summary,
    get_recurring_unknown_accounts,
)
from backend.app.accounting.service import generate_financial_statements
from backend.app.accounting.snapshot import (
    create_statement_snapshot,
    get_snapshots_for_year,
    update_snapshot_review_status,
)
from backend.app.workflow.service import execute_end_to_end_workflow, approve_workflow_and_snapshot, update_workflow_status
from backend.app.normalization.mapping_engine import COAMappingEngine


router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint to verify backend service status."""
    return {"status": "ok", "service": "financial-reporting-platform"}


# --- Pilot Feedback & Validation Endpoints (Phase 13) ---

@router.post("/pilot/feedback", response_model=schemas.PilotFeedbackRead)
def submit_pilot_feedback(
    year_id: int = Query(..., description="Fiscal Year ID"),
    feedback_data: schemas.PilotFeedbackCreate = Body(...),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Submits accountant pilot feedback or mapping correction."""
    fb = record_pilot_feedback(
        db,
        year_id=year_id,
        user_id=user.get("user_id"),
        category=feedback_data.category,
        comments=feedback_data.comments,
        account_code=feedback_data.account_code,
        original_value=feedback_data.original_value,
        corrected_value=feedback_data.corrected_value,
    )
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Submitted pilot feedback for account '{feedback_data.account_code}'.",
        entity_affected="PilotFeedback",
        action_type="CREATE",
    )
    return fb


@router.get("/pilot/feedback", response_model=List[schemas.PilotFeedbackRead])
def list_pilot_feedback(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Lists pilot feedback entries for a fiscal year."""
    return db.query(models.PilotFeedback).filter(models.PilotFeedback.year_id == year_id).all()


@router.get("/pilot/validation-logs", response_model=List[schemas.PilotValidationLogRead])
def list_pilot_validation_logs(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Lists pilot validation summary logs for a fiscal year."""
    return db.query(models.PilotValidationLog).filter(models.PilotValidationLog.year_id == year_id).all()


@router.get("/pilot/recurring-unknowns")
def list_recurring_unknown_accounts(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Lists recurring unknown or unmapped accounts detected from pilot feedback."""
    return get_recurring_unknown_accounts(db, year_id)


# --- COA Mapping Engine Endpoints ---

@router.get("/coa/unmapped", response_model=List[Dict[str, Any]])
def get_unmapped_accounts(
    year_id: int = Query(..., description="Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Detects unmapped accounts for a fiscal year."""
    engine = COAMappingEngine(db, year_id)
    return engine.detect_unmapped_accounts()


@router.post("/coa/rules", response_model=schemas.COAMappingRuleRead)
def save_coa_mapping_rule(
    year_id: int = Query(..., description="Fiscal Year ID"),
    rule_data: schemas.COAMappingRuleBase = Body(...),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Saves or updates a Chart of Accounts mapping rule."""
    engine = COAMappingEngine(db, year_id)
    rule = engine.save_mapping_rule(
        account_code=rule_data.account_code,
        account_name=rule_data.account_name,
        target_statement=rule_data.target_statement,
        statement_section=rule_data.statement_section,
        group_name=rule_data.group_name,
        is_approved=rule_data.is_approved,
    )
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Saved COAMappingRule for code '{rule_data.account_code}' in FiscalYear {year_id}.",
        entity_affected="COAMappingRule",
        action_type="CREATE",
    )
    return rule


@router.post("/coa/copy-template")
def copy_mapping_template(
    year_id: int = Query(..., description="Target Fiscal Year ID"),
    source_year_id: int = Query(..., description="Source Fiscal Year ID"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Copies approved mapping rules from a previous fiscal year for template reuse."""
    engine = COAMappingEngine(db, year_id)
    copied_count = engine.copy_template_from_year(source_year_id)
    log_audit_event(
        db,
        user_id=user.get("user_id"),
        user_action=f"Copied {copied_count} COAMappingRules from FiscalYear {source_year_id} to {year_id}.",
        entity_affected="COAMappingRule",
        action_type="CREATE",
    )
    return {"year_id": year_id, "source_year_id": source_year_id, "copied_rules_count": copied_count}


# --- Workflow Orchestration Endpoints ---

@router.post("/workflow/execute")
def execute_workflow_endpoint(
    year_id: int = Query(..., description="Fiscal Year ID"),
    file_path: str = Query(..., description="Source File Path"),
    doc_type: str = Query("ledger", description="Document Type"),
    raw_rows: List[Dict[str, Any]] = Body(..., description="Raw rows payload"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Executes complete end-to-end workflow: Ingestion -> Normalization -> Calculation -> Snapshot."""
    fy, doc, snap = execute_end_to_end_workflow(
        db,
        year_id=year_id,
        file_path=file_path,
        doc_type=doc_type,
        raw_rows=raw_rows,
        user_id=user.get("user_id"),
        username=user.get("username"),
    )
    return {
        "year_id": year_id,
        "workflow_status": fy.workflow_status,
        "source_document_id": doc.id,
        "snapshot_id": snap.id,
        "snapshot_version": snap.version,
    }


@router.post("/workflow/approve")
def approve_workflow_endpoint(
    snapshot_id: int = Query(..., description="Snapshot ID to approve"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(require_role([models.UserRole.ADMIN, models.UserRole.AUDITOR])),
):
    """Approves workflow and review snapshot."""
    fy, snap = approve_workflow_and_snapshot(
        db,
        snapshot_id=snapshot_id,
        user_id=user.get("user_id"),
        username=user.get("username"),
    )
    return {
        "year_id": fy.id,
        "workflow_status": fy.workflow_status,
        "snapshot_id": snap.id,
        "snapshot_status": snap.status,
    }


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
