# Financial Reporting Platform - Backend Foundation & Ingestion Engine (Phase 2A & 2B)

This backend application implements the persistent relational data model foundation and controlled financial source ingestion engine for the Financial Reporting Platform using Python, FastAPI, SQLAlchemy, and Pydantic.

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

- **Parsers (`backend/app/ingestion/parsers.py`)**: Supports format validation and SHA256 checksum computation for `.xlsx`, `.csv`, and `.pdf` files without mutating raw source files.
- **Service Layer (`backend/app/ingestion/service.py`)**:
  - `validate_source(file_path)`: Validates file existence, format support, and computes file hash.
  - `register_source_document(db, year_id, file_path, doc_type)`: Verifies fiscal year mutability, checks for duplicate document hashes, and records a `SourceDocument`.
  - `process_import(db, year_id, file_path, doc_type)`: Orchestrates document registration, status tracking (`REGISTERED` -> `PROCESSED`), and metadata extraction.

## Running Tests

Run the full automated test suite using `pytest`:

```bash
PYTHONPATH=. pytest -v backend/tests
```

## Data Model Core Entities

- **Company**: Corporate entity metadata (`code`, `name`).
- **FiscalYear**: Year context (`year`, `status`: `Draft`, `Approved`, `Locked`).
- **SourceDocument**: Metadata for imported ledger/statement files (`file_hash`, `processing_status`, `version`).
- **AccountVersion**: Fiscal-year isolated Chart of Accounts.
- **MappingRule**: Mapping rules linking accounts to note definitions.
- **NoteDefinition** & **NoteRow**: Financial note definitions and structural line items.
- **FinancialStatement** & **StatementLine**: Primary financial statement headers and line items.
