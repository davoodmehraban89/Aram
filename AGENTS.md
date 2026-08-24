# Repository Agent Instructions

These instructions apply to every AI coding agent working in this repository, including Jules, Copilot, and Codex.

## Source of truth

GitHub remote state is authoritative. Before editing:

1. Fetch the remote.
2. Read `PROJECT_STATUS.md`, `docs/ACCEPTANCE_POLICY.md`, and `docs/PROJECT_LOG.md`.
3. Verify the requested base branch and full base SHA.
4. If the actual SHA or repository state differs from the task, stop without changes and report the mismatch.

Never treat a local file, task summary, or agent report as proof that a branch, PR, CI run, artifact, tag, or release exists.

## Work rules

- Use one dedicated branch and one focused PR per task.
- Modify only explicitly allowed paths.
- Do not merge your own PR.
- Do not incorporate work from closed PR #7 except when a task explicitly identifies the exact feature and files to recover.
- Do not modify canonical XLSX/PDF, `data/`, databases, or financial source values unless the task is an approved data-change task with hashes and recovery steps.
- Do not commit ZIP, EXE, build output, secrets, credentials, caches, or local databases unless explicitly required by an approved artifact task.
- Do not invent financial values, mapping rules, tests, CI outcomes, URLs, or acceptance status.

## Verification

- Run the exact tests required by the task.
- Run `git diff --check`.
- Inspect the complete diff against the approved base SHA.
- Confirm the exact changed-file list.
- Push the branch and open a real PR into the requested base branch.
- Provide real commit, PR, CI, artifact, and release URLs when applicable.
- If GitHub publication fails, the task is not complete.

## Project records

Every meaningful PR must:

- update `PROJECT_STATUS.md` when current state changes;
- append a complete entry to `docs/PROJECT_LOG.md`;
- add a new ADR instead of silently rewriting an accepted decision;
- satisfy `docs/ACCEPTANCE_POLICY.md`;
- use `.github/pull_request_template.md`;
- update `docs/handoff/LATEST_HANDOFF.md` after every meaningful completed or rejected step so a successor can resume without chat history;
- keep `docs/handoff/MASTER_RECOVERY_PROMPT.md` stable unless the governance process itself changes;
- keep `docs/handoff/CHATGPT_BOOTSTRAP_PROMPT.txt` as the saveable entry point for a successor chat.

An agent's written success report is not acceptance evidence.

## Required final response

Return the verified base SHA, remote branch, full head SHA, PR number and URL, exact changed files, test commands/results, GitHub Actions URLs/results, artifact/release evidence or `NONE`, protected-data confirmation, and remaining risks.

End with: `Ready for independent GitHub review; not merged.`
