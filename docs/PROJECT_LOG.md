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
- Closed reference candidate: [PR #17](https://github.com/davoodmehraban89/Aram/pull/17), base 7c7533ee87146dc8fc78b46ebf423be55532c7eb, head 4f8648add0e2ed60f01753e979fa3fbe9ccf0f18; closed without merge on 2026-08-25 after an evidence comment; its green stale-head CI does not prove compatibility and no content is accepted
- Tests for PR #18: documentation-only; backend pytest and migration execution are not applicable; final remote diff and changed-file review remain mandatory
- GitHub Actions for PR #18: NOT_VERIFIED at entry creation; documentation-only paths may not trigger Backend CI
- Artifacts/releases: NONE
- Protected data: no application code, workflow, migration, XLSX/PDF, data/, database, financial-source, binary, ZIP, EXE, or release file changed
- Acceptance: IN_PROGRESS; PR #18 is not merged and requires independent final-head review plus explicit repository-owner authorization
- Reviewer: final PR #18 reviewer pending
- Issue metadata: [Issue #14](https://github.com/davoodmehraban89/Aram/issues/14) closed as completed with verified PR #15 evidence; [Issue #11](https://github.com/davoodmehraban89/Aram/issues/11) updated to mark Gate 2 accepted and Gate 3 blocked pending PR #18
- Recovery: close PR #18 without merge; accepted branch remains at 4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4
- Remaining risks: branch protection is disabled; PR #17 reference work remains unaccepted; Mapping/UI/release work is incomplete
- Next action: independently review Draft PR #18; do not start or merge Gate 2B work before the control decision

### 2026-08-25T06:46:16Z — PR #18 accepted; time-bound candidate record reconciled

- Actor: ChatGPT/Codex independent reviewer; repository owner explicit authorization
- Task/phase: accept the post-Gate-2A control reconciliation and correct the preceding time-bound candidate snapshot
- Accepted base before merge: `source-data-cleanup@4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4`
- Working branch: `codex/post-gate2a-control-reconciliation`
- PR: [#18](https://github.com/davoodmehraban89/Aram/pull/18)
- Reviewed PR head: `fcbeb7387218e9ab294318ae462ed59de717fc95`
- Merge method and SHA: squash; `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`
- Exact changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Tests: documentation-only; backend pytest, migration execution, and compileall were not applicable
- GitHub Actions: no workflow run was associated with reviewed head `fcbeb7387218e9ab294318ae462ed59de717fc95`; documentation-only paths did not trigger Backend CI
- Artifacts/releases: `NONE`
- Protected data: no application code, tests, workflow, migration, dependency, XLSX/PDF, `data/`, database, financial-source, binary, ZIP, EXE, artifact, or release file changed
- Acceptance: `VERIFIED_AND_MERGED`
- Reviewer: ChatGPT/Codex after full remote four-file diff review and Davood's explicit merge authorization
- Correction note: the preceding 2026-08-25T06:30:00Z entry is preserved as an accurate historical candidate snapshot; its Draft/unmerged and pending-review statements are no longer current
- Issue metadata: [Issue #11](https://github.com/davoodmehraban89/Aram/issues/11) was reconciled after the merge; Gate 3 is ready for a new focused task definition, while closed PR #17 remains reference-only
- Recovery: revert merge commit `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b` through a separately reviewed rollback PR if the accepted control reconciliation must be withdrawn
- Remaining risks: the accepted branch is unprotected; Mapping, note/sub-note workflow/UI, reproducible Windows packaging, and end-to-end Pilot acceptance remain incomplete
- Next action: fetch the live accepted head and define one new focused Gate 3 / Gate 2B Mapping task; do not revive or merge PR #17

### 2026-08-25T07:37:08Z — Role-based operating model prepared

- Actor: project manager / repository maintainer; requested by Davood
- Task/phase: record the complete Aram responsibility model in the permanent recovery prompt
- Base: `source-data-cleanup@77f9f595ccfe67a87b11024ff0f6143629dba438`
- Working branch: `governance/role-based-operating-model`
- PR: [#20](https://github.com/davoodmehraban89/Aram/pull/20)
- Published implementation head before required control-record update: `92f6e096d3471bb5de1fe876066eedee5ab8bcf9`
- Intended final changed files: `PROJECT_STATUS.md`, `docs/DECISION_LOG.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Governance change: define Davood as Project Owner, ChatGPT chat as Operational Coordinator, Jules as primary Implementation Agent, Codex Work as Senior Technical Supervisor / Independent Reviewer / Authorized Maintainer, and GitHub as the evidence source of truth
- Authority change: record standing delegation for routine technical review and merge actions after evidence gates, while retaining Davood escalation for accounting ambiguity, material scope, protected-data, release, destructive, credential, and external-authority decisions
- Clarification: a repository mismatch pauses only the affected task without edits and does not halt the project
- Tests: documentation-only; backend pytest, migrations, and compileall are not applicable; final remote content, diff, whitespace, link, and consistency checks are required
- GitHub Actions at entry creation: `NOT_VERIFIED`; documentation-only paths may not trigger Backend CI
- Artifacts/releases: `NONE`
- Protected data: no application code, test, workflow, migration, dependency, XLSX/PDF, `data/`, database, financial-source, binary, ZIP, EXE, artifact, or release file is in scope
- Acceptance at entry creation: `IN_PROGRESS`; this is a historical preparation record and the live PR state remains authoritative
- Reviewer at entry creation: pending final-head independent remote review
- Recovery: close PR #20 without merge; the accepted branch remains at `77f9f595ccfe67a87b11024ff0f6143629dba438`
- Remaining risks: the accepted branch is unprotected; role assignments do not replace evidence gates; Gate 3 Mapping and all later V1 gates remain incomplete
- Next action: finish the five-file remote candidate, independently review PR #20, and record one acceptance decision

### 2026-08-26T15:36:29Z — V1-01 safety-gate hardening prepared

- Actor: Codex Work authorized maintainer / implementation agent for the critical fix
- Task/phase: V1-01 safety-gate hardening before Gate 3 Mapping
- Base: `source-data-cleanup@b1ddee87d31ee73b3a5aeac8f9953d0a604c206a`
- Working branch: `codex/v1-01-safety-gate-hardening`
- PR: Draft [#21](https://github.com/davoodmehraban89/Aram/pull/21)
- Initial implementation commit SHA: `6d774e5dd7afb00b04e523ba255aeee4f13bfccc`; final reviewed head remains remote-state dependent
- Exact planned changed files: `index.html`, `PROJECT_STATUS.md`, `backend/src/aram_backend/models.py`, `backend/src/aram_backend/pilot_workbook.py`, `backend/tests/test_models.py`, `backend/tests/test_pilot_workbook.py`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`
- Implementation: prevent approved/locked fiscal-year identity mutation and deletion; prevent parent-company mutation/deletion when protected years exist; reject targetless, hierarchy-invalid, formula-code, review-evidence-deficient, and closing-delta-mismatched Pilot rows; replace the disconnected hard-coded root UI with an explicit quarantine page
- Local tests: `cd backend && .venv/bin/pytest -q` -> 67 passed, 1 third-party deprecation warning
- Focused static checks: `.venv/bin/ruff check src/aram_backend/models.py src/aram_backend/pilot_workbook.py` -> passed; `.venv/bin/mypy src/aram_backend/models.py src/aram_backend/pilot_workbook.py` -> passed
- Migration / compile: isolated SQLite `alembic upgrade head` and `alembic downgrade base` passed; `python -m compileall -q src tests scripts` passed
- Adversarial verification: the previously accepted targetless/`account_level=99`/`closing_delta=999` workbook is rejected; locked-year identity mutation and deletion are blocked
- GitHub Actions: pending for Draft PR #21
- Artifacts/releases: `NONE`
- Protected data: no canonical XLSX/PDF, `data/`, database, financial-source value, ZIP, EXE, tag, or release is changed
- Acceptance: `IN_PROGRESS`; implementation author must not merge this PR
- Reviewer: independent reviewer pending
- Recovery: close the candidate PR without merge; accepted branch remains at the recorded base
- Remaining risks: comprehensive Mapping, note/sub-note workflow, real Pilot UI/output, Windows packaging, and user acceptance remain incomplete
- Next action: publish the focused PR and obtain independent remote review after CI


### 2026-10-31 — read-only Mapping coverage proposal (unmerged)

- Actor: ChatGPT engineering implementation.
- Accepted base: `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- Working branch: `codex/aram-readonly-mapping-coverage-20261031`.
- Scope: new `backend/src/aram_backend/coverage_preview.py`, synthetic regression tests, `docs/READONLY_MAPPING_COVERAGE.md`, branch-local control records.
- Formal independent approval, owner sign-off, production artifact and release: **NONE**.
- Protected canonical `data/` XLSX/PDF, sample templates, DB, external credentials: unchanged.
- Acceptance: **NOT MERGED / IN_PROGRESS**. Exact CI/PR references must be appended after fresh remote verification.
- Next: verify exact-head CI, review security and financial semantics and keep Draft until independent acceptance.

### 2026-10-30T20:50Z — PR #60 integration and adversarial follow-up

- Draft PR: https://github.com/davoodmehraban89/Aram/pull/60; accepted base SHA `7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- Exact proposed paths: `PROJECT_STATUS.md`, `backend/src/aram_backend/coverage_preview.py`, `backend/src/aram_backend/coverage_preview_cli.py`, `backend/tests/test_coverage_preview.py`, `backend/tests/test_coverage_preview_cli.py`, `docs/PROJECT_LOG.md`, `docs/READONLY_MAPPING_COVERAGE.md`, `docs/handoff/LATEST_HANDOFF.md`.
- First actual CI run https://github.com/davoodmehraban89/Aram/actions/runs/41125963031 failed one assertion that expected a specific rejection layer for malformed merged cells. The workbook was rejected safely by existing preflight.
- Corrected test and verified a later exact-head CI: https://github.com/davoodmehraban89/Aram/actions/runs/41126115327 (success); subsequent CLI CI https://github.com/davoodmehraban89/Aram/actions/runs/41126235147 (success).
- Additional security review found that hidden auxiliary and unexpected sheets were not all checked; added fail-closed validation and two regression tests. **The final revised head requires another exact-head CI result before acceptance.**
- Formal C1/C2/C3 independent approvals: NONE. Release artifact: NONE. No real finance data, canonical files, production DB or accepted branch modified. Draft only, no merge.
