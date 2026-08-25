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

## ADR-011 — Tool-neutral role-based project operation

- Status: Accepted
- Supersedes: ADR-002 only where it binds responsibilities or routine merge authority to specific tool names or to repeated owner confirmation.
- Decision: Project work is governed by five durable roles: Project Owner, Operational Coordinator, Implementation Agent, Independent Reviewer / Authorized Maintainer, and GitHub as the evidence source of truth.
- Decision: The Operational Coordinator restores context, converts product intent into one focused task, prepares implementation prompts, performs first-pass evidence review, and produces a reviewer-ready evidence packet.
- Decision: The Implementation Agent works only from an exact verified base, uses one focused branch and PR, runs required checks, publishes evidence, and never merges its own PR.
- Decision: The Independent Reviewer / Authorized Maintainer re-fetches remote evidence, verifies the complete diff, tests, CI, artifacts, protected-data boundary, and rollback, then records accept/reject/revise and may merge only under recorded standing or task-specific authority.
- Decision: Davood remains the Project Owner and accounting/product authority. Routine technical confirmations must not be escalated to him when valid delegation is already recorded; accounting ambiguity, material scope expansion, protected-data changes, releases, destructive actions, and new external authority must still be escalated.
- Decision: A tool may perform more than one role only when repository policy and recorded authority permit it; it must state the active role and perform a fresh remote verification before any acceptance action.
- Rationale: Stable roles survive changes in products, models, plugins, and agents while preserving separation between implementation claims and acceptance evidence.
