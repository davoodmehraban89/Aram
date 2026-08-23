# Financial Reporting Platform - Backend Architecture (Phase 2A - Phase 4A)

This backend application implements the persistent relational data model, source document ingestion, financial data normalization, and accounting rule engine foundation for the Financial Reporting Platform using Python, FastAPI, SQLAlchemy, and Pydantic.

## Prerequisites

- Python 3.10+
- `pip`

## Quick Start

1. **Install Dependencies**:

   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Initialize Database**:

   By default, SQLite is used for local development (`financial_platform.db`).

   ```bash
   PYTHONPATH=. python3 backend/app/init_db.py
   ```

3. **Run Backend Server**:

   ```bash
   PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000
   ```

   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/api/v1/health`

## Environment Configuration

Environment variables can be overridden via system environment or a `.env` file:

- `DATABASE_URL`: SQLAlchemy connection URI (default: `sqlite:///./financial_platform.db`). Can be replaced with a PostgreSQL URI (e.g., `postgresql://user:pass@localhost:5432/financial_db`) for production.

## Ingestion Engine (Phase 2B)

The ingestion module under `backend/app/ingestion/` provides controlled financial source document importing:

- **Parsers (`backend/app/ingestion/parsers.py`)**: Format validation and SHA256 checksum computation for `.xlsx`, `.csv`, and `.pdf` files without mutating raw source files.
- **Service Layer (`backend/app/ingestion/service.py`)**: `validate_source()`, `register_source_document()`, and `process_import()`.

## Normalization Engine (Phase 3)

The normalization module under `backend/app/normalization/` converts ingested source data into standardized financial records:

- **Analyzer (`backend/app/normalization/analyzer.py`)**: Detects column headers and analyzes tabular file structure.
- **Mapper (`backend/app/normalization/mapper.py`)**: Translates raw row data into normalized attributes (`account_code`, `account_name`, `debit`, `credit`, `net_amount`, `t1`-`t4`).
- **Validator (`backend/app/normalization/validator.py`)**: Enforces required field validation, non-negative monetary constraints, and generates `ValidationErrorLog` records.
- **Service Layer (`backend/app/normalization/service.py`)**: `normalize_and_persist_records()`.

## Accounting Rule Engine Foundation (Phase 4A)

The accounting module under `backend/app/accounting/` performs rule-based calculations on normalized financial records:

- **Rules (`backend/app/accounting/rules.py`)**: Configurable account grouping rules (`AccountGroupRule`, `AccountingRuleConfig`).
- **Calculator (`backend/app/accounting/calculator.py`)**: Debit/credit aggregation and account classification logic.
- **Statements (`backend/app/accounting/statements.py`)**: Foundation generators for Trial Balance (TB), Balance Sheet (BS), and Income Statement (IS).
- **Service (`backend/app/accounting/service.py`)**: `generate_financial_statements()`.

## Running Tests

Run the full automated test suite using `pytest`:

```bash
PYTHONPATH=. pytest -v backend/tests
```

## Data Model Core Entities

- **Company**: Corporate entity metadata (`code`, `name`).
- **FiscalYear**: Year context (`year`, `status`: `Draft`, `Approved`, `Locked`).
- **SourceDocument**: Metadata for imported ledger/statement files.
- **AccountVersion**: Fiscal-year isolated Chart of Accounts.
- **MappingRule**: Mapping rules linking accounts to note definitions.
- **NoteDefinition** & **NoteRow**: Financial note definitions and structural line items.
- **FinancialStatement** & **StatementLine**: Primary financial statement headers and line items.
- **MappingTemplate**: Custom column header mapping definitions.
- **NormalizedFinancialRecord**: Standardized financial transaction/account row records.
- **ValidationErrorLog**: Log of data validation errors and warnings.
