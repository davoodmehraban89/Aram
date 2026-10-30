# Gate 3 mapping preview — test-first execution record

**Task:** [Issue #49](https://github.com/davoodmehraban89/Aram/issues/49), first safe slice. **Branch:** `codex/aram-gate3-mapping-change-preview-20261030`, stacked on Draft PR #26 `185e47f031902a8918c93c8dbb420122e7408403`, [Draft PR #50](https://github.com/davoodmehraban89/Aram/pull/50).

## Checked evidence

1. [x] Verified accepted `source-data-cleanup` at `7dc864fd032f0c4ae4d650d89304a01286a6d914`, Draft parent #26 exact SHA; created dedicated child branch, no merge.
2. [x] Test-only commit `5190535bf2e735f741bc65b61bb2ae8492cd1c61`: [RED GitHub CI 41070855173](https://github.com/davoodmehraban89/Aram/actions/runs/41070855173), **2 expected behavior failures and 88 passes, 1 warning**; both failures demonstrated acceptance of an obsolete same-year NoteDefinition target on initial save and idempotent replay.
3. [x] Fix commit `0d7f2cbad255b44eccd326c9255b9787c65f4385`: current-note check in MappingRule service before idempotent replay.
4. [x] Add new `mapping_change_preview.py`, read-only old/new snapshot, nonnegative base-version precondition, latest note/account checks, stable unsigned digest and verifier; synthetic tests in `test_mapping_change_preview.py`, including stale/forged/pending cases.
5. [x] Combined code/test head `494af5d0f8442d193591542e1076727f892ebc87`: [GREEN CI 41071138346](https://github.com/davoodmehraban89/Aram/actions/runs/41071138346), **117 passed, 1 warning**. Migration and compile steps need explicit verification in final-head run before reporting success.
6. [ ] Re-fetch exact final head after spec, plan, append-only project log and handoff, compare complete changed path inventory and CI status. Final-head test evidence is authoritative; code-only tests cannot certify later edits.
7. [ ] Separate C1 technical/security, C2 qualified accounting and C3 release/acceptance controls from distinct non-author identities; **BLOCKED by Issue #39**. Parent #26 must be accepted before child; rebase to then-current accepted SHA, rerun CI, and review again.
8. [ ] Deliver the *actual* authenticated review and approval workflow separately: distinct reviewer permissions, Draft→Reviewed→Approved, version CAS inside provider DB transaction, persisted audit and rollback, note/subnote and source ledger reconciliation. Preview SHA alone cannot authorize saving or imply approval.

## Exact scope

- `backend/src/aram_backend/mapping_service.py`: current target version guard only.
- `backend/tests/test_mapping_service.py`: negative/valid regression.
- `backend/src/aram_backend/mapping_change_preview.py`: new read-only preparation module.
- `backend/tests/test_mapping_change_preview.py`: synthetic tests.
- This spec and plan, append-only `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`.

No schema migrations, dependencies, workflows, customer or canonical financial XLSX/PDF, `data/`, production DB, API credentials, binary or Windows release. **Do not merge** until independently accepted.
