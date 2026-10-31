"""Adversarial tests for desktop statement drill-down and provenance."""
from dataclasses import replace

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.desktop_five_statement_details import (
    build_preview_details,
)
from aram_backend.desktop_five_statement_integrity import (
    validate_desktop_pipeline_result,
)
from test_five_statement_pipeline_integration import build_pipeline
from aram_backend.synthetic_five_statement_demo import cash_transactions


def test_details_cover_every_candidate_line_and_account_row():
    result = build_pipeline()
    rows = build_preview_details(result)
    expected = (
        len(result.balance_sheet.lines)
        + len(result.income_statement.lines)
        + len(result.equity_changes.note_movements)
        + len(result.equity_changes.account_movements)
        + len(result.cash_flow.cash_flow_lines)
        + len(result.cash_flow.account_reconciliations)
        + len(result.trial_balance.accounts)
    )
    assert len(rows) == expected
    assert {row.statement for row in rows} == {
        "ترازنامه", "سود و زیان", "تغییرات حقوق مالکانه",
        "جریان وجوه نقد", "تراز آزمایشی",
    }
    cash = next(row for row in rows if row.item == "Cash and cash equivalents")
    assert cash.source_detail == "50"
    assert cash.closing_or_presentation == "50"
    profit = next(row for row in rows if row.item == "Revenue")
    assert profit.closing_or_presentation == "40"
    assert all(row.state == "قابل بررسی؛ غیررسمی" for row in rows)
    assert all(len(row.values()) == 11 for row in rows)


def test_cash_transactions_and_trial_balance_accounts_are_individually_traceable():
    result = build_pipeline()
    rows = build_preview_details(result)
    cash_rows = [row for row in rows if row.statement == "جریان وجوه نقد"]
    tb_rows = [row for row in rows if row.statement == "تراز آزمایشی"]
    assert len(cash_rows) == (
        len(result.cash_flow.cash_flow_lines)
        + len(result.cash_flow.account_reconciliations)
    )
    assert any("سند" in row.reference for row in cash_rows)
    assert len(tb_rows) == len(result.trial_balance.accounts)
    assert all("کد حساب" in row.reference for row in tb_rows)


def test_blocked_pipeline_details_are_explicitly_diagnostic():
    result = build_pipeline(transactions=cash_transactions()[:-1])
    assert not result.eligible_for_analyst_review
    rows = build_preview_details(result)
    assert rows
    assert all(row.state == "مسدود؛ صرفاً تشخیصی" for row in rows)


@pytest.mark.parametrize("bad", ["NaN", "Infinity", "1e500", "", "not-a-number"])
def test_invalid_detail_amount_fails_closed(bad):
    result = build_pipeline()
    line = replace(result.balance_sheet.lines[0], presentation_amount=bad)
    changed = replace(
        result, balance_sheet=replace(
            result.balance_sheet, lines=(line,) + result.balance_sheet.lines[1:],
        ),
    )
    with pytest.raises(CoverageError):
        build_preview_details(changed)


def test_invalid_detail_text_with_control_character_fails_closed():
    result = build_pipeline()
    line = replace(result.income_statement.lines[0], line_label="Revenue\nforged")
    changed = replace(
        result, income_statement=replace(
            result.income_statement, lines=(line,) + result.income_statement.lines[1:],
        ),
    )
    with pytest.raises(CoverageError):
        build_preview_details(changed)


def test_row_cap_refuses_truncation_instead_of_silently_hiding_detail(monkeypatch):
    import aram_backend.desktop_five_statement_details as module
    monkeypatch.setattr(module, "MAX_DETAIL_ROWS", 1)
    with pytest.raises(CoverageError, match="ROW_LIMIT"):
        build_preview_details(build_pipeline())


def test_integrity_gate_rejects_forged_approval_flags():
    result = build_pipeline()
    forged = replace(
        result, balance_sheet=replace(
            result.balance_sheet, official_financial_statement=True,
        ),
    )
    with pytest.raises(CoverageError, match="PROVENANCE"):
        validate_desktop_pipeline_result(forged)


def test_integrity_gate_rejects_cross_statement_source_hash_mismatch():
    result = build_pipeline()
    changed = replace(
        result, trial_balance=replace(
            result.trial_balance, source_sha256="0" * 64,
        ),
    )
    with pytest.raises(CoverageError, match="SOURCE_SNAPSHOT"):
        validate_desktop_pipeline_result(changed)


def test_integrity_gate_rejects_tampered_summary_cross_tie():
    result = build_pipeline()
    changed = replace(
        result, balance_sheet=replace(
            result.balance_sheet, equity_total="123",
        ),
    )
    with pytest.raises(CoverageError, match="RECONCILIATION"):
        validate_desktop_pipeline_result(changed)


def test_integrity_gate_rejects_truthy_non_boolean_approval_flag():
    result = build_pipeline()
    forged = replace(
        result, cash_flow=replace(
            result.cash_flow, transaction_ledger_completeness_verified=1,
        ),
    )
    with pytest.raises(CoverageError, match="PROVENANCE"):
        validate_desktop_pipeline_result(forged)


def test_invalid_source_exposure_amount_fails_closed():
    result = build_pipeline()
    line = replace(result.balance_sheet.lines[0], source_closing_exposure="NaN")
    changed = replace(
        result, balance_sheet=replace(
            result.balance_sheet, lines=(line,) + result.balance_sheet.lines[1:],
        ),
    )
    with pytest.raises(CoverageError, match="SOURCE_INVALID"):
        build_preview_details(changed)


@pytest.mark.parametrize("hidden", ["Revenue\u202eforged", "Revenue\x85forged", "Revenue\ufeffforged"])
def test_detail_labels_reject_bidi_and_invisible_control_characters(hidden):
    result = build_pipeline()
    line = replace(result.balance_sheet.lines[0], line_label=hidden)
    changed = replace(
        result, balance_sheet=replace(
            result.balance_sheet, lines=(line,) + result.balance_sheet.lines[1:],
        ),
    )
    with pytest.raises(CoverageError, match="ITEM_INVALID"):
        build_preview_details(changed)


def test_persian_zero_width_non_joiner_is_preserved_in_detail_label():
    result = build_pipeline()
    label = "سود\u200cخالص"
    line = replace(result.income_statement.lines[0], line_label=label)
    changed = replace(
        result, income_statement=replace(
            result.income_statement, lines=(line,) + result.income_statement.lines[1:],
        ),
    )
    rows = build_preview_details(changed)
    assert any(row.item == label for row in rows)


def test_integrity_gate_rejects_malformed_policy_digest():
    result = build_pipeline()
    changed = replace(
        result, income_statement=replace(
            result.income_statement, presentation_policies_sha256="bad-digest",
        ),
    )
    with pytest.raises(CoverageError, match="PROVENANCE_HASH"):
        validate_desktop_pipeline_result(changed)


def test_integrity_gate_rejects_blocked_state_without_explanation():
    result = build_pipeline()
    changed = replace(
        result, reconciliation=replace(
            result.reconciliation, eligible_for_analyst_review=False,
        ),
    )
    with pytest.raises(CoverageError, match="BLOCKED_WITHOUT_FINDINGS"):
        validate_desktop_pipeline_result(changed)


def test_detail_filter_supports_statement_and_cross_column_search():
    from aram_backend.desktop_five_statement_details import filter_preview_details
    rows = build_preview_details(build_pipeline())
    all_rows = filter_preview_details(rows, statement="همه", query="")
    assert all_rows == rows
    income = filter_preview_details(rows, statement="سود و زیان", query="")
    assert income and all(row.statement == "سود و زیان" for row in income)
    revenue = filter_preview_details(rows, statement="همه", query="Revenue")
    assert any(row.item == "Revenue" for row in revenue)
    note = filter_preview_details(rows, statement="سود و زیان", query="یادداشت R01")
    assert len(note) == 1 and note[0].item == "Revenue"


def test_detail_filter_is_casefolded_and_handles_no_match():
    from aram_backend.desktop_five_statement_details import filter_preview_details
    rows = build_preview_details(build_pipeline())
    assert filter_preview_details(rows, statement="همه", query="revenue") == (
        filter_preview_details(rows, statement="همه", query="Revenue")
    )
    assert filter_preview_details(rows, statement="همه", query="no-such-account") == ()


@pytest.mark.parametrize("query", ["x" * 257, "bad\nquery", "bad\u202equery"])
def test_detail_filter_rejects_oversized_and_unsafe_queries(query):
    from aram_backend.desktop_five_statement_details import filter_preview_details
    rows = build_preview_details(build_pipeline())
    with pytest.raises(CoverageError, match="SEARCH_QUERY"):
        filter_preview_details(rows, statement="همه", query=query)


def test_detail_filter_rejects_invalid_statement_or_mutated_row():
    from dataclasses import replace
    from aram_backend.desktop_five_statement_details import (
        PreviewDetail, filter_preview_details,
    )
    rows = build_preview_details(build_pipeline())
    with pytest.raises(CoverageError, match="SEARCH_STATEMENT"):
        filter_preview_details(rows, statement="all", query="")
    forged = (replace(rows[0], trace="hidden\ncontrol"),) + rows[1:]
    with pytest.raises(CoverageError, match="SEARCH_ROW"):
        filter_preview_details(forged, statement="همه", query="")
    with pytest.raises(CoverageError, match="SEARCH_ROWS"):
        filter_preview_details(list(rows), statement="همه", query="")
    assert PreviewDetail is type(rows[0])


def test_detail_filter_handles_large_bounded_row_collection_without_truncation():
    from aram_backend.desktop_five_statement_details import (
        MAX_DETAIL_ROWS, filter_preview_details,
    )
    rows = build_preview_details(build_pipeline())
    repeats, remainder = divmod(MAX_DETAIL_ROWS, len(rows))
    expanded = rows * repeats + rows[:remainder]
    assert len(expanded) == MAX_DETAIL_ROWS
    matches = filter_preview_details(expanded, statement="تراز آزمایشی", query="")
    assert len(matches) == sum(
        1 for row in expanded if row.statement == "تراز آزمایشی"
    )
