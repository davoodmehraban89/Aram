"""Synthetic candidate-object tests for cross-statement integrity gate."""
from __future__ import annotations

from dataclasses import replace
from decimal import Decimal

import pytest

from aram_backend.balance_sheet_candidate import (
    BalanceSheetCandidate, CandidateBalanceSheetLine,
)
from aram_backend.cash_flow_direct_candidate import (
    CashAccountReconciliation, CashFlowLine, DirectCashFlowCandidate,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.cross_statement_reconciliation import (
    CashBalanceNoteSelection, reconcile_cross_statements,
)
from aram_backend.equity_changes_candidate import (
    EquityAccountMovement, EquityChangesCandidate, EquityComponentTotal,
    EquityNoteMovement,
)
from aram_backend.income_statement_candidate import (
    CandidateIncomeStatementLine, IncomeStatementCandidate,
)
from aram_backend.trial_balance_diagnostic import TrialBalanceAccount, TrialBalanceDiagnostic


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
        lines=(
            CandidateIncomeStatementLine(
                "Revenue", "R01", "", "REVENUE", -1, "Revenue",
                "-100", "100", "REF-REV", "POL-REV",
            ),
            CandidateIncomeStatementLine(
                "Cost", "C01", "", "COST_OF_REVENUE", 1, "Cost of revenue",
                "40", "40", "REF-COST", "POL-COST",
            ),
            CandidateIncomeStatementLine(
                "Operating", "O01", "", "OPERATING_EXPENSE", 1, "Operating expense",
                "20", "20", "REF-OPEX", "POL-OPEX",
            ),
            CandidateIncomeStatementLine(
                "Other income", "I01", "", "OTHER_INCOME", -1, "Other income",
                "-5", "5", "REF-OIN", "POL-OIN",
            ),
            CandidateIncomeStatementLine(
                "Other expense", "X01", "", "OTHER_EXPENSE", 1, "Other expense",
                "2", "2", "REF-OEX", "POL-OEX",
            ),
            CandidateIncomeStatementLine(
                "Tax", "T01", "", "TAX_EXPENSE", 1, "Tax",
                "3", "3", "REF-TAX", "POL-TAX",
            ),
        ), findings=(), eligible_for_analyst_review=eligible,
    )


def equity(*, closing="100", profit="40", eligible=True):
    closing_value = Decimal(closing)
    profit_value = Decimal(profit)
    rollforward = Decimal("60") + profit_value - closing_value
    account = EquityAccountMovement(
        account_code="EQ1", account_name="Equity", source_excel_row=3,
        source_row=2, statement_section="Equity", note_number="E01",
        subnote_code="", equity_component="RETAINED_EARNINGS",
        movement_category="NET_PROFIT_LOSS", sign_multiplier=-1,
        opening_balance="60", debit_turnover="0", credit_turnover=profit,
        movement_amount=profit, closing_balance=closing,
        policy_evidence_ref="POL-EQ",
    )
    note = EquityNoteMovement(
        statement_section="Equity", note_number="E01", subnote_code="",
        equity_component="RETAINED_EARNINGS", movement_category="NET_PROFIT_LOSS",
        line_label="Retained earnings", opening_balance="60",
        movement_amount=profit, closing_balance=closing,
        source_closing_exposure=str(-closing_value),
        note_reference_evidence="REF-EQ", policy_evidence_ref="POL-EQ",
    )
    component = EquityComponentTotal(
        equity_component="RETAINED_EARNINGS", opening_balance="60",
        movement_amount=profit, closing_balance=closing,
    )
    return EquityChangesCandidate(
        company_code="001", fiscal_year=1404, source_sha256=SOURCE,
        note_references_sha256=REFS, presentation_policies_sha256=POLICY,
        opening_equity_total="60", capital_contributions="0",
        net_profit_loss_movements=profit, dividends="0",
        other_comprehensive_income="0", transfers="0",
        prior_period_adjustments="0", other_movements="0",
        total_movement=profit, closing_equity_total=closing,
        rollforward_difference=str(rollforward), component_totals=(component,),
        note_movements=(note,), account_movements=(account,), findings=(),
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
        account_reconciliations=(CashAccountReconciliation(
            account_code="CASH1", account_name="Cash", source_row=1,
            opening_balance="40", source_debit_turnover="30",
            source_credit_turnover="20", closing_balance="50",
            transaction_debit_turnover="30", transaction_credit_turnover="20",
            debit_difference="0", credit_difference="0",
            rollforward_difference="0", policy_evidence_ref="CASH-POLICY",
        ),), cash_flow_lines=(
            CashFlowLine("L1", "V1", "1404-01-01", "CASH1", "REV", "OPERATING", "30", "0", "SRC1", "POL-REV"),
            CashFlowLine("L2", "V2", "1404-01-02", "CASH1", "EXP", "OPERATING", "0", "20", "SRC2", "POL-EXP"),
        ), findings=(),
        eligible_for_analyst_review=eligible,
    )


def trial(*, balanced=True):
    accounts = (
        TrialBalanceAccount("CASH1", "Cash", 2, 1, "40", "30", "20", "50", "10"),
        TrialBalanceAccount("EQ1", "Equity", 3, 2, "-60", "0", "40", "-100", "-40"),
        TrialBalanceAccount("REV", "Revenue", 4, 3, "0", "0", "30", "-30", "-30"),
        TrialBalanceAccount("EXP", "Expense", 5, 4, "0", "20", "0", "20", "20"),
        TrialBalanceAccount("OFFSET", "Offset", 6, 5, "20", "40", "0", "60", "40"),
    )
    return TrialBalanceDiagnostic(
        company_code="001", fiscal_year=1404, source_sha256=SOURCE,
        account_count=5, opening_debit_net_total="0",
        debit_turnover_total="90", credit_turnover_total="90",
        closing_debit_net_total="0", movement_difference="0",
        opening_to_closing_difference="0", findings=(), accounts=accounts,
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
    assert result.cash_accounts_match_trial_balance
    assert result.cash_account_totals_valid
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


def test_cash_account_source_balances_and_turnovers_must_match_trial_balance():
    source = trial()
    rows = list(source.accounts)
    rows[0] = replace(rows[0], debit="31")
    result = reconcile(trial_balance=replace(source, accounts=tuple(rows)))
    assert not result.cash_accounts_match_trial_balance
    assert "CASH_ACCOUNTS_TRIAL_BALANCE_MISMATCH" in result.findings


def test_cash_account_reconciliation_differences_block_cross_statement_gate():
    source = cash()
    row = replace(source.account_reconciliations[0], debit_difference="1")
    result = reconcile(cash_flow=replace(source, account_reconciliations=(row,)))
    assert not result.cash_account_totals_valid
    assert "CASH_ACCOUNT_TURNOVER_OR_TOTALS_INVALID" in result.findings


def test_duplicate_balance_sheet_note_rows_are_not_silently_overwritten():
    source = bs()
    result = reconcile(balance_sheet=bs(lines=source.lines + (source.lines[0],)))
    assert "DUPLICATE_BALANCE_SHEET_NOTE_LINE" in result.findings


def test_trial_balance_account_trace_count_must_be_complete():
    source = trial()
    result = reconcile(trial_balance=replace(source, account_count=3))
    assert not result.cash_accounts_match_trial_balance
    assert "CASH_ACCOUNTS_TRIAL_BALANCE_MISMATCH" in result.findings


def test_cash_flow_aggregates_must_match_individual_classified_lines():
    source = cash()
    lines = list(source.cash_flow_lines)
    lines[0] = replace(lines[0], cash_inflow="29")
    result = reconcile(cash_flow=replace(source, cash_flow_lines=tuple(lines)))
    assert not result.cash_flow_bridge_valid
    assert "CASH_FLOW_BRIDGE_INVALID" in result.findings


def test_unclassified_cash_flow_line_cannot_pass_cross_statement_gate():
    source = cash()
    lines = list(source.cash_flow_lines)
    lines[0] = replace(lines[0], activity="UNCLASSIFIED")
    result = reconcile(cash_flow=replace(source, cash_flow_lines=tuple(lines)))
    assert not result.cash_flow_bridge_valid
    assert "CASH_FLOW_BRIDGE_INVALID" in result.findings


def test_internal_cash_transfer_totals_must_be_derived_from_line_trace():
    source = cash()
    transfer = CashFlowLine(
        "L3", "V3", "1404-01-03", "CASH1", "CASH2",
        "CASH_TRANSFER", "10", "0", "SRC3", "CASH-POLICY",
    )
    bad = replace(
        source, transaction_count=3,
        cash_flow_lines=source.cash_flow_lines + (transfer,),
        internal_transfer_inflows="9", internal_transfer_outflows="10",
    )
    result = reconcile(cash_flow=bad)
    assert not result.cash_flow_bridge_valid
    assert "CASH_FLOW_BRIDGE_INVALID" in result.findings


def test_balance_sheet_line_detail_must_support_summary_totals():
    source = bs()
    lines = list(source.lines)
    lines[0] = replace(lines[0], presentation_amount="51")
    result = reconcile(balance_sheet=replace(source, lines=tuple(lines)))
    assert "BALANCE_SHEET_DETAIL_INVALID" in result.findings
    assert not result.eligible_for_analyst_review


def test_income_statement_line_detail_must_support_summary_totals():
    source = income()
    lines = list(source.lines)
    lines[0] = replace(lines[0], presentation_amount="101")
    result = reconcile(income_statement=replace(source, lines=tuple(lines)))
    assert not result.income_statement_bridge_valid
    assert "INCOME_STATEMENT_BRIDGE_INVALID" in result.findings


def test_equity_account_detail_must_support_note_and_summary_movements():
    source = equity()
    account = replace(source.account_movements[0], credit_turnover="39")
    result = reconcile(equity_changes=replace(
        source, account_movements=(account,),
    ))
    assert not result.equity_rollforward_valid
    assert "EQUITY_STATEMENT_ROLLFORWARD_INVALID" in result.findings


def test_trial_balance_row_rollforward_mismatch_cannot_net_off_globally():
    source = trial()
    rows = list(source.accounts)
    rows[0] = replace(rows[0], closing="51")
    rows[3] = replace(rows[3], closing="-41")
    result = reconcile(trial_balance=replace(source, accounts=tuple(rows)))
    assert not result.trial_balance_arithmetic_valid
    assert "TRIAL_BALANCE_ARITHMETIC_INVALID" in result.findings


def test_cash_account_transaction_turnovers_must_match_cash_flow_line_trace():
    source = cash()
    account = replace(source.account_reconciliations[0], transaction_debit_turnover="29")
    result = reconcile(cash_flow=replace(
        source, account_reconciliations=(account,),
    ))
    assert not result.cash_account_totals_valid
    assert "CASH_ACCOUNT_TURNOVER_OR_TOTALS_INVALID" in result.findings


def test_all_statement_candidates_must_share_one_note_reference_snapshot():
    result = reconcile(income_statement=replace(
        income(), note_references_sha256="e" * 64,
    ))
    assert "CROSS_STATEMENT_NOTE_REFERENCE_SNAPSHOT_MISMATCH" in result.findings
    assert not result.eligible_for_analyst_review


def test_candidate_eligibility_must_be_a_real_boolean():
    with pytest.raises(CoverageError):
        reconcile(income_statement=replace(
            income(), eligible_for_analyst_review="False",
        ))


def test_cash_scope_and_ledger_completeness_flags_cannot_be_smuggled_in():
    with pytest.raises(CoverageError):
        reconcile(cash_flow=replace(
            cash(), cash_account_scope_owner_approved=True,
        ))


def test_equity_account_movement_must_match_trial_balance_source_row():
    source = trial()
    rows = list(source.accounts)
    rows[1] = replace(rows[1], credit="39", closing="-99", debit_net_movement="-39")
    result = reconcile(trial_balance=replace(source, accounts=tuple(rows)))
    assert not result.equity_rollforward_valid
    assert "EQUITY_STATEMENT_ROLLFORWARD_INVALID" in result.findings
