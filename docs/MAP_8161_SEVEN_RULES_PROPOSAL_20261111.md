# Account 8161 — Seven Missing Mapping Rules (Controlled Proposal)

**Status:** PROPOSED — NOT APPROVED / NOT APPLIED  
**Prepared:** 2026-11-11  
**Related control item:** MAP-8161-01  
**Related evidence:** [Financial Statement Reconciliation 1402–1404](FINANCIAL_STATEMENT_RECONCILIATION_1402_1404.md)  
**Working branch:** `docs/financial-statement-reconciliation-1402-1404-20261110`

## 1. Executive conclusion

A read-only revalidation was performed directly on the Aram Windows workstation against:

- `data/source_ledgers/source_1403.xlsx`
- `data/source_ledgers/source_1404.xlsx`
- `data/mappings/mapping_1404.xlsx`

The current file hashes match the hashes recorded in the reconciliation baseline:

| File | Bytes | SHA-256 |
|---|---:|---|
| source_1403.xlsx | 23,928,541 | `747FAE7B8DE9866DFBB45CE3A983584A8AC832DEF59F2C65874302F0F87CBB22` |
| source_1404.xlsx | 32,062,394 | `5B4790DCE6E9EA169D61C68751BC6FD5DC390012BC14473B0298BA5AAC30D044` |
| mapping_1404.xlsx | 2,574,677 | `8B3F94389E61B76775E00B8BEC8B9E241F7CCE5097505C61199574855ADAE574` |

The Mapping workbook contains 66 existing rows for account 8161. Comparing the seven candidate keys against account, T1, current/capital, T4 and type (with blank Mapping dimensions treated as wildcards) found **zero matching rules** for all seven keys.

The source ledger's note ID for every non-zero candidate row is consistent with Note 10 or Note 13. This supports the proposed note routing but does not itself constitute accounting-owner approval.

## 2. Proposed seven rules

| # | Account | T1 | Current / capital | T4 | T4 description | Type | Note ID | Note title | Sub-note |
|---:|---:|---:|---|---:|---|---|---:|---|---|
| 1 | 8161 | 117001 | جاری | 4512 | علی‌الحساب پرداختی | O | 13 | پیش‌پرداخت‌ها | پیمانکاران جاری |
| 2 | 8161 | 117373 | سرمایه‌ای | 4512 | علی‌الحساب پرداختی | O | 10 | دارایی‌های ثابت | پیش‌پرداخت‌های سرمایه‌ای |
| 3 | 8161 | 117401 | جاری | 4512 | علی‌الحساب پرداختی | O | 13 | پیش‌پرداخت‌ها | پیمانکاران جاری |
| 4 | 8161 | 117488 | جاری | 4502 | حساب کنترل پیش‌پرداخت | O | 13 | پیش‌پرداخت‌ها | پیمانکاران جاری |
| 5 | 8161 | 117865 | جاری | 4512 | علی‌الحساب پرداختی | O | 13 | پیش‌پرداخت‌ها | پیمانکاران جاری |
| 6 | 8161 | 118701 | جاری | 4512 | علی‌الحساب پرداختی | O | 13 | پیش‌پرداخت‌ها | پیمانکاران جاری |
| 7 | 8161 | 117088 | سرمایه‌ای | 4512 | علی‌الحساب پرداختی | O | 10 | دارایی‌های ثابت | پیش‌پرداخت‌های سرمایه‌ای |

The Persian current/capital values and note titles above are the proposed canonical values to be entered in a separate derived Mapping candidate after approval. They are not written to the official workbook.

## 3. Source-ledger evidence by key

Amounts below are signed values in Rials from the statement-balance column. The table lists all candidate-key rows in the relevant source year, not only non-zero rows.

| Year | T1 | Current / capital | T4 | Rows | Non-zero rows | Net statement balance (Rials) | Note ID on non-zero rows |
|---|---:|---|---:|---:|---:|---:|---|
| 1403 | 117001 | جاری | 4512 | 2 | 1 | -5,425,842,707 | 13 |
| 1403 | 117373 | سرمایه‌ای | 4512 | 2 | 1 | +5,000,000,000 | 10 |
| 1403 | 117401 | جاری | 4512 | 14 | 9 | +57,139,085,409 | 13 |
| 1403 | 117488 | جاری | 4502 | 22 | 7 | +48,274,392,545 | 13 |
| 1403 | 117865 | جاری | 4512 | 1 | 1 | +8,522,211,152 | 13 |
| 1403 | 118701 | جاری | 4512 | 4 | 1 | +30,615,823,692 | 13 |
| 1404 | 117088 | سرمایه‌ای | 4512 | 2 | 1 | +11,365,395,802 | 10 |
| 1404 | 117865 | جاری | 4512 | 2 | 1 | +8,522,211,152 | 13 |
| 1404 | 118701 | جاری | 4512 | 7 | 2 | +32,894,641,756 | 13 |

For completeness, the 1403 source also contains two rows for key (117088, capital, 4512); both have zero statement balance. This key is included because it carries a non-zero row in 1404 and should be represented consistently in the derived rule set.

Totals for the non-zero rows:
- 1403: 20 rows, net +144,125,670,091 Rials.
- 1404: 4 rows, net +52,782,248,710 Rials.
- Combined: 24 rows, net +196,907,918,801 Rials.

The 86 zero-statement-balance unmatched rows remain preserved for traceability and are not included in the non-zero exposure above.

## 4. Mapping formula construction

The existing workbook uses these three helper-key columns:

- Column J — current / capital-independent helper: account + T1 + T4.
- Column K — account + current/capital + T4 + type.
- Column L — account + current/capital + T4 + type + note ID.

The seven proposed helper keys are:

| T1 | Kind | T4 | Column J | Column K | Column L |
|---:|---|---:|---|---|---|
| 117001 | جاری | 4512 | `81611170014512` | `8161جاری4512O` | `8161جاری4512O13` |
| 117373 | سرمایه‌ای | 4512 | `81611173734512` | `8161سرمایه‌ای4512O` | `8161سرمایه‌ای4512O10` |
| 117401 | جاری | 4512 | `81611174014512` | `8161جاری4512O` | `8161جاری4512O13` |
| 117488 | جاری | 4502 | `81611174884502` | `8161جاری4502O` | `8161جاری4502O13` |
| 117865 | جاری | 4512 | `81611178654512` | `8161جاری4512O` | `8161جاری4512O13` |
| 118701 | جاری | 4512 | `81611187014512` | `8161جاری4512O` | `8161جاری4512O13` |
| 117088 | سرمایه‌ای | 4512 | `81611170884512` | `8161سرمایه‌ای4512O` | `8161سرمایه‌ای4512O10` |

**Control note:** helper-key values above are derived from the observed workbook convention. Before writing a candidate workbook, verify the exact Persian code points, formula/data type, formula precedence and uniqueness against the original workbook. The official Mapping workbook remains unchanged.

## 5. Required validation before approval

1. Reproduce the current baseline counts from the exact source and Mapping hashes above.
2. Add these seven rows only to a separate proposed Mapping copy; never overwrite the official source.
3. Re-run the exact Mapping algorithm, including wildcard precedence and type normalization.
4. Confirm the seven new keys yield exactly one deterministic rule each and no ambiguous matches.
5. Confirm all 24 non-zero source rows route to the expected Note 10 / Note 13.
6. Confirm the net statement-balance exposure assigned by the seven keys equals 196,907,918,801 Rials, split by year exactly as shown.
7. Confirm all 86 zero-balance rows remain present and traceable.
8. Re-run total unmatched / ambiguous / deterministic counts and explain every count change.
9. Verify the original Mapping workbook hash is unchanged.
10. Obtain accounting-owner approval for the note classification and an independent reviewer approval for the derived Mapping candidate.

## 6. Acceptance boundary

- This document is a controlled proposal, not an approved accounting judgment.
- No official Mapping row, ledger row, financial workbook, note, statement, or database has been changed.
- No zero-balance account is deleted or hidden.
- No offsetting-counterpart relationship is inferred for account 8161.
- The 196,907,918,801 Rial exposure remains open until the proposed rules are applied in a derived copy, all controls pass, and the responsible accounting owner approves the disposition.

**Decision requested:** approve or reject the seven proposed note-routing rules as a set, with any exceptions explicitly identified. Until that decision is recorded, keep MAP-8161-01 open.


## 7. In-memory dry-run simulation (read-only) — 2026-11-11

The seven proposed rules were added only to an in-memory candidate list and evaluated against all account-8161 rows for the respective reporting years. The existing 66 Mapping rules were applied first using the same account/T1/current-capital/T4/type matching convention and blank-dimension wildcard behavior. No derived workbook was saved and no official source was edited.

| Year | Account-8161 rows | Before: unique | Before: unmatched | After: unique | After: unmatched | New rows mapped | New non-zero rows | New net statement balance (Rials) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1403 | 8,209 | 8,148 | 61 | 8,195 | 14 | 47 | 20 | +144,125,670,091 |
| 1404 | 8,866 | 8,817 | 49 | 8,845 | 21 | 28 | 4 | +52,782,248,710 |
| **Total** | **17,075** | **16,965** | **110** | **17,040** | **35** | **75** | **24** | **+196,907,918,801** |

- No ambiguous match was produced in either year before or after the proposal simulation.
- The seven proposed rules map 75 ledger rows in total: 24 non-zero and 51 zero-statement-balance rows.
- The 35 remaining unmatched rows are all zero-statement-balance rows; they remain in the ledger and are not deleted or suppressed.
- The original 86 zero-balance rows are preserved: 51 are matched by the proposed rules and 35 remain unmatched. All remain available for drill-down.
- The simulated new mapping exposure ties exactly to the previously identified 196,907,918,801 Rial exposure, with the same year split.

**Interpretation:** under the tested matching convention, the seven-rule proposal would eliminate all 24 non-zero unmapped rows and reduce the account-8161 unmatched population from 110 to 35, with no new ambiguity. This is strong technical evidence, but not approval to update the official workbook. Accounting-owner approval and independent review remain mandatory.
