from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict
from backend.app.models.entities import FiscalYearStatus, StatementType, ValidationSeverity, ReviewStatus, UserRole


class BaseORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str
    role: UserRole = UserRole.AUDITOR
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase, BaseORMModel):
    id: int
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: UserRole


class AuditLogRead(BaseORMModel):
    id: int
    user_id: Optional[int] = None
    user_action: str
    entity_affected: str
    action_type: str
    context_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


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
    processing_status: str
    version: int
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


class MappingTemplateRead(BaseORMModel):
    id: int
    year_id: int
    template_name: str
    column_mappings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class NormalizedFinancialRecordRead(BaseORMModel):
    id: int
    year_id: int
    source_document_id: int
    row_index: int
    account_code: str
    account_name: str
    debit: float
    credit: float
    net_amount: float
    t1: Optional[str] = None
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ValidationErrorLogRead(BaseORMModel):
    id: int
    year_id: int
    source_document_id: Optional[int] = None
    severity: ValidationSeverity
    error_code: str
    message: str
    context_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class StatementSnapshotRead(BaseORMModel):
    id: int
    year_id: int
    version: int
    status: ReviewStatus
    snapshot_data: Dict[str, Any]
    created_by: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
