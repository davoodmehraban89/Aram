# Aram Local Worktree Change Ownership Matrix

**Date:** 2026-11-11  
**Device:** Aram (Windows)  
**Snapshot:** `%LOCALAPPDATA%\Aram\ControlBaseline\20261111-0935`  
**Repository baseline:** `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`  
**Purpose:** classify local dirty state before any consolidation. This report does not authorize merging, copying, deleting, or cleaning any worktree.

## 1. Preservation result

Six known worktrees were inspected. The snapshot copied every modified, staged, or untracked file and retained each worktree's Git status and binary patches.

| Worktree | Dirty / untracked files | Branch | HEAD |
|---|---:|---|---|
| Aram-Engineering-Review | 5 | `local-gate3-verification-20261101` | `da06ab3c37d789e565245f2f6ee38183a6f66fb6` |
| Aram-G1-Isolated | 9 | `feat/aram-g1-architecture-20261103` | `18d6aa122d9486116c08d6e66b22675e0ebb1792` |
| Aram-G2.1-Isolated | 13 | `feat/aram-g2-1-identity-20261103` | `18d6aa122d9486116c08d6e66b22675e0ebb1792` |
| Aram-Gate3-Implementation | 34 | `feat/gate3-governed-mapping-20261101` | `9d346f098a0a2159d96080715322879b08d9a1f8` |
| Aram-Gate3-Package9-Isolated | 1 | `feat/gate3-package9-isolated-20261103` | `a0b72be87720b1ff08361298b903ba57dd4fb408` |
| Aram-Gate3-Package9-1-Security | 0 | `feat/gate3-package9-1-security-20261103` | `18d6aa122d9486116c08d6e66b22675e0ebb1792` |

**62 of 62 copied files passed SHA-256 source-to-snapshot verification.** Zero mismatches were observed. The manifest files are `manifest.csv` and `manifest.json` in the snapshot directory. This snapshot is local to the same Windows machine; it is not an off-device backup.

## 2. Overlap summary

There are 10 repository paths modified/untracked in more than one worktree:

- 3 path groups have identical file content across their copies.
- 7 path groups contain different content and must not be blindly copied or cherry-picked.
- The six worktree file counts sum to 62 entries. The overlap analysis found 10 shared path names.

| Path | Worktrees | Content relation | Required handling |
|---|---|---|---|
| `backend/migrations/env.py` | G2.1, Gate3-Implementation | Conflict | Reconcile Alembic metadata: G2.1 includes IdentityBase; Gate3 version omits it |
| `backend/pyproject.toml` | G1, G2.1, Gate3-Implementation | Conflict | Compare runtime vs test dependencies; G1/G2.1 include argon2-cffi and cryptography as runtime dependencies; Gate3 version differs |
| `backend/src/aram_backend.egg-info/dependency_links.txt` | Engineering-Review, G1 | Identical generated file | Build artifact; do not merge as source |
| `backend/src/aram_backend.egg-info/PKG-INFO` | Engineering-Review, G1 | Conflict / generated | Regenerate from final pyproject; do not merge |
| `backend/src/aram_backend.egg-info/requires.txt` | Engineering-Review, G1 | Conflict / generated | Regenerate from final pyproject; do not merge |
| `backend/src/aram_backend.egg-info/SOURCES.txt` | Engineering-Review, G1 | Conflict / generated | Regenerate from final source tree; do not merge |
| `backend/src/aram_backend.egg-info/top_level.txt` | Engineering-Review, G1 | Identical generated file | Build artifact; do not merge as source |
| `backend/src/aram_backend/mapping_workflow.py` | G1, G2.1, Gate3-Implementation | Conflict | Preserve G1/G2.1 reviewer on approval; Gate3 version overwrites reviewer with approver |
| `backend/tests/test_mapping_workflow.py` | G1, G2.1, Gate3-Implementation | Conflict | G1/G2.1 assert reviewer preservation; Gate3 variant removes those assertions |
| `docs/ARAM_G1_EXECUTION_REVIEW_20261103.md` | G1, G2.1 | Identical | Duplicate evidence file; retain one canonical copy when consolidation is approved |

## 3. Material conflicts confirmed by direct diff

### 3.1 Mapping reviewer preservation — do not accept the Gate3 variant as-is

G1/G2.1 contain logic that preserves the reviewer identity and review date when the item transitions to Approved; the approver is recorded in the audit event. Gate3-Implementation instead writes the approver into the reviewer field and replaces the review date during approval. Its tests also remove the reviewer-preservation assertions.

This is a financial segregation-of-duties evidence defect. Preserve the G1/G2.1 behavior and its regression assertions unless a documented product decision explicitly changes the control model.

### 3.2 Runtime dependency conflict

G1/G2.1 move `argon2-cffi` and `cryptography` into runtime dependencies. Gate3-Implementation has a different dependency layout: Argon2id is absent from the runtime dependency list and cryptography remains in the test extra. The final package cannot safely rely on test-only dependencies for runtime security functions.

Resolve the final dependency contract from actual import/runtime use and verify a clean installation. Do not copy one pyproject file without checking all source modules and installer requirements.

### 3.3 Alembic metadata conflict

G2.1's migration environment includes both financial and identity metadata. Gate3-Implementation's version includes only financial Base metadata. The final migration graph must include identity metadata only if the identity schema is accepted and its migrations are included. Do not merge the env.py variants without a migration-upgrade/downgrade test on a disposable database containing pre-existing synthetic financial tables.

## 4. Generated artifacts

The `backend/src/aram_backend.egg-info/` entries are generated package metadata, not authoritative source code. Their content differs because package metadata changed between worktrees. Preserve the snapshot, but exclude these artifacts from source consolidation and regenerate them from the accepted pyproject / source tree after the dependency contract is decided.

## 5. Recommended ownership and disposition

| Worktree | Disposition |
|---|---|
| Engineering-Review | Keep as a verification record; classify egg-info as generated |
| G1-Isolated | Source of the reviewer-preservation fix and runtime dependency change; retain pending PR / integration review |
| G2.1-Isolated | Source of identity models/provider/migration and associated audit evidence; keep isolated pending identity design decision |
| Gate3-Implementation | Preserve all 34 entries; selectively recover only reviewed changes after conflict resolution; do not wholesale merge |
| Package9-Isolated | Retain the isolated integration test for review; do not assume it is production evidence |
| Package9.1-Security | Clean committed candidate at the inspected SHA; security child fix is tracked separately in Draft PR #92 |

## 6. Immediate decision

- No local worktree was reset, cleaned, deleted, or overwritten.
- No files were copied from one worktree into another.
- No source code from the dirty Gate3 worktree is accepted by this report.
- The next consolidation task is a reviewed file-level merge plan for the three substantive conflict paths, plus a deliberate decision on whether G2.1 identity schema is part of the next candidate.
- Production and Gate 3 remain NO-GO.
