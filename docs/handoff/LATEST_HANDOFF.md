# Aram — Latest Handoff Prompt

> Current authoritative handoff snapshot: 2026-08-24 UTC
> Verify every statement against GitHub before acting.

## Accepted repository state

- Canonical branch: `source-data-cleanup`
- Accepted head: `7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Phase 1B-1, Phase 1B-2, Phase 2A, project controls, and Phase 2B are accepted.
- PR #12 is squash-merged; PR #9 and PR #7 are closed without merge.
- PR #13 is squash-merged and records the Phase 2B acceptance state.
- No user-ready V1 release or EXE is accepted or proven.

## Active focused candidate

- Roadmap: https://github.com/davoodmehraban89/Aram/issues/11
- Task: https://github.com/davoodmehraban89/Aram/issues/14
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Branch: `codex/gate-2a-pilot-workbook`
- Draft PR: https://github.com/davoodmehraban89/Aram/pull/15
- Candidate scope: governed blank Pilot workbook v0.1, reproducible generator,
  human-readable contract, deterministic read-only preflight, focused tests,
  and required project-control updates.
- Template path: `samples/Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx`
- Template SHA-256:
  `e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f`
- Local evidence: nine focused validation scenarios and compileall passed.
- Remote evidence: Backend CI run #23 passed with 52 tests and one warning;
  Alembic upgrade/downgrade and compileall succeeded:
  https://github.com/davoodmehraban89/Aram/actions/runs/32712716962
- Acceptance remains pending independent diff review and an explicit merge decision.

## Safety boundary

The candidate must remain a Draft and unmerged. It does not persist workbook
bytes or financial values, execute mappings, calculate statements, modify
canonical XLSX/PDF or `data/`, or create desktop/release/ZIP/EXE artifacts.

## Single next action

Fetch Draft PR #15 and its exact head, review all changed files against the
base, and verify the final head CI. Correct only failures caused by Issue #14.
Do not start Gate 3 and do not merge without a separate acceptance decision.
