# Decision Log

Accepted decisions are immutable. To change one, add a new ADR that explicitly supersedes it.

## ADR-001 — GitHub is the source of truth

- Status: Accepted
- Decision: Remote commits, pull requests, CI runs, tags, releases, and downloadable assets outrank agent-written reports.

## ADR-002 — Separate implementation and acceptance

- Status: Accepted
- Decision: Jules or another coding agent may implement. ChatGPT/Codex acts as project manager and independent GitHub reviewer. The repository owner makes the final merge decision.

## ADR-003 — Small reviewable pull requests

- Status: Accepted
- Decision: Each task uses a dedicated branch and a focused PR. Unrelated work is rejected or split.

## ADR-004 — Evidence gates are mandatory

- Status: Accepted
- Decision: No phase is accepted without the correct base SHA, remote commit, exact diff, test evidence, successful required CI, and explicit review.

## ADR-005 — Binary verification

- Status: Accepted
- Decision: EXE/ZIP files require a reproducible build workflow, checksums, retained CI artifacts, and clean-environment execution evidence.

## ADR-006 — Release verification

- Status: Accepted
- Decision: A release is accepted only after its tag, release page, URL, commit, and downloadable assets are independently verified.

## ADR-007 — PR #7 is reference material

- Status: Accepted
- Decision: [PR #7](https://github.com/davoodmehraban89/Aram/pull/7) must not be merged directly. Useful capabilities may be recovered through small, tested PRs from the accepted baseline.

## ADR-008 — Mapping is mandatory for V1

- Status: Accepted
- Decision: Comprehensive Mapping Excel import/export, company/year isolation, unknown-account handling, note mapping, sub-note mapping, and management UI are required before V1 acceptance.

## ADR-009 — Canonical financial data is protected

- Status: Accepted
- Decision: Canonical XLSX/PDF and financial-source files are immutable unless a separately approved data-change task identifies exact files, hashes, rationale, and recovery procedure.

## ADR-010 — Persistent handoff records

- Status: Accepted
- Decision: Every meaningful PR updates `PROJECT_STATUS.md` and appends an entry to `docs/PROJECT_LOG.md`. Work is not complete until the remote evidence is visible.

## ADR-011 — Role-based project operation and current assignments

- Status: Accepted
- Supersedes: ADR-002 where it requires repeated repository-owner merge confirmation or leaves the current division of responsibilities underspecified.
- Decision: Project work is governed by five durable roles: Project Owner, Operational Coordinator, Primary Implementation Agent, Senior Technical Supervisor / Independent Reviewer / Authorized Maintainer, and GitHub as the evidence source of truth.
- Current assignment: Davood is Project Owner and the accounting/product authority.
- Current assignment: ChatGPT chat is the Operational Coordinator and prepares focused tasks, implementation prompts, first-pass evidence reviews, and copy-ready handoff packets.
- Current assignment: Jules is the primary Implementation Agent and works through one exact-base branch and focused Draft PR at a time; Jules never merges its own PR.
- Current assignment: Codex Work is the Senior Technical Supervisor, Independent Reviewer, and Authorized Maintainer. It verifies remote evidence, directs technical sequencing, resolves cross-agent conflicts, may make exceptional critical fixes through focused PRs, records acceptance decisions, and has standing delegation for routine merge actions after evidence gates pass.
- Current assignment: GitHub is the authoritative evidence system for accepted branches, commits, PRs, CI, artifacts, Issues, tags, releases, and control records.
- Decision: Davood must not be burdened with routine Git, test, CI, diff, or merge confirmations covered by standing delegation. Accounting ambiguity, material product tradeoffs, protected-data changes, releases, destructive actions, credentials, and new external authority still require escalation.
- Decision: If a tool or model changes, responsibility boundaries remain in force until an accepted governance change records the new assignment.
- Decision: An implementation report is never acceptance evidence. Every acceptance action requires a fresh remote verification against the exact candidate head.
- Rationale: Explicit current assignments remove ambiguity for successors, while durable role boundaries preserve the workflow when tools or models change.

## Pending proposals — not accepted decisions

- **ADR-012 (proposed in Draft PR #29):** Excel-first V1 and future provider-neutral connectors; its unmerged proposal is not a live policy.
- **ADR-013 (proposed in Draft PR #34):** [ARAM 5+1+3 delivery and three independent review controls](adr/ADR-013-aram-5plus1plus3-delivery-governance.md). This is a nonbinding proposal until independently reviewed and merged. It extends ADR-011 without revoking existing roles or routine merge delegation. Reconcile the proposed ADR-012 and ADR-013 numbering and their states before accepting either.
