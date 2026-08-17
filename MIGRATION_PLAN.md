# MIGRATION PLAN

## Step 1: Quarantine Current Monolith
- Leave the patched `index.html` as a legacy artifact. Do not continue trying to stuff full production logic into it.

## Step 2: Set up the Backend
- Initialize a backend environment (e.g., Python FastAPI + SQLite).
- Create SQLAlchemy/Pydantic models based on `TARGET_DATA_MODEL.md`.

## Step 3: Implement Ingestion Engine
- Write modular Python scripts to parse the `data/*.xlsx` files and populate the database, strictly maintaining historical separation (1402, 1403, 1404).

## Step 4: Build Frontend Modules
- Scaffold a modern frontend framework.
- Implement the "Primary Financial Statements" view pulling from the API.
- Implement the "Financial Statement Notes" view pulling from the API.
- Implement the "Account Explorer" and drill-down layers.

## Step 5: Iterative Features
- Add Sorting/Materiality Rules UI.
- Add AI Change Assistant workflows.
- Implement Year Creation (1405).

*Immediate Next Step*: Await user approval on the Phase 1 Audit and Migration Plan before initiating Phase 2 (Persistent Data Model).
