# Gate 3 signed fiscal-year access — execution plan

**Candidate [Draft PR #56](https://github.com/davoodmehraban89/Aram/pull/56)**, exact unmerged parent [#55](https://github.com/davoodmehraban89/Aram/pull/55) at `8d82f1e7be9653bac467101234a62029bdfa3178`, original accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged. Issue #49.

1. [x] Checked actual GitHub source and parent Draft status. PR #55 checks signed identity and role, but has no per-company or per-fiscal-year grant. New branch is child of exact parent SHA, without unreviewed merges.
2. [x] Added test-first scenarios at `463b340d9bb5a88837439620e8608bcce98e770e`. [RED CI 41110810775](https://github.com/davoodmehraban89/Aram/actions/runs/41110810775): **28 expected failures and 231 passes**, including absent year-access endpoint, malformed signed scopes wrongly accepted and missing authorization module. These are concrete missing-behavior tests.
3. [x] Updated `authenticated_identity.py` with strictly validated signed `aram_scopes` and frozen `SignedYearScope`; absent scopes authenticate but cannot authorize a year. New `mapping_year_authorization.py` intersects signed scope/role with current Company/FiscalYear in SQLAlchemy session and Draft-only status; no-autoflush and populate_existing refresh. New read-only `GET /api/v1/auth/year-access/{year_id}` wires verified principal dependency, no finance write action. Initial [CI 41110973867](https://github.com/davoodmehraban89/Aram/actions/runs/41110973867) **2 fails, 257 passes**: tests expected HTTP 403 for structurally mismatched signed role, but correct security semantics are **401 invalid token**, not 403 valid-token-forbidden.
4. [x] Corrected 2 test expectations and added direct cross-role access denial test at `59cb141cad81add6523f4fea7a127c8180d080e5`. Note 401 for invalid, role-mismatched signed claims; 403 for a genuine signed role when company/year permission is absent. Re-run exact SHA CI.
5. [ ] Run final tests and add focused spec (already created)/plan, append-only logs/handoff; then **CI on exact last documentation SHA**. Check changed-file allowlist, patch sanity, no reviewer count, unchanged accepted branch. Do not claim status from earlier run on later SHA.
6. [ ] Independent C1 technical/security, C2 accounting source hierarchy, C3 release/DB-provider review, full upstream acceptance/rebase. No real reviewers have signed; Issue #39 OPEN. IdP and actual grant provisioning, actor persistence, dual control, signed decision audit, CAS apply, Excel importer containment, fiscal data reconciliation and production migration remain Issue #49/#43. No actual enterprise identity provider configured.

## Exact changed-file allowlist

- `backend/src/aram_backend/authenticated_identity.py` (verify optional, signed exact company/year/role grants)
- NEW `backend/src/aram_backend/mapping_year_authorization.py` (DB year + company check)
- `backend/src/aram_backend/main.py` (read-only scoped API)
- `backend/tests/test_authenticated_identity.py` (synthetic signing + SQL negative paths)
- New focused spec and plan under `docs/superpowers/`
- Append-only `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`

Do not touch external/accounting data, canonical XLSX/PDF, `data/`, production database, migrations, workflow, dependencies, credentials, releases or accepted branch.

**Rollback:** close this unmerged Draft; if explicitly accepted in future, independent reviewed revert. A successful read-only year permission preflight is not authenticated reviewer decision, transaction lock, audit signature or financial data permission.
