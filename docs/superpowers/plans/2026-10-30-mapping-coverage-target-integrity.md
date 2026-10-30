# Issue #42 — regression and implementation plan

- Parent PR #28 SHA `02128c54109c7f1407b920a0027938029b9e1ae8`; parent #26 SHA `185e47f031902a8918c93c8dbb420122e7408403`, both Draft/unmerged.
- Child: Draft [PR #47](https://github.com/davoodmehraban89/Aram/pull/47); branch `codex/aram-gate3-coverage-target-guard-20261030`, based directly on PR #28.

1. [x] Add negative tests for stale same-year target, foreign-year target written with intentional SQL Core bypass, and mixed valid+invalid current rules; verify a valid latest note and no autoflush. Test-only SHA `f832c6d085b31190eacfaebbe92c0c806f3d3f94`.
2. [x] [RED CI 41067478817](https://github.com/davoodmehraban89/Aram/actions/runs/41067478817): **4 expected failures, 101 passed, 1 warning**, exposing false mapped status or absent invalid queue.
3. [x] Add batch note lookup, latest-note version resolution, invalid-reason reporting and conservative mapped/unmapped categorization. Code SHA `f858b44b3a3f79bcc7bd00b264ffdf11272fb1a9`.
4. [x] [GREEN CI 41067749994](https://github.com/davoodmehraban89/Aram/actions/runs/41067749994): **105 passed, 1 warning**, Alembic upgrade/downgrade and compileall success.
5. [ ] Verify final documentation SHA with GitHub Actions and six-file allowlist, complete patch and absence of forbidden paths.
6. [ ] Get real distinct non-author technical, accounting and release reviewer approvals bound to exact SHA; C1/C2/C3 remain BLOCKED. Accept PR #26/#28 before child and rerun tests after restacking.
7. [ ] Separate provider/concurrency safety remains Issue #43.

Scope: code, tests, this plan/spec, append-only project log and handoff. No financial source XLSX/PDF, data/, production DB, migration, dependency, workflow, release or binaries. Premerge rollback: close Draft; postmerge rollback: independently reviewed revert PR.
