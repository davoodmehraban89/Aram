# Aram — Latest Handoff Prompt

> Durable accepted-state record reconciled after PR #18 on 2026-08-25 UTC.
> GitHub remote evidence remains authoritative. Always fetch the live branch head and open PRs before acting; the SHA below records a verified control event, not a perpetual current-head claim.

## Accepted repository state

- Repository: davoodmehraban89/Aram
- Canonical branch: source-data-cleanup
- Recorded accepted control event: [PR #18](https://github.com/davoodmehraban89/Aram/pull/18), reviewed head `fcbeb7387218e9ab294318ae462ed59de717fc95`, squash merge `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b` at `2026-08-25T06:46:16Z`.
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

## Single next action

Fetch the live `source-data-cleanup` head and open-PR list, then define one new focused Gate 3 / Gate 2B Mapping task, branch, and PR from that exact head. Use PR #17 only as reference.
