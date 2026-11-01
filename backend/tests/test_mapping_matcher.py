from decimal import Decimal

import pytest

from aram_backend.ledger_parser import LedgerRecord
from aram_backend.mapping_source_parser import MappingSourceRow
from aram_backend.mapping_matcher import (
    MappingMatchError,
    build_mapping_rules,
    classify_ledger_rows,
    summarize_mapping_coverage,
)


def mapping_row(row, account="8161", t1=None, js=None, t4=None, note="10-1"):
    return MappingSourceRow(
        row_number=row,
        account_code=account,
        mapping_type="O",
        note_code=note,
        note_description="یادداشت",
        main_formula="",
        sub_formula="",
        source_values=(
            ("T1_CODE", t1),
            ("جاري / سرمایه ای", js),
            ("T4_CODE", t4),
        ),
    )


def ledger_row(row, account="8161", t1=None, t4=None, closing="0"):
    return LedgerRecord(
        row_number=row,
        account_code=account,
        account_name="حساب آزمایشی",
        source_year=1404,
        entry_type="O",
        t1_code=t1,
        t2_code=None,
        t3_code=None,
        t4_code=t4,
        opening=Decimal("0"),
        debit=Decimal("0"),
        credit=Decimal("0"),
        closing=Decimal(closing),
    )


def test_blank_rule_dimensions_are_wildcards_and_populated_dimensions_are_exact():
    rules = build_mapping_rules([
        mapping_row(2, t1=None, t4=None),
        mapping_row(3, t1="01", t4="04"),
    ])

    result = list(classify_ledger_rows([ledger_row(3, t1="01", t4="04")], rules))

    assert result[0].status == "AMBIGUOUS"
    assert result[0].matching_mapping_rows == (2, 3)


def test_specific_rule_does_not_match_missing_ledger_dimension():
    rules = build_mapping_rules([mapping_row(2, t1="01")])

    result = list(classify_ledger_rows([ledger_row(3, t1=None)], rules))

    assert result[0].status == "UNMAPPED"


def test_unique_match_and_unmapped_are_distinguished():
    rules = build_mapping_rules([mapping_row(2, t1="01", t4="04")])
    rows = [ledger_row(3, t1="01", t4="04"), ledger_row(4, t1="02", t4="04")]

    result = list(classify_ledger_rows(rows, rules))

    assert [item.status for item in result] == ["UNIQUE", "UNMAPPED"]


def test_duplicate_source_rules_remain_ambiguous():
    rules = build_mapping_rules([mapping_row(2), mapping_row(3)])

    result = list(classify_ledger_rows([ledger_row(4)], rules))

    assert result[0].status == "AMBIGUOUS"
    assert result[0].matching_mapping_rows == (2, 3)


def test_system_closing_account_is_excluded_but_preserved_in_totals():
    rules = build_mapping_rules([mapping_row(2, account="8999")])
    rows = [ledger_row(3, account="8999", closing="50"), ledger_row(4, closing="20")]

    result = list(classify_ledger_rows(rows, rules))
    summary = summarize_mapping_coverage(result)

    assert [item.status for item in result] == ["EXCLUDED", "UNMAPPED"]
    assert summary.total_source_rows == 2
    assert summary.excluded_rows == 1
    assert summary.eligible_rows == 1
    assert summary.source_closing == Decimal("70")
    assert summary.eligible_closing == Decimal("20")


def test_summary_uses_exact_decimal_exposure():
    rules = build_mapping_rules([mapping_row(2)])
    rows = [
        ledger_row(3, closing="0.1"),
        ledger_row(4, closing="0.2"),
        ledger_row(5, t1="X", closing="-0.3"),
    ]

    summary = summarize_mapping_coverage(classify_ledger_rows(rows, rules))

    assert summary.unique_rows == 2
    assert summary.unmapped_rows == 1
    assert summary.unique_closing == Decimal("0.3")
    assert summary.unmapped_closing == Decimal("-0.3")


def test_missing_required_dimension_header_fails_closed():
    with pytest.raises(MappingMatchError, match="missing dimension headers"):
        build_mapping_rules([mapping_row(2)], dimension_headers=("UNKNOWN",))


def test_boolean_and_fractional_mapping_dimensions_are_rejected():
    for value in (True, 1.5):
        with pytest.raises(MappingMatchError):
            build_mapping_rules([mapping_row(2, t1=value)])


def test_ledger_row_order_and_source_ids_are_preserved():
    rules = build_mapping_rules([mapping_row(7)])
    results = list(classify_ledger_rows(
        [ledger_row(99), ledger_row(11)], rules
    ))

    assert [item.ledger_row for item in results] == [99, 11]
    assert [item.matching_mapping_rows for item in results] == [(7,), (7,)]

def test_populated_current_capital_dimension_fails_closed_until_ledger_exposes_it():
    rules = build_mapping_rules([mapping_row(2, js="جاری")])

    result = list(classify_ledger_rows([ledger_row(3)], rules))

    assert result[0].status == "UNMAPPED"
    assert result[0].matching_mapping_rows == ()
