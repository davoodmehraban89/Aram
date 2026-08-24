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
- Accepted head after Phase 2B:
  `7b5bd79b760d534dad34b3162f770e838616ebe9`
- Phase 1B-1: merged through PR #1.
- Phase 1B-2 corrections: merged through PR #4.
- Phase 2A backend foundation: merged through PR #6.
- One-file model refactor: merged through PR #8.
- Project-control foundation: merged through PR #10.
- Phase 2B ingestion foundation: independently reviewed and squash-merged
  through PR #12 on 2026-08-24.
- No user-ready V1 release has been accepted or proven.

### Accepted Phase 2B evidence

- PR: https://github.com/davoodmehraban89/Aram/pull/12
- Reviewed PR head: `f7cb6abb7caf3f1c0c28d402ae41b0e3c005a280`
- Squash merge commit:
  `7b5bd79b760d534dad34b3162f770e838616ebe9`
- Final PR CI: https://github.com/davoodmehraban89/Aram/actions/runs/32705724028
- CI conclusion: `success`; 42 tests passed, Alembic upgrade/downgrade
  succeeded, and compileall succeeded.
- Accepted capabilities: metadata-only source registration, exact-duplicate
  idempotency, semantic-conflict rejection, read-only XLSX structural
  inspection, and typed in-memory general-ledger parsing.
- Protected boundary: no canonical XLSX/PDF, `data/`, database, ZIP, EXE,
  binary, or financial-source file changed in PR #12.

### Superseded work

- PR #9: https://github.com/davoodmehraban89/Aram/pull/9
- State: CLOSED WITHOUT MERGE on 2026-08-24.
- PR #9 must not be reopened or merged; its Phase 2B role was replaced by
  accepted PR #12.
- PR #7 remains closed and unmerged. Recover any useful feature only through a
  separately approved, focused PR.

### Remaining product boundary

- Comprehensive Mapping Excel import/export is not implemented.
- Note and sub-note mapping workflow and UI are not implemented.
- Official `v1.0.0-pilot` release and clean-environment artifacts are not proven.
- GitHub Issue #11 remains the V1 Pilot roadmap:
  https://github.com/davoodmehraban89/Aram/issues/11

### Single next action

Review and merge the documentation-only post-merge control update that records
the accepted PR #12 merge and PR #9 closure. After that, verify Issue #11 and
select the next small, controlled implementation task. Do not begin work from
an old Jules task or cached branch.

### Mandatory first response

Report whether GitHub access succeeded. Verify the canonical branch head,
PR #12 merge state, PR #9 closure state, the current documentation-control PR,
and CI evidence. Do not start implementation until this comparison is complete.

## END COPY
