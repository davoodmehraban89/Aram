# V1 Pilot Workbook Contract v0.1

This contract governs the blank Pilot input and mapping workbook. The approved
artifact is `samples/Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx`; it is not
canonical financial data and contains no sample financial values.

## Sheets and exact header order

| Sheet | Exact headers |
|---|---|
| Company | `company_code`, `company_name`, `fiscal_year`, `currency`, `unit`, `prepared_by`, `status` |
| Accounts | `company_code`, `fiscal_year`, `general_code`, `general_name`, `subsidiary_code`, `subsidiary_name`, `detail1_code`, `detail1_name`, `detail2_code`, `detail2_name`, `detail3_code`, `detail3_name`, `detail4_code`, `detail4_name`, `account_full_code`, `account_name`, `opening`, `debit`, `credit`, `closing`, `source_row`, `row_status`, `closing_delta` |
| Notes | `company_code`, `fiscal_year`, `statement`, `statement_section`, `note_number`, `note_title`, `subnote_code`, `subnote_title` |
| Mapping | `mapping_id`, `company_code`, `fiscal_year`, `account_full_code`, `account_level`, `general_code`, `subsidiary_code`, `detail1_code`, `detail2_code`, `detail3_code`, `detail4_code`, `target_statement`, `statement_section`, `note_number`, `subnote_code`, `mapping_version`, `approval_status`, `reviewer`, `review_date`, `source`, `notes`, `validation_status` |
| Test_Log | `tester`, `feature`, `expected_result`, `actual_result`, `status`, `severity`, `evidence`, `notes` |
| Checks | `check_code`, `check_name`, `status`, `affected_rows`, `details` |
| Guide_FA | `section`, `instruction` |
| Lists | `list_name`, `value` |

Every sheet and the exact order above is mandatory. Entirely blank data rows are
ignored. In a populated row, fields required by the validator are:

- Company: `company_code`, `company_name`, `fiscal_year`, `status`.
- Accounts: company/year, general code/name, full code/name, four financial
  source values, `source_row`, and `row_status`.
- Notes: company/year, statement, note number, and note title.
- Mapping: mapping ID, company/year, account code/level, positive mapping
  version, and approval status.

Other fields are optional in v0.1. Fiscal years, mapping versions, and source
rows are positive integers. Financial source fields are finite decimal values;
NaN, Infinity, booleans, and formulas are invalid. Every code field is Excel
text. Numeric code cells are rejected rather than coerced, preserving leading
zeros.

## Lifecycle and relationships

- Company status: `Draft`, `Approved`, `Locked`.
- Accounts row status and Mapping approval status: `Draft`, `Reviewed`,
  `Approved`. Preflight validates but never advances a status.
- `(company_code, fiscal_year)` is unique in Company. Accounts, Notes, and
  Mapping must reference it exactly; no cross-company or cross-year fallback is
  allowed.
- `(company_code, fiscal_year, account_full_code)` is unique in Accounts.
- `mapping_id` is globally unique in the workbook. Each mapping account must
  exist in Accounts for the same company and year. Unknown accounts are errors;
  mappings are never guessed.

## Validation report

The in-memory API returns `valid`, deterministic `issues`, and counts by
severity. Every issue has `severity`, `code`, `sheet`, one-based Excel `row`,
`field`, and `message`. It collects all detectable structural and row-level
errors rather than stopping at the first.

`closing_delta` means only `opening + debit - credit - closing`. A non-zero
result is a validation error. It is not a financial-statement calculation, does
not replace any source value, and is never persisted.

## Safety boundary and artifact hash

Preflight reads supplied bytes in memory. It does not write workbook bytes,
parsed rows, financial values, mappings, or validation reports; it never guesses
or mutates values. The template generator reads no canonical file.

Committed template SHA-256: `e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f`.
