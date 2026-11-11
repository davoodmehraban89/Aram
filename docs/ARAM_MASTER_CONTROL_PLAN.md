# Aram — Master Project Control Plan

**Document status:** Active control baseline (documentation-only candidate)  
**Prepared:** 2026-11-11  
**Repository:** `davoodmehraban89/Aram`  
**Accepted baseline branch:** `source-data-cleanup`  
**Accepted baseline SHA:** `7dc864fd032f0c4ae4d650d89304a01286a6d914`  
**Control branch:** `docs/aram-master-control-plan-20261111`  
**Decision:** Continue controlled engineering; **NO-GO for production, merge of gated candidates, or release until the relevant acceptance gates pass.**

> This document is the mandatory starting point for every developer, reviewer, automation agent, and future work session on Aram. It is a control register, not evidence that unfinished work has been accepted.

---

## 1. Mission and product boundary

Aram is intended to be a controlled financial-statement preparation and reconciliation application. Its target workflow is:

1. Register an entity and fiscal year.
2. Import approved trial-balance / general-ledger and supporting workbook sources.
3. Inspect and validate source structure and provenance.
4. Map accounts and dimensions to statement lines and note disclosures.
5. Resolve unmatched and ambiguous mappings through an auditable workflow.
6. Generate the five financial statements and related notes.
7. Reconcile statements, notes, comparative periods, and source ledger.
8. Route work through maker / reviewer / approver controls.
9. Export controlled Excel / PDF outputs with traceability.
10. Preserve immutable audit evidence and prove backup / restore.
11. Package, install, operate, and support the Windows application.

A feature is **not complete** merely because source code exists or unit tests pass. Acceptance requires implementation, tests, integration, operational evidence where relevant, documentation, and an explicit reviewer decision.

## 2. Executive status

| Area | Evidence observed | Status |
|---|---|---|
| Accepted backend foundation | Existing accepted branch and prior merged phases | Baseline exists |
| Financial ingestion / workbook inspection | Backend modules and regression history | Implemented foundation; end-to-end acceptance still required |
| Mapping lifecycle / access / audit | Gate 3 candidate and synthetic tests | Candidate; not production accepted |
| Financial statement arithmetic | 69 arithmetic / cross-statement checks recorded for FY1402–FY1404 | Read-only checks pass; not an audit opinion |
| Account 8161 | 110 unmapped rows; 24 non-zero rows; net exposure IRR 196,907,918,801 | Open finance disposition |
| FY1403 equity rollforward | Difference IRR 43,241,509 million Rial in reported analysis | Open finance-owner disposition |
| Identity / authentication | Package 9.1 single-local-identity hardening; G2.1 multi-user foundation local only | Partial / NO-GO |
| Audit evidence anchor | Local receipt / hash-chain tests | Independent immutable anchor not proven |
| Backup / disaster recovery | Synthetic tests and recovery primitives | Operational DR not proven |
| Desktop UI / installer | No live application process observed during 2026-11-11 inspection | End-to-end UI / install acceptance not proven |
| Production release | No accepted release evidence | NOT READY |

### 2.1 Current governing decision

**NO-GO for production and release.** Keep the accepted baseline stable. Work may continue on isolated branches and disposable synthetic data. Do not merge a candidate, deploy, alter canonical financial source files, or claim independent approval without the evidence specified in this plan.

## 3. Repository and branch control

### 3.1 Accepted base

- Branch: `source-data-cleanup`
- SHA: `7dc864fd032f0c4ae4d650d89304a01286a6d914`
- This is the reference baseline used for the control review.
- Do not assume the repository's latest activity or a PR head is already part of this baseline.

### 3.2 Relevant pull requests observed on 2026-11-11

| PR | Scope | Observed state | Control instruction |
|---|---|---|---|
| [#82](https://github.com/davoodmehraban89/Aram/pull/82) | Gate 3 governed mapping | Draft / open / NO-GO | Do not merge; external acceptance blockers remain |
| [#88](https://github.com/davoodmehraban89/Aram/pull/88) | Package 9 isolated hardening | Draft / open | Candidate only; independent and operational evidence missing |
| [#89](https://github.com/davoodmehraban89/Aram/pull/89) | Package 9.1 security implementation | Draft / open | Single local identity; not a multi-user production IdP |
| [#90](https://github.com/davoodmehraban89/Aram/pull/90) | FY1402–FY1404 financial reconciliation documentation | Draft / open; 11 commits ahead of accepted base at inspected head | Preserve separately; accounting owner and independent review required |

PR metadata and head SHAs must be re-read before any action. The table is a dated snapshot, not a live status feed.

### 3.3 Known local Windows worktrees

Device inspected: **Aram** (Windows), 2026-11-11.

| Local path | Branch / HEAD observed | Working-tree condition observed |
|---|---|---|
| `C:\Users\Davood\Documents\Aram-Engineering-Review` | `local-gate3-verification-20261101` / `da06ab3c37d789e565245f2f6ee38183a6f66fb6` | Untracked `backend/src/aram_backend.egg-info/` |
| `C:\Users\Davood\Documents\Aram-G1-Isolated` | `feat/aram-g1-architecture-20261103` / `18d6aa122d9486116c08d6e66b22675e0ebb1792` | 3 tracked modified files plus untracked report / egg-info |
| `C:\Users\Davood\Documents\Aram-G2.1-Isolated` | `feat/aram-g2-1-identity-20261103` / same HEAD | 4 tracked modified files plus untracked identity code, migration, tests and reports |
| `C:\Users\Davood\Documents\Aram-Gate3-Implementation` | `feat/gate3-governed-mapping-20261101` / `9d346f098a0a2159d96080715322879b08d9a1f8` | Numerous tracked modifications and untracked files; preserve |
| `C:\Users\Davood\Documents\Aram-Gate3-Package9-Isolated` | `feat/gate3-package9-isolated-20261103` / `a0b72be87720b1ff08361298b903ba57dd4fb408` | One untracked integration test |
| `C:\Users\Davood\Documents\Aram-Gate3-Package9-1-Security` | `feat/gate3-package9-1-security-20261103` / `18d6aa122d9486116c08d6e66b22675e0ebb1792` | Clean at inspection |

**Critical preservation rule:** never run `git reset`, `git clean`, force checkout, force push, delete a worktree, overwrite a dirty file, or copy changes between these worktrees without first making and verifying a full-file, hash-verified backup and documenting the exact source/destination file list. The dirty Gate3 implementation worktree is particularly sensitive.

### 3.4 Single-source-of-truth policy

- Accepted base remains `source-data-cleanup` until a reviewed and explicitly accepted successor is designated.
- Each work package uses one isolated branch and one focused PR.
- No direct feature development on the accepted base.
- Do not create another parallel implementation of a capability already under review.
- Before coding, inspect this plan, current PRs, branch head, local worktree status, and latest handoff.
- After coding, update this document and the project log with exact SHAs, files, tests, decisions, blockers, and next action.

## 4. Evidence and findings register

### 4.1 Financial statements — FY1402 to FY1404

The read-only reconciliation report records 69 checks: 24 income-statement arithmetic checks, 12 statement-of-financial-position checks, 30 cash-flow checks, and 3 closing-cash cross-statement checks. All were reported PASS.

This is **not** a transaction-level General Ledger reconciliation, an audit opinion, or signed finance acceptance.

Open financial issues:

| ID | Finding | Required disposition |
|---|---|---|
| FS-1403-EQ-01 | FY1403 equity rollforward appears inconsistent by IRR 43,241,509 million Rial | Accounting owner decides the correct presentation; no silent workbook repair |
| MAP-8161-01 | 110 unmapped rows across FY1403/FY1404; 24 non-zero; net IRR 196,907,918,801 | Approve exact seven missing mapping keys and rerun reconciliation; preserve all source rows |
| FS-1403/1404-NOTE-REF-01 | Balance-sheet note references drift from printed note headings | Accounting owner confirms presentation references |
| FS-1402/1403-CF-FX-REF-01 | FY1403 FX cash-flow note reference differs from printed sub-note; FY1402 sub-note identifier unresolved | Confirm references with accounting owner |
| FS-1404-CF-01 | IRR 12,556 million FX effect ties cash bridge and is described in Note 9-3; detailed rate schedule not independently reperformed | Obtain / inspect supporting calculation if required |
| FS-1404-CF-02 | +1 / -1 million Rial comparative cash-flow presentation differences offset | Confirm rounding / presentation treatment |
| AUDIT-PDF-01 | Full auditor opinion wording not verified for all scanned PDFs | OCR / visually inspect every page and record exact opinion and emphasis paragraphs |
| BUDGET-1403/1404-N36-37-APPROVED-01 | Original approved budget cells include #REF! | Finance/budget owner determines authoritative source and treatment |
| BUDGET-1404-N39-UNIT-01 | Original-budget column mixes Rial and million-Rial scales and contains #REF! cells | Finance/budget owner approves corrected presentation; do not edit source without authorization |

Source workbooks and PDFs are canonical evidence. Keep them byte-identical unless a separately authorized and versioned correction is approved. Never suppress an error merely because it is inconvenient. Exclude only demonstrably unused auxiliary cells and zero-balance / approved control-pair effects under the documented accounting rule, while preserving every source row.

Detailed evidence: [Financial Statement Reconciliation FY1402–FY1404](docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md) on PR #90.

### 4.2 Security and identity

Package 9.1 execution report records 136 local backend tests passing on the Windows host, plus Ruff, compileall, pip check, and diff checks. A fresh rerun from the Package 9.1 worktree completed with exit code 0 on 2026-11-11; the report's recorded count is 136. A Starlette/httpx TestClient deprecation warning remains.

Known limitations:
- Package 9.1 supports one local credential identity; it is not a multi-user identity service.
- PBKDF2-to-Argon2id upgrade persistence is not fully wired to the DPAPI vault.
- Session and lockout state is process-memory based.
- Independent recovery copy / second-device restore is not proven.
- No independent security reviewer approval exists.
- G2.1 database-backed identity provider is not wired into HTTP authentication.
- G2.1 lacks durable throttling, persistent sessions/revocation, canonical company foreign-key enforcement, and identity lifecycle audit.
- Malformed Unicode handling and must-change-password enforcement were identified as defects/follow-ups.

The G2.1 report records 142 tests passing for that isolated snapshot, but the worktree contains uncommitted changes and is not a published or production-ready candidate.

### 4.3 Mapping, audit, backup and operations

Synthetic tests are useful but cannot substitute for:
- independently administered append-only / WORM audit receipt anchoring;
- protected production key custody and rotation;
- scheduled encrypted backups and independent off-device copies;
- witnessed restore drills on a separate environment;
- measured RPO / RTO and alerting;
- authorized financial owner sign-off;
- exact-head CI and independent code review.

## 5. Ordered execution roadmap

Work proceeds in the following order. A later phase may be prepared in parallel only when it does not modify shared files, operational data, or depend on an unaccepted predecessor.

### Phase 0 — Freeze, inventory, and establish the control baseline
**Priority:** P0  
**Goal:** one authoritative, recoverable engineering baseline.

Tasks:
1. Publish this plan and make it mandatory for contributors.
2. Inventory all local worktrees, branches, PRs, dirty files and exact SHAs.
3. Create hash-verified snapshots of dirty worktrees before any consolidation.
4. Identify duplicate / superseded branches and map their unique changes.
5. Compare every candidate against its declared parent and accepted base.
6. Reconcile PROJECT_STATUS, PROJECT_LOG, and LATEST_HANDOFF with live GitHub state.
7. Define one candidate integration branch; do not merge automatically.

Acceptance:
- Every worktree has an owner, purpose, SHA, dirty-file manifest, and recovery reference.
- No unexplained dirty files or untracked artifacts remain unclassified.
- The accepted base is unchanged.
- One integration plan and one next action are recorded.

### Phase 1 — Financial exception closure
**Priority:** P0  
**Goal:** convert read-only findings into approved financial dispositions.

Tasks:
1. Obtain accounting-owner decisions for FS-1403-EQ-01 and MAP-8161-01.
2. Verify all seven missing Mapping keys against source-ledger dimensions and note content.
3. Re-run year-separated mapping and note tie-outs after approval, using copies / synthetic fixtures first.
4. Complete note-reference reconciliation for FY1402–FY1404.
5. OCR and inspect full auditor reports and record exact opinion wording.
6. Resolve budget source-cell and unit anomalies with budget owner.
7. Obtain signed finance disposition; keep source files unchanged until separately authorized.

Acceptance:
- Every material exception is CLOSED or explicitly accepted with signed owner rationale.
- Reconciliation is reproducible from hashed source inputs.
- No unexplained non-zero unmapped exposure remains.
- Source integrity hashes match the authorized baseline.

### Phase 2 — Mapping workflow completion
**Priority:** P0  
**Goal:** deterministic, explainable, reversible mapping workflow.

Tasks:
1. Verify account / company / year / dimension key semantics.
2. Enforce deterministic match, ambiguity queue, unmatched queue and explicit review.
3. Preserve mapping provenance, version, actor, timestamp and source hash.
4. Complete bulk import/export, validation and round-trip tests.
5. Verify lifecycle transitions, stale-write handling and concurrent edits.
6. Add drill-down from statement line to note, mapping rule, ledger row and source workbook cell.
7. Add regression fixtures for zero-balance exclusions and approved control pairs without deleting ledger rows.

Acceptance:
- 100% of statement-impacting rows are mapped or explicitly dispositioned.
- Ambiguous matches never silently resolve.
- Re-import / export round-trip preserves values and provenance.
- Company and fiscal-year boundaries are enforced server-side.

### Phase 3 — Identity, authorization and segregation of duties
**Priority:** P0  
**Goal:** secure multi-user operation.

Tasks:
1. Choose and document the identity architecture (trusted enterprise IdP or approved multi-user local authority).
2. Wire one composition root into login, token resolution and every protected API.
3. Persist only token hashes; implement expiry, rotation, revoke-one, revoke-all and disable-user enforcement.
4. Implement persistent atomic throttling / lockout with multi-worker tests.
5. Enforce canonical company and fiscal-year membership using database constraints.
6. Implement maker / reviewer / approver roles and separation-of-duties checks.
7. Enforce must-change-password and account lifecycle.
8. Add durable security audit events and adversarial tests.

Acceptance:
- Multi-user API integration tests pass on the exact candidate SHA.
- Disabled / revoked users lose access immediately.
- Cross-company and cross-year negative tests pass.
- Concurrent workers and restart behavior are verified.
- Independent security review signs off.

### Phase 4 — Audit evidence, backup and disaster recovery
**Priority:** P0  
**Goal:** prove integrity and recoverability.

Tasks:
1. Select an independently administered immutable / append-only audit anchor.
2. Separate application and audit administration credentials.
3. Define key generation, storage, rotation, escrow and recovery ownership.
4. Implement scheduled encrypted backup, retention, monitoring and alerting.
5. Restore to a separate clean Windows host/profile or disposable environment.
6. Run tamper, corruption, missing-receipt and partial-failure drills.
7. Record measured RPO / RTO and independent witness evidence.

Acceptance:
- External audit anchor cannot be silently rewritten by the application administrator.
- Restore succeeds from an off-device backup with documented key recovery.
- Hashes and record counts reconcile after restore.
- RPO / RTO targets are met and independently witnessed.

### Phase 5 — Financial statement engine and reporting
**Priority:** P1  
**Goal:** reproducible five-statement and note generation.

Tasks:
1. Finalize statement line definitions and account/note mapping contracts.
2. Generate all five statements from approved source and mappings.
3. Reconcile cross-statement links, comparative periods, notes and cash.
4. Support approved adjustments with maker/checker/approver evidence.
5. Add explainability from every reported amount to source ledger and rule.
6. Add budget / actual / variance analysis without mixing units or bases.
7. Build regression packs from approved, anonymized or synthetic data.

Acceptance:
- All five statements and notes reconcile under approved accounting rules.
- Every reported figure is traceable.
- No unexplained difference or silent fallback remains.
- Finance owner signs the output.

### Phase 6 — User interface and workflow integration
**Priority:** P1  
**Goal:** complete Persian-first user workflow.

Tasks:
1. Inventory existing UI and identify what is real versus placeholder.
2. Define Persian RTL design system, navigation and error patterns.
3. Implement entity/year selection, import wizard, Mapping workbench, exception queue, statement preview and approval inbox.
4. Add audit history, role-aware actions and accessible validation.
5. Integrate UI with the same authenticated backend APIs.
6. Test real user journeys at normal and failure boundaries.

Acceptance:
- A finance user can complete the end-to-end workflow without direct database or command-line intervention.
- Unauthorized actions are hidden and rejected server-side.
- RTL, Persian digits / formatting, export and accessibility checks pass.

### Phase 7 — Windows packaging, installation and release
**Priority:** P1  
**Goal:** supported, reproducible V1 release.

Tasks:
1. Build reproducible signed installer.
2. Test clean installation, upgrade, uninstall and rollback.
3. Verify runtime dependencies, DPAPI behavior, file permissions and local database paths.
4. Run end-to-end tests on a clean Windows machine.
5. Produce operator, administrator, backup, recovery and troubleshooting manuals.
6. Tag release only after independent approvals.

Acceptance:
- Clean-machine installation and upgrade succeed.
- No secrets or production data are embedded in package/logs.
- Security, finance, operations and product acceptance are recorded.
- Release artifact hash and source commit are published.

## 6. Definition of Done for every work package

Every PR must include:
- problem statement and explicit scope;
- base branch and exact base SHA;
- changed-file list and reason for each file;
- data classification and confirmation that canonical data was not altered;
- migration / rollback plan where applicable;
- tests added and exact commands/results;
- lint, type / compile, dependency and diff checks where applicable;
- CI result on exact final head SHA;
- security and financial-control impact;
- screenshots / logs / evidence for UI or operational work;
- known limitations and owner dependencies;
- reviewer decision and next action.

No author may describe their own self-review as an independent approval. No test result may be claimed for a different SHA.

## 7. Non-negotiable safety rules

1. Never edit canonical financial XLSX/PDF, source ledgers, mapping workbooks, or operational databases without a separately scoped explicit authorization.
2. Never delete, net, suppress, or discard source ledger rows to make totals reconcile.
3. Never infer a control-account offset from equal amounts alone; require accounting classification and evidence.
4. Never merge, release, deploy, force-push, reset, or clean a dirty worktree as part of routine autonomous work.
5. Never store credentials, tokens, recovery passphrases, or private keys in Git, logs, test artifacts, or ordinary backups.
6. Use synthetic or anonymized fixtures for development and destructive tests.
7. Fail closed when identity, tenant scope, audit anchor, or recovery configuration is missing.
8. Distinguish code-complete, locally-tested, CI-verified, independently-reviewed, finance-approved, operationally-accepted, and released states.
9. A green unit-test suite does not prove financial correctness, security readiness, or disaster recovery.
10. Update this control plan and handoff after every accepted work package.

## 8. Immediate next actions (ordered)

1. Treat this plan as the mandatory control document for all future work.
2. Preserve and hash-inventory every dirty local worktree before consolidation.
3. Re-read live PR #82, #88, #89, and #90 metadata and exact head SHAs.
4. Create a file-level change ownership matrix to identify duplicated and unique changes.
5. Reconcile the repository's status and handoff documents on a dedicated documentation branch.
6. Obtain accounting-owner disposition for FS-1403-EQ-01 and MAP-8161-01.
7. Do not start another overlapping Gate 3 / identity implementation branch.
8. After Phase 0 is accepted, select one smallest safe code correction with a regression test and submit a focused Draft PR.

## 9. Change log

| Date | Change |
|---|---|
| 2026-11-11 | Initial master control plan created from read-only GitHub and Aram Windows host inspection. No canonical data, local worktree, merge, release or deployment changed. |

## 10. Latest handoff

**Current control branch:** `docs/aram-master-control-plan-20261111`  
**Accepted base:** `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`  
**Current decision:** NO-GO for production.  
**Next executable task:** Phase 0 file-level inventory and preservation of all local dirty worktrees.  
**Do not:** merge existing Draft PRs, modify canonical financial data, reset/clean local worktrees, or start a duplicate implementation.
