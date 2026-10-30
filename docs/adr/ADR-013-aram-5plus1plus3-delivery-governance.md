# ADR-013 (PROPOSED) — ARAM 5+1+3 delivery and verification model

- **Status:** Proposed. **Not accepted or effective** until this governance PR is independently reviewed, all applicable gates pass, and its merge into `source-data-cleanup` is verified.
- **Date:** 2026-10-30
- **Decision owner:** Davood (financial, product, scope, and reserved approvals)
- **Base reviewed:** `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`
- **Relates to:** ADR-001, ADR-003, ADR-004, ADR-008, ADR-009, ADR-010, ADR-011.
- **Numbering:** ADR-012 is already proposed in open PR #29; do not treat either proposal as accepted. Re-check numbering before final merge.

## Decision requested

Run each focused ARAM work item with **one operational project manager, five specialized execution roles and three separately evidenced acceptance controls**. These are **responsibilities**, not a claim that nine independent runtime agents exist.

### Permanent governance and authority

1. **Davood — owner:** final financial/product judgment. Reserved decisions: unresolved accounting policy, material feature scope, actual protected-data modifications, credentials or new external authority, destructive actions, and formal production release.
2. **ARAM Project Manager — coordination:** ChatGPT as operational coordinator, or an explicitly authorized successor. Recover current GitHub state, verify base and dependencies, appoint roles, avoid overlapping paths, collect evidence, escalate reserved decisions, and select one next priority.
3. **Implementation execution — Jules or authorized coding successor:** use exact-base dedicated branch and focused Draft PR; no self-merge. The designated lead may implement multiple specialist functions only when its ability is explicit and it does not self-certify independent controls.
4. **Codex Work — senior technical supervisor, independent reviewer and routine authorized maintainer:** retains standing delegation defined in ADR-011, conditional on actual availability, non-authorship of the change, fresh exact-SHA evidence and all required gates. A reviewer who authored a change must be replaced by another qualified reviewer for that change.
5. **GitHub — evidence of record:** remote PR/ref, checks, reviews, diff, artifacts, releases and durable handoff outrank summaries.

ADR-011's routine merge delegation remains unchanged. This ADR adds specialist accountability and explicit gating. If the reviewer or runtime is unavailable, report `BLOCKED`; never simulate a separate person, account, model or approval.

### Five specialist execution roles

| Role | Accountable delivery | Minimum required evidence |
|---|---|---|
| A1: Financial Accounting Expert | applicable accounting references, trial-balance and note/statement logic, comparative periods, ambiguity register | referenced rules, synthetic fixtures, reconciliation assertions, explicit owner decisions on ambiguity |
| A2: Data Engineering / Excel | validated input, immutable source lineage, versioned mapping, duplicate/idempotency/exception policies, company-year separation | field-level errors, source-to-output trace, atomic import/rollback, hostile-workbook tests |
| A3: Software Architecture / Backend | data model, API, authorization, fiscal-year lock/tenant boundaries, migration/rollback | unit/integration tests, migration round-trip, authorization/isolation checks, impact analysis |
| A4: Frontend / Financial Reporting | accountant-facing Persian RTL forms, mapping review, accessible reports, Excel/PDF and print layouts | UI workflow checks, screenshot/manual-review evidence, reconciliation of exports with backend |
| A5: QA / DevSecOps | test suites, regression matrix, dependency and secret checks, CI, reproducible Windows build | actual SHA-bound Actions runs, clean environment tests, artifacts/hashes when relevant |

Roles may be performed sequentially or by multiple authorized agents, but report the **actual executor and tools**. No assertion of independent parallel agents without actual task execution evidence.

### Three mandatory controls — each bound to one exact candidate SHA

**C1 — Technical & Security Review:** independent non-author reviewer examines complete diff, allowed paths, architecture, dependencies, secrets, access controls, migration/downgrade, test logs and check-run conclusion at head SHA. Decision: `PASS | FAIL | BLOCKED`.

**C2 — Financial Accuracy & Data Integrity:** separately qualified financial reviewer validates relevant debit/credit and opening/closing identities, reporting period and company boundaries, unit/rounding, mapping exceptions, notes/sub-notes, comparisons, and demonstrable row-level lineage using synthetic or explicitly approved test data. Where task is documentation-only or unrelated to financial behavior, mark `PASS (NOT_APPLICABLE: justified)` with rationale, reviewer identity and evidence; never assert financial validation occurred. Decision: `PASS | FAIL | BLOCKED`.

**C3 — Acceptance & Release Governance:** independent acceptance reviewer cross-checks original task, accepted base, full file inventory, exact SHA, outcomes and identities from C1/C2, PR and CI provenance, protected paths, rollback, durable docs, remaining risks, and merge/release delegation. Decision: `ACCEPT | REVISE | REJECT | BLOCKED`.

**C1, C2 and C3 must have three distinct, traceable reviewer identities, each independent of every author of the checked change and of one another.** A sequential three-pass assessment by one LLM can provide useful QA observations but **does not meet independent-review requirements**. Independence is about real reviewer identities and non-authorship, not section names. A model may not approve its own work. If no qualified independent reviewers are available, C1/C2/C3 remain `BLOCKED` and the PR stays Draft/unmerged.

### Work-item protocol

1. **Recover:** read remote `source-data-cleanup` SHA, all active and dependent PRs, Issues, branch checks, ADRs and mandatory handoff/control docs. Reconcile stale text with live GitHub before acting.
2. **Scope:** choose **one small acceptance-testable item**; identify lead A1–A5, collaborators, allowed paths, exact base, dependencies, prohibited actions, fixture provenance, success criteria and rollback.
3. **Implement:** code or docs only within allowlist, no source-financial mutation; execute targeted, negative, regression and integration tests as applicable; maintain explicit failures.
4. **Publish:** dedicated branch, Draft PR, exact changed-file list, reviewable full diff, test commands/results, CI links tied to final head, governance log/handoff.
5. **Review:** C1, C2 and C3 independently record identity, checked SHA, evidence, decision and open issues. `FAIL` or `BLOCKED` means not accepted.
6. **Repair:** return findings to author; on each head change invalidate SHA-bound reviews and repeat affected checks, including acceptance.
7. **Merge:** only delegated maintainer after all gates pass; production release, protected financial changes and reserved owner decisions require Davood's separate approval. No direct accepted-branch writes.
8. **Post-merge:** verify new branch SHA, merge commit, CI, complete change list, Issue states, log/handoff and one next highest-priority action.

### Required evidence record

Record: task identifier, goal, manager, lead/coauthors, exact base SHA, branch/head SHA, PR URL, changed paths, commands and raw results, Actions URLs/conclusions, C1 reviewer/SHA/decision, C2 reviewer/SHA/decision, C3 reviewer/SHA/decision, protected-data confirmation, financial ambiguity register, test artifact hashes if relevant, rollback, risks, and **one** of `ACCEPTED | REVISION_REQUIRED | REJECTED | BLOCKED | UNVERIFIED`.

A successful job does not prove independent review. An open or closed-unmerged PR is not accepted. A Draft PR that merely describes a planned database connector has not implemented it.

### Decision boundaries and migration plan

- Preserve existing ADR-011 role assignments and routine merge authority; add the above accountability gates only after acceptance.
- Do not change other repositories through this decision.
- Existing active Drafts (#22–#33, as discovered 2026-10-30) retain their own base/dependencies. Do not duplicate their technical scopes; review and reconcile them before beginning another implementation PR.
- PR #32 (year-isolation ORM guard) and PR #26 (mapping core) remain separate Draft changes. Their previous green CI cannot be transferred to a rebased head.
- ADR-012 in Draft PR #29 and its Excel-first V1/Peyvast-later proposal is **not accepted** by this ADR.
- If reviewer capacity for three truly independent roles does not exist, use sequential QA internally **but keep acceptance blocked**; obtain an independent reviewer later.

### Rollback

Before merge, close this Draft PR without merge. After an authorized merge, revert the governance commit through a new reviewed rollback PR; do not rewrite accepted decision history, force-push, touch source financial data, or retroactively claim the prior governance was accepted.
