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
| V1-01 safety-gate hardening | VERIFIED_AND_MERGED | [PR #21](https://github.com/davoodmehraban89/Aram/pull/21), merged 2026-08-27; squash commit `7dc864fd032f0c4ae4d650d89304a01286a6d914`; [accepted-head CI](https://github.com/davoodmehraban89/Aram/actions/runs/33063001065) succeeded with 67 tests |
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
- PR #21 is accepted and protects fiscal-year/company identity. A follow-up audit reproduced moving year-owned records out of protected years and relationship-based cross-year statement-note links; the focused candidate on `codex/v1-year-isolation-followup-20261023` addresses these gaps but is not accepted yet.
- Accepted PR #21 rejects targetless/hierarchy-invalid mappings and declared closing-delta mismatches; these previously recorded candidate risks are resolved.
- The accepted root `index.html` is an explicit quarantine page. A real Pilot UI remains unimplemented.
- PR #17 was closed without merge; its stale-base 12-file diff is reference material only, and its narrative listed only 9 files.
- PR #17 CI was green on its own stale head, but compatibility with accepted Gate 2A was never proven.
- Binary execution, release provenance, and clean Windows verification do not exist.
- Mapping, notes/sub-notes, Pilot UI, and end-to-end user acceptance remain incomplete.

## Current focused follow-up — 2026-10-23

- Base verified against GitHub: `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- Candidate branch: `codex/v1-year-isolation-followup-20261023`; status `IN_PROGRESS`, not accepted.
- Scope: original/proposed fiscal-year ownership checks, effective relationship/FK validation, and focused regression tests. No schema, dependency, workflow, canonical-data or release changes.
- Local evidence: 110 tests passed, one existing third-party deprecation warning; isolated Alembic upgrade/downgrade, compilation and whitespace checks passed.
- RED evidence: original ownership regressions reproduced 22 missing rejections; reference-resolution regressions reproduced seven missing rejections before their respective fixes.
- Independent local review found one pending-explicit-ID parent gap, addressed with eight additional direct-FK tests; four reproduced the missing behavior before the fix.
- Graph-wide changes involving clean referencing records, expired fiscal-year lifecycle/same-flush behavior, and bulk/raw/concurrent writes are not certified by this focused ORM fix and require separate release gates.
- Published Draft [PR #32](https://github.com/davoodmehraban89/Aram/pull/32), initial reviewed-code head `75f82fcbfa2d9745d4c8e358979fe4fe754a82b6`. [Backend CI](https://github.com/davoodmehraban89/Aram/actions/runs/39959519926) succeeded on that head. This subsequent documentation-only reconciliation still requires final-head CI verification and independent remote acceptance; the PR remains unmerged.
- Draft PRs #22–31 exist as of this inspection; Gate 3 candidates are active but remain unaccepted. Their older descriptions may predate current CI results.

## Next action

1. Independently review the focused isolation follow-up and its final remote CI before accepting it; the implementation author must not self-merge.
2. Reconcile PR #22 documentation and PR #26/27 mapping candidates with the safety fix. Existing drafts do not yet implement the requested persisted old/new preview, user approval, identical-input coalescing or full account/dimension identity.
3. Continue the owner-requested read-only Peyvast SQL Server integration and governed DB/Excel mapping design. The customer installation version, schema, supported interface and access remain unverified; no live connector or financial reconciliation is claimed.

## Pending child safety fix — 2026-10-30

- Draft [PR #35](https://github.com/davoodmehraban89/Aram/pull/35) is stacked on unmerged PR #32 at `28d1c57882ec20fc17c2c133bbe62ff56e12973f`; neither is accepted or merged.
- Scope: reject simultaneous Draft→Approved fiscal-year transition and mutations/new registrations within that year's ORM Session; reject same-flush Company edits. Separate Draft edit followed by approval remains valid.
- Code/testing candidate `f5f9257563f382f6663bc7b1eb0433a43482e9fd`: [Backend CI run 41059384195](https://github.com/davoodmehraban89/Aram/actions/runs/41059384195) completed successfully, 120 passed, one warning; migration round-trip and compile passed. Later documentation-only SHA must be checked anew.
- Scope limitations remain: raw/bulk SQL, external database writers, concurrency, graph-wide parent moves and database-level integrity are **not** certified or fixed here.
- Do not treat the pending ORM fix as V1 financial release acceptance. All independent controls and parent merge/rebase gates remain mandatory.

## Pending graph-wide isolation follow-up — 2026-10-30

- Stacked Draft [PR #41](https://github.com/davoodmehraban89/Aram/pull/41) is based on unmerged PR #35 at `dab37e544e441a6111d7e88a53bae4d193f10de2`; PR #35 depends on unmerged PR #32. No acceptance or merge is claimed.
- Scope: detect Draft `NoteDefinition` or `FinancialStatement` year moves that would leave unmodified `MappingRule` or `StatementLine` references crossing fiscal years. Allow valid coordinated Draft moves and reference retargeting.
- RED test-only commit `0994232dfb48eac4d448cf4ea09b8ba770ae0cf0`: [Backend CI 41060564954](https://github.com/davoodmehraban89/Aram/actions/runs/41060564954): **6 failed, 123 passed**. These failures reproduced the clean-reference bypass.
- GREEN code-plus-regressions commit `78ff0dd5a8ee35b621ae901be39f6a11d37ea063`: [Backend CI 41060899585](https://github.com/davoodmehraban89/Aram/actions/runs/41060899585): **132 passed, 1 warning**, Alembic upgrade/downgrade and compile passed. Later documentation commits must have exact-head CI independently verified.
- Limits: only affected existing references are scanned at ORM before-flush time. Database-level raw/bulk/concurrent enforcement, all races, performance at scale and provider-level constraints remain unverified.
- Protected financial sources, `data/`, customer databases, migrations, dependencies, workflows, builds and releases were not modified. C1/C2/C3 independent approvals are pending. Draft/unmerged.

## Control documents

- [Project log](docs/PROJECT_LOG.md)
- [Decision log](docs/DECISION_LOG.md)
- [Acceptance policy](docs/ACCEPTANCE_POLICY.md)
- [Jules task template](docs/JULES_TASK_TEMPLATE.md)
- [Master recovery prompt](docs/handoff/MASTER_RECOVERY_PROMPT.md)
- [Latest handoff snapshot](docs/handoff/LATEST_HANDOFF.md)
- [Saveable ChatGPT bootstrap prompt](docs/handoff/CHATGPT_BOOTSTRAP_PROMPT.txt)
