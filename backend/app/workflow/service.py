from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

from backend.app.models.entities import (
    FiscalYear,
    SourceDocument,
    StatementSnapshot,
    WorkflowStatus,
    ReviewStatus,
)
from backend.app.services.protection import check_fiscal_year_mutable
from backend.app.ingestion.service import register_source_document
from backend.app.normalization.service import normalize_and_persist_records
from backend.app.accounting.service import generate_financial_statements
from backend.app.accounting.snapshot import create_statement_snapshot, update_snapshot_review_status
from backend.app.services.audit import log_audit_event


def update_workflow_status(db: Session, year_id: int, new_status: WorkflowStatus) -> FiscalYear:
    """Updates workflow status for a fiscal year."""
    fy = db.query(FiscalYear).filter(FiscalYear.id == year_id).first()
    if not fy:
        raise ValueError(f"FiscalYear with id {year_id} not found.")

    fy.workflow_status = new_status
    db.commit()
    db.refresh(fy)
    return fy


def execute_end_to_end_workflow(
    db: Session,
    year_id: int,
    file_path: str,
    doc_type: str,
    raw_rows: List[Dict[str, Any]],
    user_id: int = None,
    username: str = "system",
) -> Tuple[FiscalYear, SourceDocument, StatementSnapshot]:
    """
    Orchestrates complete end-to-end financial workflow:
    1. Source Upload & Ingestion -> UPLOADED / PROCESSING
    2. Normalization -> NORMALIZED
    3. Accounting Calculation -> CALCULATED
    4. Snapshot Generation -> READY_FOR_REVIEW
    """
    check_fiscal_year_mutable(db, year_id)

    # Step 1: Ingestion
    update_workflow_status(db, year_id, WorkflowStatus.PROCESSING)
    source_doc = register_source_document(db, year_id, file_path, doc_type)
    log_audit_event(db, user_id, f"Workflow Ingestion complete for '{source_doc.filename}'", "SourceDocument", "CREATE")

    # Step 2: Normalization
    records, logs = normalize_and_persist_records(db, year_id, source_doc.id, raw_rows)
    update_workflow_status(db, year_id, WorkflowStatus.NORMALIZED)
    log_audit_event(db, user_id, f"Normalized {len(records)} records with {len(logs)} logs", "NormalizedFinancialRecord", "CREATE")

    # Step 3: Calculation
    calc_results = generate_financial_statements(db, year_id)
    update_workflow_status(db, year_id, WorkflowStatus.CALCULATED)
    log_audit_event(db, user_id, "Calculated financial statement foundations", "FinancialStatement", "READ")

    # Step 4: Snapshot Generation
    snapshot = create_statement_snapshot(
        db,
        year_id=year_id,
        notes="Automated E2E Workflow Snapshot",
        created_by=username,
    )
    fy = update_workflow_status(db, year_id, WorkflowStatus.READY_FOR_REVIEW)
    log_audit_event(db, user_id, f"Generated StatementSnapshot v{snapshot.version}. Workflow ready for review.", "StatementSnapshot", "CREATE")

    return fy, source_doc, snapshot


def approve_workflow_and_snapshot(
    db: Session,
    snapshot_id: int,
    user_id: int = None,
    username: str = "auditor",
) -> Tuple[FiscalYear, StatementSnapshot]:
    """Approves a review snapshot and sets workflow status to APPROVED."""
    snapshot = db.query(StatementSnapshot).filter(StatementSnapshot.id == snapshot_id).first()
    if not snapshot:
        raise ValueError(f"StatementSnapshot {snapshot_id} not found.")

    updated_snap = update_snapshot_review_status(db, snapshot_id, ReviewStatus.APPROVED, notes="E2E Approved")
    fy = update_workflow_status(db, snapshot.year_id, WorkflowStatus.APPROVED)

    log_audit_event(db, user_id, f"E2E Workflow Approved for snapshot v{snapshot.version}", "FiscalYear", "UPDATE")
    return fy, updated_snap
