# TARGET ARCHITECTURE

## Current State
- Monolithic HTML file (`index.html`) containing UI, state, and Data (`DB` object).
- Static Python parsers that mutate the HTML file directly.

## V2 Target State
The V2 directive requires a "Modular Architecture" (Section 64).

1. **Database Layer**: SQLite/PostgreSQL to store the `TARGET_DATA_MODEL`.
2. **Backend/API Layer (Python/FastAPI or Node.js)**:
   - Source Ingestion Service (parses Excel/CSV to DB).
   - Mapping Engine.
   - Financial Reconciliation Service.
   - AI Assistant Service.
3. **Frontend Layer (React/Vue or Modular Vanilla JS)**:
   - Clean separation of UI modules (Dashboard, Statements, Notes Explorer, Mapping Studio, Account Explorer).
   - Contextual overlay windows for drill-down.

## AI Integration
- AI suggestions must be stored as "Proposals" in the DB, not directly mutating source or data.
