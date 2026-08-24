import hashlib

import pytest

from aram_backend.ingestion import SourceRegistrationError, register_source_document
from aram_backend.models import Company, FiscalYear, FiscalYearStatus, SourceDocument


def make_year(session, year=1404):
    company = Company(code=f"ING-{year}", name="Ingestion Test Company")
    fiscal_year = FiscalYear(company=company, year=year)
    session.add(company)
    session.commit()
    return fiscal_year


def test_registers_hash_and_metadata_without_source_payload(session):
    year = make_year(session)
    payload = b"account_code,amount\n1000,125\n"

    source = register_source_document(
        session,
        year_id=year.id,
        filename="ledger.csv",
        document_type="general_ledger",
        content=payload,
    )
    session.commit()

    assert source.file_hash == hashlib.sha256(payload).hexdigest()
    assert source.filename == "ledger.csv"
    assert not hasattr(source, "content")


def test_registration_is_idempotent_within_a_year(session):
    year = make_year(session)
    arguments = {
        "year_id": year.id,
        "filename": "trial-balance.xlsx",
        "document_type": "trial_balance",
        "content": b"safe-test-bytes",
    }

    first = register_source_document(session, **arguments)
    session.commit()
    second = register_source_document(session, **arguments)
    session.commit()

    assert second.id == first.id
    assert session.query(SourceDocument).count() == 1


def test_same_source_is_isolated_between_fiscal_years(session):
    first_year = make_year(session, 1403)
    second_year = make_year(session, 1404)
    payload = b"same-source"

    first = register_source_document(
        session,
        year_id=first_year.id,
        filename="source.csv",
        document_type="general_ledger",
        content=payload,
    )
    second = register_source_document(
        session,
        year_id=second_year.id,
        filename="source.csv",
        document_type="general_ledger",
        content=payload,
    )
    session.commit()

    assert first.id != second.id
    assert first.file_hash == second.file_hash


@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
def test_protected_year_rejects_source_registration(session, status):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        year.status = FiscalYearStatus.LOCKED
        session.commit()

    with pytest.raises(SourceRegistrationError, match="cannot accept sources"):
        register_source_document(
            session,
            year_id=year.id,
            filename="blocked.xlsx",
            document_type="financial_statement",
            content=b"blocked",
        )


@pytest.mark.parametrize(
    ("filename", "document_type", "content"),
    [
        ("../ledger.csv", "general_ledger", b"data"),
        ("..\\ledger.csv", "general_ledger", b"data"),
        ("ledger.exe", "general_ledger", b"data"),
        ("ledger.csv", "unknown", b"data"),
        ("ledger.csv", "general_ledger", b""),
    ],
)
def test_rejects_unsafe_or_unsupported_source_metadata(
    session, filename, document_type, content
):
    year = make_year(session)

    with pytest.raises(SourceRegistrationError):
        register_source_document(
            session,
            year_id=year.id,
            filename=filename,
            document_type=document_type,
            content=content,
        )

def test_duplicate_registration_different_document_type_rejected(session):
    year = make_year(session)
    arguments = {
        "year_id": year.id,
        "filename": "trial-balance.xlsx",
        "document_type": "trial_balance",
        "content": b"safe-test-bytes-conflict",
    }

    first = register_source_document(session, **arguments)
    session.commit()

    conflict_arguments = arguments.copy()
    conflict_arguments["document_type"] = "general_ledger"

    with pytest.raises(SourceRegistrationError, match="document type mismatch for existing content hash"):
        register_source_document(session, **conflict_arguments)

    session.rollback()
    assert session.query(SourceDocument).count() == 1
    existing = session.query(SourceDocument).first()
    assert existing.document_type == "trial_balance"
    assert existing.filename == "trial-balance.xlsx"

def test_duplicate_registration_different_filename_rejected(session):
    year = make_year(session)
    arguments = {
        "year_id": year.id,
        "filename": "trial-balance.xlsx",
        "document_type": "trial_balance",
        "content": b"safe-test-bytes-conflict-2",
    }

    first = register_source_document(session, **arguments)
    session.commit()

    conflict_arguments = arguments.copy()
    conflict_arguments["filename"] = "other.xlsx"

    with pytest.raises(SourceRegistrationError, match="filename mismatch for existing content hash"):
        register_source_document(session, **conflict_arguments)

    session.rollback()
    assert session.query(SourceDocument).count() == 1
    existing = session.query(SourceDocument).first()
    assert existing.document_type == "trial_balance"
    assert existing.filename == "trial-balance.xlsx"
