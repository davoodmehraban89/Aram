# NOTE TO STATEMENT MATRIX

The relationship between Notes and Primary Financial Statements.
*Status: Domain Confirmation Required during data parsing.*

Based on standard Iranian accounting principles:
- **Income Statement (سودوزيان)**: Typically maps to notes concerning operating income, COGS, administrative expenses, other income/expenses (e.g., Notes 6, 7, ...).
- **Balance Sheet (وضعيت مالي)**: Maps to asset notes (tangible, intangible, receivables, inventory, cash) and liability/equity notes (payables, provisions, capital).
- **Cash Flow (جريان هاي نقدي)**: Maps to operational cash flow notes, capital expenditure notes.

*Action for Phase 3*: Extract the exact references inside the `سودوزيان` and `وضعيت مالي` sheets (usually column C or D contains the Note Reference number) to build the definitive matrix programmatically.
