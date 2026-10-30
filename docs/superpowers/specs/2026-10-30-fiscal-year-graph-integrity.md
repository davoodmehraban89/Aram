# Fiscal-year Unit-of-Work and Graph Integrity — 2026-10-30

- **Status:** Proposed implementation, pending independent review.
- **Authority:** [Issue #36](https://github.com/davoodmehraban89/Aram/issues/36).
- **Exact base:** unmerged [PR #32](https://github.com/davoodmehraban89/Aram/pull/32) `codex/v1-year-isolation-followup-20261023@28d1c57882ec20fc17c2c133bbe62ff56e12973f`.
- **Candidate:** [Draft PR #35](https://github.com/davoodmehraban89/Aram/pull/35), consolidated from initial separate Drafts #35 and #41; #41 is superseded by this candidate.
- **Accepted branch:** `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`, not modified.

## Purpose and threat model

Financial-year integrity is not merely a row-level constraint. SQLAlchemy's `Session.before_flush` inspects pending changes before SQL has been emitted, and persisted status may still be Draft even though the in-memory FiscalYear object is already Approved. Separately, moving a fiscal-year parent can invalidate already-persisted clean mapping/statement dependencies that are absent from the Session's dirty set.

These are reproduced defects in an **ORM application boundary**. This change does **not** claim to implement database-level invariants, row locks, concurrent-session isolation, custom permissions, PostgreSQL/SQL Server triggers, external writer restrictions, or customer data validation. Those require separate scoped designs and provider-specific evidence.

## Invariant S1 — Same-flush approval is atomic

When an existing FiscalYear transitions Draft → Approved in a Session, no creation, modification or deletion of an associated year-owned record, `NoteRow`, or `StatementLine` is permitted in that same flush. Modification of the associated Company is also forbidden. The same rules apply to Locked status.

Resolve **proposed effective status** from `Session.new | dirty | deleted` for a matching FiscalYear identity, then consult persisted status for all other years. A database query alone is inadequate before SQLAlchemy flushes the transition.

- **Reject:** Draft → Approved plus edit of AccountVersion, SourceDocument, NoteDefinition, FinancialStatement, MappingRule, NoteRow or StatementLine in one commit.
- **Reject:** Draft → Approved plus new SourceDocument, or an existing Company change in the same transaction.
- **Permit:** ordinary Draft edits committed separately before an approval-only transition, and valid Draft→Approved/Approved→Locked transitions without concurrent data mutation.
- **Rollback:** rejected transaction must persist neither the status transition nor the affected record change.

## Invariant S2 — Re-evaluate clean graph references

When a **persisted** `NoteDefinition.year_id` changes between Draft years, inspect persisted `MappingRule` and `StatementLine` rows whose target_note_id points to it, even if they are not in `Session.dirty`. Re-evaluate each dependent's effective in-session mapping year or financial-statement year against the effective target note's year.

When a **persisted** `FinancialStatement.year_id` changes between Draft years, inspect persisted linked StatementLine rows, even when unchanged; reject any non-null target note whose effective year disagrees with its financial statement's effective year.

- **Reject:** moving a Draft note while a clean mapping or note-linked statement line would remain tied to the old year, whether the years belong to the same Company or different Companies.
- **Reject:** moving a Draft statement while a clean note-linked statement line remains tied to a note in the old year.
- **Permit:** moving a previously unreferenced Draft note; moving a Draft statement whose existing lines have no target note.
- **Permit when internally consistent:** coordinated in-Session movement of a Draft note and the mapping owner, coordinated movement of a Draft note and statement parent, or an explicit reference retarget to a different note in the original Draft year.
- **Reject** any outcome still containing cross-year mapping/statement-note references. If the requested accounting operation cannot be independently reviewed and justified, prefer a **separate authorized transaction**: detach/review old references, commit, then move/rebuild the parent; do not silently carry hidden dependencies.
- **Rollback:** database reload after rejected commit shows original fiscal years and persistent references.

## Implementation boundary

Use one existing synchronous SQLAlchemy `before_flush` event. Add narrowly scoped helper(s) to inspect pending status and affected persisted references. Do **not** mutate accounting data, auto-repair links, rewrite note numbers, infer mapping decisions, or make an unauthorized mapping transfer. Parent graph checks run only when a persisted note/statement has actually changed `year_id`.

This is application-level prevention within a Session using the ORM. It does not eliminate race conditions: another Session can change the linked rows after the check without database enforcement. The target-note relations may be unindexed in the current schema; synthetic-scale performance profiling and an independently reviewed migration may be necessary before deployment.

## Acceptance tests and evidence

- RED: run newly added regressions on unchanged PR #32; demonstrate nine same-flush bypass failures and six clean-reference bypass failures (the latter reproduced after first fix; all failures must be for the intended missing ValueError).
- GREEN: full test suite verifies allowed Draft operations as well as prohibited transitions, rollback and relationship isolation. Final-head GitHub Actions must show all tests, isolated Alembic upgrade/downgrade and compileall success.
- Exact changed-file allowlist: `backend/src/aram_backend/models.py`, `backend/tests/test_models.py`, this spec, its companion plan, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`.
- No `PROJECT_STATUS.md` change relative to parent #32; no migration, database, `data/`, canonical XLSX/PDF, dependency, workflow, binary, secret or release change.
- All source-to-report financial integrity and owner accounting approvals beyond these invariants remain unverified.

## Reviewer separation and release safety

C1 technical/security, C2 financial/data integrity, and C3 acceptance/release must be three separate, verifiable, non-author reviewer identities. An author-run three-pass audit is not independent evidence. The proposal stays Draft/unmerged when any gate is missing. Rebase on an **accepted** parent SHA only after #32 itself passes its acceptance gates; then rerun all checks.

Rollback before merge: close Draft PR. After a properly authorized merge: independently reviewed revert PR; never force-push, modify protected canonical financial sources, or misstate unmerged code as accepted.
