# SOURCE LINEAGE ANALYSIS

## Current State
The existing repository extracts aggregated values directly from the `سودوزيان` and `وضعيت مالي` sheets. There is no deep source lineage linking a final statement line back to the trial balance (T1/T2/T3/T4 dimensions).

## Required Lineage Depth
According to V2 Directive:
`Final Number → Note → Mapping → Account → Source Row`

## Data Gap
- The file `مبنای ارتباط حسابها با یادداشتها سال 1404.xlsx` provides mapping from Account Code to Note (`O, Oe, E` logic).
- **Update**: The raw trial balance rows for 1403 are now **present** in `سورس تهیه صورت مالی سال 1403.xlsx` (Sheet: `Source`). This file includes `AccountId`, `T1` through `T4` codes and names, and opening/closing balances. It also maps directly to Notes (`یادداشت کل`, `یادداشت جزء`).
- The current financial numbers are baked into the Note sheets and Statement sheets.

*Action*: We must parse the `سورس تهیه صورت مالی سال 1403.xlsx` into the database. We still need similar raw source files for 1402 and 1404 to complete full traceability across all years. The 1403 source validates that the 7-layer drill-down architecture is viable.
