# Gate 3 PR #82 — Three-perspective self-audit (not independent sign-off)

Reviewed initial head: d75cbbbc16068acc3735e8d1e8204ee57d266318.
Base: source-data-cleanup at 7dc864fd032f0c4ae4d650d89304a01286a6d914.
Changed files: backend/src/aram_backend/mapping_workflow.py,
backend/src/aram_backend/mapping_store.py,
backend/tests/test_mapping_workflow.py,
backend/tests/test_mapping_store.py.

## Pass 1 — Functional QA
Checked scoped import, explicit lifecycle, review evidence, workbook preflight,
round-trip and original-sheet preservation, unknown-account queue, carry-forward.
Finding: approved mappings could not round-trip; missing review date.
Fix: store review_date in decisions, populate on transition, import/export with
Valid status and mandatory evidence. Added approved round-trip test.
Finding: exporting selected scope removed foreign-scope mappings.
Fix: preserve foreign-scope rows during export.

## Pass 2 — Architecture and security
Checked parameterized SQL, transaction boundaries, optimistic revision,
append-only audit, company/year isolation, workbook formula/code validation.
Finding: maker could review their own mapping.
Fix: forbid same actor for Draft author and Reviewed transition.
Finding: WAL mode configured on every connection.
Fix: initialize WAL once.
Residual risk: store relies on application-level audit integrity; privileged
database edits can rewrite both state and audit. No cryptographic tamper-evidence.
Residual risk: no authorization/identity provider; actor names are caller-supplied.

## Pass 3 — Adversarial / chaos
Exercised stale concurrent writers, invalid transitions, cross-company/year
inputs, duplicate IDs, missing review evidence, invalid XLSX, re-opened
persistent state and audit prefix manipulation. Automated tests pass locally.
Residual risk: multi-process stress, power-loss recovery, large-file resource
limits and adversarial malicious workbook security require separate acceptance.

## Evidence and decision
Backend CI at d75cbbb: https://github.com/davoodmehraban89/Aram/actions/runs/41334206919 — success.
Local full backend suite: 80 tests passed before latest review fixes; rerun
performed after fixes with exit code 0 (82 tests).
No binary, database, financial source or canonical template changed.
Rollback: revert the focused feature branch commits; no migrations applied to
production data. This PR remains Draft.

**Decision: CHANGES REQUESTED / NOT ACCEPTED.**
These are three sequential self-audit perspectives, not three independent
human or separately instantiated reviewer identities. External independent
review and updated final-head CI are required before formal acceptance.


## Package 3 review extension — 2026-11-01
- Exact approved base checked locally: source-data-cleanup at 7dc864fd032f0c4ae4d650d89304a01286a6d914.
- Prior reviewed head: ff6843cd0a1544a3a5355a8d555d4d692b8716fc.
- Working tree initially clean; feature branch isolated.
- Reviewer 1 (functional self-audit): found that maker could approve after another user reviewed; fixed maker/approver separation and added regression test.
- Reviewer 2 (security/architecture self-audit): found state could be persisted with a forged final status/version inconsistent with audit. Added audit-transition/version-chain and state consistency checks plus regression test.
- Reviewer 3 (adversarial self-audit): exercised invalid state and forged audit, rollback, stale concurrent writers, workbook roundtrip and foreign scope. New tests cover forged status and event version.
- These are three sequential self-audits by the implementation assistant, **not independent reviewers**. GitHub review list was empty at start.
- Known unresolved risks: no trusted identity provider / role authorization; SQLite audit is not cryptographically tamper-evident against privileged DB writers; no production recovery drill; no independent reviewer sign-off; Gate 3 financial mapping ambiguity remains material. These require separate controls and block acceptance.
- No merge, release or production financial data modification is authorized.
- Final CI and full local test evidence must be checked against the new head before any acceptance decision.
- Decision: CHANGES REQUESTED; PR remains Draft pending independent review and closure of material controls.

- Additional architecture finding: sqlite3.Connection context managers do not close connections. Fixed init/load/audit_log paths using contextlib.closing to prevent leaked file descriptors and Windows DB locks.
