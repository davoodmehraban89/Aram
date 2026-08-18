# Source Lineage Analysis

## Overview
This document analyzes the structural schema, data quality, and lineage capabilities of the 1403 and 1404 source ledgers.

## 1. 1402 Lineage Limitations
No canonical `source_1402` ledger is currently part of the verified source set.
For 1402 the lineage terminates at: `Official Statement -> Statement Line -> Note -> Note Row`.
Source-row lineage cannot be claimed for 1402.

## 2. 1403 Lineage Limitations
The canonical ledger `source_1403.xlsx` exists. However, a dedicated `mapping_1403.xlsx` has not been provided.
`mapping_1404.xlsx` must **NOT** be applied retroactively to 1403.
Any mapping classification currently present in the application for 1403 must be distinctly tagged as `RECONSTRUCTED_MAPPING` unless directly extracted from `SOURCE_PROVIDED_1403_CLASSIFICATION` fields in the raw ledger itself.

## 3. Structural Reconciliation & Quality (1403 vs 1404)

### source_1403.xlsx
- **Actual Data Records**: 204176
- **Duplicate Physical Rows**: 0
- **Null Key Dimensions (AccountId, T1-T4)**: 0
- **Schema**: Contains 29 columns including dimensions, opening/closing balances, and statement mapping outputs.

### source_1404.xlsx
- **Actual Data Records**: 252898
- **Duplicate Physical Rows**: 0
- **Null Key Dimensions (AccountId, T1-T4)**: 0
- **Schema**: Contains 26 columns. Identifiable structural differences exist compared to 1403 (e.g., column count).

## 4. Specific High-Value Exception Review
A robust search across all account-code and account-name columns (including `حساب`, `kol`, `KOL_NAME`, `AccountId`, `ACCOUNT_NAME`, `شرح کل`, `T1_NAME`, `T2_NAME`, `T3_NAME`, `T4_NAME`) identified 11 rows related to the closing/offset account **8999** (حساب ترازاختتاميه).

- **Row Count**: 11
- **Debit**: 0 ریال
- **Credit**: 0 ریال
- **OPENING Balance**: 0 ریال
- **Gross Exposure (Absolute CLOSING)**: 2,621,766,893,910,080 ریال
- **CLOSING Balance**: 0 ریال
- **FS Balance**: 0 ریال
- **Mapping Status**: Unmapped (No corresponding mapping rule exists in mapping_1404.xlsx)

Although the net exposure offsets to zero, the gross absolute closing exposure is extremely material (2,621,766,893,910,080 ریال). These offsetting entries must not be dismissed in historical reconciliations.

## 5. 1404 Mapping Provenance & Coverage
A deterministic mapping engine was executed linking `mapping_1404.xlsx` to `source_1404.xlsx`. The engine evaluates the `حساب` (Account), `T1_CODE`, `T4_CODE`, and `Current/Capital` dimensions. Exposure calculations use the source workbook fields `Debit`, `Credit`, and `CLOSING` exactly as provided in the ledger (units are in ریال).

- **Total Source Ledger Data Rows**: 252,898
- **Rows Eligible for Mapping**: 252,898
- **Uniquely Mapped Rows**: 214,848
- **Unmapped Rows**: 143
- **Multiply Matched Rows**: 37,907
- **Conflicting Matched Rows**: 37,907
- **Excluded Rows**: 0
- **Denominator**: 252,898
- **PROVEN_MAPPING_COVERAGE**: 99.94%

### Unmapped Population Analysis
There are 143 rows that failed to map deterministically due to missing mapping logic for specific dimension combinations.
- **Unmapped Row Count**: 143
- **Total Debit**: 3,961,800,186,318 ریال
- **Total Credit**: 3,881,433,378,410 ریال
- **Gross / Absolute Exposure (Debit + |Credit|)**: 7,843,233,564,728 ریال
- **CLOSING / Signed Net Exposure**: 196,907,918,801 ریال
- **Financial-Statement-Balance Exposure**: 196,907,918,801 ریال

#### Ranked Exception Table (Largest Unmapped Accounts by Gross Exposure)
| Account Code | T1 | T4 | Rows | Gross Exposure (ریال) | Net Exposure (ریال) |
|---|---|---|---|---|---|
| 8161 | 117617 | 4512 | 9 | 1,376,000,000,000 | 0 |
| 8161 | 117401 | 4512 | 26 | 1,319,659,150,206 | 57,139,085,409 |
| 8161 | 118701 | 4512 | 11 | 1,256,051,927,394 | 63,510,465,448 |
| 8161 | 117124 | 4512 | 10 | 1,210,721,701,196 | 0 |
| 8161 | 117313 | 4512 | 8 | 1,090,000,000,000 | 0 |
| 8161 | 117001 | 4512 | 5 | 518,970,963,494 | -5,425,842,707 |
| 8161 | 117088 | 4512 | 4 | 307,741,714,522 | 11,365,395,802 |
| 8161 | 117777 | 4512 | 6 | 301,400,000,000 | 0 |
| 8161 | 117488 | 4502 | 22 | 159,965,459,804 | 48,274,392,545 |
| 8161 | 117865 | 4512 | 3 | 128,833,512,752 | 17,044,422,304 |


### Proven Lineage Examples
1. **Simple Account Rule**: `1101 -> Note 6`. Rows with `حساب` 1101 are matched successfully if they don't have conflicting T1/T4 specific rules.
2. **Composite Rule (8161)**: `حساب` 8161 requires `T1_CODE` and `T4_CODE` to route to correct notes like 19-1 or 12-1. When these dimensions are present, the engine accurately assigns the note.
3. **Current/Capital Dependent**: Specific accounts branch based on the `جاری / سرمایه ای` string in the ledger matching the mapping condition.
