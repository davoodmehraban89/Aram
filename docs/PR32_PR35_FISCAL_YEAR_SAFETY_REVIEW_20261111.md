# Fiscal-Year Ownership Safety Review — PR #32 / PR #35

**Review date:** 2026-11-11  
**Status:** TESTED ORM CANDIDATE — INDEPENDENT ACCEPTANCE BLOCKED  
**Accepted baseline:** `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`

## 1. Executive decision

PR #32 and its child PR #35 contain meaningful and tested ORM-level protection for fiscal-year ownership and cross-year note references. PR #35 closes two gaps explicitly left open by PR #32: same-flush Draft-to-Approved/Locked transitions with related mutations, and moves of NoteDefinition / FinancialStatement parents that would invalidate clean, unchanged dependent rows.

This is a strong application-layer control, but it is **not a complete production integrity boundary**. Both PR descriptions explicitly exclude raw/bulk SQL and concurrent-write enforcement. Neither PR has a submitted GitHub review. The candidate must remain Draft / unmerged until independent acceptance and the residual database/concurrency boundary is addressed or formally accepted for the exact V1 deployment model.

## 2. Exact candidate lineage and CI

| Item | PR #32 | PR #35 |
|---|---|---|
| Purpose | Persisted fiscal-year ownership and note isolation | Same-flush and clean-reference gaps |
| Head branch | `codex/v1-year-isolation-followup-20261023` | `codex/aram-same-flush-fiscal-lock-20261030` |
| Final head | `28d1c57882ec20fc17c2c133bbe62ff56e12973f` | `e09aa43d22eb56eca4ceb6c41519abe1c6f571f8` |
| Base | `source-data-cleanup` | PR #32 head |
| Tests reported | 110 passed | 132 passed, 1 warning |
| Exact-head GitHub Actions | [39959793328](https://github.com/davoodmehraban89/Aram/actions/runs/39959793328) | [41062134617](https://github.com/davoodmehraban89/Aram/actions/runs/41062134617) |
| Review submissions | 0 | 0 |
| State | Draft / open / unmerged | Draft / open / unmerged |

PR #35 is a child of PR #32. Do not merge both as independent roots or cherry-pick PR #35 without its parent changes. Experimental PR #41 was closed without merge and is superseded by the consolidated PR #35 candidate.

## 3. What is implemented

### PR #32

- Reads persisted original ownership before flush, including expired attributes.
- Resolves pending relationship objects, changed foreign keys, cached references and pending explicit-ID parents.
- Rejects mutations of records belonging to Approved / Locked fiscal years.
- Rejects invalid fiscal-year status transitions and identity changes after protection.
- Checks MappingRule and StatementLine target-note fiscal-year consistency.
- Adds 43 regression / valid-path cases; final CI reports 110 passed.

### PR #35 additions

- Considers pending FiscalYear approval / locking status in the same flush when evaluating protected records.
- Rejects a Company mutation in the same transaction as Draft-to-Approved / Locked transition.
- Checks persisted, clean MappingRule and StatementLine references when a NoteDefinition moves year.
- Checks clean StatementLine references when a FinancialStatement moves year.
- Preserves valid Draft moves when references are explicitly retargeted or move together.
- Adds adversarial negative, rollback and valid-path tests; final CI reports 132 passed.

## 4. Residual risks — not covered by these PRs

### 4.1 Raw SQL / bulk DML bypass

SQLAlchemy `Session.before_flush` does not intercept direct SQL, bulk update/delete statements, external database clients, migration scripts or other applications writing to the same database. The PRs explicitly exclude these paths. If the product permits direct DB access or maintenance scripts, the ORM hook alone is not sufficient.

### 4.2 Concurrent transaction race

The guard reads persisted fiscal-year status and ownership during `before_flush`, but it does not establish a database-level lock or atomic constraint tying the status check to the subsequent write. A concurrent transaction may change status or ownership after the check. The PRs explicitly make no concurrency guarantee.

### 4.3 Provider / production database boundary

The CI evidence covers the repository's configured test database and Alembic round-trip, not a live Peyvast SQL Server or another production provider. No production schema, provider-level constraint or real multi-worker deployment is verified.

### 4.4 Query scale and performance

The clean-reference guard queries dependent MappingRule and StatementLine rows when parent years move. No workload benchmark or index review is recorded for large ledgers / note catalogs. Profile the relevant foreign-key indexes and query plan before production.

### 4.5 Independent acceptance

Both PRs have zero submitted GitHub reviews. Passing CI and the author's test report are not independent approval. The author cannot self-approve financial integrity, security and operational acceptance.

## 5. Required production acceptance gates

| Gate | Required evidence | State |
|---|---|---|
| ORM invariant tests | Exact-head regression tests for original-owner, same-flush, clean-reference, rollback and valid Draft paths | PASS in candidate CI |
| Database-level integrity | Composite foreign keys / constraints or triggers that enforce same-year references and protect Approved/Locked ownership against direct SQL | NOT_IMPLEMENTED / NOT_VERIFIED |
| Concurrency | Two-session race tests for Draft->Approved vs concurrent row mutation and parent-year moves | NOT_IMPLEMENTED |
| Raw SQL / bulk DML | Adversarial direct SQL tests proving the database rejects protected writes and cross-year links | NOT_IMPLEMENTED |
| Migration | Upgrade/downgrade against empty and pre-existing synthetic data with the chosen constraints | PARTIAL; current Alembic round-trip passes but no new DB enforcement exists |
| Performance | Explain/query-plan and workload test for clean-reference scans and foreign-key indexes | NOT_VERIFIED |
| Provider compatibility | Test on the exact V1 database provider and supported deployment topology | NOT_VERIFIED |
| Independent reviews | Separate engineering, accounting-control and release/operations approvals on exact final SHA | BLOCKED |

## 6. Recommended technical direction

For a multi-user or externally accessible deployment, add a database-level enforcement layer rather than relying solely on ORM hooks:

1. For `MappingRule`, consider a composite uniqueness key on `NoteDefinition(id, year_id)` and a composite foreign key `(target_note_id, year_id)` to prevent cross-year targets.
2. For `StatementLine`, evaluate storing / constraining its owning `year_id` so both `(statement_id, year_id)` and `(target_note_id, year_id)` can be enforced, or use provider-specific triggers if denormalization is unacceptable.
3. Add database triggers / constraints or an equivalent controlled-write boundary to prevent changing company/year identity or mutating year-owned rows once the parent year is Approved / Locked.
4. Use transaction isolation / row-locking appropriate to the actual database provider and prove race behavior with two independent sessions.
5. Keep the ORM hook as an early, user-friendly validation layer; it should complement, not replace, database enforcement.

These are design recommendations, not an approved schema change. The exact mechanism depends on the selected V1 database and migration strategy.

## 7. Integration recommendation

- Keep PR #32 and #35 as one dependency family.
- Treat PR #35 as the more complete ORM candidate, but do not call it production-ready.
- Do not merge PR #32 alone and then forget the PR #35 same-flush / clean-reference follow-up.
- Do not merge PR #35 into the accepted baseline until the database/concurrency decision is explicit, independent reviews are submitted, and final CI runs on the rebased exact head.
- Preserve PR #41 as closed-without-merge historical RED/GREEN evidence; do not resurrect it.

**Decision:** retain the family as a P0 safety candidate. Current evidence proves tested ORM-level behavior only; production fiscal-year integrity remains NO-GO until the residual gates are passed or the deployment threat model is explicitly narrowed and approved.
