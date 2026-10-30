# Issue #38 — mapping Excel visibility integrity policy

**Status:** Draft PR #46, stacked on unmerged PR #27 `6c0068a660a3834f042b89d41d62bba82cb3a498` (PR #26 unmerged). Not accepted.

## Failure mode

`preview_mapping_workbook` used `openpyxl.load_workbook(read_only=True)` and iterated mapping cells but ignored `sheet_state` and hidden rows/columns. An operator may visually review one dataset while the parser silently imports unseen mapping decisions.

**Fail-closed policy:** The only worksheet `Mapping` must have `sheet_state == visible`. Reject any marked-hidden Mapping row, including header/spacers, and any hidden column intersecting the 5-field Mapping contract. Also reject malformed hidden column ranges; make the failure deterministic and pre-database.

### Parsing design

- Maintain existing max archive bytes (10 MiB compressed / 40 MiB summed member uncompressed), entry limits, row limits, workbook single-sheet contract, formulas, strict data types and duplicate identity rules.
- Use openpyxl **read-only worksheet** for cell parsing; it does not expose `row_dimensions` or `column_dimensions`.
- Use a second **streaming XML iteration** over the same bounded worksheet member (`sheet._worksheet_path`) to inspect `row`/`col` hidden flags and related range attributes. Do not force full load_workbook(read_only=False) for untrusted XLSX. Clear processed XML elements.
- Treat hidden values `1` or `true` as hidden. No hidden contract data can reach `import_mapping_workbook`, because import begins with preview before a savepoint is opened.
- Deliberately reject hidden row metadata even if its cells appear blank; visible mapping workbooks remain valid.
- This addresses visibility metadata, not malicious spreadsheet macros, external Excel renderers or content hidden through all possible style/conditional-rendering techniques. Revisit remaining display mismatches in later security review.

### Acceptance

Tests on synthetic visible/hidden sheet, hidden header/data row, first/last contract column, and no-database-mutation import; RED → GREEN exact-head backend pytest, migration round-trip and compile. Qualified independent C1/C2/C3 must review this code and its XML parser limits. No real customer data modified, no merge until parent and review gates pass.
