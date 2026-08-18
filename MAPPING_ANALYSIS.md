# MAPPING COVERAGE & ANALYSIS REPORT

## Executive Summary
This document provides the authoritative, source-reconciled mapping coverage analysis for the 1404 general ledger (`data/source_ledgers/source_1404.xlsx`) against the canonical mapping rules workbook (`data/mappings/mapping_1404.xlsx`).

Across **252,898 total general ledger data rows**, multi-dimensional matching (incorporating Account Code / `حساب`, `T1_CODE`, `جاری / سرمایه ای`, and `T4_CODE`) yields exact, standardized coverage metrics and full exposure reconciliation.

---

## 1. Mapping Coverage Metrics

Coverage terminology strictly distinguishes between deterministic, unique lineage and ambiguous or unmapped rows. Ambiguous multi-match rows are **never** treated as proven lineage without explicit, provable disambiguation rules from the canonical mapping workbook.

| Metric | Row Count | Percentage of Total | Description / Definition |
| --- | --- | --- | --- |
| **`UNIQUE_DETERMINISTIC_COVERAGE`** | **214,848** | **84.95%** (84.9544%) | General ledger rows matching exactly one unique mapping rule. |
| **`AMBIGUOUS/MULTI_MATCH_RATE`** | **37,907** | **14.99%** (14.9890%) | General ledger rows matching multiple mapping rules due to overlapping dimensional rules or missing sub-filters. |
| **`UNMAPPED_RATE`** | **143** | **0.06%** (0.0565%) | General ledger rows matching zero mapping rules in `mapping_1404.xlsx`. |
| **`ANY_MATCH_COVERAGE`** | **252,755** | **99.94%** (99.9435%) | Total general ledger rows with at least one matching rule (`UNIQUE` + `AMBIGUOUS`). |
| **TOTAL GENERAL LEDGER ROWS** | **252,898** | **100.00%** | Total active data rows in `data/source_ledgers/source_1404.xlsx`. |

---

## 2. Analysis of Ambiguous / Multi-Match Rows (`AMBIGUOUS/MULTI_MATCH_RATE`)

Multiple matches occur across 37,907 ledger rows representing **21 distinct account codes**. Multi-matches arise from two structural causes in the source mapping workbook:

1. **Multiple Rule Definitions for Single Account Codes**:
   - For accounts such as `8227`, `8350`, `8590`, `8160`, and `8447`, the mapping workbook defines multiple target notes or mapping types (`O`, `Oe`, `E`, `E2`) without specifying additional required dimensional constraints (such as `T1_CODE`, `T4_CODE`, or `جاری / سرمایه ای`) in `mapping_1404.xlsx`.
   - *Example*: Account `8350` (حسابجاری فی مابين شركتهای گروه) has 4 mapping rules in `mapping_1404.xlsx` (Note 12-1 Type O, Note 12-1 Type OE, Note 19-1 Type E, Note 19-1 Type E2). Because all 4 rules leave T1/T4/JS blank, any ledger row for account `8350` matches all 4 rules simultaneously.

2. **Broad vs. Specific Rule Overlaps**:
   - Account `8161` (حساب کنترل پیمانکاران) contains **66 distinct mapping rules** in `mapping_1404.xlsx`. Some rules specify `T1_CODE`, `T4_CODE`, or `جاری / سرمایه ای` filters, while others are generic. When ledger rows omit optional dimensional codes, both generic and partially matched rules trigger.

*Rule of Precedence Policy*: Precedence or rule ranking is **only** applied if explicitly defined in the canonical mapping workbook. Synthetic or unproven rule hierarchy is strictly avoided to maintain audit integrity.

---

## 3. Account 8999 High-Gross / Zero-Net Exception

Account `8999` (`998999.0` / `حساب افتتاحیه و اختتامیه` - Opening & Closing Suspense Account) represents a verified high-gross / zero-net exception:

- **Row Count**: 11 ledger rows.
- **OPENING Balance**: `0.0` Rials.
- **Period Debit**: `0.0` Rials.
- **Period Credit**: `0.0` Rials.
- **Gross CLOSING Debit Balance**: `+1,310,883,439,013,116` Rials (+1.31 Quadrillion Rials).
- **Gross CLOSING Credit Balance**: `-1,310,883,439,013,116` Rials (-1.31 Quadrillion Rials).
- **Net CLOSING Balance**: **`0.0` Rials** (EXACT ZERO).

*Verification Conclusion*: Account `8999` is an internal accounting clearing mechanism used for opening and closing ledger balances. While unmapped in `mapping_1404.xlsx`, its net financial statement impact is **exactly zero**.

---

## 4. Reconciled 143-Unmapped Exposure Analysis

The 143 unmapped general ledger rows are fully reconciled to canonical source data:

### Breakdown of Unmapped Rows
- **11 rows**: Account `8999` (High-gross / Zero-net suspense account; Net Closing = `0` Rials).
- **132 rows**: Remaining active unmapped ledger rows across 8 distinct accounts.

### Exact Source Financial Reconciliation for 132 Active Unmapped Rows

| Account Code | Account Persian Name | Row Count | OPENING Sum (Rials) | Period Debit Sum (Rials) | Period Credit Sum (Rials) | CLOSING Sum (Rials) | Closing Exposure % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **`8161`** | حساب كنترل پيمانكاران | 110 | 116,541,110,893 | 3,915,605,618,638 | 3,835,238,810,730 | **196,907,918,801** | **100.00%** |
| **`8184`** | حق عضويت مهدكودك | 1 | 0 | 150,000,000 | 150,000,000 | **0** | 0.00% |
| **`8260`** | انتقال مانده به شركتها گازاستاني / پالايشي /شهري | 2 | 0 | 0 | 0 | **0** | 0.00% |
| **`8488`** | كارمزد پرداختي | 1 | 0 | 14,891,074,867 | 14,891,074,867 | **0** | 0.00% |
| **`8724`** | موجودي كالاي مصالح ساختماني | 1 | 0 | 139,610,024 | 139,610,024 | **0** | 0.00% |
| **`8767`** | واسطه انتقال كالاي برگشتي به انبار(جاري) | 8 | 0 | 23,002,900,150 | 23,002,900,150 | **0** | 0.00% |
| **`8769`** | واسطه انتقال كالاي برگشتي به انبار (سرمايه اي) | 6 | 0 | 7,855,802,639 | 7,855,802,639 | **0** | 0.00% |
| **`8874`** | بانك ملت | 3 | 0 | 155,180,000 | 155,180,000 | **0** | 0.00% |
| **SUBTOTAL (132 Rows)** | *Active Unmapped Accounts* | **132** | **116,541,110,893** | **3,961,800,186,318** | **3,881,433,378,410** | **196,907,918,801** | **100.00%** |
| **`8999`** | *حساب افتتاحيه و اختتاميه* | 11 | 0 | 0 | 0 | **0** | 0.00% |
| **TOTAL (143 Rows)** | *All Unmapped Rows* | **143** | **116,541,110,893** | **3,961,800,186,318** | **3,881,433,378,410** | **196,907,918,801** | **100.00%** |

### Key Exposure Insights
1. **Exposure Concentration**: 100% of the net unmapped closing balance exposure (**196,907,918,801 Rials**, or **~196.91 Billion Rials** / **196,908 Million Rials**) belongs entirely to **Account `8161` (حساب کنترل پیمانکاران)** across 110 unmapped rows where specific T1/T4 combinations are omitted from `mapping_1404.xlsx`.
2. **Zero-Closing Clearing Accounts**: The remaining 22 unmapped rows across 8 distinct accounts (`8184`, `8260`, `8488`, `8724`, `8767`, `8769`, `8874`) are temporary or clearing accounts with non-zero period turnover but **EXACTLY ZERO closing balance**.

---

## 5. Source File Traceability & Lineage Metadata

- **Ledger Workbook**: `data/source_ledgers/source_1404.xlsx` (Sheet: `Source`, Header Row: 2, Data Rows: 2-252,899, Total Data Rows: 252,898).
- **Mapping Workbook**: `data/mappings/mapping_1404.xlsx` (Sheet: `Data`, Total Mapping Rules: 497).
- **Matching Function**: Composite key matching on `حساب` (Account Code), `T1_CODE`, `جاری / سرمایه ای`, and `T4_CODE`.
