# Aram — Execution Progress Dashboard

**As of:** 2026-11-11  
**Repository:** [davoodmehraban89/Aram](https://github.com/davoodmehraban89/Aram)  
**Control branch:** `docs/aram-master-control-plan-20261111`  
**Accepted baseline:** `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`  
**Governing plan:** [ARAM_MASTER_CONTROL_PLAN.md](ARAM_MASTER_CONTROL_PLAN.md)  
**Decision:** **NO-GO for production, release, or promotion of unaccepted candidate branches.**

> This dashboard is the operational progress register for the eight execution phases. Percentages are engineering estimates based on the evidence listed below; they are not automatically inferred from commits, lines of code, test counts, or elapsed time. A phase is complete only when all acceptance criteria pass and the required independent / finance / operations approvals are recorded.

## 1. Executive dashboard

| Phase | Name | Estimate | Status | Gate |
|---|---|---:|---|---|
| 0 | Freeze, inventory and control baseline | **65%** | IN_PROGRESS | P0 |
| 1 | Financial exception closure | **25%** | BLOCKED_ON_OWNER | P0 |
| 2 | Mapping workflow completion | **30%** | IN_PROGRESS / INTEGRATION_BLOCKED | P0 |
| 3 | Identity, authorization and segregation of duties | **25%** | IN_PROGRESS / SECURITY_NO_GO | P0 |
| 4 | Audit evidence, backup and disaster recovery | **10%** | NOT_OPERATIONALLY_PROVEN | P0 |
| 5 | Financial statement engine and reporting | **30%** | FOUNDATION_ONLY | P1 |
| 6 | User interface and workflow integration | **10%** | NOT_ACCEPTED | P1 |
| 7 | Windows packaging, installation and release | **5%** | NOT_STARTED_FOR_ACCEPTANCE | P1 |

**Indicative overall progress: 25%.** This is the simple arithmetic mean of the eight phase estimates (200 percentage points / 8). It is a coarse portfolio indicator, not a release-readiness score. Critical P0 gates remain open, so the product is not 25% ready for production.

### Status vocabulary

- `DONE_EVIDENCED`: task has a verifiable artifact or test result.
- `PARTIAL`: some implementation or analysis exists, but the task's full exit condition is not met.
- `NOT_STARTED`: no sufficient evidence of execution.
- `BLOCKED_ON_OWNER`: requires an accounting, budget, product, security, or operations decision.
- `INTEGRATION_BLOCKED`: candidate code exists but conflicts / integration / acceptance remain open.
- `NOT_VERIFIED`: evidence has not been obtained; do not infer success.
- `ACCEPTED`: all exit criteria passed and authorized acceptance is recorded. No phase in this dashboard is currently marked ACCEPTED as a whole.

## 2. Phase 0 — Freeze, inventory and establish control baseline

**Estimate: 65% · Status: IN_PROGRESS · Priority: P0**

| Work item | State | Evidence / exit condition |
|---|---|---|
| Publish mandatory master control plan | PARTIAL | Draft PR #91 contains `docs/ARAM_MASTER_CONTROL_PLAN.md` and contributor instructions; not merged / accepted |
| Inventory six local Windows worktrees | DONE_EVIDENCED | Six worktrees, branch names, HEAD SHAs and dirty states recorded |
| Preserve dirty / untracked files | DONE_EVIDENCED | 62 files copied to local snapshot; 62/62 SHA-256 comparisons passed |
| Classify duplicate and conflicting paths | DONE_EVIDENCED | 10 overlapping paths; 3 identical-content groups and 7 content-conflict groups documented |
| Complete file-level disposition for all snapshot entries | DONE_EVIDENCED | 62/62 current source files exist and still match snapshot SHA-256; every entry has a disposition and rationale in [file-level register](ARAM_WORKTREE_FILE_LEVEL_DISPOSITION_20261111.md) |
| Resolve all substantive conflicts | PARTIAL | Reviewer-preservation, dependency and Alembic metadata conflicts identified; no integration merge performed |
| Reconcile status, log and handoff to live remote state | PARTIAL | Status / handoff records have historical inconsistencies; current PR metadata re-fetched, but durable docs still need full reconciliation |
| Select and validate one integration candidate | NOT_STARTED | Requires reviewed file ownership and exact-base integration plan |

**Remaining to close Phase 0**
1. Independently review the 62 file dispositions and confirm the proposed retain / hold / exclude decisions.
2. Resolve substantive conflicts with tests and explicit architecture decisions.
3. Select one integration branch based on the accepted baseline.
4. Reconcile all control documents and exact PR / CI heads.
5. Obtain independent review and record the accepted baseline transition.

**Key evidence:** [Draft PR #91](https://github.com/davoodmehraban89/Aram/pull/91), [worktree ownership matrix](ARAM_WORKTREE_CHANGE_OWNERSHIP_20261111.md), [62-entry file-level disposition register](ARAM_WORKTREE_FILE_LEVEL_DISPOSITION_20261111.md), local snapshot `%LOCALAPPDATA%\Aram\ControlBaseline\20261111-0935`.

## 3. Phase 1 — Financial exception closure

**Estimate: 25% · Status: BLOCKED_ON_OWNER · Priority: P0**

| Work item | State | Evidence / exit condition |
|---|---|---|
| FY1402–FY1404 arithmetic / cross-statement checks | PARTIAL | 69 read-only checks reported PASS; not a transaction-level GL reconciliation or signed finance acceptance |
| Account 8161 unmapped-row analysis | PARTIAL | 110 rows identified: 86 zero-balance and 24 non-zero; 7 missing Mapping keys identified |
| Verify all 24 non-zero rows and seven keys | PARTIAL | Direct workstation revalidation found 66 existing account-8161 rules and zero matches for all seven candidate keys; source note IDs support Notes 10/13; proposal and in-memory dry-run completed; accounting approval remains open |
| Simulate seven-rule Mapping outcome | DONE_EVIDENCED | In-memory simulation reproduced baseline (61 / 49 unmatched); proposed result: 75 new matches, 24 non-zero, 35 remaining unmatched all zero-balance, zero ambiguity; exposure ties exactly |
| FY1403 equity rollforward difference | PARTIAL / BLOCKED_ON_OWNER | Root cause strongly indicates the 43,241,509 million Rial prior-period adjustment is duplicated in the 1403 comparative opening; 1402 statement already carries the same two components. Owner must confirm original journals / approved TBs before correction |
| Note / sub-note reference reconciliation | PARTIAL | Issues identified; owner-approved final references not recorded |
| Budget source errors and unit consistency | BLOCKED_ON_OWNER | #REF! and mixed Rial / million-Rial presentation require budget-owner source decision |
| Auditor PDF review | PARTIAL | First five pages of 1402 (48p) and 1404 (47p) visually inspected; fair-presentation wording and separate litigation emphasis sections visible. 1403 extraction failed; full-page / all-matters review remains NOT_VERIFIED |
| Signed finance disposition and source hash recheck | NOT_STARTED | Mandatory exit evidence absent |

**Remaining to close Phase 1**
- Obtain accounting-owner disposition of the seven-key proposal in [MAP_8161_SEVEN_RULES_PROPOSAL_20261111.md](https://github.com/davoodmehraban89/Aram/blob/docs/financial-statement-reconciliation-1402-1404-20261110/docs/MAP_8161_SEVEN_RULES_PROPOSAL_20261111.md).
- Obtain accounting-owner disposition and independent review of the proposal and dry-run evidence.
- Only after approval, create a persistent derived Mapping copy; rerun exact workbook formulas / matcher and verify counts and source hashes.
- Preserve all 86 zero-balance rows and verify unmatched / ambiguous / deterministic counts.
- Never change the official Mapping workbook without the recorded approval and independent review.
- Resolve equity, note references, budget units and #REF! source cells with named owners.
- Inspect every auditor report page; record opinion, emphasis and other-matter paragraphs.
- Re-run year-separated reconciliations from hashed source inputs and obtain signed finance acceptance.

**Key evidence:** [PR #90](https://github.com/davoodmehraban89/Aram/pull/90) and its financial reconciliation report. PR #90 is Draft / open; its analysis is not a finance sign-off.

## 4. Phase 2 — Mapping workflow completion

**Estimate: 30% · Status: INTEGRATION_BLOCKED · Priority: P0**

| Work item | State | Evidence / exit condition |
|---|---|---|
| Mapping workflow implementation foundation | PARTIAL | Candidate implementations exist in isolated worktrees / PRs |
| Deterministic key and dimension semantics | PARTIAL | Account / company / year / dimensions need final contract and tests |
| Unmatched and ambiguous queues | PARTIAL | Candidate design / code exists; end-to-end acceptance absent |
| Reviewer / approver evidence preservation | PARTIAL | G1/G2.1 variants preserve reviewer; Gate3-Implementation variant overwrites reviewer; conflict documented |
| Bulk Excel import / export and round-trip | NOT_VERIFIED | No accepted end-to-end evidence |
| Stale-write / concurrency handling | NOT_VERIFIED | Required integration tests not proven |
| Source-cell drill-down and provenance | PARTIAL | Design requirement recorded; complete traceability not accepted |
| 100% statement-impacting row disposition | NOT_STARTED | Requires Phase 1 approved mapping decisions and full reconciliation |

**Remaining to close Phase 2**
- Decide and test one authoritative mapping key contract.
- Integrate reviewer-preserving lifecycle behavior.
- Complete Excel import/export, validation, round-trip and audit provenance.
- Test ambiguity, unmatched items, stale writes, concurrency and tenant boundaries.
- Demonstrate 100% disposition of statement-impacting rows with no silent mapping.

**Key evidence:** [Draft PR #82](https://github.com/davoodmehraban89/Aram/pull/82), worktree ownership matrix. No Gate 3 candidate is accepted.

## 5. Phase 3 — Identity, authorization and segregation of duties

**Estimate: 25% · Status: SECURITY_NO_GO · Priority: P0**

| Work item | State | Evidence / exit condition |
|---|---|---|
| Password hashing foundation (Argon2id / legacy verification) | PARTIAL | Candidate implementation and regression tests exist |
| Malformed Unicode password handling | DONE_EVIDENCED_LOCALLY | PR #92 local suite: 15 focused tests and 137 backend tests passed; exact-head CI was reported successful; PR remains Draft and independent review is pending |
| Multi-user identity provider wired to all APIs | NOT_STARTED / NOT_VERIFIED | G2.1 identity provider is not wired into HTTP authentication |
| Durable sessions, revocation and restart semantics | NOT_STARTED | Current candidate limitations include process-memory session state |
| Persistent throttling / lockout | NOT_STARTED | Durable atomic behavior and multi-worker tests absent |
| Canonical tenant / company / year enforcement | PARTIAL | Candidate foundations exist; full DB constraints and adversarial tests not accepted |
| Maker / reviewer / approver segregation | PARTIAL | Mapping lifecycle conflict remains; full API enforcement not accepted |
| Independent security review | NOT_STARTED | No independent security approval recorded |

**Remaining to close Phase 3**
- Choose and document the identity authority.
- Wire a single authentication / authorization composition root into every protected API.
- Implement persistent token/session lifecycle, revocation and atomic throttling.
- Enforce tenant membership in service logic and database constraints.
- Enforce segregation of duties server-side.
- Complete restart, multi-worker and cross-tenant negative tests.
- Obtain independent security review on the exact final candidate SHA.

**Key evidence:** [PR #92](https://github.com/davoodmehraban89/Aram/pull/92), [PR #89](https://github.com/davoodmehraban89/Aram/pull/89). PR #92 is a child candidate based on the Package 9.1 branch, not the accepted production baseline.

## 6. Phase 4 — Audit evidence, backup and disaster recovery

**Estimate: 10% · Status: NOT_OPERATIONALLY_PROVEN · Priority: P0**

| Work item | State | Evidence / exit condition |
|---|---|---|
| Local audit receipt / hash-chain primitives | PARTIAL | Synthetic / local candidate tests only |
| Independent immutable audit anchor | NOT_STARTED | No independent WORM / append-only anchor proven |
| Key custody / rotation / escrow | NOT_STARTED | Operational ownership and recovery evidence absent |
| Scheduled encrypted backups | NOT_STARTED | No accepted scheduled operational process |
| Off-device backup | NOT_STARTED | 62-file snapshot is on the same Windows machine |
| Independent restore drill | NOT_STARTED | No witnessed restore on separate host / profile |
| RPO / RTO measurement and alerting | NOT_STARTED | No measured operational evidence |

**Remaining to close Phase 4**
- Select an independently administered audit anchor and separate its administration credentials.
- Define key lifecycle and recovery ownership.
- Implement monitored encrypted backups with off-device retention.
- Restore on a clean independent environment.
- Run tamper, corruption and partial-failure drills.
- Record measured RPO / RTO and independent witness sign-off.

## 7. Phase 5 — Financial statement engine and reporting

**Estimate: 30% · Status: FOUNDATION_ONLY · Priority: P1**

| Work item | State | Evidence / exit condition |
|---|---|---|
| Ledger / workbook ingestion foundation | PARTIAL | Accepted metadata inspection and typed parsing foundations exist |
| Financial arithmetic and cross-statement validation | PARTIAL | 69 read-only checks reported PASS; not a full generation engine |
| Final account-to-statement / note contract | PARTIAL | Depends on approved Mapping and finance dispositions |
| Reproducible generation of all five statements | NOT_VERIFIED | No end-to-end accepted generation from approved source |
| Note and sub-note generation / tie-out | NOT_VERIFIED | Complete linked note output not demonstrated |
| Approved adjustments with maker-checker evidence | NOT_STARTED | Full governed workflow not accepted |
| Amount-to-source-cell traceability | PARTIAL | Required contract documented; end-to-end proof absent |
| Budget / actual / variance reporting | NOT_VERIFIED | Budget source-unit anomalies remain open |
| Finance-owner output sign-off | NOT_STARTED | No signed acceptance |

**Remaining to close Phase 5**
- Freeze approved source and mapping contracts.
- Generate all five statements and linked notes from approved data.
- Reconcile comparatives, cash, notes and cross-statement links.
- Add controlled adjustments and complete amount-to-source traceability.
- Add budget / actual / variance reporting with explicit units and bases.
- Obtain finance-owner sign-off on reproducible output.

## 8. Phase 6 — User interface and workflow integration

**Estimate: 10% · Status: NOT_ACCEPTED · Priority: P1**

| Work item | State | Evidence / exit condition |
|---|---|---|
| Existing UI / prototype inventory | PARTIAL | Older prototype references exist; current end-to-end UI not accepted |
| Persian-first RTL design system | NOT_STARTED | No accepted design-system evidence |
| Company / year and import wizard | NOT_STARTED | No accepted end-to-end user journey |
| Mapping workbench and exception queue | NOT_STARTED | Backend workflow not accepted; UI integration absent |
| Statement preview and approval inbox | NOT_STARTED | No accepted workflow evidence |
| Role-aware actions and audit history | NOT_STARTED | Depends on Phase 3 |
| Full backend API integration | NOT_STARTED | No proof of complete authenticated user journey |
| Usability / accessibility / failure-path tests | NOT_STARTED | No accepted evidence |

**Remaining to close Phase 6**
- Inventory and quarantine disconnected prototypes.
- Define Persian RTL navigation, number formatting and error conventions.
- Implement import, Mapping, exception, statement and approval screens.
- Integrate only with the accepted authenticated APIs.
- Test end-to-end user journeys, unauthorized actions, failure states and accessibility.

## 9. Phase 7 — Windows packaging, installation and release

**Estimate: 5% · Status: NOT_STARTED_FOR_ACCEPTANCE · Priority: P1**

| Work item | State | Evidence / exit condition |
|---|---|---|
| Reproducible build definition | NOT_STARTED | No accepted build provenance |
| Signed installer | NOT_STARTED | No accepted signed installer |
| Clean Windows install / upgrade / rollback | NOT_STARTED | No witnessed clean-machine evidence |
| Runtime dependency and secret handling | PARTIAL | Dependency conflicts identified; final runtime contract not accepted |
| Operator / administrator / recovery manuals | NOT_STARTED | Complete release manuals absent |
| Release tag / retained artifact / checksum | NOT_STARTED | No accepted V1 release |

**Remaining to close Phase 7**
- Finalize runtime dependency and data-location contracts.
- Produce reproducible signed installer.
- Test install, upgrade, rollback and uninstall on a clean Windows machine.
- Verify secrets, permissions, DPAPI, backup and restore.
- Publish manuals, release tag, artifact and hashes only after all approvals.

## 10. Cross-phase critical path

The following dependencies are mandatory:

1. Phase 0 must produce one reviewed integration baseline before shared-file consolidation.
2. Phase 1 must approve material financial dispositions before official mapping and statement rules are frozen.
3. Phase 2 and Phase 3 must both pass before governed multi-user Mapping can be accepted.
4. Phase 4 must prove independent backup / restore and audit evidence before operational acceptance.
5. Phase 5 depends on approved source data and Mapping contracts.
6. Phase 6 depends on stable authenticated APIs and statement workflows.
7. Phase 7 depends on the integrated, security-reviewed and finance-approved application.

Parallel work is allowed only when it does not modify shared files, canonical data, or an unaccepted dependency.

## 11. Immediate next actions — ordered and measurable

| Order | Action | Completion evidence |
|---:|---|---|
| 1 | Finish Phase 0 file-level ownership and conflict dispositions | Reviewed disposition for all 62 snapshot entries; integration branch proposal |
| 2 | Build account 8161 seven-key proposal | Seven keys, all 24 non-zero rows, source evidence, note references and reviewer checks |
| 3 | Obtain finance-owner decisions | Recorded disposition for account 8161, FY1403 equity, budget units / #REF!, note references |
| 4 | Reconcile Mapping implementation variants | One tested reviewer-preserving implementation and dependency / migration decision |
| 5 | Complete identity architecture decision | Signed architecture decision and API coverage inventory |
| 6 | Define DR acceptance plan | Off-device backup target, key owner, clean restore environment, RPO / RTO targets |
| 7 | Freeze statement-engine contract | Approved source / mapping / note contract and generation test fixtures |

## 12. Dashboard governance and update rules

1. This file is the single operational progress dashboard; `ARAM_MASTER_CONTROL_PLAN.md` remains the governing plan and policy.
2. Update this dashboard whenever a meaningful PR, test run, finance decision, security review, operational drill, or phase-gate decision changes status.
3. Every percentage change must include: previous percentage, new percentage, reason, evidence URL / SHA, and remaining acceptance criteria.
4. Never increase a phase percentage solely because code was written, commits were added, or tests ran; measure the accepted work items and exit criteria.
5. Do not mark a phase `ACCEPTED` until all its acceptance criteria pass and the authorized reviewer / owner decision is recorded.
6. For every task, use `NOT_VERIFIED` where evidence is missing. Do not convert absence of evidence into a pass.
7. Keep finance-owner, security-reviewer and operations-witness decisions distinct from developer self-review.
8. Preserve historical percentage changes in the append-only progress history below.
9. If evidence contradicts this dashboard, GitHub remote state and verified source evidence take precedence; correct the dashboard with a dated entry.
10. No phase percentage implies production approval. The overall release decision remains NO-GO until every mandatory P0 and P1 gate passes.

## 13. Progress history

### 2026-11-11 — Initial evidence-based baseline

- Phase estimates established: P0 65%, P1 25%, P2 30%, P3 25%, P4 10%, P5 30%, P6 10%, P7 5%.
- Indicative overall estimate: 25% (unweighted arithmetic mean).
- Basis: master control plan, PR #90 financial evidence, PR #91 control-plan candidate, PR #92 security correction candidate, six-worktree inventory and 62-file SHA-256 snapshot.
- No phase accepted as a whole.
- Production / release decision: NO-GO.
- Next review trigger: after Phase 0 ownership matrix completion and accounting-owner disposition of MAP-8161-01 / FS-1403-EQ-01.


### 2026-11-11 — File-level snapshot and source revalidation

- Re-read the local manifest and recalculated SHA-256 for all 62 current source files against the snapshot manifest.
- Result: 62/62 snapshot copies verified; 62/62 current source files exist and remain byte-identical to the snapshot; zero changed and zero missing source files.
- Created a disposition and rationale for every manifest entry.
- Counts: 10 generated artifacts excluded for regeneration; 3 pyproject dependency conflicts; 3 Mapping workflow conflicts; 3 Mapping regression-test entries; 2 Alembic env conflicts; 1 initial migration baseline review; 5 identity-gated files; 15 candidate tests/tools; 7 implementation candidates; 11 evidence/control docs; 1 CI workflow; 1 backend README.
- Added [ARAM_WORKTREE_FILE_LEVEL_DISPOSITION_20261111.md](ARAM_WORKTREE_FILE_LEVEL_DISPOSITION_20261111.md).
- This is a file-level proposal, not authorization to merge, copy, delete, reset or clean any worktree. Independent review and conflict resolution remain open.
- Phase 0 estimate remains 65%; no percentage increase is claimed from inventory alone.


### 2026-11-11 — Account 8161 proposal and direct source revalidation

- Added a seven-rule Mapping proposal based on direct ledger note IDs and the observed Mapping helper-key construction.
- Revalidated the three source workbook hashes on the Aram Windows host; they match the reconciliation baseline.
- Confirmed 66 existing account-8161 Mapping rows; all seven candidate keys have zero existing matches under the documented wildcard matching convention.
- No official workbook, ledger or Mapping data was changed. The proposal is not approved or applied.
- Phase 1 estimate remains 25%; proposal preparation and source verification do not close the exception or replace accounting-owner approval.
- Next gate: dry-run / derived-copy validation after approval, followed by exact count and exposure reconciliation.


### 2026-11-11 — Account 8161 in-memory dry-run completed

- Simulated the seven proposed rules against all 17,075 account-8161 rows (1403 and 1404) using the current matching dimensions and wildcard behavior.
- Baseline reproduced: 1403 61 unmatched; 1404 49 unmatched; no ambiguous matches.
- Simulated result: 75 new unique mappings (24 non-zero and 51 zero-balance), 35 remaining unmatched rows (all zero-balance), and zero ambiguous matches.
- Exposure ties exactly: 1403 +144,125,670,091 Rials; 1404 +52,782,248,710 Rials; combined +196,907,918,801 Rials.
- Simulation was in memory only; no derived workbook was saved and no official data changed.
- Phase 1 remains 25%; this is technical proposal evidence, not accounting approval or closure.
- Next gate: accounting-owner disposition and independent review before any persistent derived Mapping candidate.


### 2026-11-11 — Equity root cause and auditor opening pages

- FS-1403-EQ-01 was refined by comparing the 1402 and 1403 official equity statements: 43,241,509 million Rials is the same 33,467,967 + 9,773,542 already included in the 1402 statements. The 1403 comparative rollforward appears to repeat it at opening; likely correction is remove/correct duplicate row, not restate closing equity. Owner confirmation remains required.
- 1403 workbook prints two Note 23 headings: corrections/reclassifications (sheet 29, including 23-1-1) and non-cash transactions (sheet 30). The note catalog and matrix now distinguish these sections.
- Auditor 1402 (48 pages) and 1404 (47 pages): first five pages visually reviewed; visible fair-presentation opinion wording and separate litigation emphasis sections. 1403 PDF extraction failed; full review remains incomplete.
- No official financial workbook or PDF was changed. Phase 1 remains 25%; findings are more precise but not formally accepted.
