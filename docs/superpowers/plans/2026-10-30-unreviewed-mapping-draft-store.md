# Gate 3 — unreviewed-only durable proposal storage execution

**Issue #49**, candidate [Draft PR #53](https://github.com/davoodmehraban89/Aram/pull/53), based EXACTLY on unmerged [Draft #52](https://github.com/davoodmehraban89/Aram/pull/52) at `1063431b08a9e03e022aa9b8e6c5ed90bfb05395`. Upstream #51→#50→#26 unaccepted; accepted baseline `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` untouched.

1. [x] Inspected baseline SQLAlchemy/Base metadata, initial Alembic migration `20260820_01` using `Base.metadata.create_all`, PR #25 still unmerged and absence of application authentication/reviewer system.
2. [x] Added tests-only SHA `3ee1a4c44e9580ecc21a38ea26ea155841ebcaba`: [RED CI 41086027866](https://github.com/davoodmehraban89/Aram/actions/runs/41086027866) **missing implementation module** (test import failure).
3. [x] Added SQLAlchemy Core table on independent `MetaData` and strict unapproved-only persistence, scoped idempotency, re-verification and readback hash. Added explicit additive `20261030_02` migration. Initial CI surfaced **test fixture teardown** FK constraints when dropping `fiscal_years` before the independent table, plus an error-message mismatch for pending ORM changes. These were test/service lifecycle defects, not production DB failures; CI run [41086255707](https://github.com/davoodmehraban89/Aram/actions/runs/41086255707) is **FAILED**, do not omit this fact from history.
4. [x] Fixed fixture to drop the independent table before `Base.metadata.drop_all`; reject pending financial ORM edits before invoking the nested verifier. [GREEN CI 41086542121](https://github.com/davoodmehraban89/Aram/actions/runs/41086542121) on `b6c41f74055d6804d9f3af7bf321cdec0561ade3`: **179 passed, 1 warning**, both Alembic upgrade legs `->20260820_01->20261030_02`, both downgrades, compileall successful.
5. [x] Expanded synthetic DB integrity coverage: corrupted stored JSON, direct SQL duplicate idempotency key, migration metadata/FK isolation. Tests-only SHA `fe167c7b480517cecf302e92427d75afe51f2bc4`.
6. [ ] Verify new post-additional-tests CI and **final documentation SHA** CI, full changed paths, patch sanity, reviewer permissions and no protected file changes.
7. [ ] Independent real C1 technical/DDL, C2 qualified finance, C3 acceptance and owner approval; all blocked until real identities/branch protection exist (Issue #39). Upstream draft PRs must be accepted in order and fully restacked. PR #25 explicit initial DDL design must be reconciled to avoid migration collisions.
8. [ ] Later separate projects: actual trusted auth and role policy; durable Draft→Reviewed→Approved with actor separation, append-only audit; transactional CAS inside approved apply service; close legacy direct mapping import bypass, add provider concurrency tests, link authorized financial source ledger evidence (Issues #49, #43).

### Changed-path allowlist

- NEW `backend/src/aram_backend/mapping_draft_store.py`
- NEW `backend/tests/test_mapping_draft_store.py`
- NEW `backend/migrations/versions/20261030_02_unreviewed_mapping_drafts.py`
- NEW this focused spec and plan in `docs/superpowers/`
- APPEND ONLY `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`.

No customer/canonical accounting XLSX/PDF, `data/`, existing migrations, config/dependencies, GitHub workflows, credentials, binary, EXE, tag, release or accepted-branch writes. No login/role identity claimed. Do **not** migrate a production DB or merge as a substitute for reviewer acceptance.
