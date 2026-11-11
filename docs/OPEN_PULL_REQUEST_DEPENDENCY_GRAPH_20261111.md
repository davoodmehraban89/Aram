# Aram — Open PR Dependency Graph

**Snapshot:** 2026-11-11  
**Repository:** [davoodmehraban89/Aram](https://github.com/davoodmehraban89/Aram)  
**Method:** For each open PR, match its base branch to the head branch of any known PR (open or closed). This identifies direct parent-branch relationships; it is not a mergeability guarantee.

## 1. Graph summary

- Open PRs: 55
- Direct roots based on `source-data-cleanup`: 13
- Child PRs whose base matches another PR head: 42
- Open PRs whose base did not match any PR head in the fetched inventory: 0
- Parent PR states for matched children: open/not-merged: 42

A PR's base matching another PR's head is a dependency signal only. The parent may itself be unmerged, closed without merge, stale, or unsuitable for V1. Verify exact ancestry and compare commits before any integration.

## 2. Root PRs directly targeting the accepted baseline

| PR | Head branch | Head SHA | Workstream | Status |
|---|---|---|---|---|
| [#22](https://github.com/davoodmehraban89/Aram/pull/22) | `codex/t1-repo-hygiene-20261023` | `a344c45c70cc` | docs(T1): restore README and reconcile accepted V1-01 status | Draft |
| [#23](https://github.com/davoodmehraban89/Aram/pull/23) | `codex/t2-ci-hardening-20261023` | `ee249a725be6` | ci: add dependency audit | Draft |
| [#24](https://github.com/davoodmehraban89/Aram/pull/24) | `codex/t6a-readonly-diagnostics-20261023` | `93a2df3420fd` | docs(T6a): read-only mapping diagnostic baseline | Draft |
| [#25](https://github.com/davoodmehraban89/Aram/pull/25) | `codex/t3-explicit-migrations-20261023` | `35341a0eed60` | refactor(T3): explicit reversible Alembic initial schema | Draft |
| [#26](https://github.com/davoodmehraban89/Aram/pull/26) | `codex/gate3-mapping-core` | `185e47f03190` | Gate 3: explicit fiscal-year mapping persistence with invariant tests | Draft |
| [#29](https://github.com/davoodmehraban89/Aram/pull/29) | `codex/adr-future-connectors-pi-v1` | `4d82afcc555f` | ADR-012: keep Excel-first V1; reserve provider-neutral Peyvast connector architecture | Draft |
| [#32](https://github.com/davoodmehraban89/Aram/pull/32) | `codex/v1-year-isolation-followup-20261023` | `28d1c57882ec` | fix: preserve protected fiscal-year ownership and note isolation | Draft |
| [#34](https://github.com/davoodmehraban89/Aram/pull/34) | `governance/aram-5-1-3-controls-20261030` | `f4ff8846efda` | docs(governance): propose ARAM 5+1+3 execution and independent acceptance model | Draft |
| [#44](https://github.com/davoodmehraban89/Aram/pull/44) | `docs/aram-roadmap-dashboard-20261030` | `ef718680c1b2` | docs(roadmap): propose evidence-based ARAM phase dashboard and progress rubric | Draft |
| [#60](https://github.com/davoodmehraban89/Aram/pull/60) | `codex/aram-readonly-mapping-coverage-20261031` | `6f7a9d0ff08c` | feat(mapping): add read-only, fail-closed Pilot coverage preview (synthetic tests) | Draft |
| [#82](https://github.com/davoodmehraban89/Aram/pull/82) | `feat/gate3-governed-mapping-20261101` | `9d346f098a0a` | Gate 3 — FINAL NO-GO: independent signoffs and operational evidence required | Draft |
| [#90](https://github.com/davoodmehraban89/Aram/pull/90) | `docs/financial-statement-reconciliation-1402-1404-20261110` | `0b7fef312b69` | docs: reconcile financial statements 1402–1404 | Draft |
| [#91](https://github.com/davoodmehraban89/Aram/pull/91) | `docs/aram-master-control-plan-20261111` | `12dba0546562` | docs: establish mandatory Aram master control plan | Draft |

## 3. Parent-child dependency edges

| Parent PR | Child PR | Parent head branch | Child head branch | Child base |
|---|---|---|---|---|
| #26 (open) | #27 | `codex/gate3-mapping-core` | `codex/gate3-mapping-excel-20261023` | `codex/gate3-mapping-core` |
| #26 (open) | #28 | `codex/gate3-mapping-core` | `codex/gate3-mapping-coverage-20261023` | `codex/gate3-mapping-core` |
| #26 (open) | #30 | `codex/gate3-mapping-core` | `codex/gate3-carry-forward-preview-20261023` | `codex/gate3-mapping-core` |
| #26 (open) | #31 | `codex/gate3-mapping-core` | `codex/gate3-note-mapping-review-20261023` | `codex/gate3-mapping-core` |
| #26 (open) | #50 | `codex/gate3-mapping-core` | `codex/aram-gate3-mapping-change-preview-20261030` | `codex/gate3-mapping-core` |
| #27 (open) | #46 | `codex/gate3-mapping-excel-20261023` | `codex/aram-gate3-hidden-xlsx-guard-20261030` | `codex/gate3-mapping-excel-20261023` |
| #28 (open) | #47 | `codex/gate3-mapping-coverage-20261023` | `codex/aram-gate3-coverage-target-guard-20261030` | `codex/gate3-mapping-coverage-20261023` |
| #30 (open) | #45 | `codex/gate3-carry-forward-preview-20261023` | `codex/aram-gate3-stale-note-guard-20261030` | `codex/gate3-carry-forward-preview-20261023` |
| #32 (open) | #33 | `codex/v1-year-isolation-followup-20261023` | `codex/payvast-mapping-discovery-20261023` | `codex/v1-year-isolation-followup-20261023` |
| #32 (open) | #35 | `codex/v1-year-isolation-followup-20261023` | `codex/aram-same-flush-fiscal-lock-20261030` | `codex/v1-year-isolation-followup-20261023` |
| #50 (open) | #51 | `codex/aram-gate3-mapping-change-preview-20261030` | `codex/gate3-mapping-batch-review-20261030` | `codex/aram-gate3-mapping-change-preview-20261030` |
| #51 (open) | #52 | `codex/gate3-mapping-batch-review-20261030` | `codex/gate3-mapping-batch-freshness-20261030` | `codex/gate3-mapping-batch-review-20261030` |
| #52 (open) | #53 | `codex/gate3-mapping-batch-freshness-20261030` | `codex/gate3-unapproved-proposal-storage-20261030` | `codex/gate3-mapping-batch-freshness-20261030` |
| #53 (open) | #54 | `codex/gate3-unapproved-proposal-storage-20261030` | `codex/gate3-draft-staging-audit-20261030` | `codex/gate3-unapproved-proposal-storage-20261030` |
| #54 (open) | #55 | `codex/gate3-draft-staging-audit-20261030` | `codex/gate3-authenticated-principal-boundary-20261030` | `codex/gate3-draft-staging-audit-20261030` |
| #55 (open) | #56 | `codex/gate3-authenticated-principal-boundary-20261030` | `codex/gate3-signed-year-scope-20261030` | `codex/gate3-authenticated-principal-boundary-20261030` |
| #56 (open) | #57 | `codex/gate3-signed-year-scope-20261030` | `codex/gate3-authored-draft-staging-20261030` | `codex/gate3-signed-year-scope-20261030` |
| #57 (open) | #59 | `codex/gate3-authored-draft-staging-20261030` | `codex/windows-native-pilot-shell-20261030` | `codex/gate3-authored-draft-staging-20261030` |
| #60 (open) | #61 | `codex/aram-readonly-mapping-coverage-20261031` | `codex/aram-reconciliation-review-gate-20261031` | `codex/aram-readonly-mapping-coverage-20261031` |
| #61 (open) | #62 | `codex/aram-reconciliation-review-gate-20261031` | `codex/aram-bs-candidate-statement-20261031` | `codex/aram-reconciliation-review-gate-20261031` |
| #62 (open) | #63 | `codex/aram-bs-candidate-statement-20261031` | `codex/aram-income-statement-candidate-20261031` | `codex/aram-bs-candidate-statement-20261031` |
| #63 (open) | #64 | `codex/aram-income-statement-candidate-20261031` | `codex/aram-trial-balance-diagnostic-20261031` | `codex/aram-income-statement-candidate-20261031` |
| #64 (open) | #65 | `codex/aram-trial-balance-diagnostic-20261031` | `codex/aram-equity-changes-candidate-20261031` | `codex/aram-trial-balance-diagnostic-20261031` |
| #65 (open) | #66 | `codex/aram-equity-changes-candidate-20261031` | `codex/aram-cash-flow-direct-candidate-20261031` | `codex/aram-equity-changes-candidate-20261031` |
| #66 (open) | #67 | `codex/aram-cash-flow-direct-candidate-20261031` | `codex/aram-cross-statement-controls-20261031` | `codex/aram-cash-flow-direct-candidate-20261031` |
| #67 (open) | #68 | `codex/aram-cross-statement-controls-20261031` | `codex/aram-multistatement-mapping-20261031` | `codex/aram-cross-statement-controls-20261031` |
| #68 (open) | #69 | `codex/aram-multistatement-mapping-20261031` | `codex/aram-five-statement-integration-20261031` | `codex/aram-multistatement-mapping-20261031` |
| #69 (open) | #70 | `codex/aram-five-statement-integration-20261031` | `codex/aram-five-statement-orchestrator-20261031` | `codex/aram-five-statement-integration-20261031` |
| #70 (open) | #71 | `codex/aram-five-statement-orchestrator-20261031` | `codex/aram-five-statement-cli-20261031` | `codex/aram-five-statement-orchestrator-20261031` |
| #71 (open) | #72 | `codex/aram-five-statement-cli-20261031` | `codex/aram-pipeline-manifest-schema-20261031` | `codex/aram-five-statement-cli-20261031` |
| #72 (open) | #73 | `codex/aram-pipeline-manifest-schema-20261031` | `codex/aram-manifest-referential-integrity-20261031` | `codex/aram-pipeline-manifest-schema-20261031` |
| #73 (open) | #74 | `codex/aram-manifest-referential-integrity-20261031` | `codex/aram-actions-node24-maintenance-20261031` | `codex/aram-manifest-referential-integrity-20261031` |
| #74 (open) | #75 | `codex/aram-actions-node24-maintenance-20261031` | `codex/aram-windows-five-statement-pilot-20261031` | `codex/aram-actions-node24-maintenance-20261031` |
| #75 (open) | #76 | `codex/aram-windows-five-statement-pilot-20261031` | `codex/aram-synthetic-windows-demo-20261031` | `codex/aram-windows-five-statement-pilot-20261031` |
| #76 (open) | #77 | `codex/aram-synthetic-windows-demo-20261031` | `codex/aram-windows-statement-figures-20261031` | `codex/aram-synthetic-windows-demo-20261031` |
| #77 (open) | #78 | `codex/aram-windows-statement-figures-20261031` | `codex/aram-windows-detail-review-20261031` | `codex/aram-windows-statement-figures-20261031` |
| #78 (open) | #79 | `codex/aram-windows-detail-review-20261031` | `codex/aram-windows-background-detail-search-20261031` | `codex/aram-windows-detail-review-20261031` |
| #79 (open) | #80 | `codex/aram-windows-background-detail-search-20261031` | `codex/aram-account-note-source-trace-20261031` | `codex/aram-windows-background-detail-search-20261031` |
| #80 (open) | #81 | `codex/aram-account-note-source-trace-20261031` | `codex/aram-mapping-source-parser-20261101` | `codex/aram-account-note-source-trace-20261031` |
| #82 (open) | #88 | `feat/gate3-governed-mapping-20261101` | `feat/gate3-package9-isolated-20261103` | `feat/gate3-governed-mapping-20261101` |
| #88 (open) | #89 | `feat/gate3-package9-isolated-20261103` | `feat/gate3-package9-1-security-20261103` | `feat/gate3-package9-isolated-20261103` |
| #89 (open) | #92 | `feat/gate3-package9-1-security-20261103` | `fix/password-unicode-validation-20261111` | `feat/gate3-package9-1-security-20261103` |

## 4. Open PRs with base branch not matched to any PR head in this inventory

None.

## 5. Required integration controls

1. Do not merge child PRs before their parent chain is reviewed and accepted.
2. Closed-but-unmerged parents do not provide accepted code; children based on them must be rebased or explicitly justified.
3. A root PR targeting `source-data-cleanup` is not automatically safe; check its exact files, reviews, checks and acceptance gates.
4. Do not mass-close branches. First compare each workstream with the V1 product boundary and preserve evidence for superseded work.
5. Build a commit-level and file-level deduplication map across each chain before proposing a consolidation branch.
6. The current PRs #90/#91 are documentation candidates; #92 is based on #89 and is not a root candidate.
7. The final integration candidate must be created from the accepted baseline, contain only reviewed files, pass exact-head CI and receive independent review.

**Acceptance:** dependency inventory only. No branch was merged, closed, deleted or retargeted.
