from decimal import Decimal
from io import BytesIO

import pytest
from openpyxl import Workbook

from aram_backend.ledger_parser import LedgerParseError, parse_general_ledger


HEADERS = [
    "حساب",
    "ACCOUNT_NAME",
    "year",
    "نوع",
    "T1_CODE",
    "T2_CODE",
    "T3_CODE",
    "T4_CODE",
    "OPENING",
    "Debit",
    "Credit",
    "CLOSING",
]


def ledger_bytes(*rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Source"
    sheet.append(["source ledger"])
    sheet.append(HEADERS)
    for row in rows:
        sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def valid_row(**overrides):
    values = {
        "حساب": "0001",
        "ACCOUNT_NAME": "Test account",
        "year": "1404",
        "نوع": "O",
        "T1_CODE": None,
        "T2_CODE": None,
        "T3_CODE": None,
        "T4_CODE": None,
        "OPENING": "0",
        "Debit": "0",
        "Credit": "0",
        "CLOSING": "0",
    }
    values.update(overrides)
    return [values[header] for header in HEADERS]


def test_streams_typed_records_without_calculation():
    records = list(parse_general_ledger(ledger_bytes(valid_row())))

    assert len(records) == 1
    assert records[0].row_number == 3
    assert records[0].account_code == "0001"
    assert records[0].opening == Decimal("0")
    assert records[0].closing == Decimal("0")


def test_skips_completely_blank_rows():
    records = list(parse_general_ledger(ledger_bytes([None] * len(HEADERS), valid_row())))

    assert [record.row_number for record in records] == [4]


@pytest.mark.parametrize(
    ("field", "invalid", "message"),
    [
        ("Debit", "NaN", "must be finite"),
        ("Credit", "Infinity", "must be finite"),
        ("CLOSING", "not-numeric", "is not numeric"),
        ("ACCOUNT_NAME", None, "is required"),
        ("year", "1404.5", "positive integer"),
        ("T1_CODE", 12.5, "integer code"),
    ],
)
def test_rejects_unsafe_or_incomplete_rows(field, invalid, message):
    content = ledger_bytes(valid_row(**{field: invalid}))

    with pytest.raises(LedgerParseError, match=message):
        list(parse_general_ledger(content))
