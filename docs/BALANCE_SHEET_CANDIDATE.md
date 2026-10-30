# ARAM — unsigned balance-sheet presentation candidate (development-only)

This phase adds **explicit-policy, read-only candidate BS rows** to the upstream [Draft PR #61](https://github.com/davoodmehraban89/Aram/pull/61). This is **NOT** an Iranian statutory financial statement, not audited, not approved and not exportable for real business use.

## Source-to-candidate computation

1. Input: byte snapshot of an authorized Pilot XLSX workbook with exact company and fiscal year.
2. Every account must have an unambiguous workbook-marked Approved+Valid mapping to a note. Every mapped note, including IS/CF/EQ notes, must reconcile to a distinct supplied reference closing exposure. These are untrusted file claims, not signer authority.
3. Each **BS note only** requires exactly one explicit `BalanceSheetLinePolicy`: note tuple (section, note, subnote), presentation category `ASSETS`/`LIABILITIES`/`EQUITY`, multiplier `+1` or `-1`, human label, evidence reference. This explicit policy avoids inventing ledger debit/credit signs.
4. Non-BS notes are not silently converted into BS rows. All notes still undergo upstream reference reconciliation.
5. Displayed amount = source note closing exposure × explicitly supplied sign. Asset, liability and equity totals use exact Decimal arithmetic; `assets - liabilities - equity` must be zero to be arithmetically balanced.
6. Missing/extra/duplicate policies, negative presentation values, lack of one of three categories, blocked mappings and mismatched reference totals prohibit `eligible_for_analyst_review`.
7. Even a mathematically balanced candidate sets `official_financial_statement=False`, `accounting_policy_authorized=False`, `independently_reviewed=False`, `export_authorized=False`, `releasable=False`.

The hashes of the source workbook, references and sign/presentation policies are included in the result. Never equate those hashes with approvals.

## Example from synthetic data only

```python
from aram_backend.balance_sheet_candidate import (
    BalanceSheetLinePolicy, build_balance_sheet_candidate,
)
from aram_backend.reconciliation_review import NoteReference

candidate = build_balance_sheet_candidate(
    synthetic_bytes, company_code="001", fiscal_year=1404,
    references=[
        NoteReference("BS", "Assets", "A1", "", "100", "SYNTH-TB-A"),
        NoteReference("BS", "Liabilities", "L1", "", "-60", "SYNTH-TB-L"),
        NoteReference("BS", "Equity", "E1", "", "-40", "SYNTH-TB-E"),
    ],
    policies=[
        BalanceSheetLinePolicy("Assets", "A1", "", "ASSETS", 1, "Assets", "POL-A"),
        BalanceSheetLinePolicy("Liabilities", "L1", "", "LIABILITIES", -1, "Liabilities", "POL-L"),
        BalanceSheetLinePolicy("Equity", "E1", "", "EQUITY", -1, "Equity", "POL-E"),
    ],
)
assert candidate.balance_difference == "0"
assert not candidate.official_financial_statement
```

## Test & approval gates

- Focused: `cd backend && pytest -q tests/test_balance_sheet_candidate.py`
- Full: `cd backend && pytest -q`, `alembic upgrade head`, `alembic downgrade base`, `python -m compileall -q src tests migrations`.
- No modification to canonical `data/`, no DB writes, no migrations, no enterprise IdP, no HTML/GUI/export/print functionality in this PR.
- A real finance owner must specify the required Iranian financial-statement classification and sign policies, verify trial balance and note disclosures, and approve fiscal-year controls. Real C1/C2/C3 reviewers must independently sign off. This preview does not substitute for those controls.
