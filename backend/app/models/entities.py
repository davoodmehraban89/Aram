import enum
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Enum as SQLEnum,
    UniqueConstraint,
    JSON,
    Numeric,
    Text,
)
from sqlalchemy.orm import relationship

from backend.app.database import Base
from backend.app.models.base import TimestampMixin


class FiscalYearStatus(str, enum.Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    LOCKED = "Locked"


class StatementType(str, enum.Enum):
    BS = "BS"  # Balance Sheet
    IS = "IS"  # Income Statement
    CF = "CF"  # Cash Flow
    EQ = "EQ"  # Equity Statement


class ValidationSeverity(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)

    fiscal_years = relationship("FiscalYear", back_populates="company", cascade="all, delete-orphan")


class FiscalYear(Base, TimestampMixin):
    __tablename__ = "fiscal_years"
    __table_args__ = (
        UniqueConstraint("company_id", "year", name="uq_company_fiscal_year"),
    )

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    status = Column(SQLEnum(FiscalYearStatus), default=FiscalYearStatus.DRAFT, nullable=False)

    company = relationship("Company", back_populates="fiscal_years")
    source_documents = relationship("SourceDocument", back_populates="fiscal_year", cascade="all, delete-orphan")
    account_versions = relationship("AccountVersion", back_populates="fiscal_year", cascade="all, delete-orphan")
    mapping_rules = relationship("MappingRule", back_populates="fiscal_year", cascade="all, delete-orphan")
    note_definitions = relationship("NoteDefinition", back_populates="fiscal_year", cascade="all, delete-orphan")
    financial_statements = relationship("FinancialStatement", back_populates="fiscal_year", cascade="all, delete-orphan")
    mapping_templates = relationship("MappingTemplate", back_populates="fiscal_year", cascade="all, delete-orphan")
    normalized_records = relationship("NormalizedFinancialRecord", back_populates="fiscal_year", cascade="all, delete-orphan")
    validation_logs = relationship("ValidationErrorLog", back_populates="fiscal_year", cascade="all, delete-orphan")


class SourceDocument(Base, TimestampMixin):
    __tablename__ = "source_documents"

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=False)
    doc_type = Column(String(50), nullable=False)  # ledger, official_statement, mapping, auditor_report
    upload_date = Column(String(50), nullable=True)
    processing_status = Column(String(50), nullable=False, default="REGISTERED")
    version = Column(Integer, nullable=False, default=1)

    fiscal_year = relationship("FiscalYear", back_populates="source_documents")
    normalized_records = relationship("NormalizedFinancialRecord", back_populates="source_document", cascade="all, delete-orphan")
    validation_logs = relationship("ValidationErrorLog", back_populates="source_document", cascade="all, delete-orphan")


class AccountVersion(Base, TimestampMixin):
    __tablename__ = "account_versions"
    __table_args__ = (
        UniqueConstraint("year_id", "account_code", name="uq_year_account_code"),
    )

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    account_code = Column(String(100), nullable=False, index=True)
    account_name = Column(String(255), nullable=False)
    t1 = Column(String(100), nullable=True)
    t2 = Column(String(100), nullable=True)
    t3 = Column(String(100), nullable=True)
    t4 = Column(String(100), nullable=True)
    nature = Column(String(50), nullable=True)

    fiscal_year = relationship("FiscalYear", back_populates="account_versions")
    mapping_rules = relationship("MappingRule", back_populates="account_version", cascade="all, delete-orphan")


class MappingRule(Base, TimestampMixin):
    __tablename__ = "mapping_rules"

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    account_code = Column(String(100), nullable=False, index=True)
    account_version_id = Column(Integer, ForeignKey("account_versions.id", ondelete="SET NULL"), nullable=True)
    target_note_id = Column(Integer, ForeignKey("note_definitions.id", ondelete="SET NULL"), nullable=True)
    mapping_type = Column(String(50), nullable=False, default="DETERMINISTIC")

    fiscal_year = relationship("FiscalYear", back_populates="mapping_rules")
    account_version = relationship("AccountVersion", back_populates="mapping_rules")
    target_note = relationship("NoteDefinition", back_populates="mapping_rules")


class NoteDefinition(Base, TimestampMixin):
    __tablename__ = "note_definitions"
    __table_args__ = (
        UniqueConstraint("year_id", "note_number", name="uq_year_note_number"),
    )

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    note_number = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    configuration_json = Column(JSON, nullable=True)

    fiscal_year = relationship("FiscalYear", back_populates="note_definitions")
    rows = relationship("NoteRow", back_populates="note_definition", cascade="all, delete-orphan")
    mapping_rules = relationship("MappingRule", back_populates="target_note")
    statement_lines = relationship("StatementLine", back_populates="target_note")


class NoteRow(Base, TimestampMixin):
    __tablename__ = "note_rows"

    note_id = Column(Integer, ForeignKey("note_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    row_order = Column(Integer, nullable=False)
    label = Column(String(255), nullable=False)
    formula_logic = Column(Text, nullable=True)
    sorting_rule_id = Column(String(50), nullable=True)

    note_definition = relationship("NoteDefinition", back_populates="rows")


class FinancialStatement(Base, TimestampMixin):
    __tablename__ = "financial_statements"
    __table_args__ = (
        UniqueConstraint("year_id", "statement_type", name="uq_year_statement_type"),
    )

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    statement_type = Column(SQLEnum(StatementType), nullable=False)

    fiscal_year = relationship("FiscalYear", back_populates="financial_statements")
    lines = relationship("StatementLine", back_populates="financial_statement", cascade="all, delete-orphan")


class StatementLine(Base, TimestampMixin):
    __tablename__ = "statement_lines"

    statement_id = Column(Integer, ForeignKey("financial_statements.id", ondelete="CASCADE"), nullable=False, index=True)
    line_label = Column(String(255), nullable=False)
    target_note_id = Column(Integer, ForeignKey("note_definitions.id", ondelete="SET NULL"), nullable=True)
    mapped_total = Column(Numeric(precision=20, scale=2), nullable=True)

    financial_statement = relationship("FinancialStatement", back_populates="lines")
    target_note = relationship("NoteDefinition", back_populates="statement_lines")


class MappingTemplate(Base, TimestampMixin):
    __tablename__ = "mapping_templates"
    __table_args__ = (
        UniqueConstraint("year_id", "template_name", name="uq_year_template_name"),
    )

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    template_name = Column(String(100), nullable=False)
    column_mappings = Column(JSON, nullable=False)  # JSON dict mapping canonical fields to source column headers

    fiscal_year = relationship("FiscalYear", back_populates="mapping_templates")


class NormalizedFinancialRecord(Base, TimestampMixin):
    __tablename__ = "normalized_financial_records"

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    source_document_id = Column(Integer, ForeignKey("source_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    row_index = Column(Integer, nullable=False)
    account_code = Column(String(100), nullable=False, index=True)
    account_name = Column(String(255), nullable=False)
    debit = Column(Numeric(precision=20, scale=2), default=0.00, nullable=False)
    credit = Column(Numeric(precision=20, scale=2), default=0.00, nullable=False)
    net_amount = Column(Numeric(precision=20, scale=2), default=0.00, nullable=False)
    t1 = Column(String(100), nullable=True)
    t2 = Column(String(100), nullable=True)
    t3 = Column(String(100), nullable=True)
    t4 = Column(String(100), nullable=True)
    raw_payload = Column(JSON, nullable=True)

    fiscal_year = relationship("FiscalYear", back_populates="normalized_records")
    source_document = relationship("SourceDocument", back_populates="normalized_records")


class ValidationErrorLog(Base, TimestampMixin):
    __tablename__ = "validation_error_logs"

    year_id = Column(Integer, ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=False, index=True)
    source_document_id = Column(Integer, ForeignKey("source_documents.id", ondelete="CASCADE"), nullable=True, index=True)
    severity = Column(SQLEnum(ValidationSeverity), nullable=False, default=ValidationSeverity.ERROR)
    error_code = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    context_data = Column(JSON, nullable=True)

    fiscal_year = relationship("FiscalYear", back_populates="validation_logs")
    source_document = relationship("SourceDocument", back_populates="validation_logs")
