from __future__ import annotations

import enum
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    event,
    inspect,
    select,
)
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from aram_backend.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class FiscalYearStatus(str, enum.Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    LOCKED = "Locked"


class StatementType(str, enum.Enum):
    BALANCE_SHEET = "BS"
    INCOME_STATEMENT = "IS"
    CASH_FLOW = "CF"
    EQUITY = "EQ"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )


class Company(TimestampMixin, Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    fiscal_years: Mapped[list[FiscalYear]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )


class FiscalYear(TimestampMixin, Base):
    __tablename__ = "fiscal_years"
    __table_args__ = (
        UniqueConstraint("company_id", "year", name="uq_fiscal_year_company_year"),
        CheckConstraint("year > 0", name="positive_year"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="RESTRICT"))
    year: Mapped[int] = mapped_column(Integer)
    status: Mapped[FiscalYearStatus] = mapped_column(
        Enum(FiscalYearStatus, native_enum=False), default=FiscalYearStatus.DRAFT
    )
    company: Mapped[Company] = relationship(back_populates="fiscal_years")


class YearOwnedMixin:
    year_id: Mapped[int] = mapped_column(ForeignKey("fiscal_years.id", ondelete="RESTRICT"), index=True)


class SourceDocument(TimestampMixin, YearOwnedMixin, Base):
    __tablename__ = "source_documents"
    __table_args__ = (
        UniqueConstraint("year_id", "file_hash", name="uq_source_document_year_hash"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(512))
    file_hash: Mapped[str] = mapped_column(String(128))
    document_type: Mapped[str] = mapped_column(String(64))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AccountVersion(TimestampMixin, YearOwnedMixin, Base):
    __tablename__ = "account_versions"
    __table_args__ = (
        UniqueConstraint("year_id", "account_code", "version", name="uq_account_year_code_version"),
        CheckConstraint("version > 0", name="positive_version"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    account_code: Mapped[str] = mapped_column(String(64), index=True)
    account_name: Mapped[str] = mapped_column(String(512))
    version: Mapped[int] = mapped_column(Integer, default=1)
    t1: Mapped[str | None] = mapped_column(String(128))
    t2: Mapped[str | None] = mapped_column(String(128))
    t3: Mapped[str | None] = mapped_column(String(128))
    t4: Mapped[str | None] = mapped_column(String(128))
    nature: Mapped[str | None] = mapped_column(String(64))


class NoteDefinition(TimestampMixin, YearOwnedMixin, Base):
    __tablename__ = "note_definitions"
    __table_args__ = (
        UniqueConstraint("year_id", "note_number", "version", name="uq_note_year_number_version"),
        CheckConstraint("version > 0", name="positive_version"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    note_number: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(512))
    version: Mapped[int] = mapped_column(Integer, default=1)
    configuration_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    rows: Mapped[list[NoteRow]] = relationship(back_populates="note", cascade="all, delete-orphan")


class NoteRow(TimestampMixin, Base):
    __tablename__ = "note_rows"
    __table_args__ = (
        UniqueConstraint("note_id", "row_order", name="uq_note_row_order"),
        CheckConstraint("row_order >= 0", name="nonnegative_row_order"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("note_definitions.id", ondelete="CASCADE"), index=True)
    row_order: Mapped[int] = mapped_column(Integer)
    label: Mapped[str] = mapped_column(String(512))
    formula_logic: Mapped[str | None] = mapped_column(Text)
    sorting_rule_id: Mapped[str | None] = mapped_column(String(128))
    note: Mapped[NoteDefinition] = relationship(back_populates="rows")


class MappingRule(TimestampMixin, YearOwnedMixin, Base):
    __tablename__ = "mapping_rules"
    __table_args__ = (
        UniqueConstraint("year_id", "rule_key", "version", name="uq_mapping_year_key_version"),
        CheckConstraint("version > 0", name="positive_version"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    rule_key: Mapped[str] = mapped_column(String(128))
    version: Mapped[int] = mapped_column(Integer, default=1)
    account_code: Mapped[str] = mapped_column(String(64), index=True)
    target_note_id: Mapped[int] = mapped_column(ForeignKey("note_definitions.id", ondelete="RESTRICT"))
    mapping_type: Mapped[str] = mapped_column(String(32))
    target_note: Mapped[NoteDefinition] = relationship()


class FinancialStatement(TimestampMixin, YearOwnedMixin, Base):
    __tablename__ = "financial_statements"
    __table_args__ = (
        UniqueConstraint("year_id", "statement_type", "version", name="uq_statement_year_type_version"),
        CheckConstraint("version > 0", name="positive_version"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    statement_type: Mapped[StatementType] = mapped_column(Enum(StatementType, native_enum=False))
    version: Mapped[int] = mapped_column(Integer, default=1)
    lines: Mapped[list[StatementLine]] = relationship(
        back_populates="statement", cascade="all, delete-orphan"
    )


class StatementLine(TimestampMixin, Base):
    __tablename__ = "statement_lines"
    __table_args__ = (
        UniqueConstraint("statement_id", "line_order", name="uq_statement_line_order"),
        CheckConstraint("line_order >= 0", name="nonnegative_line_order"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    statement_id: Mapped[int] = mapped_column(ForeignKey("financial_statements.id", ondelete="CASCADE"), index=True)
    line_order: Mapped[int] = mapped_column(Integer)
    line_label: Mapped[str] = mapped_column(String(512))
    target_note_id: Mapped[int | None] = mapped_column(ForeignKey("note_definitions.id", ondelete="RESTRICT"))
    mapped_total: Mapped[Decimal | None] = mapped_column(Numeric(24, 4))
    statement: Mapped[FinancialStatement] = relationship(back_populates="lines")
    target_note: Mapped[NoteDefinition | None] = relationship()


def _year_id_for(obj: object, session: Session) -> int | None:
    if isinstance(obj, FiscalYear):
        return obj.id
    if isinstance(obj, YearOwnedMixin):
        return obj.year_id
    if isinstance(obj, NoteRow):
        if obj.note is not None:
            return obj.note.year_id
        if obj.note_id is not None:
            return session.scalar(
                select(NoteDefinition.year_id).where(NoteDefinition.id == obj.note_id)
            )
    if isinstance(obj, StatementLine):
        if obj.statement is not None:
            return obj.statement.year_id
        if obj.statement_id is not None:
            return session.scalar(
                select(FinancialStatement.year_id).where(
                    FinancialStatement.id == obj.statement_id
                )
            )
    return None


@event.listens_for(Session, "before_flush")
def enforce_audit_invariants(session: Session, _flush_context, _instances) -> None:
    for obj in session.dirty:
        if isinstance(obj, FiscalYear):
            history = inspect(obj).attrs.status.history
            if history.deleted:
                old = history.deleted[0]
                allowed = {
                    FiscalYearStatus.DRAFT: {FiscalYearStatus.APPROVED},
                    FiscalYearStatus.APPROVED: {FiscalYearStatus.LOCKED},
                    FiscalYearStatus.LOCKED: set(),
                }
                if obj.status not in allowed[old]:
                    raise ValueError(f"Invalid fiscal-year transition: {old.value} -> {obj.status.value}")

    protected = (session.new | session.dirty | session.deleted)
    for obj in protected:
        if isinstance(obj, FiscalYear):
            continue
        year_id = _year_id_for(obj, session)
        if year_id is None:
            continue
        status = session.scalar(select(FiscalYear.status).where(FiscalYear.id == year_id))
        if status in {FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED}:
            raise ValueError(
                f"Fiscal year {year_id} is {status.value.lower()} and cannot be mutated"
            )

        if isinstance(obj, MappingRule):
            target_year_id = (
                obj.target_note.year_id
                if obj.target_note is not None
                else session.scalar(
                    select(NoteDefinition.year_id).where(
                        NoteDefinition.id == obj.target_note_id
                    )
                )
            )
            if target_year_id != obj.year_id:
                raise ValueError("Mapping rule and target note must belong to the same fiscal year")
        if isinstance(obj, StatementLine) and obj.target_note_id is not None:
            target_year_id = (
                obj.target_note.year_id
                if obj.target_note is not None
                else session.scalar(
                    select(NoteDefinition.year_id).where(
                        NoteDefinition.id == obj.target_note_id
                    )
                )
            )
            if target_year_id != year_id:
                raise ValueError("Statement line and target note must belong to the same fiscal year")
