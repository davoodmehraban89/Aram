from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

from backend.app.models.entities import (
    NormalizedFinancialRecord,
    ValidationErrorLog,
    MappingTemplate,
)
from backend.app.services.protection import check_fiscal_year_mutable
from backend.app.normalization.mapper import NormalizationMapper
from backend.app.normalization.validator import NormalizationValidator
from backend.app.normalization.analyzer import analyze_source_structure


def normalize_and_persist_records(
    db: Session,
    year_id: int,
    source_document_id: int,
    raw_rows: List[Dict[str, Any]],
    template_name: str = "DEFAULT",
) -> Tuple[List[NormalizedFinancialRecord], List[ValidationErrorLog]]:
    """
    Normalizes raw financial row data using mapping template and validation framework,
    then persists NormalizedFinancialRecord and ValidationErrorLog entities.
    Enforces fiscal year mutability protection.
    """
    # Enforce fiscal year immutability check
    check_fiscal_year_mutable(db, year_id)

    # Fetch mapping template if exists
    template_obj = (
        db.query(MappingTemplate)
        .filter(MappingTemplate.year_id == year_id, MappingTemplate.template_name == template_name)
        .first()
    )
    mapping_dict = template_obj.column_mappings if template_obj else None

    mapper = NormalizationMapper(mapping_dict)
    validator = NormalizationValidator()

    normalized_records: List[NormalizedFinancialRecord] = []
    validation_logs: List[ValidationErrorLog] = []

    for idx, raw_row in enumerate(raw_rows, start=1):
        mapped_dict = mapper.map_row(raw_row, row_index=idx)
        is_valid, errors = validator.validate_record(mapped_dict)

        # Log errors / warnings
        for err in errors:
            log_entry = ValidationErrorLog(
                year_id=year_id,
                source_document_id=source_document_id,
                severity=err["severity"],
                error_code=err["error_code"],
                message=err["message"],
                context_data=err["context_data"],
            )
            db.add(log_entry)
            validation_logs.append(log_entry)

        # Only persist valid records (or records with warnings only)
        if is_valid:
            record = NormalizedFinancialRecord(
                year_id=year_id,
                source_document_id=source_document_id,
                row_index=mapped_dict["row_index"],
                account_code=mapped_dict["account_code"],
                account_name=mapped_dict["account_name"],
                debit=mapped_dict["debit"],
                credit=mapped_dict["credit"],
                net_amount=mapped_dict["net_amount"],
                t1=mapped_dict["t1"],
                t2=mapped_dict["t2"],
                t3=mapped_dict["t3"],
                t4=mapped_dict["t4"],
                raw_payload=mapped_dict["raw_payload"],
            )
            db.add(record)
            normalized_records.append(record)

    db.commit()

    for rec in normalized_records:
        db.refresh(rec)
    for log in validation_logs:
        db.refresh(log)

    return normalized_records, validation_logs
