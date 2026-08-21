from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app import models, schemas

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint to verify backend service status."""
    return {"status": "ok", "service": "financial-reporting-platform"}


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
