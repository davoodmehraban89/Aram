# Issue #38 — test-first remediation and evidence

- Parent: Draft [PR #27](https://github.com/davoodmehraban89/Aram/pull/27) `6c0068a660a3834f042b89d41d62bba82cb3a498`; depends on Draft PR #26.
- Child: Draft [PR #46](https://github.com/davoodmehraban89/Aram/pull/46); branch `codex/aram-gate3-hidden-xlsx-guard-20261030`.
- [x] Add adversarial hidden-sheet/row/header/column plus import pre-write regression tests, test-only `e266906686a265d32dfdf8032c0cafec32ff3a73`. [RED CI 41067372049](https://github.com/davoodmehraban89/Aram/actions/runs/41067372049): **8 expected failures, 109 passed, 1 warning** (missing ValueError).
- [x] Implement pre-parse visibility rejection using read-only sheet state and streaming worksheet XML; code `34500e8f0ba877f5f19839be8946790f5c163599`.
- [x] [GREEN CI 41067615098](https://github.com/davoodmehraban89/Aram/actions/runs/41067615098): **117 passed, 1 warning**; isolated Alembic upgrade/downgrade and compileall succeeded.
- [ ] Final code+documentation SHA: verify CI and changed file allowlist again; test permission/reviewer protocol.
- [ ] C1 technical / XLSX security, C2 financial correctness, C3 acceptance reviewer identities must be distinct from author and approve exact SHA; currently BLOCKED. Do not merge child before parent.
- [ ] Later: adversarial workload performance, unusual XML namespace/encoding and workbook presentation edge cases under independent review. This change does not prove all Excel display semantics or Windows compatibility.

**Allowed:** `mapping_excel.py`, its test file, this spec/plan, append-only `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`. No financial XLSX/PDF, `data/`, real database, migration, dependency, workflows, binary/release. Rollback while Draft: close unmerged PR; after acceptance: reviewed revert PR.


## Additional adversarial visibility cases (2026-10-30)

- Follow-up tests-only commit `0e78c2241ddf373bd9a1beac8db21d3b44686f09` checks Excel `veryHidden` sheet state, hidden column group spanning the contract, and attempted import of a veryHidden-only Mapping workbook.
- [Backend CI 41069448589](https://github.com/davoodmehraban89/Aram/actions/runs/41069448589) on this head: **120 passed, 1 warning**, isolated Alembic upgrade/downgrade and compile successful. These are incremental proof beyond the initial 117-test GREEN run, not replacement for historical regression evidence.
- A final documentation-head CI is required once this record and handoff are appended. The Draft remains unapproved and unmerged.
