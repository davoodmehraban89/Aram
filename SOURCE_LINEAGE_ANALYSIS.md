# SOURCE LINEAGE ANALYSIS & TRACEABILITY REPORT

## Executive Summary
This document defines the multi-tier audit lineage linking Primary Financial Statement figures back to Financial Statement Notes, Composite Mapping Rules, Trial Balance Accounts, and raw General Ledger source rows across fiscal years **1402**, **1403**, and **1404**.

---

## 1. Lineage Architecture

The system implements a 5-tier bidirectional drill-down architecture:

```
[Tier 1: Statement Cell]
        │  (Exact Sheet, Row, Col in financial_YYYY.xlsx)
        ▼
[Tier 2: Financial Note]
        │  (Note Sheet 6..39 in financial_YYYY.xlsx)
        ▼
[Tier 3: Mapping Rule]
        │  (Composite dimensional rule in mapping_1404.xlsx)
        ▼
[Tier 4: General Ledger Account]
        │  (4-digit 'حساب' / AccountId in source_YYYY.xlsx)
        ▼
[Tier 5: Raw Ledger Entry]
        │  (252,898 individual transactional rows in source_1404.xlsx)
```

---

## 2. Lineage Coverage Metrics & Disambiguation

Lineage status across all **252,898 general ledger data rows** in `data/source_ledgers/source_1404.xlsx` is categorized into strict, non-overlapping coverage classes:

| Lineage Class | Row Count | % Coverage | Lineage Status |
| --- | --- | --- | --- |
| **`UNIQUE_DETERMINISTIC_COVERAGE`** | **214,848** | **84.95%** | **Proven End-to-End Lineage**: Mapped deterministically through a single unique composite mapping rule. |
| **`AMBIGUOUS/MULTI_MATCH_RATE`** | **37,907** | **14.99%** | **Ambiguous Lineage**: Matches multiple mapping rules due to overlapping account definitions or missing sub-filters. *Not treated as proven lineage.* |
| **`UNMAPPED_RATE`** | **143** | **0.06%** | **Unmapped Lineage**: Matches zero mapping rules in `mapping_1404.xlsx`. |
| **TOTAL GENERAL LEDGER ROWS** | **252,898** | **100.00%** | Full active general ledger dataset for 1404. |

---

## 3. Statement-to-Note Cell Traceability Sample

All primary financial statements are mapped cell-by-cell in `NOTE_TO_STATEMENT_MATRIX.md`. Key statement line items map as follows:

| Statement | Fiscal Year | Line Item Caption | Statement Cell | Note Ref | Note Cell | Statement Amount (M Rials) | Verified Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Income Statement** | 1404 | درآمدهاي عملياتي | `سودوزيان!F10` | 5 | `سودوزيان!C10` | 243,097,686 | `MATCH` |
| **Income Statement** | 1404 | بهاي تمام شده درآمدهاي عملياتي | `سودوزيان!F11` | 6 | `سودوزيان!C11` | -245,897,444 | `MATCH` |
| **Balance Sheet** | 1404 | دارایی‌هاي ثابت مشهود | `وضعيت مالي!F10` | 10 | `وضعيت مالي!C10` | 673,740,637 | `MATCH` |
| **Balance Sheet** | 1404 | موجودی نقد | `وضعيت مالي!F18` | 15 | `وضعيت مالي!C18` | 19,951,136 | `MATCH` |
| **Cash Flow** | 1404 | نقد حاصل از عملیات | `جريان هاي نقدي!E7` | 23 | `جريان هاي نقدي!C7` | 99,230,533 | `MATCH` |
| **Cash Flow** | 1404 | پرداخت‌های نقدی بابت مالیات بر درآمد | `جريان هاي نقدي!E8` | 20-1 | `جريان هاي نقدي!C8` | -149,426 | `MATCH` |

*Scratchpad Column Isolation Note*: Working/scratchpad cells in statement workbooks (such as Column K in `جريان هاي نقدي` containing raw unformatted Rial calculations e.g., `109388328483`, `-33462657272375`, `41299837917`) are explicitly isolated and excluded from statement lineage.

---

## 4. Unmapped Ledger Exposure Lineage Reconciliation

Of the 143 unmapped rows:
1. **Account `8999` (11 rows)**: `حساب افتتاحیه و اختتامیه` (Opening/Closing Suspense Account) has gross debit/credit balances of `±1,310,883,439,013,116` Rials and **EXACTLY ZERO net closing balance**. Verified as a zero-net internal clearing exception.
2. **Account `8161` (110 rows)**: `حساب کنترل پیمانکاران` accounts for **100% of unmapped net closing balance exposure** (**196,907,918,801 Rials** / **196,908 Million Rials**).
3. **8 Zero-Closing Clearing Accounts (22 rows)**: Accounts `8184`, `8260`, `8488`, `8724`, `8767`, `8769`, and `8874` have non-zero turnover but **EXACTLY ZERO net closing balance**.

---

## 5. Source File Lineage Metadata
- **Official Statement Workbooks**: `data/official_statements/financial_1402.xlsx`, `financial_1403.xlsx`, `financial_1404.xlsx`.
- **General Ledger Source Workbooks**: `data/source_ledgers/source_1403.xlsx`, `source_1404.xlsx`.
- **Canonical Mapping Workbook**: `data/mappings/mapping_1404.xlsx`.
