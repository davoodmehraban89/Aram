# Gate 3 — SQLite system-only, insert-only evidence for Unreviewed draft staging

**Proposed, unmerged [Draft PR #54](https://github.com/davoodmehraban89/Aram/pull/54)**. Exact parent: unmerged [Draft PR #53](https://github.com/davoodmehraban89/Aram/pull/53) SHA `3f089d03ca134cd73082dd0db8ba2461e1e6bc7c`. That PR depends on Draft #52→#51→#50→#26; accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

## Objective and trust boundaries

There is no authenticated finance approver, identity service, or active Mapping approval workflow. A persistent Unreviewed Mapping draft in PR #53 contained a payload hash but no separate database event that could prove even a **system-staging** operation was recorded. This PR adds one passive `DraftStaged` **system** event per newly stored draft, in the exact same SQL transaction as the draft insert. **It is NOT a human decision, reviewer audit trail, proof of actor identity, release approval, source signature, independent witness, or append-only financial transaction journal.**

## Schema and integrity contract

- A new `mapping_draft_events` SQLAlchemy Core Table lives on the existing **independent** proposal MetaData, not on the baseline `Base.metadata` that is created by the initial metadata-driven migration. Each event has `draft_id` with restrictive FK to `mapping_review_drafts`, year ID, CHECK-limited `DraftStaged` event_type, original payload hash, deterministic event hash, creation timestamp, UNIQUE draft ID, and a primary key.
- New additive migration `20261030_03`, after `20261030_02`, defines explicit create-table operations and **SQLite-specific BEFORE UPDATE and BEFORE DELETE triggers** that reject direct update/deletion with an integrity error. SQLite with foreign-key enforcement blocks deleting a parent draft while its protected event exists. Those triggers and corresponding service-level checks are synthetic test targets.
- **Provider fail closed:** migration checks the actual dialect and raises before any table DDL unless it is SQLite. A SQL Server / PostgreSQL equivalent requires its own approved migration, event privileges and immutability guarantees. This PR does not claim any production provider is configured or endorsed.
- The event's deterministic SHA-256 digest covers its draft ID, year ID, request key, draft payload hash and event type. The read path checks event consistency, and the staging service inserts event and draft in the same caller-controlled transaction. A caller rollback discards both, and exact idempotent retries do **not** append another event.
- This digest is **unkeyed**, not signed, not chained to an external secure anchor, and cannot resist a privileged administrator who can drop DB triggers or replace the DB file. A malicious actor who can directly insert draft/event pairs might fabricate a whole event even with the update/delete triggers. **Do not describe this as immutable against DB administrators or as a legally compliant financial audit trail.**
- The event has no actor, approver, reviewer or authenticated user ID; absence of those fields is intentional, not missing test data. A successful event verification does not unlock application of a MappingRule.

## Acceptance and test plan

- Test-first missing module RED CI, then successful synthetic two-table transactional insert/read, rollback, same-request idempotency, SQLite direct UPDATE/DELETE denial, DB UNIQUE draft-event constraint, tampering detection when a malicious writer recomputes the draft hash, denial of cross-year event read, no approvals or MappingRule mutations.
- Full backend pytest and *disposable* Alembic upgrade all `20260820_01 -> 20261030_02 -> 20261030_03`, downgrade reverse and compileall on **final exact PR SHA**, not an earlier intermediate commit.
- Review remote changed-file allowlist and branch parent SHA, no production/customer DB, canonical XLSX/PDF or `data/`, existing migration rewrite, workflows, dependencies, releases, secrets or credentials changed.

## Still blocked

The full authenticated Draft→Reviewed→Approved workflow, separation of author/approver, immutable **financial decision** audit with signed identity, atomic compare-and-set application, provider concurrency, rejected/rework state, recovery, traceable note/subnote source mapping and real fiscal-year financial reconciliation remain in [Issue #49](https://github.com/davoodmehraban89/Aram/issues/49) and [#43](https://github.com/davoodmehraban89/Aram/issues/43). Three real non-author C1/C2/C3 reviewers/branch controls remain [#39](https://github.com/davoodmehraban89/Aram/issues/39). Baseline migration is being separately redesigned under unmerged PR #25; revision reconciliation is mandatory before merge.

No approval can be recorded by this module; parent Draft PRs and this Draft cannot be merged or released without genuine independent acceptance. A migration downgrade destroys event evidence: use only on disposable CI database until an authorized backup/retention and recovery policy is approved.


## Fail-closed upgrade from earlier candidate migration

Before creating the new audit table or triggers, `20261030_03.upgrade` checks the existing `mapping_review_drafts` table for even one row. If any draft already exists, the upgrade **raises RuntimeError before executing any DDL**. Earlier `20261030_02` drafts lack independently recorded `DraftStaged` events; fabricating them retrospectively would misstate provenance. An owner-approved migration strategy must distinguish legacy unwitnessed drafts from newly witnessed drafts and include retention/backups before any live upgrade. The synthetic adversarial test intentionally adds a draft and confirms migration refuses the upgrade, including a monkeypatched DDL method that must never run. This blocks direct in-place upgrades of nonempty candidate databases by design, not an installation defect to bypass.
