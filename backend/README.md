# Financial Reporting Platform - Production Architecture (Phase 2A - Phase 9)

This repository contains the production-grade Financial Reporting Platform implementing persistent relational data storage, source document ingestion, financial data normalization, accounting calculation engine, statement review snapshot layer, financial reporting API layer, workflow orchestration, and containerized deployment infrastructure using Python, FastAPI, SQLAlchemy, and Pydantic.

## Prerequisites

- Python 3.12+
- `pip`
- Docker & Docker Compose (for production containerized deployment)
- PostgreSQL 15+ (for production database)

## Quick Start (Local Development)

1. **Install Dependencies**:

   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Initialize Database**:

   ```bash
   PYTHONPATH=. python3 backend/app/init_db.py
   ```

3. **Run Development Server**:

   ```bash
   PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000
   ```

   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/api/v1/health`

## Production Containerized Deployment (Docker)

To deploy Aram using Docker and Docker Compose with a production PostgreSQL database:

```bash
docker-compose up -d --build
```

### Environment Configuration

Override default environment variables in `.env` or system environment:

- `DATABASE_URL`: Production PostgreSQL URI (e.g. `postgresql://aram_user:aram_password@db:5432/aram_db`).
- `SECRET_KEY`: Production secret key for JWT token signatures.

## Database Migrations (Alembic)

Alembic manages database schema migration baselines:

```bash
# Apply migrations online
alembic upgrade head

# Generate a new migration revision
alembic revision --autogenerate -m "schema revision"
```

## Backup & Restore Operations

### PostgreSQL Backup:
```bash
docker exec -t aram-db-1 pg_dump -U aram_user aram_db > aram_backup_$(date +%Y%m%d).sql
```

### PostgreSQL Restore:
```bash
cat aram_backup_20260823.sql | docker exec -i aram-db-1 psql -U aram_user -d aram_db
```

## Running Regression Tests

Run the full automated test suite using `pytest`:

```bash
PYTHONPATH=. pytest -v backend/tests
```

## System Architecture Summary

1. **Core Relational Model (`backend/app/models/`)**: Persistent entities for Companies, FiscalYears, SourceDocuments, AccountVersions, MappingRules, NoteDefinitions, FinancialStatements, MappingTemplates, NormalizedFinancialRecords, ValidationErrorLogs, StatementSnapshots, Users, and AuditLogs.
2. **Ingestion Engine (`backend/app/ingestion/`)**: Immutable source document validation and SHA256 checksum tracking for `.xlsx`, `.csv`, and `.pdf` files.
3. **Normalization Engine (`backend/app/normalization/`)**: Converts raw rows into standardized transaction records with column mapping templates and validation logs.
4. **Accounting Engine (`backend/app/accounting/`)**: Rule-based calculation layer generating Trial Balance, Balance Sheet, and Income Statement foundations.
5. **Review Snapshot Layer (`backend/app/accounting/snapshot.py`)**: Stores frozen calculation JSON and manages review workflows (`DRAFT`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`).
6. **API & Security Layer (`backend/app/api/`)**: REST API with JWT authentication, role-based access control (`ADMIN`, `AUDITOR`, `VIEWER`), and structured audit logging (`AuditLog`).
7. **Workflow Orchestration (`backend/app/workflow/`)**: Automated E2E lifecycle tracking (`UPLOADED` -> `PROCESSING` -> `NORMALIZED` -> `CALCULATED` -> `READY_FOR_REVIEW` -> `APPROVED`).
