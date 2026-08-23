import pytest
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    SourceDocument,
    MappingTemplate,
    NormalizedFinancialRecord,
    ValidationErrorLog,
    ValidationSeverity,
)
from backend.app.services.protection import LockedFiscalYearError
from backend.app.normalization.analyzer import detect_columns, analyze_source_structure
from backend.app.normalization.mapper import NormalizationMapper
from backend.app.normalization.validator import NormalizationValidator
from backend.app.normalization.service import normalize_and_persist_records


def test_source_analysis_and_column_detection():
    analysis = analyze_source_structure(
        file_path="dummy.csv",
        rows_data=[{"account_code": "101", "account_name": "Cash"}]
    )
    assert analysis["total_rows"] == 1


def test_normalization_mapper_default_column_mapping():
    mapper = NormalizationMapper()
    raw_row = {
        "کد حساب": "110101",
        "نام حساب": "موجود نقد",
        "بدهکار": "1,500,000",
        "بستانکار": "0",
        "tafsil1": "T101",
    }
    mapped = mapper.map_row(raw_row, row_index=1)
    assert mapped["account_code"] == "110101"
    assert mapped["account_name"] == "موجود نقد"
    assert mapped["debit"] == 1500000.0
    assert mapped["credit"] == 0.0
    assert mapped["net_amount"] == 1500000.0
    assert mapped["t1"] == "T101"


def test_normalization_validator_missing_account_code():
    validator = NormalizationValidator()
    invalid_record = {
        "row_index": 2,
        "account_code": "",
        "account_name": "Test Account",
        "debit": 100.0,
        "credit": 0.0,
    }
    is_valid, errors = validator.validate_record(invalid_record)
    assert is_valid is False
    assert any(e["error_code"] == "MISSING_ACCOUNT_CODE" for e in errors)


def test_normalization_validator_negative_values():
    validator = NormalizationValidator()
    invalid_record = {
        "row_index": 3,
        "account_code": "1001",
        "account_name": "Test Account",
        "debit": -50.0,
        "credit": 0.0,
    }
    is_valid, errors = validator.validate_record(invalid_record)
    assert is_valid is False
    assert any(e["error_code"] == "INVALID_DEBIT_VALUE" for e in errors)


def test_normalize_and_persist_records_success(db_session):
    comp = Company(code="NORM1", name="Norm Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger.csv", file_hash="hash123", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    raw_rows = [
        {"account_code": "1101", "account_name": "Cash", "debit": "1000.00", "credit": "0"},
        {"account_code": "2101", "account_name": "Accounts Payable", "debit": "0", "credit": "1000.00"},
    ]

    records, logs = normalize_and_persist_records(db_session, fy.id, doc.id, raw_rows)
    assert len(records) == 2
    assert len(logs) == 0

    persisted_records = db_session.query(NormalizedFinancialRecord).filter_by(source_document_id=doc.id).all()
    assert len(persisted_records) == 2
    assert persisted_records[0].account_code == "1101"
    assert persisted_records[1].account_code == "2101"


def test_normalize_and_persist_records_validation_errors(db_session):
    comp = Company(code="NORM2", name="Norm Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger_err.csv", file_hash="hash456", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    raw_rows = [
        {"account_code": "", "account_name": "Missing Code Acc", "debit": "500", "credit": "0"},
    ]

    records, logs = normalize_and_persist_records(db_session, fy.id, doc.id, raw_rows)
    assert len(records) == 0
    assert len(logs) >= 1

    persisted_logs = db_session.query(ValidationErrorLog).filter_by(source_document_id=doc.id).all()
    assert len(persisted_logs) >= 1
    assert persisted_logs[0].error_code == "MISSING_ACCOUNT_CODE"


def test_custom_mapping_template(db_session):
    comp = Company(code="NORM3", name="Norm Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    tmpl = MappingTemplate(
        year_id=fy.id,
        template_name="CUSTOM_TEMPLATE",
        column_mappings={
            "account_code": ["cust_code"],
            "account_name": ["cust_name"],
            "debit": ["cust_bed"],
            "credit": ["cust_bes"],
        }
    )
    db_session.add(tmpl)

    doc = SourceDocument(year_id=fy.id, filename="custom_ledger.csv", file_hash="hash789", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    raw_rows = [
        {"cust_code": "9901", "cust_name": "Custom Account", "cust_bed": "250.00", "cust_bes": "0"}
    ]

    records, logs = normalize_and_persist_records(db_session, fy.id, doc.id, raw_rows, template_name="CUSTOM_TEMPLATE")
    assert len(records) == 1
    assert records[0].account_code == "9901"
    assert records[0].account_name == "Custom Account"


def test_locked_year_normalization_protection(db_session):
    comp = Company(code="NORM4", name="Norm Corp 4")
    db_session.add(comp)
    db_session.commit()

    fy_locked = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.LOCKED)
    db_session.add(fy_locked)
    db_session.commit()

    doc = SourceDocument(year_id=fy_locked.id, filename="locked.csv", file_hash="hash999", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    raw_rows = [{"account_code": "1001", "account_name": "Cash", "debit": "100", "credit": "0"}]

    with pytest.raises(LockedFiscalYearError):
        normalize_and_persist_records(db_session, fy_locked.id, doc.id, raw_rows)


def test_invalid_numeric_conversion_handling():
    mapper = NormalizationMapper()
    raw_row = {
        "account_code": "1001",
        "account_name": "Cash",
        "debit": "INVALID_NUMERIC",
        "credit": "100.00",
    }
    mapped = mapper.map_row(raw_row, row_index=1)
    assert mapped["debit"] == 0.00
    assert mapped["credit"] == 100.00


def test_validation_warning_logging(db_session):
    comp = Company(code="NORM5", name="Norm Corp 5")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="warn.csv", file_hash="hash_warn", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    raw_rows = [{"account_code": "1001", "account_name": "", "debit": "100", "credit": "0"}]

    records, logs = normalize_and_persist_records(db_session, fy.id, doc.id, raw_rows)
    # Warnings allow record persistence
    assert len(records) == 1
    assert len(logs) == 1
    assert logs[0].severity == ValidationSeverity.WARNING
    assert logs[0].error_code == "MISSING_ACCOUNT_NAME"
