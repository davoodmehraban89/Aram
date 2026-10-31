# Aram — Latest Handoff Prompt

> Durable accepted-state record with persistent role assignments and recovery workflow.
> GitHub remote evidence remains authoritative. Always fetch the live branch head and open PRs before acting; recorded SHAs are verified events, not perpetual current-head claims.

## Accepted repository state

- Repository: davoodmehraban89/Aram
- Canonical branch: source-data-cleanup
- Recorded accepted control event: [PR #18](https://github.com/davoodmehraban89/Aram/pull/18), reviewed head `fcbeb7387218e9ab294318ae462ed59de717fc95`, squash merge `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b` at `2026-08-25T06:46:16Z`.
- Durable post-merge record: [PR #19](https://github.com/davoodmehraban89/Aram/pull/19), reviewed head `b9059592409606a0a4f11a71c30778cff158b6b6`, squash merge `77f9f595ccfe67a87b11024ff0f6143629dba438` at `2026-08-25T06:57:02Z`.
- Earlier accepted work includes PR #1, #4, #6, #8, #10, #12, #13, and #15.
- PR #7, PR #9, PR #16, and PR #17 are closed without merge and contribute no accepted code.
- [Issue #14](https://github.com/davoodmehraban89/Aram/issues/14) is completed. [Issue #11](https://github.com/davoodmehraban89/Aram/issues/11) records Gate 3 as ready for a new focused task definition.
- No user-ready V1 release, tag, ZIP, EXE, or retained release artifact is accepted or proven.

## Accepted Gate 2A evidence

- PR: https://github.com/davoodmehraban89/Aram/pull/15
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Reviewed PR head: `74b6a6397a2a2c9199a5c7bcf818bb661b2ebe06`
- Squash merge: `4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4`
- Final GitHub Actions: https://github.com/davoodmehraban89/Aram/actions/runs/32712900800
- CI conclusion: success; 52 passed, 1 warning; Alembic upgrade/downgrade and compileall succeeded.
- Accepted capabilities: governed Pilot workbook v0.1 contract, approved blank template, reproducible generator, and deterministic read-only in-memory preflight.
- Template path: `samples/Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx`
- Independently recomputed SHA-256: `e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f`
- Protected boundary: PR #15 changed no canonical XLSX/PDF, `data/`, database, financial-source, workflow, migration, desktop/release, ZIP, or EXE path.

## Accepted PR #18 control evidence

- Base: `source-data-cleanup@4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4`
- Reviewed head: `fcbeb7387218e9ab294318ae462ed59de717fc95`
- Squash merge: `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`
- Exact changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Verification: complete remote four-file diff and metadata reviewed; append-only project-log behavior and protected-data boundary confirmed.
- GitHub Actions: none on the reviewed head; documentation-only paths did not trigger Backend CI.
- Artifacts/releases: `NONE`
- Protected boundary: no application code, tests, workflow, migration, dependency, workbook content, financial data, binary, ZIP, EXE, artifact, or release file changed.
- Acceptance authority: Davood explicitly authorized the merge after independent review.

## Accepted PR #19 control evidence

- Base: `source-data-cleanup@f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`
- Reviewed head: `b9059592409606a0a4f11a71c30778cff158b6b6`
- Squash merge: `77f9f595ccfe67a87b11024ff0f6143629dba438`
- Exact changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`
- Verification: complete remote three-file diff, append-only log, whitespace, protected-data boundary, and post-merge accepted-head state passed.
- GitHub Actions: none on the reviewed head; documentation-only paths did not trigger Backend CI.
- Artifacts/releases: `NONE`

## Durable role-based operating model

- Permanent source: `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Decision record: ADR-011 in `docs/DECISION_LOG.md`
- Introduced through: [PR #20](https://github.com/davoodmehraban89/Aram/pull/20)
- Davood is Project Owner and the accounting/product authority.
- ChatGPT chat is Operational Coordinator: recovery, task scoping, implementation prompts, first-pass review, and copy-ready handoffs.
- Jules is the primary Implementation Agent: exact-base focused implementation, tests, Draft PR, and evidence; it never merges its own PR.
- Codex Work is Senior Technical Supervisor, Independent Reviewer, and Authorized Maintainer: technical sequencing, remote evidence review, conflict resolution, exceptional critical fixes, acceptance decisions, and routine merges under standing delegation.
- GitHub is the evidence source of truth.
- Accounting ambiguity, material scope, protected-data changes, releases, destructive actions, credentials, and new external authority remain Davood escalation points.
- A repository mismatch pauses only the affected task without edits; it does not halt the project.

## Closed superseded work

- PR #16 was closed without merge on 2026-08-25.
- It duplicated accepted PR #15, used stale base `7c7533ee87146dc8fc78b46ebf423be55532c7eb`, was dirty, and recorded incorrect merge SHA `35d45c3f200672a6ef97f13a84cf7c823ecf1bb8`.
- No file or claim from PR #16 is accepted.

## Closed Gate 3 / Gate 2B reference

- PR: https://github.com/davoodmehraban89/Aram/pull/17
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Head: `4f8648add0e2ed60f01753e979fa3fbe9ccf0f18`
- Final state: closed without merge on 2026-08-25; its code is not accepted.
- GitHub reports 12 changed files although the PR narrative names only 9.
- Backend CI run #31 succeeded with 51 tests on the stale branch head; that does not prove compatibility with accepted Gate 2A.
- Use PR #17 only as reference. Do not reopen, revive, or merge it.
- Comprehensive Mapping Excel import/export, carry-forward, unknown-account queue, note/sub-note mapping, management UI, reproducible Windows packaging, and end-to-end Pilot acceptance remain unimplemented.

## Governance and release reality

- GitHub remote evidence outranks this record and every agent report.
- The accepted branch is currently unprotected; explicit review discipline is mandatory.
- There are no accepted Git tags or GitHub Releases.
- Canonical financial XLSX/PDF and source data remain protected.
- Green CI on an unmerged PR is not acceptance evidence.
- No Gate 3 implementation candidate is accepted or active.

## Active V1-01 safety-gate candidate

- Verified base: `source-data-cleanup@b1ddee87d31ee73b3a5aeac8f9953d0a604c206a`
- Working branch: `codex/v1-01-safety-gate-hardening`
- Draft PR: [#21](https://github.com/davoodmehraban89/Aram/pull/21)
- Independently reviewed implementation head: `700d800dbd9c657f6bd510faafedcbde4847fafd`.
- Earlier exact-head candidate: `aba10b61c770ce319b1b67d960a4f0a1057e25f6`; [Backend CI #36](https://github.com/davoodmehraban89/Aram/actions/runs/32989551021) succeeded.
- A later documentation-triggered [Backend CI #38](https://github.com/davoodmehraban89/Aram/actions/runs/33015151139) exposed a flaky message-specific reparent assertion: protection fired correctly, but through the equally valid parent-company invariant.
- Stabilized candidate: `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`; the single test assertion now accepts either valid `cannot be mutated` protection message without changing product behavior.
- Latest verified CI: [Backend CI #39](https://github.com/davoodmehraban89/Aram/actions/runs/33015277194), success on `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`; 67 tests passed, migration upgrade/downgrade and compile succeeded.
- Purpose: close the independently reproduced protected-year deletion/mutation and Pilot-preflight false-negative defects before any Mapping/UI expansion.
- Planned changed files: `index.html`, `PROJECT_STATUS.md`, `backend/src/aram_backend/models.py`, `backend/src/aram_backend/pilot_workbook.py`, `backend/tests/test_models.py`, `backend/tests/test_pilot_workbook.py`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`.
- Local evidence at preparation: 67 pytest tests passed; isolated Alembic upgrade/downgrade and compileall passed; focused Ruff and mypy checks passed.
- Protected boundary: no canonical financial data, workbook, PDF, database, financial value, binary, ZIP, EXE, tag, or release is in scope.
- Independent-review decision: code, scope, diff, and protected-data boundary passed. CI #38 later revealed only a nondeterministic error-message assertion; CI #39 passed after the one-line assertion stabilization.
- Status: `IN_PROGRESS`; this durable-document reconciliation records the complete CI sequence. The resulting documentation-only head must be re-fetched and compared with `b3dc8b3a18934ffe63f615e4f650248be21a5f9c` before Ready/Squash Merge.

## Single next action

Publish this requested two-document reconciliation on PR #21 and route the resulting documentation-only head back to the independent reviewer. The reviewer must confirm that only `PROJECT_STATUS.md` and `docs/handoff/LATEST_HANDOFF.md` changed after the CI-verified stabilized head `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`, verify the final workflow result, then Ready/Squash Merge. Do not begin Gate 3 Mapping until V1-01 is accepted.


## 2026-10-31 — current read-only coverage candidate

- Active candidate branch: `codex/aram-readonly-mapping-coverage-20261031`, based directly on accepted SHA `7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- `backend/src/aram_backend/coverage_preview.py` adds fail-closed structural Mapping coverage analysis and explicit non-releasable provenance. See `docs/READONLY_MAPPING_COVERAGE.md`.
- This work is not the full financial statement engine. No company financial values are created or altered.
- Candidate remains unmerged until exact-head CI + independent accounting, QA and security acceptance. Do not infer approval from workbook cells or green unit tests.
- Keep pending PR #59 and other drafts separate from this branch; do not silently merge the unapproved stack.

### 2026-10-30 — PR #60 current candidate evidence

- Read-only mapping coverage preview + safe local CLI at https://github.com/davoodmehraban89/Aram/pull/60.
- Prior CI https://github.com/davoodmehraban89/Aram/actions/runs/41126235147 passed, but subsequent hidden-worksheet protections were committed after that run. Re-run and verify final exact-head CI. Never cite an older green run as a final-head result.
- Protected `data/`, legacy signed statements, original XLSX/PDF, server secrets, source-data-cleanup, releases: unchanged.
- This is only a non-releasable exposure diagnostic; no accounting-signoff, report generation, real IdP, CAS approvals or GUI integration.

## 2026-10-31 — downstream read-only reconciliation work
- Parent work: Draft PR #60, exact SHA `8f0e9e400c63237e00ae6d0b9847a473cb758d6e`.
- Candidate child branch: `codex/aram-reconciliation-review-gate-20261031`.
- Adds strict comparison against explicit per-note closing-balance references; source and reference SHA-256 hashes, bounded Decimal inputs and blocking unmapped/duplicate/inconsistent cases.
- This is NOT a financial-statement calculation, real reconciliation signoff, signed approval, or release. Leave Draft until exact-head CI, independent C1/C2/C3 reviews, and finance-specific policy acceptance.

## 2026-10-31 — BS candidate preview follow-on
- Parent: Draft PR #61, head `736193905d8b041a938e7285610ff207b4cd4487`.
- Child working branch `codex/aram-bs-candidate-statement-20261031` adds pure read-only explicit-policy balance-sheet candidate; docs: `docs/BALANCE_SHEET_CANDIDATE.md`.
- A zero arithmetic difference is **not accounting authorization**, audited sign policy, accepted note disclosure, or a released report. No real company financial source changed.
- Independent C1/C2/C3, accepted parent chain, financial owner review, complete UI/installer and release validation remain pending.

## 2026-10-31 — dependent income-statement candidate
- Current candidate branch: `codex/aram-income-statement-candidate-20261031`, parent unmerged PR #62 SHA `d6d0fc5da47e7209fe21fe96d48548d1489ef8a7`.
- Explicit six-category IS note presentation, exact Decimal bridge, synthetic tests and safe offline CLI. Documentation `docs/INCOME_STATEMENT_CANDIDATE.md`.
- Still **not** an approved P&L report, tax statement, posted financial entry or releasable output. Actual ledger movements, verified finance policies, three independent approvals, GUI integration and Windows installer remain pending.

## 2026-10-31 — trial balance arithmetic diagnostic
- Current branch `codex/aram-trial-balance-diagnostic-20261031` off unmerged PR #63 `5679a2e9feff582b0d0b74bd5a807387879bb358`.
- Synthetic-only, read-only debit/credit turnover and opening/closing equality checks. See `docs/TRIAL_BALANCE_DIAGNOSTIC.md`.
- Not an authenticated trial balance, complete source posting proof or regulatory financial statement. No release, independent C1/C2/C3 approval, GUI or real-ledger validation. Exact SHA CI and reviewer evidence needed before merge.

## 2026-10-31 — statement of changes in equity candidate
- Current development branch `codex/aram-equity-changes-candidate-20261031`, parent unmerged PR #64 `bfdde93bf98383470181b7ee55409e2ab9c45408`.
- Synthetic-only, read-only equity movement preview with explicit sign/category policies, exact opening + movement = closing controls, account trace and offline CLI. See `docs/EQUITY_CHANGES_CANDIDATE.md`.
- Known limitations: one movement class per note/subnote; no automated net-profit tie to P&L; actual source semantics and completeness unverified; no statutory report, C1/C2/C3 approval, UI, installer or release. Verify full CI on final SHA before any merge.

## 2026-10-31 — direct cash flow candidate
- Current branch `codex/aram-cash-flow-direct-candidate-20261031` based on unmerged PR #65 `6dd52d6e098999d22700ba2a7150bedc3846ab1a`.
- Synthetic-only direct cash flow preview from paired cash/counterpart journal lines. Explicit cash-account registry, counterpart activity mapping, source-turnover reconciliation and cash roll-forward. See `docs/CASH_FLOW_DIRECT_CANDIDATE.md`.
- Does not infer activity from aggregate TB; real source transaction completeness, cash-account scope and policy remain unverified. No official statement, C1/C2/C3 approval, GUI, installer or release. Full CI on exact head required.

## 2026-10-31 — direct cash flow exact-head verification
- Cash flow implementation SHA `392ac9e8d2a9806843bb572b8e4032d7e75e9843`, CI [41170694898](https://github.com/davoodmehraban89/Aram/actions/runs/41170694898): 365 tests passed; migration round-trip and compileall passed.
- PR #66 is still Draft. Direct cash flow requires paired source journal lines, cash account scope approval and counterpart activity policies; existing aggregated Pilot workbook alone is insufficient. No official statement, source completeness proof, independent approval, GUI or release.

## 2026-10-31 — five-statement reconciliation gate
- Current branch `codex/aram-cross-statement-controls-20261031`, parent unmerged PR #66 `6d7f949caeb73d3afefb7416608f06452df605e6`.
- Adds typed cross-statement gate for same-source BS/IS/EQ/CF/TB candidates, including P&L↔equity profit, BS equity↔EQ closing, selected BS cash notes↔CF closing and cash-account↔TB account trace. See `docs/CROSS_STATEMENT_RECONCILIATION.md`.
- Synthetic candidate tests only. Still no authenticated source completeness, signed accounting policy, C1/C2/C3 approvals, official exports, GUI or installer. Exact-head CI required.

## 2026-10-31 — cross-statement gate hardening
- Cross-statement control now recomputes from detail: P&L totals from statement bridge, cash-flow categories from classified cash lines, TB totals from all account rows, and cash-account opening/turnover/closing/source-row against TB. Internal transfers are checked from line trace.
- Based on PR #66 `6d7f949caeb73d3afefb7416608f06452df605e6`; exact final-head CI pending. Still no authenticated source completeness, financial approval, C1/C2/C3, official export or release.

## 2026-10-31 — cross-statement exact-head verification
- Cross-statement implementation SHA `34bf411430a2a87d2909c9dc5feb3ab65cb9294a`, CI [41171545629](https://github.com/davoodmehraban89/Aram/actions/runs/41171545629): 390 tests passed; Alembic round-trip and compileall passed.
- PR #67 remains Draft. It is an arithmetic gate only; no source completeness proof, signed financial-owner policy, C1/C2/C3 approval, official report, GUI or installer.


## 2026-10-31 — actual five-statement pipeline integration (verification pending)
- Current branch `codex/aram-five-statement-integration-20261031`, Draft PR #69, based on PR #68.
- New end-to-end synthetic test runs the actual five builders (BS/IS/EQ/CF/TB) on the same immutable XLSX bytes, with BS 100=10+90, IS net 20=EQ profit movement 20, EQ 70+20=90, cash 40+10=50, and balanced TB turnover 60/60. A missing transaction blocks the combined gate.
- Detail hardening: BS/IS line re-aggregation; EQ account/note/component rollforwards tied to TB account rows; TB per-account rollforward; cash line turnover recomputed for each cash account including both sides of internal transfers; shared note-reference snapshot; explicit rejection of forged approval/completeness flags.
- See `docs/CROSS_STATEMENT_RECONCILIATION.md`. Synthetic-only. Exact-head CI and adversarial reviews remain pending. No finance-owner signoff, source completeness, C1/C2/C3 acceptance, official export, GUI, installer or release.


## 2026-10-31 — five-statement integration verification
- PR #69 exact implementation SHA `b669fc29ab8f85a44b57655b23e26d12b705e215` passed [Backend CI 41183115444](https://github.com/davoodmehraban89/Aram/actions/runs/41183115444): 408 tests; Alembic round-trip and compileall passed.
- Three sequential internal engineering passes completed. PR #69 is still Draft/unmerged; no source completeness, authenticated cash scope, finance-owner signoff, independent C1/C2/C3, official export, GUI, installer or release.


## 2026-10-31 — shared-snapshot five-statement orchestrator (verification pending)
- Current branch `codex/aram-five-statement-orchestrator-20261031`, Draft PR #70, based on PR #69.
- New `aram_backend.five_statement_pipeline.build_five_statement_pipeline(...)` freezes input collections, passes the same immutable workbook bytes to all five builders, shares one references tuple across BS/IS/EQ and calls the cross-statement gate. See `docs/FIVE_STATEMENT_PIPELINE.md`.
- Returns a typed nonofficial result with all candidates/findings; blocked upstream candidates remain blocked. Tests now invoke the orchestrator end-to-end. Exact-head CI pending. No filesystem access, DB write, CLI, GUI, installer, approval or release.


## 2026-10-31 — five-statement orchestrator exact-head verification
- PR #70 exact implementation SHA `2b201d350bffecdedbd26b44bd2209e47aa50e3a` passed [Backend CI 41183509414](https://github.com/davoodmehraban89/Aram/actions/runs/41183509414): 409 tests; Alembic round-trip and compileall passed.
- Three internal engineering passes completed. PR #70 is Draft/unmerged; no finance-owner signoff, source completeness, independent C1/C2/C3, official export, GUI, installer or release.


## 2026-10-31 — offline five-statement CLI (verification pending)
- Current branch `codex/aram-five-statement-cli-20261031`, Draft PR #71, based on PR #70.
- Command: `python -m aram_backend.five_statement_pipeline_cli --file <pilot.xlsx> --manifest <pipeline.json>`. Reads bounded local XLSX and strict JSON manifest, invokes the shared-snapshot orchestrator, prints JSON to stdout only. Exit 0 = analyst preview, 3 = blocked candidate, 2 = unsafe/malformed input. See `docs/FIVE_STATEMENT_PIPELINE_CLI.md`.
- Exact-head CI pending. Real manifests contain financial information and must remain local/authorized. No DB write, posting, approval, official export, GUI, installer or release.


## 2026-10-31 — five-statement CLI exact-head verification
- PR #71 exact implementation SHA `3a1d6988fb1f5049681f4668aa14a96321cc93b7` passed [Backend CI 41183945204](https://github.com/davoodmehraban89/Aram/actions/runs/41183945204): 413 tests; Alembic round-trip and compileall passed.
- Internal functional, quality/security and edge/misuse passes completed. PR #71 is Draft/unmerged; real-source completeness, finance-owner approval, independent C1/C2/C3, official export, GUI, installer and release remain open.


## 2026-10-31 — five-statement CLI documentation-inclusive verification
- PR #71 latest head `a5a874b1d227e52c1e70e00edcb8dc5b96a77c6a` passed [CI 41184045992](https://github.com/davoodmehraban89/Aram/actions/runs/41184045992): 413 tests; Alembic round-trip and compileall passed.
- PR #71 remains Draft/unmerged. No real source completeness, finance-owner approval, independent C1/C2/C3, official export, GUI, installer or release.


## 2026-10-31 — synthetic Windows inspection demo (verification pending)
- Current child branch `codex/aram-synthetic-windows-demo-20261031`, parent Draft PR #75 (head `04397f8ad6c329d1f16d0e2d41981f57be43426d`).
- Synthetic XLSX/manifest generator `python -m aram_backend.synthetic_five_statement_demo --output-dir <NEW_FOLDER>`; **never** reads company data or overwrites existing paths. Integration tests share the same fixture definitions.
- Windows EXE CI now bundles the synthetic files and runs `--ui-valid-smoke` on the frozen executable for a real, five-result positive GUI flow. See `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`.
- Exact-head CI and reviews still pending. No C1/C2/C3 approval, real-source completeness, official report, signed installer or release.


## 2026-10-31 — financial figures in Windows pilot (verification pending)
- Branch `codex/aram-windows-statement-figures-20261031`, Draft PR child of #76. New `desktop_five_statement_figures.py` displays 28 exact, read-only, clearly nonofficial statement and reconciliation metrics in Persian, without new financial assumptions. Tk new tab clears on input changes, errors or reset. Windows valid smoke asserts key values.
- Exact final-head CI still required; no source completeness, finance-owner approval, independent C1/C2/C3, signed installer, official export or release.



## 2026-10-31 — Windows statement-detail review (verification pending)
- Current child branch `codex/aram-windows-detail-review-20261031`, Draft PR #78 based on Draft PR #77.
- New `desktop_five_statement_details.py` maps all BS/IS note lines, EQ note and account movements, cash transaction and cash-account reconciliation rows, and TB account details. Persian UI adds search, statement filter, 200-row pages and a 75k fail-closed cap.
- `desktop_five_statement_integrity.py` verifies exact typed candidate/reconciliation objects, all approval flags remain false, common source hash/company/year/reference snapshot, and critical cross-statement ties before desktop figures/details. All displayed monetary fields are validated as bounded Decimals.
- Backend/Windows exact-head CI pending. No real source files, official report, finance owner signoff, signed installer or production release.



## 2026-10-31 — latest Windows detail review exact-head status
- Current child branch `codex/aram-windows-detail-review-20261031`, Draft PR #78, tested SHA `b5b93213e65c02c514180cece8936874577e9954`.
- Backend CI #41229238766: 565 passed; one Windows-only skip on Linux. Windows CI #41229238757: 95 passed; native Tk and frozen EXE verified detail drill-down and paging. Artifact ID 13052698865, 7-day retention.
- Detail UI displays source note lines, EQ movements, CF transactions/cash account roll-forward and TB accounts, with search, statement filter, 200-row paging, 75k cap, source/policy evidence and strict Decimal/provenance checks.
- PR remains Draft/unmerged. No finance owner signoff, real source completeness, independent C1/C2/C3, official export, signed installer or production release.
