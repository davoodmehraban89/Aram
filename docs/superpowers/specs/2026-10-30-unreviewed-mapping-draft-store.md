# ARAM Gate 3 — durable UNREVIEWED Mapping draft storage

**Status:** PROPOSED, unmerged [Draft PR #53](https://github.com/davoodmehraban89/Aram/pull/53), child of unmerged Draft #52 at exact `1063431b08a9e03e022aa9b8e6c5ed90bfb05395`. Upstream #51→#50→#26 also unmerged. Accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

## Financial approval threat boundary

ARAM has **no trusted authenticated user/approver boundary**, real reviewer roster, role separation, durable approved decisions, or transactionally safe MappingRule apply path. Mere client-provided names, checksums or role labels MUST NOT represent financial approval. Therefore this PR deliberately creates **only UNREVIEWED, inactive draft evidence**. It is permitted to stage untrusted proposals for later human review, but the new service exposes **no approve, review-sign, reject-as-human, apply, activate or update-MappingRule operation**.

The database column `state` is non-null `Unreviewed` with a DB CHECK constraint allowing only this value. Both a service method and a raw SQL `state=Approved` attempt are absent/rejected; this is intentionally not a full state machine. The proposal is passive input, NOT a source of truth about financially approved mapping.

## Schema and migration safety

- New SQLAlchemy Core table `mapping_review_drafts` lives on its **own MetaData**, not `Base.metadata`. This is critical: current initial migration `20260820_01` runs `Base.metadata.create_all`; adding the new table to that Base would prematurely create it during initial migration and break a subsequent `op.create_table`.
- New additive, explicit Alembic migration `20261030_02`, `down_revision=20260820_01`, adds: integer primary key; required FK `year_id` referencing fiscal years `RESTRICT`; `request_key` max 64 characters; JSON payload of original batch evidence; SHA-256 checksum; strictly checked `state`; creation timestamp; and unique `(year_id, request_key)` for DB-backed idempotency. Downgrade drops only this table. The migration is a **candidate**, not permission to execute DDL against a real database. Its revision sequence must be reconciled with unmerged PR #25 and later migration changes before merge.
- Synthetic test suite creates/drops the isolated table separately so it never leaves a FK pointing at `fiscal_years` during `Base.metadata.drop_all`. CI's disposable Alembic upgrade/downgrade tests the complete chain.

## Safe store/read/recheck contract

- `save_unreviewed_batch(session, snapshot, request_key)`: only accepts an actual `MappingBatchPreview` with `ready_for_review=True`, trimmed bounded request key (rejects control/format characters), clean related ORM Session and current full-batch revalidation. Stores *exact serialized immutable submitted row/report evidence* and content hash, **without applying any MappingRule**. Caller controls commit/rollback.
- If the same year/key is retried with the **identical** payload/hash, returns the original row; if its payload differs, rejects conflict rather than overwriting. Database unique constraint also rejects competing inserts, but an external concurrent collision may yield `IntegrityError`: caller must roll back, never silently claim success.
- `get_unreviewed_batch(session, draft_id, year_id)` is a scoped **passive metadata read**, not a user-facing authenticated endpoint. Wrong fiscal year or invalid identifiers fail. Reject a corrupted stored payload/hash or impermissible state. Since the checksum is **unkeyed SHA-256**, it does NOT defend against a malicious DB writer able to replace both payload and hash, and is NOT an audit signature.
- `validate_unreviewed_batch_current` rehydrates the original typed source rows, recomputes the read-only full batch snapshot against current year, note, account, mapping rules and compares the original stored report. Rejects any drift. This only checks at time of read; never writes, approves or locks data.
- A stale saved proposal remains Unreviewed for subsequent diagnostic inspection. No silent refresh, deletion of source rules, fallback classification or automatic proposal application.
- No actor/approver ID, no reviewer role, no authenticated API endpoint, no audit event and no integration of old direct Excel import path are introduced.

## Tests and known limits

Synthetic proof covers persistence after commit, caller rollback, no MappingRule writes, scoped idempotency and conflicting reuse, current/stale source note/year/rule state, wrong fiscal year, invalid request keys, conflict rejection, forged preview, DB CHECK rejecting Approved, pending Session ORM writes, tampered stored JSON detection, SQL UNIQUE collision and independent metadata/FK. Full test suite, disposable upgrade/downgrade and compileall required on exact final SHA.

**NOT DONE:** authenticated Draft→Reviewed→Approved/rejection lifecycle, immutable decision audit, real reviewed proposal/apply transaction, database CAS and concurrency isolation, dual review identities, active-rule version semantics, full hierarchy and subnotes, canonical ledger reconciliation, Excel importer bypass closure, UI/Windows deployment. All remain [Issue #49](https://github.com/davoodmehraban89/Aram/issues/49), [#39](https://github.com/davoodmehraban89/Aram/issues/39), [#43](https://github.com/davoodmehraban89/Aram/issues/43). Do not merge until real independent C1/C2/C3 acceptance, upstream PR acceptance and migration reconciliation.

No canonical XLSX/PDF, `data/`, actual client SQL system or production database touched. Rollback before merge: close Draft; after authorized merge: reviewed revert (migration downgrade deletes stored unreviewed drafts, so a real upgrade needs a separately approved backup/recovery plan).
