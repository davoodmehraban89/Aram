# Aram backend

Phase 2A provides the persistent, audit-safe data foundation. It deliberately
does not ingest spreadsheets, calculate financial values, or alter canonical
source files.

## Local setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
alembic upgrade head
uvicorn aram_backend.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. The health endpoint is
`GET /api/v1/health`; read-only schema catalogs are available at
`GET /api/v1/schema/entities` and `GET /api/v1/schema/enums`.

## Tests

```bash
cd backend
pytest
```

Tests use an isolated temporary SQLite database with foreign-key enforcement.
Runtime SQLite files are ignored by Git.

## Phase 2B: Source registration and inspection

Phase 2B adds metadata-only registration plus read-only inspection of supported
source documents.

- Supported file suffixes: `.xlsx` and `.csv`.
- Supported document types: `financial_statement`, `general_ledger`,
  `mapping`, and `trial_balance`.
- Registration stores the fiscal year, safe filename, document type, and SHA-256
  content hash. It does not persist source payload bytes.
- An exact duplicate—same fiscal year, content hash, safe filename, and document
  type—is idempotent and returns the existing `SourceDocument`.
- Reusing the same fiscal year and content hash with a different safe filename,
  document type, or both raises `SourceRegistrationError`. The existing record
  remains unchanged and no second record is created.
- XLSX structural inspection is read-only. General-ledger rows are parsed as
  typed in-memory records without changing the workbook.
- Phase 2B does not persist financial values, execute mappings, calculate
  balances, or modify canonical source files.
