# ARAM — income statement candidate for analyst review (NOT OFFICIAL)

**Development status:** Draft, unmerged and dependent on the earlier Mapping, reconciliation and balance-sheet candidate branches. The software calculates a **traceable provisional income/expense bridge**, not a standards-compliant, auditor-approved income statement.

## Contract and finance boundary

The pure function `build_income_statement_candidate(workbook_bytes, company_code, fiscal_year, references, policies)` consumes an authorized Pilot XLSX snapshot, explicit company/year, separately asserted note-closing references, and a complete set of user-supplied income statement presentation policies.

Every `IS` note must have exactly one valid policy for a note tuple (statement section, note number, subnote code). Each policy requires a category, sign multiplier (+1 / -1), label and evidence reference. The allowed categories are:

| Category | Arithmetic effect |
|---|---|
| `REVENUE` | Adds to revenue |
| `COST_OF_REVENUE` | Deducted from revenue for gross profit |
| `OPERATING_EXPENSE` | Deducted from gross profit |
| `OTHER_INCOME` | Added to operating profit |
| `OTHER_EXPENSE` | Deducted before tax |
| `TAX_EXPENSE` | Deducted for net result |

All presentation amounts must be nonnegative after applying their **explicit** sign multiplier. A negative resulting net income is permitted (a real loss is not an error). Every mapped note — even from BS/CF/EQ — must pass reference reconciliation; only `IS` notes become income-statement rows. No implicit account-code or account-name classification is allowed.

The bridge is:

```text
gross_profit = revenue - cost_of_revenue
operating_profit = gross_profit - operating_expense
profit_before_tax = operating_profit + other_income - other_expense
net_result = profit_before_tax - tax_expense
```

This simplified model is **not** a substitute for accounting policy choices regarding exceptional/nonoperating items, current/deferred tax, discontinued operations, comprehensive income, comparative years or financial statement footnotes. Inputs are book-level closing exposures, *not automatically period movements*. Actual final recognition needs source balances and accounting-owner validation.

All output retains `official_financial_statement=false`, `accounting_policy_authorized=false`, `independently_reviewed=false`, `export_authorized=false`, `releasable=false`; even `eligible_for_analyst_review=true` does not indicate trusted approvals.

## Offline CLI

The manifest schema is the same as the BS candidate CLI with the six income categories. For synthetic or explicitly authorized local data:

```bash
cd backend
python -m aram_backend.income_statement_candidate_cli \
  --file ./synthetic_pilot.xlsx \
  --references ./synthetic_note_controls.json \
  --policies ./synthetic_income_policies.json
```

The strict policy JSON must contain `schema_version: 1`, `company_code`, `fiscal_year`, and `policies`. Every policy has the fields `statement_section`, `note_number`, `subnote_code`, `category`, `sign_multiplier`, `line_label`, `policy_evidence_ref`. Duplicate/unknown JSON keys, mismatched scopes, symlinks, nonregular inputs, invalid amounts and absent policies fail closed. No source files are changed and results are printed only to stdout as JSON.

Exit statuses: `0` mathematically eligible for analyst review (never official), `3` valid request with blocking issues, `2` unsafe/invalid request. No databases, releases, or financial outputs are created.

## Verification and blockers

Run `cd backend && pytest -q tests/test_income_statement_candidate.py tests/test_income_statement_candidate_cli.py` and full Backend CI, reversible Alembic migration check and compilation. Use synthetic workbook tests only. No customer spreadsheets, data files, signing keys, or database records should change.

Acceptance remains blocked on independent C1/C2/C3 reviewer approvals, signed financial owner policy, reconciliation to actual ledger/trial balance (not just control totals), and full four-statement authorization workflow. See Draft PR #60, #61, #62 for parent evidence.
