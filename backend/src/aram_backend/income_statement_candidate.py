"""Unsigned, read-only income statement candidate from reconciled Pilot XLSX.

No statutory statement, tax assessment, accounting sign inference, database
write, approval or export is performed. Every source-note classification and
sign is an explicit, untrusted external policy requiring later independent
finance-owner approval.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from typing import Any, Sequence

from aram_backend.coverage_preview import CoverageError
from aram_backend.reconciliation_review import (
    NoteReference, _money, _sum_exact, reconcile_workbook_for_review,
)

MAX_POLICIES = 10_000
CATEGORIES = frozenset({
    "REVENUE", "COST_OF_REVENUE", "OPERATING_EXPENSE",
    "OTHER_INCOME", "OTHER_EXPENSE", "TAX_EXPENSE",
})
_EXPENSES = frozenset({
    "COST_OF_REVENUE", "OPERATING_EXPENSE", "OTHER_EXPENSE", "TAX_EXPENSE",
})


@dataclass(frozen=True)
class IncomeStatementLinePolicy:
    statement_section: str
    note_number: str
    subnote_code: str
    category: str
    sign_multiplier: int
    line_label: str
    policy_evidence_ref: str


@dataclass(frozen=True)
class CandidateIncomeStatementLine:
    statement_section: str
    note_number: str
    subnote_code: str
    category: str
    sign_multiplier: int
    line_label: str
    source_closing_exposure: str
    presentation_amount: str
    note_reference_evidence: str
    policy_evidence_ref: str


@dataclass(frozen=True)
class IncomeStatementCandidate:
    company_code: str
    fiscal_year: int
    source_sha256: str
    note_references_sha256: str
    presentation_policies_sha256: str
    revenue_total: str
    cost_of_revenue_total: str
    gross_profit: str
    operating_expense_total: str
    operating_profit: str
    other_income_total: str
    other_expense_total: str
    profit_before_tax: str
    tax_expense_total: str
    net_result: str
    lines: tuple[CandidateIncomeStatementLine, ...]
    findings: tuple[str, ...]
    eligible_for_analyst_review: bool
    kind: str = "UNAPPROVED_INCOME_STATEMENT_PRESENTATION_CANDIDATE"
    official_financial_statement: bool = False
    accounting_policy_authorized: bool = False
    independently_reviewed: bool = False
    export_authorized: bool = False
    releasable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _required_text(value: object, label: str, *, blank_ok: bool = False) -> str:
    if (not isinstance(value, str) or len(value) > 256
            or value != value.strip() or (not blank_ok and not value)
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise CoverageError("INVALID_INCOME_POLICY_" + label)
    return value


def _key(policy: IncomeStatementLinePolicy) -> tuple[str, str, str]:
    return policy.statement_section, policy.note_number, policy.subnote_code


def _validate_policies(
    policies: Sequence[IncomeStatementLinePolicy],
) -> tuple[dict[tuple[str, str, str], IncomeStatementLinePolicy], str]:
    if not isinstance(policies, (list, tuple)) or len(policies) > MAX_POLICIES:
        raise CoverageError("INVALID_INCOME_POLICIES")
    result: dict[tuple[str, str, str], IncomeStatementLinePolicy] = {}
    for policy in policies:
        if not isinstance(policy, IncomeStatementLinePolicy):
            raise CoverageError("INVALID_INCOME_POLICY")
        _required_text(policy.statement_section, "SECTION")
        _required_text(policy.note_number, "NOTE")
        _required_text(policy.subnote_code, "SUBNOTE", blank_ok=True)
        _required_text(policy.line_label, "LABEL")
        _required_text(policy.policy_evidence_ref, "EVIDENCE")
        if not isinstance(policy.category, str) or policy.category not in CATEGORIES:
            raise CoverageError("INVALID_INCOME_POLICY_CATEGORY")
        if type(policy.sign_multiplier) is not int or policy.sign_multiplier not in (-1, 1):
            raise CoverageError("INVALID_INCOME_POLICY_SIGN")
        key = _key(policy)
        if key in result:
            raise CoverageError("DUPLICATE_INCOME_POLICY")
        result[key] = policy
    canonical = [asdict(result[key]) for key in sorted(result)]
    digest = sha256(json.dumps(
        canonical, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()
    return result, digest


def build_income_statement_candidate(
    workbook_bytes: bytes, *, company_code: str, fiscal_year: int,
    references: Sequence[NoteReference],
    policies: Sequence[IncomeStatementLinePolicy],
) -> IncomeStatementCandidate:
    """Create a complete-reference, explicit-sign analyst-only income preview.

    No financial-standard assumptions about account nature, cash versus
    accrual basis, taxes, extraordinary items or comparative periods are made.
    """
    selected, policy_hash = _validate_policies(policies)
    review = reconcile_workbook_for_review(
        workbook_bytes, company_code=company_code,
        fiscal_year=fiscal_year, references=references,
    )
    if (review.kind != "UNAPPROVED_NOTE_RECONCILIATION_REVIEW"
            or review.financial_statement or review.trusted_approvals
            or review.approved or review.releasable):
        raise CoverageError("INVALID_REVIEW_PROVENANCE")

    income_notes = {
        (note.section, note.note_number, note.subnote_code): note
        for note in review.notes if note.statement == "IS"
    }
    findings: list[str] = []
    if not review.matched_for_analyst_review:
        findings.append("UPSTREAM_RECONCILIATION_BLOCKED")
    if not income_notes:
        findings.append("NO_INCOME_STATEMENT_NOTES")
    if set(income_notes) - set(selected):
        findings.append("MISSING_INCOME_POLICY")
    if set(selected) - set(income_notes):
        findings.append("ORPHAN_INCOME_POLICY")

    lines: list[CandidateIncomeStatementLine] = []
    amounts_by_category: dict[str, list[Decimal]] = {
        category: [] for category in sorted(CATEGORIES)
    }

    for target in sorted(set(income_notes) & set(selected)):
        note = income_notes[target]
        policy = selected[target]
        if not note.matched or note.candidate_closing_exposure is None:
            continue
        exposure = _money(note.candidate_closing_exposure)
        # Decimal source/reference exponent and digit limits are checked
        # upstream; 400-digit precision ensures no presentation rounding.
        with localcontext() as ctx:
            ctx.prec = 400
            displayed = exposure * policy.sign_multiplier
        if displayed < 0:
            findings.append("NEGATIVE_INCOME_PRESENTATION_AMOUNT")
        amounts_by_category[policy.category].append(displayed)
        lines.append(CandidateIncomeStatementLine(
            statement_section=policy.statement_section,
            note_number=policy.note_number, subnote_code=policy.subnote_code,
            category=policy.category, sign_multiplier=policy.sign_multiplier,
            line_label=policy.line_label,
            source_closing_exposure=str(exposure),
            presentation_amount=str(displayed),
            note_reference_evidence=note.evidence_ref or "",
            policy_evidence_ref=policy.policy_evidence_ref,
        ))

    totals = {
        category: _sum_exact(amounts)
        for category, amounts in amounts_by_category.items()
    }
    revenue = totals["REVENUE"]
    cost = totals["COST_OF_REVENUE"]
    operating_expense = totals["OPERATING_EXPENSE"]
    other_income = totals["OTHER_INCOME"]
    other_expense = totals["OTHER_EXPENSE"]
    tax = totals["TAX_EXPENSE"]
    gross = _sum_exact([revenue, -cost])
    operating = _sum_exact([gross, -operating_expense])
    before_tax = _sum_exact([operating, other_income, -other_expense])
    net = _sum_exact([before_tax, -tax])

    if not any(line.category == "REVENUE" for line in lines):
        findings.append("NO_REVENUE_LINES")
    if not any(line.category in _EXPENSES for line in lines):
        findings.append("NO_EXPENSE_LINES")

    return IncomeStatementCandidate(
        company_code=review.company_code, fiscal_year=review.fiscal_year,
        source_sha256=review.source_sha256,
        note_references_sha256=review.reference_sha256,
        presentation_policies_sha256=policy_hash,
        revenue_total=str(revenue),
        cost_of_revenue_total=str(cost),
        gross_profit=str(gross),
        operating_expense_total=str(operating_expense),
        operating_profit=str(operating),
        other_income_total=str(other_income),
        other_expense_total=str(other_expense),
        profit_before_tax=str(before_tax),
        tax_expense_total=str(tax),
        net_result=str(net),
        lines=tuple(lines), findings=tuple(sorted(set(findings))),
        eligible_for_analyst_review=not findings and bool(lines),
    )
