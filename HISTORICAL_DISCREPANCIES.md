# Historical Discrepancies

## Overview
This document evaluates structural differences, stated balances, and reconciliations across the historical sources (1402, 1403, 1404).

## 1. As-Filed vs Comparative / Restated Data
Based on direct inspection of the primary statements (details in NOTE_TO_STATEMENT_MATRIX.md), figures presented as current-year in older reports are systematically presented as comparative figures in subsequent years.

## 2. Hypothesis Validations (Direct Source Extraction)

### A. 1404 Payable
The official current-year amount for Payables (پرداختنی‌هاي تجاري و ساير پرداختني‌ها) in 1404 `وضعيت مالي` row 25 is **145,241,976**.
The comparative figure (prior amount) for 1403 presented in the same 1404 sheet is **83,215,373**.
Conclusion: The application amounts (145,341,976 and 83,315,373) deviate from the canonical source by exactly 100,000. **The official source values are 145,241,976 and 83,215,373.**

### B. 1403 Other Non-Operating Income/Expense
In the 1403 `سودوزيان` statement:
- "ساير درآمدها و هزينه‌هاي غيرعملياتي" is listed as **627,800**.
There is no direct evidence in the primary statement combining this with 1,085,594 to yield 1,713,394. The canonical amount is 627,800.

### C. 1403 Net Loss
In the 1403 `سودوزيان` statement, the "زيان خالص" (Net Loss) is officially stated as **-9,454,392**.
The application's value of -8,368,798 is a deviation from the audited source. The Statement of Changes in Equity ("حقوق مالكانه") confirms the net loss applied to retained earnings is -9,454,392.

### D. 1404 Equity Statement
The `حقوق مالكانه` (Statement of Changes in Equity) in 1404 exhibits specific structural classifications. It contains columns for Capital, Reserves, and Retained Earnings. A prior-period correction (تعديلات سنواتي) and capital registration transfers are present and explicitly stated. No "omitted" equity columns were identified in the structural layout of the source workbook.

### E. Historical Dataset Mixing
There is strong evidence that the application mixes `AS_FILED` data with `COMPARATIVE_PRESENTED_IN_LATER_REPORT` data without explicitly distinguishing them. The canonical rule is that original sources are immutable. If a figure from 1402 is updated in the 1403 comparative column, both must be preserved under different flags.

### F. Auditor-Report Content
Detailed text comparison is deferred, but structurally, the application must not paraphrase or rewrite the auditor's opinion. The canonical PDFs (auditor_1402.pdf, auditor_1403.pdf, auditor_1404.pdf) are the sole source of truth for the opinion text.

## 3. Financial Statement Reconciliation Checks
- **A = L + E**: Reconciles natively within the canonical Excel workbooks (e.g., Total Assets matches Total Liabilities + Equity in 1404 `وضعيت مالي`).
- **P/L to Equity**: Net profit/loss in `سودوزيان` matches the net profit/loss entry in `حقوق مالكانه`.
- **Cash Flow to Balance Sheet**: Ending cash in `جريان هاي نقدي` matches "موجودي نقد" in `وضعيت مالي`.
