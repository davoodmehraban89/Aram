from __future__ import annotations

import hashlib
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from aram_backend.models import FiscalYear, FiscalYearStatus, SourceDocument


ALLOWED_SOURCE_SUFFIXES = frozenset({".csv", ".xlsx"})
ALLOWED_DOCUMENT_TYPES = frozenset(
    {"financial_statement", "general_ledger", "mapping", "trial_balance"}
)


class SourceRegistrationError(ValueError):
    """Raised when source metadata cannot be registered safely."""


def register_source_document(
    session: Session,
    *,
    year_id: int,
    filename: str,
    document_type: str,
    content: bytes,
) -> SourceDocument:
    """Register immutable source metadata without persisting source bytes.

    Re-registering the same bytes for the same fiscal year is idempotent. The
    caller owns the transaction and may inspect the returned row before commit.
    """

    if not filename or "/" in filename or "\\" in filename:
        raise SourceRegistrationError("filename must not contain a path")
    safe_name = Path(filename).name
    if Path(safe_name).suffix.lower() not in ALLOWED_SOURCE_SUFFIXES:
        raise SourceRegistrationError("only .csv and .xlsx source files are supported")
    if document_type not in ALLOWED_DOCUMENT_TYPES:
        raise SourceRegistrationError("unsupported source document type")
    if not content:
        raise SourceRegistrationError("source file must not be empty")

    year = session.get(FiscalYear, year_id)
    if year is None:
        raise SourceRegistrationError(f"fiscal year {year_id} does not exist")
    if year.status is not FiscalYearStatus.DRAFT:
        raise SourceRegistrationError(
            f"fiscal year {year_id} is {year.status.value.lower()} and cannot accept sources"
        )

    file_hash = hashlib.sha256(content).hexdigest()
    existing = session.scalar(
        select(SourceDocument).where(
            SourceDocument.year_id == year_id,
            SourceDocument.file_hash == file_hash,
        )
    )
    if existing is not None:
        if existing.document_type != document_type and existing.filename != safe_name:
            raise SourceRegistrationError(f"document type and filename mismatch for existing content hash")
        if existing.document_type != document_type:
            raise SourceRegistrationError(f"document type mismatch for existing content hash")
        if existing.filename != safe_name:
            raise SourceRegistrationError(f"filename mismatch for existing content hash")
        return existing

    source = SourceDocument(
        year_id=year_id,
        filename=safe_name,
        file_hash=file_hash,
        document_type=document_type,
    )
    session.add(source)
    session.flush()
    return source
