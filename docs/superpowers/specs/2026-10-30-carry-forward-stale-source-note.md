# Issue #37 — stale source note prevention in carry-forward

**Status:** Proposed Draft PR #45; not accepted, not merged. **Base:** unmerged PR #30 `dfcf3f008df54498759243001bdfcd98669a8f23` (parent PR #26 also Draft). Accepted branch unaffected.

## Invariant and failure mode

Rule selection uses latest MappingRule per `rule_key` (version descending, id descending), but that latest rule may still target an **older** NoteDefinition of the same `note_number`. Carrying it to a current target-year note would silently perpetuate an obsolete accounting classification. Never treat matching note numbers as an approval to resurrect stale source rules.

- Read all source-year NoteDefinitions, deterministically ordered by `note_number, version DESC, id DESC`.
- Resolve latest source-year NoteDefinition per `note_number`.
- If the selected latest rule references any older source NoteDefinition, return `("rule_key", "source_note_stale")` in the stable `skipped` queue and **no candidate**.
- Preserve original `source_note_missing`, `target_account_missing`, `target_note_missing`, `target_rule_exists` reasons, target-year Draft checks, chronological company/year checks and current rule selection.
- If both source rule and source note are current, accept only a **read-only preview**; no automatic persistence, target guessing, new rule or flush.
- The caller must obtain explicit accountant approval before saving through separately governed mapping service. No real ledger figures or canonical workbooks are touched.

## Acceptance

Synthetic regressions cover stale source v1 vs v2/v3, current source note, preserved target latest-note resolution, and pending unrelated Session changes not autoflushed. Full Backend CI, Alembic upgrade/downgrade, compileall on final exact SHA; separate non-author C1 technical, C2 accounting and C3 acceptance checks. No release or merge permitted while reviewers/parents unaccepted. Raw SQL/provider concurrency outside scope.
