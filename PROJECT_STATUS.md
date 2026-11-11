# Aram Project Status

> Canonical status entry point. Update this file in every meaningful pull request. Always fetch the live accepted-branch head before acting; a committed snapshot is not a substitute for GitHub remote evidence.

## Repository baseline

- Repository: [davoodmehraban89/Aram](https://github.com/davoodmehraban89/Aram)
- Accepted branch: source-data-cleanup
- Recorded accepted control event: [PR #18](https://github.com/davoodmehraban89/Aram/pull/18), reviewed head `fcbeb7387218e9ab294318ae462ed59de717fc95`, squash merge [f213d321ff4cd7d3d6fa65ba78dc48f090ee846b](https://github.com/davoodmehraban89/Aram/commit/f213d321ff4cd7d3d6fa65ba78dc48f090ee846b)
- Durable post-merge acceptance record: [PR #19](https://github.com/davoodmehraban89/Aram/pull/19), reviewed head `b9059592409606a0a4f11a71c30778cff158b6b6`, squash merge [77f9f595ccfe67a87b11024ff0f6143629dba438](https://github.com/davoodmehraban89/Aram/commit/77f9f595ccfe67a87b11024ff0f6143629dba438)
- Before starting new work, fetch the live `source-data-cleanup` head; this record intentionally avoids a self-referential current-head claim
- Product objective: a controlled, auditable accounting and financial-statement workflow that preserves canonical source data.

## Status vocabulary

| State | Meaning |
|---|---|
| VERIFIED_AND_MERGED | Present on the accepted branch with Git evidence. |
| VERIFIED_BUT_UNMERGED | Present in a remote commit or PR, but not accepted. |
| PRESENT_BUT_UNVERIFIED | Present, but required tests or evidence are missing. |
| CLAIMED_BUT_NOT_PROVEN | Reported by an actor, with no sufficient GitHub evidence. |
| NOT_IMPLEMENTED | Required capability is absent. |
| IN_PROGRESS | Work is in an open PR and is not accepted. |
| BLOCKED | Work cannot proceed until the recorded blocker is resolved. |

## Verified state

| Area | State | Evidence / note |
|---|---|---|
| Phase 1B-1 source inventory | VERIFIED_AND_MERGED | [PR #1](https://github.com/davoodmehraban89/Aram/pull/1) |
| Phase 1B-2 audit corrections | VERIFIED_AND_MERGED | [PR #4](https://github.com/davoodmehraban89/Aram/pull/4) |
| Phase 2A backend foundation | VERIFIED_AND_MERGED | [PR #6](https://github.com/davoodmehraban89/Aram/pull/6) |
| One-file model refactor | VERIFIED_AND_MERGED | [PR #8](https://github.com/davoodmehraban89/Aram/pull/8) |
| Project-control foundation | VERIFIED_AND_MERGED | [PR #10](https://github.com/davoodmehraban89/Aram/pull/10) |
| Phase 2B ingestion foundation | VERIFIED_AND_MERGED | [PR #12](https://github.com/davoodmehraban89/Aram/pull/12), squash merge 7b5bd79b760d534dad34b3162f770e838616ebe9 |
| Phase 2B control reconciliation | VERIFIED_AND_MERGED | [PR #13](https://github.com/davoodmehraban89/Aram/pull/13), squash merge 7c7533ee87146dc8fc78b46ebf423be55532c7eb |
| Gate 2A Pilot workbook contract/preflight | VERIFIED_AND_MERGED | [PR #15](https://github.com/davoodmehraban89/Aram/pull/15), reviewed head 74b6a6397a2a2c9199a5c7bcf818bb661b2ebe06, squash merge 4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4, [Backend CI #24](https://github.com/davoodmehraban89/Aram/actions/runs/32712900800) |
| V1-01 safety-gate hardening | IN_PROGRESS | Draft [PR #21](https://github.com/davoodmehraban89/Aram/pull/21) from exact base `b1ddee87d31ee73b3a5aeac8f9953d0a604c206a`; independently reviewed implementation head `700d800dbd9c657f6bd510faafedcbde4847fafd`; CI-verified stabilized candidate `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`; [Backend CI #39](https://github.com/davoodmehraban89/Aram/actions/runs/33015277194) succeeded with 67 tests, migration round-trip, and compile after broadening one reparent-rejection assertion to accept either valid protection message; code, scope, and protected-data boundary remain unchanged; final independent acceptance is pending this durable-document reconciliation |
| Post-Gate-2A control reconciliation | VERIFIED_AND_MERGED | [PR #18](https://github.com/davoodmehraban89/Aram/pull/18), reviewed head `fcbeb7387218e9ab294318ae462ed59de717fc95`, squash merge `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`; documentation only |
| Durable post-merge acceptance record | VERIFIED_AND_MERGED | [PR #19](https://github.com/davoodmehraban89/Aram/pull/19), reviewed head `b9059592409606a0a4f11a71c30778cff158b6b6`, squash merge `77f9f595ccfe67a87b11024ff0f6143629dba438`; documentation only |
| Role-based project operating model | VERIFIED_AND_MERGED | Permanent responsibilities and current assignments are defined in `docs/handoff/MASTER_RECOVERY_PROMPT.md` and ADR-011; introduced through [PR #20](https://github.com/davoodmehraban89/Aram/pull/20) |
| Parallel V1 prototype | VERIFIED_BUT_UNMERGED | Closed, unmerged [PR #7](https://github.com/davoodmehraban89/Aram/pull/7); reference/recovery source only |
| Superseded Phase 2B candidate | VERIFIED_BUT_UNMERGED | Closed, unmerged [PR #9](https://github.com/davoodmehraban89/Aram/pull/9) |
| Duplicate Gate 2A candidate | VERIFIED_BUT_UNMERGED | [PR #16](https://github.com/davoodmehraban89/Aram/pull/16) closed without merge on 2026-08-25; no content accepted |
| Gate 2B Mapping foundation candidate | VERIFIED_BUT_UNMERGED | [PR #17](https://github.com/davoodmehraban89/Aram/pull/17) closed without merge on 2026-08-25; stale-base reference only; no content accepted |
| Official V1 release | NOT_IMPLEMENTED | No accepted tag, release, retained release artifact, ZIP, or EXE |
| Comprehensive Mapping Excel import/export | NOT_IMPLEMENTED | Mandatory before V1 acceptance |
| Unknown-account queue and mapping carry-forward | NOT_IMPLEMENTED | Mandatory before V1 acceptance |
| Note and sub-note mapping workflow/UI | NOT_IMPLEMENTED | Mandatory before V1 acceptance |
| Minimal Pilot application and reviewable output | NOT_IMPLEMENTED | Required before packaging |
| Reproducible Windows package and clean-environment test | NOT_IMPLEMENTED | Required before V1 acceptance |

## Accepted product capabilities

- Read-only source inventory and workbook audit evidence.
- Persistent backend/data-model foundation with fiscal-year mutation controls.
- Metadata-only source registration, structural XLSX inspection, and typed in-memory ledger parsing.
- Governed Pilot workbook v0.1 contract, reproducible blank template generator, and deterministic read-only preflight.
- Approved Pilot template path: samples/Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx.
- Independently verified template SHA-256: e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f.

The accepted branch does not include PR #7 desktop/release work, PR #16 alternate Pilot implementation, or PR #17 Mapping implementation. Green CI on an unmerged stale-base PR is not acceptance evidence.

## Current risks and blockers

- The accepted branch is not protected by GitHub branch protection.
- The accepted branch still permits direct identity mutation/deletion of approved or locked fiscal years and parent-company deletion; the V1-01 candidate fixes this but is not accepted yet.
- The accepted Pilot preflight can still accept targetless or structurally invalid mappings and can ignore a declared closing-delta mismatch; the V1-01 candidate fixes this but is not accepted yet.
- The accepted root `index.html` is still a disconnected hard-coded prototype; the V1-01 candidate replaces it with an explicit quarantine page.
- PR #17 was closed without merge; its stale-base 12-file diff is reference material only, and its narrative listed only 9 files.
- PR #17 CI was green on its own stale head, but compatibility with accepted Gate 2A was never proven.
- Binary execution, release provenance, and clean Windows verification do not exist.
- Mapping, notes/sub-notes, Pilot UI, and end-to-end user acceptance remain incomplete.

## Next approved action

1. Publish this two-file durable-document reconciliation on Draft PR #21; [Backend CI #39](https://github.com/davoodmehraban89/Aram/actions/runs/33015277194) succeeded on stabilized candidate `b3dc8b3a18934ffe63f615e4f650248be21a5f9c` with 67 tests, migration round-trip, and compile.
2. The independent reviewer re-fetches the resulting documentation-only head, confirms that its comparison with `b3dc8b3a18934ffe63f615e4f650248be21a5f9c` changes only `PROJECT_STATUS.md` and `docs/handoff/LATEST_HANDOFF.md`, verifies the final workflow result, then marks the PR ready and squash-merges it.
3. Only after V1-01 is accepted, start the first focused Gate 3 Mapping import/persistence task from the new accepted head.

## Control documents

- [Project log](docs/PROJECT_LOG.md)
- [Decision log](docs/DECISION_LOG.md)
- [Acceptance policy](docs/ACCEPTANCE_POLICY.md)
- [Jules task template](docs/JULES_TASK_TEMPLATE.md)
- [Master recovery prompt](docs/handoff/MASTER_RECOVERY_PROMPT.md)
- [Latest handoff snapshot](docs/handoff/LATEST_HANDOFF.md)
- [Saveable ChatGPT bootstrap prompt](docs/handoff/CHATGPT_BOOTSTRAP_PROMPT.txt)


## 2026-11-10 — Financial statement reconciliation (1402–1404)

- Status: PRESENT_BUT_UNVERIFIED; statement arithmetic is reconciled, but independent accounting sign-off is pending.
- Read-only review: 66 primary-statement arithmetic checks plus 3 cash-flow-to-balance-sheet closing-cash checks passed.
- 1404 Note 22 restatement of 1402/1403 comparative figures reconciles to the 1404 statements.
- Open accounting presentation item: 1403 Statement of Changes in Equity appears to repeat the 43,241,509 million Rial prior-period correction in its opening-balance section while its closing balance does not carry that repeated adjustment. See docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md, FS-1403-EQ-01.
- Open support item: 1404 cash-flow FX effect of 12,556 million Rials ties mathematically to closing cash; separate support / note cross-reference not yet identified.
- 1404 comparative cash-flow operating/investing lines differ from 1403 current figures by +1/-1 million Rials, with no net cash effect.
- Owner-confirmed rule: ignore only irrelevant auxiliary errors and zero-closing / proven offset accounts in statement calculations; preserve original source rows. Do not suppress all errors or auto-net accounts without evidence.
- All ten canonical source files were SHA-256 hashed. No source file, database, financial value, code, or Mapping row was modified.
- Draft PR: https://github.com/davoodmehraban89/Aram/pull/90 (base 7dc864fd032f0c4ae4d650d89304a01286a6d914; see live PR metadata for current head). Not merged; independent review pending.
- Next action: independent review of PR #90 and accounting disposition of FS-1403-EQ-01 / FS-1404-CF-01; continue note-level and ledger-level reconciliation under the documented exclusion rule.


## 2026-11-10 — Control-account pair verification

- Read-only aggregation of source_1404.xlsx by fiscal year confirms two owner-identified control-account pairs with exactly offsetting entity-level closing balances: 8708/8709 and 8718/8719.
- Each account in both pairs maps to the same Note 12-1 sub-note (employees / advances), type O.
- 1403 and 1404 pair totals each net to exactly zero independently.
- T1-level exceptions remain: 8708/8709 has 4 unmatched T1 groups in 1403 and 2 in 1404; 8718/8719 has 6 in 1403 and none in 1404. Netting is therefore approved only at the full reporting-entity level, not per T1 subgroup.
- Preserve all source rows, turnovers, mappings and drill-downs. Exclude only the combined net effect from statement totals.
- Evidence and amounts are recorded in docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md, section 9.


## 2026-11-10 — Note-level reconciliation and year-aware note map

- Expanded read-only reconciliation on Draft PR #90. The 1404 income-statement notes 5–9 tie to the primary statement; all seven asset-side balance-sheet lines tie to Notes 10–15; liability/equity lines tie to Notes 16–21 when matched to actual note-page headings.
- 1404 total assets 733,743,718; total liabilities 917,629,178; equity -183,885,460; liabilities plus equity equal assets.
- Note 9-3 explicitly identifies the 12,556 million Rial exchange-rate effect and cites NIGC letter No. 1830 dated 1405/01/16. The earlier no-note-reference finding is superseded; detailed rate-calculation reperformance remains outside this pass.
- New issue FS-1403/1404-NOTE-REF-01: 1403/1404 balance-sheet note references 17–22 lag the actual note-page headings after the separate Note 17 capital-in-progress section disappears. Amounts tie when matched to actual note content; source workbook is not modified.
- NOTE_CATALOG.md and NOTE_TO_SHEET_MATRIX.md now record year-aware note numbering and actual physical sheet names. Physical sheet names are not logical note IDs; multiple notes can share a sheet and one note can span sheets.
- FS-1403-EQ-01 remains open. FS-1404-CF-02 remains a +1/-1 million Rial comparative cash-flow presentation difference with no net cash effect. The 1404 auditor PDF opinion wording remains unverified due image-only extraction.
- Owner-confirmed exclusion rule remains in force: ignore only non-presented auxiliary errors and zero-closing / proven-offset accounts in statement calculations; preserve every source row.
- Draft PR: https://github.com/davoodmehraban89/Aram/pull/90. Base source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914; not merged; independent review pending.
- No canonical workbook/PDF, ledger row, Mapping row, database, code, or financial value was modified.
- Next action: independent review of the expanded documentation and continued read-only reconciliation of remaining 1402/1403 note amounts and relevant ledger ties.


## 2026-11-11 — 1402/1403 note-level reconciliation extension

- Extended direct note-page amount tie-outs to 1402 and 1403 Income Statements and Statements of Financial Position; all listed numeric statement amounts match the actual note-page cells or narrative disclosures.
- 1402 income statement Notes 5–9 match; 1403 income statement Notes 5–9 and Note 20-3 tax expense match.
- 1402 asset-side and liability-side lines match the year-specific Notes 10–22. 1403 asset-side lines match Notes 10–15; liabilities and tax/advances match the actual printed Notes 18–21, despite the statement's stale references.
- Confirmed year-aware note drift: after the standalone 1402 Note 17 capital-in-progress disclosure disappears, 1403/1404 printed Note 17 is legal reserve, Note 18 payables, Note 19 employee benefits, Note 20 tax, and Note 21 advances. Statement references 17–22 were not consistently updated.
- New open issue FS-1402/1403-CF-FX-REF-01: 1403 cash-flow FX amount 4,403 appears in Note 9-4 while the statement points to 9-5; 1402 FX amount 819 appears on the Note 9 page but its sub-note identifier is not yet confirmed. 1404 FX support remains identified in Note 9-3.
- Initial visual inspection of 1402/1404 auditor report pages found emphasis-of-matter paragraphs; this is not, by itself, a modified opinion. The 1403 PDF reader returned no page content. Full auditor report OCR/review remains outstanding.
- Owner-confirmed exclusion rule applied: irrelevant auxiliary errors are ignored only when they do not feed official statement/note values; zero-balance / proven offset control accounts are excluded from statement totals only at the evidenced aggregation level. All source rows and workbooks remain preserved.
- No canonical XLSX/PDF, ledger row, Mapping row, database, application code, or financial value was modified.
- Evidence: docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md, section 13; NOTE_TO_STATEMENT_MATRIX.md; NOTE_CATALOG.md.
- PR #90 remains Draft/open/unmerged; independent review pending. Do not merge.

## 2026-11-11 — Account 8161 unmapped exposure refinement

- 1403: 61 unmapped rows; 41 zero-balance, 20 non-zero; net statement-balance exposure 144,125,670,091 Rials.
- 1404: 49 unmapped rows; 45 zero-balance, 4 non-zero; net statement-balance exposure 52,782,248,710 Rials.
- Combined: 110 rows; 86 zero-balance and 24 non-zero; net exposure 196,907,918,801 Rials.
- Seven distinct non-zero mapping keys are absent from the current 8161 Mapping population. All 24 non-zero source rows carry consistent Note 10/13 IDs in source-ledger column A; see report section 15.3.
- Open item MAP-8161-01: confirm the seven non-zero mapping keys, then rerun all mapping counts. Do not exclude 8161 or infer a netting counterpart.
- No source ledger, mapping workbook, statement or financial value changed.
- Next action: accounting-owner disposition of FS-1403-EQ-01 and FS-1402/1403-CF-FX-REF-01, then complete OCR review of auditor reports.


## 2026-11-11 — FS-1403-EQ-01 rollforward reperformance

- The 1403 equity statement's displayed restated opening balance (-80,551,230), 1402 net loss (-15,709,645), and capital-in-progress increase (+14,069,826) imply a 1402 closing balance of -82,191,049.
- Reported closing equity is -38,949,540, exactly 43,241,509 higher; that is the same correction displayed in the opening section.
- The reported closing amount is reproduced only when the pre-adjustment opening balance (-37,309,721) is used. The correction is shown in the opening section but not carried into closing.
- This establishes an internal rollforward inconsistency. Accounting owner must decide the proper comparative presentation; official workbook remains unchanged.


## 2026-11-11 — Budget Notes 36–39 reconciliation

- Reconciled Notes 36/37 actual revenue, current expenses and profit/loss to the primary statements for 1402, 1403 and 1404.
- Reconciled Note 39 actual resources to actual uses for all three years: 47,443,159; 61,677,400; and 71,738,067 million Rials respectively.
- 1404 budget performance: revenue 13.98% below revised budget; current expenses 13.46% above; service cost 84.1% above; distribution/administrative/general expenses 53.9% below. Note 38 attributes artificial deviations partly to traditional, non-activity-based allocation.
- New issue BUDGET-1403/1404-N36-37-APPROVED-01: #REF! in original-approved-budget cells (1403 G120/G123; 1404 G127/G130). Revised-budget and actual columns reconcile; original-budget comparison is incomplete.
- New issue BUDGET-1404-N39-UNIT-01: original-budget column E22:E32 contains Rial-scale values while the table states million Rials and F/G columns are in million Rials; E35 is already in million-Rial scale; E9/E16 are #REF!. Actual/revised resources and uses still tie.
- Zero/zero percentage cells #DIV/0! in 1402 Note 38 I38 and 1403/1404 Note 39 I38 are excluded: amount and denominator are both zero, with no effect on totals.
- No canonical source workbook/PDF, ledger row, Mapping row, database, application code or financial value changed.
- Accounting/budget owner disposition is required for the two original-budget disclosure issues. These are separate from primary-statement arithmetic and do not block continued review.
