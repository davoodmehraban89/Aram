# T6a — Read-only mapping and lineage diagnostic (documentary baseline)

**Status:** DOCUMENT_REVIEW_ONLY. This is a reproducible *document review*, not a fresh calculation against protected workbooks. No mapping decisions are authorized here.

## Source of figures

- `MAPPING_ANALYSIS.md` (accepted repository report)
- `SOURCE_LINEAGE_ANALYSIS.md` (accepted repository report)
- Canonical sources identified by those reports: `data/source_ledgers/source_1404.xlsx` and `data/mappings/mapping_1404.xlsx`; **not opened or modified in this task**.

## Reported 1404 row reconciliation

| Category | Rows | Denominator |
| --- | ---: | --- |
| All source rows | 252,898 | full ledger |
| System closing account 8999 (excluded from mapping only) | 11 | full ledger |
| Mapping-eligible rows | 252,887 | eligible ledger |
| Unique deterministic matches | 214,848 | eligible ledger |
| Ambiguous / multiple matches | 37,907 | eligible ledger |
| Unmapped | 132 | eligible ledger |

**Arithmetic checks on published figures:** 252,898 − 11 = 252,887; 214,848 + 37,907 + 132 = 252,887; 214,848 + 37,907 = 252,755 (any-match). The reports quote 84.96% unique, 14.99% ambiguous and 0.05% unmapped, rounded. These are *reported* counts, not newly verified against XLSX.

## Accounting and product risks

1. **37,907 ambiguous rows:** no single mapping lineage is proven. Do not auto-select a rule based on first match, row order or convenience.
2. **132 unmapped rows:** require explicit owner disposition; never silently drop from totals.
3. **11 account-8999 closing rows:** preserve in source and audit lineage; exclude only from mapping scope per documented domain decision. Do not delete.
4. **Version and approval:** mapping and reclassification O/OE/E/E2 need owner-approved interpretation and traceable versioning before T6/T7 computation.
5. **Cross-year and statement lineage:** verify the proposed statement → note → mapping → account → source-row links with the original source workbooks before claiming complete provenance.

## Required next diagnostic run (NOT EXECUTED)

On a controlled read-only checkout, hash the canonical XLSX files; load them without writeback; recompute row counts and composite-key cardinalities; export only a sanitized discrepancy summary; verify source file hashes unchanged. Record exact command, environment, script SHA, outputs and reviewer. Do not modify protected `data/` files or approve mapping rules as a side effect.

## Owner decision required before T6/T7

Resolve ambiguous rule classes and unmapped rows by explicit, auditable rules; confirm treatment of reclassification O/OE/E/E2 and target note/statement references. This diagnostic does not implement or approve those decisions.
