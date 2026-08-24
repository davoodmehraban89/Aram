# Aram Architecture & Project Decision Log (ADR)

This document records the official **Architecture Decision Records (ADR)** for the Aram repository.

**DECISION LOG RULES**:
- Stable decision IDs (`ADR-001`, `ADR-002`, etc.) must be used.
- Decisions must never be silently altered or deleted; if a decision is superseded, create a new ADR referencing the superseded decision ID.

---

## ADR-001: GitHub Commits, Merges, and CI as Single Source of Truth
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: AI agents may generate text summaries claiming completed tests, release approvals, or code merges that are not reflected in actual GitHub PRs or CI runs.
- **Decision**: GitHub merged PRs, verifiable git commit SHAs, passing GitHub Actions CI runs, and published release tags are the **sole source of truth**. Agent text reports do NOT constitute evidence of project completion.

---

## ADR-002: Agent Role Responsibilities & Governance
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: Clear division of responsibilities is required between automated implementation agents and project oversight.
- **Decision**:
  - **Jules**: Acts as implementation engineer responsible for coding, testing, and submitting narrow Pull Requests.
  - **ChatGPT Manager**: Acts as project manager, independent reviewer, and custodian of project state.

---

## ADR-003: Small, Independently Reviewable Pull Requests
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: Large monolithic PRs combining multiple phases introduce hidden regressions and make independent review impossible.
- **Decision**: All work must proceed through small, focused PRs targeting a single objective or sub-phase. Broad multi-phase PRs will be rejected.

---

## ADR-004: GitHub CI Evidence Requirement
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: Local test runs in sandboxes may pass while failing in production CI environments.
- **Decision**: No Pull Request or phase is accepted without passing GitHub Actions CI runs (`.github/workflows/ai-review.yml`).

---

## ADR-005: Independent Verification of Binary Artifacts & Releases
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: AI agents may claim to build ZIP or EXE release packages locally that are never published to GitHub.
- **Decision**: Binary artifacts (ZIP, EXE) and GitHub Releases are NOT accepted until the release tag, release page URL, and downloadable release assets are independently verified on GitHub.

---

## ADR-006: Treatment of Unmerged Prototype PR #7
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: PR #7 contains extensive backend, desktop, and documentation code created during an earlier iteration, but was closed unmerged without independent CI validation.
- **Decision**: PR #7 MUST NOT be merged directly into `source-data-cleanup`. Code from PR #7 may only be used as a reference/recovery source when re-implementing phases through reviewable PRs.

---

## ADR-007: Mandatory Comprehensive Financial Mapping Engine Before V1
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: Financial statement generation requires mapping raw ledgers to Chart of Accounts categories, notes, and sub-notes.
- **Decision**: Aram cannot be accepted as V1-ready without a complete, verified Mapping engine supporting Excel template import/export, note/sub-note mapping, and a dedicated Mapping UI.

---

## ADR-008: Absolute Protection of Canonical Financial Sources
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: Original Excel files, CSV ledgers, and auditor PDFs in `data/` represent authoritative historical evidence.
- **Decision**: Canonical source files under `data/` are strictly **immutable**. Systems and parsers must read them in read-only mode and never modify, overwrite, or re-save them.

---

## ADR-009: Strict Fiscal-Year Status Protection & Immutability
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: Financial reporting platforms require strict audit protection against retroactive manipulation of finalized financial years.
- **Decision**: Any fiscal year marked as `Approved` or `Locked` is strictly immutable. Ingestion, normalization, or snapshot modification requests targeting approved/locked years must be rejected with `LockedFiscalYearError`.

---

## ADR-010: Database Security Boundary & API Isolation
- **Date**: 2026-08-23
- **Status**: `ACCEPTED`
- **Context**: Exposing database connection strings or credentials to client interfaces introduces severe security vulnerabilities.
- **Decision**: Database connection settings must remain internal to the backend service layer. Desktop and web clients must interact exclusively via authenticated REST API endpoints (`/api/v1/`).
