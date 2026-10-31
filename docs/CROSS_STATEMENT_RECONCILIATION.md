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

1. **Common provenance:** company, fiscal year and source XLSX SHA-256 must match across all five candidates. BS, IS and EQ must also share one exact note-reference snapshot. Candidate eligibility must be a real boolean; nonempty findings or forged completeness/approval flags cannot be smuggled through.
2. **Balance sheet detail:** re-aggregates every BS presentation line by category from its source closing exposure and explicit sign multiplier. Recomputes assets − liabilities − equity = 0; duplicate note keys, negative presentation lines and summary/detail mismatches block.
3. **Income statement detail:** re-aggregates revenue, cost, operating expense, other income/expense and tax from individual presentation lines. Recomputes gross profit, operating profit, profit before tax and net result; the summary cannot pass if the underlying line amounts or sign policies differ.
4. **Equity detail:** re-aggregates account movements into note movements, component totals and movement categories. Recomputes opening + movement = closing at account, note, component and statement levels. Each EQ account's opening, debit, credit, closing, account name and source-row identity must match its exact trial-balance account.
5. **Trial balance:** recomputes each account's own opening + debit − credit = closing before aggregating totals. It also recomputes opening, debit, credit, closing and net movement totals from the full account trace; offsetting row errors cannot cancel to a green global total.
6. **Five-statement bridges:** BS equity must equal EQ closing; IS net result must equal the EQ movement explicitly classified as `NET_PROFIT_LOSS`. All comparisons use exact Decimal arithmetic and zero tolerance.
7. **Cash note policy:** caller must explicitly select the BS asset note/subnote keys that represent cash and cash equivalents, with separate evidence references. Their presentation total must equal direct cash-flow closing cash. Selection evidence is traceability, not authenticated approval.
8. **Cash-flow detail:** re-aggregates operating/investing/financing inflows and outflows from individual classified lines, recomputes internal transfers, and verifies opening + net change = closing.
9. **Cash account trace:** each registered cash account must exist in the TB trace. Transaction debit/credit turnovers are recomputed from cash-flow lines, including both sides of internal transfers, then tied to source turnover, opening/closing balances and source-row identity in TB.

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

## End-to-end integration test

`tests/test_five_statement_pipeline_integration.py` builds one synthetic Pilot XLSX and invokes the actual BS, IS, EQ, direct-CF and TB builders against the exact same workbook bytes. The synthetic ledger demonstrates:

- BS: assets 100 = liabilities 10 + equity 90
- IS: net result 20 = EQ net-profit movement 20
- EQ: opening 70 + movement 20 = closing 90
- CF: opening cash 40 + net change 10 = closing cash 50
- TB: opening and closing debit-net totals zero; debit and credit turnover both 60

A second test omits a cash transaction and verifies that the combined gate blocks. These are synthetic software tests, not evidence that a real ledger or bank transaction population is complete.

## Interpretation and limits

`eligible_for_analyst_review=true` means the provided candidates, references and arithmetic tie out under their explicit user-supplied policies. It does **not** prove that the ledger, bank transactions, cash-account registry, mapping or note selection is complete or authentic.

The result permanently marks `source_ledger_completeness_verified=false`, `accounting_policy_authorized=false`, `independently_reviewed=false`, `trusted_approvals=false`, `official_financial_statement=false`, `export_authorized=false`, `releasable=false`.

No real accounting approval, statutory compliance, tax treatment, authenticated C1/C2/C3 review, database write, report export, GUI or installer is implemented by this gate. It is an engineering control only.

Run `cd backend && pytest -q tests/test_cross_statement_reconciliation.py tests/test_five_statement_pipeline_integration.py` and full Backend CI. Synthetic candidate objects are used in tests; never place real financial files or approvals in public GitHub.
