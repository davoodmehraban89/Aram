"""Synthetic desktop arithmetic-figure regression tests."""
from __future__ import annotations
from dataclasses import replace

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.desktop_five_statement_figures import (
    SPECS, build_preview_figures,
)
from test_five_statement_pipeline_integration import (
    build_pipeline, cash_transactions,
)


def test_all_five_statements_and_cross_ties_have_visible_exact_figures():
    result = build_pipeline()
    figures = build_preview_figures(result)
    assert len(figures) == len(SPECS) == 28
    by_key = {(item.statement, item.label): item for item in figures}
    assert by_key[("ترازنامه", "دارایی‌ها")].value == "100"
    assert by_key[("ترازنامه", "حقوق مالکانه")].value == "90"
    assert by_key[("سود و زیان", "سود خالص")].value == "20"
    assert by_key[("تغییرات حقوق مالکانه", "پایان دوره")].value == "90"
    assert by_key[("جریان نقد", "نقد پایان دوره")].value == "50"
    assert by_key[("تراز آزمایشی", "گردش بدهکار")].value == "60"
    assert by_key[("تطبیق", "اختلاف نقد")].value == "0"
    assert all("غیررسمی" in row.state for row in figures)


def test_blocked_cash_transaction_shows_diagnostic_not_passed_figures():
    result = build_pipeline(transactions=cash_transactions()[:-1])
    assert not result.eligible_for_analyst_review
    rows = build_preview_figures(result)
    assert len(rows) == len(SPECS)
    assert all("مسدود" in item.state for item in rows)


@pytest.mark.parametrize("bad", ["NaN", "Infinity", "1e500", "", "hello"])
def test_malformed_candidate_amount_is_rejected(bad):
    result = build_pipeline()
    corrupted = replace(
        result, balance_sheet=replace(result.balance_sheet, assets_total=bad),
    )
    with pytest.raises(CoverageError):
        build_preview_figures(corrupted)


def test_report_values_preserve_exact_decimal_scale_without_rounding():
    result = build_pipeline()
    updated_bs = replace(result.balance_sheet, liabilities_total="1.234500")
    modified = replace(result, balance_sheet=updated_bs)
    fields = build_preview_figures(modified)
    assert next(x for x in fields if x.label == "بدهی‌ها").value == "1.234500"


def test_input_must_be_typed_pipeline_result():
    with pytest.raises(CoverageError):
        build_preview_figures({"eligible_for_analyst_review": True})
