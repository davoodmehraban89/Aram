"""Single-snapshot orchestration for ARAM's five unsigned statement engines.

The pipeline is read-only. It invokes each existing candidate builder with the
same immutable workbook bytes and the same frozen note-reference collection,
then runs the cross-statement arithmetic gate. It never authorizes, posts,
exports or releases financial statements.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from aram_backend.balance_sheet_candidate import (
    BalanceSheetCandidate, BalanceSheetLinePolicy, build_balance_sheet_candidate,
)
from aram_backend.cash_flow_direct_candidate import (
    CashAccountPolicy, CashCounterpartPolicy, CashFlowEntry,
    DirectCashFlowCandidate, build_direct_cash_flow_candidate,
)
from aram_backend.coverage_preview import (
    CoverageError, CoveragePreview, preview_mapping_coverage,
)
from aram_backend.cross_statement_reconciliation import (
    CashBalanceNoteSelection, CrossStatementReconciliation,
    reconcile_cross_statements,
)
from aram_backend.equity_changes_candidate import (
    EquityChangesCandidate, EquityMovementPolicy, build_equity_changes_candidate,
)
from aram_backend.income_statement_candidate import (
    IncomeStatementCandidate, IncomeStatementLinePolicy,
    build_income_statement_candidate,
)
from aram_backend.reconciliation_review import NoteReference
from aram_backend.trial_balance_diagnostic import (
    TrialBalanceDiagnostic, analyze_trial_balance,
)


def _freeze_sequence(value: object, label: str) -> tuple[Any, ...]:
    if not isinstance(value, (tuple, list)):
        raise CoverageError("INVALID_FIVE_STATEMENT_" + label)
    return tuple(value)


@dataclass(frozen=True)
class FiveStatementPipelineResult:
    balance_sheet: BalanceSheetCandidate
    income_statement: IncomeStatementCandidate
    equity_changes: EquityChangesCandidate
    cash_flow: DirectCashFlowCandidate
    trial_balance: TrialBalanceDiagnostic
    reconciliation: CrossStatementReconciliation
    mapping_coverage: CoveragePreview
    kind: str = "UNAPPROVED_FIVE_STATEMENT_PIPELINE_CANDIDATE"
    source_ledger_completeness_verified: bool = False
    accounting_policy_authorized: bool = False
    independently_reviewed: bool = False
    trusted_approvals: bool = False
    official_financial_statement: bool = False
    export_authorized: bool = False
    releasable: bool = False

    @property
    def company_code(self) -> str:
        return self.reconciliation.company_code

    @property
    def fiscal_year(self) -> int:
        return self.reconciliation.fiscal_year

    @property
    def source_sha256(self) -> str:
        return self.reconciliation.source_sha256

    @property
    def eligible_for_analyst_review(self) -> bool:
        return self.reconciliation.eligible_for_analyst_review

    @property
    def findings(self) -> tuple[str, ...]:
        return self.reconciliation.findings

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "company_code": self.company_code,
            "fiscal_year": self.fiscal_year,
            "source_sha256": self.source_sha256,
            "eligible_for_analyst_review": self.eligible_for_analyst_review,
            "findings": list(self.findings),
            "balance_sheet": self.balance_sheet.to_dict(),
            "income_statement": self.income_statement.to_dict(),
            "equity_changes": self.equity_changes.to_dict(),
            "cash_flow": self.cash_flow.to_dict(),
            "trial_balance": self.trial_balance.to_dict(),
            "reconciliation": self.reconciliation.to_dict(),
            "mapping_coverage": self.mapping_coverage.to_dict(),
            "source_ledger_completeness_verified": False,
            "accounting_policy_authorized": False,
            "independently_reviewed": False,
            "trusted_approvals": False,
            "official_financial_statement": False,
            "export_authorized": False,
            "releasable": False,
        }


def build_five_statement_pipeline(
    workbook_bytes: bytes, *,
    company_code: str,
    fiscal_year: int,
    references: Sequence[NoteReference],
    balance_sheet_policies: Sequence[BalanceSheetLinePolicy],
    income_statement_policies: Sequence[IncomeStatementLinePolicy],
    equity_movement_policies: Sequence[EquityMovementPolicy],
    currency: str,
    unit: str,
    cash_accounts: Sequence[CashAccountPolicy],
    counterpart_policies: Sequence[CashCounterpartPolicy],
    transactions: Sequence[CashFlowEntry],
    cash_balance_notes: Sequence[CashBalanceNoteSelection],
) -> FiveStatementPipelineResult:
    """Run all five candidate builders on one source snapshot and reconcile.

    Input sequences are frozen once at the orchestration boundary. In
    particular, the exact same immutable reference tuple is supplied to BS,
    IS and EQ, preventing accidental reference-snapshot drift between engines.
    A blocked upstream candidate is returned as a blocked pipeline result;
    invalid source/policy preconditions raise CoverageError.
    """
    if type(workbook_bytes) is not bytes or not workbook_bytes:
        raise CoverageError("INVALID_FIVE_STATEMENT_WORKBOOK_BYTES")
    if (not isinstance(company_code, str) or not company_code.strip()
            or company_code != company_code.strip()):
        raise CoverageError("INVALID_FIVE_STATEMENT_COMPANY_SCOPE")
    if type(fiscal_year) is not int or fiscal_year <= 0:
        raise CoverageError("INVALID_FIVE_STATEMENT_FISCAL_YEAR")

    shared_references = _freeze_sequence(references, "NOTE_REFERENCES")
    bs_policies = _freeze_sequence(balance_sheet_policies, "BS_POLICIES")
    is_policies = _freeze_sequence(income_statement_policies, "IS_POLICIES")
    eq_policies = _freeze_sequence(equity_movement_policies, "EQ_POLICIES")
    selected_cash_accounts = _freeze_sequence(cash_accounts, "CASH_ACCOUNTS")
    selected_counterpart_policies = _freeze_sequence(
        counterpart_policies, "COUNTERPART_POLICIES",
    )
    transaction_rows = _freeze_sequence(transactions, "CASH_TRANSACTIONS")
    cash_note_selections = _freeze_sequence(
        cash_balance_notes, "CASH_NOTE_SELECTIONS",
    )

    balance_sheet = build_balance_sheet_candidate(
        workbook_bytes, company_code=company_code, fiscal_year=fiscal_year,
        references=shared_references, policies=bs_policies,
    )
    income_statement = build_income_statement_candidate(
        workbook_bytes, company_code=company_code, fiscal_year=fiscal_year,
        references=shared_references, policies=is_policies,
    )
    equity_changes = build_equity_changes_candidate(
        workbook_bytes, company_code=company_code, fiscal_year=fiscal_year,
        references=shared_references, policies=eq_policies,
    )
    cash_flow = build_direct_cash_flow_candidate(
        workbook_bytes, company_code=company_code, fiscal_year=fiscal_year,
        currency=currency, unit=unit,
        cash_accounts=selected_cash_accounts,
        counterpart_policies=selected_counterpart_policies,
        transactions=transaction_rows,
    )
    trial_balance = analyze_trial_balance(
        workbook_bytes, company_code=company_code, fiscal_year=fiscal_year,
    )
    mapping_coverage = preview_mapping_coverage(
        workbook_bytes, company_code=company_code, fiscal_year=fiscal_year,
    )
    reconciliation = reconcile_cross_statements(
        balance_sheet=balance_sheet,
        income_statement=income_statement,
        equity_changes=equity_changes,
        cash_flow=cash_flow,
        trial_balance=trial_balance,
        cash_balance_notes=cash_note_selections,
    )
    return FiveStatementPipelineResult(
        balance_sheet=balance_sheet,
        income_statement=income_statement,
        equity_changes=equity_changes,
        cash_flow=cash_flow,
        trial_balance=trial_balance,
        reconciliation=reconciliation,
        mapping_coverage=mapping_coverage,
    )
