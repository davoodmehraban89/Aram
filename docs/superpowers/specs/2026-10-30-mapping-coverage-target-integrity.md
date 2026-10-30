# Issue #42 — current-note target integrity in read-only Mapping coverage

**Status:** Draft PR #47; not accepted. **Exact parent:** unmerged PR #28 at `02128c54109c7f1407b920a0027938029b9e1ae8` (PR #26 unmerged).

## Failure mode and accounting contract

Earlier `inspect_mapping_coverage` counted every latest rule's `target_note_id` as mapped when the account existed, regardless of target fiscal year, deleted/missing target or obsolete same-year NoteDefinition version. This could give a false positive green mapped status, particularly for rule targets changed via a SQL/bulk path bypassing ORM hooks.

- Select current account/rule versions deterministically, as before.
- Resolve each latest rule's actual target NoteDefinition (in one batch SELECT), plus latest version per `note_number` for the **requested** fiscal year, ordered by version descending then id descending.
- Treat missing target (`target_note_missing`), foreign fiscal year (`target_note_wrong_year`) and stale same-year note version (`target_note_stale`) as deterministic invalids.
- Add an **additive queue** `invalid_target_rules: tuple[(rule_key, account_code, reason), ...]` sorted for stable review. No automatic repairs.
- **Fail closed:** an account with any invalid current rule is **unmapped/action-needed**, even when another current rule is valid. Never call it cleanly mapped. Preserve the `total_accounts == len(mapped)+len(unmapped)+len(ambiguous)` partition and existing orphan-rule behavior.
- A wholly valid one-target rule remains mapped; multiple distinct valid targets remain ambiguous.
- Use `Session.no_autoflush`; no writes and no fabricated accounting figures. All integrity tests operate on synthetic fixtures only.

## Limits

Coverage diagnostics do not enforce database constraints; direct SQL can bypass ORM protection and is intentionally simulated for one cross-year test. Database locks/concurrency and real Peyvast connector remain Issue #43. No canonical financial workbooks are read or changed. Qualified independent C1 technical/security, C2 financial correctness and C3 acceptance reviews remain mandatory on the exact final SHA; parent dependencies cannot be skipped.
