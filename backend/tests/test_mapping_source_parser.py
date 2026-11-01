from io import BytesIO

import pytest
from openpyxl import Workbook

from aram_backend.mapping_source_parser import (
    MappingSourceParseError,
    parse_mapping_source,
)


HEADERS = [
    "کد حساب",
    "نوع",
    "کد یادداشت",
    "شرح یادداشت",
    "فرمول یادداشت اصلی",
    "فرمول یادداشت فرعی",
    "T1_CODE",
    "T4_CODE",
    "جاری / سرمایه ای",
]


def mapping_bytes(*rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Data"
    sheet.append(HEADERS)
    for row in rows:
        sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def valid_row(**overrides):
    values = {
        "کد حساب": "08161",
        "نوع": "O",
        "کد یادداشت": "10-1",
        "شرح یادداشت": "آزمون",
        "فرمول یادداشت اصلی": "=SUM(A1:A2)",
        "فرمول یادداشت فرعی": "",
        "T1_CODE": "001",
        "T4_CODE": "004",
        "جاری / سرمایه ای": "جاری",
    }
    values.update(overrides)
    return [values[header] for header in HEADERS]


def test_preserves_original_row_number_and_all_dimension_columns():
    records = list(parse_mapping_source(mapping_bytes(valid_row())))

    assert len(records) == 1
    assert records[0].row_number == 2
    assert records[0].account_code == "08161"
    assert records[0].note_code == "10-1"
    assert dict(records[0].source_values)["T1_CODE"] == "001"
    assert dict(records[0].source_values)["T4_CODE"] == "004"
    assert records[0].main_formula == "=SUM(A1:A2)"


def test_skips_blank_rows_without_renumbering_source_rows():
    records = list(
        parse_mapping_source(mapping_bytes([None] * len(HEADERS), valid_row()))
    )

    assert [record.row_number for record in records] == [3]


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("کد حساب", None),
        ("نوع", ""),
        ("کد یادداشت", None),
        ("کد حساب", 12.5),
        ("شرح یادداشت", True),
    ],
)
def test_rejects_incomplete_or_invalid_required_values(field, invalid):
    with pytest.raises(MappingSourceParseError):
        list(parse_mapping_source(mapping_bytes(valid_row(**{field: invalid}))))


def test_does_not_evaluate_mapping_formulas():
    records = list(parse_mapping_source(mapping_bytes(valid_row())))

    assert records[0].main_formula.startswith("=")
    assert records[0].source_values[4][1] == "=SUM(A1:A2)"


def test_preserves_duplicate_mapping_rows_as_distinct_source_evidence():
    records = list(
        parse_mapping_source(mapping_bytes(valid_row(), valid_row()))
    )

    assert [record.row_number for record in records] == [2, 3]
    assert records[0].source_values == records[1].source_values
