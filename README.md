# Aram — Persian Financial Statements

Aram is an on-premise-oriented financial reporting project intended to generate auditable Persian financial statements from ledger sources and approved mapping rules. **The accepted branch is a backend foundation, not a released product.**

## Authoritative project records

- [Project status](PROJECT_STATUS.md)
- [Agent instructions](AGENTS.md)
- [Acceptance policy](docs/ACCEPTANCE_POLICY.md)
- [Decision log](docs/DECISION_LOG.md)
- [Latest handoff](docs/handoff/LATEST_HANDOFF.md)

## Working principles

The accepted branch is `source-data-cleanup`. Verify its exact remote HEAD before working. Use one focused branch and Draft PR per task. Canonical `data/` sources are read-only. Financial calculations must use exact Decimal Rials; ledger rows must satisfy opening + debit − credit − closing = 0. Accounting interpretation and changes to mapping/reclassification/approval logic require owner review.

## Current scope

The repository includes backend models, ingestion/preflight foundations and a quarantined legacy `index.html`; it is **not** a usable end-to-end Persian financial-statement application. The intended product includes BS, IS, CF, EQ, notes, reconciliation to official statements, an RTL/Jalali review UI and reproducible on-prem packaging. See `PROJECT_STATUS.md` for verified progress and outstanding work.

## Development

Inspect `backend/` for the Python application, tests and Alembic configuration. Follow the actual repository workflow and `AGENTS.md`; do not treat this README as evidence of passing tests or CI.

## Recommended branch protection

Protect `source-data-cleanup`: require pull requests, at least one independent approval, passing backend and security checks, no force-push or branch deletion, and resolution of review conversations. Confirm the actual GitHub check names before enabling required checks. These settings are recommendations, **not verified as enabled**.
