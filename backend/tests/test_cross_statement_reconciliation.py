"""Synthetic candidate-object tests for cross-statement integrity gate."""
from __future__ import annotations

from dataclasses import replace
from decimal import Decimal

import pytest

from aram_backend.balance_sheet_candidate import (
    BalanceSheetCandidate, CandidateBalanceSheetLine,
)
from aram_backend.cash_flow_direct_candidate import DirectCashFlowCandidate
from aram_backend.coverage_preview import CoverageError
from aram_backend.cross_statement_reconciliation import (
    CashBalanceNoteSelection, reconcile_cross_statements,
)
from aram_backend.equity_changes_candidate import EquityChangesCandidate
from aram_backend.income_statement_candidate import IncomeStatementCandidate
from aram_backend.trial_balance_diagnostic import TrialBalanceDiagnostic


SOURCE = "a" * 64
REFS = "b" * 64
POLICY = "c" * 64
TXNS = "d" * 64


def bs(*, equity="100", cash="50", difference="0", eligible=True, lines=None):
    rows = lines or (
        CandidateBalanceSheetLine(
            "Current assets", "CASH1", "", "ASSETS", 1, "Cash",
            cash, cash, "REF-CASH", "POL-CASH",
        ),
        CandidateBalanceSheetLine(
            "Current assets", "A02", "", "ASSETS", 1, "Receivables",
            "150", "150", "REF-AR", "POL-AR",
        ),
        CandidateBalanceSheetLine(
            "Current liabilities", "L01", "", "LIABILITIES", -1, "Payables",
            "-100", "100", "REF-AP", "POL-AP",
        ),
        CandidateBalanceSheetLine(
            "Equity", "E01", "", "EQUITY", -1, "Equity",
            "-100", equity, "REF-EQ", "POL-EQ",
        ),
    )
    return BalanceSheetCandidate(
        company_code="001", fiscal_year=1404,
        source_sha256=SOURCE, note_references_sha256=REFS,
        presentation_policies_sha256=POLICY,
        assets_total=str(Decimal(cash) + Decimal("150")),
        liabilities_total="100", equity_total=equity,
        balance_difference=difference, lines=rows, findings=(),
        arithmetically_balanced=difference == "0",
        eligible_for_analyst_review=eligible,
    )


def income(*, net="40", gross="60", eligible=True):
    return IncomeStatementCandidate(
        company_code="001", fiscal_year=1404, source_sha256=SOURCE,
        note_references_sha256=REFS, presentation_policies_sha256=POLICY,
        revenue_total="100", cost_of_revenue_total="40",
        gross_profit=gross, operating_expense_total="20",
        operating_profit="40", other_income_total="5",
        other_expense_total="2", profit_before_tax="43",
        tax_expense_total="3", net_result=net,
        lines=(), findings=(), eligible_for_analyst_review=eligible,
    )


def equity(*, closing="100", profit="40", eligible=True):
    return EquityChangesCandidate(
        company_code="001", fiscal_year=1404, source_sha256=SOURCE,
        note_references_sha256=REFS, presentation_policies_sha256=POLICY,
        opening_equity_total="60", capital_contributions="0",
        net_profit_loss_movements=profit, dividends="0",
        other_comprehensive_income="0", transfers="0",
        prior_period_adjustments="0", other_movements="0",
        total_movement="40", closing_equity_total=closing,
        rollforward_difference="0", component_totals=(),
        note_movements=(), account_movements=(), findings=(),
        eligible_for_analyst_review=eligible,
    )


def cash(*, closing="50", net="10", eligible=True):
    return DirectCashFlowCandidate(
        company_code="001", fiscal_year=1404, currency="IRR", unit="Rial",
        source_sha256=SOURCE, transaction_ledger_sha256=TXNS,
        classification_policies_sha256=POLICY,
        cash_account_count=1, transaction_count=2,
        opening_cash_and_equivalents="40",
        operating_inflows="30", operating_outflows="20",
        operating_net_cash_flow="10", investing_inflows="0",
        investing_outflows="0", investing_net_cash_flow="0",
        financing_inflows="0", financing_outflows="0",
        financing_net_cash_flow="0", internal_transfer_inflows="0",
        internal_transfer_outflows="0", net_change_in_cash=net,
        closing_cash_and_equivalents=closing, rollforward_difference="0",
        account_reconciliations=(), cash_flow_lines=(), findings=(),
        eligible_for_analyst_review=eligible,
    )


def trial(*, balanced=True):
    return TrialBalanceDiagnostic(
        company_code="001", fiscal_year=1404, source_sha256=SOURCE,
        account_count=4, opening_debit_net_total="0",
        debit_turnover_total="100", credit_turnover_total="100",
        closing_debit_net_total="0", movement_difference="0",
        opening_to_closing_difference="0", findings=(), accounts=(),
        balanced_for_analyst_review=balanced,
    )


def reconcile(**overrides):
    inputs = {
        "balance_sheet": bs(),
        "income_statement": income(),
        "equity_changes": equity(),
        "cash_flow": cash(),
        "trial_balance": trial(),
        "cash_balance_notes": [
            CashBalanceNoteSelection("Current assets", "CASH1", "", "FINANCE-POLICY-CASH")
        ],
    }
    inputs.update(overrides)
    return reconcile_cross_statements(**inputs)


def test_all_five_statements_tie_exactly_without_claiming_approval():
    result = reconcile()
    assert result.eligible_for_analyst_review
    assert not result.findings
    assert result.same_source_snapshot
    assert result.balance_sheet_difference == "0"
    assert result.balance_sheet_equity_difference == "0"
    assert result.net_profit_equity_difference == "0"
    assert result.balance_sheet_cash_total == "50"
    assert result.cash_flow_closing_cash == "50"
    assert result.balance_sheet_cash_difference == "0"
    assert result.income_statement_bridge_valid
    assert result.cash_flow_bridge_valid
    assert result.equity_rollforward_valid
    assert result.trial_balance_arithmetic_valid
    assert len(result.selected_cash_notes) == 1
    assert not result.source_ledger_completeness_verified
    assert not result.accounting_policy_authorized
    assert not result.independently_reviewed
    assert not result.trusted_approvals
    assert not result.official_financial_statement
    assert not result.export_authorized
    assert not result.releasable


def test_different_source_snapshots_block_cross_statement_match():
    result = reconcile(cash_flow=replace(cash(), source_sha256="e" * 64))
    assert not result.eligible_for_analyst_review
    assert not result.same_source_snapshot
    assert "CROSS_STATEMENT_SOURCE_SNAPSHOT_MISMATCH" in result.findings


def test_company_or_year_mismatch_blocks():
    result = reconcile(equity_changes=replace(equity(), company_code="002"))
    assert "CROSS_STATEMENT_COMPANY_YEAR_MISMATCH" in result.findings
    result = reconcile(trial_balance=replace(trial(), fiscal_year=1403))
    assert "CROSS_STATEMENT_COMPANY_YEAR_MISMATCH" in result.findings


def test_balance_sheet_equity_must_equal_equity_statement_closing():
    result = reconcile(equity_changes=equity(closing="99"))
    assert result.balance_sheet_equity_difference == "1"
    assert "BALANCE_SHEET_EQUITY_CLOSING_MISMATCH" in result.findings


def test_income_net_result_must_equal_equity_profit_movement():
    result = reconcile(equity_changes=equity(profit="39"))
    assert result.net_profit_equity_difference == "1"
    assert "INCOME_RESULT_EQUITY_MOVEMENT_MISMATCH" in result.findings


def test_cash_flow_closing_must_equal_selected_balance_sheet_cash_notes():
    result = reconcile(cash_flow=cash(closing="49"))
    assert result.balance_sheet_cash_difference == "1"
    assert "BALANCE_SHEET_CASH_FLOW_CLOSING_MISMATCH" in result.findings


def test_cash_note_selection_must_exist_and_be_an_asset():
    result = reconcile(cash_balance_notes=[
        CashBalanceNoteSelection("Missing", "C99", "", "POLICY")
    ])
    assert "CASH_BALANCE_NOTE_NOT_FOUND_IN_BALANCE_SHEET" in result.findings
    assert "CASH_BALANCE_NOTE_SELECTION_INCOMPLETE" in result.findings
    assert "BALANCE_SHEET_CASH_FLOW_CLOSING_MISMATCH" in result.findings

    wrong = list(bs().lines)
    wrong[0] = replace(wrong[0], category="LIABILITIES")
    result = reconcile(balance_sheet=bs(lines=tuple(wrong)))
    assert "CASH_BALANCE_NOTE_NOT_ASSET" in result.findings


def test_duplicate_or_empty_cash_note_selection_is_rejected():
    selection = CashBalanceNoteSelection("Current assets", "CASH1", "", "POLICY")
    with pytest.raises(CoverageError):
        reconcile(cash_balance_notes=[selection, selection])
    with pytest.raises(CoverageError):
        reconcile(cash_balance_notes=[])


def test_blocked_upstream_candidates_block_cross_statement_gate():
    result = reconcile(income_statement=income(eligible=False))
    assert not result.eligible_for_analyst_review
    assert "INCOME_STATEMENT_CANDIDATE_BLOCKED" in result.findings
    result = reconcile(trial_balance=trial(balanced=False))
    assert "TRIAL_BALANCE_CANDIDATE_BLOCKED" in result.findings
    assert "TRIAL_BALANCE_ARITHMETIC_INVALID" in result.findings


def test_income_statement_internal_bridge_is_recomputed():
    result = reconcile(income_statement=income(gross="61"))
    assert not result.income_statement_bridge_valid
    assert "INCOME_STATEMENT_BRIDGE_INVALID" in result.findings


def test_cash_flow_internal_bridge_is_recomputed():
    result = reconcile(cash_flow=cash(net="9"))
    assert not result.cash_flow_bridge_valid
    assert "CASH_FLOW_BRIDGE_INVALID" in result.findings


def test_balance_sheet_equation_is_recomputed():
    result = reconcile(balance_sheet=bs(difference="1"))
    assert "BALANCE_SHEET_EQUATION_INVALID" in result.findings


def test_equity_rollforward_is_recomputed():
    bad = replace(equity(), rollforward_difference="1")
    result = reconcile(equity_changes=bad)
    assert not result.equity_rollforward_valid
    assert "EQUITY_STATEMENT_ROLLFORWARD_INVALID" in result.findings


def test_invalid_candidate_kind_or_object_is_rejected():
    with pytest.raises(CoverageError):
        reconcile(income_statement={"kind": "bad"})
    with pytest.raises(CoverageError):
        reconcile(balance_sheet=replace(bs(), kind="OFFICIAL"))


def test_approval_flags_cannot_be_smuggled_into_candidate_objects():
    with pytest.raises(CoverageError):
        reconcile(cash_flow=replace(cash(), official_financial_statement=True))
    with pytest.raises(CoverageError):
        reconcile(equity_changes=replace(equity(), releasable=True))


def test_invalid_source_hash_is_rejected():
    with pytest.raises(CoverageError):
        reconcile(balance_sheet=replace(bs(), source_sha256="not-a-hash"))


def test_cash_selection_hash_is_order_independent():
    first = reconcile()
    second = reconcile(cash_balance_notes=[
        CashBalanceNoteSelection("Current assets", "CASH1", "", "FINANCE-POLICY-CASH")
    ])
    assert first.cash_note_selection_sha256 == second.cash_note_selection_sha256


def test_decimal_differences_are_not_rounded_or_tolerated():
    result = reconcile(equity_changes=equity(closing="100.0000000001"))
    assert result.balance_sheet_equity_difference == "-1E-10"
    assert "BALANCE_SHEET_EQUITY_CLOSING_MISMATCH" in result.findings
