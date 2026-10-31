# ARAM — direct-method cash flow candidate (NOT OFFICIAL)

## Why this needs a different source

An account-level trial balance only supplies opening balances and aggregate debit/credit turnover. **It does not tell us which cash transaction was operating, investing or financing.** Guessing cash-flow categories from account codes or names would produce a misleading report.

The direct-method candidate therefore requires a separate, explicitly scoped transaction export made of paired cash/counterpart journal lines. It does not manufacture cash-flow categories from aggregate balances.

## Required inputs

1. A structurally valid Pilot XLSX containing the selected company's account balances and turnovers.
2. A local JSON manifest with the same company, fiscal year, currency and unit.
3. An explicit registry of all cash and cash-equivalent accounts in scope, each with evidence.
4. A counterpart-account policy assigning each noncash counterpart account to `OPERATING`, `INVESTING` or `FINANCING`, with evidence.
5. A transaction line for every paired cash posting. Each row contains company/year, unique line ID, voucher/transaction ID, posting date, cash account, counterpart account, cash debit/credit, counterpart debit/credit and evidence reference.

Each transaction row represents **one cash posting paired to one counterpart posting**. If a voucher has several counterpart lines, split it into separately identified paired rows. The cash side must have exactly one nonzero debit or credit; the counterpart must equal the opposite side. All amounts are exact decimal strings. Every counterpart account must exist in the scoped Pilot account list.

If the counterpart account is itself in the cash-account registry, the line is an internal cash transfer. Both cash accounts' turnovers are reconciled, and the transfer is excluded from operating/investing/financing totals. Both sides are included in the transparent internal-transfer totals.

## Arithmetic and reconciliation

For every registered cash account, aggregate the cash-side and any cash-counterpart debit/credit from the transaction manifest and compare them exactly to the account's source turnovers:

```text
opening_cash + source_debits - source_credits = closing_cash
transaction_debits = source_debits
transaction_credits = source_credits
```

For each external counterpart policy:
- Cash debit is an inflow.
- Cash credit is an outflow.
- The explicit counterpart policy supplies the activity category.

Each counterpart account receives exactly one activity category in this version. If one counterpart account contains transactions from multiple cash-flow activities, this account-level policy is insufficient: split the source account into more granular subaccounts or add transaction-level approved classification evidence before using a candidate. The registry itself is user-supplied and is not independently authenticated.

Then:

```text
operating_net = operating_inflows - operating_outflows
investing_net = investing_inflows - investing_outflows
financing_net = financing_inflows - financing_outflows
net_change = operating_net + investing_net + financing_net
opening_cash_and_equivalents + net_change = closing_cash_and_equivalents
```

Cash account opening/closing values use the Pilot source's **debit-net signed** convention; no sign multiplier or account-name inference is applied. A source cash-account turnover mismatch, unmatched cash roll-forward, unclassified counterpart, orphan policy, invalid paired posting, or wrong company/year blocks analyst eligibility.

The manifest's `posting_date` is shape-checked as `YYYY-MM-DD`, month 1–12 and day 1–31, with its year prefix equal to the selected source fiscal-year label. **No Gregorian/Jalali conversion or calendar-date validity proof is performed.** Finance owner must confirm the source date convention.

## Local CLI

For synthetic or explicitly authorized local files:

```bash
cd backend
python -m aram_backend.cash_flow_direct_candidate_cli \
  --file ./synthetic_pilot.xlsx \
  --manifest ./synthetic_cash_transactions.json
```

The manifest root contains `schema_version`, `company_code`, `fiscal_year`, `currency`, `unit`, `cash_accounts`, `counterpart_policies` and `transactions`. Every nested object is strict: unknown or duplicate keys fail closed. Cash manifest max size is 20 MiB; max 5,000 cash accounts, 20,000 counterpart policies and 30,000 transaction pairs. The CLI rejects symlink/nonregular/changed files and emits diagnostic JSON to stdout only. Exit 0 is analyst-preview eligibility only; exit 3 is a valid but blocked reconciliation; exit 2 is invalid/unsafe input.

## Non-approval and release blockers

The candidate always marks `cash_account_scope_owner_approved=false`, `transaction_ledger_completeness_verified=false`, `accounting_policy_authorized=false`, `official_financial_statement=false`, `independently_reviewed=false`, `export_authorized=false`, `releasable=false`. Even an eligible preview does not prove that the registry includes every cash equivalent or that the transaction export is complete/authentic.

Before any official use:
- Confirm completeness of all cash/bank/cash-equivalent accounts and their approved accounting scope.
- Reconcile every paired transaction line to source voucher IDs and immutable source evidence.
- Confirm classification of every counterpart account with the financial owner.
- Review bank overdrafts, restricted cash, foreign currency, noncash transactions, leases, taxes and other applicable cash-flow policy.
- Cross-check closing cash to the balance sheet and net income/working-capital effects to the income statement.
- Obtain authenticated finance-owner signoff and three genuinely independent C1/C2/C3 approvals.
- Build immutable official export and Windows UI only after accounting and security gates pass.

No real company ledger, bank statement, source export, database, migration, secret or release artifact is included in this public repository. Use synthetic fixtures in the tests.
