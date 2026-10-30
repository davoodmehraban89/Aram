# Aram — Latest Handoff Prompt

> Durable accepted-state record with persistent role assignments and recovery workflow.
> GitHub remote evidence remains authoritative. Always fetch the live branch head and open PRs before acting; recorded SHAs are verified events, not perpetual current-head claims.

## Current correction and focused candidate — 2026-10-23

This dated correction supersedes the older PR #21 candidate/single-next-action narrative below; earlier details remain historical evidence.

- Live accepted base verified: `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- PR #21 is merged (2026-08-27). Accepted-head [Backend CI](https://github.com/davoodmehraban89/Aram/actions/runs/33063001065) succeeded; 67 tests. The legacy UI is quarantined and the PR #21 validation/identity fixes are accepted.
- New branch `codex/v1-year-isolation-followup-20261023` contains a focused, unaccepted follow-up for original-year ownership and relationship/FK reference validation.
- Local follow-up evidence: 110 pytest tests passed, one existing third-party warning; migration round-trip, compile and whitespace checks passed. Original-owner regressions first produced 22 expected failures; effective-reference regressions first produced seven expected failures.
- Exact application scope: `backend/src/aram_backend/models.py`, `backend/tests/test_models.py`. Control scope: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, this handoff, and `docs/superpowers/{specs/2026-10-23-year-isolation-design.md,plans/2026-10-23-year-isolation.md}`.
- Independent local review requested a pending-explicit-ID parent correction; eight regressions were added and all 110 tests passed after the fix. Final remote acceptance remains pending.
- Remaining boundaries: graph-wide moves of clean referencing records, expired fiscal-year lifecycle/same-flush behavior, and bulk/raw/concurrent writes require separate focused acceptance before a financial release.
- Published Draft [PR #32](https://github.com/davoodmehraban89/Aram/pull/32); initial code head `75f82fcbfa2d9745d4c8e358979fe4fe754a82b6`, [Backend CI](https://github.com/davoodmehraban89/Aram/actions/runs/39959519926) success. This reconciliation changes documentation only. Fetch the resulting final head and CI before acceptance. Independent remote acceptance remains required; author must not self-merge.
- Draft PRs #22–31 are active and unaccepted. In particular #26/27 supply mapping foundations, but do not fulfill full account/dimension identity, persisted old/new preview, approval or identical-input duplicate coalescing.
- Owner clarified Peyvast is the first database source, alongside Excel. Vendor FAQ identifies default Microsoft SQL Server, supports 2019/2022 and recommends 2022: https://payvast.com/نرم-افزار-حسابداری/ . The customer installation/schema/access have not been inspected; no live extraction is claimed.
- Preserve canonical data. No migration, dependency, workflow, source XLSX/PDF, `data/`, financial-source value, ZIP/EXE, tag or release changed.
- Next: independent safety review, reconcile dependent drafts, then shared DB/Excel and governed mapping work against documented customer source semantics. A separate design note exists in the task workspace, not as accepted repository functionality.

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

## 2026-10-30 — Same-flush protected-year candidate, not accepted

- Stacked Draft [PR #35](https://github.com/davoodmehraban89/Aram/pull/35) from Draft PR #32 SHA `28d1c57882ec20fc17c2c133bbe62ff56e12973f`; base accepted branch remains unchanged at `7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- Candidate fixes the pending-approval/same-flush ORM validation gap and tests seven record kinds, new source, Company edit, rollback and valid separate-transaction Draft editing.
- Code commit `f5f9257563f382f6663bc7b1eb0433a43482e9fd`; verified [Backend CI 41059384195](https://github.com/davoodmehraban89/Aram/actions/runs/41059384195) passed **120 tests, one warning**, Alembic round-trip and compile.
- Independent reviewers C1/C2/C3 not established. Parent PR #32 is not accepted. Graph-wide, raw SQL and concurrent DB writes remain outside this patch.
- No canonical financial data, application database, migration, workflow, ZIP, EXE or release was modified. This record is documentation about an unmerged candidate, not evidence of acceptance.
- Next action: obtain independent exact-SHA review, then reconcile PR #35 onto an accepted parent only after PR #32 passes its own controls. No merge while blocked.

## 2026-10-30 — Cross-year clean-reference regression candidate (unaccepted)

- Draft [PR #41](https://github.com/davoodmehraban89/Aram/pull/41) depends on unmerged Draft PR #35 `dab37e544e441a6111d7e88a53bae4d193f10de2` and ultimately unmerged PR #32; do not merge a child before its accepted parent is verified.
- Reproduction: clean MappingRule and StatementLine references become inconsistent when their NoteDefinition or FinancialStatement parent changes year. RED [CI 41060564954](https://github.com/davoodmehraban89/Aram/actions/runs/41060564954) showed **6 expected failures, 123 passes**.
- First corrective CI [41060729930](https://github.com/davoodmehraban89/Aram/actions/runs/41060729930) was green (129 passed); expanded valid-path CI [41060899585](https://github.com/davoodmehraban89/Aram/actions/runs/41060899585) also succeeded on code/test SHA `78ff0dd5a8ee35b621ae901be39f6a11d37ea063`: **132 passed, one warning**; migration and compile succeeded.
- Exact final head after documentation updates requires a fresh GitHub verification. No protected data, schema, dependencies, workflows, binaries, production databases or releases changed.
- Remaining: raw/bulk SQL, concurrency and provider-specific database safety are not covered. Three genuinely independent reviewer controls remain `BLOCKED`; neither this child nor its parents has been accepted.
- Next action: independently review final PR #32, #35 and #41 SHAs, reconcile dependent bases after each acceptance, and address DB-level isolation/performance as separately scoped work.

## 2026-10-30 — Follow-up: Issue #36 consolidation, single review candidate

- Existing [Issue #36](https://github.com/davoodmehraban89/Aram/issues/36) requires both ORM gaps together, with six explicit allowed files and parent PR #32 SHA `28d1c57882ec20fc17c2c133bbe62ff56e12973f`.
- Consolidated [Draft PR #35](https://github.com/davoodmehraban89/Aram/pull/35) now implements both fixes using the previously proven 132-test code, design/plan, and append-only evidence; earlier [Draft PR #41](https://github.com/davoodmehraban89/Aram/pull/41) is a superseded experimental child, not a second approval path.
- `PROJECT_STATUS.md` reverted to parent #32 content on PR #35, keeping the exact Issue #36 allowlist. Any older references in this handoff to PR #41 as the next candidate are superseded by this entry.
- Verify the new exact PR #35 final SHA and its GitHub Actions before closing PR #41 without merge. Do not merge PR #35, PR #32 or PR #33 until their independent financial/technical/governance controls pass.
- ORM-only boundary: raw/bulk SQL, external database writers, concurrency and target-note scan performance remain pending separate evidence. No original accounting source data or production database changed.

## 2026-10-30 — Consolidated candidate and duplicate cleanup verified

- [PR #35](https://github.com/davoodmehraban89/Aram/pull/35) now has both Issue #36 ORM fixes, 132 tests and the six-file allowed diff. Code/docs SHA `8bd5817b324e1585aca88b72285a4fc00187369d` passed [Backend CI 41061793756](https://github.com/davoodmehraban89/Aram/actions/runs/41061793756): SUCCESS, **132 passed, 1 warning**, migration round-trip and compile succeeded.
- Duplicate [PR #41](https://github.com/davoodmehraban89/Aram/pull/41) was **closed unmerged** after successful consolidation. The previous handoff's description of #41 as a pending child is superseded; its CI remains historical test evidence.
- `PROJECT_STATUS.md` is unchanged relative to PR #32; PR #35's changed paths are the six permitted by [Issue #36](https://github.com/davoodmehraban89/Aram/issues/36).
- Final documentation SHA will differ; verify the live PR head and exact-head CI before review. No independent C1/C2/C3 approvals; acceptance remains BLOCKED. The accepted branch remains unchanged and no protected data/source files were modified.
