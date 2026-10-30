from __future__ import annotations

import enum
from datetime import UTC, datetime
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
    return datetime.now(UTC)


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


def _resolve_parent_year_id(
    obj: Any, session: Session, rel_attr: str, fk_attr: str, parent_cls: type[Any]
) -> int | None:
    state = inspect(obj)
    relationship_history = state.attrs[rel_attr].history
    foreign_key_history = state.attrs[fk_attr].history
    fk_val = getattr(obj, fk_attr, None)
    if relationship_history.has_changes():
        parent = getattr(obj, rel_attr, None)
        parent_id = parent.id if parent is not None else None
        if foreign_key_history.has_changes() and fk_val != parent_id:
            raise ValueError(f"Conflicting {rel_attr} relationship and {fk_attr}")
    elif fk_val is not None:
        # A raw FK assignment does not invalidate an already cached relationship.
        parent = session.get(parent_cls, fk_val)
        if parent is None:
            # Pending explicit-ID parents are not in the Session identity map yet.
            parent = next(
                (
                    candidate for candidate in session.new
                    if isinstance(candidate, parent_cls) and candidate.id == fk_val
                ),
                None,
            )
    else:
        parent = None
    return parent.year_id if parent is not None else None


def _year_id_for(obj: object, session: Session) -> int | None:
    if isinstance(obj, FiscalYear):
        return obj.id
    if isinstance(obj, YearOwnedMixin):
        return obj.year_id
    if isinstance(obj, NoteRow):
        return _resolve_parent_year_id(obj, session, "note", "note_id", NoteDefinition)
    if isinstance(obj, StatementLine):
        return _resolve_parent_year_id(obj, session, "statement", "statement_id", FinancialStatement)
    return None


def _persisted_year_id_for(obj: Any, session: Session) -> int | None:
    """Read original ownership before flush, even when attributes are expired."""
    identity = inspect(obj).identity
    if identity is None:
        return None
    if isinstance(obj, YearOwnedMixin):
        model = type(obj)
        query = select(model.year_id).where(model.id == identity[0])
    elif isinstance(obj, NoteRow):
        query = (
            select(NoteDefinition.year_id)
            .join(NoteRow, NoteRow.note_id == NoteDefinition.id)
            .where(NoteRow.id == identity[0])
        )
    elif isinstance(obj, StatementLine):
        query = (
            select(FinancialStatement.year_id)
            .join(StatementLine, StatementLine.statement_id == FinancialStatement.id)
            .where(StatementLine.id == identity[0])
        )
    else:
        return None
    return session.scalar(query)


_PROTECTED_YEAR_STATUSES = {FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED}


def _protected_year_status(session: Session, year_id: int) -> FiscalYearStatus | None:
    """Protect both persisted status and an in-flight approval/locking transition.

    A database SELECT alone sees Draft until the pending FiscalYear status is
    flushed, allowing a second dirty object to change in the approval flush.
    """
    for candidate in session.new | session.dirty | session.deleted:
        if (
            isinstance(candidate, FiscalYear)
            and candidate.id == year_id
            and candidate.status in _PROTECTED_YEAR_STATUSES
        ):
            return candidate.status

    persisted = session.scalar(select(FiscalYear.status).where(FiscalYear.id == year_id))
    return persisted if persisted in _PROTECTED_YEAR_STATUSES else None



def _company_has_protected_year(session: Session, company_id: int) -> bool:
    # A Company edit in the same transaction as Draft -> Approved is forbidden.
    for candidate in session.new | session.dirty:
        if isinstance(candidate, FiscalYear) and candidate.status in _PROTECTED_YEAR_STATUSES:
            linked_id = candidate.company_id
            if linked_id is None and candidate.company is not None:
                linked_id = candidate.company.id
            if linked_id == company_id:
                return True

    status = session.scalar(
        select(FiscalYear.status).where(
            FiscalYear.company_id == company_id,
            FiscalYear.status.in_(_PROTECTED_YEAR_STATUSES),
        ).limit(1)
    )
    return status is not None


@event.listens_for(Session, "before_flush")
def enforce_audit_invariants(session: Session, _flush_context, _instances) -> None:
    for obj in session.deleted:
        if isinstance(obj, FiscalYear) and obj.status in _PROTECTED_YEAR_STATUSES:
            raise ValueError(
                f"Fiscal year {obj.id} is {obj.status.value.lower()} and cannot be deleted"
            )

    for obj in session.dirty:
        if (
            isinstance(obj, Company)
            and obj.id is not None
            and _company_has_protected_year(session, obj.id)
        ):
            raise ValueError(
                f"Company {obj.id} has approved or locked fiscal years and cannot be mutated"
            )

        if not isinstance(obj, FiscalYear):
            continue

        state = inspect(obj)
        status_history = state.attrs.status.history
        old_status = status_history.deleted[0] if status_history.deleted else obj.status
        if status_history.deleted:
            allowed = {
                FiscalYearStatus.DRAFT: {FiscalYearStatus.APPROVED},
                FiscalYearStatus.APPROVED: {FiscalYearStatus.LOCKED},
                FiscalYearStatus.LOCKED: set(),
            }
            if obj.status not in allowed[old_status]:
                raise ValueError(
                    f"Invalid fiscal-year transition: {old_status.value} -> {obj.status.value}"
                )

        protected_metadata_changed = state.attrs.company.history.has_changes() or any(
            state.attrs[field].history.has_changes() for field in ("company_id", "year")
        )
        if old_status in _PROTECTED_YEAR_STATUSES and protected_metadata_changed:
            raise ValueError(
                f"Fiscal year {obj.id} is {old_status.value.lower()} and its identity cannot be mutated"
            )

    for obj in session.deleted:
        if (
            isinstance(obj, Company)
            and obj.id is not None
            and _company_has_protected_year(session, obj.id)
        ):
            raise ValueError(
                f"Company {obj.id} has approved or locked fiscal years and cannot be deleted"
            )

    protected = (session.new | session.dirty | session.deleted)
    for obj in protected:
        if isinstance(obj, FiscalYear):
            continue
        year_id = _year_id_for(obj, session)
        original_year_id = _persisted_year_id_for(obj, session)
        for affected_year_id in {year_id, original_year_id} - {None}:
            status = _protected_year_status(session, affected_year_id)
            if status is not None:
                raise ValueError(
                    f"Fiscal year {affected_year_id} is {status.value.lower()} and cannot be mutated"
                )
        if year_id is None:
            continue

        if isinstance(obj, MappingRule):
            target_year_id = _resolve_parent_year_id(obj, session, "target_note", "target_note_id", NoteDefinition)
            if target_year_id != obj.year_id:
                raise ValueError("Mapping rule and target note must belong to the same fiscal year")
        if isinstance(obj, StatementLine):
            target_year_id = _resolve_parent_year_id(obj, session, "target_note", "target_note_id", NoteDefinition)
            if target_year_id is not None and target_year_id != year_id:
                raise ValueError("Statement line and target note must belong to the same fiscal year")
