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


## Phase 2B: Source Registration and Inspection

Phase 2B introduces metadata-only source registration and read-only source inspection:

*   **Metadata-only registration**: Registers exact file hashes and metadata for canonical fiscal documents.
*   **Idempotency & Rejection**: Exact-duplicate registrations (same hash, year, filename, and document type) are strictly idempotent. Semantic conflicts (differing filename or document type for an existing hash) are aggressively rejected via `SourceRegistrationError`.
*   **No Payload Persistence**: Source file bytes (e.g. XLSX/CSV payloads) are never persisted to the database.
*   **Supported Types**: Only `.xlsx` and `.csv` files representing `financial_statement`, `general_ledger`, `mapping`, or `trial_balance` are permitted.
*   **Read-only Inspection**: Safely inspects raw XLSX structural boundaries and parse general-ledger streams purely in-memory without modification of canonical data.
*   **Financial Safety**: Financial values, data cells, and mapping behaviors remain completely untouched.
