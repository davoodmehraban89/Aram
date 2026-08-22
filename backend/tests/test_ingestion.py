import os
import tempfile
import pytest
from backend.app.models import Company, FiscalYear, FiscalYearStatus, SourceDocument
from backend.app.services.protection import LockedFiscalYearError
from backend.app.ingestion.service import (
    validate_source,
    register_source_document,
    process_import,
    DuplicateSourceError,
)
from backend.app.ingestion.parsers import compute_file_hash


@pytest.fixture
def temp_source_files():
    temp_dir = tempfile.mkdtemp()

    xlsx_path = os.path.join(temp_dir, "sample_ledger.xlsx")
    with open(xlsx_path, "wb") as f:
        f.write(b"DUMMY XLSX CONTENT FOR TESTING 1402")

    csv_path = os.path.join(temp_dir, "sample_mapping.csv")
    with open(csv_path, "wb") as f:
        f.write(b"account_code,note\n1001,5")

    pdf_path = os.path.join(temp_dir, "auditor_report.pdf")
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4 DUMMY PDF CONTENT")

    invalid_path = os.path.join(temp_dir, "doc.docx")
    with open(invalid_path, "wb") as f:
        f.write(b"DOCX content")

    yield {
        "xlsx": xlsx_path,
        "csv": csv_path,
        "pdf": pdf_path,
        "invalid": invalid_path,
        "dir": temp_dir,
    }


def test_validate_source_valid_files(temp_source_files):
    meta_xlsx = validate_source(temp_source_files["xlsx"])
    assert meta_xlsx["format"] == "xlsx"
    assert meta_xlsx["filename"] == "sample_ledger.xlsx"
    assert len(meta_xlsx["file_hash"]) == 64

    meta_csv = validate_source(temp_source_files["csv"])
    assert meta_csv["format"] == "csv"

    meta_pdf = validate_source(temp_source_files["pdf"])
    assert meta_pdf["format"] == "pdf"


def test_validate_source_file_not_found():
    with pytest.raises(FileNotFoundError):
        validate_source("non_existent_file.xlsx")


def test_unsupported_format_rejection(temp_source_files):
    with pytest.raises(ValueError) as exc_info:
        validate_source(temp_source_files["invalid"])
    assert "Unsupported file format" in str(exc_info.value)


def test_checksum_validation(temp_source_files):
    hash1 = compute_file_hash(temp_source_files["xlsx"])
    hash2 = compute_file_hash(temp_source_files["xlsx"])
    assert hash1 == hash2
    assert len(hash1) == 64


def test_valid_source_registration(db_session, temp_source_files):
    comp = Company(code="ING1", name="Ingestion Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = register_source_document(
        db_session,
        year_id=fy.id,
        file_path=temp_source_files["xlsx"],
        doc_type="ledger",
    )

    assert doc.id is not None
    assert doc.filename == "sample_ledger.xlsx"
    assert doc.doc_type == "ledger"
    assert doc.processing_status == "REGISTERED"
    assert doc.version == 1


def test_duplicate_file_detection(db_session, temp_source_files):
    comp = Company(code="ING2", name="Ingestion Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    register_source_document(db_session, fy.id, temp_source_files["csv"], "mapping")

    with pytest.raises(DuplicateSourceError) as exc_info:
        register_source_document(db_session, fy.id, temp_source_files["csv"], "mapping")

    assert "sample_mapping.csv" in str(exc_info.value)


def test_database_persistence_and_versioning(db_session, temp_source_files):
    comp = Company(code="ING3", name="Ingestion Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc, meta = process_import(db_session, fy.id, temp_source_files["pdf"], "auditor_report")

    assert doc.processing_status == "PROCESSED"
    assert meta["format"] == "pdf"

    # Query from database to verify persistence
    persisted = db_session.query(SourceDocument).filter_by(id=doc.id).first()
    assert persisted is not None
    assert persisted.filename == "auditor_report.pdf"
    assert persisted.processing_status == "PROCESSED"


def test_locked_year_import_protection(db_session, temp_source_files):
    comp = Company(code="ING4", name="Ingestion Corp 4")
    db_session.add(comp)
    db_session.commit()

    fy_locked = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.LOCKED)
    db_session.add(fy_locked)
    db_session.commit()

    with pytest.raises(LockedFiscalYearError):
        register_source_document(db_session, fy_locked.id, temp_source_files["xlsx"], "ledger")


def test_pdf_metadata_extraction(temp_source_files):
    metadata = validate_source(temp_source_files["pdf"])
    assert metadata["format"] == "pdf"
    assert metadata["file_size"] > 0


def test_csv_metadata_extraction(temp_source_files):
    metadata = validate_source(temp_source_files["csv"])
    assert metadata["format"] == "csv"
    assert metadata["file_size"] > 0
