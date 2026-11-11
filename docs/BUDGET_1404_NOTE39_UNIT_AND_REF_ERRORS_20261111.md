# Budget 1404 Note 39 — Unit-scale and broken-reference validation

**Status:** TECHNICAL FINDING CONFIRMED — BUDGET OWNER SOURCE REQUIRED  
**Prepared:** 2026-11-11  
**Affected workbook:** `data/official_statements/financial_1404.xlsx`  
**Related items:** BUDGET-1403/1404-N36-37-APPROVED-01; BUDGET-1404-N39-UNIT-01  
**No official workbook was modified.**

## 1. Executive conclusion

Direct read-only inspection of the 1403 and 1404 workbooks confirms:

1. The original-approved-budget cells in the identified #REF! locations are stored as Excel error values (`data_type = e`), not recoverable formulas. The workbook itself does not contain the missing formula expression.
2. In 1404 Note 39 (physical sheet 39), original-budget column E is inconsistent in unit scale across the capital-investment block:
   - E22:E32 contain Rial-scale values.
   - F22:F32 (revised budget) and G22:G32 (actual) are in million Rials, consistent with the printed heading.
   - For every non-zero row 22–32, E equals F multiplied by exactly 1,000,000.
3. E35 is 12,500,000 in both 1403 and 1404 and is not multiplied by 1,000,000. This supports treating E35 as already in million-Rial scale, unlike E22:E32.
4. The 1403 Note 39 values in E22:E32 are in million-Rial scale and match the revised-budget column. The 1404 unit inconsistency is therefore year-specific, not a general workbook convention.

Because the original approved-budget source file is not present in the inspected project data directory, the correct original budget cannot be independently reconstructed. Do not divide or rewrite source cells without the approved budget source and budget-owner confirmation.

## 2. Exact #REF! cell evidence

| Workbook | Physical sheet | Cell | data_only value | Formula-mode value | Cell type |
|---|---|---|---|---|---|
| financial_1403.xlsx | 36-37 | G120 | #REF! | #REF! | `e` |
| financial_1403.xlsx | 36-37 | G123 | #REF! | #REF! | `e` |
| financial_1404.xlsx | 36-37 | G127 | #REF! | #REF! | `e` |
| financial_1404.xlsx | 36-37 | G130 | #REF! | #REF! | `e` |
| financial_1404.xlsx | 39 | E9 | #REF! | #REF! | `e` |
| financial_1404.xlsx | 39 | E16 | #REF! | #REF! | `e` |

The same `#REF!` is returned in both data-only and formula-mode loads, with cell type `e`. These are stored error cells, not intact formulas that can be repaired by refreshing calculation. Rebuilding them requires the original approved-budget source or approved calculation schedule.

## 3. 1404 Note 39 — unit-scale test

Printed heading: `(مبالغ به میلیون ریال)`.

| Cell | Original approved budget E (as stored) | Revised budget F | E / F |
|---|---:|---:|---:|
| E22 / F22 — ساختمان | 7,771,200,000,000 | 7,771,200 | 1,000,000 |
| E23 / F23 — تأسیسات | 64,312,400,000,000 | 64,312,400 | 1,000,000 |
| E24 / F24 — ماشین‌آلات | 4,170,000,000,000 | 4,170,000 | 1,000,000 |
| E25 / F25 — لوازم و ابزار فنی | 1,000,000,000,000 | 1,000,000 | 1,000,000 |
| E26 / F26 — وسایط نقلیه | 6,300,000,000,000 | 6,300,000 | 1,000,000 |
| E27 / F27 — اثاثیه و لوازم اداری | 8,566,400,000,000 | 8,566,400 | 1,000,000 |
| E28 / F28 — سایر مؤسسات | 0 | 0 | n/a |
| E29 / F29 — تحقیقات و پژوهش | 330,000,000,000 | 330,000 | 1,000,000 |
| E30 / F30 — حفظ محیط زیست | 3,550,000,000,000 | 3,550,000 | 1,000,000 |
| E31 / F31 — سایر | 1,000,000,000,000 | 1,000,000 | 1,000,000 |
| E32 / F32 — جمع هزینه‌های سرمایه‌ای | 97,000,000,000,000 | 97,000,000 | 1,000,000 |

The arithmetic proves the unit-scale difference relative to the revised-budget column. It does **not** prove that the original-approved budget amount equals the revised budget amount; that requires the approved original budget source.

### 3.1 E35 exception

- 1403 Note 39 E35 = 12,500,000; F35 = 0.
- 1404 Note 39 E35 = 12,500,000; F35 = 0.
- The printed unit is million Rials in both workbooks.
- E35 is not part of the 1,000,000 scale anomaly observed in E22:E32. Keep it separate; do not divide it by 1,000,000.

### 3.2 Total impact if a unit correction is later approved

The stored E37 total is 97,000,012,500,000, while the revised-budget F37 total is 117,000,000. A purely mechanical conversion of E22:E32 by 1,000,000, retaining E35 as displayed, would produce 97,012,500 million Rials for the original-approved uses. This is an analytical scenario only, not an approved correction and not a substitute for the missing original budget source.

## 4. 1403 comparator

The 1403 Note 39 table (physical sheet 39) shows original budget E22:E32 and revised budget F22:F32 in the same million-Rial scale. Examples:
- E22 = F22 = 18,785,300.
- E23 = F23 = 31,864,100.
- E32 = F32 = 55,633,600.
- E35 = 12,500,000 in both 1403 and 1404.

This confirms that the 1404 E22:E32 scale is an exception relative to the prior-year presentation.

## 5. Source integrity

| File | Bytes | SHA-256 |
|---|---:|---|
| financial_1404.xlsx | 930,495 | `F764E3B6A2B6135997248BFAD0B5A60EDC9BE9ED3DFEF8631096C50713552BD3` |

The workbook was inspected in read-only mode; the hash was computed after inspection. No cells were edited or saved.

## 6. Required owner evidence and acceptance

1. Obtain the approved original 1404 budget workbook / signed schedule and its unit convention.
2. Confirm whether E22:E32 were stored in Rials while the printed note says million Rials, or whether the source values are intentionally different.
3. Reconcile original-approved budget values for rows 22–32 and E35 against the approved source, not against the revised budget.
4. Restore the missing original-approved-budget values for E9/E16 and the four Note 36–37 cells only from an authoritative source or approved calculation schedule.
5. Confirm Note 39 original budget resources and uses totals after correction.
6. Prepare a separate derived workbook, compare every corrected cell to source evidence, and obtain budget-owner approval plus independent review.
7. Keep actual and revised-budget values unchanged; preserve the original file hash.

**Current decision:** unit-scale and error-cell defects are confirmed; exact original-budget values and formula lineage are NOT_VERIFIED. No source correction is authorized.
