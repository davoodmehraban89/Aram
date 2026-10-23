# ADR-012: Excel-first V1, provider-neutral integrations later

Status: PROPOSED
Date: 2026-10-23
Baseline: source-data-cleanup at 7dc864fd032f0c4ae4d650d89304a01286a6d914

## Decision

The owner confirms that the first intended accounting integration is Peyvast, used by Iran Gas Transmission Company. Later integrations may include Rahkaran, Sepidar, and other vendors. V1 remains the existing governed Excel/CSV Pilot. There is no live database connector in V1.

Keep source acquisition separate from normalization, preflight, mapping, reconciliation, statement generation and approved exports. A future vendor adapter must translate authorized vendor records to a versioned provider-neutral source snapshot. Reporting logic must not depend on vendor table names.

The first future adapter is Peyvast, subject to checking the actual product version, supported API/export/database interface, authorization and schema documentation. No database engine or table structure is assumed. Each other vendor needs its own adapter and compatibility tests.

Future source access must be read-only and least-privilege, with credentials outside source control, company/year isolation, audit records, idempotent import, replay safety and source freshness monitoring. A worker for periodic or incremental sync would run independently of the Windows UI. Never claim instantaneous updates without measuring lag. A complete snapshot remains the fallback when reliable incremental changes are unavailable.

Draft reports may refresh automatically, but issued statements must be versioned and protected by explicit review. AI mapping suggestions must not silently change financial mappings.

## V1 non-goals

No live Peyvast connection, vendor-specific SQL, secrets, background polling service, cloud hosting, database writes, or change to protected canonical financial data. Windows-first offline delivery remains the initial target.

## Future activation checks

Verify approved vendor access and schema; define normalized snapshot version and provenance; test duplicates, corrections, deletes, partial reads, stale checkpoints, year isolation, failures and replay; compare authorized anonymized Excel and connector output; then implement and review each adapter as a separate task.

## Rollback

Close the draft PR without merging. This decision record changes no runtime code or financial records.
