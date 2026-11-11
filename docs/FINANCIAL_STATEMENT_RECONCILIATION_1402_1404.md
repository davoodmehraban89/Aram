# Financial Statement Reconciliation — Fiscal Years 1402–1404

**Status:** PRESENT_BUT_UNVERIFIED — independent accounting sign-off remains pending  
**Prepared:** 2026-11-10  
**Repository base:** source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914  
**Scope:** Read-only reconciliation of official primary statements, comparative figures, equity movements, cash flow, and disclosed restatements. No source workbook or PDF was modified.

## 1. Executive result

- 66 arithmetic checks passed across the Income Statement, Statement of Financial Position, and Cash Flow Statement for 1402, 1403, and 1404, including comparative columns.
- 3 additional cross-statement cash checks passed: each year's cash-flow closing balance equals the cash balance in the corresponding Statement of Financial Position.
- The restated 1403 comparative figures presented in the 1404 statements reconcile to Note 22.
- Note-page amount tie-outs now cover the primary Income Statement and Statement of Financial Position lines for all three years (1402–1404), with narrative-only disclosures and year-specific note-reference drift explicitly identified.
- The 1403 equity rollforward's 43,241,509 million Rial opening adjustment is now traced to the same two prior-period actuarial corrections already reflected in the 1402 statements (33,467,967 + 9,773,542). The 1403 comparative rollforward appears to repeat them; accounting-owner confirmation remains required. The 1403 workbook also duplicates top-level Note 23 numbering across corrections (sheet 29) and non-cash transactions (sheet 30).
- The 1404 exchange-rate effect of 12,556 million Rials mathematically reconciles the cash-flow closing balance and is explicitly discussed in Note 9-3, which cites NIGC letter No. 1830 dated 1405/01/16. The prior claim that no note cross-reference existed is withdrawn; a separate rate-calculation schedule was not independently reproduced.
- A one-million-Rial difference exists between 1403 current and 1404 comparative operating and investing cash-flow lines; the differences offset and do not affect net cash movement or closing cash.

These results are a statement-level arithmetic and disclosure cross-check, not an independent audit opinion, signed finance approval, or full transaction-level reconciliation to the General Ledger.

## 2. Owner-confirmed treatment of irrelevant Excel errors and zero-balance accounts

The accounting owner confirmed on 2026-11-10 that certain workbook errors (#REF!, #VALUE!, #DIV/0!) occur in unused growth / auxiliary calculations and accounts that have no effect on the official statements. Those cells are not to block progress when all of the following are true:

1. The cell is outside the authoritative statement presentation columns and is not referenced by an official statement amount or required note.
2. The underlying account has zero net closing balance at the relevant reporting date, or a documented counterpart account offsets it under the accounting control-account arrangement.
3. The item does not affect turnover-based disclosures, cash flow, commitments, related-party disclosures, or another required note.

Preservation rule: Exclude qualifying zero-balance / paired control accounts from statement totals and materiality analysis, but retain every original ledger row and source workbook unchanged for traceability. Do not globally suppress Excel errors, delete source rows, or infer offset pairs from equal amounts alone.

Account 8999 remains a domain-confirmed system opening/closing account excluded from Mapping scope, with its 11 ledger rows preserved. The 22 rows across seven zero-closing clearing accounts remain excluded from closing exposure. Account 8161 has a separately reported non-zero closing exposure in the existing Mapping analysis and is not automatically excluded by the zero-balance rule; any claimed offset must be evidenced by its counterpart and approved accounting classification.

## 3. Source files and integrity baseline

All ten canonical files tracked at the accepted base were present and readable. SHA-256 values below were computed from the isolated worktree based on the accepted branch; no source bytes were changed.

| Source | Bytes | SHA-256 |
|---|---:|---|
| data/official_statements/financial_1402.xlsx | 1,014,773 | DF40940EBA3D286F82DF364BC84E14CD6796AB3E1F8C4FFF658408182282F4EF |
| data/official_statements/financial_1403.xlsx | 990,782 | AEB279A3A01058B6998B998A2A44CF68B48A1081F477B87E271CEB2984D23ABE |
| data/official_statements/financial_1404.xlsx | 930,495 | F764E3B6A2B6135997248BFAD0B5A60EDC9BE9ED3DFEF8631096C50713552BD3 |
| data/source_ledgers/source_1403.xlsx | 23,928,541 | 747FAE7B8DE9866DFBB45CE3A983584A8AC832DEF59F2C65874302F0F87CBB22 |
| data/source_ledgers/source_1404.xlsx | 32,062,394 | 5B4790DCE6E9EA169D61C68751BC6FD5DC390012BC14473B0298BA5AAC30D044 |
| data/mappings/mapping_1404.xlsx | 2,574,677 | 8B3F94389E61B76775E00B8BEC8B9E241F7CCE5097505C61199574855ADAE574 |
| data/auditor_reports/auditor_1402.pdf | 9,051,280 | ECA2DDD234433245CA681E32F55D92003F899CA329E7235D2D5DF3966163F3E2 |
| data/auditor_reports/auditor_1403.pdf | 4,483,471 | 1C67CA03FA3ADDB834E7764F6DE0C7E7D7853C47603F08670932148E16645D69 |
| data/auditor_reports/auditor_1404.pdf | 1,694,985 | B6AD99D5EFACC403C4837A52326F32AF62EE02DC9621CE7443389139BCC617CF |
| data/templates/audit_organization_sample.pdf | 2,596,884 | 3C609E574883B252248D839BD1340EC9232A49D008A58C48A4D13143D19129AA |

## 4. Arithmetic validation

Authoritative presentation columns were used: Income Statement and Statement of Financial Position current/comparative columns F/H; Cash Flow current/comparative columns E/G. Scratchpad columns to the right of the official presentation were excluded.

| Statement | Checks | Result |
|---|---:|---|
| Income Statement: gross result, operating result, pre-tax result, net result × current/comparative × 3 years | 24 | 24 PASS |
| Statement of Financial Position: total assets and total equity/liabilities × current/comparative × 3 years | 12 | 12 PASS |
| Cash Flow: operating, investing, pre-financing, net change, closing cash × current/comparative × 3 years | 30 | 30 PASS |
| Closing cash: Cash Flow vs Statement of Financial Position × 3 years | 3 | 3 PASS |
| Total | 69 | 69 PASS |

### Key closing balances (million Rials)

| Fiscal year | Total assets | Total liabilities | Total equity | Cash at year-end |
|---|---:|---:|---:|---:|
| 1402 | 275,669,532 | 314,619,072 | -38,949,540 | 2,134,188 |
| 1403 (as originally reported) | 369,190,077 | 417,594,009 | -48,403,932 | 3,368,287 |
| 1404 | 733,743,718 | 917,629,178 | -183,885,460 | 19,951,136 |

For each year, total assets equal total liabilities plus equity. Cash-flow closing cash equals the corresponding balance-sheet cash amount.

## 5. Restatement reconciliation

### 5.1 1403 comparative Income Statement in the 1404 workbook

Note 22 explains a 1403 prior-period correction of 18,907,037 million Rials to depreciation / cost of sales:

- Cost of sales: 157,476,581 + 18,907,037 = 176,383,618.
- Net loss: -9,454,392 - 18,907,037 = -28,361,429.

These are the 1403 comparative figures presented in the 1404 Income Statement. The change is disclosed; it is not a simple data-entry mismatch.

### 5.2 1403 comparative Statement of Financial Position in the 1404 workbook

The 1404 Note 22 restatement table reconciles the 1403 comparative figures:

- Tangible fixed assets: 328,178,321 + 174,759,885 = 502,938,206.
- Intangible assets: 192,282 + 23,955 = 216,237.
- Trade and other payables: -235,828,055 - 230,896,470 = -466,724,525 (liability presentation).
- Accumulated losses: 68,405,546 + 56,112,630 = 124,518,176 (loss magnitude; equity presentation is negative).

The restated asset increase (174,783,840) equals the combined liability increase and equity reduction (230,896,470 - 56,112,630).

### 5.3 1402 comparative balance-sheet restatement disclosed in 1404 Note 22

- Tangible fixed assets: 235,873,638 + 193,666,922 = 429,540,560.
- Intangible assets: 190,321 + 23,955 = 214,276.
- Trade and other payables: -188,478,601 - 230,896,470 = -419,375,071.
- Accumulated losses: 73,020,979 + 37,205,593 = 110,226,572 (loss magnitude).

The restated asset increase (193,690,877) equals the liability increase less the equity reduction (230,896,470 - 37,205,593).

### 5.4 1404 equity rollforward

The 1404 Statement of Changes in Equity reconciles after restatement:

- Opening 1403 equity: -38,949,540.
- Prior-period correction: -37,205,593.
- Restated opening equity: -76,155,133.
- Restated 1403 net loss: -28,361,429.
- Net capital reclassification: 0.
- Restated 1403 closing equity: -104,516,562.
- 1404 net loss: -79,368,898.
- 1404 closing equity: -183,885,460.

## 6. Exceptions requiring explicit disposition

### FS-1403-EQ-01 — Opening equity restatement appears duplicated

In financial_1403.xlsx, sheet حقوق مالكانه:

- Row 7 already carries opening equity of -37,309,721, identical to the 1402 closing equity in financial_1402.xlsx.
- The 1403 workbook then shows a further correction of -43,241,509 million Rials in row 8 and restated opening equity of -80,551,230 in row 9.
- However, row 14 closing equity is -38,949,540, which reconciles to row 7 plus the 1402 net loss and capital-in-progress movement, without carrying the row-8 correction.
- The 1402 workbook's equity statement already includes the 43,241,509 prior-period employee-retirement-obligation correction in its 1401 restated balances. The 1403 Note 23 table also identifies the 43,241,509 as a 1402 comparative/prior-period correction (9,773,542 + 33,467,967).

Reperformance of the 1402 movement inside the 1403 equity statement makes the inconsistency explicit:

- If the displayed restated opening balance of -80,551,230 is used, then adding 1402 net loss of -15,709,645 and capital-in-progress increase of +14,069,826 produces an expected closing balance of -82,191,049.
- The reported closing balance is -38,949,540, a difference of exactly 43,241,509.
- The reported closing balance is instead reproduced by using the pre-adjustment opening balance: -37,309,721 - 15,709,645 + 14,069,826 = -38,949,540.
- Therefore, the 43,241,509 opening adjustment is displayed in the rollforward but not carried through the 1402 closing row. This is an internal rollforward inconsistency, not a mismatch in the balance-sheet total.

Direct comparison with financial_1402.xlsx materially narrows the likely root cause. The 1402 workbook already records the same 43,241,509 million Rial adjustment as two components: -33,467,967 at the 1401 opening balance and -9,773,542 as a correction to the 1401 loss. Its 1401 closing equity is -37,309,721 and its 1402 closing equity is -38,949,540. The 1403 workbook repeats the same two components in Note 23-1 (9,773,542 + 33,467,967) and appears to apply the full amount again to the 1402/01/01 opening balance, while the reported 1402 closing remains the already-adjusted -38,949,540. The most likely correction is to remove or correct the duplicate comparative opening adjustment, not to restate the closing equity to -82,191,049. This remains a proposed accounting treatment until the owner confirms the original journal entries and approved trial balances. Do not modify the official workbook.

### FS-1404-CF-01 — Exchange-rate effect support

The official Cash Flow amount in جريان هاي نقدي!E22 is 12,556 million Rials.

- Closing-cash bridge: 3,368,287 + 16,570,293 + 12,556 = 19,951,136.
- Note 9-3 explicitly describes the 12,556 million Rial exchange-rate effect and cites National Iranian Gas Company letter No. 1830 dated 1405/01/16.
- The previous statement that no supporting note cross-reference had been identified is superseded.
- A separate detailed rate-calculation schedule was not independently reproduced from the workbook; this is a limitation of this read-only pass, not evidence that the disclosed amount lacks support.

Disposition: DISCLOSURE_REFERENCE_IDENTIFIED; CASH_BRIDGE_PASS; RATE_CALCULATION_NOT_INDEPENDENTLY_REPERFORMED.
### FS-1402/1403-CF-FX-REF-01 — Foreign-exchange cash-flow note reference

- 1403 Cash Flow row 22 reports 4,403 million Rials and references Note 9-5, while the matching amount appears in the Note 9 page at sheet 13!N48 under printed sub-note 9-4.
- 1402 Cash Flow row 22 reports 819 million Rials with no note reference; the matching amount appears in the Note 9 page at sheet 13!N47, but its exact printed sub-note identifier remains unconfirmed.
- Both cash-flow bridges reconcile to closing cash. This is a disclosure cross-reference issue, not an arithmetic difference.

Disposition: REQUIRES_ACCOUNTING_OWNER_CONFIRMATION; no source workbook change.

### FS-1404-CF-02 — One-million-Rial comparative presentation difference

The 1404 comparative Cash Flow column differs from 1403 current figures by +1 in operating cash flow and -1 in investing cash flow (million Rials). Both differences offset; pre-financing net cash movement and closing cash remain identical. Classify as ROUNDING_OR_PRESENTATION_DIFFERENCE_NO_NET_EFFECT, subject to finance confirmation.

### Auditor PDF limitation

The auditor PDFs are scanned/image-based. Initial report pages from the 1402 and 1404 PDFs were visually inspected and contain emphasis-of-matter paragraphs, including litigation and fixed-asset insurance matters. Those paragraphs do not, by themselves, establish a modified opinion. The 1403 PDF did not return page content through the available reader. Full-page OCR and verification of the complete opinion wording and all report matters remain outstanding. Do not infer an unqualified opinion from workbook arithmetic checks.

## 7. Mapping-scope interaction

The existing 1404 Mapping analysis remains separate from this statement arithmetic result:

- 214,848 rows have unique deterministic Mapping.
- 37,907 rows are multi-match / ambiguous and are not proven lineage.
- 132 rows are unmapped; 22 zero-closing rows across seven clearing accounts have no closing exposure.
- 110 rows for account 8161 carry a net 196,907,918,801 Rial statement-balance exposure across 1403–1404. A year-by-year re-performance found 86 zero-balance rows and 24 non-zero rows within this population; the 24 non-zero rows account for the full net exposure. See section 15. This account must not be excluded solely because other zero-balance control accounts are irrelevant. A counterpart / netting relationship requires explicit source evidence and accounting classification.
- Account 8999 has 11 system opening/closing rows; it is excluded from Mapping scope but retained in the source ledger.

## 8. Source-protection and acceptance

- All ten source files were hashed; their bytes were not modified by this task.
- No canonical XLSX/PDF, ledger row, Mapping row, database, application code, or financial value was changed.
- This report is a read-only reconciliation record, not a formal independent audit or signed finance approval.
- FS-1403-EQ-01 remains open. The 1404 FX disclosure reference is identified in Note 9-3; only independent reproduction of the underlying rate calculation remains outside this pass. FS-1402/1403-CF-FX-REF-01 records the 1403 Note 9-5 versus printed 9-4 mismatch and the unresolved 1402 sub-note identifier. A separate 1403/1404 balance-sheet note-reference drift is documented in FS-1403/1404-NOTE-REF-01.
- Auditor PDF opinion text remains unverified due image-only source extraction.

Recommended next action: complete the remaining read-only 1402/1403 note-amount and ledger tie-outs, resolve the documented year-specific note-reference drift through accounting-owner disposition, and route the expanded Draft PR #90 for independent review. Preserve all source rows and keep ambiguous / non-zero exposure accounts visible.


## 9. Control-account pairs verified in the 1403/1404 source ledger

The 1404 source ledger contains rows for fiscal years 1403 and 1404. A separate year-by-year aggregation of closing balances identified two exact account-level control pairs:

| Fiscal year | Debit-side account | Closing balance (Rials) | Credit-side account | Closing balance (Rials) | Combined |
|---|---|---:|---|---:|---:|
| 1403 | 8708 — تسهیم حقوق کارکنان | -67,397,848,445,282 | 8709 — کنترل حقوق کارکنان | +67,397,848,445,282 | 0 |
| 1404 | 8708 — تسهیم حقوق کارکنان | -9,683,034,125,526 | 8709 — کنترل حقوق کارکنان | +9,683,034,125,526 | 0 |
| 1403 | 8718 — تسهیم دستمزد کارگران | -10,330,082,681,061 | 8719 — کنترل دستمزد کارگران | +10,330,082,681,061 | 0 |
| 1404 | 8718 — تسهیم دستمزد کارگران | -4,452,935,519,939 | 8719 — کنترل دستمزد کارگران | +4,452,935,519,939 | 0 |

Both accounts in each pair have a Mapping rule to the same Note 12-1 sub-note, «کارکنان (وام مساعده)», with type O. The account-level balances net to exactly zero separately for 1403 and 1404.

### Dimension caveat

The account-level pair totals do not mean every T1 subgroup nets to zero:

- 8708/8709: 4 T1-dimension mismatches in 1403 and 2 in 1404; the mismatches offset across T1 codes at the full reporting-entity total.
- 8718/8719: 6 T1-dimension mismatches in 1403; all 46 compared T1 groups matched in 1404.

**Presentation rule:** Under the accounting owner's confirmation that these are non-presented control accounts, their combined net closing balance may be excluded from the financial-statement total at the full reporting-entity level. Do not net them independently within each T1 dimension where the subgroup does not match. Preserve both accounts, every underlying ledger row, debit/credit turnover, original Mapping rules, and full drill-down traceability. Their gross balances must not be silently deleted or hidden from the audit trail.

This evidence supports the user's control-account treatment for these two pairs. It does not justify automatically excluding other accounts, including account 8161's separate unmapped non-zero exposure.


## 10. Note-level tie-outs completed — 1404

The following checks were performed against the canonical financial_1404.xlsx workbook. Amounts are million Rials.

### 10.1 Income Statement

| Statement line | Statement amount | Actual note-page content | Result |
|---|---:|---:|---|
| Operating revenue | 243,097,686 | Note 5 — 243,097,686 | MATCH |
| Cost of revenue | -245,897,444 | Note 6 — 245,897,444 | MATCH |
| Selling, administrative and general expenses | -62,814,143 | Note 7 dedicated SGA column — 62,814,143 | MATCH |
| Other income | 1,543,514 | Note 8 — 1,543,514 | MATCH |
| Other non-operating income / expenses | -10,601,182 | Note 9 — -10,601,182 | MATCH |
| Income-tax expense | -4,697,329 | Note 20-3 — 4,697,329 | MATCH |

Note 9 arithmetic: 143,087 + 103,822 + 12,556 - 10,860,647 = -10,601,182. Note 9-3 is the supporting narrative for the exchange-rate effect and cites letter No. 1830 dated 1405/01/16.

Note 7's dedicated selling / administrative / general expense column agrees with the Statement of Profit or Loss. Its gross expense and production/project allocation columns were not assumed to be mutually exclusive or additive without a documented allocation basis; no unsupported cross-foot assertion was imposed.

### 10.2 Statement of Financial Position — asset side

| Asset line | Statement amount | Actual note-page content | Result |
|---|---:|---|---|
| Tangible fixed assets | 673,740,637 | Note 10 | MATCH |
| Intangible assets | 242,194 | Note 11 | MATCH |
| Non-current receivables | 8,310,168 | Note 12-2 | MATCH |
| Prepayments | 6,839,535 | Note 13 | MATCH |
| Inventories | 11,273,650 | Note 14 | MATCH |
| Current receivables | 13,386,398 | Note 12-1 | MATCH |
| Cash | 19,951,136 | Note 15 and Cash Flow closing cash | MATCH |
| **Total assets** | **733,743,718** | Sum of the above seven lines | **MATCH** |

Non-current assets total 682,292,999; current assets total 51,450,719; together they equal total assets of 733,743,718.

### 10.3 Statement of Financial Position — liabilities and equity

| Liability / equity line | Statement amount | Actual note-page content | Result |
|---|---:|---|---|
| Current payables | 145,241,976 | Note 18 current payables | MATCH |
| Non-current payables | 630,414,220 | Note 18 non-current payables | MATCH |
| Employee benefits / future staff obligations | 133,078,121 | Note 19 (34,744,097 + 98,334,024) | MATCH |
| Tax payable | 8,833,412 | Note 20 closing balance | MATCH |
| Advances received | 61,449 | Note 21 | MATCH |
| Share capital | 20,000,000 | Note 16 | MATCH |
| Legal reserve | 1,614 | Note 17 | MATCH |
| Accumulated losses | -203,887,074 | Statement of Changes in Equity | MATCH |

Payables total 775,656,196 (145,241,976 current + 630,414,220 non-current). Total liabilities are 917,629,178. Equity is -183,885,460. Liabilities plus equity equal total assets: 917,629,178 - 183,885,460 = 733,743,718.

The amounts reconcile; the separate statement-reference / note-heading drift is recorded as FS-1403/1404-NOTE-REF-01.

### 10.4 Cash Flow

- Cash from operations: 99,230,533, agreeing to the Note 23 disclosure.
- Cash tax paid: -149,426, agreeing to Note 20-1.
- Exchange-rate effect: 12,556, with Note 9-3 narrative support.
- Closing cash: 19,951,136, agreeing to Note 15 and the Statement of Financial Position.

## 11. Year-aware note structure and ingestion consequence

The former generic note catalog and one-to-one sheet matrix were not reliable. A source-heading audit across the three workbooks established that:

1. One physical worksheet may contain multiple logical notes.
2. One logical note may span several physical worksheets.
3. The logical note sequence changes by fiscal year.
4. In 1403/1404, the separate Note 17 capital-in-progress section present in 1402 is absent; Note 17 becomes legal reserve, and later note numbers shift.
5. The 1403/1404 Statement of Financial Position retained several older note references, creating the cross-reference drift documented in FS-1403/1404-NOTE-REF-01.
6. Physical sheet names are not logical note identifiers. For example, 1404 physical sheet 13 contains Notes 7, 8 and 9; physical sheet 22 contains Notes 13 and 14; physical sheet 23 contains Notes 15, 16 and 17.

The corrected year-aware catalog and physical-sheet matrix are recorded in NOTE_CATALOG.md and NOTE_TO_SHEET_MATRIX.md. The ingestion model must store at least: fiscal year, statement cell/reference, logical note number, printed heading, physical sheet name, and sub-note identifier. Do not infer a note identifier from the sheet name alone.

## 12. Current disposition and next action

- 1402, 1403 and 1404 primary Income Statement and Statement of Financial Position lines now have note-level amount tie-outs recorded above.
- Cash-flow operating cash and closing cash tie to the applicable year-specific note disclosures. The 1403 FX statement cross-reference mismatch and the 1402 FX sub-note identifier remain open; the 1404 Note 9-3 disclosure is identified.
- The 1403 equity rollforward presentation remains open (FS-1403-EQ-01).
- The 1403/1404 balance-sheet note-reference drift remains open for document-owner disposition (FS-1403/1404-NOTE-REF-01).
- The +1/-1 million Rial comparative cash-flow presentation difference remains documented (FS-1404-CF-02).
- Auditor PDF opinion wording and the complete set of report matters remain unverified pending OCR / full-page review.
- Budget-note items BUDGET-1403/1404-N36-37-APPROVED-01 and BUDGET-1404-N39-UNIT-01 affect original-budget disclosure completeness, not actual/revised-budget or primary-statement totals.
- Next action: obtain accounting/budget-owner disposition for FS-1403-EQ-01, FS-1402/1403-CF-FX-REF-01 and the two budget-note disclosure issues; complete full auditor-report extraction; then route the expanded Draft PR #90 for independent review. No source workbook correction is authorized in this task.


## 13. Note-level tie-outs — 1402 and 1403

This section extends the 1404 note-level review to the 1402 and 1403 official workbooks. Amounts are in million Rials. Numeric values were read from the canonical workbook cells; narrative-only disclosures are identified as such. A matching amount is not treated as proof of an unrelated sub-note or a complete transaction-level ledger reconciliation.

### 13.1 Fiscal year 1402 — Income Statement

| Statement line | Statement amount | Actual note-page evidence | Result |
|---|---:|---|---|
| Operating revenue | 123,297,650 | Note 5; financial_1402 sheets 10!J36 and 11!G53 | MATCH |
| Cost of revenue | -123,355,486 | Note 6; sheet 12!K22 | MATCH |
| Selling, administrative and general expenses | -19,618,654 | Note 7; sheet 13!N22 | MATCH |
| Other income | 1,421,110 | Note 8; sheet 13!N36 | MATCH |
| Other non-operating income / expenses | 2,545,735 | Note 9; sheet 13!N51 | MATCH |
| Income-tax expense | No current-year amount presented | Statement row 18 is blank for 1402; comparative amount is -1,068,664. The statement carries note reference 22-4; this current-year blank is not forced into a numeric tie-out. | NO CURRENT-YEAR AMOUNT |

The statement arithmetic remains consistent: gross loss -57,836; operating loss -18,255,380; pre-tax loss -15,709,645; and net loss -15,709,645 million Rials.

### 13.2 Fiscal year 1402 — Statement of Financial Position

| Statement line | Statement amount | Actual note-page evidence | Result |
|---|---:|---|---|
| Tangible fixed assets | 235,873,638 | Note 10; sheet 14!AK29 | MATCH |
| Intangible assets | 190,321 | Note 11; sheet 19!J22 | MATCH |
| Non-current receivables | 6,652,479 | Note 12-2; sheet 21!G22 | MATCH |
| Prepayments | 8,007,661 | Note 13; sheet 22!K19 | MATCH |
| Inventories | 6,818,189 | Note 14; sheet 22!G37 / K37 | MATCH |
| Current receivables | 15,993,056 | Note 12-1; sheet 20!H23 | MATCH |
| Cash | 2,134,188 | Note 15; sheet 23!H11 | MATCH |
| Share capital | 20,000,000 | Note 16 narrative; sheet 23!B17 | MATCH — NARRATIVE |
| Capital in progress | 14,069,826 | Note 17 narrative; sheet 23!B19 | MATCH — NARRATIVE |
| Legal reserve | 1,614 | Note 18 narrative; sheet 23!B22 | MATCH — NARRATIVE |
| Current payables | 46,997,254 | Note 19-1; sheet 24!I23 | MATCH |
| Non-current payables | 188,478,601 | Note 19-2; sheet 27!J8 | MATCH |
| Employee benefits / future staff obligations | 77,644,296 | Note 20; sheet 27!J27 | MATCH |
| Tax payable | 1,363,294 | Note 21; sheet 28!K10 | MATCH |
| Advances received | 135,627 | Note 22; sheet 29!H22 | MATCH |
| Accumulated losses | -73,020,980 | Statement of Changes in Equity; not treated as a note-page amount | STATEMENT ROLL-FORWARD |

The official statement totals remain: total assets 275,669,532; total liabilities 314,619,072; total equity -38,949,540; liabilities plus equity 275,669,532 million Rials.

### 13.3 Fiscal year 1403 — Income Statement

| Statement line | Statement amount | Actual note-page evidence | Result |
|---|---:|---|---|
| Operating revenue | 174,585,508 | Note 5; sheets 10!J36 and 11!G53 | MATCH |
| Cost of revenue | -157,476,581 | Note 6; sheet 12!K22 | MATCH |
| Selling, administrative and general expenses | -25,354,498 | Note 7; sheet 13!N20 | MATCH |
| Other income | 1,085,594 | Note 8; sheet 13!N37 | MATCH |
| Other non-operating income / expenses | 627,800 | Note 9; sheet 13!N52 | MATCH |
| Income-tax expense | -2,922,215 | Note 20-3; sheet 28!K64 / K65 | MATCH |

The #REF! value in sheet 13!S52 is not the amount used for this statement tie-out. The numeric note amount is in N52; the unrelated auxiliary/error cell is not treated as a statement input under the owner-confirmed exclusion rule.

The statement arithmetic remains consistent: gross profit 17,108,927; operating loss -7,159,977; pre-tax loss -6,532,177; and net loss -9,454,392 million Rials.

### 13.4 Fiscal year 1403 — Statement of Financial Position

| Statement line | Statement amount | Actual note-page evidence | Result |
|---|---:|---|---|
| Tangible fixed assets | 328,178,321 | Note 10; sheet 14!AK29 | MATCH |
| Intangible assets | 192,282 | Note 11; sheet 19!J22 | MATCH |
| Non-current receivables | 10,811,230 | Note 12-2; sheet 21!G22 | MATCH |
| Prepayments | 3,354,446 | Note 13; sheet 22!K19 | MATCH |
| Inventories | 8,305,043 | Note 14; sheet 22!G43 / K43 | MATCH |
| Current receivables | 14,980,468 | Note 12-1; sheet 20!H23 | MATCH |
| Cash | 3,368,287 | Note 15; sheet 23!H11 | MATCH |
| Share capital | 20,000,000 | Note 16 narrative; sheet 23!B17 | MATCH — NARRATIVE |
| Legal reserve | 1,614 | Note 17 narrative; sheet 23!B22 | MATCH — NARRATIVE |
| Current payables | 83,215,373 | Actual Note 18-1; sheet 24!I23 | MATCH |
| Non-current payables | 235,828,055 | Actual Note 18-2; sheet 27!J8 | MATCH |
| Employee benefits / future staff obligations | 94,199,107 | Actual Note 19; sheet 27!J27 | MATCH |
| Tax payable | 4,285,509 | Actual Note 20; sheet 28!K10 | MATCH |
| Advances received | 65,965 | Actual Note 21; sheet 29!H19 | MATCH |
| Accumulated losses | -68,405,546 | Statement of Changes in Equity; not treated as a note-page amount | STATEMENT ROLL-FORWARD |

The official statement totals remain: total assets 369,190,077; total liabilities 417,594,009; total equity -48,403,932; liabilities plus equity 369,190,077 million Rials.

### 13.5 Cash-flow note tie-outs and foreign-exchange reference

- 1402 cash from operations of 29,242,666 million Rials ties to the cash-flow disclosure on sheet 29!H74 (logical Note 24).
- 1403 cash from operations of 83,057,772 million Rials ties to sheet 29!H74 (logical Note 22).
- 1402 closing cash of 2,134,188 and 1403 closing cash of 3,368,287 tie to Note 15 on sheet 23!H11 in each workbook.
- 1403 foreign-exchange effect of 4,403 million Rials appears in the Note 9 page at sheet 13!N48, whose printed sub-note identifier is 9-4. The Cash Flow statement row 22 points to 9-5. This is a cross-reference mismatch, not a cash-bridge arithmetic failure.
- 1402 foreign-exchange effect of 819 million Rials appears in the Note 9 page at sheet 13!N47. The Cash Flow statement does not show a note reference for this line; the precise printed sub-note identifier still needs confirmation.
- 1404 foreign-exchange effect of 12,556 million Rials is explicitly described in Note 9-3 and cites NIGC letter No. 1830 dated 1405/01/16, as recorded in section 6.

**New open item FS-1402/1403-CF-FX-REF-01:** confirm the 1402 Note 9 sub-note identifier and correct the 1403 Cash Flow cross-reference (9-5 versus actual Note 9-4) through accounting-owner disposition. Do not change source workbooks in this task.

### 13.6 Confirmed year-aware balance-sheet note-reference drift

The 1402 balance-sheet references align with the printed note sequence: Note 17 is capital in progress, Note 18 is legal reserve, Note 19 is payables, Note 20 is employee benefits, Note 21 is tax payable, and Note 22 is advances received.

In 1403 and 1404, the separate Note 17 capital-in-progress disclosure is no longer present as a standalone note. The printed note sequence is therefore:
- Note 16 — share capital (including 1403 capital reduction/increase narrative);
- Note 17 — legal reserve;
- Note 18 — trade and other payables;
- Note 19 — employee benefits / future staff obligations;
- Note 20 — tax payable and income-tax disclosure;
- Note 21 — advances received / related disclosures.

The 1403/1404 balance-sheet note-reference cells retain several prior numbers (17–22). The underlying statement amounts tie to the actual printed note content shown above, but the cross-reference drift remains a presentation/documentation issue. The official workbooks are preserved unchanged.

### 13.7 Scope and evidence limitations

- This pass extends note-page amount checks for 1402 and 1403; it does not claim complete General Ledger transaction-to-note reconciliation for those years.
- Narrative-only amounts (share capital, capital in progress, legal reserve) were checked against the printed explanatory text, not a numeric total cell.
- The 1402 and 1404 auditor reports were visually inspected only on their initial report pages; emphasis-of-matter paragraphs are present. This does not by itself establish a modified opinion. The 1403 auditor PDF did not return page content through the available reader. Full-page OCR and complete extraction of all three auditor reports remain outstanding.
- The 1403 equity opening-balance presentation item FS-1403-EQ-01 remains open. The statement totals and closing equity still reconcile arithmetically.
- No canonical source workbook/PDF, ledger row, Mapping row, database, application code, or financial value was modified.


## 14. Budget performance, resources and uses — Notes 36–39

This section checks the year-specific budget-performance disclosures against the primary statements and checks the resources-and-uses summaries. Amounts are in million Rials. It also distinguishes non-impacting zero-denominator ratio cells from separate budget-disclosure defects.

### 14.1 Note 36/37 — Performance totals tie to the financial statements

| Fiscal year | Budgeted revenue (revised) | Actual revenue | Revenue variance | Budgeted current expenses (revised) | Actual current expenses | Expense variance |
|---|---:|---:|---:|---:|---:|---:|
| 1402 | 129,806,500 | 127,264,495 | -2,542,005 (-1.96%) | 129,806,500 | 142,974,140 | +13,167,640 (+10.14% overrun) |
| 1403 | 187,773,600 | 176,298,902 | -11,474,698 (-6.11%) | 187,773,600 | 182,831,079 | -4,942,521 (2.63% below budget) |
| 1404 | 272,082,640 | 234,040,018 | -38,042,622 (-13.98%) | 272,082,640 | 308,711,587 | +36,628,947 (+13.46% overrun) |

Primary-statement tie-outs:
- 1402 actual revenue 127,264,495 = service revenue 123,297,650 + other income/non-operating income 3,966,845. Actual current expenses 142,974,140 = cost of revenue 123,355,486 + selling/administrative/general expenses 19,618,654. Net loss is 15,709,645.
- 1403 actual revenue 176,298,902 = service revenue 174,585,508 + other income 1,085,594 + other non-operating income 627,800. Actual current expenses 182,831,079 = cost of revenue 157,476,581 + selling/administrative/general expenses 25,354,498. Pre-tax loss 6,532,177 less income-tax expense 2,922,215 gives net loss 9,454,392.
- 1404 actual revenue 234,040,018 = service revenue 243,097,686 less other non-operating loss 9,057,668. Actual current expenses 308,711,587 = cost of services 245,897,444 + distribution/administrative/general expenses 62,814,143. Pre-tax loss 74,671,569 less income-tax expense 4,697,329 gives net loss 79,368,898.

The actual and revised-budget columns reconcile to the statement amounts. The original-approved-budget column is treated separately below where its source cells are incomplete.

### 14.2 1404 cost allocation and operating variance

The 1403 budget note already shows the same allocation pattern:
- Cost of services: revised budget 101,468,975; actual 157,476,581; overrun 56,007,606 (55.2%).
- Distribution/administrative/general: revised budget 85,104,625; actual 25,354,498; underspend 59,750,127 (70.2%).
- Combined actual current expenses 182,831,079 are 4,942,521 below the revised total budget 187,773,600. Thus a favourable total expense variance coexists with a large cost-of-service overrun.

The 1403 gross-profit budget was 74,682,275 versus actual gross profit of 17,108,927, an adverse variance of 57,573,348. The 1404 budget note shows a larger split between service cost and distribution/administrative expenses:

| Cost group | Revised budget | Actual | Variance | Interpretation |
|---|---:|---:|---:|---|
| Cost of services | 133,555,243 | 245,897,444 | +112,342,201 | 84.1% over budget |
| Distribution and administrative/general | 136,145,357 | 62,814,143 | -73,331,214 | 53.9% below budget |
| Cost-group subtotal (excluding other payments) | 269,700,600 | 308,711,587 | +39,010,987 | Subtotal only; see note below |

**Important reconciliation boundary:** the first two revised-budget subtotals above are the actual note 36/37 category amounts. The note's overall revised-budget total for the full current-expense section is 272,082,640, not the simple sum 269,700,600, because the separate other-payments row carries a revised budget of 2,382,040 and actual zero. The authoritative total-row variance remains 36,628,947 as shown in section 14.1. Do not replace the official total with the subtotal arithmetic.

The service-cost gross result also changed materially: revised-budget gross profit was 117,922,057, while actual gross result was a loss of 2,799,758 — an adverse movement of 120,721,815.

The 1404 Note 38 narrative itself states that traditional budgeting rather than activity-based budgeting creates artificial deviations when costs are split between cost of services and distribution/administrative/general expenses. It says activity-based budgeting is expected to reduce this distortion. This is consistent with the large cost-of-service overrun and distribution/administrative underspend. It does not prove that every variance is only classification; the operational drivers still need separate validation.

Other notable 1404 drivers documented in the note:
- Depreciation of production factors: revised budget 36,440,000; actual 71,342,750; adverse variance 34,902,750. The narrative attributes the increase to assets transferred from the Gas Engineering and Development Company for the sixth national pipeline (BOT) and depreciation from the assets' commissioning date.
- Legal-entity service contracts: revised budget 39,314,000; actual 72,323,422; adverse variance 33,009,422.
- Future employee retirement obligations: actual 44,228,423 versus revised budget 18,524,000; adverse variance 25,704,423. The narrative attributes this to an updated actuarial estimate.
- Other non-operating income/expense: revised budget +8,105,340 versus actual -9,057,668; adverse movement 17,163,008.
- Other receipts: revised budget 12,500,000; actual zero.

### 14.3 Note 39 — Resources and uses reconcile for all three years

| Fiscal year | Revised-budget resources | Actual resources | Actual uses | Resource/uses tie |
|---|---:|---:|---:|---|
| 1402 | 65,000,000 | 47,443,159 | 47,443,159 | MATCH |
| 1403 | 56,633,600 | 61,677,400 | 61,677,400 | MATCH |
| 1404 | 117,000,000 | 71,738,067 | 71,738,067 | MATCH |

Composition:
- 1402 actual resources: depreciation reserve 47,443,159; actual capital investment 39,974,394 plus debt repayments 7,468,765 equals actual uses 47,443,159.
- 1403 actual resources: depreciation reserve 54,138,598 plus other resources/receivables 7,538,802 equals 61,677,400; actual capital investment is 61,677,400 and debt repayment is zero.
- 1404 actual resources: depreciation reserve 71,738,067 and other resources/receivables zero; actual capital investment 67,261,515 plus debt repayments 4,476,552 equals 71,738,067.

1404 execution against revised budget:
- Actual resources/uses 71,738,067 versus revised 117,000,000: shortfall 45,261,933 (38.69%).
- Depreciation reserve 71,738,067 versus revised 64,000,000: 7,738,067 above budget (12.09%).
- Other resources/receivables zero versus revised 53,000,000: 53,000,000 shortfall.
- Capital investment 67,261,515 versus revised 97,000,000: 29,738,485 below budget (30.66%).
- Debt repayments 4,476,552 versus revised 20,000,000: 15,523,448 below budget (77.62%).

### 14.4 Quantitative operating targets

| Measure | 1402 target / actual | 1403 target / actual | 1404 target / actual |
|---|---:|---:|---:|
| Coating replacement (km) | 43 / 20 (46.5%) | 60 / 56 (93.3%) | 22 / 17 (77.3%) |
| Class change / pipe replacement (km) | 0 / 2 (ratio not meaningful; target zero) | 4 / 4 (100%) | 1 / 0.821 (82.1%) |
| Intelligent pipeline pigging (km) | 566 / 504 (89.0%) | 1,915 / 1,406 (73.4%) | 1,100 / 807 (73.4%) |
| Turbo-compressor repairs (units) | 217 / 188 (86.6%) | 75 / 70 (93.3%) | 75 / 54 (72.0%) |

These are physical-output indicators, not financial statement amounts. They should not be combined with financial variances without considering project scope, commissioning, asset availability and approved work-program changes.

### 14.5 Budget-note disclosure anomalies — separate from primary-statement errors

**BUDGET-1403/1404-N36-37-APPROVED-01**
- In 1403 Note 36-37, original-approved-budget cells G120 and G123 are stored as #REF!.
- In 1404 Note 36-37, original-approved-budget cells G127 and G130 are stored as #REF!.
- Revised-budget and actual columns (I/K in 1403; I/K in 1404) are populated and reconcile to the financial statements.
- These errors do not change actual statement amounts or the revised-budget performance totals, but the original-approved-budget comparison is incomplete. They are not classified as zero-balance control-account errors.

**BUDGET-1404-N39-UNIT-01**
- Note 39 states that amounts are in million Rials.
- In the 1404 workbook, original-budget cells E22:E32 contain raw Rial-scale values while revised-budget and actual cells F/G contain million-Rial values. Example: E22 = 7,771,200,000,000 while F22 = 7,771,200 and G22 = 4,537,751; E32 = 97,000,000,000,000 while F32 = 97,000,000 and G32 = 67,261,515.
- The E-column cells use ordinary integer number formatting without a million-scale display adjustment. E35, by contrast, is 12,500,000, consistent with the million-Rial convention. The original-budget column is therefore mixed-unit, not simply a uniform Rial column.
- E9 and E16 in the same original-budget column are #REF!. The revised-budget and actual resources/uses totals still tie at 71,738,067, but the original-budget comparison in Note 39 is not reliable as displayed.
- Do not silently divide or repair the source values. Accounting/reporting owner must confirm whether the original-budget source values were entered in Rials and should be normalized for presentation.

**BUDGET-ZERO-RATIO-01 — excluded from material issue count**
- #DIV/0! occurs in percentage cells where the corresponding amount and budget denominator are both zero: 1402 Note 38 I38; 1403 Note 39 I38; 1404 Note 39 I38.
- These are undefined zero/zero ratios only. No amount or total is affected; they are excluded from statement-impact exceptions under the owner-confirmed rule.

### 14.6 Budget review conclusion and next action

- Note 36/37 actual revenue, current expenses and profit/loss figures reconcile to the primary statements for all three years.
- Note 39 actual resources and uses reconcile exactly for all three years.
- The 1404 performance story is not a simple across-the-board overspend: cost of services is materially over budget while distribution/administrative expenses are materially under budget. The note's own narrative identifies traditional cost allocation as a source of artificial variance.
- The original-approved-budget columns in 1403/1404 have #REF! gaps; the 1404 Note 39 original-budget column additionally mixes Rial-scale and million-Rial-scale values. These do not invalidate the primary statements or the actual/revised-budget tie-outs, but they do prevent full reliance on those original-budget comparisons.
- Next action: obtain accounting/budget-owner disposition for BUDGET-1403/1404-N36-37-APPROVED-01, BUDGET-1404-N39-UNIT-01 and MAP-8161-01. Do not edit official workbooks in this task.

## 15. Account 8161 — year-by-year unmapped exposure refinement

A targeted re-performance of the 1403 and 1404 source-ledger rows against the 1404 Mapping rules separates zero-balance rows from rows that affect the statement-balance column. Matching uses account, T1, current/capital, T4 and type; blank Mapping dimensions are treated as wildcards, consistent with the existing helper-key design.

### 15.1 Reconciled population

| Fiscal year | Unmapped rows | Zero statement-balance | Non-zero statement-balance | Net exposure (Rials) |
|---|---:|---:|---:|---:|
| 1403 | 61 | 41 | 20 | 144,125,670,091 |
| 1404 | 49 | 45 | 4 | 52,782,248,710 |
| **Total** | **110** | **86** | **24** | **196,907,918,801** |

The source columns are AA (CLOSING) and AC (مانده صورت مالی) for 1403, and X (CLOSING) and Z (مانده صورت مالی) for 1404. Signed closing and statement-balance totals agree for the unmapped subsets in both years. The 86 zero-balance rows remain preserved but are not material statement exposure.

### 15.2 Non-zero unmatched combinations

| Year | T1 code | Current / capital | T4 code | Rows | Non-zero rows | Net statement balance (Rials) |
|---|---:|---|---:|---:|---:|---:|
| 1403 | 117001 | Current | 4512 | 2 | 1 | -5,425,842,707 |
| 1403 | 117373 | Capital | 4512 | 2 | 1 | +5,000,000,000 |
| 1403 | 117401 | Current | 4512 | 14 | 9 | +57,139,085,409 |
| 1403 | 117488 | Current | 4502 | 22 | 7 | +48,274,392,545 |
| 1403 | 117865 | Current | 4512 | 1 | 1 | +8,522,211,152 |
| 1403 | 118701 | Current | 4512 | 4 | 1 | +30,615,823,692 |
| 1404 | 117088 | Capital | 4512 | 2 | 1 | +11,365,395,802 |
| 1404 | 117865 | Current | 4512 | 2 | 1 | +8,522,211,152 |
| 1404 | 118701 | Current | 4512 | 7 | 2 | +32,894,641,756 |

These nine year/key combinations represent seven distinct candidate mapping keys. The recurring 117865 and 118701 combinations appear in both years.

### 15.3 Mapping disposition — source note references corroborate the missing rules

All 24 non-zero unmatched rows were inspected individually. Their source-ledger column A (یادداشت کل) already contains a consistent note reference for each of the seven missing mapping keys:

| T1 code | Current / capital | T4 code | Source-ledger note ID | Note title in source ledger |
|---|---|---:|---:|---|
| 117001 | Current | 4512 | 13 | پیمانکاران جاری |
| 117373 | Capital | 4512 | 10 | پیش پرداخت های سرمایه ای |
| 117401 | Current | 4512 | 13 | پیمانکاران جاری |
| 117488 | Current | 4502 | 13 | پیمانکاران جاری |
| 117865 | Current | 4512 | 13 | پیمانکاران جاری |
| 118701 | Current | 4512 | 13 | پیمانکاران جاری |
| 117088 | Capital | 4512 | 10 | پیش پرداخت های سرمایه ای |

This is direct source-ledger evidence for the intended note ID, not an inference from the T4 account description alone. It supports adding seven corresponding rules to the derived Mapping logic, subject to a final control check that the Mapping workbook's key construction and rule precedence reproduce these source note IDs. The official mapping workbook remains unchanged.

**Open item MAP-8161-01:** add the seven rules in a controlled, versioned Mapping update using the source-ledger note IDs above; rerun deterministic/ambiguous/unmapped counts; verify all 24 non-zero rows map to Notes 10 or 13 as shown; and confirm the 196,907,918,801 Rial statement-balance exposure is fully assigned. Preserve the 86 zero-balance rows for drill-down traceability.

### 15.4 Acceptance boundary

This refinement does not establish that account 8161 is a zero-net control account, does not identify an offsetting counterpart, and does not authorize exclusion from the financial statements. The non-zero balances remain an open mapping/classification exposure until disposition.


### 15.5 Direct workstation revalidation and seven-rule proposal — 2026-11-11

A read-only validation was performed directly against the three source workbooks on the Aram Windows workstation. The current SHA-256 values match the source integrity baseline in section 3; no workbook was modified.

- The Mapping sheet contains 66 rows for account 8161.
- All seven candidate keys were tested against account, T1, current/capital, T4 and type using the existing blank-dimension wildcard convention. No existing row matched any of the seven keys.
- The 24 non-zero rows continue to route to source note IDs 10 or 13 exactly as recorded in section 15.3.
- The 1403 source workbook and the 1404 source workbook both contain the 1403 population; the 1403 key-level results are consistent. The year-specific totals remain 1403: 20 non-zero rows / 144,125,670,091 Rials; 1404: 4 non-zero rows / 52,782,248,710 Rials.
- The proposed seven rows, observed helper-key construction, key-level row counts, source note IDs, source hashes, and acceptance checks are recorded in [MAP_8161_SEVEN_RULES_PROPOSAL_20261111.md](MAP_8161_SEVEN_RULES_PROPOSAL_20261111.md).

This improves the evidence and proposal quality but does not close MAP-8161-01. The proposal is not approved or applied; the official Mapping workbook and all source ledgers remain unchanged. Accounting-owner approval, independent review, a derived-copy rerun and exact count/exposure reconciliation are still required.


### 15.6 In-memory dry-run of the seven-rule proposal

The seven candidate rules were evaluated in memory against all account-8161 ledger rows for 1403 and 1404 using the current Mapping match dimensions and wildcard behavior. The 66 existing Mapping rows were retained as the baseline; the seven candidates were appended only to an in-memory list. No workbook was saved or modified.

| Year | Account-8161 rows | Before unique | Before unmatched | After unique | After unmatched | New rows mapped | New non-zero rows | New net statement balance (Rials) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1403 | 8,209 | 8,148 | 61 | 8,195 | 14 | 47 | 20 | +144,125,670,091 |
| 1404 | 8,866 | 8,817 | 49 | 8,845 | 21 | 28 | 4 | +52,782,248,710 |
| **Total** | **17,075** | **16,965** | **110** | **17,040** | **35** | **75** | **24** | **+196,907,918,801** |

No ambiguous matches were produced before or after the simulation. The proposed rules match 75 rows (24 non-zero and 51 zero-balance); 35 remaining unmatched rows all have zero statement balance. Thus all original 86 zero-balance rows remain preserved and traceable: 51 would gain a rule match and 35 would remain unmatched. The 24 non-zero rows and their full signed exposure reconcile exactly.

This simulation supports the technical correctness of the proposed rule set under the current matcher. It does not constitute accounting-owner approval, independent review, or permission to edit the official Mapping workbook. MAP-8161-01 remains open.


### 15.7 Root-cause refinement — FS-1403-EQ-01 and duplicate Note 23

A direct side-by-side inspection of the official 1402 and 1403 equity statements, plus the 1403 Note 23 pages, refined the earlier interpretation. The 43,241,509 million Rial amount is not a new unexplained adjustment: it is exactly the sum of two prior-period corrections already recorded in the 1402 workbook (-33,467,967 at the 1401 opening and -9,773,542 against the 1401 loss). The 1402 workbook carries these through to closing 1401 equity of -37,309,721 and closing 1402 equity of -38,949,540. The 1403 workbook repeats the same total at the opening of its 1402 comparative rollforward, but its reported 1402 closing remains -38,949,540. This strongly indicates a duplicated comparative opening adjustment. Do not restate the closing balance to -82,191,049 based on the displayed row 9 alone.

The 1403 Note 23 section is also duplicated: sheet 29 contains Note 23 corrections/reclassifications (including Note 23-1-1 actuarial adjustment disclosure); sheet 30 separately prints Note 23 non-cash transactions. The equity statement's generic Note 23 reference is ambiguous and should be made specific to the relevant subnote after owner approval.

See [FS_1403_EQUITY_DUPLICATE_PRIOR_PERIOD_ADJUSTMENT_20261111.md](FS_1403_EQUITY_DUPLICATE_PRIOR_PERIOD_ADJUSTMENT_20261111.md) for cell-level evidence, exact workbook hashes, recommended disposition and acceptance checklist. Official financial workbooks remain unchanged.


### 15.8 Auditor-report visual extraction status — 2026-11-11

- `auditor_1402.pdf`: 48 pages. The reader rendered the first five pages as page images; the text layer is empty. The visible opinion page uses fair-presentation wording and contains a separate emphasis-of-matter section concerning the consequences of legal claims. No modified-opinion wording was visible in the inspected opening pages.
- `auditor_1404.pdf`: 47 pages. The reader rendered the first five pages as page images; the text layer is empty. The visible opinion page uses fair-presentation wording and contains a separate emphasis-of-matter section concerning the consequences of legal claims. No modified-opinion wording was visible in the inspected opening pages.
- `auditor_1403.pdf`: the local reader failed with `Cannot read properties of undefined (reading 'toLowerCase')`; no page content was returned.
- Windows OCR reports only the English recognizer is installed; Persian OCR is not available through the local Windows OCR API. No unsupported translation or opinion inference has been made.

This is an opening-pages visual review only, not a full-page report review. Complete auditor opinion / all-matters classification remains NOT_VERIFIED, especially for 1403. No PDF was modified.


### 15.9 Budget #REF! and Note 39 unit validation — 2026-11-11

Direct read-only inspection confirmed all six identified #REF! cells are stored Excel error values (`data_type = e`) in both formula-mode and data-only reads; they are not intact formulas that can be refreshed. The affected cells are 1403 sheet 36-37 G120/G123; 1404 sheet 36-37 G127/G130; and 1404 sheet 39 E9/E16. Rebuilding these values requires an authoritative original-approved-budget workbook or signed calculation schedule.

The 1404 Note 39 original-budget column E has a confirmed unit-scale inconsistency in rows E22:E32: every non-zero value is exactly 1,000,000 times the corresponding revised-budget F value, while the printed table unit is million Rials. The 1403 Note 39 comparator has E22:E32 and F22:F32 in the same million-Rial scale. E35 is 12,500,000 in both years and is not part of the 1,000,000 scale anomaly; retain it separately pending source verification. A mechanical conversion scenario for E22:E32 would make original-budget uses 97,012,500 million Rials, but this is not an approved correction and must not be applied without the original budget source.

See [BUDGET_1404_NOTE39_UNIT_AND_REF_ERRORS_20261111.md](BUDGET_1404_NOTE39_UNIT_AND_REF_ERRORS_20261111.md) for cell-level values, ratios, hashes and acceptance steps. No source workbook was modified.
