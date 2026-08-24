# Aram Project Status & Control Entry Point

This file serves as the **canonical entry point** at the repository root for human developers, AI agents (Jules, ChatGPT Manager), and project stakeholders. It reflects verified facts from GitHub merges, commits, and CI pipelines, providing an authoritative overview of project state and governance.

---

## 1. Baseline Metadata
- **Repository**: `davoodmehraban89/Aram`
- **Default Branch**: `source-data-cleanup`
- **Current Accepted Baseline Commit**: `f8084268c1080595d9da672d490834ed677ad77f` (Merge PR #4: *Correct Phase 1B-2 Validation Blockers*)
- **Expected Baseline Reference**: `5122fd052ebe0ffe0e07dbb8153a872a4f047355` (Historical baseline reference before PR #4 consolidation)
- **Current Product Objective**: Transition Aram from monolithic JavaScript/HTML prototype to a modular, production-grade financial reporting platform with a persistent database, multi-layer account drill-down, and strict audit compliance.

---

## 2. Project State Categorization Matrix

| Feature / Phase / Artifact | State | Status Details & Verified Evidence |
| :--- | :---: | :--- |
| **Phase 1B-1 Audit Report** | `VERIFIED_AND_MERGED` | Merged via PR #1 (`cd07409`). Authoritative source file inventory & classification. |
| **Phase 1B-2 Validation & Metadata Fix** | `VERIFIED_AND_MERGED` | Merged via PR #4 (`f808426`). Canonical financial XLSX/PDF alignment and lineage validation. |
| **PR #6 (Phase 2A Foundation)** | `VERIFIED_AND_MERGED` | Merged backend foundation PR. Implements core SQLAlchemy models & FastAPI scaffolding. |
| **PR #8 (Code Health Refactor)** | `VERIFIED_AND_MERGED` | Merged single-file refactor (`ce77f75`) restoring FY1402 equity official statement figures. |
| **PR #7 (Phase 2A Parallel Prototype)** | `VERIFIED_BUT_UNMERGED` | Closed & unmerged PR containing parallel prototype code (`backend/`, `desktop/`, `dist/`). Useful as recovery/reference source only. |
| **PR #9 (Phase 2B Source Ingestion)** | `IN_PROGRESS` | Open draft PR for Phase 2B source ingestion framework. Must NOT be treated as merged. |
| **Accepted Default Branch V1 Assets** | `NOT_IMPLEMENTED` | `source-data-cleanup` branch does NOT currently contain `desktop/`, `dist/`, or V1 release assets from PR #7. |
| **v1.0.0-pilot GitHub Release** | `CLAIMED_BUT_NOT_PROVEN` | Claimed release artifacts (ZIP/EXE) are unverified on GitHub releases; no official release accepted on `main` or default branch. |
| **Comprehensive Financial Mapping UI** | `NOT_IMPLEMENTED` | Comprehensive Mapping Excel import/export, note mapping, sub-note mapping, and Mapping management UI are incomplete on baseline branch. |
| **Canonical Financial Source Protection** | `VERIFIED_AND_MERGED` | Canonical files under `data/` are strictly immutable and protected by project directives. |

---

## 3. Pull Request Index

### Merged & Accepted PRs
- **PR #1**: Phase 1B-1 Audit Report & Data Folder Organization (`cd07409`)
- **PR #4**: Phase 1B-2 Validation Blockers Correction (`f808426`)
- **PR #6**: Phase 2A Backend Foundation
- **PR #8**: FY1402 Equity Official Statement Figures Refactor (`ce77f75`)

### Open & Unmerged PRs
- **PR #9**: Open Draft PR for Phase 2B Source Ingestion Engine.

### Closed / Unmerged Reference PRs
- **PR #7**: Closed parallel V1 prototype. Contains backend/desktop scaffolding, installer guides, and claimed test suites. Unmerged and must NOT be treated as accepted baseline code.

---

## 4. Current CI & V1 Readiness Status
- **Current CI Status**: GitHub Actions pipeline configured for unit/coverage execution (`.github/workflows/ai-review.yml`).
- **V1 Product Readiness**: **NOT V1-READY**. Current baseline requires completing Phase 2B (Ingestion Engine), Phase 3 (Normalization), Phase 4 (Accounting Engine), and comprehensive Chart of Accounts / Note Mapping UI before V1 acceptance.

---

## 5. Known Risks & Governance Blockers
1. **Agent Claim Inflation Risk**: AI agents claiming release readiness or test pass rates from local unmerged branches without GitHub CI evidence.
2. **Data Mutability Risk**: Accidental modification of immutable canonical Excel/PDF source files under `data/`.
3. **Branch Drift Risk**: Committing features to parallel branches without merging into `source-data-cleanup` baseline.

---

## 6. Next Approved Action
- Complete independent review of this documentation-control PR.
- Proceed with Phase 2B (Source Ingestion Engine) via narrow, reviewable PRs following `docs/ACCEPTANCE_POLICY.md`.

---

## 7. Project Documentation Index
- **Chronological Work Log**: [`docs/PROJECT_LOG.md`](docs/PROJECT_LOG.md)
- **Architecture Decision Log**: [`docs/DECISION_LOG.md`](docs/DECISION_LOG.md)
- **Acceptance Policy & Gates**: [`docs/ACCEPTANCE_POLICY.md`](docs/ACCEPTANCE_POLICY.md)
- **Agent Task Template**: [`docs/JULES_TASK_TEMPLATE.md`](docs/JULES_TASK_TEMPLATE.md)
- **Pull Request Template**: [`.github/pull_request_template.md`](.github/pull_request_template.md)
