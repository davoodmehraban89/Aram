from decimal import Decimal

from aram_backend.ledger_parser import LedgerRecord
from aram_backend.mapping_matcher import classify_ledger_rows, summarize_mapping_coverage


def ledger(row: int, account: str, closing: str) -> LedgerRecord:
    return LedgerRecord(
        row_number=row,
        account_code=account,
        account_name="precision test",
        source_year=1404,
        entry_type="O",
        t1_code=None,
        t2_code=None,
        t3_code=None,
        t4_code=None,
        opening=Decimal("0"),
        debit=Decimal("0"),
        credit=Decimal("0"),
        closing=Decimal(closing),
    )


def test_eligible_closing_subtraction_keeps_large_decimal_precision():
    rows = [
        ledger(3, "8999", "100000000000000000000000000000.01"),
        ledger(4, "8161", "100000000000000000000000000000.02"),
    ]

    summary = summarize_mapping_coverage(classify_ledger_rows(rows, ()))

    assert summary.source_closing == Decimal("200000000000000000000000000000.03")
    assert summary.eligible_closing == Decimal("100000000000000000000000000000.02")
