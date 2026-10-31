"""Fail-closed provenance and tie-out checks for desktop-only previews."""
from __future__ import annotations

import re

from aram_backend.coverage_preview import (
    AccountTrace, CoverageError, CoveragePreview, MappingTrace,
)
from aram_backend.reconciliation_review import _money, _sum_exact
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
    # The mapping trace is generated from the same immutable XLSX bytes as
    # the five statements. Do not render account-to-note lineage if it lacks
    # the exact company, year, source hash, account rows or debit-net figures.
    coverage = result.mapping_coverage
    if type(coverage) is not CoveragePreview:
        raise CoverageError("DESKTOP_PREVIEW_MAPPING_TYPE_INVALID")
    if (
        coverage.kind != "UNAPPROVED_MAPPING_COVERAGE_PREVIEW"
        or type(coverage.financial_statement) is not bool
        or type(coverage.trusted_approvals) is not bool
        or type(coverage.releasable) is not bool
        or coverage.financial_statement or coverage.trusted_approvals
        or coverage.releasable
        or coverage.company_code != reconciliation.company_code
        or coverage.fiscal_year != reconciliation.fiscal_year
        or coverage.source_sha256 != reconciliation.source_sha256
    ):
        raise CoverageError("DESKTOP_PREVIEW_MAPPING_PROVENANCE_INVALID")
    if (type(coverage.accounts) is not tuple
            or type(coverage.mappings) is not tuple
            or type(coverage.notes) is not tuple
            or type(coverage.account_count) is not int
            or coverage.account_count != len(coverage.accounts)):
        raise CoverageError("DESKTOP_PREVIEW_MAPPING_COUNT_INVALID")
    tb_by_code = {
        row.account_code: row for row in result.trial_balance.accounts
    }
    if len(tb_by_code) != len(result.trial_balance.accounts):
        raise CoverageError("DESKTOP_PREVIEW_TB_DUPLICATE_ACCOUNT")
    by_account: dict[str, AccountTrace] = {}
    for account in coverage.accounts:
        if type(account) is not AccountTrace or account.account_code in by_account:
            raise CoverageError("DESKTOP_PREVIEW_MAPPING_ACCOUNT_INVALID")
        tb_account = tb_by_code.get(account.account_code)
        if (
            tb_account is None or account.account_name != tb_account.account_name
            or account.account_excel_row != tb_account.excel_row
            or account.source_row != tb_account.source_row
            or _money(account.closing_exposure) != _money(tb_account.closing)
        ):
            raise CoverageError("DESKTOP_PREVIEW_MAPPING_SOURCE_MISMATCH")
        by_account[account.account_code] = account
    if set(by_account) != set(tb_by_code):
        raise CoverageError("DESKTOP_PREVIEW_MAPPING_SOURCE_MISMATCH")

    mapping_counts: dict[str, int] = {}
    included_accounts: set[str] = set()
    seen_mapping_rows: set[int] = set()
    seen_mapping_ids: set[str] = set()
    note_amounts: dict[tuple[str, str, str, str], list] = {}
    note_codes: dict[tuple[str, str, str, str], list[str]] = {}
    seen_account_statement: set[tuple[str, str]] = set()
    for mapping in coverage.mappings:
        if type(mapping) is not MappingTrace:
            raise CoverageError("DESKTOP_PREVIEW_MAPPING_ROW_INVALID")
        account = by_account.get(mapping.account_code)
        if (
            account is None or type(mapping.included) is not bool
            or mapping.account_name != account.account_name
            or mapping.account_excel_row != account.account_excel_row
            or mapping.source_row != account.source_row
            or _money(mapping.closing_exposure) != _money(account.closing_exposure)
            or type(mapping.mapping_excel_row) is not int
            or mapping.mapping_excel_row < 2
            or mapping.mapping_excel_row in seen_mapping_rows
            or not isinstance(mapping.mapping_id, str)
            or not mapping.mapping_id
            or mapping.mapping_id in seen_mapping_ids
        ):
            raise CoverageError("DESKTOP_PREVIEW_MAPPING_ROW_INVALID")
        seen_mapping_rows.add(mapping.mapping_excel_row)
        seen_mapping_ids.add(mapping.mapping_id)
        mapping_counts[mapping.account_code] = (
            mapping_counts.get(mapping.account_code, 0) + 1
        )
        if mapping.included:
            statement_key = (mapping.account_code, mapping.target_statement)
            if statement_key in seen_account_statement:
                raise CoverageError("DESKTOP_PREVIEW_DUPLICATE_MAPPING_TARGET")
            seen_account_statement.add(statement_key)
            included_accounts.add(mapping.account_code)
            note_key = (
                mapping.target_statement, mapping.target_section,
                mapping.target_note, mapping.target_subnote,
            )
            note_amounts.setdefault(note_key, []).append(
                _money(mapping.closing_exposure)
            )
            note_codes.setdefault(note_key, []).append(mapping.account_code)
    for account in coverage.accounts:
        if (
            type(account.mapping_count) is not int
            or account.mapping_count != mapping_counts.get(account.account_code, 0)
            or type(account.included) is not bool
            or account.included != (account.account_code in included_accounts)
        ):
            raise CoverageError("DESKTOP_PREVIEW_MAPPING_COUNT_INVALID")
    if (
        coverage.candidate_mapped_accounts != len(included_accounts)
        or coverage.blocked_accounts != len(coverage.accounts) - len(included_accounts)
    ):
        raise CoverageError("DESKTOP_PREVIEW_MAPPING_COUNT_INVALID")

    seen_note_keys: set[tuple[str, str, str, str]] = set()
    for note in coverage.notes:
        note_key = (
            note.statement, note.section, note.note_number, note.subnote_code,
        )
        if note_key in seen_note_keys:
            raise CoverageError("DESKTOP_PREVIEW_MAPPING_NOTE_DUPLICATE")
        seen_note_keys.add(note_key)
        if (
            note_key not in note_amounts
            or _money(note.closing_exposure) != _sum_exact(note_amounts[note_key])
            or tuple(note_codes[note_key]) != note.account_codes
        ):
            raise CoverageError("DESKTOP_PREVIEW_MAPPING_NOTE_INVALID")
    if seen_note_keys != set(note_amounts):
        raise CoverageError("DESKTOP_PREVIEW_MAPPING_NOTE_INVALID")

    # Every displayed BS/IS/EQ candidate note must use the same exact
    # unrounded exposure as the account-to-note mapping built from this XLSX.
    # Do not infer accounting signs or reconcile unlike statements together.
    candidates_by_statement = (
        ("BS", result.balance_sheet.lines),
        ("IS", result.income_statement.lines),
        ("EQ", result.equity_changes.note_movements),
    )
    covered_notes = {
        (note.statement, note.section, note.note_number, note.subnote_code):
            _money(note.closing_exposure)
        for note in coverage.notes
    }
    for statement, lines in candidates_by_statement:
        for line in lines:
            key = (
                statement, line.statement_section,
                line.note_number, line.subnote_code,
            )
            if key not in covered_notes:
                raise CoverageError("DESKTOP_PREVIEW_NOTE_SOURCE_MISSING")
            try:
                line_exposure = _money(line.source_closing_exposure)
            except CoverageError as exc:
                raise CoverageError("DESKTOP_PREVIEW_NOTE_SOURCE_INVALID") from exc
            if line_exposure != covered_notes[key]:
                raise CoverageError("DESKTOP_PREVIEW_NOTE_SOURCE_MISMATCH")

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
