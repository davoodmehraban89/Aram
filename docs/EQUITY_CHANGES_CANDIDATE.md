# ARAM — statement of changes in equity candidate (NOT OFFICIAL)

## Purpose and boundary

This module builds a **read-only, unsigned equity movement preview** from an authorized Pilot XLSX snapshot, explicit note-closing references and a user-supplied note-level presentation policy. It is not a statutory statement, audited report, accounting approval, posting, or export.

Each mapped `EQ` note requires one policy containing:
- An equity component (`SHARE_CAPITAL`, `SHARE_PREMIUM`, `RETAINED_EARNINGS`, `REVALUATION_SURPLUS`, `OTHER_RESERVES`, `NONCONTROLLING_INTEREST`, `OTHER_EQUITY`).
- A movement class (`CAPITAL_CONTRIBUTION`, `NET_PROFIT_LOSS`, `DIVIDENDS`, `OTHER_COMPREHENSIVE_INCOME`, `TRANSFER`, `PRIOR_PERIOD_ADJUSTMENT`, `OTHER_MOVEMENT`).
- An explicit debit-net sign multiplier (+1/-1), line label and policy evidence reference.

No account-code, account-name, or presumed debit/credit sign is inferred. All mapped statements must still pass the upstream note reconciliation; missing or ambiguous mappings block the candidate.

## Arithmetic

Under the **explicit source assumption** that opening/closing balances are debit-net signed and debit/credit are nonnegative period turnovers:

```text
source_movement = debit_turnover - credit_turnover
source_opening + source_movement = source_closing

presentation_opening = source_opening * sign_multiplier
presentation_movement = source_movement * sign_multiplier
presentation_closing = source_closing * sign_multiplier

opening_equity + total_movements = closing_equity
```

All arithmetic is exact Decimal; source rows, account identifiers, note references and policy evidence are retained. The module rejects per-account roll-forward errors, negative turnover, missing note controls, missing/extra policies and wrong company/year.

**Important granularity constraint:** one policy classifies *all* turnover mapped to one note/subnote as one movement category. If the same account/note contains several transaction types (for example, current-year profit and dividends), split the mappings into separately controlled subnotes or do not use this preview. A single account's debit/credit turnover does not itself prove that a movement is a dividend, profit, contribution or other equity transaction.

The category `NET_PROFIT_LOSS` is a user-supplied classification and is **not yet automatically cross-checked against the income-statement net result**. No cash-flow, tax, other comprehensive income or statutory disclosure is inferred. Comparative periods, ownership changes, non-controlling interests, retrospective adjustments and transfers require separate accounting policy design.

The candidate always marks `official_financial_statement=false`, `accounting_policy_authorized=false`, `source_ledger_completeness_verified=false`, `independently_reviewed=false`, `export_authorized=false`, `releasable=false`. Even `eligible_for_analyst_review=true` means only that this limited arithmetic and supplied control data passed.

## Local-only CLI

For synthetic or explicitly authorized local files:

```bash
cd backend
python -m aram_backend.equity_changes_candidate_cli \
  --file ./synthetic_pilot.xlsx \
  --references ./synthetic_note_controls.json \
  --policies ./synthetic_equity_policies.json
```

Policy JSON root: `schema_version`, `company_code`, `fiscal_year`, `policies`. Each policy has `statement_section`, `note_number`, `subnote_code`, `equity_component`, `movement_category`, `sign_multiplier`, `line_label`, `policy_evidence_ref`. The reference JSON uses the strict note-reconciliation schema.

Exit 0: limited analyst preview only. Exit 3: blocking accounting/reconciliation findings. Exit 2: invalid or unsafe input. The CLI reads local files and emits diagnostic JSON to stdout only; it creates no workbook, PDF, database write or posting.

## Acceptance blockers

- Confirm actual ledger sign and turnover semantics against the source system and approved trial balance.
- Confirm ledger completeness and independently validate every account-to-note mapping.
- Split mixed transaction types to independently controlled subnotes.
- Cross-check profit/loss movements against the income statement and closing equity against the balance sheet.
- Implement authenticated financial-owner approval, three independent C1/C2/C3 reviews, immutable snapshots and official reporting controls.
- Add cash flow statement and the full cross-statement validation layer before release.
- Do not put real company financial data in public GitHub.

Run `cd backend && pytest -q tests/test_equity_changes_candidate.py tests/test_equity_changes_candidate_cli.py`, full backend CI, reversible migration check and compileall. The upstream PR #60–#64 chain is still draft/unmerged.
