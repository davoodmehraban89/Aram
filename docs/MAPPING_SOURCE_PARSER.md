# Mapping source parser

## Scope

`aram_backend.mapping_source_parser.parse_mapping_source` is the first read-only import boundary for the canonical mapping workbook. It reads the `Data` sheet using the existing mapping workbook inspection profile and retains original Excel row numbers and all source columns.

## Safety and accounting boundaries

- Formula cells are read as formula text; formulas are never evaluated.
- No mapping precedence is inferred.
- Duplicate rows are retained as separate source evidence.
- Dimension columns (including T1/T4 and current/capital classification when present) are preserved verbatim in `source_values`; this parser does not interpret their business meaning.
- Missing account, mapping type or note code is rejected.
- The parser is streaming and rejects more than 100,000 nonblank data rows.
- This module does not connect ledger rows to mapping rows and does not authorize a mapping.

## Next integration gate

Before implementing composite matching, record and test the exact header names and allowed values from an authorized copy of the mapping workbook. The matching layer must use the full account + dimensional key, expose zero/one/multiple matches, and never silently choose a rule. A finance owner must approve any normalization or precedence policy.
