# TARGET DATA MODEL (High Level)

Based on Directive Section 65, the system requires a persistent relational or document model.

## Core Entities
- **Company**: `id, code, name`
- **FiscalYear**: `id, company_id, year, status (Draft, Approved, Locked)`
- **SourceDocument**: `id, year_id, filename, file_hash, type, upload_date`
- **AccountVersion**: `id, year_id, account_code, account_name, t1, t2, t3, t4, nature`
- **MappingRule**: `id, year_id, account_code, target_note_id, mapping_type`
- **NoteDefinition**: `id, year_id, note_number, title, configuration_json`
- **NoteRow**: `id, note_id, row_order, label, formula_logic, sorting_rule_id`
- **FinancialStatement**: `id, year_id, type (BS, IS, CF, EQ)`
- **StatementLine**: `id, statement_id, line_label, target_note_id, mapped_total`

*Note: This architecture implies moving away from storing data in a single JavaScript object in `index.html`.*
