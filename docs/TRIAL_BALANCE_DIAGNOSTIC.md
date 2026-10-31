# ARAM — unsigned trial balance arithmetic diagnostic

## Scope

This is a **read-only, nonofficial, fail-closed** trial balance control for one explicit company and fiscal year in an authorized Pilot XLSX file. It does not claim that the source ledger is complete, authentic, approved or compliant with any accounting standard.

**Important accounting assumption:** `opening` and `closing` are treated as **net-debit signed balances**; credit-net balances must be negative. `debit` and `credit` represent nonnegative period turnovers. If the real Peyvast/source ledger uses different sign or cumulative semantics, this diagnostic is **not valid** until an approved data normalization rule is implemented. Never infer sign from the account code or label.

## Calculations

For each account:

```text
net_debit_movement = debit - credit
closing = opening + net_debit_movement
```

Across all accounts of the selected company and fiscal year:

```text
opening_net_total = sum(opening)
debit_total = sum(debit)
credit_total = sum(credit)
closing_net_total = sum(closing)
debit_credit_difference = debit_total - credit_total
rollforward_difference = opening_net_total + sum(net_debit_movement) - closing_net_total
```

An opening or closing total different from zero is reported; unequal debit/credit period turnovers are reported; nonmatching per-account opening/turnover/closing fails the input gate. Totals use exact Decimal aggregation; all-zero accounts are valid arithmetic, but still do **not** prove completeness. Accounts with negative debit/credit turnovers are rejected under the documented convention.

The result includes the source SHA-256, scoped account count, ordered account/source-row trace, errors and arithmetic totals. It always includes `source_ledger_completeness_verified=false`, `accounting_policies_verified=false`, `official_financial_statement=false`, `independently_reviewed=false`, `releasable=false`. The flag `balanced_for_analyst_review=true` certifies **neither** account completeness nor correctness of the underlying accounting postings.

## Local CLI

```bash
cd backend
python -m aram_backend.trial_balance_diagnostic_cli \
  --file ./synthetic.xlsx \
  --company-code 001 \
  --fiscal-year 1404
```

Exit status `0`: balanced arithmetic for analyst review only. `3`: parsed but one or more accounting totals do not balance (the JSON includes each finding). `2`: invalid/untrusted input, read error, or bad scope; no JSON success output. Nothing is uploaded, stored, posted or exported; only JSON is written to stdout.

The parser rejects oversized XLSX, excessive ZIP expansion, hidden/merged financial data, invalid headers, wrong company/year, duplicate accounts, negative turnovers, invalid decimal figures and changed/missing local files. Results are calculated entirely in memory; XLSX bytes are never mutated.

## Gaps before any real financial release

- Verify the actual net debit/credit sign convention in Peyvast and imported financial data.
- Confirm **completeness** of source ledger; synthetic balanced totals can also be incomplete or fabricated.
- Reconcile account movements, period postings, trial balance and approved Mapping rules into statement numbers and note disclosures.
- Obtain company/year role identities, independent C1/C2/C3 reviews and a formal finance-owner approval.
- Implement authenticated audit signoff, locked fiscal years, immutable snapshots, official XLSX/PDF export and the final Windows GUI.
- Do not upload real financial source documents to the public GitHub repository.

Run `cd backend && pytest -q tests/test_trial_balance_diagnostic.py tests/test_trial_balance_diagnostic_cli.py`, full Backend CI, migration round-trip and compilation. Exact-head CI evidence must be verified from GitHub. Upstream PR #60–#63 remain unmerged.
