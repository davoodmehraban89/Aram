# Aram backend

## Pilot workbook preflight

Gate 2A adds a strictly in-memory validator for the governed Pilot workbook.
Generate the approved blank template from the repository root with:

```bash
cd backend
PYTHONPATH=src python scripts/generate_pilot_template.py
```

Call `preflight_pilot_workbook(workbook_bytes)` from
`aram_backend.pilot_workbook`. The result reports every detectable error with
an exact sheet, Excel row, and field. The function does not persist inputs,
parsed values, mappings, or reports and never guesses a financial value.

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

## Personal Windows setup (local-only pilot)

In PowerShell, from the `backend` directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[test]'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn aram_backend.main:app --host 127.0.0.1 --port 8000
```

If `py` is not on PATH, use the installed Python 3.12 executable directly.
The default install uses plain `uvicorn`; optional optimized `uvicorn[standard]`
extras are available with `pip install -e '.[server-standard,test]'` when the
package index supplies compatible Windows wheels. WebSockets are not required
for the current HTTP-only pilot. Do not bind to `0.0.0.0` or expose this API
outside localhost until real authentication and deployment hardening are verified.
Passing tests does not authorize production financial processing or Gate 3 GO.
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
