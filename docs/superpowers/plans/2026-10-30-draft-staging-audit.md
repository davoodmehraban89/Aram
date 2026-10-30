# Gate 3 — staging system audit, test-first execution and remaining gates

**Project:** ARAM, Issue #49. **PR:** [Draft #54](https://github.com/davoodmehraban89/Aram/pull/54), parent Draft #53 exact `3f089d03ca134cd73082dd0db8ba2461e1e6bc7c`; original accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

## Executed evidence

1. [x] Checked the actual parent PR #53, its independent SQLAlchemy Core table, Alembic `20261030_02`, test setup/teardown and absence of a trustworthy authenticated actor/approver service. Created dedicated child `codex/gate3-draft-staging-audit-20261030`, never merged a parent.
2. [x] Added 8 synthetic tests first at `82fb726d3e38c58270d8999bd68ad153ddbeceaf` for atomic staging event, same-transaction rollback, no second event on idempotent replay, direct SQLite UPDATE/DELETE forbidden, detection of draft payload replacement even when unkeyed payload SHA is recomputed, cross-year read rejection, DB uniqueness and absence of reviewer fields/approval. [RED CI 41088848958](https://github.com/davoodmehraban89/Aram/actions/runs/41088848958) **failed collection on missing `mapping_draft_audit` module**, a missing-feature proof (not a behavior regression).
3. [x] Added `mapping_draft_audit.py` and explicit `20261030_03` SQLite-only table/triggers. `mapping_draft_store.py` now inserts exactly one `DraftStaged` **SYSTEM** event in the same caller transaction; scoped reads verify the event against the original draft. Extended synthetic fixture to create and remove both independent tables safely. [GREEN CI 41089095498](https://github.com/davoodmehraban89/Aram/actions/runs/41089095498): **190 passed, one warning**, three Alembic upgrade legs, all reverse downgrades and compileall successful.
4. [x] Added 3 adversarial tests at `4ad6fc5239c9cf08e7fb960026d235ad05af438f`: parent draft delete must be FK-blocked while event exists, separate requests create distinct events, and migration must refuse preexisting `20261030_02` drafts unless their missing audit provenance receives an owner-approved backfill/recovery procedure. [RED CI 41089408299](https://github.com/davoodmehraban89/Aram/actions/runs/41089408299) **1 intended missing migration guard failure, 192 passed, one warning**.
5. [x] Added pre-DDL SQLite `SELECT 1 ... LIMIT 1` guard to `20261030_03` upgrade; it **raises RuntimeError for ANY existing Unreviewed drafts**. No synthetic historical audit fabricated. [GREEN CI 41089569653](https://github.com/davoodmehraban89/Aram/actions/runs/41089569653) on `01ab6a28447c27be1378ea48adb97dba6ca4ce72`: **193 passed, one warning**, migrations up/down and compileall successful.
6. [ ] Run final exact docs-head CI after focused spec/plan, append-only project log and handoff; check remote PR full changed-file list and patch, accepted SHA, reviewer count and parent exact SHA.
7. [ ] **Blocked by genuine independent acceptance:** upstream Draft PRs #26→#50→#51→#52→#53 and migration design PR #25 remain unmerged; three qualified non-author C1/C2/C3 reviewers absent under Issue #39. Never self-approve/merge.
8. [ ] Future separately reviewed work: real actor identity integration, author/reviewer separation, meaningful approval/rejection/rework lifecycle, append-only human financial decisions with authenticated provenance, transactional version compare-and-set and audited mapping rule apply, shared XLSX path, documented full note/subnote semantics, provider-specific security and canonical 1402–1404 reconciliation.

## Exact PR allowlist

- NEW `backend/src/aram_backend/mapping_draft_audit.py`.
- MODIFY `backend/src/aram_backend/mapping_draft_store.py`.
- NEW `backend/migrations/versions/20261030_03_system_staging_audit.py`.
- MODIFY `backend/tests/test_mapping_draft_store.py`.
- NEW focused `docs/superpowers/specs/2026-10-30-draft-staging-audit.md` and this plan.
- APPEND-ONLY `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`.

No canonical XLSX/PDF, `data/`, actual customer or production database, original migrations, dependencies, workflows, credentials, releases, executables or accepted-branch writes.

## Not a compliant financial audit

The event is **SYSTEM-created staging evidence**, not a human audit decision. SQLite triggers resist ordinary DML UPDATE/DELETE, not DB administrators who drop triggers, replace the SQLite DB or forge insert events. Event hash is unsigned/unkeyed; neither trusted actor provenance nor external WORM/anchored immutability is provided. Dialects other than SQLite are deliberately refused before DDL. Upgrade to migration 03 on DB with old drafts **blocks deliberately** until explicitly authorized retention and provenance handling. An approved downgrade deletes the event table and needs a reviewed backup/retention plan. Gate 3 stays formally unaccepted.
