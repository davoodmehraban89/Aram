# Aram Project Status

> Canonical status entry point. Update this file in every meaningful pull request.

## Repository baseline

- Repository: [davoodmehraban89/Aram](https://github.com/davoodmehraban89/Aram)
- Accepted branch: `source-data-cleanup`
- Accepted baseline commit: [`7c7533ee87146dc8fc78b46ebf423be55532c7eb`](https://github.com/davoodmehraban89/Aram/commit/7c7533ee87146dc8fc78b46ebf423be55532c7eb)
- Product objective: a controlled, auditable accounting and financial-statement workflow that preserves canonical source data.

## Status vocabulary

| State | Meaning |
|---|---|
| `VERIFIED_AND_MERGED` | Present on the accepted branch with Git evidence. |
| `VERIFIED_BUT_UNMERGED` | Present in a remote commit or PR, but not accepted. |
| `PRESENT_BUT_UNVERIFIED` | Present, but required tests or evidence are missing. |
| `CLAIMED_BUT_NOT_PROVEN` | Reported by an actor, with no sufficient GitHub evidence. |
| `NOT_IMPLEMENTED` | Required capability is absent. |
| `IN_PROGRESS` | Work is in an open PR and is not accepted. |
| `BLOCKED` | Work cannot proceed until the recorded blocker is resolved. |

## Verified state

| Area | State | Evidence / note |
|---|---|---|
| Phase 1B-1 source inventory | `VERIFIED_AND_MERGED` | [PR #1](https://github.com/davoodmehraban89/Aram/pull/1) |
| Phase 1B-2 audit corrections | `VERIFIED_AND_MERGED` | [PR #4](https://github.com/davoodmehraban89/Aram/pull/4) |
| Phase 2A backend foundation | `VERIFIED_AND_MERGED` | [PR #6](https://github.com/davoodmehraban89/Aram/pull/6) |
| Project control refactor | `VERIFIED_AND_MERGED` | [PR #10](https://github.com/davoodmehraban89/Aram/pull/10) |
| One-file model refactor | `VERIFIED_AND_MERGED` | [PR #8](https://github.com/davoodmehraban89/Aram/pull/8) |
| Phase 2B ingestion foundation | `VERIFIED_AND_MERGED` | [PR #12](https://github.com/davoodmehraban89/Aram/pull/12), squash merge `7b5bd79b760d534dad34b3162f770e838616ebe9` |
| Phase 2B control reconciliation | `VERIFIED_AND_MERGED` | [PR #13](https://github.com/davoodmehraban89/Aram/pull/13), squash merge `7c7533ee87146dc8fc78b46ebf423be55532c7eb` |
| Gate 2A Pilot workbook contract/preflight | `IN_PROGRESS` | Draft [PR #15](https://github.com/davoodmehraban89/Aram/pull/15); Backend CI run #23 passed with 52 tests |
| Parallel V1 prototype | `VERIFIED_BUT_UNMERGED` | Closed, unmerged [PR #7](https://github.com/davoodmehraban89/Aram/pull/7); reference/recovery source only |
| PR #7 test/release claims | `CLAIMED_BUT_NOT_PROVEN` | No independent acceptance evidence recorded |
| Official V1 release | `NOT_IMPLEMENTED` | No accepted user-ready release |
| Comprehensive Mapping Excel import/export | `NOT_IMPLEMENTED` | Mandatory before V1 acceptance |
| Note and sub-note mapping workflow/UI | `NOT_IMPLEMENTED` | Mandatory before V1 acceptance |

The accepted branch does not include PR #7's `desktop/`, `dist/`, ZIP/EXE, or V1 release-documentation changes. A generated binary inside an unmerged branch is not an official release.

## Current risks and blockers

- Agent reports have previously diverged from the remote repository.
- PR #7 is large, unmerged, and cannot be accepted as a single unit.
- PR #12 is accepted and merged; superseded PR #9 is closed without merge.
- Binary execution on a clean Windows environment has not been independently proven.
- Mapping, notes, and sub-notes are incomplete for V1.

## Next approved action

1. Independently review the focused Gate 2A Draft PR implementing [Issue #14](https://github.com/davoodmehraban89/Aram/issues/14).
2. Require a green full Backend CI run and verify the generated blank template checksum.
3. Do not merge without a separate acceptance decision; do not revive PR #9 or merge PR #7 directly.

## Control documents

- [Project log](docs/PROJECT_LOG.md)
- [Decision log](docs/DECISION_LOG.md)
- [Acceptance policy](docs/ACCEPTANCE_POLICY.md)
- [Jules task template](docs/JULES_TASK_TEMPLATE.md)
- [Master recovery prompt](docs/handoff/MASTER_RECOVERY_PROMPT.md)
- [Latest handoff snapshot](docs/handoff/LATEST_HANDOFF.md)
- [Saveable ChatGPT bootstrap prompt](docs/handoff/CHATGPT_BOOTSTRAP_PROMPT.txt)
