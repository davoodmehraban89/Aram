# Aram — Open Pull Request and Branch Dependency Inventory

**Snapshot:** 2026-11-11  
**Repository:** [davoodmehraban89/Aram](https://github.com/davoodmehraban89/Aram)  
**Source:** GitHub live Pull Requests API (`state=open`, up to 100 results)  
**Purpose:** prevent accidental merging of stacked drafts and make the actual integration backlog visible.

## 1. Executive summary

- Open pull requests: **55**
- Draft: **55**
- Ready for review: **0**
- Directly based on accepted branch `source-data-cleanup`: **13**
- Stacked on another unmerged feature / documentation branch: **42**

All 55 open pull requests were Draft at the time of inspection: yes.

**Critical implication:** PRs based on other unmerged PR branches are not independently mergeable into the accepted baseline in arbitrary order. The PR list is a dependency graph, not a flat queue. Do not merge every green PR or promote a child branch without its parent chain and acceptance gates.

## 2. Direct-to-baseline versus stacked PRs

### Directly based on `source-data-cleanup`

- [PR #22 — docs(T1): restore README and reconcile accepted V1-01 status](https://github.com/davoodmehraban89/Aram/pull/22) — head `codex/t1-repo-hygiene-20261023` @ `a344c45c70cc`
- [PR #23 — ci: add dependency audit](https://github.com/davoodmehraban89/Aram/pull/23) — head `codex/t2-ci-hardening-20261023` @ `ee249a725be6`
- [PR #24 — docs(T6a): read-only mapping diagnostic baseline](https://github.com/davoodmehraban89/Aram/pull/24) — head `codex/t6a-readonly-diagnostics-20261023` @ `93a2df3420fd`
- [PR #25 — refactor(T3): explicit reversible Alembic initial schema](https://github.com/davoodmehraban89/Aram/pull/25) — head `codex/t3-explicit-migrations-20261023` @ `35341a0eed60`
- [PR #26 — Gate 3: explicit fiscal-year mapping persistence with invariant tests](https://github.com/davoodmehraban89/Aram/pull/26) — head `codex/gate3-mapping-core` @ `185e47f03190`
- [PR #29 — ADR-012: keep Excel-first V1; reserve provider-neutral Peyvast connector architecture](https://github.com/davoodmehraban89/Aram/pull/29) — head `codex/adr-future-connectors-pi-v1` @ `4d82afcc555f`
- [PR #32 — fix: preserve protected fiscal-year ownership and note isolation](https://github.com/davoodmehraban89/Aram/pull/32) — head `codex/v1-year-isolation-followup-20261023` @ `28d1c57882ec`
- [PR #34 — docs(governance): propose ARAM 5+1+3 execution and independent acceptance model](https://github.com/davoodmehraban89/Aram/pull/34) — head `governance/aram-5-1-3-controls-20261030` @ `f4ff8846efda`
- [PR #44 — docs(roadmap): propose evidence-based ARAM phase dashboard and progress rubric](https://github.com/davoodmehraban89/Aram/pull/44) — head `docs/aram-roadmap-dashboard-20261030` @ `ef718680c1b2`
- [PR #60 — feat(mapping): add read-only, fail-closed Pilot coverage preview (synthetic tests)](https://github.com/davoodmehraban89/Aram/pull/60) — head `codex/aram-readonly-mapping-coverage-20261031` @ `6f7a9d0ff08c`
- [PR #82 — Gate 3 — FINAL NO-GO: independent signoffs and operational evidence required](https://github.com/davoodmehraban89/Aram/pull/82) — head `feat/gate3-governed-mapping-20261101` @ `9d346f098a0a`
- [PR #90 — docs: reconcile financial statements 1402–1404](https://github.com/davoodmehraban89/Aram/pull/90) — head `docs/financial-statement-reconciliation-1402-1404-20261110` @ `0b7fef312b69`
- [PR #91 — docs: establish mandatory Aram master control plan](https://github.com/davoodmehraban89/Aram/pull/91) — head `docs/aram-master-control-plan-20261111` @ `7c7a852b28ed`

### Stacked on another branch

- [PR #27 — Gate 3 Mapping XLSX interchange with atomic import and hostile-input checks](https://github.com/davoodmehraban89/Aram/pull/27) — head `codex/gate3-mapping-excel-20261023`, base `codex/gate3-mapping-core`
- [PR #28 — Gate 3: deterministic read-only mapping coverage and exception queues](https://github.com/davoodmehraban89/Aram/pull/28) — head `codex/gate3-mapping-coverage-20261023`, base `codex/gate3-mapping-core`
- [PR #30 — Gate 3: read-only reviewed mapping carry-forward preview](https://github.com/davoodmehraban89/Aram/pull/30) — head `codex/gate3-carry-forward-preview-20261023`, base `codex/gate3-mapping-core`
- [PR #31 — Gate 3: read-only note mapping review and exception queues](https://github.com/davoodmehraban89/Aram/pull/31) — head `codex/gate3-note-mapping-review-20261023`, base `codex/gate3-mapping-core`
- [PR #33 — docs: specify Peyvast ingestion and mapping approval workflow](https://github.com/davoodmehraban89/Aram/pull/33) — head `codex/payvast-mapping-discovery-20261023`, base `codex/v1-year-isolation-followup-20261023`
- [PR #35 — fix(financial integrity): close issue #36 same-flush and clean-reference gaps](https://github.com/davoodmehraban89/Aram/pull/35) — head `codex/aram-same-flush-fiscal-lock-20261030`, base `codex/v1-year-isolation-followup-20261023`
- [PR #45 — fix: reject stale note versions in mapping carry-forward](https://github.com/davoodmehraban89/Aram/pull/45) — head `codex/aram-gate3-stale-note-guard-20261030`, base `codex/gate3-carry-forward-preview-20261023`
- [PR #46 — fix: reject hidden XLSX mapping content before import](https://github.com/davoodmehraban89/Aram/pull/46) — head `codex/aram-gate3-hidden-xlsx-guard-20261030`, base `codex/gate3-mapping-excel-20261023`
- [PR #47 — fix: flag stale and cross-year note mapping coverage](https://github.com/davoodmehraban89/Aram/pull/47) — head `codex/aram-gate3-coverage-target-guard-20261030`, base `codex/gate3-mapping-coverage-20261023`
- [PR #50 — fix(mapping): require current note targets and prepare reviewed change previews](https://github.com/davoodmehraban89/Aram/pull/50) — head `codex/aram-gate3-mapping-change-preview-20261030`, base `codex/gate3-mapping-core`
- [PR #51 — feat(mapping): fail-closed batch review and duplicate/exception preflight](https://github.com/davoodmehraban89/Aram/pull/51) — head `codex/gate3-mapping-batch-review-20261030`, base `codex/aram-gate3-mapping-change-preview-20261030`
- [PR #52 — fix(mapping): invalidate stale bulk review snapshots before authorization](https://github.com/davoodmehraban89/Aram/pull/52) — head `codex/gate3-mapping-batch-freshness-20261030`, base `codex/gate3-mapping-batch-review-20261030`
- [PR #53 — feat(mapping): store Unreviewed proposal drafts without approval or apply authority](https://github.com/davoodmehraban89/Aram/pull/53) — head `codex/gate3-unapproved-proposal-storage-20261030`, base `codex/gate3-mapping-batch-freshness-20261030`
- [PR #54 — feat(mapping): atomic insert-only system audit for Unreviewed draft staging](https://github.com/davoodmehraban89/Aram/pull/54) — head `codex/gate3-draft-staging-audit-20261030`, base `codex/gate3-unapproved-proposal-storage-20261030`
- [PR #55 — feat(auth): fail-closed RS256 principal verification, no financial approval](https://github.com/davoodmehraban89/Aram/pull/55) — head `codex/gate3-authenticated-principal-boundary-20261030`, base `codex/gate3-draft-staging-audit-20261030`
- [PR #56 — fix(auth): require signed company/year/role grants for Mapping access](https://github.com/davoodmehraban89/Aram/pull/56) — head `codex/gate3-signed-year-scope-20261030`, base `codex/gate3-authenticated-principal-boundary-20261030`
- [PR #57 — feat(mapping): atomically bind signed proposer identity to Unreviewed drafts](https://github.com/davoodmehraban89/Aram/pull/57) — head `codex/gate3-authored-draft-staging-20261030`, base `codex/gate3-signed-year-scope-20261030`
- [PR #59 — feat(desktop): native Windows pilot shell and safe workbook preflight, EXE build candidate](https://github.com/davoodmehraban89/Aram/pull/59) — head `codex/windows-native-pilot-shell-20261030`, base `codex/gate3-authored-draft-staging-20261030`
- [PR #61 — feat(review): strict read-only reconciliation of Mapping note exposures against explicit references](https://github.com/davoodmehraban89/Aram/pull/61) — head `codex/aram-reconciliation-review-gate-20261031`, base `codex/aram-readonly-mapping-coverage-20261031`
- [PR #62 — feat(statements): unsigned balance sheet candidate with explicit sign policy and financial equation](https://github.com/davoodmehraban89/Aram/pull/62) — head `codex/aram-bs-candidate-statement-20261031`, base `codex/aram-reconciliation-review-gate-20261031`
- [PR #63 — feat(statements): read-only explicit-policy income statement candidate and guarded CLI](https://github.com/davoodmehraban89/Aram/pull/63) — head `codex/aram-income-statement-candidate-20261031`, base `codex/aram-bs-candidate-statement-20261031`
- [PR #64 — feat(finance): read-only trial balance diagnostic with source turnover controls](https://github.com/davoodmehraban89/Aram/pull/64) — head `codex/aram-trial-balance-diagnostic-20261031`, base `codex/aram-income-statement-candidate-20261031`
- [PR #65 — feat(statements): add read-only explicit-policy statement of changes in equity](https://github.com/davoodmehraban89/Aram/pull/65) — head `codex/aram-equity-changes-candidate-20261031`, base `codex/aram-trial-balance-diagnostic-20261031`
- [PR #66 — feat(statements): add paired-transaction direct cash flow candidate and safe CLI](https://github.com/davoodmehraban89/Aram/pull/66) — head `codex/aram-cash-flow-direct-candidate-20261031`, base `codex/aram-equity-changes-candidate-20261031`
- [PR #67 — feat(control): add exact five-statement cross-reconciliation and cash/TB tie-out](https://github.com/davoodmehraban89/Aram/pull/67) — head `codex/aram-cross-statement-controls-20261031`, base `codex/aram-cash-flow-direct-candidate-20261031`
- [PR #68 — feat(mapping): support one account mapped to multiple financial statements](https://github.com/davoodmehraban89/Aram/pull/68) — head `codex/aram-multistatement-mapping-20261031`, base `codex/aram-cross-statement-controls-20261031`
- [PR #69 — test(control): exercise full five-statement pipeline and harden detail-level reconciliation](https://github.com/davoodmehraban89/Aram/pull/69) — head `codex/aram-five-statement-integration-20261031`, base `codex/aram-multistatement-mapping-20261031`
- [PR #70 — feat(pipeline): orchestrate all five statement candidates from one source snapshot](https://github.com/davoodmehraban89/Aram/pull/70) — head `codex/aram-five-statement-orchestrator-20261031`, base `codex/aram-five-statement-integration-20261031`
- [PR #71 — feat(cli): add strict offline five-statement pipeline preview](https://github.com/davoodmehraban89/Aram/pull/71) — head `codex/aram-five-statement-cli-20261031`, base `codex/aram-five-statement-orchestrator-20261031`
- [PR #72 — fix(cli): enforce strict financial manifest types and transaction scope](https://github.com/davoodmehraban89/Aram/pull/72) — head `codex/aram-pipeline-manifest-schema-20261031`, base `codex/aram-five-statement-cli-20261031`
- [PR #73 — fix(cli): enforce five-statement manifest referential integrity before workbook reads](https://github.com/davoodmehraban89/Aram/pull/73) — head `codex/aram-manifest-referential-integrity-20261031`, base `codex/aram-pipeline-manifest-schema-20261031`
- [PR #74 — ci: migrate Backend CI to Node24 actions and disable persisted git credentials](https://github.com/davoodmehraban89/Aram/pull/74) — head `codex/aram-actions-node24-maintenance-20261031`, base `codex/aram-manifest-referential-integrity-20261031`
- [PR #75 — feat(desktop): native Windows five-statement read-only pilot and unsigned EXE CI](https://github.com/davoodmehraban89/Aram/pull/75) — head `codex/aram-windows-five-statement-pilot-20261031`, base `codex/aram-actions-node24-maintenance-20261031`
- [PR #76 — feat(demo): bundle synthetic XLSX/manifest and validate frozen Windows positive flow](https://github.com/davoodmehraban89/Aram/pull/76) — head `codex/aram-synthetic-windows-demo-20261031`, base `codex/aram-windows-five-statement-pilot-20261031`
- [PR #77 — feat(desktop): show exact nonofficial statement figures and reconciliation differences](https://github.com/davoodmehraban89/Aram/pull/77) — head `codex/aram-windows-statement-figures-20261031`, base `codex/aram-synthetic-windows-demo-20261031`
- [PR #78 — feat(desktop): add searchable statement-line and transaction drill-down](https://github.com/davoodmehraban89/Aram/pull/78) — head `codex/aram-windows-detail-review-20261031`, base `codex/aram-windows-statement-figures-20261031`
- [PR #79 — perf(desktop): move 75k-row detail search off the Windows UI thread](https://github.com/davoodmehraban89/Aram/pull/79) — head `codex/aram-windows-background-detail-search-20261031`, base `codex/aram-windows-detail-review-20261031`
- [PR #80 — feat(trace): show exact account-to-note source lineage in Windows analyst drill-down](https://github.com/davoodmehraban89/Aram/pull/80) — head `codex/aram-account-note-source-trace-20261031`, base `codex/aram-windows-background-detail-search-20261031`
- [PR #81 — feat(ingestion): add read-only mapping source parser](https://github.com/davoodmehraban89/Aram/pull/81) — head `codex/aram-mapping-source-parser-20261101`, base `codex/aram-account-note-source-trace-20261031`
- [PR #88 — Gate 3 Package 9 — isolated local hardening candidate (NO-GO)](https://github.com/davoodmehraban89/Aram/pull/88) — head `feat/gate3-package9-isolated-20261103`, base `feat/gate3-governed-mapping-20261101`
- [PR #89 — Security 9.1: Argon2id API integration, DPAPI vault and recovery envelope (partial, NO-GO)](https://github.com/davoodmehraban89/Aram/pull/89) — head `feat/gate3-package9-1-security-20261103`, base `feat/gate3-package9-isolated-20261103`
- [PR #92 — fix(security): fail closed on malformed Unicode passwords](https://github.com/davoodmehraban89/Aram/pull/92) — head `fix/password-unicode-validation-20261111`, base `feat/gate3-package9-1-security-20261103`

## 3. Complete live inventory

| PR | State | Head branch | Base branch | Head SHA (12) | Workstream | Last updated (UTC date) |
|---|---|---|---|---|---|---|
| [#22](https://github.com/davoodmehraban89/Aram/pull/22) | Draft | `codex/t1-repo-hygiene-20261023` | `source-data-cleanup` | `a344c45c70cc` | Other | 2026-10-30 |
| [#23](https://github.com/davoodmehraban89/Aram/pull/23) | Draft | `codex/t2-ci-hardening-20261023` | `source-data-cleanup` | `ee249a725be6` | Other | 2026-10-30 |
| [#24](https://github.com/davoodmehraban89/Aram/pull/24) | Draft | `codex/t6a-readonly-diagnostics-20261023` | `source-data-cleanup` | `93a2df3420fd` | Other | 2026-10-22 |
| [#25](https://github.com/davoodmehraban89/Aram/pull/25) | Draft | `codex/t3-explicit-migrations-20261023` | `source-data-cleanup` | `35341a0eed60` | Other | 2026-10-30 |
| [#26](https://github.com/davoodmehraban89/Aram/pull/26) | Draft | `codex/gate3-mapping-core` | `source-data-cleanup` | `185e47f03190` | Gate 3 / Mapping | 2026-10-30 |
| [#27](https://github.com/davoodmehraban89/Aram/pull/27) | Draft | `codex/gate3-mapping-excel-20261023` | `codex/gate3-mapping-core` | `6c0068a660a3` | Gate 3 / Mapping | 2026-10-30 |
| [#28](https://github.com/davoodmehraban89/Aram/pull/28) | Draft | `codex/gate3-mapping-coverage-20261023` | `codex/gate3-mapping-core` | `02128c54109c` | Gate 3 / Mapping | 2026-10-30 |
| [#29](https://github.com/davoodmehraban89/Aram/pull/29) | Draft | `codex/adr-future-connectors-pi-v1` | `source-data-cleanup` | `4d82afcc555f` | Governance / connectors | 2026-10-23 |
| [#30](https://github.com/davoodmehraban89/Aram/pull/30) | Draft | `codex/gate3-carry-forward-preview-20261023` | `codex/gate3-mapping-core` | `dfcf3f008df5` | Gate 3 / Mapping | 2026-10-30 |
| [#31](https://github.com/davoodmehraban89/Aram/pull/31) | Draft | `codex/gate3-note-mapping-review-20261023` | `codex/gate3-mapping-core` | `e119586500d6` | Gate 3 / Mapping | 2026-10-30 |
| [#32](https://github.com/davoodmehraban89/Aram/pull/32) | Draft | `codex/v1-year-isolation-followup-20261023` | `source-data-cleanup` | `28d1c57882ec` | Other | 2026-10-30 |
| [#33](https://github.com/davoodmehraban89/Aram/pull/33) | Draft | `codex/payvast-mapping-discovery-20261023` | `codex/v1-year-isolation-followup-20261023` | `dfc01f7970ae` | Gate 3 / Mapping | 2026-10-30 |
| [#34](https://github.com/davoodmehraban89/Aram/pull/34) | Draft | `governance/aram-5-1-3-controls-20261030` | `source-data-cleanup` | `f4ff8846efda` | Governance / connectors | 2026-10-30 |
| [#35](https://github.com/davoodmehraban89/Aram/pull/35) | Draft | `codex/aram-same-flush-fiscal-lock-20261030` | `codex/v1-year-isolation-followup-20261023` | `e09aa43d22eb` | Other | 2026-10-30 |
| [#44](https://github.com/davoodmehraban89/Aram/pull/44) | Draft | `docs/aram-roadmap-dashboard-20261030` | `source-data-cleanup` | `ef718680c1b2` | Documentation / control | 2026-10-30 |
| [#45](https://github.com/davoodmehraban89/Aram/pull/45) | Draft | `codex/aram-gate3-stale-note-guard-20261030` | `codex/gate3-carry-forward-preview-20261023` | `57b2cb38a247` | Gate 3 / Mapping | 2026-10-30 |
| [#46](https://github.com/davoodmehraban89/Aram/pull/46) | Draft | `codex/aram-gate3-hidden-xlsx-guard-20261030` | `codex/gate3-mapping-excel-20261023` | `44c616f45de4` | Gate 3 / Mapping | 2026-10-30 |
| [#47](https://github.com/davoodmehraban89/Aram/pull/47) | Draft | `codex/aram-gate3-coverage-target-guard-20261030` | `codex/gate3-mapping-coverage-20261023` | `39f52fedd359` | Gate 3 / Mapping | 2026-10-30 |
| [#50](https://github.com/davoodmehraban89/Aram/pull/50) | Draft | `codex/aram-gate3-mapping-change-preview-20261030` | `codex/gate3-mapping-core` | `f79947a8624a` | Gate 3 / Mapping | 2026-10-30 |
| [#51](https://github.com/davoodmehraban89/Aram/pull/51) | Draft | `codex/gate3-mapping-batch-review-20261030` | `codex/aram-gate3-mapping-change-preview-20261030` | `d022ac48e78d` | Gate 3 / Mapping | 2026-10-30 |
| [#52](https://github.com/davoodmehraban89/Aram/pull/52) | Draft | `codex/gate3-mapping-batch-freshness-20261030` | `codex/gate3-mapping-batch-review-20261030` | `1063431b08a9` | Gate 3 / Mapping | 2026-10-30 |
| [#53](https://github.com/davoodmehraban89/Aram/pull/53) | Draft | `codex/gate3-unapproved-proposal-storage-20261030` | `codex/gate3-mapping-batch-freshness-20261030` | `3f089d03ca13` | Gate 3 / Mapping | 2026-10-30 |
| [#54](https://github.com/davoodmehraban89/Aram/pull/54) | Draft | `codex/gate3-draft-staging-audit-20261030` | `codex/gate3-unapproved-proposal-storage-20261030` | `c5e3fb7f8917` | Gate 3 / Mapping | 2026-10-30 |
| [#55](https://github.com/davoodmehraban89/Aram/pull/55) | Draft | `codex/gate3-authenticated-principal-boundary-20261030` | `codex/gate3-draft-staging-audit-20261030` | `8d82f1e7be96` | Gate 3 / Mapping | 2026-10-30 |
| [#56](https://github.com/davoodmehraban89/Aram/pull/56) | Draft | `codex/gate3-signed-year-scope-20261030` | `codex/gate3-authenticated-principal-boundary-20261030` | `0fc0713bd9e0` | Gate 3 / Mapping | 2026-10-30 |
| [#57](https://github.com/davoodmehraban89/Aram/pull/57) | Draft | `codex/gate3-authored-draft-staging-20261030` | `codex/gate3-signed-year-scope-20261030` | `6b6aca8883ad` | Gate 3 / Mapping | 2026-10-30 |
| [#59](https://github.com/davoodmehraban89/Aram/pull/59) | Draft | `codex/windows-native-pilot-shell-20261030` | `codex/gate3-authored-draft-staging-20261030` | `4cef1a1f3ff9` | Five-statement / Windows | 2026-10-30 |
| [#60](https://github.com/davoodmehraban89/Aram/pull/60) | Draft | `codex/aram-readonly-mapping-coverage-20261031` | `source-data-cleanup` | `6f7a9d0ff08c` | Gate 3 / Mapping | 2026-10-30 |
| [#61](https://github.com/davoodmehraban89/Aram/pull/61) | Draft | `codex/aram-reconciliation-review-gate-20261031` | `codex/aram-readonly-mapping-coverage-20261031` | `7c1afec2c306` | Other | 2026-10-30 |
| [#62](https://github.com/davoodmehraban89/Aram/pull/62) | Draft | `codex/aram-bs-candidate-statement-20261031` | `codex/aram-reconciliation-review-gate-20261031` | `d6d0fc5da47e` | Five-statement / Windows | 2026-10-30 |
| [#63](https://github.com/davoodmehraban89/Aram/pull/63) | Draft | `codex/aram-income-statement-candidate-20261031` | `codex/aram-bs-candidate-statement-20261031` | `5679a2e9feff` | Five-statement / Windows | 2026-10-31 |
| [#64](https://github.com/davoodmehraban89/Aram/pull/64) | Draft | `codex/aram-trial-balance-diagnostic-20261031` | `codex/aram-income-statement-candidate-20261031` | `bfdde93bf983` | Other | 2026-10-31 |
| [#65](https://github.com/davoodmehraban89/Aram/pull/65) | Draft | `codex/aram-equity-changes-candidate-20261031` | `codex/aram-trial-balance-diagnostic-20261031` | `6dd52d6e0989` | Other | 2026-10-31 |
| [#66](https://github.com/davoodmehraban89/Aram/pull/66) | Draft | `codex/aram-cash-flow-direct-candidate-20261031` | `codex/aram-equity-changes-candidate-20261031` | `6d7f949caeb7` | Other | 2026-10-31 |
| [#67](https://github.com/davoodmehraban89/Aram/pull/67) | Draft | `codex/aram-cross-statement-controls-20261031` | `codex/aram-cash-flow-direct-candidate-20261031` | `d1f52179dcd7` | Five-statement / Windows | 2026-10-31 |
| [#68](https://github.com/davoodmehraban89/Aram/pull/68) | Draft | `codex/aram-multistatement-mapping-20261031` | `codex/aram-cross-statement-controls-20261031` | `692150599ebc` | Gate 3 / Mapping | 2026-10-31 |
| [#69](https://github.com/davoodmehraban89/Aram/pull/69) | Draft | `codex/aram-five-statement-integration-20261031` | `codex/aram-multistatement-mapping-20261031` | `6a6548e2cb98` | Five-statement / Windows | 2026-10-31 |
| [#70](https://github.com/davoodmehraban89/Aram/pull/70) | Draft | `codex/aram-five-statement-orchestrator-20261031` | `codex/aram-five-statement-integration-20261031` | `e6876e0b1c3e` | Five-statement / Windows | 2026-10-31 |
| [#71](https://github.com/davoodmehraban89/Aram/pull/71) | Draft | `codex/aram-five-statement-cli-20261031` | `codex/aram-five-statement-orchestrator-20261031` | `3d498bcaf052` | Five-statement / Windows | 2026-10-31 |
| [#72](https://github.com/davoodmehraban89/Aram/pull/72) | Draft | `codex/aram-pipeline-manifest-schema-20261031` | `codex/aram-five-statement-cli-20261031` | `63c0cc94c1cd` | Other | 2026-10-31 |
| [#73](https://github.com/davoodmehraban89/Aram/pull/73) | Draft | `codex/aram-manifest-referential-integrity-20261031` | `codex/aram-pipeline-manifest-schema-20261031` | `475c114aef8c` | Other | 2026-10-31 |
| [#74](https://github.com/davoodmehraban89/Aram/pull/74) | Draft | `codex/aram-actions-node24-maintenance-20261031` | `codex/aram-manifest-referential-integrity-20261031` | `df39299230d5` | Other | 2026-10-31 |
| [#75](https://github.com/davoodmehraban89/Aram/pull/75) | Draft | `codex/aram-windows-five-statement-pilot-20261031` | `codex/aram-actions-node24-maintenance-20261031` | `04397f8ad6c3` | Five-statement / Windows | 2026-10-31 |
| [#76](https://github.com/davoodmehraban89/Aram/pull/76) | Draft | `codex/aram-synthetic-windows-demo-20261031` | `codex/aram-windows-five-statement-pilot-20261031` | `94e3e19fff7f` | Five-statement / Windows | 2026-10-31 |
| [#77](https://github.com/davoodmehraban89/Aram/pull/77) | Draft | `codex/aram-windows-statement-figures-20261031` | `codex/aram-synthetic-windows-demo-20261031` | `b3793f26437b` | Five-statement / Windows | 2026-10-31 |
| [#78](https://github.com/davoodmehraban89/Aram/pull/78) | Draft | `codex/aram-windows-detail-review-20261031` | `codex/aram-windows-statement-figures-20261031` | `7894ab136d5d` | Five-statement / Windows | 2026-10-31 |
| [#79](https://github.com/davoodmehraban89/Aram/pull/79) | Draft | `codex/aram-windows-background-detail-search-20261031` | `codex/aram-windows-detail-review-20261031` | `e7a803bee3da` | Five-statement / Windows | 2026-10-31 |
| [#80](https://github.com/davoodmehraban89/Aram/pull/80) | Draft | `codex/aram-account-note-source-trace-20261031` | `codex/aram-windows-background-detail-search-20261031` | `919c3c298815` | Five-statement / Windows | 2026-10-31 |
| [#81](https://github.com/davoodmehraban89/Aram/pull/81) | Draft | `codex/aram-mapping-source-parser-20261101` | `codex/aram-account-note-source-trace-20261031` | `da06ab3c37d7` | Gate 3 / Mapping | 2026-11-01 |
| [#82](https://github.com/davoodmehraban89/Aram/pull/82) | Draft | `feat/gate3-governed-mapping-20261101` | `source-data-cleanup` | `9d346f098a0a` | Gate 3 / Mapping | 2026-11-01 |
| [#88](https://github.com/davoodmehraban89/Aram/pull/88) | Draft | `feat/gate3-package9-isolated-20261103` | `feat/gate3-governed-mapping-20261101` | `a0b72be87720` | Gate 3 / Mapping | 2026-11-03 |
| [#89](https://github.com/davoodmehraban89/Aram/pull/89) | Draft | `feat/gate3-package9-1-security-20261103` | `feat/gate3-package9-isolated-20261103` | `18d6aa122d94` | Gate 3 / Mapping | 2026-11-03 |
| [#90](https://github.com/davoodmehraban89/Aram/pull/90) | Draft | `docs/financial-statement-reconciliation-1402-1404-20261110` | `source-data-cleanup` | `0b7fef312b69` | Documentation / control | 2026-11-11 |
| [#91](https://github.com/davoodmehraban89/Aram/pull/91) | Draft | `docs/aram-master-control-plan-20261111` | `source-data-cleanup` | `7c7a852b28ed` | Documentation / control | 2026-11-11 |
| [#92](https://github.com/davoodmehraban89/Aram/pull/92) | Draft | `fix/password-unicode-validation-20261111` | `feat/gate3-package9-1-security-20261103` | `191b9c4b0285` | Security | 2026-11-11 |

## 4. Workstream counts

| Workstream | Open PRs |
|---|---:|
| Documentation / control | 3 |
| Five-statement / Windows | 13 |
| Gate 3 / Mapping | 23 |
| Governance / connectors | 2 |
| Other | 13 |
| Security | 1 |

## 5. Control findings and integration policy

1. Treat each stacked PR as dependent on its base branch until a reviewed dependency graph proves otherwise.
2. No branch is accepted merely because it is open, Draft, has passing tests, or contains useful code.
3. Before promoting a child PR, inspect the full parent chain and compare every commit against the accepted baseline to avoid duplicate or missing changes.
4. For any candidate, verify exact head SHA, changed files, review threads, check-runs, source-of-truth boundaries and acceptance evidence.
5. PR #82 is explicitly titled FINAL NO-GO; PRs #88 and #89 are downstream Gate 3 / security candidates and remain isolated.
6. PRs #90 and #91 are documentation / control candidates directly based on the accepted baseline. PR #92 is a security child based on PR #89's branch, not the accepted baseline.
7. The long Windows / five-statement chain (PRs #62–#81) is stacked across many branches; do not cherry-pick the final child without reviewing every parent.
8. The Gate 3 Mapping chain (PRs #26–#57, plus #82/#88/#89) is likewise stacked; its draft status and NO-GO notes must remain visible.
9. Keep all existing branches and worktrees until a replacement integration candidate passes exact-base tests and independent review.
10. Re-fetch the live PR list before any merge, close, retarget, or release decision; this inventory is a timestamped snapshot, not a live view.

## 6. Recommended next action

Build a branch-family dependency DAG and a commit/file overlap matrix for the direct-to-baseline PRs and their stacked descendants. Then decide which workstreams are still in scope for V1, which are superseded, and which require a formal close-with-record. Do not mass-close or merge drafts without that review.

**Acceptance:** inventory only; no PR was merged, closed, retargeted, or modified by this report.
