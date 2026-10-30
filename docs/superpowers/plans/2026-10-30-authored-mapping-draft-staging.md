# Gate 3 authenticated Unreviewed Mapping proposal staging — execution

**Issue #49**, [Draft PR #57](https://github.com/davoodmehraban89/Aram/pull/57), exact parent unmerged [Draft #56](https://github.com/davoodmehraban89/Aram/pull/56) SHA `0fc0713bd9e0906954c16d7a6b25aad8bf793383`. Accepted branch `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

1. [x] Inspected GitHub's actual PR #56 and code: RSA-verified subject and signed year scope in read-only routes only; unbound `save_unreviewed_batch`, separate insert-only SYSTEM staging events and no author record. No real enterprise IdP or approval endpoint. Continued in exact-parent stacked branch.
2. [x] Added test-first `backend/tests/test_authored_mapping_draft.py`, commit `b31bf83778a1e5bcb404290fd00a7e5c445fd6e9`: signed scoped proposer can stage exactly one 3-record unit; wrong role/company/year/identity rejected; legacy request-key cannot be stolen; replay idempotent only with same actor; forged JSON/header/Bearer rejected; author records insert-only; forced author insert failure atomically rolls back draft and system event; reviewer same (`issuer`, `subject`) denied; separately signed distinct reviewer passes *read-only* separation check, no MappingRule modification. [RED CI 41116237163](https://github.com/davoodmehraban89/Aram/actions/runs/41116237163) **FAILED test collection** with missing new `authored_mapping_draft` module (missing-feature RED, not demonstrated business behavior).
3. [x] Added new independent `mapping_draft_authors` Core table and service. Explicit SQLite-only `20261030_04` Alembic migration adds restrictive FK, unique author per draft, CHECK proposer-only and UPDATE/DELETE-denying triggers; refuses non-SQLite. Existing legacy unbound drafts remain unbound and cannot be retroactively claimed. No WORM or signed external evidence implied.
4. [x] Added strict Pydantic request DTO + **only** new mutation endpoint `POST /api/v1/mapping/unreviewed-drafts` with verified RS256 principal + current exact same-company/year `mapping_proposer` grant. Uses one SQL transaction: draft, `DraftStaged` event and immutable proposer binding; no real finance review/approval/MappingRule apply.
5. [x] [GREEN CI 41116509978](https://github.com/davoodmehraban89/Aram/actions/runs/41116509978) on code SHA `ed9703da28d04bef7d09692a974322987280f401`: **275 passed, 2 warnings**, disposable Alembic `20260820_01→20261030_02→20261030_03→20261030_04` and full reverse downgrade, compileall succeeded.
6. [ ] Add focused spec (already added), plan and append-only logs/handoff, verify full remote allowlist and exact PR parent, **run CI on final documentation SHA**, confirm reviewers remain unaccepted and original branch unchanged. Update PR and Issue #49/#11 with evidence (do not claim final SHA green until checked).
7. [ ] Real C1 technical/security, C2 finance/account source hierarchy and C3 DB/release independent non-author reviews must be obtained from actual qualified humans. All upstream PRs #26→#50→#51→#52→#53→#54→#55→#56 remain Draft/unmerged. Exact revision integration with initial DDL PR #25 and migration service-compatibility needs separate review.

## Allowed paths

- NEW `backend/src/aram_backend/authored_mapping_draft.py`.
- MODIFY `backend/src/aram_backend/main.py`.
- NEW `backend/migrations/versions/20261030_04_authored_drafts.py`.
- NEW `backend/tests/test_authored_mapping_draft.py`.
- NEW focused spec and plan under `docs/superpowers/`.
- APPEND only `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`.

No canonical accounting XLSX/PDF, `data/`, customer SQL, actual production database, original migrations, dependencies, GitHub workflow, signing private key, binary, release, accepted branch or human reviewer state modified.

## Important unfinished security controls

This PR is a *new identity-bound staging route*, not a global replacement for the old unbound staging service or Excel importer. Even a success from the read-only `check_independent_mapping_reviewer` is NOT approval: no durable reviewer decision, immutable signed audit, lock/CAS or atomic MappingRule posting. A Python `VerifiedPrincipal` object is not proof of authentication outside the FastAPI RSA dependency. All tests use synthetic test users and temporary signing keys. Enterprise IdP installation, stable scopes and roles, key rotation/revocation, real company users, financial accounting validation and true C1/C2/C3 signoffs remain absent. Never merge, deploy to actual financial ledger or describe Gate 3 as accepted.

Rollback before merge: close Draft. After independently approved merge, any migration downgrade destroys author evidence and requires explicit recovery/retention review.
