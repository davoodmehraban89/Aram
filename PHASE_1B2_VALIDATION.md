# PHASE 1B-2 VALIDATION REPORT

## Executive Summary
This document serves as the final, authoritative validation report for **Phase 1B-2** (Cell-by-Cell Statement Extraction, Dimensional Mapping Coverage Standardization, and Lineage Exposure Reconciliation).

Phase 1B-2 has completed all required audit corrections directly on the accepted `source-data-cleanup` baseline. Phase 2 has **NOT** been started.

---

## 1. Core Validation Deliverables & Metrics

### A. Cell-by-Cell Primary Statement Extraction (`NOTE_TO_STATEMENT_MATRIX.md`)
- **Statements Extracted**: All four primary financial statements (`سودوزيان`, `وضعيت مالي`, `حقوق مالكانه`, `جريان هاي نقدي`) across fiscal years **1402**, **1403**, and **1404**.
- **Source Verification**: Every line item caption, note reference, current period amount, and comparative period amount is mapped directly to its exact Excel cell coordinate (`Sheet!ColRow`).
- **Scratchpad Anomaly Isolation**: Working/scratchpad columns (e.g. Column K in cash flow workbooks containing unformatted raw Rial numbers like `109388328483`, `-33462657272375`, `41299837917`, `-301280000000`, `1594875501283`) are isolated and excluded from statement values. No cell concatenation or column-shift errors are accepted as verified statement values.
- **Verification Gate**: Only statement items whose exact source cells are verified are marked **`MATCH`**; anomalous or unresolved source cells remain **`UNVERIFIED`**.

### B. Standardized Mapping Coverage Metrics (`MAPPING_ANALYSIS.md`)
The canonical source ledger contains **252,898 total rows**. Account `8999` contributes 11 domain-confirmed system closing rows that are retained in source but excluded from mapping scope, leaving **252,887 mapping-eligible rows**.

| Standardized Coverage Metric | Row Count | Percentage of Mapping-Eligible Rows | Definition |
| --- | --- | --- | --- |
| **`UNIQUE_DETERMINISTIC_COVERAGE`** | **214,848** | **84.96%** (84.9581%) | Mapping-eligible rows matching exactly one unique mapping rule. |
| **`AMBIGUOUS/MULTI_MATCH_RATE`** | **37,907** | **14.99%** (14.9897%) | Mapping-eligible rows matching multiple mapping rules due to overlapping dimensional rules or missing sub-filters. *Not called proven lineage.* |
| **`UNMAPPED_RATE`** | **132** | **0.05%** (0.0522%) | Mapping-eligible rows matching zero mapping rules in `mapping_1404.xlsx`. |
| **`ANY_MATCH_COVERAGE`** | **252,755** | **99.95%** (99.9478%) | Mapping-eligible rows with at least one matching rule (`UNIQUE` + `AMBIGUOUS`). |
| **TOTAL MAPPING-ELIGIBLE ROWS** | **252,887** | **100.00%** | Source rows used as the mapping coverage denominator. |

### C. Reconciled Exposure Analysis
1. **Account 8999 System Closing Account — Excluded From Mapping Scope**:
   - 11 rows remain unchanged in `source_1404.xlsx` for audit traceability.
   - Domain-confirmed system opening/closing account.
   - Not intended to map to a financial statement note and therefore not counted as a true unmapped-account exception.
   - Excluded from mapping coverage denominators and unmapped-exposure metrics.

2. **132 True Mapping-Eligible Unmapped Rows Exposure**:
   - **OPENING Sum**: 116,541,110,893 Rials.
   - **Debit Sum**: 3,961,800,186,318 Rials.
   - **Credit Sum**: 3,881,433,378,410 Rials.
   - **CLOSING Sum**: **196,907,918,801 Rials** (~196.91 Billion Rials / 196,908 Million Rials).
   - **100% Exposure Concentration**: Account `8161` (حساب کنترل پیمانکاران) accounts for 110 rows and **100%** of the closing balance exposure (196,907,918,801 Rials).
   - **Seven Zero-Closing Clearing Accounts**: 22 rows across 7 distinct zero-closing accounts (`8184`, `8260`, `8488`, `8724`, `8767`, `8769`, `8874`) have **EXACTLY ZERO closing balance**.

---

## 2. Updated Phase 1B-2 Markdown File Inventory

The following approved Phase 1B-2 Markdown files have been updated for consistency:
1. `NOTE_TO_STATEMENT_MATRIX.md` (Cell-by-cell statement-to-note extraction matrix)
2. `MAPPING_ANALYSIS.md` (Standardized mapping coverage & exposure analysis)
3. `SOURCE_LINEAGE_ANALYSIS.md` (Multi-tier lineage architecture & traceability)
4. `NOTE_CATALOG.md` (Catalog of financial statement notes across 1402-1404)
5. `NOTE_TO_SHEET_MATRIX.md` (Logical note to physical sheet mapping matrix)
6. `HISTORICAL_DISCREPANCIES.md` (Historical restatements, structural shifts & anomalies)
7. `PHASE_1B2_VALIDATION.md` (This summary validation report)

---

## 3. Strict Boundary Compliance
- **Protected Files Untouched**: `SOURCE_INVENTORY.md`, `WORKBOOK_SHEET_CATALOG.md`, `PHASE_1B1_VALIDATION.md`, XLSX/PDF files, and production code were **NOT** modified.
- **No Temporary Artifacts**: All temporary analysis scripts created during validation have been completely removed.
- **Phase 2 Gate**: Phase 2 has **NOT** been started. The codebase remains cleanly at the Phase 1B-2 baseline ready for independent review.
