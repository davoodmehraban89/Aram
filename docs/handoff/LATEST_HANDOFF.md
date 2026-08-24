# Aram — Latest Handoff Prompt

> Current authoritative handoff snapshot created: 2026-08-24 UTC
> This file supersedes every earlier handoff prompt. After each meaningful project step, replace this file with a newer version. Do not use older versions as the continuation baseline.

---

## COPY FROM HERE

Use the permanent instructions in `ARAM_MASTER_RECOVERY_PROMPT.md`, then verify this current handoff against the private GitHub repository `davoodmehraban89/Aram`.

### Last independently verified repository state

- Default/canonical branch: `source-data-cleanup`
- Accepted governance merge SHA: `e42d76a24e591a265d3bb6c79ac614ff5b2f211f`
- Governance merge URL: `https://github.com/davoodmehraban89/Aram/commit/e42d76a24e591a265d3bb6c79ac614ff5b2f211f`
- Note: a later documentation-only commit may move the branch head beyond this SHA. Always fetch the current branch head; `e42d76a...` remains the independently verified PR #10 merge evidence.

### Accepted and merged state

- Phase 1B-1: merged through PR #1.
- Phase 1B-2 corrections: merged through PR #4.
- Phase 2A backend/data-model foundation: merged through PR #6.
- One-file model refactor: merged through PR #8.
- Project-control and durable handoff foundation: merged through PR #10 at `e42d76a24e591a265d3bb6c79ac614ff5b2f211f`.
- No accepted, user-ready V1 release has been proven.

### Work currently requiring attention

#### PR #10 — project-control foundation

- URL: `https://github.com/davoodmehraban89/Aram/pull/10`
- State at last verification: CLOSED AND MERGED
- Merged at: `2026-08-24T06:46:50Z`
- Merge SHA: `e42d76a24e591a265d3bb6c79ac614ff5b2f211f`
- Base: `source-data-cleanup`
- Verified base SHA: `5122fd052ebe0ffe0e07dbb8153a872a4f047355`
- Head branch: `codex/project-control-foundation`
- Final reviewed head SHA: `7650aafd06a913d660704ae80dea260eb3728b04`
- Verified scope: 10 files, 794 additions, and 0 deletions.
- Verified changed files:
  - `.github/pull_request_template.md`
  - `AGENTS.md`
  - `PROJECT_STATUS.md`
  - `docs/ACCEPTANCE_POLICY.md`
  - `docs/DECISION_LOG.md`
  - `docs/JULES_TASK_TEMPLATE.md`
  - `docs/PROJECT_LOG.md`
  - `docs/handoff/CHATGPT_BOOTSTRAP_PROMPT.txt`
  - `docs/handoff/LATEST_HANDOFF.md`
  - `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Verification: no trailing whitespace and no conflict markers were found.
- Scope: documentation, agent instructions, and PR template only.
- No application code, tests, workflows, XLSX, PDF, ZIP, EXE, database, or financial-data file changed.
- GitHub Actions/check status at last verification: no workflow run and no status checks were attached to the head commit.
- Acceptance result: independently reviewed, explicitly authorized by Davood, and squash-merged successfully. The durable controls now exist on the accepted branch.

The ten-file count supersedes the earlier six-file, seven-file, and nine-file reports. `AGENTS.md` was added after confirming from official Jules documentation that Jules reads repository-level instructions. Two durable handoff files were added so recovery remains possible when ChatGPT history is unavailable. A plain-text `CHATGPT_BOOTSTRAP_PROMPT.txt` was then added as the saveable entry point that guides a successor chat through official GitHub connection and evidence recovery.

#### PR #9 — Phase 2B ingestion foundation

- URL: `https://github.com/davoodmehraban89/Aram/pull/9`
- Last known state: OPEN, DRAFT, NOT MERGED
- Original base: `source-data-cleanup@5122fd052ebe0ffe0e07dbb8153a872a4f047355`; it must now be rebased or updated onto the accepted governance baseline.
- Last observed head SHA: `8b141d793ad2d534fdf7399bb79d101d53ae29af`
- Claimed scope: source registration, read-only XLSX preflight, and ledger parsing.
- Independent verification confirmed Backend CI run #14 succeeded with the PR head and the exact eight-file scope.
- An independent review comment requested two changes before acceptance: reject same-hash registrations when filename/document type conflicts with the existing record, and integrate the project-control documents after PR #10 becomes the baseline.
- Review comment ID: `5391629767`.

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
- A governed Pilot Excel contract named `Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx` has been created for user testing and future importer implementation. It contains Company, Accounts, Notes, Mapping, Test_Log, Checks, and data-dictionary sheets. It is a data contract, not proof that the current application can import it yet.
- GitHub Issue #11 is the canonical V1 Pilot roadmap: `https://github.com/davoodmehraban89/Aram/issues/11`.

### Current operating decision

- Davood has Google AI Pro and therefore uses Jules in Pro. At the time of this handoff, the published Jules in Pro allowance is 100 tasks per rolling 24 hours and 15 concurrent tasks; this is not expected to constrain the project's controlled, sequential workflow.
- Jules is the primary implementation agent under the repository controls in `AGENTS.md` and the acceptance policy.
- ChatGPT/Codex must independently verify the remote branch, commit, diff, CI, and artifacts after each task.
- GitHub Copilot Cloud Agent is not the planned replacement because it requires a paid Copilot plan and may introduce payment/access risk for Davood in Iran.
- If Jules reports completion that is absent or contradictory in GitHub, reject that task and issue one controlled corrective prompt. Escalate the specific task to direct GitHub/Codex implementation only if the corrective attempt also fails.
- The project must never depend on a single chat session or agent memory.

### Single next action

Send Jules the focused corrective task for PR #9: fix the same-hash semantic identity collision, add regression tests, rebase or update from the accepted governance baseline, and update `PROJECT_STATUS.md` plus append `docs/PROJECT_LOG.md`. Then independently verify its branch, commit, exact diff, CI, and GitHub evidence. Do not begin the Excel importer until the corrected Phase 2B foundation is accepted.

### Mandatory first response

Report whether GitHub access succeeded, then compare this handoff with current GitHub evidence. Do not ask Davood to retell the history and do not start new implementation work before the comparison is complete.

## END COPY

## PR #12 Candidate
- PR #12 is the current Phase 2B review candidate.
- PR #9 is an older candidate that must not be merged while PR #12 is under review.
- PR #12 remains Draft and unmerged.
- The single next action is independent review of PR #12.
