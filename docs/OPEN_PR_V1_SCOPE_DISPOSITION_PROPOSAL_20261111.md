# Aram — V1 Scope and Disposition Proposal for 55 Open PRs

**Prepared:** 2026-11-11  
**Repository:** `davoodmehraban89/Aram`  
**Accepted baseline:** `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`  
**Status:** PROPOSAL ONLY — no PR merged, closed, retargeted or deleted.

## 1. Executive summary

The live GitHub inventory contains 55 open PRs, all Draft, organized into 13 dependency families:

| Root PR | Family size | Workstream | Proposed disposition |
|---:|---:|---|---|
| 22 | 1 | Repository hygiene / README | Review useful README-only changes; reconcile status/log with new control docs |
| 23 | 1 | Dependency security audit | Retain as candidate; exact-head audit and backend CI evidence exists; reconcile pyproject with runtime imports |
| 24 | 1 | Read-only Mapping diagnostic baseline | Preserve as historical evidence; likely superseded by fresh PR #90 and implementation PR #60; review before close |
| 25 | 1 | Explicit reversible Alembic schema | Retain as migration candidate; validate against identity metadata and final schema contract |
| 26 | 17 | Gate 3 Mapping core and hardening | HOLD as one dependent chain; no child promotion until fiscal-year safety and independent Gate 3 acceptance |
| 29 | 1 | ADR-012 Excel-first V1 / future Peyvast | Retain as proposed architecture decision; owner / governance acceptance required |
| 32 | 3 | Fiscal-year ownership and note isolation | Critical P0 safety candidate; complete same-flush / graph-wide / lifecycle gates and independent tests |
| 34 | 1 | 5+1+3 governance proposal | Hold for owner decision; reconcile with current master plan before acceptance |
| 44 | 1 | Older roadmap dashboard proposal | Likely superseded by PR #91; preserve historical evidence, compare before close |
| 60 | 22 | Read-only Mapping coverage, five-statement engine and Windows pilot | HOLD as one stacked V1 candidate chain; do not merge child PRs individually |
| 82 | 4 | Gate 3 / Package 9 / Security 9.1 | FINAL NO-GO family; preserve as evidence, no merge or release until external gates pass |
| 90 | 1 | Financial reconciliation | Retain as financial evidence candidate; owner decisions remain open |
| 91 | 1 | Master control plan / execution dashboard | Retain as control-doc candidate; independent review required |

## 2. Family-level recommendations

### Family rooted at PR #22 — repository hygiene

**Members:** #22.

- Useful scope: README restoration and historical V1-01 status reconciliation.
- Risk: overlaps `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, and `docs/handoff/LATEST_HANDOFF.md`, now also changed by PR #91.
- Recommendation: review and selectively retain README-only improvements; do not overwrite the new control/status record with stale PR #21 next actions.

### Family rooted at PR #23 — dependency audit

**Members:** #23.

- Exact-head evidence in the PR body reports successful dependency audit and Backend CI.
- Recommendation: retain as a candidate, but reconcile `backend/pyproject.toml` with the final runtime dependency set and current security code before merge.
- Do not assume a historical audit result covers later dependency changes.

### Family rooted at PR #24 — diagnostic baseline

**Members:** #24.

- Documentary baseline only; its own description says the canonical XLSX was not opened and a fresh workbook-level diagnostic remains pending.
- Recommendation: preserve as historical evidence; likely superseded by the direct workbook validation in PR #90 and read-only preview chain rooted at #60. Close only after confirming no unique evidence is lost.

### Family rooted at PR #25 — explicit migrations

**Members:** #25.

- Exact-head CI / migration tests are recorded in its PR body.
- Recommendation: retain as a migration candidate. Reconcile it with the final identity schema decision and the G2.1 `IdentityBase` metadata requirement. Test upgrade/downgrade against disposable databases containing existing synthetic financial tables.

### Family rooted at PR #26 — Gate 3 Mapping core

**Members:** #26, #27, #28, #30, #31, #45, #46, #47, #50, #51, #52, #53, #54, #55, #56, #57, #59.

- This is a 17-PR stacked family: persistence, Excel interchange, coverage, carry-forward, review, stale-note/hidden-content guards, draft staging, identity, and desktop staging.
- PR #26 itself says the fiscal-year safety work in PR #32 is a prerequisite and that the ORM-only year protection is not a raw/bulk SQL or concurrency guarantee.
- Recommendation: hold the entire family as an integration unit. Do not merge the final child or cherry-pick isolated pieces until PR #32 / #35 safety gates are accepted, branch ancestry is rebased to the accepted SHA, and independent financial/security reviews pass.
- Preserve the reviewer-identity fix from the isolated G1/G2.1 worktree; do not accept the Gate3 variant that replaces reviewer with approver on approval.

### Family rooted at PR #29 — ADR-012

**Members:** #29.

- The PR body records the owner direction: Excel/CSV and Windows-first V1; Peyvast as a later provider-neutral connector.
- Recommendation: retain as an architecture proposal; confirm its wording is consistent with the master control plan and obtain governance acceptance before treating it as binding.

### Family rooted at PR #32 — fiscal-year safety

**Members:** #32, #33, #35.

- This family contains protected fiscal-year ownership, note isolation, same-flush follow-up and Peyvast discovery.
- PR #35 records remaining same-flush, direct non-Draft creation and graph-wide move gaps.
- Recommendation: treat as P0 safety work. Complete the missing invariants and tests before accepting Mapping persistence, approval or connector work. Do not treat a passing subset as complete fiscal-year safety.

### Family rooted at PR #34 — governance proposal

**Members:** #34.

- Proposes five specialist responsibilities + one operational manager + three independent acceptance controls; its own body states it is not accepted.
- Recommendation: hold for owner decision. Reconcile roles, reserved decisions and acceptance authority with the new master plan; do not silently supersede existing ADRs.

### Family rooted at PR #44 — older roadmap dashboard

**Members:** #44.

- Proposes a different seven-gate / weighted dashboard and explicitly says its weights require owner approval.
- Recommendation: treat as historical proposal likely superseded by PR #91's eight-phase evidence-based dashboard. Preserve its unique decisions/evidence, then close with a supersession record only after review.

### Family rooted at PR #60 — read-only Mapping and five-statement / Windows chain

**Members:** #60–#81 (22 PRs).

- This is a long stacked chain from read-only Mapping coverage through reconciliation, balance sheet, income statement, equity, cash flow, multi-statement pipeline, CLI hardening, Windows pilot and source drill-down.
- Several child PRs intentionally touch the same desktop and pipeline files. The changed-file matrix identifies these overlaps; they are not automatically conflicts.
- Recommendation: keep as one candidate workstream. Validate the full final child against its immediate base and the accepted baseline; run exact-head tests on a clean Windows machine; verify all displayed values remain non-official until owner approval; do not merge each child independently.

### Family rooted at PR #82 — Gate 3 / Package 9 / Security 9.1

**Members:** #82, #88, #89, #92.

- PR #82 explicitly states FINAL NO-GO due to missing independent signoffs and operational evidence.
- PR #88/#89 are downstream isolated candidates; PR #92 is a security child based on #89, not the accepted baseline.
- Recommendation: preserve this family as a no-go evidence record. Do not merge, release, or treat #92's focused fix / green tests as approval of the parent security design. Require independent security review, persistent session/throttling evidence, DR proof, and accounting/operations signoffs.

### Family rooted at PR #90 — financial reconciliation

**Members:** #90.

- Read-only reconciliation, account 8161 seven-rule proposal and simulation, equity root-cause refinement, duplicate Note 23, budget unit and #REF! findings, partial auditor PDF review.
- Recommendation: retain as the current financial evidence candidate. Obtain accounting and budget-owner dispositions before changing any canonical workbook; full auditor review remains open.

### Family rooted at PR #91 — master control and dashboard

**Members:** #91.

- Documentation-only master plan, eight-phase dashboard, worktree ownership, 62-file disposition, 55-PR inventory/dependency graph and 427-entry file overlap matrix.
- Recommendation: retain as the single control-document candidate after independent review. It does not authorize code merges or production release.

## 3. Cross-family blockers

1. **Control-document contention:** `docs/PROJECT_LOG.md` appears in 45 PRs, `docs/handoff/LATEST_HANDOFF.md` in 41, and `PROJECT_STATUS.md` in 31. Consolidate these documents once on a reviewed control branch; never wholesale-copy branch-local status files.
2. **Runtime dependency contention:** `backend/pyproject.toml` appears in multiple security / migration candidates. Resolve from actual runtime imports and clean installation.
3. **Security / API composition:** `backend/src/aram_backend/main.py` is touched by multiple auth / Gate 3 PRs. Review the complete router and principal composition before integration.
4. **Windows five-statement chain:** several desktop source, test and workflow files are shared across PRs #75–#80. Compare each child to its immediate parent to avoid duplicate patches.
5. **Mapping lifecycle:** preserve reviewer identity and review timestamp at approval; approver identity belongs in the audit event.
6. **Migration metadata:** decide whether identity schema is in the V1 candidate and ensure Alembic target metadata includes exactly the accepted models.

## 4. Proposed disposition vocabulary

- `KEEP_CANDIDATE`: unique in-scope work; review and rebase before integration.
- `HOLD_DEPENDENCY_CHAIN`: do not merge independently; parent chain must be accepted first.
- `HOLD_NO_GO`: explicit safety / acceptance gate failed; preserve evidence.
- `LIKELY_SUPERSEDED`: compare unique changes, archive evidence, then close with a clear reason if nothing remains.
- `OWNER_DECISION_REQUIRED`: product/governance/accounting/security decision is missing.
- `ACCEPTED`: only after merge into accepted baseline with required review and exact-head CI. No open PR in this inventory is accepted.

## 5. Immediate execution order

1. Review PR #32 / #35 fiscal-year safety and record exact remaining invariants.
2. Reconcile the direct-to-baseline migration/dependency candidates #23 and #25.
3. Decide V1 scope for the #60 five-statement/Windows chain.
4. Decide governance and architecture proposals #29, #34 and #44.
5. Reconcile the #22 README candidate with PR #91 control docs.
6. Keep #82/#88/#89/#92 NO-GO until independent security and operations gates pass.
7. Only then create one integration candidate from `source-data-cleanup` with a reviewed commit/file ownership manifest.

**No PR was merged, closed, retargeted, or deleted by this proposal.**
