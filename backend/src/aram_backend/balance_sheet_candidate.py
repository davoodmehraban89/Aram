"""Non-official balance-sheet presentation candidate with explicit accounting policy.

This is a read-only analyst preview, not an Iranian statutory financial
statement. It uses full-precision Decimal arithmetic and never infers a
debit/credit nature, classification or sign from the source chart of accounts.
An independently authorized finance owner must still approve each policy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from hashlib import sha256
import json
from typing import Any, Sequence

from aram_backend.coverage_preview import CoverageError
from aram_backend.reconciliation_review import (
    NoteReference, ReconciliationReview, _money, _sum_exact,
    reconcile_workbook_for_review,
)

MAX_POLICIES = 10_000
CATEGORIES = frozenset({"ASSETS", "LIABILITIES", "EQUITY"})


@dataclass(frozen=True)
class BalanceSheetLinePolicy:
    """Explicit external presentation rule; never a source of financial authority."""

    statement_section: str
    note_number: str
    subnote_code: str
    category: str
    sign_multiplier: int
    line_label: str
    policy_evidence_ref: str


@dataclass(frozen=True)
class CandidateBalanceSheetLine:
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
class BalanceSheetCandidate:
    company_code: str
    fiscal_year: int
    source_sha256: str
    note_references_sha256: str
    presentation_policies_sha256: str
    assets_total: str
    liabilities_total: str
    equity_total: str
    balance_difference: str
    lines: tuple[CandidateBalanceSheetLine, ...]
    findings: tuple[str, ...]
    arithmetically_balanced: bool
    eligible_for_analyst_review: bool
    kind: str = "UNAPPROVED_BALANCE_SHEET_PRESENTATION_CANDIDATE"
    official_financial_statement: bool = False
    accounting_policy_authorized: bool = False
    independently_reviewed: bool = False
    export_authorized: bool = False
    releasable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _required_text(value: object, label: str, *, blank_ok: bool = False) -> str:
    if not isinstance(value, str) or len(value) > 256:
        raise CoverageError("INVALID_PRESENTATION_" + label)
    if (value != value.strip() or (not value and not blank_ok)
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise CoverageError("INVALID_PRESENTATION_" + label)
    return value


def _key(policy: BalanceSheetLinePolicy) -> tuple[str, str, str]:
    return policy.statement_section, policy.note_number, policy.subnote_code


def _policies(
    policies: Sequence[BalanceSheetLinePolicy],
) -> tuple[dict[tuple[str, str, str], BalanceSheetLinePolicy], str]:
    if not isinstance(policies, (tuple, list)) or len(policies) > MAX_POLICIES:
        raise CoverageError("INVALID_PRESENTATION_POLICIES")
    selected: dict[tuple[str, str, str], BalanceSheetLinePolicy] = {}
    for policy in policies:
        if not isinstance(policy, BalanceSheetLinePolicy):
            raise CoverageError("INVALID_PRESENTATION_POLICY")
        _required_text(policy.statement_section, "SECTION")
        _required_text(policy.note_number, "NOTE")
        _required_text(policy.subnote_code, "SUBNOTE", blank_ok=True)
        _required_text(policy.line_label, "LABEL")
        _required_text(policy.policy_evidence_ref, "EVIDENCE")
        if policy.category not in CATEGORIES:
            raise CoverageError("INVALID_PRESENTATION_CATEGORY")
        if type(policy.sign_multiplier) is not int or policy.sign_multiplier not in {-1, 1}:
            raise CoverageError("INVALID_PRESENTATION_SIGN")
        key = _key(policy)
        if key in selected:
            raise CoverageError("DUPLICATE_PRESENTATION_POLICY")
        selected[key] = policy
    canonical = [
        asdict(selected[key]) for key in sorted(selected)
    ]
    digest = sha256(
        json.dumps(
            canonical, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return selected, digest


def build_balance_sheet_candidate(
    workbook_bytes: bytes, *,
    company_code: str,
    fiscal_year: int,
    references: Sequence[NoteReference],
    policies: Sequence[BalanceSheetLinePolicy],
) -> BalanceSheetCandidate:
    """Build ONLY a traceable unsigned BS analyst presentation candidate.

    Every candidate BS note must have an exact reference AND one explicit
    accounting policy. Other statement notes are not presented as BS rows.
    All mapped accounts across statements still undergo reconciliation.
    """
    policy_by_note, policy_digest = _policies(policies)
    review: ReconciliationReview = reconcile_workbook_for_review(
        workbook_bytes, company_code=company_code,
        fiscal_year=fiscal_year, references=references,
    )
    if (review.kind != "UNAPPROVED_NOTE_RECONCILIATION_REVIEW"
            or review.financial_statement or review.trusted_approvals
            or review.approved or review.releasable):
        raise CoverageError("REVIEW_PROVENANCE_INVALID")

    bs_notes = {
        (note.section, note.note_number, note.subnote_code): note
        for note in review.notes if note.statement == "BS"
    }
    findings: list[str] = []
    if not review.matched_for_analyst_review:
        findings.append("UPSTREAM_RECONCILIATION_BLOCKED")
    if not bs_notes:
        findings.append("NO_BALANCE_SHEET_NOTES")
    missing = sorted(set(bs_notes) - set(policy_by_note))
    extra = sorted(set(policy_by_note) - set(bs_notes))
    if missing:
        findings.append("MISSING_EXPLICIT_PRESENTATION_POLICY")
    if extra:
        findings.append("ORPHAN_PRESENTATION_POLICY")

    buckets: dict[str, list[Decimal]] = {cat: [] for cat in sorted(CATEGORIES)}
    output: list[CandidateBalanceSheetLine] = []
    for target in sorted(set(bs_notes) & set(policy_by_note)):
        note = bs_notes[target]
        policy = policy_by_note[target]
        if not note.matched or note.candidate_closing_exposure is None:
            continue
        # Display amount uses an explicit sign; never guessed from account codes.
        exposure = _money(note.candidate_closing_exposure)
        with __import__("decimal").localcontext() as context:
            context.prec = 256
            displayed = exposure * policy.sign_multiplier
        buckets[policy.category].append(displayed)
        if displayed < 0:
            findings.append("NEGATIVE_PRESENTATION_AMOUNT")
        output.append(CandidateBalanceSheetLine(
            statement_section=policy.statement_section,
            note_number=policy.note_number, subnote_code=policy.subnote_code,
            category=policy.category, sign_multiplier=policy.sign_multiplier,
            line_label=policy.line_label,
            source_closing_exposure=str(exposure),
            presentation_amount=str(displayed),
            note_reference_evidence=note.evidence_ref or "",
            policy_evidence_ref=policy.policy_evidence_ref,
        ))

    totals = {key: _sum_exact(values) for key, values in buckets.items()}
    diff = _sum_exact([
        totals["ASSETS"], -totals["LIABILITIES"], -totals["EQUITY"]
    ])
    if diff != 0:
        findings.append("BALANCE_SHEET_DOES_NOT_BALANCE")
    # A balanced collection of negative offsetting lines is not accepted
    # as analyst-ready even when the equation happens to hold.
    if not any(line.category == "ASSETS" for line in output):
        findings.append("NO_ASSET_LINES")
    if not any(line.category == "LIABILITIES" for line in output):
        findings.append("NO_LIABILITY_LINES")
    if not any(line.category == "EQUITY" for line in output):
        findings.append("NO_EQUITY_LINES")

    return BalanceSheetCandidate(
        company_code=review.company_code, fiscal_year=review.fiscal_year,
        source_sha256=review.source_sha256,
        note_references_sha256=review.reference_sha256,
        presentation_policies_sha256=policy_digest,
        assets_total=str(totals["ASSETS"]),
        liabilities_total=str(totals["LIABILITIES"]),
        equity_total=str(totals["EQUITY"]),
        balance_difference=str(diff), lines=tuple(output),
        findings=tuple(sorted(set(findings))),
        arithmetically_balanced=diff == 0,
        eligible_for_analyst_review=not findings and bool(output),
    )
