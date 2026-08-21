# Financial Reporting Platform - Backend Foundation (Phase 2A)

This backend application implements the persistent relational data model foundation for the Financial Reporting Platform using Python, FastAPI, SQLAlchemy, and Pydantic.

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
