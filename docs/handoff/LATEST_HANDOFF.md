# Aram — Latest Handoff Prompt

> Durable accepted-state record with persistent role assignments and recovery workflow.
> GitHub remote evidence remains authoritative. Always fetch the live branch head and open PRs before acting; recorded SHAs are verified events, not perpetual current-head claims.

## Accepted repository state

- Repository: davoodmehraban89/Aram
- Canonical branch: source-data-cleanup
- Recorded accepted control event: [PR #18](https://github.com/davoodmehraban89/Aram/pull/18), reviewed head `fcbeb7387218e9ab294318ae462ed59de717fc95`, squash merge `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b` at `2026-08-25T06:46:16Z`.
- Durable post-merge record: [PR #19](https://github.com/davoodmehraban89/Aram/pull/19), reviewed head `b9059592409606a0a4f11a71c30778cff158b6b6`, squash merge `77f9f595ccfe67a87b11024ff0f6143629dba438` at `2026-08-25T06:57:02Z`.
- Earlier accepted work includes PR #1, #4, #6, #8, #10, #12, #13, and #15.
- PR #7, PR #9, PR #16, and PR #17 are closed without merge and contribute no accepted code.
- [Issue #14](https://github.com/davoodmehraban89/Aram/issues/14) is completed. [Issue #11](https://github.com/davoodmehraban89/Aram/issues/11) records Gate 3 as ready for a new focused task definition.
- No user-ready V1 release, tag, ZIP, EXE, or retained release artifact is accepted or proven.

## Accepted Gate 2A evidence

- PR: https://github.com/davoodmehraban89/Aram/pull/15
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Reviewed PR head: `74b6a6397a2a2c9199a5c7bcf818bb661b2ebe06`
- Squash merge: `4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4`
- Final GitHub Actions: https://github.com/davoodmehraban89/Aram/actions/runs/32712900800
- CI conclusion: success; 52 passed, 1 warning; Alembic upgrade/downgrade and compileall succeeded.
- Accepted capabilities: governed Pilot workbook v0.1 contract, approved blank template, reproducible generator, and deterministic read-only in-memory preflight.
- Template path: `samples/Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx`
- Independently recomputed SHA-256: `e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f`
- Protected boundary: PR #15 changed no canonical XLSX/PDF, `data/`, database, financial-source, workflow, migration, desktop/release, ZIP, or EXE path.

## Accepted PR #18 control evidence

- Base: `source-data-cleanup@4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4`
- Reviewed head: `fcbeb7387218e9ab294318ae462ed59de717fc95`
- Squash merge: `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`
- Exact changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Verification: complete remote four-file diff and metadata reviewed; append-only project-log behavior and protected-data boundary confirmed.
- GitHub Actions: none on the reviewed head; documentation-only paths did not trigger Backend CI.
- Artifacts/releases: `NONE`
- Protected boundary: no application code, tests, workflow, migration, dependency, workbook content, financial data, binary, ZIP, EXE, artifact, or release file changed.
- Acceptance authority: Davood explicitly authorized the merge after independent review.

## Accepted PR #19 control evidence

- Base: `source-data-cleanup@f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`
- Reviewed head: `b9059592409606a0a4f11a71c30778cff158b6b6`
- Squash merge: `77f9f595ccfe67a87b11024ff0f6143629dba438`
- Exact changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`
- Verification: complete remote three-file diff, append-only log, whitespace, protected-data boundary, and post-merge accepted-head state passed.
- GitHub Actions: none on the reviewed head; documentation-only paths did not trigger Backend CI.
- Artifacts/releases: `NONE`

## Durable role-based operating model

- Permanent source: `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Decision record: ADR-011 in `docs/DECISION_LOG.md`
- Introduced through: [PR #20](https://github.com/davoodmehraban89/Aram/pull/20)
- Davood is Project Owner and the accounting/product authority.
- ChatGPT chat is Operational Coordinator: recovery, task scoping, implementation prompts, first-pass review, and copy-ready handoffs.
- Jules is the primary Implementation Agent: exact-base focused implementation, tests, Draft PR, and evidence; it never merges its own PR.
- Codex Work is Senior Technical Supervisor, Independent Reviewer, and Authorized Maintainer: technical sequencing, remote evidence review, conflict resolution, exceptional critical fixes, acceptance decisions, and routine merges under standing delegation.
- GitHub is the evidence source of truth.
- Accounting ambiguity, material scope, protected-data changes, releases, destructive actions, credentials, and new external authority remain Davood escalation points.
- A repository mismatch pauses only the affected task without edits; it does not halt the project.

## Closed superseded work

- PR #16 was closed without merge on 2026-08-25.
- It duplicated accepted PR #15, used stale base `7c7533ee87146dc8fc78b46ebf423be55532c7eb`, was dirty, and recorded incorrect merge SHA `35d45c3f200672a6ef97f13a84cf7c823ecf1bb8`.
- No file or claim from PR #16 is accepted.

## Closed Gate 3 / Gate 2B reference

- PR: https://github.com/davoodmehraban89/Aram/pull/17
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Head: `4f8648add0e2ed60f01753e979fa3fbe9ccf0f18`
- Final state: closed without merge on 2026-08-25; its code is not accepted.
- GitHub reports 12 changed files although the PR narrative names only 9.
- Backend CI run #31 succeeded with 51 tests on the stale branch head; that does not prove compatibility with accepted Gate 2A.
- Use PR #17 only as reference. Do not reopen, revive, or merge it.
- Comprehensive Mapping Excel import/export, carry-forward, unknown-account queue, note/sub-note mapping, management UI, reproducible Windows packaging, and end-to-end Pilot acceptance remain unimplemented.

## Governance and release reality

- GitHub remote evidence outranks this record and every agent report.
- The accepted branch is currently unprotected; explicit review discipline is mandatory.
- There are no accepted Git tags or GitHub Releases.
- Canonical financial XLSX/PDF and source data remain protected.
- Green CI on an unmerged PR is not acceptance evidence.
- No Gate 3 implementation candidate is accepted or active.

## Active V1-01 safety-gate candidate

- Verified base: `source-data-cleanup@b1ddee87d31ee73b3a5aeac8f9953d0a604c206a`
- Working branch: `codex/v1-01-safety-gate-hardening`
- Draft PR: [#21](https://github.com/davoodmehraban89/Aram/pull/21)
- Independently reviewed implementation head: `700d800dbd9c657f6bd510faafedcbde4847fafd`.
- Earlier exact-head candidate: `aba10b61c770ce319b1b67d960a4f0a1057e25f6`; [Backend CI #36](https://github.com/davoodmehraban89/Aram/actions/runs/32989551021) succeeded.
- A later documentation-triggered [Backend CI #38](https://github.com/davoodmehraban89/Aram/actions/runs/33015151139) exposed a flaky message-specific reparent assertion: protection fired correctly, but through the equally valid parent-company invariant.
- Stabilized candidate: `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`; the single test assertion now accepts either valid `cannot be mutated` protection message without changing product behavior.
- Latest verified CI: [Backend CI #39](https://github.com/davoodmehraban89/Aram/actions/runs/33015277194), success on `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`; 67 tests passed, migration upgrade/downgrade and compile succeeded.
- Purpose: close the independently reproduced protected-year deletion/mutation and Pilot-preflight false-negative defects before any Mapping/UI expansion.
- Planned changed files: `index.html`, `PROJECT_STATUS.md`, `backend/src/aram_backend/models.py`, `backend/src/aram_backend/pilot_workbook.py`, `backend/tests/test_models.py`, `backend/tests/test_pilot_workbook.py`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`.
- Local evidence at preparation: 67 pytest tests passed; isolated Alembic upgrade/downgrade and compileall passed; focused Ruff and mypy checks passed.
- Protected boundary: no canonical financial data, workbook, PDF, database, financial value, binary, ZIP, EXE, tag, or release is in scope.
- Independent-review decision: code, scope, diff, and protected-data boundary passed. CI #38 later revealed only a nondeterministic error-message assertion; CI #39 passed after the one-line assertion stabilization.
- Status: `IN_PROGRESS`; this durable-document reconciliation records the complete CI sequence. The resulting documentation-only head must be re-fetched and compared with `b3dc8b3a18934ffe63f615e4f650248be21a5f9c` before Ready/Squash Merge.

## Single next action

Publish this requested two-document reconciliation on PR #21 and route the resulting documentation-only head back to the independent reviewer. The reviewer must confirm that only `PROJECT_STATUS.md` and `docs/handoff/LATEST_HANDOFF.md` changed after the CI-verified stabilized head `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`, verify the final workflow result, then Ready/Squash Merge. Do not begin Gate 3 Mapping until V1-01 is accepted.


## 2026-11-11 — Eight-phase progress dashboard handoff

- Operational progress register: `docs/ARAM_EXECUTION_PROGRESS_DASHBOARD.md`.
- Governing policy and phase acceptance rules: `docs/ARAM_MASTER_CONTROL_PLAN.md`.
- Dashboard was added on control branch `docs/aram-master-control-plan-20261111`, commit `8891c614001eb5090363bf6f77be530f0edfa1f8`.
- Draft PR #91 remains open; this is not merged into accepted baseline.
- Initial estimates: Phase 0 65%, Phase 1 25%, Phase 2 30%, Phase 3 25%, Phase 4 10%, Phase 5 30%, Phase 6 10%, Phase 7 5%; unweighted mean 25%.
- Percentages are estimates from available evidence. No phase is fully accepted; production / release remains NO-GO.
- Dashboard records work-item evidence states, remaining work, blockers, exit criteria and immediate priorities. Any future percentage change must cite the exact evidence URL / SHA and preserve progress history.
- Next action: independent review of dashboard and control-plan updates on PR #91; then keep the dashboard current as financial, mapping, security and operational gates progress.


## 2026-11-11 — File-level worktree disposition

- Detailed register: `docs/ARAM_WORKTREE_FILE_LEVEL_DISPOSITION_20261111.md`.
- All 62 current source files still exist and match the snapshot manifest SHA-256; no post-snapshot source changes detected.
- All 62 entries have a proposed disposition and rationale.
- This does not authorize integration. Keep original worktrees and snapshot untouched.
- Phase 0 remains 65%; next task is independent disposition review and resolution of the Mapping / dependency / migration conflicts.


## 2026-11-11 — Account 8161 dry-run update

- The seven-rule proposal now has an in-memory simulation across 17,075 account-8161 rows.
- It predicts 75 new unique matches (24 non-zero, 51 zero-balance), 35 remaining unmatched rows all zero-balance, and no ambiguity.
- Simulated exposure ties exactly to 196,907,918,801 Rials.
- No workbook was saved; official Mapping and ledgers remain unchanged.
- Accounting-owner approval and independent review remain required before persistent changes.


## 2026-11-11 — Latest Phase 1 handoff

- Account 8161: read the seven-rule proposal and in-memory simulation in Draft PR #90; no official Mapping workbook changed.
- 1403 equity: likely duplicated prior-period adjustment; read `FS_1403_EQUITY_DUPLICATE_PRIOR_PERIOD_ADJUSTMENT_20261111.md` and obtain owner confirmation of original journals / approved trial balances.
- 1403 Note 23 is duplicated across sheet29 and sheet30; note catalog and matrix distinguish both sections.
- 1402/1404 auditor opening pages reviewed; full report review incomplete; 1403 PDF extraction failed.
- No source financial workbook/PDF modified.


## 2026-11-11 — Budget source integrity handoff

- Read `docs/BUDGET_1404_NOTE39_UNIT_AND_REF_ERRORS_20261111.md`.
- Do not repair #REF! cells or convert E22:E32 without the approved original budget source.
- E22:E32 in 1404 are exactly 1,000,000x corresponding revised-budget F values; E35 is not part of the anomaly.
- All source financial workbooks remain unchanged.


## 2026-11-11 — Open PR backlog handoff

- 55 open PRs exist; all are Draft.
- 13 target `source-data-cleanup` directly; 42 are stacked on another PR head. See `docs/OPEN_PULL_REQUEST_DEPENDENCY_INVENTORY_20261111.md` and `docs/OPEN_PULL_REQUEST_DEPENDENCY_GRAPH_20261111.md`.
- Do not merge children before reviewing parents. Do not mass-close or retarget branches.
- Phase 0 estimate is now 55% (revised from 65% due expanded scope); overall unweighted estimate is 24%. Other phase estimates unchanged.
- Next Phase 0 task: V1 scope classification and commit/file overlap matrix for the 55 PRs.


## 2026-11-11 — Open PR file overlap handoff

- Full changed-file inventory: `docs/OPEN_PULL_REQUEST_FILE_OVERLAP_MATRIX_20261111.md`.
- 55 open PRs; 427 changed-file entries; 221 unique paths; 64 shared paths; 1,048 PR-pair/path overlaps.
- Control docs are heavily shared across draft PRs; compare each stacked PR against its immediate base before merging or cherry-picking.
- Phase 0 remains 55%; V1 scope classification and semantic/commit-level review remain the next gates.
