import pytest
from pathlib import Path
from decimal import Decimal
from openpyxl import Workbook
from io import BytesIO

from aram_backend.pilot_workbook import validate_pilot_workbook, REQUIRED_SHEETS, EXPECTED_HEADERS


def test_validate_generated_template():
    # Verify the committed blank template is valid (except it has no data, so it should just pass structural checks)
    template_path = Path(__file__).parent.parent.parent / "samples" / "Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx"
    if template_path.exists():
        with open(template_path, "rb") as f:
            res = validate_pilot_workbook(f.read())
        assert res.is_valid, f"Template should be valid, got issues: {res.issues}"

def create_in_memory_workbook(modifications: dict = None) -> bytes:
    wb = Workbook()
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    for sheet_name in REQUIRED_SHEETS:
        sheet = wb.create_sheet(title=sheet_name)
        sheet.append(EXPECTED_HEADERS.get(sheet_name, ["dummy"]))

    # Add valid minimal data
    wb["Company"].append(["C1", "Company 1", 1403, "Draft"])
    wb["Accounts"].append(["C1", 1403, "1001", "Cash", None, None, None, None, None, 100, 50, 20, 130])
    wb["Notes"].append(["C1", 1403, "N1", "Note 1", 1, "Label"])
    wb["Mapping"].append(["C1", 1403, "M1", "1001", "N1", "EXACT"])

    if modifications:
        for sheet_name, mod_func in modifications.items():
            if sheet_name in wb.sheetnames:
                mod_func(wb[sheet_name])

    out = BytesIO()
    wb.save(out)
    return out.getvalue()

def test_minimal_valid_workbook():
    data = create_in_memory_workbook()
    res = validate_pilot_workbook(data)
    assert res.is_valid
    assert len(res.issues) == 0

def test_missing_sheets():
    wb = Workbook()
    wb.create_sheet(title="Company")
    out = BytesIO()
    wb.save(out)

    res = validate_pilot_workbook(out.getvalue())
    assert not res.is_valid
    missing_codes = [i.code for i in res.issues]
    assert "MISSING_SHEET" in missing_codes

def test_incorrect_header_order():
    def modify_headers(sheet):
        # Swap first two headers
        headers = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))[0]
        new_headers = [headers[1], headers[0]] + list(headers[2:])
        sheet.delete_rows(1)
        sheet.insert_rows(1)
        for col_idx, val in enumerate(new_headers, start=1):
            sheet.cell(row=1, column=col_idx, value=val)

    data = create_in_memory_workbook({"Company": modify_headers})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "INVALID_HEADERS" and i.sheet == "Company" for i in res.issues)

def test_numeric_code_rejection():
    def mod(sheet):
        # Change account code to numeric
        sheet.cell(row=2, column=3, value=1001)

    data = create_in_memory_workbook({"Accounts": mod})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "NUMERIC_CODE" and i.field == "account_code" for i in res.issues)

    def mod2(sheet):
        # Change note number to numeric
        sheet.cell(row=2, column=3, value=1)

    data = create_in_memory_workbook({"Notes": mod2})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "NUMERIC_CODE" and i.field == "note_number" for i in res.issues)

def test_duplicate_rows():
    def mod(sheet):
        # Add duplicate account
        sheet.append(["C1", 1403, "1001", "Cash2", None, None, None, None, None, 0, 0, 0, 0])

    data = create_in_memory_workbook({"Accounts": mod})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "DUPLICATE_KEY" and i.sheet == "Accounts" for i in res.issues)

def test_unknown_mapping_account():
    def mod(sheet):
        # Map to unknown account
        sheet.cell(row=2, column=4, value="9999")

    data = create_in_memory_workbook({"Mapping": mod})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "UNKNOWN_ACCOUNT" and i.sheet == "Mapping" for i in res.issues)

def test_invalid_lifecycle_values():
    def mod(sheet):
        sheet.cell(row=2, column=4, value="UnknownStatus")

    data = create_in_memory_workbook({"Company": mod})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "INVALID_STATUS" and i.sheet == "Company" for i in res.issues)

def test_non_zero_closing_delta():
    def mod(sheet):
        # 100 + 50 - 20 = 130, change closing to 140 to force delta
        sheet.cell(row=2, column=13, value=140)

    data = create_in_memory_workbook({"Accounts": mod})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "NON_ZERO_DELTA" for i in res.issues)

def test_nan_and_infinity_rejection():
    def mod_nan(sheet):
        sheet.cell(row=2, column=10, value="NaN")

    data = create_in_memory_workbook({"Accounts": mod_nan})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "INVALID_TYPE" and i.field == "opening" for i in res.issues)

    def mod_inf(sheet):
        sheet.cell(row=2, column=11, value="Infinity")

    data = create_in_memory_workbook({"Accounts": mod_inf})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "INVALID_TYPE" and i.field == "debit" for i in res.issues)

def test_simultaneous_multi_error_collection_and_order():
    def mod_company(sheet):
        sheet.cell(row=2, column=4, value="Bad") # Row 2, INVALID_STATUS
    def mod_accounts(sheet):
        sheet.cell(row=2, column=3, value=123) # Row 2, NUMERIC_CODE
        sheet.cell(row=2, column=13, value=1) # Row 2, NON_ZERO_DELTA

    def mod_mapping(sheet):
        sheet.cell(row=2, column=1, value=1)
        sheet.cell(row=2, column=3, value=1)
        sheet.cell(row=2, column=5, value=1)

    data = create_in_memory_workbook({"Company": mod_company, "Accounts": mod_accounts, "Mapping": mod_mapping})
    res = validate_pilot_workbook(data)
    assert not res.is_valid

    assert any(i.code == "NUMERIC_CODE" and i.sheet == "Mapping" and i.field == "company_code" for i in res.issues)
    assert any(i.code == "NUMERIC_CODE" and i.sheet == "Mapping" and i.field == "mapping_id" for i in res.issues)
    assert any(i.code == "NUMERIC_CODE" and i.sheet == "Mapping" and i.field == "note_number" for i in res.issues)

    # We also get an UNKNOWN_ACCOUNT error in Mapping because '1001' is no longer in accounts_set (it was parsed as numeric 123)
    # The numeric code changes the a_code, so the mapping for "1001" fails. We just filter to the errors we care about for the test.
    relevant_issues = [i for i in res.issues if i.code in {"NUMERIC_CODE", "NON_ZERO_DELTA", "INVALID_STATUS"} and i.sheet in {"Company", "Accounts"}]
    assert len(relevant_issues) == 3

    # Check deterministic ordering (sheet, row, field, code)
    assert relevant_issues[0].sheet == "Accounts"
    assert relevant_issues[0].code == "NUMERIC_CODE" # account_code
    assert relevant_issues[1].sheet == "Accounts"
    assert relevant_issues[1].code == "NON_ZERO_DELTA" # closing
    assert relevant_issues[2].sheet == "Company"
    assert relevant_issues[2].code == "INVALID_STATUS"

def test_missing_cross_sheet():
    def mod_mapping(sheet):
        # M1 references account 9999 which does not exist
        sheet.cell(row=2, column=4, value="9999")
    data = create_in_memory_workbook({"Mapping": mod_mapping})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "UNKNOWN_ACCOUNT" and i.sheet == "Mapping" for i in res.issues)

def test_cross_company_year_references():
    def mod_mapping(sheet):
        # Map to an account that belongs to a different company year
        sheet.cell(row=2, column=2, value=1404)

    def mod_company(sheet):
        # Add year 1404
        sheet.append(["C1", "Company 1", 1404, "Draft"])

    def mod_accounts(sheet):
        # Account is only in 1403
        pass

    data = create_in_memory_workbook({"Company": mod_company, "Mapping": mod_mapping})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    # The mapping should say account not found since it's looking for C1-1404-1001
    assert any(i.code == "UNKNOWN_ACCOUNT" and i.sheet == "Mapping" for i in res.issues)

def test_preserve_leading_zero():
    def mod_accounts(sheet):
        # Change account code to a text string with leading zero
        sheet.cell(row=2, column=3, value="0123")

    def mod_mapping(sheet):
        sheet.cell(row=2, column=4, value="0123")

    data = create_in_memory_workbook({"Accounts": mod_accounts, "Mapping": mod_mapping})
    res = validate_pilot_workbook(data)
    # The leading zero is preserved as text
    assert res.is_valid

def test_incomplete_row():
    def mod_accounts(sheet):
        # Change required field account_code to empty string so it's not completely skipped by the empty row check
        sheet.cell(row=2, column=3, value="")

    data = create_in_memory_workbook({"Accounts": mod_accounts})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "INCOMPLETE_ROW" and i.sheet == "Accounts" for i in res.issues)

    def mod_accounts_none(sheet):
        # The base row already has 1001 in column 3, setting to None doesn't overwrite it properly for iter_rows sometimes
        # We delete the entire row and re-insert an incomplete one
        sheet.delete_rows(2)
        sheet.append(["C1", 1403, None, "Cash", None, None, None, None, None, 100, 50, 20, 130])

    data = create_in_memory_workbook({"Accounts": mod_accounts_none})
    res = validate_pilot_workbook(data)
    assert not res.is_valid
    assert any(i.code == "INCOMPLETE_ROW" and i.sheet == "Accounts" for i in res.issues)

def test_no_persistence(monkeypatch):
    import aram_backend.pilot_workbook as pw

    data = create_in_memory_workbook()

    # We monkeypatch load_workbook to track if it's called
    load_called = False
    orig_load = pw.load_workbook
    def mock_load(*args, **kwargs):
        nonlocal load_called
        load_called = True
        # Ensure we only use data_only and read_only
        assert kwargs.get("data_only") is True
        assert kwargs.get("read_only") is True
        return orig_load(*args, **kwargs)

    monkeypatch.setattr(pw, "load_workbook", mock_load)

    res = pw.validate_pilot_workbook(data)
    assert load_called
    assert res.is_valid

    # It takes bytes, returns object, doesn't interact with DB.
    # The read_only=True parameter on openpyxl guarantees no file writes possible to the BytesIO stream.
