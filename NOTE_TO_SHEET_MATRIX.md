# NOTE TO SHEET MATRIX

In the current dataset, the mapping between a Note and its Source Sheet is 1:1.

| Logical Note | Source Workbook Sheet Name | Years Applicable |
| --- | --- | --- |
| یادداشت ۶ | `6` | 1402, 1403, 1404 |
| یادداشت ۷ | `7` | 1402, 1403, 1404 |
| یادداشت ۸ | `8` | 1402, 1403, 1404 |
| ... | ... | ... |
| یادداشت ۳۵ | `35` | 1402, 1403, 1404 |
| یادداشت ۳۶ | `36` (1402), `36-37` (1403, 1404) | 1402, 1403, 1404 |
| یادداشت ۳۷ | `37` (1402), `36-37` (1403, 1404) | 1402, 1403, 1404 |
| یادداشت ۳۸ | `38` | 1402, 1403, 1404 |
| یادداشت ۳۹ | `39` | 1403, 1404 |

*Observation*: Some notes (e.g., 36 and 37) are merged into a single sheet in later years. The ingestion engine must support multi-note parsing from a single sheet.
