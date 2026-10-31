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

from aram_backend.balance_sheet_candidate import (
    CATEGORIES as BALANCE_SHEET_CATEGORIES,
    BalanceSheetCandidate, CandidateBalanceSheetLine,
)
from aram_backend.cash_flow_direct_candidate import (
    CashAccountReconciliation, CashFlowLine, DirectCashFlowCandidate,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.equity_changes_candidate import (
    EQUITY_COMPONENTS, MOVEMENT_CATEGORIES, EquityAccountMovement,
    EquityChangesCandidate, EquityComponentTotal, EquityNoteMovement,
)
from aram_backend.income_statement_candidate import (
    CATEGORIES as INCOME_STATEMENT_CATEGORIES,
    CandidateIncomeStatementLine, IncomeStatementCandidate,
)
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
        raise CoverageError("INVALID_CROSS_STATEMENT_" + label.upper() + "_OBJECT")
    if getattr(candidate, "kind", None) != EXPECTED_KINDS[label]:
        raise CoverageError("INVALID_CROSS_STATEMENT_" + label.upper() + "_KIND")
    forbidden = (
        "official_financial_statement", "independently_reviewed",
        "export_authorized", "releasable", "accounting_policy_authorized",
        "trusted_approvals", "source_ledger_completeness_verified",
        "cash_account_scope_owner_approved",
        "transaction_ledger_completeness_verified",
        "accounting_policies_verified",
    )
    for flag in forbidden:
        if hasattr(candidate, flag):
            value = getattr(candidate, flag)
            if type(value) is not bool or value:
                raise CoverageError("CROSS_STATEMENT_APPROVAL_PROVENANCE_INVALID")
    eligible_field = (
        "balanced_for_analyst_review" if label == "trial_balance"
        else "eligible_for_analyst_review"
    )
    eligible = getattr(candidate, eligible_field, None)
    if type(eligible) is not bool:
        raise CoverageError("CROSS_STATEMENT_CANDIDATE_ELIGIBILITY_INVALID")
    findings = getattr(candidate, "findings", None)
    if (not isinstance(findings, tuple)
            or any(not isinstance(item, str) or not item for item in findings)
            or (eligible and findings)):
        raise CoverageError("CROSS_STATEMENT_CANDIDATE_FINDINGS_INVALID")
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


def _balance_sheet_detail_bridge(balance: BalanceSheetCandidate) -> bool:
    if not isinstance(balance.lines, tuple) or not balance.lines:
        return False
    buckets: dict[str, list[Decimal]] = {
        category: [] for category in BALANCE_SHEET_CATEGORIES
    }
    seen: set[tuple[str, str, str]] = set()
    for line in balance.lines:
        if not isinstance(line, CandidateBalanceSheetLine):
            return False
        key = (
            _text(line.statement_section, "BS_DETAIL_SECTION"),
            _text(line.note_number, "BS_DETAIL_NOTE"),
            _text(line.subnote_code, "BS_DETAIL_SUBNOTE", blank_ok=True),
        )
        if key in seen or line.category not in BALANCE_SHEET_CATEGORIES:
            return False
        seen.add(key)
        if type(line.sign_multiplier) is not int or line.sign_multiplier not in (-1, 1):
            return False
        source = _money(line.source_closing_exposure)
        amount = _money(line.presentation_amount)
        if amount != source * line.sign_multiplier or amount < 0:
            return False
        _text(line.line_label, "BS_DETAIL_LABEL")
        _text(line.note_reference_evidence, "BS_DETAIL_REFERENCE")
        _text(line.policy_evidence_ref, "BS_DETAIL_POLICY")
        buckets[line.category].append(amount)
    totals = {key: _sum_exact(values) for key, values in buckets.items()}
    return (
        all(buckets[key] for key in BALANCE_SHEET_CATEGORIES)
        and totals["ASSETS"] == _money(balance.assets_total)
        and totals["LIABILITIES"] == _money(balance.liabilities_total)
        and totals["EQUITY"] == _money(balance.equity_total)
        and _sum_exact([
            totals["ASSETS"], -totals["LIABILITIES"], -totals["EQUITY"],
        ]) == _money(balance.balance_difference) == 0
        and balance.arithmetically_balanced is True
    )


def _income_detail_bridge(income: IncomeStatementCandidate) -> bool:
    if not isinstance(income.lines, tuple) or not income.lines:
        return False
    buckets: dict[str, list[Decimal]] = {
        category: [] for category in INCOME_STATEMENT_CATEGORIES
    }
    seen: set[tuple[str, str, str]] = set()
    for line in income.lines:
        if not isinstance(line, CandidateIncomeStatementLine):
            return False
        key = (
            _text(line.statement_section, "IS_DETAIL_SECTION"),
            _text(line.note_number, "IS_DETAIL_NOTE"),
            _text(line.subnote_code, "IS_DETAIL_SUBNOTE", blank_ok=True),
        )
        if key in seen or line.category not in INCOME_STATEMENT_CATEGORIES:
            return False
        seen.add(key)
        if type(line.sign_multiplier) is not int or line.sign_multiplier not in (-1, 1):
            return False
        source = _money(line.source_closing_exposure)
        amount = _money(line.presentation_amount)
        if amount != source * line.sign_multiplier or amount < 0:
            return False
        _text(line.line_label, "IS_DETAIL_LABEL")
        _text(line.note_reference_evidence, "IS_DETAIL_REFERENCE")
        _text(line.policy_evidence_ref, "IS_DETAIL_POLICY")
        buckets[line.category].append(amount)
    totals = {key: _sum_exact(values) for key, values in buckets.items()}
    revenue = totals["REVENUE"]
    cost = totals["COST_OF_REVENUE"]
    gross = _sum_exact([revenue, -cost])
    operating = _sum_exact([gross, -totals["OPERATING_EXPENSE"]])
    pretax = _sum_exact([
        operating, totals["OTHER_INCOME"], -totals["OTHER_EXPENSE"],
    ])
    net = _sum_exact([pretax, -totals["TAX_EXPENSE"]])
    return (
        bool(buckets["REVENUE"])
        and any(buckets[key] for key in (
            "COST_OF_REVENUE", "OPERATING_EXPENSE",
            "OTHER_EXPENSE", "TAX_EXPENSE",
        ))
        and revenue == _money(income.revenue_total)
        and cost == _money(income.cost_of_revenue_total)
        and gross == _money(income.gross_profit)
        and totals["OPERATING_EXPENSE"] == _money(income.operating_expense_total)
        and operating == _money(income.operating_profit)
        and totals["OTHER_INCOME"] == _money(income.other_income_total)
        and totals["OTHER_EXPENSE"] == _money(income.other_expense_total)
        and pretax == _money(income.profit_before_tax)
        and totals["TAX_EXPENSE"] == _money(income.tax_expense_total)
        and net == _money(income.net_result)
    )


def _equity_detail_bridge(equity: EquityChangesCandidate) -> bool:
    if (not isinstance(equity.note_movements, tuple) or not equity.note_movements
            or not isinstance(equity.account_movements, tuple)
            or not equity.account_movements
            or not isinstance(equity.component_totals, tuple)):
        return False
    accounts_by_note: dict[tuple[str, str, str], list[EquityAccountMovement]] = {}
    seen_accounts: set[str] = set()
    for account in equity.account_movements:
        if not isinstance(account, EquityAccountMovement):
            return False
        code = _text(account.account_code, "EQ_DETAIL_ACCOUNT")
        if code in seen_accounts:
            return False
        seen_accounts.add(code)
        key = (
            _text(account.statement_section, "EQ_DETAIL_SECTION"),
            _text(account.note_number, "EQ_DETAIL_NOTE"),
            _text(account.subnote_code, "EQ_DETAIL_SUBNOTE", blank_ok=True),
        )
        if (account.equity_component not in EQUITY_COMPONENTS
                or account.movement_category not in MOVEMENT_CATEGORIES
                or type(account.sign_multiplier) is not int
                or account.sign_multiplier not in (-1, 1)
                or type(account.source_excel_row) is not int
                or account.source_excel_row < 2
                or type(account.source_row) is not int
                or account.source_row <= 0):
            return False
        opening = _money(account.opening_balance)
        debit = _money(account.debit_turnover)
        credit = _money(account.credit_turnover)
        movement = _money(account.movement_amount)
        closing = _money(account.closing_balance)
        if (debit < 0 or credit < 0
                or movement != _sum_exact([debit, -credit]) * account.sign_multiplier
                or _sum_exact([opening, movement, -closing]) != 0):
            return False
        _text(account.account_name, "EQ_DETAIL_ACCOUNT_NAME")
        _text(account.policy_evidence_ref, "EQ_DETAIL_POLICY")
        accounts_by_note.setdefault(key, []).append(account)

    note_by_key: dict[tuple[str, str, str], EquityNoteMovement] = {}
    category_movements: dict[str, list[Decimal]] = {
        category: [] for category in MOVEMENT_CATEGORIES
    }
    component_values: dict[str, dict[str, list[Decimal]]] = {}
    opening_values: list[Decimal] = []
    movement_values: list[Decimal] = []
    closing_values: list[Decimal] = []
    for note in equity.note_movements:
        if not isinstance(note, EquityNoteMovement):
            return False
        key = (
            _text(note.statement_section, "EQ_DETAIL_SECTION"),
            _text(note.note_number, "EQ_DETAIL_NOTE"),
            _text(note.subnote_code, "EQ_DETAIL_SUBNOTE", blank_ok=True),
        )
        if key in note_by_key or key not in accounts_by_note:
            return False
        if (note.equity_component not in EQUITY_COMPONENTS
                or note.movement_category not in MOVEMENT_CATEGORIES):
            return False
        _text(note.line_label, "EQ_DETAIL_LABEL")
        _text(note.note_reference_evidence, "EQ_DETAIL_REFERENCE")
        _text(note.policy_evidence_ref, "EQ_DETAIL_POLICY")
        rows = accounts_by_note[key]
        if any(
            row.equity_component != note.equity_component
            or row.movement_category != note.movement_category
            for row in rows
        ):
            return False
        opening = _sum_exact([_money(row.opening_balance) for row in rows])
        movement = _sum_exact([_money(row.movement_amount) for row in rows])
        closing = _sum_exact([_money(row.closing_balance) for row in rows])
        raw_closing = _sum_exact([
            _money(row.closing_balance) * row.sign_multiplier for row in rows
        ])
        note_opening = _money(note.opening_balance)
        note_movement = _money(note.movement_amount)
        note_closing = _money(note.closing_balance)
        if (
            opening != note_opening or movement != note_movement
            or closing != note_closing
            or raw_closing != _money(note.source_closing_exposure)
            or _sum_exact([note_opening, note_movement, -note_closing]) != 0
        ):
            return False
        note_by_key[key] = note
        opening_values.append(note_opening)
        movement_values.append(note_movement)
        closing_values.append(note_closing)
        category_movements[note.movement_category].append(note_movement)
        group = component_values.setdefault(note.equity_component, {
            "opening": [], "movement": [], "closing": [],
        })
        group["opening"].append(note_opening)
        group["movement"].append(note_movement)
        group["closing"].append(note_closing)
    if set(accounts_by_note) != set(note_by_key):
        return False

    component_by_key: dict[str, EquityComponentTotal] = {}
    for item in equity.component_totals:
        if not isinstance(item, EquityComponentTotal):
            return False
        if item.equity_component not in EQUITY_COMPONENTS or item.equity_component in component_by_key:
            return False
        component_by_key[item.equity_component] = item
    if set(component_by_key) != set(component_values):
        return False
    for component, group in component_values.items():
        item = component_by_key[component]
        if (
            _money(item.opening_balance) != _sum_exact(group["opening"])
            or _money(item.movement_amount) != _sum_exact(group["movement"])
            or _money(item.closing_balance) != _sum_exact(group["closing"])
        ):
            return False

    summary_categories = {
        "CAPITAL_CONTRIBUTION": equity.capital_contributions,
        "NET_PROFIT_LOSS": equity.net_profit_loss_movements,
        "DIVIDENDS": equity.dividends,
        "OTHER_COMPREHENSIVE_INCOME": equity.other_comprehensive_income,
        "TRANSFER": equity.transfers,
        "PRIOR_PERIOD_ADJUSTMENT": equity.prior_period_adjustments,
        "OTHER_MOVEMENT": equity.other_movements,
    }
    return (
        _sum_exact(opening_values) == _money(equity.opening_equity_total)
        and _sum_exact(movement_values) == _money(equity.total_movement)
        and _sum_exact(closing_values) == _money(equity.closing_equity_total)
        and _sum_exact([
            _money(equity.opening_equity_total),
            _money(equity.total_movement),
            -_money(equity.closing_equity_total),
        ]) == _money(equity.rollforward_difference) == 0
        and all(
            _sum_exact(category_movements[category]) == _money(amount)
            for category, amount in summary_categories.items()
        )
    )


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
        _income_detail_bridge(income)
        and _sum_exact([revenue, -cost, -gross]) == 0
        and _sum_exact([gross, -operating_expense, -operating]) == 0
        and _sum_exact([operating, other_income, -other_expense, -pretax]) == 0
        and _sum_exact([pretax, -tax, -net]) == 0
    )


def _cash_flow_bridge(cash: DirectCashFlowCandidate) -> bool:
    categories = {
        activity: {"inflows": [], "outflows": []}
        for activity in ("OPERATING", "INVESTING", "FINANCING")
    }
    line_ids: set[str] = set()
    transfer_values: list[Decimal] = []
    if (type(cash.transaction_count) is not int
            or not isinstance(cash.cash_flow_lines, tuple)
            or cash.transaction_count != len(cash.cash_flow_lines)):
        return False
    for line in cash.cash_flow_lines:
        if not isinstance(line, CashFlowLine):
            return False
        line_id = _text(line.line_id, "CASH_FLOW_LINE_ID")
        _text(line.transaction_id, "CASH_FLOW_TRANSACTION_ID")
        _text(line.posting_date, "CASH_FLOW_POSTING_DATE")
        cash_code = _text(line.cash_account_code, "CASH_FLOW_CASH_ACCOUNT")
        counterpart_code = _text(line.counterpart_account_code, "CASH_FLOW_COUNTERPART")
        activity = _text(line.activity, "CASH_FLOW_ACTIVITY")
        _text(line.source_evidence_ref, "CASH_FLOW_SOURCE_EVIDENCE")
        _text(line.classification_evidence_ref, "CASH_FLOW_CLASSIFICATION_EVIDENCE")
        if line_id in line_ids or cash_code == counterpart_code:
            return False
        line_ids.add(line_id)
        inflow = _money(line.cash_inflow)
        outflow = _money(line.cash_outflow)
        if inflow < 0 or outflow < 0 or not ((inflow > 0) ^ (outflow > 0)):
            return False
        if activity in categories:
            categories[activity]["inflows"].append(inflow)
            categories[activity]["outflows"].append(outflow)
        elif activity == "CASH_TRANSFER":
            transfer_values.append(_sum_exact([inflow, outflow]))
        else:
            return False

    operating = _sum_exact([
        _sum_exact(categories["OPERATING"]["inflows"]),
        -_sum_exact(categories["OPERATING"]["outflows"]),
    ])
    investing = _sum_exact([
        _sum_exact(categories["INVESTING"]["inflows"]),
        -_sum_exact(categories["INVESTING"]["outflows"]),
    ])
    financing = _sum_exact([
        _sum_exact(categories["FINANCING"]["inflows"]),
        -_sum_exact(categories["FINANCING"]["outflows"]),
    ])
    net_change = _money(cash.net_change_in_cash)
    transfer_total = _sum_exact(transfer_values)
    rollforward = _sum_exact([
        _money(cash.opening_cash_and_equivalents), net_change,
        -_money(cash.closing_cash_and_equivalents),
    ])
    return (
        _sum_exact(categories["OPERATING"]["inflows"]) == _money(cash.operating_inflows)
        and _sum_exact(categories["OPERATING"]["outflows"]) == _money(cash.operating_outflows)
        and operating == _money(cash.operating_net_cash_flow)
        and _sum_exact(categories["INVESTING"]["inflows"]) == _money(cash.investing_inflows)
        and _sum_exact(categories["INVESTING"]["outflows"]) == _money(cash.investing_outflows)
        and investing == _money(cash.investing_net_cash_flow)
        and _sum_exact(categories["FINANCING"]["inflows"]) == _money(cash.financing_inflows)
        and _sum_exact(categories["FINANCING"]["outflows"]) == _money(cash.financing_outflows)
        and financing == _money(cash.financing_net_cash_flow)
        and _sum_exact([operating, investing, financing, -net_change]) == 0
        and _money(cash.internal_transfer_inflows) == transfer_total
        and _money(cash.internal_transfer_outflows) == transfer_total
        and rollforward == _money(cash.rollforward_difference) == 0
    )


def _trial_balance_bridge(trial: TrialBalanceDiagnostic) -> bool:
    if (type(trial.account_count) is not int
            or not isinstance(trial.accounts, tuple)
            or trial.account_count != len(trial.accounts) or not trial.accounts
            or type(trial.balanced_for_analyst_review) is not bool):
        return False
    seen: set[str] = set()
    openings: list[Decimal] = []
    debits: list[Decimal] = []
    credits: list[Decimal] = []
    closings: list[Decimal] = []
    source_rows: set[int] = set()
    for account in trial.accounts:
        if not isinstance(account, TrialBalanceAccount):
            return False
        code = _text(account.account_code, "TRIAL_BALANCE_ACCOUNT_CODE")
        if code in seen:
            return False
        seen.add(code)
        if (type(account.source_row) is not int or account.source_row <= 0
                or account.source_row in source_rows):
            return False
        source_rows.add(account.source_row)
        _text(account.account_name, "TRIAL_BALANCE_ACCOUNT_NAME")
        opening = _money(account.opening)
        debit = _money(account.debit)
        credit = _money(account.credit)
        closing = _money(account.closing)
        if (debit < 0 or credit < 0
                or _sum_exact([debit, -credit]) != _money(account.debit_net_movement)
                or _sum_exact([opening, debit, -credit, -closing]) != 0):
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
            or trial.account_count != len(trial.accounts)
            or type(cash.cash_account_count) is not int
            or not isinstance(cash.account_reconciliations, tuple)
            or cash.cash_account_count != len(cash.account_reconciliations)
            or cash.cash_account_count < 1
            or not isinstance(cash.cash_flow_lines, tuple)):
        findings_valid = False

    trial_by_code: dict[str, TrialBalanceAccount] = {}
    for account in trial.accounts:
        if (not isinstance(account, TrialBalanceAccount)
                or not isinstance(account.account_code, str)
                or account.account_code != account.account_code.strip()
                or not account.account_code
                or account.account_code in trial_by_code):
            findings_valid = False
            continue
        trial_by_code[account.account_code] = account

    cash_by_code: dict[str, CashAccountReconciliation] = {}
    for item in cash.account_reconciliations:
        if (not isinstance(item, CashAccountReconciliation)
                or not isinstance(item.account_code, str)
                or item.account_code != item.account_code.strip()
                or not item.account_code or item.account_code in cash_by_code):
            findings_valid = False
            continue
        cash_by_code[item.account_code] = item

    line_debits: dict[str, list[Decimal]] = {
        code: [] for code in cash_by_code
    }
    line_credits: dict[str, list[Decimal]] = {
        code: [] for code in cash_by_code
    }
    for line in cash.cash_flow_lines:
        if not isinstance(line, CashFlowLine):
            findings_valid = False
            continue
        cash_code = line.cash_account_code
        counterpart_code = line.counterpart_account_code
        if (not isinstance(cash_code, str) or cash_code not in cash_by_code
                or not isinstance(counterpart_code, str)
                or counterpart_code not in trial_by_code):
            findings_valid = False
            continue
        inflow = _money(line.cash_inflow)
        outflow = _money(line.cash_outflow)
        if inflow > 0:
            line_debits[cash_code].append(inflow)
        if outflow > 0:
            line_credits[cash_code].append(outflow)
        if line.activity == "CASH_TRANSFER":
            if counterpart_code not in cash_by_code:
                findings_valid = False
                continue
            if inflow > 0:
                line_credits[counterpart_code].append(inflow)
            elif outflow > 0:
                line_debits[counterpart_code].append(outflow)
            else:
                findings_valid = False
        elif counterpart_code in cash_by_code:
            findings_valid = False

    seen: set[str] = set()
    opening_values: list[Decimal] = []
    closing_values: list[Decimal] = []
    for code, item in cash_by_code.items():
        if code in seen:
            findings_valid = False
            continue
        seen.add(code)
        trial_account = trial_by_code.get(code)
        if trial_account is None:
            findings_valid = False
            continue
        if (type(item.source_row) is not int or item.source_row <= 0
                or item.source_row != trial_account.source_row
                or item.account_name != trial_account.account_name):
            findings_valid = False
        _text(item.policy_evidence_ref, "CASH_ACCOUNT_POLICY_EVIDENCE")
        source_values = (
            _money(item.opening_balance), _money(item.source_debit_turnover),
            _money(item.source_credit_turnover), _money(item.closing_balance),
        )
        trial_values = (
            _money(trial_account.opening), _money(trial_account.debit),
            _money(trial_account.credit), _money(trial_account.closing),
        )
        if source_values != trial_values:
            findings_valid = False
        transaction_debit = _sum_exact(line_debits[code])
        transaction_credit = _sum_exact(line_credits[code])
        if (
            transaction_debit != _money(item.transaction_debit_turnover)
            or transaction_credit != _money(item.transaction_credit_turnover)
        ):
            totals_valid = False
        debit_difference = _sum_exact([
            transaction_debit, -_money(item.source_debit_turnover),
        ])
        credit_difference = _sum_exact([
            transaction_credit, -_money(item.source_credit_turnover),
        ])
        rollforward = _sum_exact([
            source_values[0], source_values[1], -source_values[2], -source_values[3],
        ])
        if (debit_difference != 0 or credit_difference != 0 or rollforward != 0
                or _money(item.debit_difference) != debit_difference
                or _money(item.credit_difference) != credit_difference
                or _money(item.rollforward_difference) != rollforward):
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
    reference_hashes = {
        balance_sheet.note_references_sha256,
        income_statement.note_references_sha256,
        equity_changes.note_references_sha256,
    }
    if len(reference_hashes) != 1:
        findings.append("CROSS_STATEMENT_NOTE_REFERENCE_SNAPSHOT_MISMATCH")
    source_hash = base.source_sha256

    for label, candidate, _ in candidates:
        eligible = (
            getattr(candidate, "eligible_for_analyst_review", None)
            if label != "trial_balance"
            else candidate.balanced_for_analyst_review
        )
        if not eligible:
            findings.append(label.upper() + "_CANDIDATE_BLOCKED")

    if not _balance_sheet_detail_bridge(balance_sheet):
        findings.append("BALANCE_SHEET_DETAIL_INVALID")

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
        _equity_detail_bridge(equity_changes)
        and equity_rollforward == 0
        and _money(equity_changes.rollforward_difference) == 0
    )
    if not equity_rollforward_valid:
        findings.append("EQUITY_STATEMENT_ROLLFORWARD_INVALID")

    bs_lines = {}
    for line in (
        balance_sheet.lines if isinstance(balance_sheet.lines, (tuple, list)) else ()
    ):
        if not isinstance(line, CandidateBalanceSheetLine):
            continue
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
