from io import BytesIO

import pytest
from openpyxl import Workbook

from aram_backend.workbook_inspection import WorkbookInspectionError, inspect_xlsx


def workbook_bytes(sheet_rows):
    workbook = Workbook()
    default = workbook.active
    workbook.remove(default)
    for sheet_name, rows in sheet_rows:
        sheet = workbook.create_sheet(sheet_name)
        for row in rows:
            sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def test_inspects_accepted_general_ledger_structure():
    headers = [
        "حساب",
        "ACCOUNT_NAME",
        "year",
        "OPENING",
        "Debit",
        "Credit",
        "CLOSING",
    ]
    content = workbook_bytes([("Source", [["source ledger"], headers])])

    result = inspect_xlsx(content, document_type="general_ledger")

    assert result.data_sheet == "Source"
    assert result.header_row == 2
    assert result.headers == tuple(headers)


def test_inspects_accepted_mapping_structure():
    headers = [
        "کد حساب",
        "نوع",
        "کد یادداشت",
        "شرح یادداشت",
        "فرمول یادداشت اصلی",
        "فرمول یادداشت فرعی",
    ]
    content = workbook_bytes([("Data", [headers])])

    result = inspect_xlsx(content, document_type="mapping")

    assert result.data_sheet == "Data"
    assert result.header_row == 1


def test_inspects_primary_financial_statement_sheet_set():
    names = ["سودوزيان", "وضعيت مالي", "حقوق مالكانه", "جريان هاي نقدي"]
    content = workbook_bytes([(name, []) for name in names])

    result = inspect_xlsx(content, document_type="financial_statement")

    assert result.sheet_names == tuple(names)
    assert result.headers == ()


@pytest.mark.parametrize(
    "content",
    [
        workbook_bytes([("Wrong", [["not the expected sheet"]])]),
        workbook_bytes([("Source", [["source ledger"], ["حساب"]])]),
        b"not-an-xlsx-file",
    ],
)
def test_rejects_invalid_or_mismatched_workbooks(content):
    with pytest.raises(WorkbookInspectionError):
        inspect_xlsx(content, document_type="general_ledger")


def test_rejects_document_type_without_an_xlsx_profile():
    content = workbook_bytes([("Sheet", [])])

    with pytest.raises(WorkbookInspectionError, match="no XLSX inspection profile"):
        inspect_xlsx(content, document_type="trial_balance")
