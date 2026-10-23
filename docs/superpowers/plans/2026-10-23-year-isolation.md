# Fiscal-year Isolation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Close the reproduced protected-ownership and relationship-based cross-year reference gaps.

**Architecture:** Extend the existing before-flush hook with persisted-origin checks and change-aware relationship resolution. Keep database schema and dependencies unchanged.

**Tech Stack:** Python 3.12, SQLAlchemy, pytest, SQLite, Alembic.

**Spec:** `docs/superpowers/specs/2026-10-23-year-isolation-design.md`

## Global Constraints

- Exact base: `7dc864fd032f0c4ae4d650d89304a01286a6d914`; branch `source-data-cleanup`.
- No dependency, workflow, migration, canonical XLSX/PDF, `data/`, persisted database, financial-source value, binary or release change.
- No recovery from closed PR #7 and no acceptance or merge of other draft PRs.
- Application scope: `backend/src/aram_backend/models.py` and `backend/tests/test_models.py`.
- Control records: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, and this design/plan pair.

## Review Focus

- Original owner is unloaded/expired: moving data must still detect its protected source year.
- Parent relationship was cached before a direct FK change: inspect the proposed parent, not the old cache.
- New relationship-only statement-note reference: validate before FK synchronization.
- Both a relationship and FK are supplied inconsistently: reject conflicting identities.
- No target note and valid Draft-only edits: preserve allowed operations.

### Task 1: Enforce original and proposed ownership

**Files:** Modify `backend/src/aram_backend/models.py`; test `backend/tests/test_models.py`.

**Interfaces:** Existing ORM models and `enforce_audit_invariants`; private helpers may resolve persisted ownership and effective parents. No public API changes.

- [x] Write regressions for moving AccountVersion and year-owned model variants from Approved/Locked to Draft, including expired ownership; assert rejection plus unchanged stored state after rollback.
- [x] Add raw-FK and relationship reparenting regressions for NoteRow and StatementLine leaving protected years; retain valid Draft-only operations.
- [x] Run the new regressions on unchanged production code; expected meaningful failures proving the bypasses.
- [x] Resolve original ownership by persisted identity, then enforce protection on original and proposed years before flush.
- [x] Run the focused regressions and full `PYTHONPATH=src python -m pytest`; expected all pass.

### Task 2: Enforce effective statement-note reference identity

**Files:** Modify the same two application files.

**Interfaces:** Private `_resolve_parent_year_id` and the existing same-year invariant.

- [x] Add regressions for relationship-only cross-year/cross-company statement-note creation, cached-parent raw-FK updates, conflicting relationship/FK values, and valid same-year/no-target cases.
- [x] Run new regressions before changing resolution; expected invalid references fail their rejection assertions.
- [x] Resolve effective parent using relationship/FK change history, reject conflicting assignments, and remove the FK-population gate from optional note validation.
- [x] Run focused regressions and the full suite; expected all pass.

### Task 3: Record and publish evidence

**Files:** The three control records and design/plan pair.

**Interfaces:** Repository acceptance policy and PR template.

- [x] Correct the obsolete PR #21 status using verified remote merge evidence; record this new candidate separately as unaccepted.
- [x] Record exact changed paths, tests, risks, rollback and remaining Peyvast/mapping work; append the project log.
- [x] Run isolated migration upgrade/downgrade, compile and `git diff --check`; expected success and no protected-path diff.
- [x] Obtain independent whole-branch review and resolve material findings with regressions.
- [x] Publish a dedicated remote branch and focused Draft PR; verify final-head GitHub Actions and record its real URL. Do not self-merge.
