# ARAM — Note exposure reconciliation gate (UNRELEASED)

## Purpose and approved boundaries

This focused component compares **workbook-derived candidate account closing exposures** against separately entered per-note **reference closing exposures**. It does not decide whether the signs, account nature, accruals, cash flows, equity movements, or statutory financial statements are correct.

Upstream: Draft PR #60 read-only coverage preview (`coverage_preview.py`). This change must remain a Draft child until its parent, security controls and actual accounting owner decisions are accepted.

## API

```python
from aram_backend.reconciliation_review import NoteReference, reconcile_workbook_for_review

result = reconcile_workbook_for_review(
    workbook_bytes,
    company_code="001",
    fiscal_year=1404,
    references=[
        NoteReference(
            statement="BS",
            section="Assets",
            note_number="N01",
            subnote_code="",
            expected_closing_exposure="126.00",
            evidence_ref="SYNTHETIC-CONTROL-TOTAL-01",
        )
    ],
)
assert not result.approved
assert not result.releasable
```

References and workbooks **must** be synthetic or authorized. The reference amount and evidence identifier are *untrusted assertions*, not independently verified source facts. Never copy production data into tests or repository logs.

## Fail-closed rules

- Explicit company/year only; no cross-year fallback.
- Pilot workbook must pass upstream preflight, including detection of hidden and merged data.
- Missing/ambiguous/unapproved Mapping accounts remain blocking exceptions.
- Every candidate note requires one unique explicit reference; an extra or duplicate reference blocks or rejects the comparison.
- Exact Decimal comparisons with no silent tolerance, rounding or invented sign rules; amounts must be finite bounded text values (not floats).
- Source workbook SHA-256 and canonical independent reference SHA-256 are attached to every result. Changing source or control reference changes provenance.
- Output is structured in-memory data only. No database writes, ledger mutation, report export, approval action, PDF or EXE.
- Even an exact match means only `matched_for_analyst_review=True`, while `financial_statement=False`, `trusted_approvals=False`, `approved=False`, and `releasable=False`.

## Scope explicitly NOT implemented

Statement generation and financial-sign policy, authenticated reviewer identities, documented year/company approval, independently signed audit decisions, atomic Mapping application, database locking/CAS, cash flow movement reconciliation, official note disclosures, PDF/XLSX printing and release packaging are out of scope.

## Verification

Run `cd backend && pytest tests/test_reconciliation_review.py` and then full Backend CI (all tests, SQLite migration round trip, bytecode compilation) on the exact last commit. Review against the accepted parent, keep accounting sources untouched, and obtain real external C1/C2/C3 reviews before any merge. Use the linked PR's CI instead of agent-written counts for acceptance.