import hashlib
from pathlib import Path

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def _setup_sheet(wb: Workbook, sheet_name: str, headers: list[str]) -> Worksheet:
    sheet = wb.create_sheet(title=sheet_name)
    sheet.append(headers)
    return sheet


def generate_template(output_path: Path) -> str:
    """Generates the blank Pilot template and returns its SHA-256."""
    wb = Workbook()
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    # 1. Company
    _setup_sheet(wb, "Company", ["company_code", "company_name", "fiscal_year", "status"])

    # 2. Accounts
    _setup_sheet(wb, "Accounts", [
        "company_code", "fiscal_year", "account_code", "account_name",
        "t1_code", "t2_code", "t3_code", "t4_code", "nature",
        "opening", "debit", "credit", "closing"
    ])

    # 3. Notes
    _setup_sheet(wb, "Notes", [
        "company_code", "fiscal_year", "note_number", "title", "row_order", "label"
    ])

    # 4. Mapping
    _setup_sheet(wb, "Mapping", [
        "company_code", "fiscal_year", "mapping_id", "account_code",
        "note_number", "mapping_type"
    ])

    # 5. Test_Log
    _setup_sheet(wb, "Test_Log", ["test_id", "description", "result"])

    # 6. Checks
    checks_sheet = _setup_sheet(wb, "Checks", ["check_name", "status"])

    # 7. Guide_FA
    guide_sheet = _setup_sheet(wb, "Guide_FA", ["راهنما (Guide)"])

    # 8. Lists
    lists_sheet = _setup_sheet(wb, "Lists", ["List_Name", "Value"])

    # Add checks
    checks_sheet.append(["required-field completeness", "PENDING"])
    checks_sheet.append(["duplicate accounts", "PENDING"])
    checks_sheet.append(["unknown mapping accounts", "PENDING"])
    checks_sheet.append(["invalid mappings", "PENDING"])
    checks_sheet.append(["non-zero closing_delta", "PENDING"])

    # Add guide
    guide_sheet.append(["لطفاً مقادیر شرکت، حساب‌ها، یادداشت‌ها و نقشه‌برداری را با رعایت یکپارچگی سال مالی وارد کنید."])
    guide_sheet.append(["فیلدهای کد حساب باید متنی باشند. از وارد کردن اعداد بدون فرمت متنی خودداری کنید."])

    # Add lists
    lists_sheet.append(["status", "Draft"])
    lists_sheet.append(["status", "Reviewed"])
    lists_sheet.append(["status", "Approved"])
    lists_sheet.append(["mapping_type", "EXACT"])
    lists_sheet.append(["mapping_type", "FORMULA"])

    wb.save(output_path)

    with open(output_path, "rb") as f:
        file_bytes = f.read()
    return hashlib.sha256(file_bytes).hexdigest()

if __name__ == "__main__":
    out_dir = Path(__file__).parent.parent.parent / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx"
    sha = generate_template(out_path)
    print(f"Generated {out_path.name}")
    print(f"SHA-256: {sha}")
