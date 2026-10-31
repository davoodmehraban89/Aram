"""Fail-closed provenance and tie-out checks for desktop-only previews."""
from __future__ import annotations

import re

from aram_backend.coverage_preview import CoverageError
from aram_backend.balance_sheet_candidate import BalanceSheetCandidate
from aram_backend.cash_flow_direct_candidate import DirectCashFlowCandidate
from aram_backend.cross_statement_reconciliation import CrossStatementReconciliation
from aram_backend.equity_changes_candidate import EquityChangesCandidate
from aram_backend.five_statement_pipeline import FiveStatementPipelineResult
from aram_backend.income_statement_candidate import IncomeStatementCandidate
from aram_backend.trial_balance_diagnostic import TrialBalanceDiagnostic


def _require_false(obj: object, fields: tuple[str, ...]) -> None:
    for field in fields:
        value = getattr(obj, field)
        if type(value) is not bool or value:
            raise CoverageError("DESKTOP_PREVIEW_PROVENANCE_INVALID")


def _require_bool(obj: object, field: str) -> bool:
    value = getattr(obj, field)
    if type(value) is not bool:
        raise CoverageError("DESKTOP_PREVIEW_BOOLEAN_INVALID")
    return value


def validate_desktop_pipeline_result(result: FiveStatementPipelineResult) -> None:
    """Verify the exact typed orchestration result before rendering any data."""
    if type(result) is not FiveStatementPipelineResult:
        raise CoverageError("DESKTOP_PREVIEW_PIPELINE_TYPE_INVALID")
    candidates = (
        (result.balance_sheet, BalanceSheetCandidate, "UNAPPROVED_BALANCE_SHEET_PRESENTATION_CANDIDATE"),
        (result.income_statement, IncomeStatementCandidate, "UNAPPROVED_INCOME_STATEMENT_PRESENTATION_CANDIDATE"),
        (result.equity_changes, EquityChangesCandidate, "UNAPPROVED_EQUITY_CHANGES_PRESENTATION_CANDIDATE"),
        (result.cash_flow, DirectCashFlowCandidate, "UNAPPROVED_DIRECT_CASH_FLOW_CANDIDATE"),
        (result.trial_balance, TrialBalanceDiagnostic, "UNAPPROVED_TRIAL_BALANCE_DIAGNOSTIC"),
    )
    if result.kind != "UNAPPROVED_FIVE_STATEMENT_PIPELINE_CANDIDATE":
        raise CoverageError("DESKTOP_PREVIEW_PIPELINE_KIND_INVALID")
    if type(result.reconciliation) is not CrossStatementReconciliation:
        raise CoverageError("DESKTOP_PREVIEW_RECONCILIATION_TYPE_INVALID")
    if result.reconciliation.kind != "UNAPPROVED_CROSS_STATEMENT_RECONCILIATION":
        raise CoverageError("DESKTOP_PREVIEW_RECONCILIATION_KIND_INVALID")
    _require_false(result, (
        "source_ledger_completeness_verified", "accounting_policy_authorized",
        "independently_reviewed", "trusted_approvals",
        "official_financial_statement", "export_authorized", "releasable",
    ))
    _require_false(result.reconciliation, (
        "source_ledger_completeness_verified", "accounting_policy_authorized",
        "independently_reviewed", "trusted_approvals",
        "official_financial_statement", "export_authorized", "releasable",
    ))
    source_hashes: set[str] = set()
    companies: set[str] = set()
    years: set[int] = set()
    eligibility: list[bool] = []
    for candidate, expected_type, expected_kind in candidates:
        if type(candidate) is not expected_type or candidate.kind != expected_kind:
            raise CoverageError("DESKTOP_PREVIEW_CANDIDATE_TYPE_INVALID")
        if (not isinstance(candidate.source_sha256, str)
                or not re.fullmatch(r"[0-9a-f]{64}", candidate.source_sha256)):
            raise CoverageError("DESKTOP_PREVIEW_SOURCE_HASH_INVALID")
        source_hashes.add(candidate.source_sha256)
        if (not isinstance(candidate.company_code, str)
                or not candidate.company_code
                or candidate.company_code != candidate.company_code.strip()
                or type(candidate.fiscal_year) is not int
                or candidate.fiscal_year <= 0):
            raise CoverageError("DESKTOP_PREVIEW_SCOPE_INVALID")
        companies.add(candidate.company_code)
        years.add(candidate.fiscal_year)
        for hash_field in (
            "note_references_sha256", "presentation_policies_sha256",
            "transaction_ledger_sha256", "classification_policies_sha256",
        ):
            if hasattr(candidate, hash_field):
                digest = getattr(candidate, hash_field)
                if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                    raise CoverageError("DESKTOP_PREVIEW_PROVENANCE_HASH_INVALID")
        eligible_field = (
            "balanced_for_analyst_review" if isinstance(candidate, TrialBalanceDiagnostic)
            else "eligible_for_analyst_review"
        )
        eligibility.append(_require_bool(candidate, eligible_field))
        findings = candidate.findings
        if not isinstance(findings, tuple) or any(
            not isinstance(item, str) or not item for item in findings
        ):
            raise CoverageError("DESKTOP_PREVIEW_FINDINGS_INVALID")
        if isinstance(candidate, BalanceSheetCandidate):
            flags = ("official_financial_statement", "accounting_policy_authorized",
                     "independently_reviewed", "export_authorized", "releasable")
        elif isinstance(candidate, IncomeStatementCandidate):
            flags = ("official_financial_statement", "accounting_policy_authorized",
                     "independently_reviewed", "export_authorized", "releasable")
        elif isinstance(candidate, EquityChangesCandidate):
            flags = ("official_financial_statement", "accounting_policy_authorized",
                     "source_ledger_completeness_verified", "independently_reviewed",
                     "export_authorized", "releasable")
        elif isinstance(candidate, DirectCashFlowCandidate):
            flags = ("cash_account_scope_owner_approved",
                     "transaction_ledger_completeness_verified",
                     "accounting_policy_authorized", "official_financial_statement",
                     "independently_reviewed", "export_authorized", "releasable")
        else:
            flags = ("source_ledger_completeness_verified",
                     "accounting_policies_verified", "official_financial_statement",
                     "independently_reviewed", "releasable")
        _require_false(candidate, flags)
    reconciliation = result.reconciliation
    if (len(source_hashes) != 1
            or reconciliation.source_sha256 not in source_hashes
            or not isinstance(reconciliation.source_sha256, str)
            or not re.fullmatch(r"[0-9a-f]{64}", reconciliation.source_sha256)
            or reconciliation.same_source_snapshot is not True):
        raise CoverageError("DESKTOP_PREVIEW_SOURCE_SNAPSHOT_MISMATCH")
    if (not isinstance(reconciliation.cash_flow_transaction_ledger_sha256, str)
            or not re.fullmatch(r"[0-9a-f]{64}", reconciliation.cash_flow_transaction_ledger_sha256)
            or not isinstance(reconciliation.cash_note_selection_sha256, str)
            or not re.fullmatch(r"[0-9a-f]{64}", reconciliation.cash_note_selection_sha256)):
        raise CoverageError("DESKTOP_PREVIEW_RECONCILIATION_HASH_INVALID")
    if (not isinstance(reconciliation.findings, tuple)
            or any(not isinstance(item, str) or not item for item in reconciliation.findings)):
        raise CoverageError("DESKTOP_PREVIEW_RECONCILIATION_FINDINGS_INVALID")
    if companies != {reconciliation.company_code} or years != {reconciliation.fiscal_year}:
        raise CoverageError("DESKTOP_PREVIEW_SCOPE_MISMATCH")
    if (result.balance_sheet.note_references_sha256
            != result.income_statement.note_references_sha256
            or result.balance_sheet.note_references_sha256
            != result.equity_changes.note_references_sha256):
        raise CoverageError("DESKTOP_PREVIEW_REFERENCE_SNAPSHOT_MISMATCH")
    ties = (
        (result.balance_sheet.equity_total, reconciliation.balance_sheet_equity_total),
        (result.balance_sheet.balance_difference, reconciliation.balance_sheet_difference),
        (result.income_statement.net_result, reconciliation.income_statement_net_result),
        (result.equity_changes.closing_equity_total, reconciliation.equity_statement_closing_total),
        (result.equity_changes.net_profit_loss_movements, reconciliation.equity_net_profit_loss_movements),
        (result.cash_flow.closing_cash_and_equivalents, reconciliation.cash_flow_closing_cash),
        (result.trial_balance.opening_debit_net_total, reconciliation.trial_balance_opening_debit_net_total),
        (result.trial_balance.movement_difference, reconciliation.trial_balance_movement_difference),
        (result.trial_balance.closing_debit_net_total, reconciliation.trial_balance_closing_debit_net_total),
        (result.cash_flow.transaction_ledger_sha256, reconciliation.cash_flow_transaction_ledger_sha256),
    )
    if any(left != right for left, right in ties):
        raise CoverageError("DESKTOP_PREVIEW_RECONCILIATION_MISMATCH")
    overall = _require_bool(result, "eligible_for_analyst_review")
    if overall:
        if (not _require_bool(reconciliation, "eligible_for_analyst_review")
                or not all(eligibility) or result.findings
                or any(candidate.findings for candidate, _, _ in candidates)):
            raise CoverageError("DESKTOP_PREVIEW_FALSE_ELIGIBILITY")
    else:
        if _require_bool(reconciliation, "eligible_for_analyst_review"):
            raise CoverageError("DESKTOP_PREVIEW_ELIGIBILITY_MISMATCH")
        if not reconciliation.findings and all(eligibility) and not any(
            candidate.findings for candidate, _, _ in candidates
        ):
            raise CoverageError("DESKTOP_PREVIEW_BLOCKED_WITHOUT_FINDINGS")
