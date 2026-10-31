# ARAM — cross-statement reconciliation gate (NOT APPROVAL)

## Purpose

The five independent previews now need a single arithmetic gate before any combined analyst review packet can be considered:

- Trial balance diagnostic
- Balance sheet candidate
- Income statement candidate
- Statement of changes in equity candidate
- Direct-method cash flow candidate

`reconcile_cross_statements(...)` consumes the typed candidate objects produced by those modules. It does not rebuild or trust a report just because an individual module returned a positive eligibility flag.

## Exact controls

1. **Common source:** company code, fiscal year and source XLSX SHA-256 must be identical across all five candidates.
2. **Trial balance:** recomputes opening, debit, credit, closing and net movement totals from the complete account trace; requires the debit-net opening and closing totals and debit/credit movement difference to be zero.
3. **Balance sheet:** recomputes assets − liabilities − equity = 0 and compares the reported difference.
4. **Equity:** balance-sheet equity total must exactly equal the statement-of-changes-in-equity closing total.
5. **Profit:** income-statement net result must exactly equal the equity movement explicitly classified as `NET_PROFIT_LOSS`.
6. **Cash:** caller must select the exact BS asset note/subnote keys that represent cash and cash equivalents, with a separate evidence reference for each. Their presentation total must exactly equal direct cash-flow closing cash.
7. **Internal bridges:** recomputes P&L and equity arithmetic, and re-aggregates operating/investing/financing cash inflows/outflows from the individual classified cash-flow lines. Internal transfers are recomputed from line trace and must net to zero. Cash opening + net change = closing.
8. **Cash account trace:** every cash account in the direct cash-flow candidate must exist in the trial-balance trace; opening, debit turnover, credit turnover, closing and source-row lineage must match exactly. Transaction turnover differences and account roll-forward are recomputed, not trusted from summary fields. The cash account list and opening/closing totals must also reconcile.

All comparisons use exact Decimal values and zero tolerance. A missing note selection, duplicate BS note line, mismatched source hash, wrong scope, blocked upstream candidate or arithmetic mismatch makes the result ineligible.

## Example invocation

After the application has created all five typed candidates from the **same immutable workbook bytes**:

```python
from aram_backend.cross_statement_reconciliation import (
    CashBalanceNoteSelection,
    reconcile_cross_statements,
)

result = reconcile_cross_statements(
    balance_sheet=bs_candidate,
    income_statement=is_candidate,
    equity_changes=equity_candidate,
    cash_flow=cash_candidate,
    trial_balance=trial_balance_diagnostic,
    cash_balance_notes=[
        CashBalanceNoteSelection(
            statement_section="Current assets",
            note_number="C01",
            subnote_code="",
            evidence_ref="FINANCE-OWNER-CASH-NOTE-POLICY",
        ),
    ],
)
if not result.eligible_for_analyst_review:
    # Resolve every finding; never override or silently ignore it.
    print(result.findings)
```

The cash-note selection is an untrusted input. Its evidence reference is traceability, not authenticated approval. The caller must ensure that the selected BS notes include **all and only** cash and cash equivalents, including approved treatment of restricted cash and overdrafts.

## Interpretation and limits

`eligible_for_analyst_review=true` means the provided candidates, references and arithmetic tie out under their explicit user-supplied policies. It does **not** prove that the ledger, bank transactions, cash-account registry, mapping or note selection is complete or authentic.

The result permanently marks `source_ledger_completeness_verified=false`, `accounting_policy_authorized=false`, `independently_reviewed=false`, `trusted_approvals=false`, `official_financial_statement=false`, `export_authorized=false`, `releasable=false`.

No real accounting approval, statutory compliance, tax treatment, authenticated C1/C2/C3 review, database write, report export, GUI or installer is implemented by this gate. It is an engineering control only.

Run `cd backend && pytest -q tests/test_cross_statement_reconciliation.py` and full Backend CI. Synthetic candidate objects are used in tests; never place real financial files or approvals in public GitHub.
