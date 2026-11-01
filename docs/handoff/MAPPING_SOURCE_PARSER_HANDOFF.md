## 2026-11-01 — read-only mapping source parser (DRAFT)
- New branch `codex/aram-mapping-source-parser-20261101`, based on PR #80 exact head `919c3c2988153124543fbb2f8bf4b91b5771067b`.
- Adds a streaming parser for the canonical mapping workbook's existing `Data` sheet profile. It preserves source row numbers, formula text and all raw source columns; it does not evaluate formulas, infer precedence, or match ledger rows.
- Synthetic parser tests cover required fields, blank rows, original row identity, dimension preservation, duplicate source rows and formula non-evaluation.
- This is an ingestion boundary only. Composite matching, exact real-workbook header/value validation, full source reconciliation and finance-owner policy approval remain open. No canonical source files, database records, accepted branch or official outputs changed.
