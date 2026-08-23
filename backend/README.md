# Financial Reporting Platform - Production Architecture (Phase 2A - Phase 12)

This repository contains the production-grade Financial Reporting Platform implementing persistent relational data storage, source document ingestion, financial data normalization, Chart of Accounts mapping engine, accounting calculation engine, statement review snapshot layer, financial reporting API layer, workflow orchestration, and containerized deployment infrastructure using Python, FastAPI, SQLAlchemy, and Pydantic.

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

## Chart of Accounts Mapping Engine (Phase 12)

The COA Mapping Engine under `backend/app/normalization/mapping_engine.py` prepares real financial ledger files for accountant testing:

- **Unmapped Account Detection**: `detect_unmapped_accounts()` identifies account codes without approved mapping rules and provides automated classification suggestions based on Iranian accounting standard heuristics.
- **Rule Management & Review Workflow**: `save_mapping_rule()` records or updates approved mapping rules (`COAMappingRule`) for a fiscal year.
- **Template Reuse**: `copy_template_from_year()` copies approved mapping rules from prior fiscal years (e.g. 1402 -> 1403) while maintaining strict company and fiscal year isolation.
- **Account Hierarchy Classification (`backend/app/ingestion/ledger_validator.py`)**: Classifies accounts into General Ledger (کل), Subsidiary Ledger (معین), and Detail levels 1-4 (تفصیل ۱-۴) based on code structure.

## API Endpoints for COA Mapping Engine

- `GET /api/v1/coa/unmapped`: Detects unmapped accounts for a fiscal year.
- `POST /api/v1/coa/rules`: Saves or approves a Chart of Accounts mapping rule.
- `POST /api/v1/coa/copy-template`: Copies approved mapping rules from a previous fiscal year.

## Running Tests

Run the full automated test suite using `pytest`:

```bash
PYTHONPATH=. pytest -v backend/tests desktop/tests
```

## System Architecture Summary

1. **Core Relational Model (`backend/app/models/`)**: Persistent entities for Companies, FiscalYears, SourceDocuments, AccountVersions, MappingRules, COAMappingRules, NoteDefinitions, FinancialStatements, MappingTemplates, NormalizedFinancialRecords, ValidationErrorLogs, StatementSnapshots, Users, and AuditLogs.
2. **Ingestion Engine (`backend/app/ingestion/`)**: Immutable source document validation, SHA256 checksum tracking, and real Excel/CSV ledger structure validation.
3. **Normalization & Mapping Engine (`backend/app/normalization/`)**: Standardizes transaction records, detects unmapped accounts, and manages rule templates per fiscal year.
4. **Accounting Engine (`backend/app/accounting/`)**: Rule-based calculation layer generating Trial Balance, Balance Sheet, and Income Statement foundations.
5. **Review Snapshot Layer (`backend/app/accounting/snapshot.py`)**: Stores frozen calculation JSON and manages review workflows (`DRAFT`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`).
6. **API & Security Layer (`backend/app/api/`)**: REST API with JWT authentication, role-based access control (`ADMIN`, `AUDITOR`, `VIEWER`), and structured audit logging (`AuditLog`).
7. **Workflow Orchestration (`backend/app/workflow/`)**: Automated E2E lifecycle tracking (`UPLOADED` -> `PROCESSING` -> `NORMALIZED` -> `CALCULATED` -> `READY_FOR_REVIEW` -> `APPROVED`).
