# Financial Statement Reconciliation — Fiscal Years 1402–1404

**Status:** PRESENT_BUT_UNVERIFIED — independent accounting sign-off remains pending  
**Prepared:** 2026-11-10  
**Repository base:** source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914  
**Scope:** Read-only reconciliation of official primary statements, comparative figures, equity movements, cash flow, and disclosed restatements. No source workbook or PDF was modified.

## 1. Executive result

- 66 arithmetic checks passed across the Income Statement, Statement of Financial Position, and Cash Flow Statement for 1402, 1403, and 1404, including comparative columns.
- 3 additional cross-statement cash checks passed: each year's cash-flow closing balance equals the cash balance in the corresponding Statement of Financial Position.
- The restated 1403 comparative figures presented in the 1404 statements reconcile to Note 22.
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

Assessment: likely duplicated / inconsistently rolled-forward opening restatement presentation in the 1403 equity statement. The reported 1402 closing equity and 1403 balance-sheet equity still tie; this is not evidence that the 1402 or 1403 balance-sheet totals are arithmetically wrong. Keep as REQUIRES_ACCOUNTING_OWNER_DISPOSITION; do not silently repair the official workbook.

### FS-1404-CF-01 — Exchange-rate effect support

The official Cash Flow amount in جريان هاي نقدي!E22 is 12,556 million Rials.

- Closing-cash bridge: 3,368,287 + 16,570,293 + 12,556 = 19,951,136.
- Note 9-3 explicitly describes the 12,556 million Rial exchange-rate effect and cites National Iranian Gas Company letter No. 1830 dated 1405/01/16.
- The previous statement that no supporting note cross-reference had been identified is superseded.
- A separate detailed rate-calculation schedule was not independently reproduced from the workbook; this is a limitation of this read-only pass, not evidence that the disclosed amount lacks support.

Disposition: DISCLOSURE_REFERENCE_IDENTIFIED; CASH_BRIDGE_PASS; RATE_CALCULATION_NOT_INDEPENDENTLY_REPERFORMED.
### FS-1404-CF-02 — One-million-Rial comparative presentation difference

The 1404 comparative Cash Flow column differs from 1403 current figures by +1 in operating cash flow and -1 in investing cash flow (million Rials). Both differences offset; pre-financing net cash movement and closing cash remain identical. Classify as ROUNDING_OR_PRESENTATION_DIFFERENCE_NO_NET_EFFECT, subject to finance confirmation.

### Auditor PDF limitation

The 1404 auditor PDF text extraction returned image-only pages (47 pages, no searchable text). The auditor's opinion wording and report qualifications were therefore not verified in this pass. Do not infer an unqualified opinion from the workbook checks.

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
- FS-1403-EQ-01 remains open. The 1404 FX disclosure reference is now identified in Note 9-3; only independent reproduction of the underlying rate calculation remains outside this pass. A separate 1403/1404 balance-sheet note-reference drift is newly documented in FS-1403/1404-NOTE-REF-01.
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

- 1404 primary Income Statement and all primary Statement of Financial Position lines now have note-level amount tie-outs recorded above.
- 1404 cash-flow closing cash and Note 9-3 exchange-rate disclosure are identified; detailed FX rate calculation is not independently reperformed.
- The 1403 equity rollforward presentation remains open (FS-1403-EQ-01).
- The 1403/1404 balance-sheet note-reference drift remains open for document-owner disposition (FS-1403/1404-NOTE-REF-01).
- The +1/-1 million Rial comparative cash-flow presentation difference remains documented (FS-1404-CF-02).
- Auditor PDF opinion wording remains unverified because the 1404 PDF is image-only in text extraction.
- Next action: independent review of the expanded documentation PR and a separate read-only reconciliation of the remaining 1402/1403 note amounts and relevant ledger ties. No source workbook correction is authorized in this task.
