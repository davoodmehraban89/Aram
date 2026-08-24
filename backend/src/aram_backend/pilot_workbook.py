from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from io import BytesIO
from typing import Any

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    sheet: str
    row: int
    field: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    issues: list[ValidationIssue]


REQUIRED_SHEETS = [
    "Company",
    "Accounts",
    "Notes",
    "Mapping",
    "Test_Log",
    "Checks",
    "Guide_FA",
    "Lists",
]

EXPECTED_HEADERS = {
    "Company": ["company_code", "company_name", "fiscal_year", "status"],
    "Accounts": [
        "company_code",
        "fiscal_year",
        "account_code",
        "account_name",
        "t1_code",
        "t2_code",
        "t3_code",
        "t4_code",
        "nature",
        "opening",
        "debit",
        "credit",
        "closing",
    ],
    "Notes": ["company_code", "fiscal_year", "note_number", "title", "row_order", "label"],
    "Mapping": ["company_code", "fiscal_year", "mapping_id", "account_code", "note_number", "mapping_type"],
    "Test_Log": ["test_id", "description", "result"],
    "Checks": ["check_name", "status"],
    "Guide_FA": ["راهنما (Guide)"],
    "Lists": ["List_Name", "Value"],
}

def _validate_headers(sheet: Worksheet, sheet_name: str, issues: list[ValidationIssue]) -> bool:
    if sheet_name not in EXPECTED_HEADERS:
        return True

    expected = EXPECTED_HEADERS[sheet_name]
    row_iter = sheet.iter_rows(min_row=1, max_row=1, values_only=True)
    try:
        actual_row = next(row_iter)
    except StopIteration:
        actual_row = []

    actual = [str(val).strip() if val is not None else "" for val in actual_row]

    if actual[:len(expected)] != expected:
        issues.append(
            ValidationIssue(
                severity="ERROR",
                code="INVALID_HEADERS",
                sheet=sheet_name,
                row=1,
                field="Headers",
                message=f"Expected headers {expected}, got {actual}",
            )
        )
        return False
    return True

def validate_pilot_workbook(workbook_bytes: bytes) -> ValidationResult:
    """Preflight API to validate a Pilot workbook without persisting data."""
    issues: list[ValidationIssue] = []

    try:
        wb = load_workbook(filename=BytesIO(workbook_bytes), data_only=True, read_only=True)
    except Exception as e:
        issues.append(
            ValidationIssue(
                severity="ERROR",
                code="INVALID_FILE",
                sheet="Global",
                row=0,
                field="File",
                message=f"Failed to load workbook: {e}",
            )
        )
        return ValidationResult(is_valid=False, issues=issues)

    for required in REQUIRED_SHEETS:
        if required not in wb.sheetnames:
            issues.append(
                ValidationIssue(
                    severity="ERROR",
                    code="MISSING_SHEET",
                    sheet=required,
                    row=0,
                    field="Sheet",
                    message=f"Missing required sheet: {required}",
                )
            )

    if issues:
        wb.close()
        return ValidationResult(is_valid=False, issues=issues)

    for sheet_name in REQUIRED_SHEETS:
        _validate_headers(wb[sheet_name], sheet_name, issues)

    if issues:
        wb.close()
        return ValidationResult(is_valid=False, issues=issues)

    defined_company_years = set()
    accounts_set = set()

    # Validate Company
    for row_idx, row in enumerate(wb["Company"].iter_rows(min_row=2, values_only=True), start=2):
        if not any(row):
            continue
        c_code, c_name, year, status = row[:4]
        if not c_code or not year:
            continue

        if isinstance(c_code, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Company", row_idx, "company_code", "Codes must be text, not numeric"))

        try:
            year_int = int(year)
            if year_int <= 0:
                raise ValueError
        except (ValueError, TypeError):
            issues.append(ValidationIssue("ERROR", "INVALID_TYPE", "Company", row_idx, "fiscal_year", "Must be positive integer"))
            continue

        key = (str(c_code), year_int)
        if key in defined_company_years:
            issues.append(ValidationIssue("ERROR", "DUPLICATE_KEY", "Company", row_idx, "company_code", "Duplicate company/year"))
        defined_company_years.add(key)

        if status not in {"Draft", "Reviewed", "Approved"}:
            issues.append(ValidationIssue("ERROR", "INVALID_STATUS", "Company", row_idx, "status", "Invalid status"))

    # Validate Accounts
    for row_idx, row in enumerate(wb["Accounts"].iter_rows(min_row=2, values_only=True), start=2):
        padded_row = list(row) + [None] * (max(13, len(row)) - len(row))

        # Limit to the expected length
        is_empty = all(val is None or str(val).strip() == "" for val in padded_row[:13])
        if is_empty:
            continue

        c_code, year, a_code = padded_row[:3]
        if not c_code or str(c_code).strip() == "" or not year or str(year).strip() == "" or a_code is None or str(a_code).strip() == "":
            issues.append(ValidationIssue("ERROR", "INCOMPLETE_ROW", "Accounts", row_idx, "Keys", "Missing company, year or account code"))
            continue

        if isinstance(c_code, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Accounts", row_idx, "company_code", "Codes must be text, not numeric"))

        if isinstance(a_code, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Accounts", row_idx, "account_code", "Codes must be text, not numeric"))

        try:
            year_int = int(year)
        except (ValueError, TypeError):
            year_int = None

        key = (str(c_code), year_int)
        if key not in defined_company_years:
            issues.append(ValidationIssue("ERROR", "UNKNOWN_COMPANY_YEAR", "Accounts", row_idx, "company_code", "References undefined company/year"))

        a_code_str = str(a_code)
        account_key = (str(c_code), year_int, a_code_str)
        if account_key in accounts_set:
            issues.append(ValidationIssue("ERROR", "DUPLICATE_KEY", "Accounts", row_idx, "account_code", "Duplicate account code"))
        accounts_set.add(account_key)

        # Financials
        financials = padded_row[9:13]
        parsed_fin = []
        for i, val in enumerate(financials):
            try:
                dec = Decimal(str(val))
                if not dec.is_finite():
                    raise InvalidOperation
                parsed_fin.append(dec)
            except (InvalidOperation, TypeError):
                col_name = ["opening", "debit", "credit", "closing"][i]
                issues.append(ValidationIssue("ERROR", "INVALID_TYPE", "Accounts", row_idx, col_name, "Must be a finite Decimal"))
                parsed_fin.append(None)

        if all(f is not None for f in parsed_fin):
            op, db, cr, cl = parsed_fin
            delta = op + db - cr - cl
            if delta != Decimal(0):
                issues.append(ValidationIssue("ERROR", "NON_ZERO_DELTA", "Accounts", row_idx, "closing", f"closing_delta is non-zero: {delta}"))

    # Validate Notes
    notes_set = set()
    for row_idx, row in enumerate(wb["Notes"].iter_rows(min_row=2, values_only=True), start=2):
        if not any(row):
            continue
        c_code, year, n_num = row[:3]
        if not c_code or not year or n_num is None:
            issues.append(ValidationIssue("ERROR", "INCOMPLETE_ROW", "Notes", row_idx, "Keys", "Missing keys"))
            continue

        if isinstance(c_code, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Notes", row_idx, "company_code", "Codes must be text, not numeric"))

        if isinstance(n_num, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Notes", row_idx, "note_number", "Codes must be text, not numeric"))

        try:
            year_int = int(year)
        except (ValueError, TypeError):
            year_int = None

        key = (str(c_code), year_int)
        if key not in defined_company_years:
            issues.append(ValidationIssue("ERROR", "UNKNOWN_COMPANY_YEAR", "Notes", row_idx, "company_code", "References undefined company/year"))

        # Row order uniqueness per note is not strictly duplicate note_number error, but combination
        row_order = row[4]
        note_key = (str(c_code), year_int, str(n_num), row_order)
        if note_key in notes_set:
            issues.append(ValidationIssue("ERROR", "DUPLICATE_KEY", "Notes", row_idx, "row_order", "Duplicate row order in note"))
        notes_set.add(note_key)

    # Validate Mapping
    mappings_set = set()
    for row_idx, row in enumerate(wb["Mapping"].iter_rows(min_row=2, values_only=True), start=2):
        if not any(row):
            continue
        c_code, year, m_id, a_code = row[:4]
        target_n_num = row[4] if len(row) > 4 else None

        if not c_code or not year or m_id is None or a_code is None or target_n_num is None:
            issues.append(ValidationIssue("ERROR", "INCOMPLETE_ROW", "Mapping", row_idx, "Keys", "Missing keys"))
            continue

        if isinstance(c_code, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Mapping", row_idx, "company_code", "Codes must be text, not numeric"))

        if isinstance(m_id, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Mapping", row_idx, "mapping_id", "Codes must be text, not numeric"))

        if isinstance(a_code, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Mapping", row_idx, "account_code", "Codes must be text, not numeric"))

        if isinstance(target_n_num, (int, float)):
            issues.append(ValidationIssue("ERROR", "NUMERIC_CODE", "Mapping", row_idx, "note_number", "Codes must be text, not numeric"))

        try:
            year_int = int(year)
        except (ValueError, TypeError):
            year_int = None

        key = (str(c_code), year_int)
        if key not in defined_company_years:
            issues.append(ValidationIssue("ERROR", "UNKNOWN_COMPANY_YEAR", "Mapping", row_idx, "company_code", "References undefined company/year"))

        mapping_key = (str(c_code), year_int, str(m_id))
        if mapping_key in mappings_set:
            issues.append(ValidationIssue("ERROR", "DUPLICATE_KEY", "Mapping", row_idx, "mapping_id", "Duplicate mapping id"))
        mappings_set.add(mapping_key)

        account_key = (str(c_code), year_int, str(a_code))
        if account_key not in accounts_set and key in defined_company_years:
            issues.append(ValidationIssue("ERROR", "UNKNOWN_ACCOUNT", "Mapping", row_idx, "account_code", "Mapped account not found in Accounts sheet"))

    wb.close()

    # Sort issues deterministically
    issues.sort(key=lambda i: (i.sheet, i.row, i.field, i.code))

    return ValidationResult(is_valid=len(issues) == 0, issues=issues)
