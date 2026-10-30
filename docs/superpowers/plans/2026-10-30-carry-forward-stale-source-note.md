# Issue #37 — test-first implementation and handoff

**Exact parent SHA:** `dfcf3f008df54498759243001bdfcd98669a8f23` (PR #30, unmerged, parent #26 unmerged).
**Child:** Draft [PR #45](https://github.com/davoodmehraban89/Aram/pull/45); branch `codex/aram-gate3-stale-note-guard-20261030`.

1. [x] Add regressions against the unchanged source: test-only SHA `109f43c263f6a78600ce57f8b943f34d1adea8ad`; [RED Backend CI 41067133189](https://github.com/davoodmehraban89/Aram/actions/runs/41067133189): **3 failed (old note accepted), 103 passed, one warning**.
2. [x] Resolve latest source note per note_number, version descending; if reference is stale, skip with `source_note_stale` instead of selecting a candidate. Code SHA `ee16035d85d35fe4dfb69ab2381ecb3f876e1fbc`.
3. [x] [GREEN Backend CI 41067277084](https://github.com/davoodmehraban89/Aram/actions/runs/41067277084): **106 passed, 1 warning**, Alembic upgrade/downgrade and compileall success.
4. [ ] Verify exact **final documentation SHA** with GitHub Actions and complete PR patch/allowlist. Correct record if additional commits alter head.
5. [ ] Obtain independent qualified C1/C2/C3 reviews on final SHA; all remain BLOCKED until actual separate identities/approvals. Do not self-merge or accept parent #30/#26.
6. [ ] After independent parent approvals, reconcile child base onto accepted SHA and rerun everything.

**Scope allowlist:** `mapping_carry_forward.py`, its tests, this spec, this plan, append-only project log and handoff. **Never** modify canonical financial data, DB, migration, dependency, workflow, binaries or release. Rollback while Draft: close unmerged PR; after authorized merge: separately reviewed revert.
