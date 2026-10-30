# Implementation and Verification Plan — Fiscal-Year Graph Integrity

- Date: 2026-10-30.
- Issue: [#36](https://github.com/davoodmehraban89/Aram/issues/36).
- Parent: [PR #32](https://github.com/davoodmehraban89/Aram/pull/32) @ `28d1c57882ec20fc17c2c133bbe62ff56e12973f` (unaccepted).
- Combined candidate: [Draft PR #35](https://github.com/davoodmehraban89/Aram/pull/35), superseding the separately tested Draft PR #41.
- Design: [fiscal-year-graph-integrity.md](../specs/2026-10-30-fiscal-year-graph-integrity.md).
- Scope: `models.py`, `test_models.py`, spec, plan, append-only log/handoff. No migration or financial source changes.

## Work item A — Same-flush lifecycle protection

1. [x] Branch from exact #32 head. Add regressions without changing implementation.
2. [x] Demonstrate failures against unmodified parent: commit `8e637e96a8c09b5f2fc826922dd4b53a7ec512a3`, [CI 41059319522](https://github.com/davoodmehraban89/Aram/actions/runs/41059319522): **9 failed, 111 passed**. Failure cause: missing expected ValueError on seven existing-record changes, new source document, same-flush company change. A separately committed Draft edit followed by approval remains a passing control.
3. [x] Resolve proposed status from in-session FiscalYear before querying persisted state, and apply same-flush Company guard.
4. [x] Re-run all: fix SHA `f5f9257563f382f6663bc7b1eb0433a43482e9fd`, [CI 41059384195](https://github.com/davoodmehraban89/Aram/actions/runs/41059384195): **120 passed, 1 warning**, Alembic round-trip and compile passed.

## Work item B — Persisted clean dependent references

1. [x] Reproduce gap separately on a child Draft: RED SHA `0994232dfb48eac4d448cf4ea09b8ba770ae0cf0`, [CI 41060564954](https://github.com/davoodmehraban89/Aram/actions/runs/41060564954): **6 failed, 123 passed**. The six failures are cross-year unmodified reference bypasses for two note-reference kinds and statement-year moves, each tested across same and different companies.
2. [x] Add before-flush checks for persisted dependent MappingRule and StatementLine references when NoteDefinition or FinancialStatement year changes. GREEN SHA `c3df2611fdcf20812ca9d9a8c794f1b31d9fcddf`, [CI 41060729930](https://github.com/davoodmehraban89/Aram/actions/runs/41060729930): **129 passed, 1 warning**.
3. [x] Add positive behavior checks: valid unreferenced parent movement, explicit old-year mapping/note-line retarget and moving note and statement parents together. GREEN SHA `78ff0dd5a8ee35b621ae901be39f6a11d37ea063`, [CI 41060899585](https://github.com/davoodmehraban89/Aram/actions/runs/41060899585): **132 passed, 1 warning**.
4. [x] Verify pre-consolidation exact final-head run: `331ce349777b39394c633be929ebbbde904c37b5`, [CI 41061089312](https://github.com/davoodmehraban89/Aram/actions/runs/41061089312): **132 passed, 1 warning**, migrations and compile successful.

## Work item C — Consolidation under Issue #36

1. [x] Copy the verified graph-integrity code and regressions into PR #35's branch, which targets PR #32's exact head.
2. [x] Restore `PROJECT_STATUS.md` from PR #32 to honor Issue #36's file allowlist.
3. [x] Add this design/plan pair; preserve append-only project log and handoff entries with explicit supersession of PR #41.
4. [ ] **Verify CI on the combined PR #35 exact final head** after all consolidation docs have been committed. Required commands in backend:
   - `python -m pip install -e '.[test]'`
   - `pytest`
   - `ARAM_DATABASE_URL=sqlite:///./ci-migration.db alembic upgrade head`
   - `ARAM_DATABASE_URL=sqlite:///./ci-migration.db alembic downgrade base`
   - `python -m compileall -q src tests migrations`
   - `git diff --check` (local when available or inspect complete GitHub patch; do not invent it as executed).
5. [ ] Inspect exact 6-file diff, document performance and concurrency limitations, compare main SHA, and obtain genuine non-author C1/C2/C3 review. All reviewer names and signed-off SHAs must be visible remotely.
6. [ ] Only after consolidated PR #35 has successful final-head tests, close superseded PR #41 *without merge*, link it and the original RED/GREEN evidence in #35.
7. [ ] After the parent #32 itself is independently accepted, rebase/retarget onto the new accepted head and rerun every mandatory check. No routine merge while controls are blocked.

## Acceptance and rollback

- Separate responsibility: ChatGPT authored test/code/docs; it cannot self-certify C1/C2/C3. Controls stay **BLOCKED** until actual distinct reviewers participate.
- This work does not validate raw/bulk SQL, external writers, PostgreSQL/SQL Server concurrency, real accounting data, access permissions, release binaries, or end-to-end source-to-statement reconciliation.
- A reviewer can reject any undeclared changed path, failure log, stale SHA, unindexed reference-scan performance issue or unapproved accounting operation.
- Rollback before merge: close Draft candidate. If later merged with approval, use a new independently reviewed revert PR. Do not modify canonical data or force-push.
