# Aram — Latest Handoff Prompt

> Current authoritative handoff snapshot: 2026-08-24 UTC
> This file supersedes every earlier handoff prompt. Verify every statement against GitHub before acting.

---

## COPY FROM HERE

Use the permanent instructions in `docs/handoff/MASTER_RECOVERY_PROMPT.md`, then
verify this snapshot against the private repository `davoodmehraban89/Aram`.
Do not ask Davood to reconstruct project history from memory.

### Accepted repository state

- Canonical branch: `source-data-cleanup`
- Approved base used by the active Phase 2B candidate:
  `a41b07d7a7dd192c3ae4a277eb4903327883456f`
- Phase 1B-1: merged through PR #1.
- Phase 1B-2 corrections: merged through PR #4.
- Phase 2A backend foundation: merged through PR #6.
- One-file model refactor: merged through PR #8.
- Project-control foundation: merged through PR #10.
- No Phase 2B candidate and no user-ready V1 release has been accepted or merged.

### Active Phase 2B candidate: PR #12

- URL: https://github.com/davoodmehraban89/Aram/pull/12
- Branch: `codex/phase-2b-source-registration-12955190277775369594`
- Base: `source-data-cleanup@a41b07d7a7dd192c3ae4a277eb4903327883456f`
- State at last verification: OPEN, DRAFT, MERGEABLE, NOT MERGED.
- Independently reviewed implementation head:
  `9e90533658e400a51402db673efae9cbd0aa37d1`
- Scope at that head: 11 files; no canonical XLSX/PDF, `data/`, database,
  ZIP, EXE, or financial-source file.
- Backend CI run #17:
  https://github.com/davoodmehraban89/Aram/actions/runs/32703999006
- Run #17 conclusion: `success`.
- Regression tests cover exact-duplicate idempotency and rejection of same-year,
  same-hash conflicts in filename, document type, or both. Rejected conflicts
  leave one unchanged original `SourceDocument`.
- Backend README documents metadata-only registration, supported types,
  read-only XLSX inspection and ledger parsing, semantic-conflict rejection,
  and the non-persistence of payload bytes and financial values.
- Documentation-control corrections were added after the reviewed implementation
  head; fetch the current PR head and its newest CI before deciding acceptance.

### Superseded candidate: PR #9

- URL: https://github.com/davoodmehraban89/Aram/pull/9
- PR #9 is the older Phase 2B candidate.
- Do not merge PR #9 while PR #12 is under review.
- Close or otherwise disposition PR #9 only after PR #12 receives an explicit
  independent acceptance decision.

### Protected boundaries

- Do not modify canonical XLSX/PDF files, `data/`, financial source values,
  databases, ZIP/EXE artifacts, mappings, desktop code, or release code as part
  of Phase 2B candidate review.
- PR #7 remains closed and unmerged; recover work from it only through separately
  approved focused tasks.
- Mapping import/export, note/sub-note workflow, UI, and an official tested V1
  release remain incomplete.

### Single next action

Independently review the current remote head of Draft PR #12: verify its complete
diff, changed-file list, new Backend CI result, regression behavior, and protected
data boundary. Record an explicit acceptance decision. Do not merge either PR #12
or PR #9 before that decision.

### Mandatory first response

Report whether GitHub access succeeded. Then report the current PR #12 head,
Draft/merge state, exact changed files, and CI evidence compared with this handoff.
Do not start new implementation work until that comparison is complete.

## END COPY
