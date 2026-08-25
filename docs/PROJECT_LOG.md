# Project Log

This is an append-only operational log. Never delete or rewrite accepted entries. Corrections must be added as new entries that reference the original entry.

## Required entry fields

Each new entry must record: UTC timestamp, actor, task/phase, base branch and SHA, working branch, PR number/URL, commit SHA, exact changed files, test command, GitHub Actions run URL/result, artifact or release URL, acceptance status, reviewer, remaining risks, and next action. Unknown evidence must be written as `NOT_VERIFIED`, never guessed.

## Historical entries imported from GitHub

### 2026-08-18T11:08:12Z — Phase 1B-1

- Actor: Jules / repository owner
- Base: `source-data-cleanup@d18287a74c9453e8071ed03db6b369805b5ccde3`
- Working branch: `phase-1b1-audit-report-7365389436990903239`
- PR: [#1](https://github.com/davoodmehraban89/Aram/pull/1)
- Head SHA: `a3e3f675ca637b5ab719b1d6e5fc37c9fb47f707`
- Merge SHA: `cd074095c3d63a4a2da1ab8490ce772f555fc91d`
- Changed files: 3; exact list available in the PR
- Tests / CI / artifacts: `NOT_VERIFIED`
- Acceptance: `VERIFIED_AND_MERGED`
- Reviewer: repository owner
- Remaining risk: historical test evidence not recorded here
- Next action: Phase 1B-2

### 2026-08-19T16:29:06Z — Phase 1B-2 corrections

- Actor: Jules / repository owner
- Base: `source-data-cleanup@cd074095c3d63a4a2da1ab8490ce772f555fc91d`
- Working branch: `jules-1168663913887856558-73b8a885`
- PR: [#4](https://github.com/davoodmehraban89/Aram/pull/4)
- Head SHA: `ce77f7511066ff85845e6d1f383f20a264f4730b`
- Merge SHA: `f8084268c1080595d9da672d490834ed677ad77f`
- Changed files: 7; exact list available in the PR
- Tests / CI / artifacts: `NOT_VERIFIED`
- Acceptance: `VERIFIED_AND_MERGED`
- Reviewer: repository owner
- Remaining risk: claims must still be interpreted against the source evidence
- Next action: Phase 2A

### 2026-08-20T18:53:39Z — Phase 2A backend foundation

- Actor: ChatGPT/Codex implementation; repository owner
- Base: `source-data-cleanup@f8084268c1080595d9da672d490834ed677ad77f`
- Working branch: `codex/phase-2a-backend-foundation`
- PR: [#6](https://github.com/davoodmehraban89/Aram/pull/6)
- Head SHA: `2bcf2b3cbab6d3df1d9340397cec43e363aec8f7`
- Merge SHA: `84b19ef1a6efe3e82291a565829ba3e1fc47d246`
- Changed files: 18; exact list available in the PR
- Reported test command: `cd backend && pytest`
- GitHub Actions: reported successful in PR; direct run URL not recorded here
- Artifacts: none
- Acceptance: `VERIFIED_AND_MERGED`
- Reviewer: repository owner
- Remaining risk: preserve data and fiscal-year invariants
- Next action: focused ingestion work

### 2026-08-24T00:34:12Z — Model refactor

- Actor: Jules / repository owner
- Base: `source-data-cleanup@84b19ef1a6efe3e82291a565829ba3e1fc47d246`
- Working branch: `refactor/drg-parent-year-id-15088443704684163304`
- PR: [#8](https://github.com/davoodmehraban89/Aram/pull/8)
- Head SHA: `b602ced45b04ac0876acac2dcca381d72de38c27`
- Merge SHA: `5122fd052ebe0ffe0e07dbb8153a872a4f047355`
- Changed files: `backend/src/aram_backend/models.py`
- Reported test command: `python -m pytest backend/tests/`
- GitHub Actions URL: `NOT_VERIFIED`
- Artifacts: none
- Acceptance: `VERIFIED_AND_MERGED`
- Reviewer: repository owner
- Remaining risk: none newly recorded
- Next action: Phase 2B review

### 2026-08-24T00:34:36Z — Parallel V1 prototype closed

- Actor: Jules / repository owner
- Base: `source-data-cleanup@84b19ef1a6efe3e82291a565829ba3e1fc47d246`
- Working branch: `phase-2a-backend-foundation-10237597358138521261`
- PR: [#7](https://github.com/davoodmehraban89/Aram/pull/7)
- Head SHA: `a06aab6f2e2c50ec8111316b1a689fb71660c000`
- Merge SHA: none
- Changed files: 94; exact list available in the PR
- Tests / GitHub Actions / official release: `NOT_VERIFIED`
- Branch artifacts: present in the unmerged PR; not accepted release assets
- Acceptance: `VERIFIED_BUT_UNMERGED`; closed, superseded/out of scope
- Reviewer: repository owner
- Remaining risk: large parallel implementation; do not merge directly
- Next action: recover feature-by-feature through focused PRs

### 2026-08-24T01:34:25Z — Phase 2B ingestion foundation opened

- Actor: ChatGPT/Codex implementation; repository owner
- Base: `source-data-cleanup@5122fd052ebe0ffe0e07dbb8153a872a4f047355`
- Working branch: `codex/phase-2b-source-registration`
- PR: [#9](https://github.com/davoodmehraban89/Aram/pull/9)
- Head SHA at import: `8b141d793ad2d534fdf7399bb79d101d53ae29af`
- Changed files: 8; exact list available in the PR
- Reported test command: `pytest`
- Reported GitHub Actions: success; direct run URL must be checked during review
- Artifacts: none
- Acceptance: `IN_PROGRESS`; draft, not merged
- Reviewer: pending independent review
- Remaining risk: evidence and diff review incomplete
- Next action: review before any acceptance

### [2026-08-24] Phase 2B Replacement Candidate (PR #12)
- Recorded PR #10 governance merge in PROJECT_STATUS.md.
- Created and recorded PR #12 as the replacement candidate for Phase 2B, superseding PR #9.
- Current active branch: `codex/phase-2b-source-registration-12955190277775369594`
- Base SHA: `a41b07d7a7dd192c3ae4a277eb4903327883456f`
- Verified CI evidence: GitHub Backend CI run #16 successful on PR #12.
- Updated docs to ensure Phase 2B metadata-registration conflict rejection is thoroughly tested and verified.

### 2026-08-24T08:00:00Z — PR #12 corrective evidence and documentation finalization

- Actor: Jules implementation; ChatGPT/Codex independent remote verification and documentation correction
- Task/phase: Phase 2B ingestion foundation replacement candidate
- Base: `source-data-cleanup@a41b07d7a7dd192c3ae4a277eb4903327883456f`
- Working branch: `codex/phase-2b-source-registration-12955190277775369594`
- PR: [#12](https://github.com/davoodmehraban89/Aram/pull/12)
- Independently reviewed implementation head: `9e90533658e400a51402db673efae9cbd0aa37d1`
- Changed files at reviewed head: `PROJECT_STATUS.md`, `backend/README.md`, `backend/pyproject.toml`, `backend/src/aram_backend/ingestion.py`, `backend/src/aram_backend/ledger_parser.py`, `backend/src/aram_backend/workbook_inspection.py`, `backend/tests/test_ingestion.py`, `backend/tests/test_ledger_parser.py`, `backend/tests/test_workbook_inspection.py`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`
- Regression evidence: exact duplicate remains idempotent; same-year/same-hash conflicts in document type, filename, or both raise `SourceRegistrationError`; each rejection leaves one unchanged original `SourceDocument`
- Reported local verification by Jules: full backend pytest suite, compileall, Alembic upgrade/downgrade round-trip, and `git diff --check` passed; exact pytest count was not independently captured and remains `NOT_VERIFIED`
- GitHub Actions: [Backend CI run #17](https://github.com/davoodmehraban89/Aram/actions/runs/32703999006), `success`
- Artifacts/releases: none
- Protected data: the complete PR filename list contains no canonical XLSX/PDF, `data/`, database, ZIP, EXE, or financial-source file
- Acceptance: `IN_PROGRESS`; Draft and unmerged
- Reviewer: ChatGPT/Codex candidate-requirements review; final acceptance pending
- Remaining risks: final documentation commits require their own CI result; independent acceptance decision is not yet recorded
- Recovery: close PR #12 without merging to leave the accepted branch unchanged
- Next action: independently review the final remote head and record an explicit decision

### 2026-08-24T08:35:40Z — Phase 2B accepted; superseded candidate closed

- Actor: ChatGPT/Codex independent reviewer; repository owner authorization
- Task/phase: Phase 2B ingestion foundation acceptance and post-merge control reconciliation
- Accepted base before merge: `source-data-cleanup@a41b07d7a7dd192c3ae4a277eb4903327883456f`
- Accepted branch after merge: `source-data-cleanup@7b5bd79b760d534dad34b3162f770e838616ebe9`
- Accepted PR: [#12](https://github.com/davoodmehraban89/Aram/pull/12)
- Reviewed PR #12 head: `f7cb6abb7caf3f1c0c28d402ae41b0e3c005a280`
- Merge method and SHA: squash; `7b5bd79b760d534dad34b3162f770e838616ebe9`
- Final PR #12 GitHub Actions: [Backend CI run #21](https://github.com/davoodmehraban89/Aram/actions/runs/32705724028), `success`
- Test evidence: 42 passed, 1 warning; Alembic upgrade/downgrade and compileall succeeded
- Superseded PR: [#9](https://github.com/davoodmehraban89/Aram/pull/9), closed without merge
- Post-merge control branch: `codex/phase-2b-post-merge-record`
- Post-merge control PR: [#13](https://github.com/davoodmehraban89/Aram/pull/13)
- PR #13 base: `source-data-cleanup@7b5bd79b760d534dad34b3162f770e838616ebe9`
- PR #13 changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`
- PR #13 tests / CI / artifacts: documentation-only; no backend workflow triggered; artifacts `NONE`
- Protected data: no application code, tests, workflows, canonical XLSX/PDF, `data/`, database, binary, ZIP, EXE, or financial-source file changed
- Acceptance: PR #12 `VERIFIED_AND_MERGED`; PR #9 closed unmerged; PR #13 `IN_PROGRESS`
- Reviewer: PR #12 independently accepted by ChatGPT/Codex with explicit repository-owner merge authorization; PR #13 review pending
- Recovery: revert merge commit `7b5bd79b760d534dad34b3162f770e838616ebe9` through a separately reviewed rollback PR if Phase 2B must be withdrawn
- Remaining risk: PR #13 must be independently reviewed before its documentation becomes accepted
- Next action: review PR #13, then select the next focused Issue #11 roadmap task

### 2026-08-24T09:29:00Z — Gate 2A implementation candidate prepared

- Actor: ChatGPT/Codex implementation
- Task/phase: Issue #14, Pilot workbook contract and read-only preflight
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Working branch: `codex/gate-2a-pilot-workbook`
- Scope: typed in-memory preflight, reproducible blank workbook generator,
  approved blank template, contract, regression tests, and control records
- Local focused verification: 9 targeted preflight scenarios passed through a
  direct Python harness; compileall succeeded
- Full pytest/Alembic: pending GitHub Backend CI because the automation runtime
  could not install the repository test dependencies from the external package
  index
- Template SHA-256:
  `e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f`
- Protected data: no canonical XLSX/PDF, `data/`, database, financial-source,
  migration, workflow, ZIP, EXE, desktop, or release file changed
- Acceptance: `IN_PROGRESS`; Draft and unmerged
- Remaining risks: full Backend CI and independent diff review are required
- Recovery: close the Draft PR without merge; accepted branch remains unchanged

### 2026-08-24T09:40:00Z — Gate 2A Draft PR and CI verified

- Draft PR: [#15](https://github.com/davoodmehraban89/Aram/pull/15)
- Published head: `8b0431b54392e3c19ae995e2b38bdf08a56a0473`
- Changed files: 9, all within the Issue #14 allowlist
- GitHub Actions: [Backend CI run #23](https://github.com/davoodmehraban89/Aram/actions/runs/32712716962), `success`
- Test evidence: 52 passed, 1 warning; Alembic upgrade/downgrade and compileall succeeded
- PR state: Draft, open, mergeable, and unmerged
- Acceptance: `IN_PROGRESS`; independent diff review and explicit merge decision remain required

### 2026-08-25T06:30:00Z — Post-Gate-2A control reconciliation and stale-work cleanup

- Actor: Codex successor project manager / independent GitHub reviewer; cleanup authorized by repository owner
- Task/phase: reconcile accepted Gate 2A evidence, close its duplicate candidate, and block stale-base Gate 2B work before continuation
- Accepted base: source-data-cleanup@4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4
- Working branch: codex/post-gate2a-control-reconciliation
- PR: [#18](https://github.com/davoodmehraban89/Aram/pull/18), Draft and unmerged
- Initial publication commit: c6eefc26955c694c388371bcfaa96452b1b5f469
- Exact changed files planned/finalized: PROJECT_STATUS.md, docs/PROJECT_LOG.md, docs/handoff/LATEST_HANDOFF.md, docs/handoff/MASTER_RECOVERY_PROMPT.md
- Accepted Gate 2A evidence: [PR #15](https://github.com/davoodmehraban89/Aram/pull/15), reviewed head 74b6a6397a2a2c9199a5c7bcf818bb661b2ebe06, squash merge 4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4
- Final Gate 2A GitHub Actions: [Backend CI run #24](https://github.com/davoodmehraban89/Aram/actions/runs/32712900800), success; 52 passed, 1 warning; Alembic upgrade/downgrade and compileall succeeded
- Pilot template SHA-256 independently recomputed from the accepted GitHub file: e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f
- Superseded duplicate: [PR #16](https://github.com/davoodmehraban89/Aram/pull/16) closed without merge on 2026-08-25 after an evidence comment; it duplicated accepted Gate 2A, was dirty, and recorded incorrect merge SHA 35d45c3f200672a6ef97f13a84cf7c823ecf1bb8
- Blocked candidate: [PR #17](https://github.com/davoodmehraban89/Aram/pull/17), base 7c7533ee87146dc8fc78b46ebf423be55532c7eb, head 4f8648add0e2ed60f01753e979fa3fbe9ccf0f18, open/non-Draft/dirty; its green CI does not prove compatibility with the accepted head
- Tests for PR #18: documentation-only; backend pytest and migration execution are not applicable; final remote diff and changed-file review remain mandatory
- GitHub Actions for PR #18: NOT_VERIFIED at entry creation; documentation-only paths may not trigger Backend CI
- Artifacts/releases: NONE
- Protected data: no application code, workflow, migration, XLSX/PDF, data/, database, financial-source, binary, ZIP, EXE, or release file changed
- Acceptance: IN_PROGRESS; PR #18 is not merged and requires independent final-head review plus explicit repository-owner authorization
- Reviewer: final PR #18 reviewer pending
- Recovery: close PR #18 without merge; accepted branch remains at 4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4
- Remaining risks: branch protection is disabled; PR #17 remains open and stale; Mapping/UI/release work is incomplete
- Next action: independently review Draft PR #18; do not start or merge Gate 2B work before the control decision
