# Year-Aware Note-to-Sheet Matrix — 1402–1404

**Status:** Reconstructed from canonical workbook section headings. This supersedes the previous one-to-one sheet-name matrix.

## Rules

- The first column is the logical note number for that fiscal year; the sheet column contains the actual physical worksheet tab name(s).
- A single physical sheet can contain multiple notes. A single note can span multiple sheets.
- Logical note numbers differ across years. In particular, Note 17 is capital-in-progress in 1402 but legal reserve in 1403/1404.
- Do not infer a logical note number from the physical sheet name.
- In 1403/1404, several Statement of Financial Position references (17–22) are stale by one relative to note-page headings. See the cross-reference exception below.
- In 1403 only, top-level Note 23 is duplicated across two physical sheets: corrections/reclassifications on sheet 29 and non-cash transactions on sheet 30. Keep section identity and subnote number separate; do not collapse these into one logical note.

## 1. Fiscal year 1402

| Logical note | Physical sheet(s) | Content |
|---:|---|---|
| 5 | 10, 11 | Operating revenue |
| 6 | 12 | Cost of revenue |
| 7–9 | 13 | SG&A; other income; non-operating income/expenses |
| 10 | 14–18 | Tangible fixed assets and subnotes |
| 11 | 19 | Intangible assets |
| 12 | 20, 21 | Trade and other receivables |
| 13–14 | 22 | Prepayments; inventories |
| 15–18 | 23 | Cash; capital; capital in progress; legal reserve |
| 19 | 24–27 | Trade and other payables |
| 20 | 27, 28 | Employee benefits / future staff obligations |
| 21 | 28, 29 | Tax payable / dividends payable |
| 22–24 | 29 | Advances received; corrections/reclassifications; cash from operations |
| 25 | 30 | Non-cash transactions |
| 26 | 30–32 | Financial risk management |
| 27 | 32 | Foreign-currency position |
| 28 | 33, 34 | Related-party transactions and balances |
| 29–30 | 35 | Commitments/contingencies; subsequent events |
| 36 | 36 | Budget performance — revenues |
| 37 | 37 | Budget performance — expenses |
| 38 | 38 | Budget justification |
| 39 | Absent | Not present in 1402 |

## 2. Fiscal year 1403

| Logical note | Physical sheet(s) | Content |
|---:|---|---|
| 5 | 10, 11 | Operating revenue |
| 6 | 12 | Cost of revenue |
| 7–9 | 13 | SG&A; other income; non-operating income/expenses |
| 10 | 14–18 | Tangible fixed assets and subnotes |
| 11 | 19 | Intangible assets |
| 12 | 20, 21 | Trade and other receivables |
| 13–14 | 22 | Prepayments; inventories |
| 15–17 | 23 | Cash; capital; legal reserve |
| 18 | 24–27 | Trade and other payables |
| 19 | 27 | Employee benefits / future staff obligations |
| 20 | 28 | Tax payable |
| 21–22 | 29 | Dividends payable / advances received; cash from operations |
| 23 (section A; subnotes 23-1 to 23-3) | 29 | Corrections / reclassifications |
| 23 (duplicate section B) | 30 | Non-cash transactions |
| 24 | 30–32 | Financial risk management |
| 25 | 32 | Foreign-currency position |
| 26 | 33, 34 | Related-party transactions and balances |
| 27–28 | 35 | Commitments/contingencies; subsequent events |
| 36–37 | 36-37 | Merged budget-performance sheet |
| 38 | 38 | Budget justification |
| 39 | 39 | Summary of sources and uses |

## 3. Fiscal year 1404

| Logical note | Physical sheet(s) | Content |
|---:|---|---|
| 5 | 10, 11 | Operating revenue |
| 6 | 12 | Cost of revenue |
| 7–9 | 13 | SG&A; other income; non-operating income/expenses |
| 10 | 14–18 | Tangible fixed assets and subnotes |
| 11 | 19 | Intangible assets |
| 12 | 20, 21 | Trade and other receivables |
| 13–14 | 22 | Prepayments; inventories |
| 15–17 | 23 | Cash; capital; legal reserve |
| 18 | 24–27 | Trade and other payables |
| 19 | 27 | Employee benefits / future staff obligations |
| 20 | 28 | Tax payable |
| 21 | 29 | Dividends payable / advances received |
| 22 | 29 | Corrections and restatements |
| 23 | 29, 30 | Cash from operations and supporting disclosures |
| 24 | 30 | Non-cash transactions |
| 25 | 30–32 | Financial risk management |
| 26 | 32 | Foreign-currency position |
| 27 | 33, 34 | Related-party transactions and balances |
| 28–29 | 35 | Commitments/contingencies; subsequent events |
| 36–37 | 36-37 | Merged budget-performance sheet |
| 38 | 38 | Budget justification |
| 39 | 39 | Summary of sources and uses |

## 4. 1403/1404 Statement of Financial Position cross-reference drift

The 1403 and 1404 balance sheets retain references that do not match the printed note-page headings:

| Balance-sheet reference | Note-page heading actually found | Physical sheet |
|---|---|---:|
| 17-1 / 17-2 — capital in progress | No matching Note 17-1 / 17-2 heading; capital details appear under Note 16, while printed Note 17 is legal reserve | 23 |
| 18 — legal reserve | 17 — legal reserve | 23 |
| 19-1 / 19-2 — payables | 18 — payables | 24–27 |
| 20 — employee benefits | 19 — employee benefits | 27 |
| 21 — tax payable | 20 — tax payable | 28 |
| 22 — advances received | 21 — advances received | 29 |

The underlying amounts tie to the note-page content; this is a cross-reference / numbering defect. The 1402 workbook retains the earlier sequence (Note 17 capital-in-progress, Note 18 legal reserve, Note 19 payables, etc.) and does not have this same one-number drift.

**Ingestion requirement:** store fiscal_year, statement_reference, logical_note_number, printed_heading, physical_sheet_name, and subnote_number separately. Preserve the source mismatch for review; do not rewrite canonical XLSX/PDF.


## 5. 1403 duplicate Note 23 — explicit exception

The 1403 workbook prints two top-level sections with the same logical note number:
- Physical sheet 29, row 27: Note 23 — corrections and reclassifications; subnotes 23-1, 23-2 and 23-3.
- Physical sheet 30, row 5: Note 23 — non-cash transactions.

The 1403 Statement of Changes in Equity refers generically to Note 23 for its prior-period adjustment. The supporting actuarial disclosure is specifically in Note 23-1-1 on physical sheet 29. A generic Note 23 reference is ambiguous because of the duplicate heading. The catalog and application model must retain section identity, subnote and physical sheet separately until the accounting owner approves the final printed reference.
