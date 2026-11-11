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
- One equity rollforward presentation inconsistency remains in the 1403 workbook: the opening balance appears to repeat a 43,241,509 million Rial prior-period correction already reflected in the 1402 closing balance, while the 1402 closing row does not carry that repeated adjustment through.
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

The correct accounting presentation (remove the repeated opening adjustment versus carry it through a restated comparative closing balance) requires the accounting owner’s decision. The reported 1402 closing equity and 1403 balance-sheet equity still tie; this is not evidence that the 1402 or 1403 balance-sheet totals are arithmetically wrong. Keep as REQUIRES_ACCOUNTING_OWNER_DISPOSITION; do not silently repair the official workbook.

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
- 110 rows for account 8161 carry 196,907,918,801 Rials of non-zero closing exposure. This account must not be excluded solely because other zero-balance control accounts are irrelevant. A counterpart / netting relationship requires explicit source evidence and accounting classification.
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
- Next action: resolve FS-1403-EQ-01 and FS-1402/1403-CF-FX-REF-01 with the accounting document owner; complete full auditor-report extraction; then route the expanded Draft PR #90 for independent review. No source workbook correction is authorized in this task.


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
