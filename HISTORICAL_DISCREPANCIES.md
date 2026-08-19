# HISTORICAL DISCREPANCIES & STRUCTURAL ANOMALIES

## Executive Summary
This document records all historical discrepancies, restatements, structural shifts, and excel authoring anomalies identified across the canonical official statement workbooks (`financial_1402.xlsx`, `financial_1403.xlsx`, `financial_1404.xlsx`) and general ledger files (`source_1403.xlsx`, `source_1404.xlsx`).

---

## 1. Statement Sheet Scratchpad Anomaly (Cash Flow & Financial Position)

### Anomaly Description
In canonical official statement workbooks (`financial_1402.xlsx`, `financial_1403.xlsx`, `financial_1404.xlsx`), certain statement worksheets contain raw, unformatted Rial working calculations or check figures in columns to the right of official statement columns (e.g., Column K in `جريان هاي نقدي` and Column N in `وضعيت مالي`).

### Examples
- **Row 8 Col K** in Cash Flow (`جريان هاي نقدي`): Contains `109388328483` (unformatted raw Rial working value for income tax).
- **Row 10 Col K** in Cash Flow (`جريان هاي نقدي`): Contains `-33462657272375` (unformatted raw Rial working value for investing cash flows).
- **Row 12 Col K** in Cash Flow (`جريان هاي نقدي`): Contains `41299837917` (unformatted raw Rial working value for tangible asset sales).
- **Row 19 Col K** in Cash Flow (`جريان هاي نقدي`): Contains `-301280000000` (unformatted raw Rial value for financing flows).
- **Row 21 Col K** in Cash Flow (`جريان هاي نقدي`): Contains `1594875501283` (unformatted raw Rial cash balance).

### Resolution & Audit Rule
Official financial statement line item figures are strictly extracted from authoritative statement columns (Column E for current year, Column G for comparative year in Cash Flow; Column F for current year, Column H for comparative year in Balance Sheet/Income Statement).
Scratchpad columns (Column K, L, N, etc.) are **never** concatenated or treated as financial statement line item values.

---

## 2. Structural Note Shifts Across Fiscal Years

1. **Note Merger (`Notes 36 & 37`)**:
   - Fiscal Year 1402 contains separate worksheets for Sheet `36` and Sheet `37`.
   - Fiscal Years 1403 and 1404 merge Notes 36 and 37 into a single combined worksheet named `36-37`.

2. **Note Addition (`Note 39`)**:
   - Note 39 (`39` - `خلاصه منابع و مصارف`) exists in 1403 and 1404 workbooks, but is completely absent in 1402.

3. **Signature Worksheet (`ص امضا`)**:
   - Present in 1402 and 1403 workbooks, but absent in 1404.

---

## 3. General Ledger Mapping-Scope Reconciliation

### Account 8999 System Closing Account — Excluded From Mapping Scope
- **Account**: `998999.0` (`حساب افتتاحیه و اختتامیه`).
- **Data**: 11 rows remain unchanged in `source_1404.xlsx`.
- **Business Classification**: Domain-confirmed system opening/closing account.
- **Mapping Status**: Excluded from mapping scope; not treated as a true unmapped-account exception.
- **Audit Rule**: Source rows are preserved for traceability, while mapping coverage denominators and unmapped-exposure metrics exclude these 11 rows.

### 132 True Mapping-Eligible Unmapped Ledger Rows Exposure
- **Total Unmapped Closing Exposure**: **196,907,918,801 Rials** (~196.91 Billion Rials / 196,908 Million Rials).
- **Account 8161 Concentration**: 100% of the closing balance exposure belongs to Account `8161` (حساب کنترل پیمانکاران) across 110 unmapped rows where specific T1/T4 combinations are missing from `mapping_1404.xlsx`.
- **Seven Zero-Closing Clearing Accounts**: 22 rows across 7 distinct zero-closing accounts (`8184`, `8260`, `8488`, `8724`, `8767`, `8769`, `8874`) have non-zero turnover but **EXACTLY ZERO net closing balance**.
