# ARAM — offline five-statement pipeline CLI (NOT APPROVAL)

## Command

From the backend directory:

```powershell
python -m aram_backend.five_statement_pipeline_cli --file "C:\\finance\\pilot.xlsx" --manifest "C:\\finance\\pipeline.json"
```

The CLI reads a local Pilot XLSX snapshot and one strict JSON manifest, runs BS/IS/EQ/direct-CF/TB candidates on the same workbook bytes, then runs the cross-statement gate. JSON is written to standard output only.

## Exit codes

- `0`: all candidate engines and cross-statement arithmetic gate are eligible for analyst review. This is **not approval**.
- `3`: source was readable, but one or more candidates or cross-statement controls are blocked. JSON findings are still printed.
- `2`: unsafe or malformed input, unsupported manifest schema, unreadable workbook/manifest or a blocked precondition. A concise error code is printed to standard error.

## Manifest contract

The root object must contain exactly:

`schema_version`, `company_code`, `fiscal_year`, `currency`, `unit`, `references`, `balance_sheet_policies`, `income_statement_policies`, `equity_movement_policies`, `cash_accounts`, `counterpart_policies`, `transactions`, `cash_balance_notes`.

- Schema version is integer `1`; duplicate keys and unknown fields are rejected.
- Currency, units, source company code and year must be explicit; each transaction's company/year must match the root scope before execution.
- Monetary amounts in reference controls and journal transaction rows must be **decimal strings**, not JSON numeric literals or booleans. NaN, Infinity, excessive exponents and out-of-range precision are rejected.
- Presentation sign multipliers must be exactly the JSON integers `1` or `-1`. Numeric booleans and floating-point `1.0` are invalid.
- Identity, category, activity, label and evidence fields must be nonempty strings without leading/trailing whitespace, control characters or excessive length. An explicitly blank `subnote_code` remains supported.
- References use the same fields as the note reconciliation manifest.
- BS/IS/EQ policy rows use the exact dataclass fields of their respective policy classes.
- Cash-account, counterpart and transaction rows use the exact fields of `CashAccountPolicy`, `CashCounterpartPolicy` and `CashFlowEntry`.
- Cash-note selections use `statement_section`, `note_number`, `subnote_code`, `evidence_ref`.
- Limits: manifest 20 MiB; 10,000 references and per-statement policies; 5,000 cash accounts; 20,000 counterpart policies; 30,000 paired cash transactions; 10,000 cash-note selections. The cash registry and cash-note selection cannot be empty.

## Local file safety and privacy

The workbook uses the existing bounded XLSX reader. The manifest uses the existing bounded JSON reader. Both require regular files, reject symlinks, detect file replacement or modification during reads, and do not modify input files. The CLI does not create output files, call a network service, write to the database, post entries, sign or approve statements, or create an official report.

A real manifest can contain account mappings, financial references and transaction details. Keep it in an authorized local directory; **do not commit real company data or transaction manifests to public GitHub**.

## Interpretation

The manifest is a user-supplied policy and evidence package, not authenticated approval. An exit code of zero only means that the supplied candidates reconcile arithmetically. It does not establish source-ledger completeness, bank transaction completeness, accounting-policy authorization, tax compliance, financial-owner approval, C1/C2/C3 review, official report status, or release authorization.
