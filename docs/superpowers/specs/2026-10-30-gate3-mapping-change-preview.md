# ARAM Gate 3 — current note targets and read-only mapping change preview

**Status:** PROPOSED, unaccepted Draft [PR #50](https://github.com/davoodmehraban89/Aram/pull/50). **Parent:** Draft [PR #26](https://github.com/davoodmehraban89/Aram/pull/26) exact SHA `185e47f031902a8918c93c8dbb420122e7408403`. Accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` is unchanged.

## Financial integrity contract

The existing explicit `save_mapping_rule` validated *same fiscal year* but could persist a MappingRule that targets an **obsolete NoteDefinition version** of that year. A later review would classify it stale, while initial persistence had already succeeded. This is an inconsistent financial classification boundary.

- `save_mapping_rule` must reject stale NoteDefinition targets, where stale means a different NoteDefinition of the same `year_id` and `note_number` has the latest `version DESC, id DESC`. This check must happen **before** replay/idempotence handling, preventing an obsolete rule from silently being reaffirmed.
- A current target version remains valid for explicit persistence, subject to the existing Draft, company/year/account code, length, input and caller-controlled commit checks.
- This guard is **SQLAlchemy ORM/service only**, not DB protection against raw SQL, bulk SQL, external writers or races. Provider-level enforcement is a later gate [Issue #43](https://github.com/davoodmehraban89/Aram/issues/43).

## Review preview contract — NOT approval

Provide `preview_mapping_change` as a deterministic, strictly **read-only** preparation stage for a future authenticated human approval workflow:

1. Caller must supply positive `year_id`, exact `rule_key`, `account_code`, `target_note_id`, `mapping_type` and a nonnegative `expected_base_version`. `0` is the explicit precondition that this rule key has no saved version.
2. Fiscal year must be Draft; account must exist in the same year; note must exist in the same year **and be its latest version**. Never guess account, note, version, precedence or financial value.
3. Read the latest rule for the exact year/key. Reject a stale expected version, and reject a no-op proposal instead of pretending it is a review decision. Propose **exactly** `previous.version + 1` (or version 1 on first creation).
4. Return immutable old/new snapshots, fiscal year and company IDs, latest target-note version/number, latest account version ID/version and deterministic SHA-256 fingerprint of their canonical JSON representation. This digest is an **unsigned comparison checksum**, **not** user identity, authorization, review proof, tamper-resistant signature or approval.
5. `verify_mapping_change_preview_current` must regenerate all authoritative values from the Session and reject changed rule version/target, account version, target-note version, fiscal-year status or altered preview data. It only checks staleness at query time and does **not** save changes.
6. Fail closed on unflushed pending changes to FiscalYear, AccountVersion, MappingRule or NoteDefinition rather than silently capture a misleading persisted snapshot. Unrelated pending Company objects are not implicitly flushed. Query path uses Session.no_autoflush.
7. **No approval state transition**, actor account, role, audit write, generated statement, mapping mutation, automatically persisted candidate or financial source file can be produced by either preview function.

## Why this is not a complete approval lifecycle

A caller still can invoke the existing low-level `save_mapping_rule` directly without going through preview. No authenticated principal, qualified reviewer roster, approved mapping decision, immutable audit trail or DB-level transaction lock is in place. Even a perfectly matching `verify` result is not safe against a concurrent update *after* verification. Only a separately reviewed authenticated approval endpoint/service with strict user roles, distinct identities, transactional version compare-and-set, immutable audit and provider-specific isolation may execute an Approved transition.

Those outstanding deliverables remain tracked by [Issue #49](https://github.com/davoodmehraban89/Aram/issues/49), [Issue #39](https://github.com/davoodmehraban89/Aram/issues/39) and [Issue #43](https://github.com/davoodmehraban89/Aram/issues/43). Do not advertise this PR as Gate 3 complete or merge before parent and independent C1/C2/C3 controls pass.

## Acceptance tests

Synthetic-only regression: stale same-year note rejected on save and on attempted idempotent replay; latest note allowed. Read-only preview: creation, current old/new, version increments, no-op, stale expected version, changed source rule, changed note, changed account, year lock, wrong-year target, falsified comparison fields, invalid inputs, fail-closed pending writes, no autoflush and no DB mutation. Full pytest, disposable Alembic round-trip, compileall and final-head CI; independent finance acceptance required. No customer XLSX/PDF or production database touched.

**Rollback:** close the unmerged Draft, or revert with separately reviewed PR after authorized merge.


## Explicit external-writer / identity-map stale-read control

A Session identity map may hold objects loaded before an independent connection updated a Rule or FiscalYear. Calling `Session.get` without refresh, or executing an ORM select without refreshing existing identity-map objects, can **return stale object fields** even when a SQL SELECT runs. Merely recalculating a fingerprint against those cached objects is inadequate.

- For the fiscal-year row and requested NoteDefinition use `Session.get(..., populate_existing=True)`; for the latest Rule, latest NoteDefinition and latest AccountVersion queries use `.execution_options(populate_existing=True)`. All remain within `Session.no_autoflush` and the clean-related-Session precondition.
- Synthetic two-session tests prove the former implementation wrongly accepted the old preview after an independent SQL UPDATE of the same Rule content or FiscalYear status.
- This improvement refreshes visible committed state under the **test SQLite transaction behavior**. It is **not** an isolation-level guarantee for every provider, not a lock, and cannot prevent a concurrent transaction that commits *after* verification. Provider-specific transaction/compare-and-set enforcement and human approval remain separate.
