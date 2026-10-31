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


## 2026-10-31 — unmerged read-only Mapping coverage candidate

- Development-only branch: `codex/aram-readonly-mapping-coverage-20261031`, based on accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- New `coverage_preview.py` and synthetic tests check account-to-note exposure, exceptions and bounded untrusted XLSX inputs, with no DB or statement output.
- Status: **IN_PROGRESS / NOT ACCEPTED**. No financial approval, released EXE, merge or real-data reconciliation is claimed.
- This entry is a branch-local candidate record; historical stale PR #21 status in this file is superseded by live GitHub evidence.

### PR #60 evidence checkpoint (2026-10-30)

- Actual Draft: https://github.com/davoodmehraban89/Aram/pull/60, from exact accepted base `7dc864fd032f0c4ae4d650d89304a01286a6d914`; no merge.
- Adds safe local CLI and synthetic CLI tests to read-only coverage engine; further hardens hidden helper and extra sheet handling. Earlier CI https://github.com/davoodmehraban89/Aram/actions/runs/41126235147 succeeded, **but final-head acceptance remains pending a new run**.
- Never treat workbook `Approved` labels as corporate approval. All output is advisory, non-releasable, no official financial values posted.

## Draft Gate 3 — note exposure reconciliation candidate (2026-10-31)
- Branch `codex/aram-reconciliation-review-gate-20261031` is based on unmerged coverage PR #60 head `8f0e9e400c63237e00ae6d0b9847a473cb758d6e`.
- Adds `reconciliation_review.py`, synthetic tests and `docs/NOTE_RECONCILIATION_REVIEW.md` for exact per-note candidate/reference comparisons.
- No financial statement, authenticated approval, mapped account write, release, canonical XLSX/PDF change, or accepted-branch merge. Status: DRAFT / NOT ACCEPTED. Independent C1/C2/C3 reviews required.

## 2026-10-31 — unsigned balance-sheet candidate (Draft)
- New dependent branch `codex/aram-bs-candidate-statement-20261031` based on Draft PR #61 exact head `736193905d8b041a938e7285610ff207b4cd4487`.
- Adds explicit-policy BS candidate and synthetic security/accounting tests. The equity equation is an arithmetic **diagnostic**, never a verified statutory balance sheet. No data source, migration, release or accepted branch touched.
- PR and exact-head CI must be verified separately. Independent C1/C2/C3 and accounting-owner acceptance **not completed**. Status: NOT ACCEPTED / UNMERGED.

## 2026-10-31 — unsigned income statement candidate (Draft)
- Independent development branch `codex/aram-income-statement-candidate-20261031`, based on unmerged PR #62 at `d6d0fc5da47e7209fe21fe96d48548d1489ef8a7`.
- Introduces explicit income/cost/expense/tax sign policies, provisional period-result arithmetic, strict offline CLI and synthetic adversarial tests. Real recognition, comparison-year rules and statutory reporting not implemented.
- No canonical financial sources, original migrations, database writes, releases, and accepted branch modifications. **DRAFT / NOT ACCEPTED** until CI and C1/C2/C3 + financial owner review.

## 2026-10-31 — trial balance source arithmetic diagnostic (DRAFT)
- Child branch `codex/aram-trial-balance-diagnostic-20261031`, based on unmerged income candidate PR #63 `5679a2e9feff582b0d0b74bd5a807387879bb358`.
- Read-only company/year trial-balance equality and per-account movement checks with synthetic tests, local-only CLI and explicit signed net-debit assumptions. Not a verified or complete source ledger.
- Data files, migrations, customer credentials, released artifact and accepted base untouched; formal C1/C2/C3 reviews and accountant signoff pending. NOT ACCEPTED.

## 2026-10-31 — statement of changes in equity candidate (DRAFT)
- Child branch `codex/aram-equity-changes-candidate-20261031`, based on unmerged PR #64 SHA `bfdde93bf98383470181b7ee55409e2ab9c45408`.
- Adds explicit note-level equity component/movement classifications, debit-net sign policy, opening/movement/closing exact roll-forward, account trace, guarded offline CLI and synthetic tests.
- A single note policy classifies all mapped turnovers in that note as one movement type; mixed movements need split subnotes. Profit/loss movement is not yet automatically tied to the income statement. No financial authority, source completeness or independent signoff is claimed.
- Canonical source files, database migrations, accepted branch, customer records and releases unchanged. NOT ACCEPTED; exact-head CI and finance-owner/C1/C2/C3 approvals pending.

## 2026-10-31 — direct-method cash flow candidate (DRAFT)
- Child branch `codex/aram-cash-flow-direct-candidate-20261031`, based on unmerged PR #65 SHA `6dd52d6e098999d22700ba2a7150bedc3846ab1a`.
- Requires paired transaction-level cash/counterpart postings, explicit cash-account registry and counterpart activity policies; ties transaction debit/credit to source cash-account turnovers and opening + net flow = closing.
- Does not infer cash flow from aggregate trial balance. No proof of completeness/authenticity, no owner-approved cash-account scope, no official statement, no export, no finance approval. Date convention requires source-owner confirmation.
- Synthetic-only implementation/tests; canonical data, DB/migrations, accepted branch, customer records and releases unchanged. Exact-head CI and independent C1/C2/C3 remain pending.
