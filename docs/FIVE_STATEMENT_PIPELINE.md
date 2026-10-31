# ARAM — five-statement pipeline orchestrator (NOT APPROVAL)

## Purpose

`aram_backend.five_statement_pipeline.build_five_statement_pipeline(...)` is the single in-memory orchestration entry point for the five read-only engines:

1. Balance sheet candidate
2. Income statement candidate
3. Statement of changes in equity candidate
4. Direct-method cash flow candidate
5. Trial balance diagnostic

It invokes the existing builders; it does not replace their policies or calculations.

## Snapshot guarantees

- `workbook_bytes` must be an immutable Python `bytes` object.
- The same bytes object is passed to all five builders.
- Input collections are frozen to tuples once at the boundary.
- The exact same frozen `NoteReference` tuple is passed to BS, IS and EQ.
- The cross-statement reconciliation is run after all five candidate objects are produced.
- If a candidate is blocked by a mismatch or missing transaction, the pipeline returns a blocked result with findings. Invalid workbook or policy preconditions raise `CoverageError`.

## Example

```python
from aram_backend.five_statement_pipeline import build_five_statement_pipeline

result = build_five_statement_pipeline(
    workbook_bytes,
    company_code="001",
    fiscal_year=1404,
    references=note_references,
    balance_sheet_policies=bs_policies,
    income_statement_policies=is_policies,
    equity_movement_policies=equity_policies,
    currency="IRR",
    unit="Rial",
    cash_accounts=cash_account_registry,
    counterpart_policies=counterpart_activity_policies,
    transactions=paired_cash_journal_lines,
    cash_balance_notes=selected_bs_cash_notes,
)

if not result.eligible_for_analyst_review:
    print(result.findings)

payload = result.to_dict()
```

The result exposes all five candidates, the cross-statement report, source hash, eligibility and findings. It permanently keeps source completeness, accounting authorization, independent review, trusted approvals, official statement, export and release flags false.

## Input responsibilities and limits

The caller still owns the correctness and completeness of the source workbook, references, statement sign policies, equity movement classifications, cash-account registry, counterpart classifications, transaction population and cash-note selection. Tuple freezing prevents collection mutation during orchestration; it does not authenticate the values.

This function is an in-memory library API, **not a desktop workflow or CLI**. It performs no filesystem access, database writes, posting, signing, approval, report export, GUI action or installer operation. No actual accounting-standard or statutory compliance is asserted.
