# V1 Pilot Workbook Contract v0.1

This document governs the strictly structured V1 Pilot workbook format. It outlines the schema, validation rules, and cross-sheet relationships to ensure audit-safe processing and strict determinism.

## 1. Required Sheet Names and Header Order

The workbook must contain exactly the following sheets, with headers occurring exactly in this order.

### `Company`
1. `company_code` (Text, Required)
2. `company_name` (Text, Required)
3. `fiscal_year` (Integer, Required)
4. `status` (Text, Required: Draft, Reviewed, Approved)

### `Accounts`
1. `company_code` (Text, Required)
2. `fiscal_year` (Integer, Required)
3. `account_code` (Text, Required, Unique within company/year)
4. `account_name` (Text, Required)
5. `t1_code` (Text, Optional)
6. `t2_code` (Text, Optional)
7. `t3_code` (Text, Optional)
8. `t4_code` (Text, Optional)
9. `nature` (Text, Optional)
10. `opening` (Decimal, Required)
11. `debit` (Decimal, Required)
12. `credit` (Decimal, Required)
13. `closing` (Decimal, Required)

### `Notes`
1. `company_code` (Text, Required)
2. `fiscal_year` (Integer, Required)
3. `note_number` (Text, Required, Unique within company/year)
4. `title` (Text, Required)
5. `row_order` (Integer, Required)
6. `label` (Text, Required)

### `Mapping`
1. `company_code` (Text, Required)
2. `fiscal_year` (Integer, Required)
3. `mapping_id` (Text, Required, Unique within company/year)
4. `account_code` (Text, Required)
5. `note_number` (Text, Required)
6. `mapping_type` (Text, Required)

### `Test_Log`
1. `test_id`
2. `description`
3. `result`

### `Checks`
1. `check_name`
2. `status`

### `Guide_FA`
Contains instructional text in Persian guiding the user on how to populate the workbook.

### `Lists`
Contains valid dropdown values for fields like `status` and `mapping_type`.

## 2. Constraints and Rules

### 2.1 Lifecycle/Status Values
The `status` field in the `Company` sheet must be exactly one of: `Draft`, `Reviewed`, `Approved`. The validation engine checks this value but never advances or mutates it.

### 2.2 Company/Year Isolation
All cross-sheet lookups and validations are strictly scoped by the composite key of `company_code` + `fiscal_year`.
- Every row in `Accounts`, `Notes`, and `Mapping` must correspond to a defined `company_code` + `fiscal_year` present in the `Company` sheet.

### 2.3 Cross-Sheet Keys & Duplicate Rules
- **Accounts:** `account_code` must be unique per `company_code` + `fiscal_year`.
- **Notes:** `note_number` must be unique per `company_code` + `fiscal_year`. (Duplicate rows for the same note are allowed if `row_order` varies, representing note lines).
- **Mapping:** `mapping_id` must be unique per `company_code` + `fiscal_year`. `account_code` referenced here must exist in the `Accounts` sheet for the same company/year.
- **Unknown Accounts:** Any mapping row referencing an `account_code` not found in `Accounts` will be reported as an error. The system will *never* silently ignore them or guess values.

### 2.4 Financial Validation & `closing_delta`
The validator will compute `closing_delta = opening + debit - credit - closing` using strict Decimal arithmetic.
- A non-zero `closing_delta` is reported as a validation error.
- This calculation is strictly for validation. The system must *never* mutate source values, force balances, or treat this calculation as a financial statement rollup.

### 2.5 Validation Error Schema
Errors must be collected deterministically and reported comprehensively (no fail-fast). The error schema is:
- **Severity**: e.g., `ERROR`, `WARNING`
- **Code**: e.g., `MISSING_FIELD`, `DUPLICATE_KEY`, `INVALID_TYPE`, `UNKNOWN_ACCOUNT`, `NON_ZERO_DELTA`
- **Sheet**: Name of the sheet
- **Row**: 1-indexed Excel row number
- **Field**: The column header name
- **Message**: A descriptive error message

### 2.6 Immutability and No-Persistence Boundary
- The preflight validation API is read-only. It operates entirely in memory.
- It must *never* write to the database.
- It must *never* alter the uploaded workbook bytes.
- It must *never* perform automated corrections or silent guessing.
