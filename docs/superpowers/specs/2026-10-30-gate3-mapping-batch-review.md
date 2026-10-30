# Gate 3 — read-only batch Mapping change classification

**Proposed Draft PR #51**, child of **unmerged Draft PR #50** at exact SHA `f79947a8624adbd8e84c3f8247ac3ca4a7bd4240`; ultimately depends on Draft #26 and accepted base `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`.

**Problem:** a five-column Excel import currently calls `save_mapping_rule` directly, and a manual preview only evaluates one mapping. Bulk review must not silently use first/last matching row or apply one good row while hiding another conflicting/invalid row. This PR introduces a READ-ONLY, provider-neutral proposal classifier, **not** an approved Excel importer or an authorization change.

## Canonical input, classification and safe boundary

`ProposedMappingRow` carries explicit source locator, rule key, literal account code, actual in-scope note ID, mapping type, and expected persisted base version. Future Excel/manual/connector adapters must provide a validated row locator and exact scope; no source system table/column is invented.

A batch preview is bounded to **1–10,000** typed rows with unique, nonblank, trimmed, bounded source locators. It validates the year ID and requires the specified year to be Draft. It checks that no related financial-domain ORM edits are pending; uses `Session.no_autoflush` and does not commit or write.

For each scoped `rule_key`:
- **new:** no saved version; proposed version one; captures full old/new preview.
- **changed:** an existing rule is modified with exact current expected version; shows persisted old values and next proposed version.
- **unchanged:** current persisted rule is exactly the proposed content; no new version is produced, and no fake review decision is counted.
- **coalesced:** repeated identical input for the same rule key, including expected version; preserve the original and additional row locators, count at most one new/changed proposal.
- **conflict:** two or more rows for a rule key have different target/account/mapping-type/expected-base content; **every conflicting row** receives a conflict result. No silent first/last wins.
- **invalid:** nonexistent or stale account/note, cross-year target, wrong expected version, invalid input, or an identical repeat of an invalid first proposal.

Any conflict or invalid item sets `ready_for_review=False` **for the entire batch**, even if other rows are valid. An entirely unchanged batch is not an approvable change. A read-only preview never applies rules; omitted existing rules are not deletion instructions.

Outputs include per-row reason, stable locators, optional `MappingChangePreview`, deterministic review checksum and counts. This checksum is UNSIGNED: no actor identity, audit event, authenticated review, verified authorization, transaction lock or approval is encoded. An external apply service would still need transactionally re-validate the entire batch; there is deliberately **no apply function** here.

## Known limits and gates

- `mapping_change_preview.py` raises a typed `MappingNoChange` (subclass of the existing validation error) for valid no-ops; avoids unsafe error-message parsing. Existing public error semantics are preserved.
- Current `mapping_excel.import_mapping_workbook` is **unchanged** and can still save without this batch preview. It must be routed through a future approved common proposal/apply service; this PR does not claim bypass elimination.
- Source locator labels are presentation-only; an input adapter must attest actual source file SHA, sheet, and row. This batch preview is not a financial-source reconciliation.
- Different rule keys that overlap on a ledger account are not resolved by rule-key duplicate detection. Accounting owners must approve full account hierarchy, source predicate, multi-match precedence and note/subnote semantics before such overlap can be safely classified.
- The method is read-only but does not provide a cross-database transactionally consistent snapshot under all isolation levels. External SQL writers may mutate facts after preview; Issue #43 requires provider-level enforcement and concurrency controls.
- Genuine C1/C2/C3 independent reviewers and branch protection remain Issue #39; full durable Draft→Reviewed→Approved and audit remain Issue #49. Do not merge Draft #51 until parents and reviews are accepted.

## Acceptance harness

Synthetic cases: first-time batch without writes; identical duplicates coalesced; conflicting duplicates poison every row; valid old/new diff and no-op; stale version rejects only affected row and blocks all approval; foreign-year and unknown accounts; obsolete same-year target; all-noop no approval delta; deterministic digest and unrelated no-autoflush; pending dirty MappingRule rejected; empty/malformed/oversized batch; repeated locator; Approved/Locked year; malformed row fail closed. Exact-final-SHA remote GitHub CI, migration round-trip and compile needed. Do not read/change canonical financial XLSX/PDF, `data/`, customer databases, migrations, dependencies, workflows or releases.

Rollback: close this unmerged Draft, or use an independently reviewed revert after authorized merge.


## Additional financial identity and provenance hardening

- Python treats `True == 1`; a malformed Boolean `target_note_id=True` or `expected_base_version=True` must never coalesce with a valid integer `1`. Comparison signatures preserve **actual Python type** for each identifier/value; differing types yield explicit conflicting-source results, not a false "coalesced" success.
- A `source_locator` is an auditable provenance label; reject Unicode category `Cc`, `Cf`, and `Cs` (including newline, tab, NUL, bidi overrides and invisible format characters) rather than allowing log/row-spoofing. Source file hashes and actual cell coordinates must still be verified by the later Excel adapter.
- These are fail-closed **pre-review** rules only. They do not confer authenticated ownership, signed review, or ability to apply any Mapping proposal.
