from typing import List, Dict, Any, Tuple
from backend.app.models.entities import ValidationSeverity


class NormalizationValidator:
    """Validates standardized financial record attributes and generates error log payload."""
    def validate_record(self, record: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
        errors = []

        # Validate required Account Code
        if not record.get("account_code"):
            errors.append({
                "severity": ValidationSeverity.ERROR,
                "error_code": "MISSING_ACCOUNT_CODE",
                "message": f"Row {record.get('row_index')}: Account code is missing or empty.",
                "context_data": record,
            })

        # Validate Account Name
        if not record.get("account_name"):
            errors.append({
                "severity": ValidationSeverity.WARNING,
                "error_code": "MISSING_ACCOUNT_NAME",
                "message": f"Row {record.get('row_index')}: Account name is missing.",
                "context_data": record,
            })

        # Validate numeric non-negativity for debit/credit if explicitly negative
        if record.get("debit", 0.0) < 0:
            errors.append({
                "severity": ValidationSeverity.ERROR,
                "error_code": "INVALID_DEBIT_VALUE",
                "message": f"Row {record.get('row_index')}: Debit value cannot be negative ({record.get('debit')}).",
                "context_data": record,
            })

        if record.get("credit", 0.0) < 0:
            errors.append({
                "severity": ValidationSeverity.ERROR,
                "error_code": "INVALID_CREDIT_VALUE",
                "message": f"Row {record.get('row_index')}: Credit value cannot be negative ({record.get('credit')}).",
                "context_data": record,
            })

        is_valid = not any(e["severity"] == ValidationSeverity.ERROR for e in errors)
        return is_valid, errors
