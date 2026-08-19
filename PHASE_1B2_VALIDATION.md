# PHASE 1B-2 VALIDATION REPORT

## Executive Summary
This document serves as the final, authoritative validation report for **Phase 1B-2** (Cell-by-Cell Statement Extraction, Dimensional Mapping Coverage Standardization, and Lineage Exposure Reconciliation).

Phase 1B-2 has completed all required audit corrections directly on the accepted `source-data-cleanup` baseline. Phase 2 has **NOT** been started.

---

## 1. Core Validation Deliverables & Metrics

### A. Cell-by-Cell Primary Statement Extraction (`NOTE_TO_STATEMENT_MATRIX.md`)
- **Statements Extracted**: All four primary financial statements (`سودوزيان`, `وضعيت مالي`, `حقوق مالكانه`, `جريان هاي نقدي`) across fiscal years **1402**, **1403**, and **1404**.
- **Source Verification**: Every line item caption, note reference, current period amount, and comparative period amount is mapped directly to its exact Excel cell coordinate (`Sheet!ColRow`).
- **Scratchpad Anomaly Isolation**: Working/scratchpad columns (e.g. Column K in cash flow workbooks containing unformatted raw Rial numbers like `109388328483`, `-33462657272375`, `41299837917`, `-301280000000`, `1594875501283`) are isolated and excluded from statement values. No cell concatenation or column-shift errors exist.
- **Verification Gate**: 100% of verified statement items are marked **`MATCH`**.

### B. Standardized Mapping Coverage Metrics (`MAPPING_ANALYSIS.md`)
Across **252,898 total general ledger data rows** in `data/source_ledgers/source_1404.xlsx`:

| Standardized Coverage Metric | Row Count | Percentage | Definition |
| --- | --- | --- | --- |
| **`UNIQUE_DETERMINISTIC_COVERAGE`** | **214,848** | **84.95%** (84.9544%) | Rows matching exactly one unique mapping rule. |
| **`AMBIGUOUS/MULTI_MATCH_RATE`** | **37,907** | **14.99%** (14.9890%) | Rows matching multiple mapping rules due to overlapping dimensional rules or missing sub-filters. *Not called proven lineage.* |
| **`UNMAPPED_RATE`** | **143** | **0.06%** (0.0565%) | Rows matching zero mapping rules in `mapping_1404.xlsx`. |
| **`ANY_MATCH_COVERAGE`** | **252,755** | **99.94%** (99.9435%) | Total rows with at least one matching rule (`UNIQUE` + `AMBIGUOUS`). |

### C. Reconciled Exposure Analysis
1. **Account 8999 High-Gross / Zero-Net Exception**:
   - 11 rows in `source_1404.xlsx`.
   - Gross CLOSING Debit/Credit = `±1,310,883,439,013,116` Rials.
   - Net CLOSING Balance = **`0.0` Rials** (EXACT ZERO). Verified zero financial statement impact.

2. **132 Active Unmapped Rows Exposure**:
   - **OPENING Sum**: 116,541,110,893 Rials.
   - **Debit Sum**: 3,961,800,186,318 Rials.
   - **Credit Sum**: 3,881,433,378,410 Rials.
   - **CLOSING Sum**: **196,907,918,801 Rials** (~196.91 Billion Rials / 196,908 Million Rials).
   - **100% Exposure Concentration**: Account `8161` (حساب کنترل پیمانکاران) accounts for 110 rows and **100%** of the closing balance exposure (196,907,918,801 Rials).
   - **Zero-Closing Clearing Accounts**: 22 rows across 7 distinct zero-closing accounts (`8184`, `8260`, `8488`, `8724`, `8767`, `8769`, `8874`) have **EXACTLY ZERO closing balance**.

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
