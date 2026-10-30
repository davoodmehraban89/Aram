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

- Branch-protection state for `source-data-cleanup` has not been re-verified in the current session: the connected GitHub API returned HTTP 403. The previous PR #21 record stated the branch was unprotected; treat current enforcement as unknown until the owner verifies it. See [Issue #39](https://github.com/davoodmehraban89/Aram/issues/39).
- V1-01 was squash-merged by PR #21 at accepted commit `7dc864fd032f0c4ae4d650d89304a01286a6d914`. The accepted baseline includes protected fiscal-year identity/deletion and company guards, Pilot preflight validation for mapping hierarchy/targets/lifecycle/closing-delta, and a quarantined root `index.html`.
- Residual isolation gaps remain: the accepted ORM hook can miss moving existing year-owned records out of Approved/Locked years and certain cached/relationship-based cross-year references. Draft PR #32 adds persisted-origin and relationship checks (110 passed on its exact head), but same-flush approval and graph-wide parent moves remain open in [Issue #36](https://github.com/davoodmehraban89/Aram/issues/36). Do not describe PR #32 as accepted or database-level enforcement.
- The root `index.html` is a quarantine notice, not a functional Pilot UI. A real accountant-facing UI, reporting workflow, packaging and user acceptance remain incomplete.
- PR #17 was closed without merge; its stale-base 12-file diff is reference material only, and its narrative listed only 9 files.
- PR #17 CI was green on its own stale head, but compatibility with accepted Gate 2A was never proven.
- Binary execution, release provenance, and clean Windows verification do not exist.
- Mapping, notes/sub-notes, Pilot UI, and end-to-end user acceptance remain incomplete.

## Next execution priorities — all candidate PRs remain unaccepted

1. **Fiscal-year safety:** complete [Issue #36](https://github.com/davoodmehraban89/Aram/issues/36) against Draft [PR #32](https://github.com/davoodmehraban89/Aram/pull/32), then rerun Backend CI on the exact final head. PR #33 is stacked on #32 and must be reconciled after parent acceptance.
2. **Mapping core and dependents:** independently review [PR #26](https://github.com/davoodmehraban89/Aram/pull/26), then reconcile stacked #27, #28, #30 and #31. Resolve [Issue #38](https://github.com/davoodmehraban89/Aram/issues/38) (hidden XLSX content) before accepting import, and [Issue #37](https://github.com/davoodmehraban89/Aram/issues/37) (stale source-note carry-forward) before accepting carry-forward.
3. **Independent governance:** establish three distinct qualified reviewers and verify branch-protection/ruleset state through [Issue #39](https://github.com/davoodmehraban89/Aram/issues/39). Only then can Draft [PR #34](https://github.com/davoodmehraban89/Aram/pull/34) and other pending governance proposals receive valid independent acceptance.

Existing PR #23 (dependency audit) and PR #25 (explicit migration) have successful exact-head CI evidence, but remain Draft and have no independent review. CI success alone does not authorize merge or production use.

## Control documents

- [Project log](docs/PROJECT_LOG.md)
- [Decision log](docs/DECISION_LOG.md)
- [Acceptance policy](docs/ACCEPTANCE_POLICY.md)
- [Jules task template](docs/JULES_TASK_TEMPLATE.md)
- [Master recovery prompt](docs/handoff/MASTER_RECOVERY_PROMPT.md)
- [Latest handoff snapshot](docs/handoff/LATEST_HANDOFF.md)
- [Saveable ChatGPT bootstrap prompt](docs/handoff/CHATGPT_BOOTSTRAP_PROMPT.txt)

## 2026-10-23 repository-hygiene correction (pending review)

The accepted V1-01 safety-gate change was squash-merged as commit `7dc864fd032f0c4ae4d650d89304a01286a6d914` (PR #21). Earlier `IN_PROGRESS` references to PR #21 above are historical and superseded by this entry. The legacy root `index.html` is quarantined, not a functional production UI. This documentation correction is proposed on a separate Draft PR and is not accepted until merged.
