# Fiscal-year ownership and note-reference safety

## Intent

Prevent persisted accounting records from leaving an Approved or Locked fiscal year, and enforce statement-to-note year isolation for both ORM relationships and direct foreign-key assignments. These are reproducible gaps in accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`.

The owner authorized continuing the proposed safety-first work before database-connector and mapping expansion. This focused change implements only that safety prerequisite.

## Behavior

- Validate both persisted original ownership and proposed ownership before flushing modifications or deletions of year-owned records, note rows, and statement lines.
- Protect Approved and Locked years; preserve ordinary Draft-year edits and valid same-year references.
- Resolve changed foreign keys without trusting a cached old relationship. Resolve relationship assignments before SQLAlchemy synchronizes their foreign keys.
- Reject a statement line referencing a note from another fiscal year, including cross-company years. Permit a statement line with no target note.
- Reject conflicting simultaneous relationship/foreign-key assignments instead of validating one identity and persisting another.
- A rejected transaction must leave the stored original row and relationships unchanged after rollback and reload.

## Approach

Use the existing `Session.before_flush` invariant hook, query original ownership by persisted identity, and resolve proposed relationships from attribute change history. Checking only current `year_id` misses removal from a protected year. Database triggers or composite-key schema changes would require a separate migration and broader provider-specific review; they are not introduced here.

## Constraints

- Exact base: `7dc864fd032f0c4ae4d650d89304a01286a6d914`; branch `source-data-cleanup`.
- No dependency, workflow, migration, canonical XLSX/PDF, `data/`, persisted database, financial-source value, binary or release change.
- No recovery from closed PR #7 and no acceptance or merge of other draft PRs.
- Application scope: `backend/src/aram_backend/models.py` and `backend/tests/test_models.py`.
- Control records: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, and this design/plan pair.
- No raw SQL/bulk-write authorization API is added. The hook's existing ORM boundary remains explicit.

## Acceptance

Regressions fail on the accepted base and pass with the fix; all existing tests pass; isolated SQLite Alembic upgrade/downgrade and compilation succeed. An independent reviewer inspects the complete remote candidate. The implementation is published as a focused Draft PR and is not self-merged.
