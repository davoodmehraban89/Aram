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

