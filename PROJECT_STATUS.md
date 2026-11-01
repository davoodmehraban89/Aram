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


## 2026-11-01 — Gate 3 current review status (supersedes older Gate 3 status above)
- Candidate: Draft PR #82 on feat/gate3-governed-mapping-20261101, based on source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914.
- Local Gate 3 implementation includes scoped mapping lifecycle, SQLite state/audit, optimistic concurrency, Pilot workbook roundtrip and unknown-account queue.
- Package 3 hardening adds separation of maker/reviewer/approver and validation that persisted mapping state agrees with append-only audit transitions.
- Three sequential self-audit passes documented at docs/GATE3_REVIEW_82.md; independent GitHub reviewers have not signed off.
- Status: CHANGES REQUESTED; Gate 3 is not formally accepted. No merge or release.
- Unresolved: authenticated identity and authorization, privileged-database tamper resistance, independent review, operational recovery drill, mapping ambiguity and real-data acceptance.
- Rollback: revert isolated PR commits; accepted base and canonical financial source files remain untouched.

## 2026-11-01 — Gate 3 Package 4 (supersedes earlier Gate 3 summaries)
- Isolated branch and Draft PR #82; accepted base source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914 unchanged.
- New security facade: role/scope checks with injected trusted identity resolver; NOT connected to production API/IdP.
- New integrity verification and consistent SQLite backup-to-fresh-file test; no external tamper-evident audit anchor.
- Conservative ambiguity assessment; Excel hierarchy/notes roundtrip fixes; no real-ledger reconciliation claimed.
- Review evidence: docs/GATE3_PACKAGE4_REVIEW.md (three self-review perspectives, not independent reviewers).
- Formal Gate 3 status: CHANGES REQUESTED; PR must remain Draft. Do not merge/release/start Gate 4 implementation before independent acceptance.
- Remaining blockers: independent reviewer approval, API/IdP authorization integration, external audit integrity, authorized financial reconciliation and operational recovery evidence.

## 2026-11-01 — Gate 3 Package 5 (current status)
- Branch feat/gate3-governed-mapping-20261101; PR #82 remains Draft; base source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914 unchanged.
- Protected mapping HTTP endpoints added; server-only resolver required and absent by default (fail closed). No real production IdP integration is claimed.
- SHA-256 per-event audit chain and externally verifiable receipt support added. No separately protected receipt anchor configured; privileged tampering remains possible.
- Synthetic HTTP, audit tamper, backup/restore and financial mapping tests added; no authorized real financial data or production DR drill performed.
- Three perspective-based self-audits, NOT three independent reviewers. See docs/GATE3_PACKAGE5_ACCEPTANCE.md.
- Decision: NO-GO / CHANGES REQUESTED. Do not merge, release or begin Gate 4 until policy prerequisites satisfied.

## 2026-11-01 — Gate 3 Package 6 (latest)
- Branch feat/gate3-governed-mapping-20261101, PR #82 Draft, base source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914.
- Fail-closed resolver exceptions and separate-directory experimental audit receipt archive with exclusive creation, fsync, verification and tamper tests.
- Full local backend suite, scoped Ruff and CI evidence are in PR #82; see docs/GATE3_PACKAGE6_FINAL.md for final acceptance matrix.
- Three self-audit perspectives are not independent reviewers. Real IdP, protected external anchor, authorized financial reconciliation, operational DR drill and independent signoffs remain external prerequisites.
- **NO-GO — Gate 3 NOT accepted.** No Merge, Release, production data edits or Gate 4 implementation.

## 2026-11-01 — Gate 3 Package 7: closure dossier (latest)
- Initial feature SHA 1856de1beaf32073932a4d9c17b6364438a603e1, approved base source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914, PR #82 Draft, working tree clean.
- All 98 backend tests passed locally. No production identity provider, independently protected audit receipt repository, approved real-ledger reconciliation, staging DR evidence or independent PR review was available.
- Closure dossier and reviewer signoff checklist: docs/GATE3_PACKAGE7_CLOSURE_DOSSIER.md.
- **Formal decision: NO-GO / CHANGES REQUESTED.** Assistant's technical work package closes; Gate 3 remains blocked on named external owners. No further assistant-only packages without new evidence or verified defect.
- No Merge, Release, canonical data changes or Gate 4 implementation.
