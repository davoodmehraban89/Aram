# ARAM Gate 3 — read-only Mapping coverage preview (candidate)

**Status:** development-only, not accepted, not a financial report and not a reviewer approval.

This isolated candidate is intentionally based on accepted `source-data-cleanup` rather than the unmerged Gate 3 parent branches. It adds a narrow, independent analysis of an existing Pilot XLSX byte snapshot. It does not alter source documents, write databases, execute Mapping changes, or create any official statements or export files.

## Contract

Call `preview_mapping_coverage(workbook_bytes, company_code="001", fiscal_year=1404)` from `aram_backend.coverage_preview`.

The input must pass `preflight_pilot_workbook`. It must contain an explicit company/fiscal-year record and at least one account. The result includes the source SHA-256, full account lineage (Excel row/source row), candidate note exposure, ambiguous/unmapped/unapproved exceptions, and source/covered/blocked closing exposures.

Only an account with **exactly one** Mapping row marked `Approved` and `Valid` **in the workbook** is included in the *candidate* group. These are untrusted workbook claims, **not** authorization. Duplicated mappings are excluded regardless of their stated approval status. Missing mappings are excluded. A closing balance is **not** a statement line, cash flow, income, or auditor-approved figure.

Each output has `kind="UNAPPROVED_MAPPING_COVERAGE_PREVIEW"`, `financial_statement=false`, `trusted_approvals=false`, `releasable=false`. Do not remove these protections or expose an approval/export UI until authenticated independent reviews, source-to-statement semantics and reconciliation are accepted.

Input size limit: 20 MiB; archive has at most 500 entries and 128 MiB declared expanded size. The tool rejects hidden input sheets/rows/columns and merged input ranges in the four authoritative sheets and forbids a cross-company or cross-year fallback. It uses Decimal arithmetic and deterministic ordering; it does not auto-map based on descriptions.

## Verification

Synthetic tests in `backend/tests/test_coverage_preview.py` cover accepted unique Mapping, unmapped and ambiguous accounts, workbook-marked Draft/Approved states, source preservation, hidden/merged inputs, invalid/oversized workbooks, absent company/year scopes and JSON-safe results.

Run `cd backend && python -m pytest tests/test_coverage_preview.py -q` and then full backend CI with migration round-trip and compilation. No live customer data is required or permitted in tests.

## Remaining acceptance dependencies

- Real signed employee identity and scoped roles, reviewer segregation of duties and persisted decisions;
- Database-enforced company/year immutability, concurrency/CAS and auditable Mapping application;
- Financial owner confirmation of note/sub-note, account nature and debit/credit signs;
- Reconciliation of historical financial figures and signed output/print;
- Real GUI, clean Windows installation, end-to-end testing and independent C1/C2/C3 review.

These are not implemented by this preview.
