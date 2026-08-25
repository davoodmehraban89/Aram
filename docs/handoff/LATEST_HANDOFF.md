# Aram — Latest Handoff Prompt

> Current authoritative candidate snapshot: 2026-08-25 UTC
> GitHub remote evidence remains authoritative. Fetch the live branch and PR heads before acting.

## Accepted repository state

- Repository: davoodmehraban89/Aram
- Canonical branch: source-data-cleanup
- Last independently verified accepted head before the active control candidate: 4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4
- That commit is the squash merge of accepted [PR #15](https://github.com/davoodmehraban89/Aram/pull/15).
- Earlier accepted work includes PR #1, #4, #6, #8, #10, #12, and #13.
- PR #7, PR #9, and PR #16 are closed without merge and contribute no accepted code.
- No user-ready V1 release, tag, ZIP, EXE, or retained release artifact is accepted or proven.

## Accepted Gate 2A evidence

- PR: https://github.com/davoodmehraban89/Aram/pull/15
- Base: source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb
- Reviewed PR head: 74b6a6397a2a2c9199a5c7bcf818bb661b2ebe06
- Squash merge: 4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4
- Final GitHub Actions: https://github.com/davoodmehraban89/Aram/actions/runs/32712900800
- CI conclusion: success; 52 passed, 1 warning; Alembic upgrade/downgrade and compileall succeeded.
- Accepted capabilities: governed Pilot workbook v0.1 contract, approved blank template, reproducible generator, and deterministic read-only in-memory preflight.
- Template path: samples/Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx
- Independently recomputed SHA-256: e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f
- Protected boundary: PR #15 changed no canonical XLSX/PDF, data/, database, financial-source, workflow, migration, desktop/release, ZIP, or EXE path.

## Active control candidate

- Draft PR: https://github.com/davoodmehraban89/Aram/pull/18
- Branch: codex/post-gate2a-control-reconciliation
- Required base: source-data-cleanup@4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4
- Scope: PROJECT_STATUS.md, append-only docs/PROJECT_LOG.md, docs/handoff/LATEST_HANDOFF.md, and the stale-path correction in docs/handoff/MASTER_RECOVERY_PROMPT.md.
- Application code, tests, workflows, migrations, workbook content, financial data, artifacts, and releases are excluded.
- PR #18 remains Draft and unmerged. Its final remote head and four-file diff must be fetched and independently reviewed.

## Closed superseded work

- PR #16 was closed without merge on 2026-08-25.
- It duplicated accepted PR #15, was based on stale head 7c7533ee87146dc8fc78b46ebf423be55532c7eb, had mergeable_state dirty, and recorded the incorrect merge SHA 35d45c3f200672a6ef97f13a84cf7c823ecf1bb8.
- No file or claim from PR #16 is accepted.

## Blocked Gate 2B candidate

- PR: https://github.com/davoodmehraban89/Aram/pull/17
- Base: source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb
- Head: 4f8648add0e2ed60f01753e979fa3fbe9ccf0f18
- State at verification: open, non-Draft, unmerged, mergeable_state dirty.
- GitHub reports 12 changed files although the PR narrative names only 9.
- Backend CI run #31 succeeded with 51 tests, but it ran on the stale branch head and does not prove compatibility with accepted Gate 2A.
- The Mapping code in PR #17 is not accepted. Do not merge or patch that PR in place.
- Comprehensive Mapping Excel import/export, carry-forward, unknown-account queue, note/sub-note mapping, management UI, reproducible Windows packaging, and end-to-end Pilot acceptance remain unimplemented.

## Governance and release reality

- GitHub remote evidence outranks this snapshot and every agent report.
- The accepted branch is currently unprotected; explicit review discipline is therefore mandatory.
- There are no accepted Git tags or GitHub Releases.
- Canonical financial XLSX/PDF and source data remain protected.
- Green CI on an unmerged PR is not acceptance evidence.

## Single next action

Fetch Draft PR #18, verify its final head, exact four-file diff, Draft/unmerged state, protected-data boundary, and any GitHub checks. Record one explicit decision. Do not start, merge, or repair Gate 2B until that control decision is complete.
