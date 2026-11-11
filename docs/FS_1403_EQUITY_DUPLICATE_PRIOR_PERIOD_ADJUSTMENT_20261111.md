# FS-1403-EQ-01 — Repeated Prior-Period Equity Adjustment and Ambiguous Note Reference

**Status:** TECHNICAL ROOT-CAUSE IDENTIFIED — ACCOUNTING OWNER CONFIRMATION REQUIRED  
**Prepared:** 2026-11-11  
**Affected source:** `data/official_statements/financial_1402.xlsx`, `financial_1403.xlsx`  
**Related issue:** FS-1403-EQ-01  
**No source workbook was modified.**

## 1. Executive finding

The 43,241,509 million Rial difference is no longer an unexplained arithmetic discrepancy. A direct comparison of the 1402 and 1403 official equity statements shows that the 1403 comparative rollforward appears to repeat a prior-period adjustment that was already incorporated in the 1402 financial statements.

The amount is exactly composed of two adjustments already recorded in the 1402 equity statement:

- 33,467,967 million Rials: correction at the opening of 1401.
- 9,773,542 million Rials: correction to the 1401 reported loss.
- Total: 43,241,509 million Rials.

The 1403 report's Note 23-1 splits the same amount into the same two components. The 1403 equity statement then adds the full 43,241,509 again to its 1402/01/01 opening balance, but its reported 1402 closing balance does not carry that additional amount. This is consistent with a duplicated comparative adjustment line, not evidence that the 1402 closing equity should be restated a second time.

## 2. Exact workbook evidence

### 2.1 Financial_1402.xlsx — equity statement

Worksheet: `حقوق مالكانه` (fourth worksheet).

| Row | Description | Total equity (million Rials) |
|---:|---|---:|
| 7 | Opening 1401/01/01 | +6,748,715 |
| 8 | Prior-period correction | -33,467,967 |
| 9 | Restated opening 1401/01/01 | -26,719,252 |
| 11 | Reported 1401 net loss | -816,927 |
| 12 | Correction to 1401 loss | -9,773,542 |
| 13 | Restated 1401 net loss | -10,590,469 |
| 14 | Closing 1401/12/29 | -37,309,721 |
| 16 | 1402 net loss | -15,709,645 |
| 17 | Capital-in-progress increase | +14,069,826 |
| 18 | Closing 1402/12/29 | -38,949,540 |

The 1402 report therefore already incorporates both components of the 43,241,509 million Rial adjustment before reaching its 1402 closing balance.

### 2.2 Financial_1403.xlsx — comparative equity statement

Worksheet: `حقوق مالكانه` (fourth worksheet).

| Row | Description | Total equity (million Rials) |
|---:|---|---:|
| 7 | Opening 1402/01/01 | -37,309,721 |
| 8 | Correction (Note 23) | -43,241,509 |
| 9 | Restated opening 1402/01/01 | -80,551,230 |
| 11 | 1402 reported net loss | -15,709,645 |
| 13 | Capital-in-progress increase | +14,069,826 |
| 14 | Reported closing 1402/12/29 | -38,949,540 |
| 16 | 1403 net loss | -9,454,392 |
| 19 | Closing 1403/12/30 | -48,403,932 |

The reported 1402 closing is reproduced exactly from the row-7 opening, without applying row 8 a second time:

`-37,309,721 - 15,709,645 + 14,069,826 = -38,949,540`

If row 8 were a new incremental adjustment, the 1402 closing would instead be `-82,191,049`, which is not the published 1402 closing and is not the closing shown in the 1403 comparative column. Therefore do **not** recommend changing the closing balance to -82,191,049 on the basis of this arithmetic alone.

### 2.3 Note 23-1 — same adjustment components

In `financial_1403.xlsx`, worksheet `29`:

- Row 27 labels Note 23 as `اصلاح اشتباهات و تجدید طبقه بندی`.
- Row 29 records 9,773,542 million Rials in the 1402 comparative column for the 1401 pension-reserve adjustment.
- Row 30 records 33,467,967 million Rials in the 1402 comparative column for the pre-1401 pension-reserve adjustment.
- Row 31 totals 43,241,509 million Rials.
- Row 33 explains the amount as actuarially calculated pension obligations related to personnel of group companies, charged against payables.

This is the same amount and same split as the 1402 equity statement's prior-period corrections.

## 3. Additional disclosure defect — duplicate Note 23 numbering

The 1403 workbook contains two separate top-level sections numbered Note 23:

1. Worksheet `29`, row 27: `23- اصلاح اشتباهات و تجدید طبقه بندی`.
2. Worksheet `30`, row 5: `23- معاملات غیرنقدی`.

The equity statement's generic reference `یادداشت توضیحی 23` is therefore ambiguous. If the correction disclosure is intended, the reference should be specific to the relevant sub-note (for example 23-1), subject to the approved note catalogue and pagination. The duplicate top-level note numbering itself must be resolved in the final disclosure index.

## 4. Most likely explanation

The evidence strongly suggests the 1403 comparative equity rollforward copied the 1402 opening balance and then re-applied the same 43,241,509 million Rial adjustment that was already reflected in the 1402 financial statements. The 1403 row-14 closing and row-19 closing continue to use the already-adjusted 1402 closing balance.

This is a presentation / comparative rollforward duplication, not proof that the balance sheet closing equity is wrong by 43,241,509 million Rials.

## 5. Proposed accounting-owner disposition

**Recommended proposal for owner review:**

1. Confirm from the approved 1402 closing trial balance and the actuarial journal entries that the 33,467,967 and 9,773,542 amounts were already posted and incorporated into the 1402 opening / 1401 restated loss and the 1402 closing equity.
2. If confirmed, remove or correct the duplicate 43,241,509 adjustment row in the 1403 comparative 1402 rollforward; the comparative opening should reconcile to the 1402 approved closing of -37,309,721 at 1402/01/01, and the 1402 closing should remain -38,949,540.
3. Preserve the 1403 closing equity of -48,403,932 only if it continues to reconcile to the approved 1403 trial balance and balance sheet.
4. Correct the generic Note 23 reference to the exact approved sub-note and resolve duplicate top-level Note 23 numbering.
5. Retain the actuarial calculation, journal vouchers, approved trial-balance extracts and comparative restatement approval as evidence.

**Do not apply this proposal until the accounting owner confirms the original journal entries and the approved 1402 opening / closing balances.** If the journal evidence shows the adjustment was not actually included in 1402 closing, this conclusion must be revisited and the balance-sheet accounts reconciled before any correction.

## 6. Source integrity

| File | Bytes | SHA-256 |
|---|---:|---|
| financial_1402.xlsx | 1,014,773 | `DF40940EBA3D286F82DF364BC84E14CD6796AB3E1F8C4FFF658408182282F4EF` |
| financial_1403.xlsx | 990,782 | `AEB279A3A01058B6998B998A2A44CF68B48A1081F477B87E271CEB2984D23ABE` |

These hashes were computed after read-only inspection. Neither workbook was saved or modified.

## 7. Acceptance checklist

- [ ] Accounting owner confirms the two prior-period journal entries and their posting dates.
- [ ] Approved 1402 opening and closing trial-balance extracts are attached.
- [ ] Approved 1403 comparative rollforward treatment is recorded.
- [ ] The 1403 equity statement is corrected only in a derived candidate workbook.
- [ ] The 1403 statement of financial position still balances and equity ties to the ledger.
- [ ] Duplicate Note 23 numbering is resolved in the note catalogue and cross-reference matrix.
- [ ] The final note reference is specific and agrees to the printed note index.
- [ ] Independent reviewer signs off on the comparative rollforward and source hashes.

**Current decision:** root cause strongly indicated; accounting-owner confirmation pending; no official financial statement workbook changed.
