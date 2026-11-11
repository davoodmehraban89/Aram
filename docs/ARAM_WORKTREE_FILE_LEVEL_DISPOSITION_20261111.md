# Aram — File-level Worktree Disposition

Date: 2026-11-11
Snapshot: %LOCALAPPDATA%\Aram\ControlBaseline\20261111-0935

## Verification

- 62 manifest entries examined.
- 62/62 snapshot copies match the manifest SHA-256.
- 62/62 current source files still exist and match the manifest SHA-256.
- 0 source files changed since the snapshot.
- This is a classification proposal, not permission to copy, merge, delete, reset or clean any worktree.

## Disposition counts

| Disposition | Entries |
|---|---:|
| CONFLICT_RECONCILE_MIGRATION_METADATA | 2 |
| CONFLICT_RECONCILE_REVIEWER_PRESERVATION | 3 |
| CONFLICT_RECONCILE_RUNTIME_DEPENDENCIES | 3 |
| EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | 11 |
| EXCLUDE_GENERATED_REBUILD | 10 |
| HOLD_IDENTITY_ARCHITECTURE_GATE | 5 |
| MERGE_REGRESSION_TESTS | 3 |
| RETAIN_AS_CANDIDATE_TEST_OR_TOOL | 15 |
| REVIEW_CI_WORKFLOW | 1 |
| REVIEW_DOCUMENTATION | 1 |
| REVIEW_IMPLEMENTATION_CANDIDATE | 7 |
| REVIEW_MIGRATION_BASELINE | 1 |

## File-level register

| Worktree | Path | Current source | Disposition | Rationale |
|---|---|---|---|---|
| Aram-Engineering-Review | backend/src/aram_backend.egg-info/dependency_links.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-Engineering-Review | backend/src/aram_backend.egg-info/PKG-INFO | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-Engineering-Review | backend/src/aram_backend.egg-info/requires.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-Engineering-Review | backend/src/aram_backend.egg-info/SOURCES.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-Engineering-Review | backend/src/aram_backend.egg-info/top_level.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-G1-Isolated | backend/pyproject.toml | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_RUNTIME_DEPENDENCIES | Resolve runtime imports and clean-install dependency contract; no blind file replacement. |
| Aram-G1-Isolated | backend/src/aram_backend.egg-info/dependency_links.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-G1-Isolated | backend/src/aram_backend.egg-info/PKG-INFO | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-G1-Isolated | backend/src/aram_backend.egg-info/requires.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-G1-Isolated | backend/src/aram_backend.egg-info/SOURCES.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-G1-Isolated | backend/src/aram_backend.egg-info/top_level.txt | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EXCLUDE_GENERATED_REBUILD | Generated package metadata; regenerate from accepted pyproject and source tree. |
| Aram-G1-Isolated | backend/src/aram_backend/mapping_workflow.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_REVIEWER_PRESERVATION | Choose reviewer-preserving lifecycle; do not accept approver-overwrites-reviewer variant. |
| Aram-G1-Isolated | backend/tests/test_mapping_workflow.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | MERGE_REGRESSION_TESTS | Retain reviewer-preservation assertions and combine only compatible tests. |
| Aram-G1-Isolated | docs/ARAM_G1_EXECUTION_REVIEW_20261103.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-G2.1-Isolated | backend/migrations/env.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_MIGRATION_METADATA | Decide identity schema inclusion and test upgrade/downgrade on disposable DB. |
| Aram-G2.1-Isolated | backend/migrations/versions/20261103_02_identity_foundation.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | HOLD_IDENTITY_ARCHITECTURE_GATE | Identity candidate; hold until schema, auth wiring and migration ownership are approved. |
| Aram-G2.1-Isolated | backend/pyproject.toml | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_RUNTIME_DEPENDENCIES | Resolve runtime imports and clean-install dependency contract; no blind file replacement. |
| Aram-G2.1-Isolated | backend/src/aram_backend/identity_models.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | HOLD_IDENTITY_ARCHITECTURE_GATE | Identity candidate; hold until schema, auth wiring and migration ownership are approved. |
| Aram-G2.1-Isolated | backend/src/aram_backend/identity_provider.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | HOLD_IDENTITY_ARCHITECTURE_GATE | Identity candidate; hold until schema, auth wiring and migration ownership are approved. |
| Aram-G2.1-Isolated | backend/src/aram_backend/mapping_workflow.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_REVIEWER_PRESERVATION | Choose reviewer-preserving lifecycle; do not accept approver-overwrites-reviewer variant. |
| Aram-G2.1-Isolated | backend/tests/test_identity_migration.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | HOLD_IDENTITY_ARCHITECTURE_GATE | Identity candidate; hold until schema, auth wiring and migration ownership are approved. |
| Aram-G2.1-Isolated | backend/tests/test_identity_provider.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | HOLD_IDENTITY_ARCHITECTURE_GATE | Identity candidate; hold until schema, auth wiring and migration ownership are approved. |
| Aram-G2.1-Isolated | backend/tests/test_mapping_workflow.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | MERGE_REGRESSION_TESTS | Retain reviewer-preservation assertions and combine only compatible tests. |
| Aram-G2.1-Isolated | docs/ARAM_G1_EXECUTION_REVIEW_20261103.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-G2.1-Isolated | docs/ARAM_G2_1_DEEP_SECURITY_AUDIT_20261103.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-G2.1-Isolated | docs/ARAM_G2_1_EXECUTION_REVIEW_20261103.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-G2.1-Isolated | docs/ARAM_G2_1_S1_0_ENVIRONMENT_GATE_20261103.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-Gate3-Implementation | .github/workflows/backend-ci.yml | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_CI_WORKFLOW | Review permissions, triggers, secrets and exact-head test coverage before adoption. |
| Aram-Gate3-Implementation | backend/migrations/env.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_MIGRATION_METADATA | Decide identity schema inclusion and test upgrade/downgrade on disposable DB. |
| Aram-Gate3-Implementation | backend/migrations/versions/20260820_01_initial_schema.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_MIGRATION_BASELINE | Initial schema migration; verify ancestry, revision graph and upgrade compatibility before integration. |
| Aram-Gate3-Implementation | backend/pyproject.toml | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_RUNTIME_DEPENDENCIES | Resolve runtime imports and clean-install dependency contract; no blind file replacement. |
| Aram-Gate3-Implementation | backend/README.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_DOCUMENTATION | Reconcile instructions with final dependency and runtime contracts. |
| Aram-Gate3-Implementation | backend/src/aram_backend/ingestion.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_IMPLEMENTATION_CANDIDATE | Review imports, API integration, tests and security boundary before selective integration. |
| Aram-Gate3-Implementation | backend/src/aram_backend/ledger_parser.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_IMPLEMENTATION_CANDIDATE | Review imports, API integration, tests and security boundary before selective integration. |
| Aram-Gate3-Implementation | backend/src/aram_backend/local_auth.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_IMPLEMENTATION_CANDIDATE | Review imports, API integration, tests and security boundary before selective integration. |
| Aram-Gate3-Implementation | backend/src/aram_backend/mapping_access.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_IMPLEMENTATION_CANDIDATE | Review imports, API integration, tests and security boundary before selective integration. |
| Aram-Gate3-Implementation | backend/src/aram_backend/mapping_api.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_IMPLEMENTATION_CANDIDATE | Review imports, API integration, tests and security boundary before selective integration. |
| Aram-Gate3-Implementation | backend/src/aram_backend/mapping_store.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_IMPLEMENTATION_CANDIDATE | Review imports, API integration, tests and security boundary before selective integration. |
| Aram-Gate3-Implementation | backend/src/aram_backend/mapping_workflow.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | CONFLICT_RECONCILE_REVIEWER_PRESERVATION | Choose reviewer-preserving lifecycle; do not accept approver-overwrites-reviewer variant. |
| Aram-Gate3-Implementation | backend/src/aram_backend/workbook_inspection.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | REVIEW_IMPLEMENTATION_CANDIDATE | Review imports, API integration, tests and security boundary before selective integration. |
| Aram-Gate3-Implementation | backend/tests/test_gate3_encrypted_backup.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_gate3_recovery_drill.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_ingestion.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_ledger_parser.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_local_auth.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_mapping_access.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_mapping_api.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_mapping_hash_chain.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_mapping_receipts.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_mapping_recovery_quality.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_mapping_store.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tests/test_mapping_workflow.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | MERGE_REGRESSION_TESTS | Retain reviewer-preservation assertions and combine only compatible tests. |
| Aram-Gate3-Implementation | backend/tests/test_owner_acceptance.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tools/gate3_synthetic_cloud_drill.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | backend/tools/gate3_synthetic_cloud_restore.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |
| Aram-Gate3-Implementation | docs/GATE3_PACKAGE8_EXECUTION_REPORT_20261103.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-Gate3-Implementation | docs/GATE3_PACKAGE9_BASELINE_20261103.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-Gate3-Implementation | docs/GATE3_PERSONAL_WINDOWS_ARCHITECTURE_DRAFT.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-Gate3-Implementation | docs/GATE3_SINGLE_PASS_EXECUTION_20261102.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-Gate3-Implementation | docs/PROJECT_LOG.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-Gate3-Implementation | PROJECT_STATUS.md | SOURCE_UNCHANGED_SINCE_SNAPSHOT | EVIDENCE_ONLY_RECONCILE_CONTROL_DOCS | Review for currentness and consistency; never let branch-local status overwrite canonical accepted state. |
| Aram-Gate3-Package9-Isolated | backend/tests/test_local_auth_mapping_integration.py | SOURCE_UNCHANGED_SINCE_SNAPSHOT | RETAIN_AS_CANDIDATE_TEST_OR_TOOL | Keep as candidate evidence; verify relevance, isolation and determinism before adoption. |

## Integration rules

1. Generated egg-info metadata is excluded from source integration and must be regenerated after the accepted dependency contract is fixed.
2. Mapping workflow must preserve reviewer identity and review timestamp on approval; approver identity belongs in the approval/audit event. Keep regression assertions.
3. pyproject.toml variants must be reconciled from actual runtime imports and a clean installation; do not wholesale replace.
4. Alembic env.py variants require a deliberate decision on identity metadata and a disposable-database upgrade/downgrade test.
5. Identity provider/models/migration remain isolated until authentication wiring, tenancy, session persistence and migration ownership are accepted.
6. Gate3 code, tests and synthetic recovery tools are candidates only; their existence or passing isolated tests does not establish production readiness.
7. Branch-local status and log documents are evidence only; canonical status must be reconciled to the accepted remote baseline.

## Next action

Create a reviewed integration plan from this register, then selectively integrate files on a new branch from the accepted baseline. Preserve all original worktrees and snapshots until the integrated candidate passes exact-head tests and independent review.
