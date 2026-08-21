from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict
from backend.app.models.entities import FiscalYearStatus, StatementType


class BaseORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CompanyBase(BaseModel):
    code: str
    name: str


class CompanyRead(CompanyBase, BaseORMModel):
    id: int
    created_at: datetime
    updated_at: datetime


class FiscalYearBase(BaseModel):
    company_id: int
    year: int
    status: FiscalYearStatus = FiscalYearStatus.DRAFT


class FiscalYearRead(FiscalYearBase, BaseORMModel):
    id: int
    created_at: datetime
    updated_at: datetime


class SourceDocumentRead(BaseORMModel):
    id: int
    year_id: int
    filename: str
    file_hash: str
    doc_type: str
    upload_date: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class NoteRowRead(BaseORMModel):
    id: int
    note_id: int
    row_order: int
    label: str
    formula_logic: Optional[str] = None
    sorting_rule_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class NoteDefinitionRead(BaseORMModel):
    id: int
    year_id: int
    note_number: int
    title: str
    configuration_json: Optional[Any] = None
    created_at: datetime
    updated_at: datetime


class StatementLineRead(BaseORMModel):
    id: int
    statement_id: int
    line_label: str
    target_note_id: Optional[int] = None
    mapped_total: Optional[float] = None
    created_at: datetime
    updated_at: datetime


class FinancialStatementRead(BaseORMModel):
    id: int
    year_id: int
    statement_type: StatementType
    created_at: datetime
    updated_at: datetime
