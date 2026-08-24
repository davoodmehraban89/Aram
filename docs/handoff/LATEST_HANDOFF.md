# Aram — Latest Handoff Prompt

> Current authoritative handoff snapshot created: 2026-08-24 UTC
> This file supersedes every earlier handoff prompt. After each meaningful project step, replace this file with a newer version. Do not use older versions as the continuation baseline.

---

## COPY FROM HERE

Use the permanent instructions in `ARAM_MASTER_RECOVERY_PROMPT.md`, then verify this current handoff against the private GitHub repository `davoodmehraban89/Aram`.

### Last independently verified repository state

- Default/canonical branch: `source-data-cleanup`
- Accepted baseline SHA at the start of the control-documentation work: `5122fd052ebe0ffe0e07dbb8153a872a4f047355`
- Baseline URL: `https://github.com/davoodmehraban89/Aram/commit/5122fd052ebe0ffe0e07dbb8153a872a4f047355`

### Accepted and merged state

- Phase 1B-1: merged through PR #1.
- Phase 1B-2 corrections: merged through PR #4.
- Phase 2A backend/data-model foundation: merged through PR #6.
- One-file model refactor: merged through PR #8.
- No accepted, user-ready V1 release has been proven.

### Work currently requiring attention

#### PR #10 — project-control foundation

- URL: `https://github.com/davoodmehraban89/Aram/pull/10`
- State at last verification: OPEN, DRAFT, NOT MERGED
- Base: `source-data-cleanup`
- Verified base SHA: `5122fd052ebe0ffe0e07dbb8153a872a4f047355`
- Head branch: `codex/project-control-foundation`
- Precursor head SHA immediately before this handoff update: `a0440cb2e18effc8ef405fb92a398323a996167b`
- Important: the commit that updates this handoff file necessarily changes the PR head again. Always fetch the current PR head from GitHub; do not treat the embedded precursor SHA as the current head.
- Verified scope: 9 files and 0 deletions; immediately before this handoff update GitHub reported 680 additions.
- Verified changed files:
  - `.github/pull_request_template.md`
  - `AGENTS.md`
  - `PROJECT_STATUS.md`
  - `docs/ACCEPTANCE_POLICY.md`
  - `docs/DECISION_LOG.md`
  - `docs/JULES_TASK_TEMPLATE.md`
  - `docs/PROJECT_LOG.md`
  - `docs/handoff/LATEST_HANDOFF.md`
  - `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Verification: no trailing whitespace and no conflict markers were found.
- Scope: documentation, agent instructions, and PR template only.
- No application code, tests, workflows, XLSX, PDF, ZIP, EXE, database, or financial-data file changed.
- GitHub Actions/check status at last verification: no workflow run and no status checks were attached to the head commit.
- Mergeability at last verification: GitHub reported mergeable, but it was intentionally left Draft and unmerged.

The nine-file count supersedes the earlier six-file and seven-file reports. `AGENTS.md` was added after confirming from official Jules documentation that Jules reads repository-level instructions. The two handoff files were then added so recovery remains possible even when ChatGPT history is unavailable.

#### PR #9 — Phase 2B ingestion foundation

- URL: `https://github.com/davoodmehraban89/Aram/pull/9`
- Last known state: OPEN, DRAFT, NOT MERGED
- Base: `source-data-cleanup@5122fd052ebe0ffe0e07dbb8153a872a4f047355`
- Last observed head SHA: `8b141d793ad2d534fdf7399bb79d101d53ae29af`
- Claimed scope: source registration, read-only XLSX preflight, and ledger parsing.
- Do not accept its reported tests or CI from this handoff alone; re-fetch the current PR, diff, run URLs, and conclusions.

#### PR #7 — closed prototype/recovery source

- URL: `https://github.com/davoodmehraban89/Aram/pull/7`
- State: CLOSED, UNMERGED.
- It contains a large parallel prototype including desktop and branch-level ZIP/EXE work.
- It is not an accepted V1 and must not be merged directly.
- Recover useful features only through small, focused PRs based on the accepted branch.

### Current product boundary

- Comprehensive financial-statement Mapping Excel import/export is not complete.
- Note and sub-note mapping workflow is not complete.
- Mapping management UI is not complete.
- Official `v1.0.0-pilot` GitHub Release and independently verified downloadable assets have not been proven.
- Branch-level ZIP/EXE existence does not equal an official or tested release.

### Current operating decision

- Jules may remain the implementation agent only under the repository controls in `AGENTS.md` and the acceptance policy.
- ChatGPT/Codex must independently verify the remote branch, commit, diff, CI, and artifacts after each task.
- If Jules again reports completion that is absent or contradictory in GitHub, migrate implementation work to GitHub Copilot Cloud Agent.
- The project must never depend on a single chat session or agent memory.

### Single next action

Re-fetch PR #10 from GitHub and independently verify:

1. it still targets `source-data-cleanup`;
2. its current head SHA and exact nine-file diff;
3. no code, workflow, binary, database, or canonical financial-data changes exist;
4. the contents accurately reflect GitHub reality;
5. whether any branch conflict or new check appeared.

Then give Davood an explicit decision: approve PR #10 for merge, or reject it with exact requested changes. Do not merge without his explicit authorization. Only after PR #10 is resolved should PR #9 be independently reviewed.

### Mandatory first response

Report whether GitHub access succeeded, then compare this handoff with current GitHub evidence. Do not ask Davood to retell the history and do not start new implementation work before the comparison is complete.

## END COPY
