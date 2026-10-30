# Gate 3 mapping batch freshness — implementation and verification plan

**Issue:** [#49](https://github.com/davoodmehraban89/Aram/issues/49). Child [Draft PR #52](https://github.com/davoodmehraban89/Aram/pull/52) of unmerged [Draft #51](https://github.com/davoodmehraban89/Aram/pull/51) at exact parent `d022ac48e78d06eb3c17ec820435ccbaac7a6a9c`; parent stack #50→#26 unmerged. Accepted baseline `7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

## What was done

1. [x] Verified remote parent #51/base #50 and exact accepted SHA before creating new dedicated child branch.
2. [x] Added synthetic regression tests **before production changes** at `84318eff89246fa5557275d17a6a4233786c6bd1`: full-batch recheck for new rules; version drift, external SQL writer, year approval, changed note version, changed account version on an *unchanged* row; forged input/report/status/fingerprint/year; invalid or all-noop rejection; no pending company autoflush or rule writes; invalid type.
3. [x] [RED GitHub CI 41083365885](https://github.com/davoodmehraban89/Aram/actions/runs/41083365885) failed at collection with explicit missing `verify_mapping_batch_current` import. This is a test-first missing-feature proof, **not** an adversarial behavioral test failure.
4. [x] Implemented read-only `allow_unchanged` evidence mode while preserving the single-row no-op rejection default. Batch previews now hold original `source_rows` and full catalog/version snapshots for unchanged rows too; `verify_mapping_batch_current` re-runs all submitted rows, checks ready status and refuses any changed old/new/identity/hash evidence.
5. [x] Test assertions updated to explicitly require complete unchanged-row evidence. **Initial GREEN code/test SHA `70760f33026c7cb7f2ad6ac6be164de708f93d41`**: [GitHub CI 41083623835](https://github.com/davoodmehraban89/Aram/actions/runs/41083623835) **159 passed, one warning**, Alembic upgrade/downgrade and compileall successful.
6. [ ] Re-run full backend CI on the **exact final documentation HEAD** once spec, plan, append-only project log and latest handoff are committed. Verify exact changed-file allowlist, review status and accepted base unchanged.
7. [ ] Obtain three truly independent non-author reviewer C1 technical, C2 finance, C3 release signoffs and parent acceptance before any merge. Review fully integrated DB-provider concurrency protections separately.

## Scope / allowlist

- Modify `backend/src/aram_backend/mapping_batch_review.py`.
- Modify `backend/src/aram_backend/mapping_change_preview.py`.
- Modify `backend/tests/test_mapping_batch_review.py`.
- Add this focused spec and plan in `docs/superpowers`.
- Append only `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`.

No financial source XLSX/PDF, `data/`, production database, real user account, schema/migration, dependencies, workflows, binaries, tags or releases touched.

## Unfinished, not optional

This PR is **NOT** an authenticated/persisted Draft→Reviewed→Approved service, not an audit trail, not a signature/permission model, and not a transactionally safe apply function. Revalidating a preview is a read-only check with time-of-check/time-of-use risk. Existing direct mapping Excel imports and service writes remain unaffected. Issues #49/#39/#43 stay OPEN; Gate 3 is **not** formally accepted. No reviewer identities or approvals may be invented.

Rollback: close unmerged Draft; if ever merged under explicit independently verified acceptance, create and review a revert PR.
