## 2026-11-01 — composite mapping matcher (DRAFT)
- Added an isolated matcher for account + T1 + T4 with explicit wildcard semantics, source row trace, duplicate-rule ambiguity and 8999 scope exclusion.
- The source ledger parser does not expose a current/capital field, so the JS dimension is intentionally not applied. Full four-dimensional matching is NOT claimed.
- Added synthetic unit tests for wildcard/exact matching, missing dimensions, duplicates, exclusion, Decimal exposure, malformed rules and source row identity.
- Full real-workbook run and finance-owner approval remain blocked pending exact source-field validation.
