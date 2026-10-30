"""Strict, read-only note reconciliation for a synthetic or authorized Pilot workbook.

The module compares candidate mapped closing exposures to explicit, separately
provided reference totals. It neither infers debit/credit sign semantics nor
creates statutory financial statements, approvals, postings, or files.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, localcontext
from hashlib import sha256
import json
from typing import Any, Sequence

from aram_backend.coverage_preview import (
    CoverageError,
    CoveragePreview,
    preview_mapping_coverage,
)

MAX_REFERENCES = 10_000
MAX_TEXT = 256
ALLOWED_STATEMENTS = frozenset({"BS", "IS", "CF", "EQ"})


@dataclass(frozen=True)
class NoteReference:
    statement: str
    section: str
    note_number: str
    subnote_code: str
    expected_closing_exposure: str
    evidence_ref: str


@dataclass(frozen=True)
class ReconciledNote:
    statement: str
    section: str
    note_number: str
    subnote_code: str
    candidate_closing_exposure: str | None
    reference_closing_exposure: str | None
    difference: str | None
    evidence_ref: str | None
    matched: bool


@dataclass(frozen=True)
class ReviewFinding:
    code: str
    account_code: str
    statement: str
    section: str
    note_number: str
    subnote_code: str


@dataclass(frozen=True)
class ReconciliationReview:
    source_sha256: str
    reference_sha256: str
    company_code: str
    fiscal_year: int
    account_count: int
    candidate_mapped_accounts: int
    blocked_accounts: int
    source_closing_exposure: str
    candidate_closing_exposure: str
    blocked_closing_exposure: str
    notes: tuple[ReconciledNote, ...]
    findings: tuple[ReviewFinding, ...]
    matched_for_analyst_review: bool
    kind: str = "UNAPPROVED_NOTE_RECONCILIATION_REVIEW"
    financial_statement: bool = False
    trusted_approvals: bool = False
    approved: bool = False
    releasable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _text(value: object, *, allow_blank: bool = False) -> str:
    if not isinstance(value, str):
        raise CoverageError("INVALID_REFERENCE_TEXT")
    if len(value) > MAX_TEXT or value != value.strip():
        raise CoverageError("INVALID_REFERENCE_TEXT")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise CoverageError("INVALID_REFERENCE_TEXT")
    if not allow_blank and not value:
        raise CoverageError("INVALID_REFERENCE_TEXT")
    return value


def _money(value: object) -> Decimal:
    if not isinstance(value, str) or len(value) > 180 or not value.strip():
        raise CoverageError("INVALID_REFERENCE_AMOUNT")
    try:
        number = Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise CoverageError("INVALID_REFERENCE_AMOUNT") from exc
    # Prevent giant-context denial of service even for zero exponent values.
    if (not number.is_finite() or abs(number.as_tuple().exponent) > 140
            or (number != 0 and abs(number.adjusted()) > 70)):
        raise CoverageError("INVALID_REFERENCE_AMOUNT")
    if len(number.as_tuple().digits) > 150:
        raise CoverageError("INVALID_REFERENCE_AMOUNT")
    return number


def _key(
    statement: str, section: str, note: str, subnote: str
) -> tuple[str, str, str, str]:
    return statement, section, note, subnote


def _sum_exact(amounts: Sequence[Decimal]) -> Decimal:
    if not amounts:
        return Decimal(0)
    integer_digits = max((amount.adjusted() + 1 for amount in amounts if amount), default=1)
    decimal_places = max(0, *(-amount.as_tuple().exponent for amount in amounts))
    with localcontext() as context:
        context.prec = max(100, integer_digits + decimal_places + len(str(len(amounts))) + 8)
        return sum(amounts, Decimal(0))


def _validated_preview(content: bytes, preview: CoveragePreview) -> None:
    if (preview.financial_statement or preview.trusted_approvals
            or preview.releasable or preview.kind != "UNAPPROVED_MAPPING_COVERAGE_PREVIEW"):
        raise CoverageError("COVERAGE_PROVENANCE_INVALID")
    if sha256(content).hexdigest() != preview.source_sha256:
        raise CoverageError("SOURCE_HASH_MISMATCH")
    if (preview.account_count < 1
            or preview.account_count != len(preview.accounts)
            or preview.account_count != preview.candidate_mapped_accounts + preview.blocked_accounts
            or preview.candidate_mapped_accounts != sum(a.included for a in preview.accounts)):
        raise CoverageError("COVERAGE_COUNT_MISMATCH")
    if len({account.account_code for account in preview.accounts}) != preview.account_count:
        raise CoverageError("DUPLICATE_SOURCE_ACCOUNT")
    source_values = [_money(a.closing_exposure) for a in preview.accounts]
    candidate_values = [
        _money(a.closing_exposure) for a in preview.accounts if a.included
    ]
    blocked_values = [
        _money(a.closing_exposure) for a in preview.accounts if not a.included
    ]
    note_values = [_money(n.closing_exposure) for n in preview.notes]
    if (len(preview.notes) != len({
            _key(n.statement, n.section, n.note_number, n.subnote_code)
            for n in preview.notes
        })):
        raise CoverageError("DUPLICATE_CANDIDATE_NOTE")
    if (_sum_exact(source_values) != _money(preview.source_closing_exposure)
            or _sum_exact(candidate_values) != _money(preview.candidate_closing_exposure)
            or _sum_exact(blocked_values) != _money(preview.blocked_closing_exposure)
            or _sum_exact(note_values) != _sum_exact(candidate_values)):
        raise CoverageError("COVERAGE_RECONCILIATION_FAILED")


def reconcile_workbook_for_review(
    content: bytes, *, company_code: str, fiscal_year: int,
    references: Sequence[NoteReference],
) -> ReconciliationReview:
    """Compare workbook-marked candidate closings with explicit *untrusted* references.

    The result is at most an analyst review packet, not approval. Strict,
    zero-tolerance Decimal matching does not certify any statement semantics.
    """
    if not isinstance(references, (tuple, list)) or len(references) > MAX_REFERENCES:
        raise CoverageError("INVALID_REFERENCE_COLLECTION")

    normalized: dict[tuple[str, str, str, str], tuple[Decimal, str]] = {}
    for ref in references:
        if not isinstance(ref, NoteReference):
            raise CoverageError("INVALID_REFERENCE_OBJECT")
        statement = _text(ref.statement)
        if statement not in ALLOWED_STATEMENTS:
            raise CoverageError("INVALID_REFERENCE_STATEMENT")
        target = _key(
            statement, _text(ref.section), _text(ref.note_number),
            _text(ref.subnote_code, allow_blank=True),
        )
        if target in normalized:
            raise CoverageError("DUPLICATE_NOTE_REFERENCE")
        normalized[target] = (_money(ref.expected_closing_exposure), _text(ref.evidence_ref))

    canonical = [
        {
            "target": list(target),
            "expected_closing_exposure": str(amount),
            "evidence_ref": reference,
        }
        for target, (amount, reference) in sorted(normalized.items())
    ]
    reference_hash = sha256(
        json.dumps(canonical, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    preview = preview_mapping_coverage(
        content, company_code=company_code, fiscal_year=fiscal_year,
    )
    _validated_preview(content, preview)

    candidates = {
        _key(n.statement, n.section, n.note_number, n.subnote_code): n
        for n in preview.notes
    }
    findings: list[ReviewFinding] = [
        ReviewFinding(
            code="BLOCKED_ACCOUNT_" + exception.code,
            account_code=exception.account_code,
            statement="", section="", note_number="", subnote_code="",
        ) for exception in preview.exceptions
    ]

    lines: list[ReconciledNote] = []
    for target in sorted(set(candidates) | set(normalized)):
        candidate = candidates.get(target)
        baseline = normalized.get(target)
        actual = _money(candidate.closing_exposure) if candidate is not None else None
        expected = baseline[0] if baseline is not None else None
        if actual is None:
            code = "UNKNOWN_REFERENCE_TARGET"
        elif expected is None:
            code = "MISSING_NOTE_REFERENCE"
        elif actual != expected:
            code = "NOTE_EXPOSURE_MISMATCH"
        else:
            code = None
        if code is not None:
            findings.append(ReviewFinding(
                code=code, account_code="",
                statement=target[0], section=target[1],
                note_number=target[2], subnote_code=target[3],
            ))
        difference = None
        if actual is not None and expected is not None:
            difference = str(_sum_exact([actual, -expected]))
        lines.append(ReconciledNote(
            statement=target[0], section=target[1],
            note_number=target[2], subnote_code=target[3],
            candidate_closing_exposure=str(actual) if actual is not None else None,
            reference_closing_exposure=str(expected) if expected is not None else None,
            difference=difference, evidence_ref=baseline[1] if baseline else None,
            matched=code is None,
        ))

    if preview.blocked_accounts > 0 and not preview.exceptions:
        raise CoverageError("BLOCKED_ACCOUNTS_UNEXPLAINED")
    return ReconciliationReview(
        source_sha256=preview.source_sha256, reference_sha256=reference_hash,
        company_code=preview.company_code, fiscal_year=preview.fiscal_year,
        account_count=preview.account_count,
        candidate_mapped_accounts=preview.candidate_mapped_accounts,
        blocked_accounts=preview.blocked_accounts,
        source_closing_exposure=preview.source_closing_exposure,
        candidate_closing_exposure=preview.candidate_closing_exposure,
        blocked_closing_exposure=preview.blocked_closing_exposure,
        notes=tuple(lines),
        findings=tuple(sorted(
            findings, key=lambda f: (
                f.account_code, f.statement, f.section,
                f.note_number, f.subnote_code, f.code,
            )
        )),
        matched_for_analyst_review=not findings and preview.blocked_accounts == 0
        and bool(lines),
    )
