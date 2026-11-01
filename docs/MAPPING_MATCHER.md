# Multi-dimensional mapping matcher

## Scope and status

This module classifies ledger rows against the canonical mapping rows. It is a read-only diagnostic, not an approval workflow and not a statement-generation input.

## Composite key

The matching dimensions are:
- Account code (`حساب` in ledger, `کد حساب` in mapping)
- `T1_CODE`
- `جاري / سرمایه ای`
- `T4_CODE`

The current `LedgerRecord` parser does not expose a `جاري / سرمایه ای` ledger field. The matcher therefore deliberately does **not** pretend that dimension was checked. Its current default matching contract only checks T1 and T4, and the JS mapping value is not yet accepted as a discriminator. This is a known integration blocker, not a verified full composite match.

Rule semantics implemented:
- Blank mapping dimension = wildcard.
- Populated mapping dimension = exact match required.
- A populated mapping dimension does not match a missing ledger dimension.
- Every source mapping row remains distinct; duplicate rows create ambiguity.
- No rule precedence, formula evaluation, or auto-approval.

## Exclusions and exposure

Account `8999` is excluded from the mapping-eligible denominator, consistent with the existing source-analysis decision. Its source row remains present in total source counts and source closing exposure. The exclusion is configurable at the API boundary.

## Required next gate

Before calling this production-ready, add the source ledger's approved current/capital classification field (if present) to `LedgerRecord`, verify the exact workbook header/value domain with an authorized source workbook, and run the full 252,898-row reconciliation. Do not interpret this preview as finance approval.

## Header consistency correction
The mapping workbook fixture uses `جاری / سرمایه ای` (Arabic/Persian yeh variants matter). The matcher now accepts the canonical spelling and its documented alternate spelling; this does not imply the ledger has a current/capital classification field. Populated current/capital mapping constraints continue to fail closed until an approved ledger-side source is available.
