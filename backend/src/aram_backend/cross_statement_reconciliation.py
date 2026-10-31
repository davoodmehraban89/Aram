"""Cross-statement arithmetic and provenance gate for unsigned ARAM candidates.

Consumes only the typed, nonofficial candidate objects produced by the earlier
read-only engines. Exact matches are necessary, not sufficient, for approval.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from hashlib import sha256
import json
import re
from typing import Any, Sequence

from aram_backend.balance_sheet_candidate import BalanceSheetCandidate
from aram_backend.cash_flow_direct_candidate import (
    CashAccountReconciliation, DirectCashFlowCandidate,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.equity_changes_candidate import EquityChangesCandidate
from aram_backend.income_statement_candidate import IncomeStatementCandidate
from aram_backend.reconciliation_review import _money, _sum_exact
from aram_backend.trial_balance_diagnostic import (
    TrialBalanceAccount, TrialBalanceDiagnostic,
)

EXPECTED_KINDS = {
    "balance_sheet": "UNAPPROVED_BALANCE_SHEET_PRESENTATION_CANDIDATE",
    "income_statement": "UNAPPROVED_INCOME_STATEMENT_PRESENTATION_CANDIDATE",
    "equity_changes": "UNAPPROVED_EQUITY_CHANGES_PRESENTATION_CANDIDATE",
    "cash_flow": "UNAPPROVED_DIRECT_CASH_FLOW_CANDIDATE",
    "trial_balance": "UNAPPROVED_TRIAL_BALANCE_DIAGNOSTIC",
}


@dataclass(frozen=True)
class CashBalanceNoteSelection:
    statement_section: str
    note_number: str
    subnote_code: str
    evidence_ref: str


@dataclass(frozen=True)
class SelectedCashBalanceNote:
    statement_section: str
    note_number: str
    subnote_code: str
    presentation_amount: str
    evidence_ref: str


@dataclass(frozen=True)
class CrossStatementReconciliation:
    company_code: str
    fiscal_year: int
    source_sha256: str
    cash_flow_transaction_ledger_sha256: str
    cash_note_selection_sha256: str
    same_source_snapshot: bool
    trial_balance_opening_debit_net_total: str
    trial_balance_movement_difference: str
    trial_balance_closing_debit_net_total: str
    trial_balance_rollforward_difference: str
    balance_sheet_difference: str
    balance_sheet_equity_total: str
    equity_statement_closing_total: str
    balance_sheet_equity_difference: str
    income_statement_net_result: str
    equity_net_profit_loss_movements: str
    net_profit_equity_difference: str
    balance_sheet_cash_total: str
    cash_flow_closing_cash: str
    balance_sheet_cash_difference: str
    income_statement_bridge_valid: bool
    cash_flow_bridge_valid: bool
    equity_rollforward_valid: bool
    trial_balance_arithmetic_valid: bool
    cash_accounts_match_trial_balance: bool
    cash_account_totals_valid: bool
    selected_cash_notes: tuple[SelectedCashBalanceNote, ...]
    findings: tuple[str, ...]
    eligible_for_analyst_review: bool
    kind: str = "UNAPPROVED_CROSS_STATEMENT_RECONCILIATION"
    source_ledger_completeness_verified: bool = False
    accounting_policy_authorized: bool = False
    independently_reviewed: bool = False
    trusted_approvals: bool = False
    official_financial_statement: bool = False
    export_authorized: bool = False
    releasable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _hash(value: object, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise CoverageError("INVALID_CROSS_STATEMENT_" + label)
    return value


def _text(value: object, label: str, *, blank_ok: bool = False) -> str:
    if (not isinstance(value, str) or len(value) > 256
            or value != value.strip() or (not value and not blank_ok)
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise CoverageError("INVALID_CROSS_STATEMENT_" + label)
    return value


def _validate_candidate(candidate: object, label: str, expected_type: type) -> None:
    if type(candidate) is not expected_type:
        raise CoverageError("INVALID_CROSS_STATEMENT_" + label + "_OBJECT")
    if getattr(candidate, "kind", None) != EXPECTED_KINDS[label]:
        raise CoverageError("INVALID_CROSS_STATEMENT_" + label + "_KIND")
    forbidden = (
        "official_financial_statement", "independently_reviewed",
        "export_authorized", "releasable", "accounting_policy_authorized",
        "trusted_approvals",
    )
    if any(getattr(candidate, flag, False) for flag in forbidden):
        raise CoverageError("CROSS_STATEMENT_APPROVAL_PROVENANCE_INVALID")
    _hash(candidate.source_sha256, label.upper() + "_SOURCE_HASH")
    for hash_field in (
        "note_references_sha256", "presentation_policies_sha256",
        "transaction_ledger_sha256", "classification_policies_sha256",
    ):
        if hasattr(candidate, hash_field):
            _hash(getattr(candidate, hash_field), label.upper() + "_" + hash_field.upper())
    _text(candidate.company_code, label.upper() + "_COMPANY")
    if type(candidate.fiscal_year) is not int or candidate.fiscal_year <= 0:
        raise CoverageError("INVALID_CROSS_STATEMENT_" + label.upper() + "_YEAR")


def _income_bridge(income: IncomeStatementCandidate) -> bool:
    revenue = _money(income.revenue_total)
    cost = _money(income.cost_of_revenue_total)
    gross = _money(income.gross_profit)
    operating_expense = _money(income.operating_expense_total)
    operating = _money(income.operating_profit)
    other_income = _money(income.other_income_total)
    other_expense = _money(income.other_expense_total)
    pretax = _money(income.profit_before_tax)
    tax = _money(income.tax_expense_total)
    net = _money(income.net_result)
    return (
        _sum_exact([revenue, -cost, -gross]) == 0
        and _sum_exact([gross, -operating_expense, -operating]) == 0
        and _sum_exact([operating, other_income, -other_expense, -pretax]) == 0
        and _sum_exact([pretax, -tax, -net]) == 0
    )


def _cash_flow_bridge(cash: DirectCashFlowCandidate) -> bool:
    operating = _sum_exact([
        _money(cash.operating_inflows), -_money(cash.operating_outflows),
    ])
    investing = _sum_exact([
        _money(cash.investing_inflows), -_money(cash.investing_outflows),
    ])
    financing = _sum_exact([
        _money(cash.financing_inflows), -_money(cash.financing_outflows),
    ])
    net_change = _money(cash.net_change_in_cash)
    rollforward = _sum_exact([
        _money(cash.opening_cash_and_equivalents), net_change,
        -_money(cash.closing_cash_and_equivalents),
    ])
    return (
        operating == _money(cash.operating_net_cash_flow)
        and investing == _money(cash.investing_net_cash_flow)
        and financing == _money(cash.financing_net_cash_flow)
        and _sum_exact([operating, investing, financing, -net_change]) == 0
        and rollforward == _money(cash.rollforward_difference) == 0
    )


def _trial_balance_bridge(trial: TrialBalanceDiagnostic) -> bool:
    if (type(trial.account_count) is not int
            or trial.account_count != len(trial.accounts) or not trial.accounts):
        return False
    seen: set[str] = set()
    openings: list[Decimal] = []
    debits: list[Decimal] = []
    credits: list[Decimal] = []
    closings: list[Decimal] = []
    for account in trial.accounts:
        if not isinstance(account, TrialBalanceAccount):
            return False
        code = _text(account.account_code, "TRIAL_BALANCE_ACCOUNT_CODE")
        if code in seen:
            return False
        seen.add(code)
        opening = _money(account.opening)
        debit = _money(account.debit)
        credit = _money(account.credit)
        closing = _money(account.closing)
        if _sum_exact([debit, -credit]) != _money(account.debit_net_movement):
            return False
        openings.append(opening)
        debits.append(debit)
        credits.append(credit)
        closings.append(closing)
    opening_total = _sum_exact(openings)
    debit_total = _sum_exact(debits)
    credit_total = _sum_exact(credits)
    closing_total = _sum_exact(closings)
    movement = _sum_exact([debit_total, -credit_total])
    rollforward = _sum_exact([opening_total, movement, -closing_total])
    return (
        trial.balanced_for_analyst_review
        and opening_total == _money(trial.opening_debit_net_total)
        and debit_total == _money(trial.debit_turnover_total)
        and credit_total == _money(trial.credit_turnover_total)
        and closing_total == _money(trial.closing_debit_net_total)
        and movement == _money(trial.movement_difference) == 0
        and opening_total == 0 and closing_total == 0
        and rollforward == _money(trial.opening_to_closing_difference) == 0
    )


def _cash_accounts_match_trial_balance(
    cash: DirectCashFlowCandidate, trial: TrialBalanceDiagnostic,
) -> tuple[bool, bool]:
    findings_valid = True
    totals_valid = True
    if (type(trial.account_count) is not int
            or trial.account_count != len(trial.accounts)):
        findings_valid = False
    trial_by_code: dict[str, TrialBalanceAccount] = {}
    for account in trial.accounts:
        if (not isinstance(account, TrialBalanceAccount)
                or not isinstance(account.account_code, str)
                or account.account_code in trial_by_code):
            findings_valid = False
            continue
        trial_by_code[account.account_code] = account

    if (type(cash.cash_account_count) is not int
            or cash.cash_account_count != len(cash.account_reconciliations)):
        findings_valid = False
    seen: set[str] = set()
    opening_values: list[Decimal] = []
    closing_values: list[Decimal] = []
    for item in cash.account_reconciliations:
        if (not isinstance(item, CashAccountReconciliation)
                or not isinstance(item.account_code, str)
                or item.account_code in seen):
            findings_valid = False
            continue
        seen.add(item.account_code)
        trial_account = trial_by_code.get(item.account_code)
        if trial_account is None:
            findings_valid = False
            continue
        source_values = (
            _money(item.opening_balance), _money(item.source_debit_turnover),
            _money(item.source_credit_turnover), _money(item.closing_balance),
        )
        trial_values = (
            _money(trial_account.opening), _money(trial_account.debit),
            _money(trial_account.credit), _money(trial_account.closing),
        )
        if (source_values != trial_values
                or item.source_row != trial_account.source_row):
            findings_valid = False
        if (_money(item.debit_difference) != 0
                or _money(item.credit_difference) != 0
                or _money(item.rollforward_difference) != 0):
            totals_valid = False
        opening_values.append(source_values[0])
        closing_values.append(source_values[3])

    if (_sum_exact(opening_values) != _money(cash.opening_cash_and_equivalents)
            or _sum_exact(closing_values) != _money(cash.closing_cash_and_equivalents)):
        totals_valid = False
    return findings_valid, totals_valid


def reconcile_cross_statements(
    *, balance_sheet: BalanceSheetCandidate,
    income_statement: IncomeStatementCandidate,
    equity_changes: EquityChangesCandidate,
    cash_flow: DirectCashFlowCandidate,
    trial_balance: TrialBalanceDiagnostic,
    cash_balance_notes: Sequence[CashBalanceNoteSelection],
) -> CrossStatementReconciliation:
    """Reconcile BS/IS/EQ/CF/TB candidates without granting financial approval.

    The caller must explicitly select the BS asset notes that represent cash
    and cash equivalents. This policy is evidence-bearing and untrusted. Exact
    Decimal comparison uses zero tolerance; any scope/hash mismatch or blocked
    upstream candidate prevents analyst eligibility.
    """
    candidates = (
        ("balance_sheet", balance_sheet, BalanceSheetCandidate),
        ("income_statement", income_statement, IncomeStatementCandidate),
        ("equity_changes", equity_changes, EquityChangesCandidate),
        ("cash_flow", cash_flow, DirectCashFlowCandidate),
        ("trial_balance", trial_balance, TrialBalanceDiagnostic),
    )
    for label, candidate, expected_type in candidates:
        _validate_candidate(candidate, label, expected_type)

    if not isinstance(cash_balance_notes, (list, tuple)) or not 0 < len(cash_balance_notes) <= 5_000:
        raise CoverageError("INVALID_CASH_BALANCE_NOTE_SELECTION")

    selected: dict[tuple[str, str, str], CashBalanceNoteSelection] = {}
    for item in cash_balance_notes:
        if not isinstance(item, CashBalanceNoteSelection):
            raise CoverageError("INVALID_CASH_BALANCE_NOTE_SELECTION")
        key = (
            _text(item.statement_section, "CASH_NOTE_SECTION"),
            _text(item.note_number, "CASH_NOTE_NUMBER"),
            _text(item.subnote_code, "CASH_NOTE_SUBNOTE", blank_ok=True),
        )
        _text(item.evidence_ref, "CASH_NOTE_EVIDENCE")
        if key in selected:
            raise CoverageError("DUPLICATE_CASH_BALANCE_NOTE_SELECTION")
        selected[key] = item
    selection_hash = sha256(json.dumps(
        [asdict(selected[key]) for key in sorted(selected)],
        ensure_ascii=True, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()

    findings: list[str] = []
    base = balance_sheet
    if any(
        candidate.company_code != base.company_code
        or candidate.fiscal_year != base.fiscal_year
        for _, candidate, _ in candidates
    ):
        findings.append("CROSS_STATEMENT_COMPANY_YEAR_MISMATCH")

    hashes = {candidate.source_sha256 for _, candidate, _ in candidates}
    same_snapshot = len(hashes) == 1
    if not same_snapshot:
        findings.append("CROSS_STATEMENT_SOURCE_SNAPSHOT_MISMATCH")
    source_hash = base.source_sha256

    for label, candidate, _ in candidates:
        eligible = (
            getattr(candidate, "eligible_for_analyst_review", None)
            if label != "trial_balance"
            else candidate.balanced_for_analyst_review
        )
        if not eligible:
            findings.append(label.upper() + "_CANDIDATE_BLOCKED")

    bs_computed_difference = _sum_exact([
        _money(balance_sheet.assets_total),
        -_money(balance_sheet.liabilities_total),
        -_money(balance_sheet.equity_total),
    ])
    bs_reported_difference = _money(balance_sheet.balance_difference)
    if (bs_computed_difference != bs_reported_difference
            or bs_reported_difference != 0
            or not balance_sheet.arithmetically_balanced):
        findings.append("BALANCE_SHEET_EQUATION_INVALID")

    equity_difference = _sum_exact([
        _money(balance_sheet.equity_total),
        -_money(equity_changes.closing_equity_total),
    ])
    if equity_difference != 0:
        findings.append("BALANCE_SHEET_EQUITY_CLOSING_MISMATCH")

    profit_difference = _sum_exact([
        _money(income_statement.net_result),
        -_money(equity_changes.net_profit_loss_movements),
    ])
    if profit_difference != 0:
        findings.append("INCOME_RESULT_EQUITY_MOVEMENT_MISMATCH")

    income_valid = _income_bridge(income_statement)
    if not income_valid:
        findings.append("INCOME_STATEMENT_BRIDGE_INVALID")

    equity_rollforward = _sum_exact([
        _money(equity_changes.opening_equity_total),
        _money(equity_changes.total_movement),
        -_money(equity_changes.closing_equity_total),
    ])
    equity_rollforward_valid = (
        equity_rollforward == 0
        and _money(equity_changes.rollforward_difference) == 0
    )
    if not equity_rollforward_valid:
        findings.append("EQUITY_STATEMENT_ROLLFORWARD_INVALID")

    bs_lines = {}
    for line in balance_sheet.lines:
        key = (line.statement_section, line.note_number, line.subnote_code)
        if key in bs_lines:
            findings.append("DUPLICATE_BALANCE_SHEET_NOTE_LINE")
        else:
            bs_lines[key] = line
    selected_lines: list[SelectedCashBalanceNote] = []
    cash_amounts: list[Decimal] = []
    for key in sorted(selected):
        line = bs_lines.get(key)
        if line is None:
            findings.append("CASH_BALANCE_NOTE_NOT_FOUND_IN_BALANCE_SHEET")
            continue
        if line.category != "ASSETS":
            findings.append("CASH_BALANCE_NOTE_NOT_ASSET")
            continue
        amount = _money(line.presentation_amount)
        cash_amounts.append(amount)
        selected_lines.append(SelectedCashBalanceNote(
            statement_section=key[0], note_number=key[1],
            subnote_code=key[2], presentation_amount=str(amount),
            evidence_ref=selected[key].evidence_ref,
        ))
    if len(selected_lines) != len(selected):
        findings.append("CASH_BALANCE_NOTE_SELECTION_INCOMPLETE")
    bs_cash_total = _sum_exact(cash_amounts)
    cash_difference = _sum_exact([
        bs_cash_total, -_money(cash_flow.closing_cash_and_equivalents),
    ])
    if cash_difference != 0:
        findings.append("BALANCE_SHEET_CASH_FLOW_CLOSING_MISMATCH")

    cash_valid = _cash_flow_bridge(cash_flow)
    if not cash_valid:
        findings.append("CASH_FLOW_BRIDGE_INVALID")

    cash_accounts_match_tb, cash_account_totals_valid = (
        _cash_accounts_match_trial_balance(cash_flow, trial_balance)
    )
    if not cash_accounts_match_tb:
        findings.append("CASH_ACCOUNTS_TRIAL_BALANCE_MISMATCH")
    if not cash_account_totals_valid:
        findings.append("CASH_ACCOUNT_TURNOVER_OR_TOTALS_INVALID")

    trial_valid = _trial_balance_bridge(trial_balance)
    if not trial_valid:
        findings.append("TRIAL_BALANCE_ARITHMETIC_INVALID")

    tb_opening = _money(trial_balance.opening_debit_net_total)
    tb_movement = _money(trial_balance.movement_difference)
    tb_closing = _money(trial_balance.closing_debit_net_total)
    tb_rollforward = _money(trial_balance.opening_to_closing_difference)

    return CrossStatementReconciliation(
        company_code=base.company_code, fiscal_year=base.fiscal_year,
        source_sha256=source_hash,
        cash_flow_transaction_ledger_sha256=_hash(
            cash_flow.transaction_ledger_sha256, "CASH_FLOW_TRANSACTION_HASH",
        ),
        cash_note_selection_sha256=selection_hash,
        same_source_snapshot=same_snapshot,
        trial_balance_opening_debit_net_total=str(tb_opening),
        trial_balance_movement_difference=str(tb_movement),
        trial_balance_closing_debit_net_total=str(tb_closing),
        trial_balance_rollforward_difference=str(tb_rollforward),
        balance_sheet_difference=str(bs_reported_difference),
        balance_sheet_equity_total=str(_money(balance_sheet.equity_total)),
        equity_statement_closing_total=str(_money(equity_changes.closing_equity_total)),
        balance_sheet_equity_difference=str(equity_difference),
        income_statement_net_result=str(_money(income_statement.net_result)),
        equity_net_profit_loss_movements=str(_money(equity_changes.net_profit_loss_movements)),
        net_profit_equity_difference=str(profit_difference),
        balance_sheet_cash_total=str(bs_cash_total),
        cash_flow_closing_cash=str(_money(cash_flow.closing_cash_and_equivalents)),
        balance_sheet_cash_difference=str(cash_difference),
        income_statement_bridge_valid=income_valid,
        cash_flow_bridge_valid=cash_valid,
        equity_rollforward_valid=equity_rollforward_valid,
        trial_balance_arithmetic_valid=trial_valid,
        cash_accounts_match_trial_balance=cash_accounts_match_tb,
        cash_account_totals_valid=cash_account_totals_valid,
        selected_cash_notes=tuple(selected_lines),
        findings=tuple(sorted(set(findings))),
        eligible_for_analyst_review=not findings,
    )
