# Gate 3 batch Mapping preflight — implementation and handoff

**Scope:** Read-only candidate for [Issue #49](https://github.com/davoodmehraban89/Aram/issues/49), child [Draft PR #51](https://github.com/davoodmehraban89/Aram/pull/51) of **unmerged** [Draft PR #50](https://github.com/davoodmehraban89/Aram/pull/50), exact parent SHA `f79947a8624adbd8e84c3f8247ac3ca4a7bd4240`. Original accepted head `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

## Test-first evidence

1. [x] Added unit and security tests for row states, deterministic checksum, old/new diffs, explicit expected version, same-year note validity, duplicates, conflicts, no-op, company/year protection, no autoflush and **zero stored mappings** in the preview.
2. [x] [RED CI 41081238728](https://github.com/davoodmehraban89/Aram/actions/runs/41081238728) on initial tests-only SHA `cc64b3a4daec3fe793946831864bd57b8023eb38`: expected missing-module import error.
3. [x] Added `mapping_batch_review.py` plus typed `MappingNoChange` signal from existing change-preview module; [GREEN CI 41081481135](https://github.com/davoodmehraban89/Aram/actions/runs/41081481135) on `2d30a93e01b14d2cf84ff88207c8ef73642f14bd`: **138 passed, 1 warning**, Alembic upgrade/downgrade and compile success.
4. [x] Added six negative cases for Boolean/int collisions (`True == 1`) and newline/tab/NUL locator injection at test SHA `e4b2608bd827f249755a5280142fb1c12a78174c`. [RED CI 41081877772](https://github.com/davoodmehraban89/Aram/actions/runs/41081877772): **6 expected failures and 138 passes**.
5. [x] Fixed comparison to include the actual type of each component and rejected `Cc/Cf/Cs` Unicode control/format characters in source locators at SHA `c0b547983925ac912641ebd795fc0c345f01a1a7`. [GREEN CI 41082029761](https://github.com/davoodmehraban89/Aram/actions/runs/41082029761): **144 passed, 1 warning**, Alembic migration round-trip and compile success.
6. [ ] Run full backend CI on **final documentation/log/handoff SHA**, confirm exact changed-file inventory, patch sanity and reviewer state. Earlier runs only certify their own SHAs.
7. [ ] Reconcile and accept upstream PRs #26 then #50 under real independent non-author C1/C2/C3 approval (Issue #39), then restack/retest this child. No self-merge.
8. [ ] **Future separate work:** build documented Excel adapter to this canonical batch contract; authenticate users and persist proposals; explicit Reviewed→Approved with immutable audit trail, transactional compare-and-set, idempotency and rollback; verify canonical 1402–1404 ledger reconciliation and provider concurrency. This PR does **not** implement that authority or write path.

## Exact change allowlist

- NEW `backend/src/aram_backend/mapping_batch_review.py`
- NEW `backend/tests/test_mapping_batch_review.py`
- MODIFY `backend/src/aram_backend/mapping_change_preview.py` only to type valid no-op (subclass of existing error)
- NEW spec + this plan under `docs/superpowers/`
- APPEND ONLY `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`.

No canonical XLSX/PDF, `data/`, production/customer SQL, migrations, dependency lockfile, GitHub workflow, secret, binary, ZIP/EXE, release or accepted-branch writes. No authenticated reviewers/approval IDs manufactured. Rollback before merge: close Draft; after authorized merge: independently reviewed revert.
