# ARAM Gate 3 — full-batch Mapping preview staleness verification

**Status:** PROPOSED, [Draft PR #52](https://github.com/davoodmehraban89/Aram/pull/52), unmerged. Exact parent: [Draft PR #51](https://github.com/davoodmehraban89/Aram/pull/51) SHA `d022ac48e78d06eb3c17ec820435ccbaac7a6a9c`; upstream #50 and #26 are also unmerged. Accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` must remain unchanged.

## Why a single-row verifier was inadequate

The earlier bulk review module provided a checksum and classified proposals but **did not retain the original complete typed source-row set** or provide a whole-batch recheck. A changed row, changed fiscal-year lifecycle, account-version supersession or new MappingRule could invalidate an earlier review. Particularly, `unchanged` rows were represented without their underlying account/note/rule catalog snapshot; an unchanged item later becoming stale could be invisible while other items were still ready.

A digest alone is neither evidence of persistence nor a digital signature; it is trivial for a caller to recompute. The correct first step is a strict read-only re-evaluation of *all* source rows against current persisted facts, followed by byte-exact-equivalent immutable value comparison. This protects against changes **visible to a new DB read at check time only**.

## Contract

- The immutable `MappingBatchPreview` carries the exact typed `source_rows` tuple, complete status rows (including old/new per-rule snapshots), and existing unsigned deterministic report checksum.
- `preview_mapping_change(..., allow_unchanged=True)` supports a strictly read-only complete snapshot for an unchanged mapping, including existing MappingRule data, account version ID/version, target note version and company/year. Default behavior **unchanged**: individual no-op still raises typed `MappingNoChange`; a no-op is not a reviewable delta.
- `preview_mapping_batch` returns `unchanged` with full unmodified source catalog evidence; `new` and `changed` retain their previous semantics. Status-only classification is NOT proof of authorization or human acceptance.
- `verify_mapping_batch_current` accepts only an actual `MappingBatchPreview` with `ready_for_review=True`. Invalid/conflict-only or all-noop batches are not review-ready and are rejected. It reruns `preview_mapping_batch` from the **exact captured original typed source rows** against database state using no-autoflush, independently refreshes ORM-loaded facts, and rejects ANY inequality with the original immutable evidence and checksum. It never silently substitutes a regenerated snapshot for approval.
- This is read-only: it does not call `save_mapping_rule`, does not flush pending mapping edits, does not mutate an audit table, does not commit, and does not apply or approve a single account mapping.
- A nested source row cannot be silently altered (all row evidence is frozen dataclasses); changing a source-row tuple, row result, status, checksum, company/year or rule/note version causes stale/invalid rejection.

## Tests

Synthetic positive: fresh new two-rule batch verified, no MappingRule mutation, pending unrelated Company not autoflushed. Synthetic negative: persisted newer MappingRule, independent same-version rule content update, independently approved FiscalYear, newer NoteDefinition, newer AccountVersion *on an unchanged row*, forged original source tuple, changed row status, changed checksum, altered year, invalid/conflicting proposal, all-noop proposal, invalid object. Distinct SQLAlchemy Session updates are covered on the test SQLite engine; these tests are **not** direct proof for SQL Server or other provider isolation.

## Explicit remaining controls

- **Critical:** A successful verification is only a time-of-check result. An authorized transactional apply service must recheck inside the *same correctly isolated write transaction*, use database compare-and-set/locking, prevent replay, and record an immutable audit with authenticated actor/approver identities. The low-level `save_mapping_rule` and old Excel import remain possible independent write paths, so this PR does not close the authorization bypass.
- Source ledger hierarchy/predicate semantics, note/subnote, multi-target resolution and accounting classification require actual financial owner approval. Do not infer precedence.
- Actual three non-author C1/C2/C3 reviews and branch protection remain [Issue #39](https://github.com/davoodmehraban89/Aram/issues/39), the authenticated/audited workflow remains [Issue #49](https://github.com/davoodmehraban89/Aram/issues/49), database/provider concurrency remains [Issue #43](https://github.com/davoodmehraban89/Aram/issues/43).
- Canonical XLSX/PDF, financial `data/`, customer SQL, schema/migration, dependency, CI workflows, EXE/ZIP and accepted branch are immutable here. Do not self-merge or claim Gate 3 financial acceptance. Rollback before merge: close this Draft; after acceptance: separately reviewed revert.
