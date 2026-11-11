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


## 2026-11-10 — Financial statement reconciliation snapshot (1402–1404)

- Accepted base at task start: source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914.
- Working branch: docs/financial-statement-reconciliation-1402-1404-20261110.
- Read-only primary statement reconciliation: 66 arithmetic checks PASS and 3 closing-cash cross-statement checks PASS.
- 1404 Note 22 restated 1402/1403 comparative figures reconcile to the presented financial statements.
- Open item FS-1403-EQ-01: the 1403 equity statement appears to repeat a 43,241,509 million Rial prior-period correction in its opening balance, although the 1402 closing balance already includes it and the 1403 closing row does not carry the repeated adjustment.
- Open item FS-1404-CF-01: 12,556 million Rial FX effect ties mathematically to cash closing; detailed source support / note cross-reference is pending.
- Open item FS-1404-CF-02: +1/-1 million Rial 1404 comparative cash-flow presentation differences offset and have no net cash effect.
- 1404 auditor PDF is image-only in extraction; auditor opinion wording remains unverified.
- Owner-confirmed exclusion rule: ignore auxiliary errors only when outside official statement/note use and related to zero-closing or proven offset accounts; preserve all source rows. Never auto-net an account based on amount equality alone.
- All ten canonical source files SHA-256 hashed; no canonical data, ledger row, Mapping row, database, or code changed.
- Detailed evidence: docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md.
- Status: PRESENT_BUT_UNVERIFIED; independent finance and technical review pending.
- Draft PR: https://github.com/davoodmehraban89/Aram/pull/90, latest verified head at publication update 0213f049dd0530f5660e8a57deb574deb61c75f5, base source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914. Not merged.
- Next action: independent review of PR #90 and accounting disposition of the open equity / FX support items; then continue note-level and ledger-level reconciliation. Do not merge this candidate.


## 2026-11-10 — PR #90 current-head note

- PR #90 remains Draft / open / unmerged.
- The remote head was verified as 2d4eba9c1fc0fd0a89c550651b9a1c7ea138b015 immediately before this control-record update; the live GitHub PR metadata is authoritative for the subsequent control-record commit.
- The latest commit had zero GitHub check-runs; no workflow was observed for this documentation-only PR.
- No source data changed. The PR contains four documentation files only.
- Next action remains independent review and accounting-owner disposition; do not merge.


## 2026-11-10 — Control-account pair verification update

- Verified year-separated entity-level closing balance pairs in source_1404.xlsx:
  - 1403: 8708 = -67,397,848,445,282 Rials; 8709 = +67,397,848,445,282 Rials.
  - 1404: 8708 = -9,683,034,125,526 Rials; 8709 = +9,683,034,125,526 Rials.
  - 1403: 8718 = -10,330,082,681,061 Rials; 8719 = +10,330,082,681,061 Rials.
  - 1404: 8718 = -4,452,935,519,939 Rials; 8719 = +4,452,935,519,939 Rials.
- All four accounts map to Note 12-1 / employees (advances), type O. Each pair nets to zero separately in each fiscal year.
- T1 dimension mismatches exist for some groups; do not net by T1. Exclude only the pair's net effect at the full reporting-entity level, retaining all ledger rows and drill-down.
- Detailed evidence: docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md, section 9.
- Account 8161 unmapped exposure remains separate and is not excluded.
- PR #90 remains Draft / open / unmerged. Next action: independent review and continue note/ledger reconciliation.


## 2026-11-10 — Note-level reconciliation and note-reference audit

- Accepted base: source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914.
- Working branch: docs/financial-statement-reconciliation-1402-1404-20261110.
- Draft PR: #90; open, not merged.
- The 1404 primary Income Statement notes 5–9 tie to the statement amounts; Note 20-3 ties to income-tax expense.
- The 1404 asset side ties line-by-line to Notes 10–15; total assets = 733,743,718 million Rials.
- The 1404 liability/equity side ties to Notes 16–21; total liabilities = 917,629,178, equity = -183,885,460, and liabilities plus equity = 733,743,718 million Rials.
- Note 9-3 identifies the 12,556 million Rial FX effect and cites NIGC letter No. 1830 dated 1405/01/16. Detailed rate-calculation reperformance remains outside this pass.
- New open issue: FS-1403/1404-NOTE-REF-01. The 1403/1404 Statement of Financial Position retains note references 17–22 that lag actual note-page headings after the separate 1402 Note 17 capital-in-progress section disappears. Amounts tie when matched to content; do not alter source workbooks.
- NOTE_CATALOG.md and NOTE_TO_SHEET_MATRIX.md now use year-aware note numbering and actual physical sheet names. Multiple notes can share one sheet; a note can span several sheets.
- FS-1403-EQ-01 remains open; FS-1404-CF-02 remains a +1/-1 million Rial comparative cash-flow difference with no net cash effect; 1404 auditor opinion wording remains unverified.
- Owner-confirmed rule: exclude only non-presented auxiliary errors and zero-closing / proven-offset accounts from statement calculations; preserve all source rows and drill-downs.
- Exact changed files: NOTE_CATALOG.md; NOTE_TO_SHEET_MATRIX.md; PROJECT_STATUS.md; docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md; docs/PROJECT_LOG.md; docs/handoff/LATEST_HANDOFF.md.
- git diff --check passed. The data/ path diff is empty.
- No canonical XLSX/PDF, ledger row, Mapping row, database, code or financial value changed.
- Next action: publish the documentation update to Draft PR #90, verify remote head/checks, then route it to an independent reviewer. Do not merge.


## 2026-11-11 — 1402/1403 note-level tie-out extension

- Draft PR: #90; branch docs/financial-statement-reconciliation-1402-1404-20261110; base source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914.
- 1402 Income Statement Notes 5–9 and 1403 Income Statement Notes 5–9 / 20-3 were checked against actual note-page cells and match.
- 1402 Statement of Financial Position lines tie to actual Notes 10–22; 1403 asset lines tie to Notes 10–15 and liability/tax/advance lines tie to actual printed Notes 18–21.
- Confirmed presentation drift: 1403/1404 statement references 17–22 lag printed note headings after the 1402 capital-in-progress Note 17 is absent as a standalone disclosure. Amounts match actual note content; source workbooks remain unchanged.
- New issue FS-1402/1403-CF-FX-REF-01: 1403 cash-flow FX amount 4,403 appears in Note 9-4 while statement reference is 9-5; 1402 amount 819 appears on Note 9 page but sub-note identifier is unconfirmed.
- Initial 1402/1404 auditor report pages show emphasis-of-matter paragraphs; complete report and opinion review remains outstanding. 1403 PDF reader returned no page content.
- FS-1403-EQ-01 remains open. No source XLSX/PDF, ledger row, Mapping row, database, code or financial value changed.
- Status: PRESENT_BUT_UNVERIFIED. PR #90 remains Draft/open/unmerged; no merge.
- Next action: accounting-owner disposition of FS-1403-EQ-01 and FS-1402/1403-CF-FX-REF-01, plus complete auditor report OCR/review.


## 2026-11-11 — FS-1403-EQ-01 arithmetic evidence

- The 1403 equity rollforward is internally inconsistent by exactly 43,241,509 million Rials: using its restated opening balance implies closing equity -82,191,049, while the reported closing is -38,949,540.
- The reported closing amount is reproduced from the pre-adjustment opening balance, proving the displayed opening correction is not carried through.
- Accounting owner must decide whether the opening adjustment is repeated or the comparative closing should be restated. No official workbook change is authorized.


## 2026-11-11 — Budget Notes 36–39 reconciliation

- Notes 36/37 actuals for 1402–1404 tie to primary statement revenue, expense and profit/loss values.
- Note 39 actual resources equal actual uses in all years: 47,443,159 / 61,677,400 / 71,738,067 million Rials.
- 1404 revenue is 13.98% below revised budget and current expenses are 13.46% above. Cost of services is 84.1% above revised budget while distribution/administrative/general expenses are 53.9% below; Note 38 identifies traditional allocation as a source of artificial variance.
- BUDGET-1403/1404-N36-37-APPROVED-01: original-budget cells #REF! in 1403/1404; actual and revised columns remain reconcilable.
- BUDGET-1404-N39-UNIT-01: 1404 Note 39 original-budget column E mixes Rial-scale and million-Rial values and has #REF! in E9/E16; actual/revised resource-use totals still tie.
- Zero/zero ratio #DIV/0! cells are excluded because no amount or total is affected.
- No canonical workbook/PDF or financial value modified. Accounting/budget-owner disposition required for original-budget disclosure anomalies.
