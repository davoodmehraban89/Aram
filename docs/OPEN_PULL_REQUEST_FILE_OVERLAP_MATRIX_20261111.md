# Aram — Open PR File Overlap and Scope Matrix

**Snapshot:** 2026-11-11  
**Repository:** [davoodmehraban89/Aram](https://github.com/davoodmehraban89/Aram)  
**Source:** Live GitHub open PR metadata and the paginated changed-filename listing for every open PR.

## 1. Executive summary

- Open PRs inspected: **55**.
- All 55 are Draft.
- Total changed-file entries: **427**.
- Unique repository paths touched: **221**.
- Paths touched by more than one open PR: **64**.
- PR pairs sharing at least one path: **1048**.
- PRs touching a path matching a financial-source / workbook / migration / security name heuristic: **10**.

This is a path-overlap screen, not a semantic conflict analysis. Stacked child PRs may share files with parents by design. Compare each child against its immediate base before deciding whether overlap is duplication or an independent conflict.

## 2. Per-PR changed-file inventory

| PR | Head branch | Base branch | Files | Paths |
|---|---|---|---:|---|
| [#22](https://github.com/davoodmehraban89/Aram/pull/22) | `codex/t1-repo-hygiene-20261023` | `source-data-cleanup` | 4 | `PROJECT_STATUS.md`<br>`README.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#23](https://github.com/davoodmehraban89/Aram/pull/23) | `codex/t2-ci-hardening-20261023` | `source-data-cleanup` | 2 | `.github/workflows/security-checks.yml`<br>`backend/pyproject.toml` |
| [#24](https://github.com/davoodmehraban89/Aram/pull/24) | `codex/t6a-readonly-diagnostics-20261023` | `source-data-cleanup` | 1 | `docs/T6A_READONLY_DIAGNOSTIC.md` |
| [#25](https://github.com/davoodmehraban89/Aram/pull/25) | `codex/t3-explicit-migrations-20261023` | `source-data-cleanup` | 5 | `backend/migrations/versions/20260820_01_initial_schema.py`<br>`backend/tests/test_migration_ddl.py`<br>`backend/tests/test_migration_schema.py`<br>`docs/PROJECT_LOG.md`<br>`docs/T3_MIGRATION_REVIEW.md` |
| [#26](https://github.com/davoodmehraban89/Aram/pull/26) | `codex/gate3-mapping-core` | `source-data-cleanup` | 5 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/mapping_service.py`<br>`backend/tests/test_mapping_service.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#27](https://github.com/davoodmehraban89/Aram/pull/27) | `codex/gate3-mapping-excel-20261023` | `codex/gate3-mapping-core` | 5 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/mapping_excel.py`<br>`backend/tests/test_mapping_excel.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#28](https://github.com/davoodmehraban89/Aram/pull/28) | `codex/gate3-mapping-coverage-20261023` | `codex/gate3-mapping-core` | 5 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/mapping_coverage.py`<br>`backend/tests/test_mapping_coverage.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#29](https://github.com/davoodmehraban89/Aram/pull/29) | `codex/adr-future-connectors-pi-v1` | `source-data-cleanup` | 4 | `PROJECT_STATUS.md`<br>`docs/PROJECT_LOG.md`<br>`docs/adr/ADR-012-excel-first-future-connectors.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#30](https://github.com/davoodmehraban89/Aram/pull/30) | `codex/gate3-carry-forward-preview-20261023` | `codex/gate3-mapping-core` | 5 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/mapping_carry_forward.py`<br>`backend/tests/test_mapping_carry_forward.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#31](https://github.com/davoodmehraban89/Aram/pull/31) | `codex/gate3-note-mapping-review-20261023` | `codex/gate3-mapping-core` | 5 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/note_mapping_review.py`<br>`backend/tests/test_note_mapping_review.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#32](https://github.com/davoodmehraban89/Aram/pull/32) | `codex/v1-year-isolation-followup-20261023` | `source-data-cleanup` | 7 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/models.py`<br>`backend/tests/test_models.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-23-year-isolation.md`<br>`docs/superpowers/specs/2026-10-23-year-isolation-design.md` |
| [#33](https://github.com/davoodmehraban89/Aram/pull/33) | `codex/payvast-mapping-discovery-20261023` | `codex/v1-year-isolation-followup-20261023` | 6 | `PROJECT_STATUS.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/integrations/PAYVAST_SQLSERVER_DISCOVERY.md`<br>`docs/integrations/payvast-schema-discovery.sql`<br>`docs/superpowers/specs/2026-10-23-payvast-governed-mapping-design.md` |
| [#34](https://github.com/davoodmehraban89/Aram/pull/34) | `governance/aram-5-1-3-controls-20261030` | `source-data-cleanup` | 8 | `.github/pull_request_template.md`<br>`AGENTS.md`<br>`docs/ACCEPTANCE_POLICY.md`<br>`docs/DECISION_LOG.md`<br>`docs/PROJECT_LOG.md`<br>`docs/adr/ADR-013-aram-5plus1plus3-delivery-governance.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/handoff/MASTER_RECOVERY_PROMPT.md` |
| [#35](https://github.com/davoodmehraban89/Aram/pull/35) | `codex/aram-same-flush-fiscal-lock-20261030` | `codex/v1-year-isolation-followup-20261023` | 6 | `backend/src/aram_backend/models.py`<br>`backend/tests/test_models.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-fiscal-year-graph-integrity.md`<br>`docs/superpowers/specs/2026-10-30-fiscal-year-graph-integrity.md` |
| [#44](https://github.com/davoodmehraban89/Aram/pull/44) | `docs/aram-roadmap-dashboard-20261030` | `source-data-cleanup` | 2 | `docs/PROJECT_LOG.md`<br>`docs/ROADMAP_DASHBOARD.md` |
| [#45](https://github.com/davoodmehraban89/Aram/pull/45) | `codex/aram-gate3-stale-note-guard-20261030` | `codex/gate3-carry-forward-preview-20261023` | 6 | `backend/src/aram_backend/mapping_carry_forward.py`<br>`backend/tests/test_mapping_carry_forward.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-carry-forward-stale-source-note.md`<br>`docs/superpowers/specs/2026-10-30-carry-forward-stale-source-note.md` |
| [#46](https://github.com/davoodmehraban89/Aram/pull/46) | `codex/aram-gate3-hidden-xlsx-guard-20261030` | `codex/gate3-mapping-excel-20261023` | 6 | `backend/src/aram_backend/mapping_excel.py`<br>`backend/tests/test_mapping_excel.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-mapping-workbook-visibility.md`<br>`docs/superpowers/specs/2026-10-30-mapping-workbook-visibility.md` |
| [#47](https://github.com/davoodmehraban89/Aram/pull/47) | `codex/aram-gate3-coverage-target-guard-20261030` | `codex/gate3-mapping-coverage-20261023` | 6 | `backend/src/aram_backend/mapping_coverage.py`<br>`backend/tests/test_mapping_coverage.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-mapping-coverage-target-integrity.md`<br>`docs/superpowers/specs/2026-10-30-mapping-coverage-target-integrity.md` |
| [#50](https://github.com/davoodmehraban89/Aram/pull/50) | `codex/aram-gate3-mapping-change-preview-20261030` | `codex/gate3-mapping-core` | 8 | `backend/src/aram_backend/mapping_change_preview.py`<br>`backend/src/aram_backend/mapping_service.py`<br>`backend/tests/test_mapping_change_preview.py`<br>`backend/tests/test_mapping_service.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-gate3-mapping-change-preview.md`<br>`docs/superpowers/specs/2026-10-30-gate3-mapping-change-preview.md` |
| [#51](https://github.com/davoodmehraban89/Aram/pull/51) | `codex/gate3-mapping-batch-review-20261030` | `codex/aram-gate3-mapping-change-preview-20261030` | 7 | `backend/src/aram_backend/mapping_batch_review.py`<br>`backend/src/aram_backend/mapping_change_preview.py`<br>`backend/tests/test_mapping_batch_review.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-gate3-mapping-batch-review.md`<br>`docs/superpowers/specs/2026-10-30-gate3-mapping-batch-review.md` |
| [#52](https://github.com/davoodmehraban89/Aram/pull/52) | `codex/gate3-mapping-batch-freshness-20261030` | `codex/gate3-mapping-batch-review-20261030` | 7 | `backend/src/aram_backend/mapping_batch_review.py`<br>`backend/src/aram_backend/mapping_change_preview.py`<br>`backend/tests/test_mapping_batch_review.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-gate3-batch-freshness.md`<br>`docs/superpowers/specs/2026-10-30-gate3-batch-freshness.md` |
| [#53](https://github.com/davoodmehraban89/Aram/pull/53) | `codex/gate3-unapproved-proposal-storage-20261030` | `codex/gate3-mapping-batch-freshness-20261030` | 7 | `backend/migrations/versions/20261030_02_unreviewed_mapping_drafts.py`<br>`backend/src/aram_backend/mapping_draft_store.py`<br>`backend/tests/test_mapping_draft_store.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-unreviewed-mapping-draft-store.md`<br>`docs/superpowers/specs/2026-10-30-unreviewed-mapping-draft-store.md` |
| [#54](https://github.com/davoodmehraban89/Aram/pull/54) | `codex/gate3-draft-staging-audit-20261030` | `codex/gate3-unapproved-proposal-storage-20261030` | 8 | `backend/migrations/versions/20261030_03_system_staging_audit.py`<br>`backend/src/aram_backend/mapping_draft_audit.py`<br>`backend/src/aram_backend/mapping_draft_store.py`<br>`backend/tests/test_mapping_draft_store.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-draft-staging-audit.md`<br>`docs/superpowers/specs/2026-10-30-draft-staging-audit.md` |
| [#55](https://github.com/davoodmehraban89/Aram/pull/55) | `codex/gate3-authenticated-principal-boundary-20261030` | `codex/gate3-draft-staging-audit-20261030` | 9 | `backend/pyproject.toml`<br>`backend/src/aram_backend/authenticated_identity.py`<br>`backend/src/aram_backend/config.py`<br>`backend/src/aram_backend/main.py`<br>`backend/tests/test_authenticated_identity.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-authenticated-principal-boundary.md`<br>`docs/superpowers/specs/2026-10-30-authenticated-principal-boundary.md` |
| [#56](https://github.com/davoodmehraban89/Aram/pull/56) | `codex/gate3-signed-year-scope-20261030` | `codex/gate3-authenticated-principal-boundary-20261030` | 8 | `backend/src/aram_backend/authenticated_identity.py`<br>`backend/src/aram_backend/main.py`<br>`backend/src/aram_backend/mapping_year_authorization.py`<br>`backend/tests/test_authenticated_identity.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-signed-year-scope.md`<br>`docs/superpowers/specs/2026-10-30-signed-year-scope.md` |
| [#57](https://github.com/davoodmehraban89/Aram/pull/57) | `codex/gate3-authored-draft-staging-20261030` | `codex/gate3-signed-year-scope-20261030` | 8 | `backend/migrations/versions/20261030_04_authored_drafts.py`<br>`backend/src/aram_backend/authored_mapping_draft.py`<br>`backend/src/aram_backend/main.py`<br>`backend/tests/test_authored_mapping_draft.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-authored-mapping-draft-staging.md`<br>`docs/superpowers/specs/2026-10-30-authored-mapping-draft-staging.md` |
| [#59](https://github.com/davoodmehraban89/Aram/pull/59) | `codex/windows-native-pilot-shell-20261030` | `codex/gate3-authored-draft-staging-20261030` | 13 | `.github/workflows/desktop-windows-ci.yml`<br>`PROJECT_STATUS.md`<br>`backend/desktop/README.md`<br>`backend/desktop/aram_pilot_entry.py`<br>`backend/desktop/build_windows_exe.ps1`<br>`backend/src/aram_backend/desktop_pilot.py`<br>`backend/src/aram_backend/desktop_pilot_core.py`<br>`backend/tests/test_desktop_pilot.py`<br>`docs/DECISION_LOG.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md`<br>`docs/superpowers/plans/2026-10-30-windows-native-desktop-pilot.md`<br>`docs/superpowers/specs/2026-10-30-windows-native-desktop-pilot.md` |
| [#60](https://github.com/davoodmehraban89/Aram/pull/60) | `codex/aram-readonly-mapping-coverage-20261031` | `source-data-cleanup` | 8 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/coverage_preview.py`<br>`backend/src/aram_backend/coverage_preview_cli.py`<br>`backend/tests/test_coverage_preview.py`<br>`backend/tests/test_coverage_preview_cli.py`<br>`docs/PROJECT_LOG.md`<br>`docs/READONLY_MAPPING_COVERAGE.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#61](https://github.com/davoodmehraban89/Aram/pull/61) | `codex/aram-reconciliation-review-gate-20261031` | `codex/aram-readonly-mapping-coverage-20261031` | 10 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/coverage_preview.py`<br>`backend/src/aram_backend/reconciliation_review.py`<br>`backend/src/aram_backend/reconciliation_review_cli.py`<br>`backend/tests/test_coverage_preview.py`<br>`backend/tests/test_reconciliation_review.py`<br>`backend/tests/test_reconciliation_review_cli.py`<br>`docs/NOTE_RECONCILIATION_REVIEW.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#62](https://github.com/davoodmehraban89/Aram/pull/62) | `codex/aram-bs-candidate-statement-20261031` | `codex/aram-reconciliation-review-gate-20261031` | 12 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/balance_sheet_candidate.py`<br>`backend/src/aram_backend/balance_sheet_candidate_cli.py`<br>`backend/src/aram_backend/coverage_preview.py`<br>`backend/src/aram_backend/reconciliation_review.py`<br>`backend/tests/test_balance_sheet_candidate.py`<br>`backend/tests/test_balance_sheet_candidate_cli.py`<br>`backend/tests/test_coverage_preview.py`<br>`backend/tests/test_reconciliation_review.py`<br>`docs/BALANCE_SHEET_CANDIDATE.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#63](https://github.com/davoodmehraban89/Aram/pull/63) | `codex/aram-income-statement-candidate-20261031` | `codex/aram-bs-candidate-statement-20261031` | 8 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/income_statement_candidate.py`<br>`backend/src/aram_backend/income_statement_candidate_cli.py`<br>`backend/tests/test_income_statement_candidate.py`<br>`backend/tests/test_income_statement_candidate_cli.py`<br>`docs/INCOME_STATEMENT_CANDIDATE.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#64](https://github.com/davoodmehraban89/Aram/pull/64) | `codex/aram-trial-balance-diagnostic-20261031` | `codex/aram-income-statement-candidate-20261031` | 8 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/trial_balance_diagnostic.py`<br>`backend/src/aram_backend/trial_balance_diagnostic_cli.py`<br>`backend/tests/test_trial_balance_diagnostic.py`<br>`backend/tests/test_trial_balance_diagnostic_cli.py`<br>`docs/PROJECT_LOG.md`<br>`docs/TRIAL_BALANCE_DIAGNOSTIC.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#65](https://github.com/davoodmehraban89/Aram/pull/65) | `codex/aram-equity-changes-candidate-20261031` | `codex/aram-trial-balance-diagnostic-20261031` | 8 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/equity_changes_candidate.py`<br>`backend/src/aram_backend/equity_changes_candidate_cli.py`<br>`backend/tests/test_equity_changes_candidate.py`<br>`backend/tests/test_equity_changes_candidate_cli.py`<br>`docs/EQUITY_CHANGES_CANDIDATE.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#66](https://github.com/davoodmehraban89/Aram/pull/66) | `codex/aram-cash-flow-direct-candidate-20261031` | `codex/aram-equity-changes-candidate-20261031` | 8 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/cash_flow_direct_candidate.py`<br>`backend/src/aram_backend/cash_flow_direct_candidate_cli.py`<br>`backend/tests/test_cash_flow_direct_candidate.py`<br>`backend/tests/test_cash_flow_direct_candidate_cli.py`<br>`docs/CASH_FLOW_DIRECT_CANDIDATE.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#67](https://github.com/davoodmehraban89/Aram/pull/67) | `codex/aram-cross-statement-controls-20261031` | `codex/aram-cash-flow-direct-candidate-20261031` | 6 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/cross_statement_reconciliation.py`<br>`backend/tests/test_cross_statement_reconciliation.py`<br>`docs/CROSS_STATEMENT_RECONCILIATION.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#68](https://github.com/davoodmehraban89/Aram/pull/68) | `codex/aram-multistatement-mapping-20261031` | `codex/aram-cross-statement-controls-20261031` | 9 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/coverage_preview.py`<br>`backend/src/aram_backend/equity_changes_candidate.py`<br>`backend/src/aram_backend/reconciliation_review.py`<br>`backend/tests/test_coverage_preview.py`<br>`backend/tests/test_equity_changes_candidate.py`<br>`backend/tests/test_reconciliation_review.py`<br>`docs/PILOT_WORKBOOK_CONTRACT.md`<br>`docs/READONLY_MAPPING_COVERAGE.md` |
| [#69](https://github.com/davoodmehraban89/Aram/pull/69) | `codex/aram-five-statement-integration-20261031` | `codex/aram-multistatement-mapping-20261031` | 7 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/cross_statement_reconciliation.py`<br>`backend/tests/test_cross_statement_reconciliation.py`<br>`backend/tests/test_five_statement_pipeline_integration.py`<br>`docs/CROSS_STATEMENT_RECONCILIATION.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#70](https://github.com/davoodmehraban89/Aram/pull/70) | `codex/aram-five-statement-orchestrator-20261031` | `codex/aram-five-statement-integration-20261031` | 6 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/five_statement_pipeline.py`<br>`backend/tests/test_five_statement_pipeline_integration.py`<br>`docs/FIVE_STATEMENT_PIPELINE.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#71](https://github.com/davoodmehraban89/Aram/pull/71) | `codex/aram-five-statement-cli-20261031` | `codex/aram-five-statement-orchestrator-20261031` | 6 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/five_statement_pipeline_cli.py`<br>`backend/tests/test_five_statement_pipeline_integration.py`<br>`docs/FIVE_STATEMENT_PIPELINE_CLI.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#72](https://github.com/davoodmehraban89/Aram/pull/72) | `codex/aram-pipeline-manifest-schema-20261031` | `codex/aram-five-statement-cli-20261031` | 3 | `backend/src/aram_backend/five_statement_pipeline_cli.py`<br>`backend/tests/test_five_statement_manifest_strictness.py`<br>`docs/FIVE_STATEMENT_PIPELINE_CLI.md` |
| [#73](https://github.com/davoodmehraban89/Aram/pull/73) | `codex/aram-manifest-referential-integrity-20261031` | `codex/aram-pipeline-manifest-schema-20261031` | 3 | `backend/src/aram_backend/five_statement_pipeline_cli.py`<br>`backend/tests/test_five_statement_manifest_referential_integrity.py`<br>`docs/FIVE_STATEMENT_PIPELINE_CLI.md` |
| [#74](https://github.com/davoodmehraban89/Aram/pull/74) | `codex/aram-actions-node24-maintenance-20261031` | `codex/aram-manifest-referential-integrity-20261031` | 1 | `.github/workflows/backend-ci.yml` |
| [#75](https://github.com/davoodmehraban89/Aram/pull/75) | `codex/aram-windows-five-statement-pilot-20261031` | `codex/aram-actions-node24-maintenance-20261031` | 7 | `.github/workflows/desktop-five-statement-windows-ci.yml`<br>`backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`<br>`backend/desktop/aram_five_statement_entry.py`<br>`backend/desktop/build_five_statement_windows.ps1`<br>`backend/src/aram_backend/desktop_five_statement.py`<br>`backend/src/aram_backend/desktop_five_statement_core.py`<br>`backend/tests/test_desktop_five_statement.py` |
| [#76](https://github.com/davoodmehraban89/Aram/pull/76) | `codex/aram-synthetic-windows-demo-20261031` | `codex/aram-windows-five-statement-pilot-20261031` | 9 | `.github/workflows/desktop-five-statement-windows-ci.yml`<br>`PROJECT_STATUS.md`<br>`backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`<br>`backend/src/aram_backend/desktop_five_statement.py`<br>`backend/src/aram_backend/synthetic_five_statement_demo.py`<br>`backend/tests/test_five_statement_pipeline_integration.py`<br>`backend/tests/test_synthetic_five_statement_demo.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#77](https://github.com/davoodmehraban89/Aram/pull/77) | `codex/aram-windows-statement-figures-20261031` | `codex/aram-synthetic-windows-demo-20261031` | 8 | `PROJECT_STATUS.md`<br>`backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`<br>`backend/src/aram_backend/desktop_five_statement.py`<br>`backend/src/aram_backend/desktop_five_statement_figures.py`<br>`backend/tests/test_desktop_five_statement.py`<br>`backend/tests/test_desktop_five_statement_figures.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#78](https://github.com/davoodmehraban89/Aram/pull/78) | `codex/aram-windows-detail-review-20261031` | `codex/aram-windows-statement-figures-20261031` | 11 | `.github/workflows/desktop-five-statement-windows-ci.yml`<br>`PROJECT_STATUS.md`<br>`backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`<br>`backend/src/aram_backend/desktop_five_statement.py`<br>`backend/src/aram_backend/desktop_five_statement_details.py`<br>`backend/src/aram_backend/desktop_five_statement_figures.py`<br>`backend/src/aram_backend/desktop_five_statement_integrity.py`<br>`backend/tests/test_desktop_five_statement.py`<br>`backend/tests/test_desktop_five_statement_details.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#79](https://github.com/davoodmehraban89/Aram/pull/79) | `codex/aram-windows-background-detail-search-20261031` | `codex/aram-windows-detail-review-20261031` | 8 | `PROJECT_STATUS.md`<br>`backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`<br>`backend/src/aram_backend/desktop_five_statement.py`<br>`backend/src/aram_backend/desktop_five_statement_details.py`<br>`backend/tests/test_desktop_five_statement.py`<br>`backend/tests/test_desktop_five_statement_details.py`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#80](https://github.com/davoodmehraban89/Aram/pull/80) | `codex/aram-account-note-source-trace-20261031` | `codex/aram-windows-background-detail-search-20261031` | 8 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`<br>`backend/src/aram_backend/desktop_five_statement.py`<br>`backend/src/aram_backend/desktop_five_statement_details.py`<br>`backend/src/aram_backend/desktop_five_statement_integrity.py`<br>`backend/src/aram_backend/five_statement_pipeline.py`<br>`backend/tests/test_desktop_account_note_trace.py`<br>`backend/tests/test_desktop_five_statement.py`<br>`backend/tests/test_desktop_five_statement_details.py` |
| [#81](https://github.com/davoodmehraban89/Aram/pull/81) | `codex/aram-mapping-source-parser-20261101` | `codex/aram-account-note-source-trace-20261031` | 11 | `backend/src/aram_backend/mapping_matcher.py`<br>`backend/src/aram_backend/mapping_source_parser.py`<br>`backend/tests/test_desktop_five_statement.py`<br>`backend/tests/test_mapping_matcher.py`<br>`backend/tests/test_mapping_parser_limits.py`<br>`backend/tests/test_mapping_precision.py`<br>`backend/tests/test_mapping_source_parser.py`<br>`docs/MAPPING_MATCHER.md`<br>`docs/MAPPING_SOURCE_PARSER.md`<br>`docs/handoff/MAPPING_MATCHER_HANDOFF.md`<br>`docs/handoff/MAPPING_SOURCE_PARSER_HANDOFF.md` |
| [#82](https://github.com/davoodmehraban89/Aram/pull/82) | `feat/gate3-governed-mapping-20261101` | `source-data-cleanup` | 22 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/main.py`<br>`backend/src/aram_backend/mapping_access.py`<br>`backend/src/aram_backend/mapping_api.py`<br>`backend/src/aram_backend/mapping_integrity.py`<br>`backend/src/aram_backend/mapping_quality.py`<br>`backend/src/aram_backend/mapping_receipts.py`<br>`backend/src/aram_backend/mapping_store.py`<br>`backend/src/aram_backend/mapping_workflow.py`<br>`backend/tests/test_mapping_access.py`<br>`backend/tests/test_mapping_api.py`<br>`backend/tests/test_mapping_hash_chain.py`<br>`backend/tests/test_mapping_receipts.py`<br>`backend/tests/test_mapping_recovery_quality.py`<br>`backend/tests/test_mapping_store.py`<br>`backend/tests/test_mapping_workflow.py`<br>`docs/GATE3_PACKAGE4_REVIEW.md`<br>`docs/GATE3_PACKAGE5_ACCEPTANCE.md`<br>`docs/GATE3_PACKAGE6_FINAL.md`<br>`docs/GATE3_PACKAGE7_CLOSURE_DOSSIER.md`<br>`docs/GATE3_REVIEW_82.md`<br>`docs/PROJECT_LOG.md` |
| [#88](https://github.com/davoodmehraban89/Aram/pull/88) | `feat/gate3-package9-isolated-20261103` | `feat/gate3-governed-mapping-20261101` | 34 | `.github/workflows/backend-ci.yml`<br>`PROJECT_STATUS.md`<br>`backend/README.md`<br>`backend/migrations/env.py`<br>`backend/migrations/versions/20260820_01_initial_schema.py`<br>`backend/pyproject.toml`<br>`backend/src/aram_backend/ingestion.py`<br>`backend/src/aram_backend/ledger_parser.py`<br>`backend/src/aram_backend/local_auth.py`<br>`backend/src/aram_backend/mapping_access.py`<br>`backend/src/aram_backend/mapping_api.py`<br>`backend/src/aram_backend/mapping_store.py`<br>`backend/src/aram_backend/mapping_workflow.py`<br>`backend/src/aram_backend/workbook_inspection.py`<br>`backend/tests/test_gate3_encrypted_backup.py`<br>`backend/tests/test_gate3_recovery_drill.py`<br>`backend/tests/test_ingestion.py`<br>`backend/tests/test_ledger_parser.py`<br>`backend/tests/test_local_auth.py`<br>`backend/tests/test_mapping_access.py`<br>`backend/tests/test_mapping_api.py`<br>`backend/tests/test_mapping_hash_chain.py`<br>`backend/tests/test_mapping_receipts.py`<br>`backend/tests/test_mapping_recovery_quality.py`<br>`backend/tests/test_mapping_store.py`<br>`backend/tests/test_mapping_workflow.py`<br>`backend/tests/test_owner_acceptance.py`<br>`backend/tools/gate3_synthetic_cloud_drill.py`<br>`backend/tools/gate3_synthetic_cloud_restore.py`<br>`docs/GATE3_PACKAGE8_EXECUTION_REPORT_20261103.md`<br>`docs/GATE3_PACKAGE9_BASELINE_20261103.md`<br>`docs/GATE3_PERSONAL_WINDOWS_ARCHITECTURE_DRAFT.md`<br>`docs/GATE3_SINGLE_PASS_EXECUTION_20261102.md`<br>`docs/PROJECT_LOG.md` |
| [#89](https://github.com/davoodmehraban89/Aram/pull/89) | `feat/gate3-package9-1-security-20261103` | `feat/gate3-package9-isolated-20261103` | 15 | `backend/pyproject.toml`<br>`backend/src/aram_backend/auth_api.py`<br>`backend/src/aram_backend/config.py`<br>`backend/src/aram_backend/credential_recovery.py`<br>`backend/src/aram_backend/local_auth.py`<br>`backend/src/aram_backend/main.py`<br>`backend/src/aram_backend/password_security.py`<br>`backend/src/aram_backend/windows_credential_vault.py`<br>`backend/tests/test_auth_api.py`<br>`backend/tests/test_credential_recovery.py`<br>`backend/tests/test_local_auth.py`<br>`backend/tests/test_password_security.py`<br>`backend/tests/test_windows_credential_vault.py`<br>`docs/GATE3_PACKAGE9_1_EXECUTION_REPORT_20261103.md`<br>`docs/GATE3_PACKAGE9_1_SECURITY_REPORT.md` |
| [#90](https://github.com/davoodmehraban89/Aram/pull/90) | `docs/financial-statement-reconciliation-1402-1404-20261110` | `source-data-cleanup` | 9 | `NOTE_CATALOG.md`<br>`NOTE_TO_SHEET_MATRIX.md`<br>`PROJECT_STATUS.md`<br>`docs/BUDGET_1404_NOTE39_UNIT_AND_REF_ERRORS_20261111.md`<br>`docs/FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md`<br>`docs/FS_1403_EQUITY_DUPLICATE_PRIOR_PERIOD_ADJUSTMENT_20261111.md`<br>`docs/MAP_8161_SEVEN_RULES_PROPOSAL_20261111.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#91](https://github.com/davoodmehraban89/Aram/pull/91) | `docs/aram-master-control-plan-20261111` | `source-data-cleanup` | 13 | `AGENTS.md`<br>`PROJECT_STATUS.md`<br>`docs/.tmp_open_pr_file_inventory_part1.json`<br>`docs/.tmp_open_pr_file_inventory_part2.json`<br>`docs/.tmp_open_pr_file_inventory_part3.json`<br>`docs/ARAM_EXECUTION_PROGRESS_DASHBOARD.md`<br>`docs/ARAM_MASTER_CONTROL_PLAN.md`<br>`docs/ARAM_WORKTREE_CHANGE_OWNERSHIP_20261111.md`<br>`docs/ARAM_WORKTREE_FILE_LEVEL_DISPOSITION_20261111.md`<br>`docs/OPEN_PULL_REQUEST_DEPENDENCY_GRAPH_20261111.md`<br>`docs/OPEN_PULL_REQUEST_DEPENDENCY_INVENTORY_20261111.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |
| [#92](https://github.com/davoodmehraban89/Aram/pull/92) | `fix/password-unicode-validation-20261111` | `feat/gate3-package9-1-security-20261103` | 6 | `PROJECT_STATUS.md`<br>`backend/src/aram_backend/password_security.py`<br>`backend/tests/test_password_security.py`<br>`docs/PASSWORD_UNICODE_HARDENING_20261111.md`<br>`docs/PROJECT_LOG.md`<br>`docs/handoff/LATEST_HANDOFF.md` |

## 3. Shared repository paths

| Path | PRs touching path | Count |
|---|---|---:|
| `docs/PROJECT_LOG.md` | [#22](https://github.com/davoodmehraban89/Aram/pull/22), [#25](https://github.com/davoodmehraban89/Aram/pull/25), [#26](https://github.com/davoodmehraban89/Aram/pull/26), [#27](https://github.com/davoodmehraban89/Aram/pull/27), [#28](https://github.com/davoodmehraban89/Aram/pull/28), [#29](https://github.com/davoodmehraban89/Aram/pull/29), [#30](https://github.com/davoodmehraban89/Aram/pull/30), [#31](https://github.com/davoodmehraban89/Aram/pull/31), [#32](https://github.com/davoodmehraban89/Aram/pull/32), [#33](https://github.com/davoodmehraban89/Aram/pull/33), [#34](https://github.com/davoodmehraban89/Aram/pull/34), [#35](https://github.com/davoodmehraban89/Aram/pull/35), [#44](https://github.com/davoodmehraban89/Aram/pull/44), [#45](https://github.com/davoodmehraban89/Aram/pull/45), [#46](https://github.com/davoodmehraban89/Aram/pull/46), [#47](https://github.com/davoodmehraban89/Aram/pull/47), [#50](https://github.com/davoodmehraban89/Aram/pull/50), [#51](https://github.com/davoodmehraban89/Aram/pull/51), [#52](https://github.com/davoodmehraban89/Aram/pull/52), [#53](https://github.com/davoodmehraban89/Aram/pull/53), [#54](https://github.com/davoodmehraban89/Aram/pull/54), [#55](https://github.com/davoodmehraban89/Aram/pull/55), [#56](https://github.com/davoodmehraban89/Aram/pull/56), [#57](https://github.com/davoodmehraban89/Aram/pull/57), [#59](https://github.com/davoodmehraban89/Aram/pull/59), [#60](https://github.com/davoodmehraban89/Aram/pull/60), [#61](https://github.com/davoodmehraban89/Aram/pull/61), [#62](https://github.com/davoodmehraban89/Aram/pull/62), [#63](https://github.com/davoodmehraban89/Aram/pull/63), [#64](https://github.com/davoodmehraban89/Aram/pull/64), [#65](https://github.com/davoodmehraban89/Aram/pull/65), [#66](https://github.com/davoodmehraban89/Aram/pull/66), [#67](https://github.com/davoodmehraban89/Aram/pull/67), [#69](https://github.com/davoodmehraban89/Aram/pull/69), [#70](https://github.com/davoodmehraban89/Aram/pull/70), [#71](https://github.com/davoodmehraban89/Aram/pull/71), [#76](https://github.com/davoodmehraban89/Aram/pull/76), [#77](https://github.com/davoodmehraban89/Aram/pull/77), [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88), [#90](https://github.com/davoodmehraban89/Aram/pull/90), [#91](https://github.com/davoodmehraban89/Aram/pull/91), [#92](https://github.com/davoodmehraban89/Aram/pull/92) | 45 |
| `docs/handoff/LATEST_HANDOFF.md` | [#22](https://github.com/davoodmehraban89/Aram/pull/22), [#26](https://github.com/davoodmehraban89/Aram/pull/26), [#27](https://github.com/davoodmehraban89/Aram/pull/27), [#28](https://github.com/davoodmehraban89/Aram/pull/28), [#29](https://github.com/davoodmehraban89/Aram/pull/29), [#30](https://github.com/davoodmehraban89/Aram/pull/30), [#31](https://github.com/davoodmehraban89/Aram/pull/31), [#32](https://github.com/davoodmehraban89/Aram/pull/32), [#33](https://github.com/davoodmehraban89/Aram/pull/33), [#34](https://github.com/davoodmehraban89/Aram/pull/34), [#35](https://github.com/davoodmehraban89/Aram/pull/35), [#45](https://github.com/davoodmehraban89/Aram/pull/45), [#46](https://github.com/davoodmehraban89/Aram/pull/46), [#47](https://github.com/davoodmehraban89/Aram/pull/47), [#50](https://github.com/davoodmehraban89/Aram/pull/50), [#51](https://github.com/davoodmehraban89/Aram/pull/51), [#52](https://github.com/davoodmehraban89/Aram/pull/52), [#53](https://github.com/davoodmehraban89/Aram/pull/53), [#54](https://github.com/davoodmehraban89/Aram/pull/54), [#55](https://github.com/davoodmehraban89/Aram/pull/55), [#56](https://github.com/davoodmehraban89/Aram/pull/56), [#57](https://github.com/davoodmehraban89/Aram/pull/57), [#59](https://github.com/davoodmehraban89/Aram/pull/59), [#60](https://github.com/davoodmehraban89/Aram/pull/60), [#61](https://github.com/davoodmehraban89/Aram/pull/61), [#62](https://github.com/davoodmehraban89/Aram/pull/62), [#63](https://github.com/davoodmehraban89/Aram/pull/63), [#64](https://github.com/davoodmehraban89/Aram/pull/64), [#65](https://github.com/davoodmehraban89/Aram/pull/65), [#66](https://github.com/davoodmehraban89/Aram/pull/66), [#67](https://github.com/davoodmehraban89/Aram/pull/67), [#69](https://github.com/davoodmehraban89/Aram/pull/69), [#70](https://github.com/davoodmehraban89/Aram/pull/70), [#71](https://github.com/davoodmehraban89/Aram/pull/71), [#76](https://github.com/davoodmehraban89/Aram/pull/76), [#77](https://github.com/davoodmehraban89/Aram/pull/77), [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#90](https://github.com/davoodmehraban89/Aram/pull/90), [#91](https://github.com/davoodmehraban89/Aram/pull/91), [#92](https://github.com/davoodmehraban89/Aram/pull/92) | 41 |
| `PROJECT_STATUS.md` | [#22](https://github.com/davoodmehraban89/Aram/pull/22), [#26](https://github.com/davoodmehraban89/Aram/pull/26), [#27](https://github.com/davoodmehraban89/Aram/pull/27), [#28](https://github.com/davoodmehraban89/Aram/pull/28), [#29](https://github.com/davoodmehraban89/Aram/pull/29), [#30](https://github.com/davoodmehraban89/Aram/pull/30), [#31](https://github.com/davoodmehraban89/Aram/pull/31), [#32](https://github.com/davoodmehraban89/Aram/pull/32), [#33](https://github.com/davoodmehraban89/Aram/pull/33), [#59](https://github.com/davoodmehraban89/Aram/pull/59), [#60](https://github.com/davoodmehraban89/Aram/pull/60), [#61](https://github.com/davoodmehraban89/Aram/pull/61), [#62](https://github.com/davoodmehraban89/Aram/pull/62), [#63](https://github.com/davoodmehraban89/Aram/pull/63), [#64](https://github.com/davoodmehraban89/Aram/pull/64), [#65](https://github.com/davoodmehraban89/Aram/pull/65), [#66](https://github.com/davoodmehraban89/Aram/pull/66), [#67](https://github.com/davoodmehraban89/Aram/pull/67), [#68](https://github.com/davoodmehraban89/Aram/pull/68), [#69](https://github.com/davoodmehraban89/Aram/pull/69), [#70](https://github.com/davoodmehraban89/Aram/pull/70), [#71](https://github.com/davoodmehraban89/Aram/pull/71), [#76](https://github.com/davoodmehraban89/Aram/pull/76), [#77](https://github.com/davoodmehraban89/Aram/pull/77), [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88), [#90](https://github.com/davoodmehraban89/Aram/pull/90), [#91](https://github.com/davoodmehraban89/Aram/pull/91), [#92](https://github.com/davoodmehraban89/Aram/pull/92) | 31 |
| `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md` | [#75](https://github.com/davoodmehraban89/Aram/pull/75), [#76](https://github.com/davoodmehraban89/Aram/pull/76), [#77](https://github.com/davoodmehraban89/Aram/pull/77), [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#80](https://github.com/davoodmehraban89/Aram/pull/80) | 6 |
| `backend/src/aram_backend/desktop_five_statement.py` | [#75](https://github.com/davoodmehraban89/Aram/pull/75), [#76](https://github.com/davoodmehraban89/Aram/pull/76), [#77](https://github.com/davoodmehraban89/Aram/pull/77), [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#80](https://github.com/davoodmehraban89/Aram/pull/80) | 6 |
| `backend/tests/test_desktop_five_statement.py` | [#75](https://github.com/davoodmehraban89/Aram/pull/75), [#77](https://github.com/davoodmehraban89/Aram/pull/77), [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#80](https://github.com/davoodmehraban89/Aram/pull/80), [#81](https://github.com/davoodmehraban89/Aram/pull/81) | 6 |
| `backend/src/aram_backend/main.py` | [#55](https://github.com/davoodmehraban89/Aram/pull/55), [#56](https://github.com/davoodmehraban89/Aram/pull/56), [#57](https://github.com/davoodmehraban89/Aram/pull/57), [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#89](https://github.com/davoodmehraban89/Aram/pull/89) | 5 |
| `backend/pyproject.toml` | [#23](https://github.com/davoodmehraban89/Aram/pull/23), [#55](https://github.com/davoodmehraban89/Aram/pull/55), [#88](https://github.com/davoodmehraban89/Aram/pull/88), [#89](https://github.com/davoodmehraban89/Aram/pull/89) | 4 |
| `backend/src/aram_backend/coverage_preview.py` | [#60](https://github.com/davoodmehraban89/Aram/pull/60), [#61](https://github.com/davoodmehraban89/Aram/pull/61), [#62](https://github.com/davoodmehraban89/Aram/pull/62), [#68](https://github.com/davoodmehraban89/Aram/pull/68) | 4 |
| `backend/tests/test_coverage_preview.py` | [#60](https://github.com/davoodmehraban89/Aram/pull/60), [#61](https://github.com/davoodmehraban89/Aram/pull/61), [#62](https://github.com/davoodmehraban89/Aram/pull/62), [#68](https://github.com/davoodmehraban89/Aram/pull/68) | 4 |
| `backend/tests/test_five_statement_pipeline_integration.py` | [#69](https://github.com/davoodmehraban89/Aram/pull/69), [#70](https://github.com/davoodmehraban89/Aram/pull/70), [#71](https://github.com/davoodmehraban89/Aram/pull/71), [#76](https://github.com/davoodmehraban89/Aram/pull/76) | 4 |
| `.github/workflows/desktop-five-statement-windows-ci.yml` | [#75](https://github.com/davoodmehraban89/Aram/pull/75), [#76](https://github.com/davoodmehraban89/Aram/pull/76), [#78](https://github.com/davoodmehraban89/Aram/pull/78) | 3 |
| `backend/src/aram_backend/desktop_five_statement_details.py` | [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#80](https://github.com/davoodmehraban89/Aram/pull/80) | 3 |
| `backend/src/aram_backend/five_statement_pipeline_cli.py` | [#71](https://github.com/davoodmehraban89/Aram/pull/71), [#72](https://github.com/davoodmehraban89/Aram/pull/72), [#73](https://github.com/davoodmehraban89/Aram/pull/73) | 3 |
| `backend/src/aram_backend/mapping_change_preview.py` | [#50](https://github.com/davoodmehraban89/Aram/pull/50), [#51](https://github.com/davoodmehraban89/Aram/pull/51), [#52](https://github.com/davoodmehraban89/Aram/pull/52) | 3 |
| `backend/src/aram_backend/reconciliation_review.py` | [#61](https://github.com/davoodmehraban89/Aram/pull/61), [#62](https://github.com/davoodmehraban89/Aram/pull/62), [#68](https://github.com/davoodmehraban89/Aram/pull/68) | 3 |
| `backend/tests/test_desktop_five_statement_details.py` | [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#79](https://github.com/davoodmehraban89/Aram/pull/79), [#80](https://github.com/davoodmehraban89/Aram/pull/80) | 3 |
| `backend/tests/test_reconciliation_review.py` | [#61](https://github.com/davoodmehraban89/Aram/pull/61), [#62](https://github.com/davoodmehraban89/Aram/pull/62), [#68](https://github.com/davoodmehraban89/Aram/pull/68) | 3 |
| `docs/FIVE_STATEMENT_PIPELINE_CLI.md` | [#71](https://github.com/davoodmehraban89/Aram/pull/71), [#72](https://github.com/davoodmehraban89/Aram/pull/72), [#73](https://github.com/davoodmehraban89/Aram/pull/73) | 3 |
| `.github/workflows/backend-ci.yml` | [#74](https://github.com/davoodmehraban89/Aram/pull/74), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `AGENTS.md` | [#34](https://github.com/davoodmehraban89/Aram/pull/34), [#91](https://github.com/davoodmehraban89/Aram/pull/91) | 2 |
| `backend/migrations/versions/20260820_01_initial_schema.py` | [#25](https://github.com/davoodmehraban89/Aram/pull/25), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/src/aram_backend/authenticated_identity.py` | [#55](https://github.com/davoodmehraban89/Aram/pull/55), [#56](https://github.com/davoodmehraban89/Aram/pull/56) | 2 |
| `backend/src/aram_backend/config.py` | [#55](https://github.com/davoodmehraban89/Aram/pull/55), [#89](https://github.com/davoodmehraban89/Aram/pull/89) | 2 |
| `backend/src/aram_backend/cross_statement_reconciliation.py` | [#67](https://github.com/davoodmehraban89/Aram/pull/67), [#69](https://github.com/davoodmehraban89/Aram/pull/69) | 2 |
| `backend/src/aram_backend/desktop_five_statement_figures.py` | [#77](https://github.com/davoodmehraban89/Aram/pull/77), [#78](https://github.com/davoodmehraban89/Aram/pull/78) | 2 |
| `backend/src/aram_backend/desktop_five_statement_integrity.py` | [#78](https://github.com/davoodmehraban89/Aram/pull/78), [#80](https://github.com/davoodmehraban89/Aram/pull/80) | 2 |
| `backend/src/aram_backend/equity_changes_candidate.py` | [#65](https://github.com/davoodmehraban89/Aram/pull/65), [#68](https://github.com/davoodmehraban89/Aram/pull/68) | 2 |
| `backend/src/aram_backend/five_statement_pipeline.py` | [#70](https://github.com/davoodmehraban89/Aram/pull/70), [#80](https://github.com/davoodmehraban89/Aram/pull/80) | 2 |
| `backend/src/aram_backend/local_auth.py` | [#88](https://github.com/davoodmehraban89/Aram/pull/88), [#89](https://github.com/davoodmehraban89/Aram/pull/89) | 2 |
| `backend/src/aram_backend/mapping_access.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/src/aram_backend/mapping_api.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/src/aram_backend/mapping_batch_review.py` | [#51](https://github.com/davoodmehraban89/Aram/pull/51), [#52](https://github.com/davoodmehraban89/Aram/pull/52) | 2 |
| `backend/src/aram_backend/mapping_carry_forward.py` | [#30](https://github.com/davoodmehraban89/Aram/pull/30), [#45](https://github.com/davoodmehraban89/Aram/pull/45) | 2 |
| `backend/src/aram_backend/mapping_coverage.py` | [#28](https://github.com/davoodmehraban89/Aram/pull/28), [#47](https://github.com/davoodmehraban89/Aram/pull/47) | 2 |
| `backend/src/aram_backend/mapping_draft_store.py` | [#53](https://github.com/davoodmehraban89/Aram/pull/53), [#54](https://github.com/davoodmehraban89/Aram/pull/54) | 2 |
| `backend/src/aram_backend/mapping_excel.py` | [#27](https://github.com/davoodmehraban89/Aram/pull/27), [#46](https://github.com/davoodmehraban89/Aram/pull/46) | 2 |
| `backend/src/aram_backend/mapping_service.py` | [#26](https://github.com/davoodmehraban89/Aram/pull/26), [#50](https://github.com/davoodmehraban89/Aram/pull/50) | 2 |
| `backend/src/aram_backend/mapping_store.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/src/aram_backend/mapping_workflow.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/src/aram_backend/models.py` | [#32](https://github.com/davoodmehraban89/Aram/pull/32), [#35](https://github.com/davoodmehraban89/Aram/pull/35) | 2 |
| `backend/src/aram_backend/password_security.py` | [#89](https://github.com/davoodmehraban89/Aram/pull/89), [#92](https://github.com/davoodmehraban89/Aram/pull/92) | 2 |
| `backend/tests/test_authenticated_identity.py` | [#55](https://github.com/davoodmehraban89/Aram/pull/55), [#56](https://github.com/davoodmehraban89/Aram/pull/56) | 2 |
| `backend/tests/test_cross_statement_reconciliation.py` | [#67](https://github.com/davoodmehraban89/Aram/pull/67), [#69](https://github.com/davoodmehraban89/Aram/pull/69) | 2 |
| `backend/tests/test_equity_changes_candidate.py` | [#65](https://github.com/davoodmehraban89/Aram/pull/65), [#68](https://github.com/davoodmehraban89/Aram/pull/68) | 2 |
| `backend/tests/test_local_auth.py` | [#88](https://github.com/davoodmehraban89/Aram/pull/88), [#89](https://github.com/davoodmehraban89/Aram/pull/89) | 2 |
| `backend/tests/test_mapping_access.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/tests/test_mapping_api.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/tests/test_mapping_batch_review.py` | [#51](https://github.com/davoodmehraban89/Aram/pull/51), [#52](https://github.com/davoodmehraban89/Aram/pull/52) | 2 |
| `backend/tests/test_mapping_carry_forward.py` | [#30](https://github.com/davoodmehraban89/Aram/pull/30), [#45](https://github.com/davoodmehraban89/Aram/pull/45) | 2 |
| `backend/tests/test_mapping_coverage.py` | [#28](https://github.com/davoodmehraban89/Aram/pull/28), [#47](https://github.com/davoodmehraban89/Aram/pull/47) | 2 |
| `backend/tests/test_mapping_draft_store.py` | [#53](https://github.com/davoodmehraban89/Aram/pull/53), [#54](https://github.com/davoodmehraban89/Aram/pull/54) | 2 |
| `backend/tests/test_mapping_excel.py` | [#27](https://github.com/davoodmehraban89/Aram/pull/27), [#46](https://github.com/davoodmehraban89/Aram/pull/46) | 2 |
| `backend/tests/test_mapping_hash_chain.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/tests/test_mapping_receipts.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/tests/test_mapping_recovery_quality.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/tests/test_mapping_service.py` | [#26](https://github.com/davoodmehraban89/Aram/pull/26), [#50](https://github.com/davoodmehraban89/Aram/pull/50) | 2 |
| `backend/tests/test_mapping_store.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/tests/test_mapping_workflow.py` | [#82](https://github.com/davoodmehraban89/Aram/pull/82), [#88](https://github.com/davoodmehraban89/Aram/pull/88) | 2 |
| `backend/tests/test_models.py` | [#32](https://github.com/davoodmehraban89/Aram/pull/32), [#35](https://github.com/davoodmehraban89/Aram/pull/35) | 2 |
| `backend/tests/test_password_security.py` | [#89](https://github.com/davoodmehraban89/Aram/pull/89), [#92](https://github.com/davoodmehraban89/Aram/pull/92) | 2 |
| `docs/CROSS_STATEMENT_RECONCILIATION.md` | [#67](https://github.com/davoodmehraban89/Aram/pull/67), [#69](https://github.com/davoodmehraban89/Aram/pull/69) | 2 |
| `docs/DECISION_LOG.md` | [#34](https://github.com/davoodmehraban89/Aram/pull/34), [#59](https://github.com/davoodmehraban89/Aram/pull/59) | 2 |
| `docs/READONLY_MAPPING_COVERAGE.md` | [#60](https://github.com/davoodmehraban89/Aram/pull/60), [#68](https://github.com/davoodmehraban89/Aram/pull/68) | 2 |

## 4. PR pairs with shared paths

| PR pair | Shared path count | Shared paths |
|---|---:|---|
| #82 ↔ #88 | 13 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md`, `backend/src/aram_backend/mapping_access.py`, `backend/src/aram_backend/mapping_api.py`, `backend/src/aram_backend/mapping_store.py`, `backend/src/aram_backend/mapping_workflow.py`, `backend/tests/test_mapping_access.py`, `backend/tests/test_mapping_api.py`, `backend/tests/test_mapping_hash_chain.py`, `backend/tests/test_mapping_receipts.py`, `backend/tests/test_mapping_recovery_quality.py`, `backend/tests/test_mapping_store.py`, `backend/tests/test_mapping_workflow.py` |
| #78 ↔ #79 | 8 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py`, `backend/src/aram_backend/desktop_five_statement_details.py`, `backend/tests/test_desktop_five_statement_details.py` |
| #61 ↔ #62 | 7 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/src/aram_backend/coverage_preview.py`, `backend/tests/test_coverage_preview.py`, `backend/src/aram_backend/reconciliation_review.py`, `backend/tests/test_reconciliation_review.py` |
| #77 ↔ #78 | 7 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py`, `backend/src/aram_backend/desktop_five_statement_figures.py` |
| #67 ↔ #69 | 6 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/src/aram_backend/cross_statement_reconciliation.py`, `backend/tests/test_cross_statement_reconciliation.py`, `docs/CROSS_STATEMENT_RECONCILIATION.md` |
| #76 ↔ #78 | 6 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `.github/workflows/desktop-five-statement-windows-ci.yml` |
| #77 ↔ #79 | 6 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py` |
| #78 ↔ #80 | 6 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py`, `backend/src/aram_backend/desktop_five_statement_details.py`, `backend/tests/test_desktop_five_statement_details.py`, `backend/src/aram_backend/desktop_five_statement_integrity.py` |
| #51 ↔ #52 | 5 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_change_preview.py`, `backend/src/aram_backend/mapping_batch_review.py`, `backend/tests/test_mapping_batch_review.py` |
| #55 ↔ #56 | 5 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/main.py`, `backend/src/aram_backend/authenticated_identity.py`, `backend/tests/test_authenticated_identity.py` |
| #60 ↔ #61 | 5 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/src/aram_backend/coverage_preview.py`, `backend/tests/test_coverage_preview.py` |
| #60 ↔ #62 | 5 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/src/aram_backend/coverage_preview.py`, `backend/tests/test_coverage_preview.py` |
| #61 ↔ #68 | 5 | `PROJECT_STATUS.md`, `backend/src/aram_backend/coverage_preview.py`, `backend/tests/test_coverage_preview.py`, `backend/src/aram_backend/reconciliation_review.py`, `backend/tests/test_reconciliation_review.py` |
| #62 ↔ #68 | 5 | `PROJECT_STATUS.md`, `backend/src/aram_backend/coverage_preview.py`, `backend/tests/test_coverage_preview.py`, `backend/src/aram_backend/reconciliation_review.py`, `backend/tests/test_reconciliation_review.py` |
| #76 ↔ #77 | 5 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py` |
| #76 ↔ #79 | 5 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py` |
| #79 ↔ #80 | 5 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py`, `backend/src/aram_backend/desktop_five_statement_details.py`, `backend/tests/test_desktop_five_statement_details.py` |
| #26 ↔ #50 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_service.py`, `backend/tests/test_mapping_service.py` |
| #27 ↔ #46 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_excel.py`, `backend/tests/test_mapping_excel.py` |
| #28 ↔ #47 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_coverage.py`, `backend/tests/test_mapping_coverage.py` |
| #30 ↔ #45 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_carry_forward.py`, `backend/tests/test_mapping_carry_forward.py` |
| #32 ↔ #35 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/models.py`, `backend/tests/test_models.py` |
| #53 ↔ #54 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_draft_store.py`, `backend/tests/test_mapping_draft_store.py` |
| #60 ↔ #68 | 4 | `PROJECT_STATUS.md`, `backend/src/aram_backend/coverage_preview.py`, `backend/tests/test_coverage_preview.py`, `docs/READONLY_MAPPING_COVERAGE.md` |
| #69 ↔ #70 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/tests/test_five_statement_pipeline_integration.py` |
| #69 ↔ #71 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/tests/test_five_statement_pipeline_integration.py` |
| #69 ↔ #76 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/tests/test_five_statement_pipeline_integration.py` |
| #70 ↔ #71 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/tests/test_five_statement_pipeline_integration.py` |
| #70 ↔ #76 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/tests/test_five_statement_pipeline_integration.py` |
| #71 ↔ #76 | 4 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md`, `backend/tests/test_five_statement_pipeline_integration.py` |
| #75 ↔ #78 | 4 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py`, `.github/workflows/desktop-five-statement-windows-ci.yml` |
| #22 ↔ #26 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #27 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #28 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #29 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #30 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #31 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #32 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #27 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #28 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #29 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #30 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #31 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #32 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #26 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #28 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #29 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #30 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #31 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #32 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #27 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #29 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #30 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #31 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #32 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #28 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #30 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #31 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #32 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #29 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #31 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #32 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #30 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #32 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #31 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #33 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #32 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #33 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #34 ↔ #59 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `docs/DECISION_LOG.md` |
| #34 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `AGENTS.md` |
| #50 ↔ #51 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_change_preview.py` |
| #50 ↔ #52 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/mapping_change_preview.py` |
| #55 ↔ #57 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/main.py` |
| #55 ↔ #89 | 3 | `backend/src/aram_backend/main.py`, `backend/pyproject.toml`, `backend/src/aram_backend/config.py` |
| #56 ↔ #57 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `backend/src/aram_backend/main.py` |
| #59 ↔ #60 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #61 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #62 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #59 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #60 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #61 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #63 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #62 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #64 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #63 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #65 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #64 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #66 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #65 ↔ #68 | 3 | `PROJECT_STATUS.md`, `backend/src/aram_backend/equity_changes_candidate.py`, `backend/tests/test_equity_changes_candidate.py` |
| #66 ↔ #67 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #69 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #66 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #70 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #71 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #76 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #67 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #69 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #69 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #69 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #69 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #69 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #69 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #70 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #70 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #70 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #70 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #70 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #70 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #71 ↔ #77 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #71 ↔ #78 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #71 ↔ #79 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #71 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #71 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #71 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #75 ↔ #76 | 3 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `.github/workflows/desktop-five-statement-windows-ci.yml` |
| #75 ↔ #77 | 3 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py` |
| #75 ↔ #79 | 3 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py` |
| #75 ↔ #80 | 3 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py` |
| #76 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #76 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #76 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #77 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #77 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #77 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #77 ↔ #80 | 3 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py`, `backend/tests/test_desktop_five_statement.py` |
| #78 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #78 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #78 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #79 ↔ #90 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #79 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #79 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #88 ↔ #89 | 3 | `backend/pyproject.toml`, `backend/src/aram_backend/local_auth.py`, `backend/tests/test_local_auth.py` |
| #90 ↔ #91 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #90 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #91 ↔ #92 | 3 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `PROJECT_STATUS.md` |
| #22 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #22 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #22 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #25 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `backend/migrations/versions/20260820_01_initial_schema.py` |
| #26 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #26 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #26 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #27 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #27 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #27 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #28 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #28 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #28 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #29 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #29 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #29 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #30 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #30 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #30 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #31 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #31 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #31 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #32 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #32 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #32 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #33 ↔ #34 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #33 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #33 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #34 ↔ #35 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #34 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #45 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #35 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #46 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #45 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #47 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #46 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #50 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #51 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #52 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #47 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #50 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #51 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #53 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #54 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #52 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #53 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #55 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #56 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #57 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #54 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `backend/src/aram_backend/main.py` |
| #55 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `backend/pyproject.toml` |
| #55 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #55 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `backend/src/aram_backend/main.py` |
| #56 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #56 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #59 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #60 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #61 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #62 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #63 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #64 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #65 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #66 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #67 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #69 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #70 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #71 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #76 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #77 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #78 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #79 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `backend/src/aram_backend/main.py` |
| #57 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #57 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md` |
| #59 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #59 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #60 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #60 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #61 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #61 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #62 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #62 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #63 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #63 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #64 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #64 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #65 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #65 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #66 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #66 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #67 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #67 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #69 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #69 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #70 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #70 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #71 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #71 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #71 ↔ #72 | 2 | `backend/src/aram_backend/five_statement_pipeline_cli.py`, `docs/FIVE_STATEMENT_PIPELINE_CLI.md` |
| #71 ↔ #73 | 2 | `backend/src/aram_backend/five_statement_pipeline_cli.py`, `docs/FIVE_STATEMENT_PIPELINE_CLI.md` |
| #72 ↔ #73 | 2 | `backend/src/aram_backend/five_statement_pipeline_cli.py`, `docs/FIVE_STATEMENT_PIPELINE_CLI.md` |
| #76 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #76 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #76 ↔ #80 | 2 | `backend/desktop/FIVE_STATEMENT_WINDOWS_README.md`, `backend/src/aram_backend/desktop_five_statement.py` |
| #77 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #77 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #78 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #78 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #79 ↔ #82 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #79 ↔ #88 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #82 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #82 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #82 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #88 ↔ #90 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #88 ↔ #91 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #88 ↔ #92 | 2 | `docs/PROJECT_LOG.md`, `PROJECT_STATUS.md` |
| #89 ↔ #92 | 2 | `backend/src/aram_backend/password_security.py`, `backend/tests/test_password_security.py` |
| #22 ↔ #25 | 1 | `docs/PROJECT_LOG.md` |
| #22 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #22 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #23 ↔ #55 | 1 | `backend/pyproject.toml` |
| #23 ↔ #88 | 1 | `backend/pyproject.toml` |
| #23 ↔ #89 | 1 | `backend/pyproject.toml` |
| #25 ↔ #26 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #27 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #28 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #29 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #30 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #31 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #32 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #33 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #34 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #35 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #45 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #46 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #47 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #50 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #51 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #52 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #53 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #54 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #55 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #56 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #57 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #59 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #60 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #61 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #62 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #63 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #64 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #65 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #66 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #67 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #69 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #70 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #71 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #76 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #77 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #78 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #79 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #90 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #91 | 1 | `docs/PROJECT_LOG.md` |
| #25 ↔ #92 | 1 | `docs/PROJECT_LOG.md` |
| #26 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #26 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #27 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #27 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #28 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #28 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #29 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #29 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #30 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #30 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #31 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #31 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #32 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #32 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #33 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #33 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #34 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #34 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #34 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #35 ↔ #44 | 1 | `docs/PROJECT_LOG.md` |
| #35 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #35 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #45 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #46 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #47 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #50 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #51 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #52 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #53 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #54 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #55 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #56 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #57 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #59 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #60 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #61 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #62 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #63 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #64 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #65 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #66 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #67 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #69 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #70 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #71 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #76 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #77 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #78 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #79 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #90 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #91 | 1 | `docs/PROJECT_LOG.md` |
| #44 ↔ #92 | 1 | `docs/PROJECT_LOG.md` |
| #45 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #45 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #46 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #46 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #47 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #47 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #50 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #50 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #51 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #51 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #52 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #52 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #53 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #53 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #54 ↔ #82 | 1 | `docs/PROJECT_LOG.md` |
| #54 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #56 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #56 ↔ #89 | 1 | `backend/src/aram_backend/main.py` |
| #57 ↔ #88 | 1 | `docs/PROJECT_LOG.md` |
| #57 ↔ #89 | 1 | `backend/src/aram_backend/main.py` |
| #59 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #63 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #64 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #66 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #67 ↔ #68 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #69 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #70 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #71 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #76 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #77 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #78 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #79 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #82 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #88 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #90 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #91 | 1 | `PROJECT_STATUS.md` |
| #68 ↔ #92 | 1 | `PROJECT_STATUS.md` |
| #70 ↔ #80 | 1 | `backend/src/aram_backend/five_statement_pipeline.py` |
| #74 ↔ #88 | 1 | `.github/workflows/backend-ci.yml` |
| #75 ↔ #81 | 1 | `backend/tests/test_desktop_five_statement.py` |
| #77 ↔ #81 | 1 | `backend/tests/test_desktop_five_statement.py` |
| #78 ↔ #81 | 1 | `backend/tests/test_desktop_five_statement.py` |
| #79 ↔ #81 | 1 | `backend/tests/test_desktop_five_statement.py` |
| #80 ↔ #81 | 1 | `backend/tests/test_desktop_five_statement.py` |
| #82 ↔ #89 | 1 | `backend/src/aram_backend/main.py` |

## 5. Sensitive-path name screen

- PR #23: `.github/workflows/security-checks.yml`
- PR #25: `backend/migrations/versions/20260820_01_initial_schema.py`, `backend/tests/test_migration_ddl.py`, `backend/tests/test_migration_schema.py`, `docs/T3_MIGRATION_REVIEW.md`
- PR #53: `backend/migrations/versions/20261030_02_unreviewed_mapping_drafts.py`
- PR #54: `backend/migrations/versions/20261030_03_system_staging_audit.py`
- PR #55: `backend/src/aram_backend/authenticated_identity.py`, `backend/tests/test_authenticated_identity.py`, `docs/superpowers/plans/2026-10-30-authenticated-principal-boundary.md`, `docs/superpowers/specs/2026-10-30-authenticated-principal-boundary.md`
- PR #56: `backend/src/aram_backend/authenticated_identity.py`, `backend/src/aram_backend/mapping_year_authorization.py`, `backend/tests/test_authenticated_identity.py`
- PR #57: `backend/migrations/versions/20261030_04_authored_drafts.py`, `backend/src/aram_backend/authored_mapping_draft.py`, `backend/tests/test_authored_mapping_draft.py`, `docs/superpowers/plans/2026-10-30-authored-mapping-draft-staging.md`, `docs/superpowers/specs/2026-10-30-authored-mapping-draft-staging.md`
- PR #88: `backend/migrations/env.py`, `backend/migrations/versions/20260820_01_initial_schema.py`, `backend/src/aram_backend/local_auth.py`, `backend/tests/test_local_auth.py`
- PR #89: `backend/src/aram_backend/auth_api.py`, `backend/src/aram_backend/local_auth.py`, `backend/src/aram_backend/password_security.py`, `backend/tests/test_auth_api.py`, `backend/tests/test_local_auth.py`, `backend/tests/test_password_security.py`, `docs/GATE3_PACKAGE9_1_SECURITY_REPORT.md`
- PR #92: `backend/src/aram_backend/password_security.py`, `backend/tests/test_password_security.py`

This heuristic is only a review aid. It does not prove that canonical data was modified; inspect the exact diff and source hash for any sensitive-looking path.

## 6. Integration controls

1. Review the parent-child dependency graph before interpreting shared paths.
2. For direct-to-baseline PRs, inspect the complete patch independently.
3. For stacked chains, compare each PR to its immediate base, not only the final head to the accepted baseline.
4. Identify files with multiple independent owners and choose one canonical implementation.
5. Treat financial workbooks, source ledgers, migrations, authentication, security and approval workflows as protected paths.
6. Do not cherry-pick from a child without the required parent commits.
7. Preserve all branches and worktrees until a clean integration candidate passes exact-head tests and independent review.

**Acceptance:** filename inventory and overlap screening only. No code, data, branch or PR state was modified.
