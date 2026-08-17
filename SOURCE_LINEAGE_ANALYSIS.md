# SOURCE LINEAGE ANALYSIS

## Current State
The existing repository extracts aggregated values directly from the `سودوزيان` and `وضعيت مالي` sheets. There is no deep source lineage linking a final statement line back to the trial balance (T1/T2/T3/T4 dimensions).

## Required Lineage Depth
According to V2 Directive:
`Final Number → Note → Mapping → Account → Source Row`

## Data Gap
- The file `مبنای ارتباط حسابها با یادداشتها سال 1404.xlsx` provides mapping from Account Code to Note (`O, Oe, E` logic).
- However, the raw trial balance rows with their actual amounts for 1402, 1403, and 1404 that feed into this mapping are **not present** as raw datasets.
- The current financial numbers are baked into the Note sheets and Statement sheets.

*Action*: Request the user to provide the Raw Trial Balance CSV/Excel files for 1402, 1403, 1404 to establish full 7-layer traceability. Otherwise, lineage ends at the "Note Row" layer.
