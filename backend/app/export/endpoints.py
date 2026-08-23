from typing import Dict, Any
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.api.auth import get_current_user
from backend.app.accounting.service import generate_financial_statements
from backend.app.accounting.snapshot import get_snapshots_for_year
from backend.app.export.service import export_statement_to_csv, export_statement_to_pdf_structure

router = APIRouter()


@router.get("/export/csv")
def export_statement_csv(
    year_id: int = Query(..., description="Fiscal Year ID"),
    statement_type: str = Query("TB", description="Statement Type (TB, BS, IS)"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Exports specified financial statement calculation to CSV file response."""
    statements = generate_financial_statements(db, year_id=year_id)
    if statement_type == "BS":
        data = statements["balance_sheet"]
    elif statement_type == "IS":
        data = statements["income_statement"]
    else:
        data = statements["trial_balance"]

    csv_content = export_statement_to_csv(data)
    filename = f"{statement_type}_year_{year_id}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/pdf-structure")
def export_statement_pdf_structure(
    year_id: int = Query(..., description="Fiscal Year ID"),
    statement_type: str = Query("TB", description="Statement Type (TB, BS, IS)"),
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Returns PDF-ready structured payload for financial statement."""
    statements = generate_financial_statements(db, year_id=year_id)
    if statement_type == "BS":
        data = statements["balance_sheet"]
    elif statement_type == "IS":
        data = statements["income_statement"]
    else:
        data = statements["trial_balance"]

    return export_statement_to_pdf_structure(data)
