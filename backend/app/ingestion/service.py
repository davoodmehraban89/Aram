import os
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session

from backend.app.models.entities import SourceDocument
from backend.app.services.protection import check_fiscal_year_mutable
from backend.app.ingestion.parsers import compute_file_hash, get_parser


class DuplicateSourceError(Exception):
    """Raised when a source file with identical checksum is registered for the same fiscal year."""
    def __init__(self, filename: str, file_hash: str):
        self.filename = filename
        self.file_hash = file_hash
        super().__init__(f"Source document '{filename}' with hash '{file_hash}' has already been registered.")


def validate_source(file_path: str) -> Dict[str, Any]:
    """
    Validates existence, format, and computes hash for a source file.
    Does not mutate the source file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found at path: '{file_path}'")

    parser = get_parser(file_path)
    metadata = parser.extract_metadata(file_path)
    return metadata


def register_source_document(
    db: Session,
    year_id: int,
    file_path: str,
    doc_type: str,
) -> SourceDocument:
    """
    Validates fiscal year mutability, verifies source file, checks for duplicates,
    and persists a SourceDocument record.
    """
    # Enforce fiscal year mutability protection
    check_fiscal_year_mutable(db, year_id)

    # Validate source file
    metadata = validate_source(file_path)
    file_hash = metadata["file_hash"]
    filename = metadata["filename"]

    # Check for duplicate document in the same fiscal year
    existing = (
        db.query(SourceDocument)
        .filter(SourceDocument.year_id == year_id, SourceDocument.file_hash == file_hash)
        .first()
    )
    if existing:
        raise DuplicateSourceError(filename, file_hash)

    doc = SourceDocument(
        year_id=year_id,
        filename=filename,
        file_hash=file_hash,
        doc_type=doc_type,
        upload_date=datetime.now(timezone.utc).isoformat(),
        processing_status="REGISTERED",
        version=1,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def process_import(
    db: Session,
    year_id: int,
    file_path: str,
    doc_type: str,
) -> Tuple[SourceDocument, Dict[str, Any]]:
    """
    Orchestrates validation, registration, and parsing metadata extraction.
    Updates processing_status upon completion.
    """
    doc = register_source_document(db, year_id, file_path, doc_type)
    metadata = validate_source(file_path)

    doc.processing_status = "PROCESSED"
    db.commit()
    db.refresh(doc)

    return doc, metadata
