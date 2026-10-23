# Aram: Peyvast source connector and governed mapping requirements

Prepared 2026-10-23. Design and acceptance note only; no implementation, repository change, source access, database change, provisioning, or accounting decision is authorized by this document.

## Purpose and evidence boundary

Aram must accept accounting data from Peyvast (پیوست) and Excel through a shared canonical representation, then let an authorized user create and maintain explicit mappings with reviewable changes and reliable recovery. Source accounting systems and supplied workbooks remain read-only. Imported snapshots and mapping decisions belong to Aram; neither is written back to Peyvast or the source workbook.

The official vendor accounting FAQ supplied for this task, [payvast.com/نرم-افزار-حسابداری/](https://payvast.com/نرم-افزار-حسابداری/), identifies Microsoft SQL Server as the default database, mentions SQL Server 2019/2022, and recommends 2022. This is vendor product guidance, not evidence of the customer's installation. The customer's Peyvast edition/build, SQL Server version, database topology, schema, supported extraction interface, credentials, and network access are unknown. No vendor table or column names, connection strings, credentials, or accounting rules are specified or inferred here.

Repository reference: `davoodmehraban89/Aram`, accepted baseline `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`, inspected in the task workspace. GitHub remote PR metadata and diffs were read on 2026-10-23. This is a time-bound design snapshot, not an acceptance decision or evidence of later branch state.

## What exists and what remains

| Area | Observed baseline or candidate | Remaining requirement |
| --- | --- | --- |
| Fiscal-year model | Baseline has companies, company/year identity, year-owned records, version fields, Draft/Approved/Locked lifecycle, and mutation guards. | Close and independently verify the separate P0 isolation work before extending persistence. Do not assume every foreign-key relationship or reparenting path is isolated because an entry point validates it. |
| Source provenance | Baseline source registration stores year, filename, type, content SHA-256, and upload time; identical registration is idempotent. Source bytes and parsed financial records are not persisted. | Database snapshot provenance, canonical source snapshots, durable row lineage, reproducibility, and cross-input equivalence are not implemented. |
| Excel input | Baseline reads XLSX structure and typed ledger records in memory. Pilot preflight validates a governed workbook with hierarchy, company/year, target, and review fields. | A Pilot preflight is not a live connector, persisted import, mapping editor, or approval service. The legacy ledger parser and Pilot contract have different shapes and require explicit adapters. |
| Mapping persistence | [Draft PR #26](https://github.com/davoodmehraban89/Aram/pull/26), head `185e47f031902a8918c93c8dbb420122e7408403`, is open and unmerged. Its service requires a Draft year, existing same-year account and note, explicit identifiers, and rejects conflicting content at an existing rule/version. Identical service replay returns the existing row. | Account-code-only mapping lacks the required full hierarchical predicate. An integer version does not provide an approved change workflow, active-version policy, audit history, or rollback by itself. |
| Mapping XLSX | [Draft PR #27](https://github.com/davoodmehraban89/Aram/pull/27), head `6c0068a660a3834f042b89d41d62bba82cb3a498`, is open and unmerged, stacked on #26. It parses/exports a five-column Mapping sheet, rejects formulas and oversized archives, and stages imports atomically under caller transaction control. | Its preview is parsing only: no stored old/new diff, authorization, approval, or stale-preview token. It rejects every repeated rule-key/version inside a workbook, including identical repeats, which conflicts with the requested no-op semantics. Its raw note IDs and five-column shape do not cover the governed Pilot hierarchy/target contract. |
| Peyvast | No live Peyvast connector was identified in the inspected baseline. | Customer-specific, read-only extraction, documented translation, and customer-verified reconciliation remain blocked on the facts below. |

The PR descriptions and test files are implementation evidence, not acceptance or current-CI evidence. This note does not claim either candidate passes its latest CI or is safe to merge. Candidate work must be reconciled with the isolated model and independently reviewed at its exact final head.

## Source approach

Recommended order:

1. Ask the customer/vendor for an official supported read interface: documented read-only views, an export interface, or an API, if available. Prefer a supported interface that exposes the required data and stable identifiers, and assess its authentication, licensing, consistency, and change guarantees. The existence of such an interface is unconfirmed.
2. If no adequate supported interface exists, use documented customer tables through a customer-approved, least-privilege read account. First obtain schema documentation, representative redacted samples, key relationships, version information, and an approved query/extraction contract. Build against those facts; do not infer joins from similarly named fields.
3. Keep Excel as a first-class input route for initial onboarding, disconnected operation, comparison, and mapping exchange. It must feed the same validation and mapping services as the database route.

A direct table connector offers access to customer detail but is more sensitive to schema changes and transaction semantics. A supported interface reduces coupling when its guarantees are sufficient. These are proposed integration choices, not a claim that Peyvast publishes either interface. Aram's internal application database is a separate concern; the vendor's SQL Server choice does not require moving Aram's own storage or provisioning another provider.

## Shared canonical contract

Define and version a canonical input contract before writing an adapter. Names below are Aram concepts, not Peyvast schema names.

- **Scope:** explicit company identity, explicit fiscal-year identity/calendar and source-to-Aram identity mapping. Identical account codes in different companies or years are distinct. No default company or fallback year is allowed.
- **Account and hierarchy:** stable source account identifier when available, literal text code/name, account level, general/subsidiary hierarchy, and ordered detail/dimension identifiers with their parent context. The current Pilot has detail1 through detail4; the customer's actual meaning and available depth must be confirmed. Preserve missing, explicit empty, and exact-match values distinctly where the approved predicate model needs that distinction.
- **Source facts:** source record key or a documented row locator, original codes, source year/period, row/document type, supplied amounts as exact decimals, currency and unit, and extraction locator. Retain the original source meaning; no inferred balances, sign changes, scale conversion, synthetic codes, target classification, or hierarchy is introduced by an adapter.
- **Provenance:** immutable snapshot ID, connector/input type, customer installation identifier, company/year filter, extraction start/end UTC, supplied as-of/cutoff, interface/schema version, adapter and canonical-contract versions, query/export contract identifier and parameters without secrets, row counts, and deterministic snapshot/content hashes. For Excel retain file SHA-256, sheet/header/row references; for database rows retain documented source keys and extraction boundaries.
- **Validation:** one shared validation report identifies scope, source locator, field, severity, and stable reason code. Unknown accounts, unresolved targets, incomplete hierarchy, and ambiguous matches stay visible and block affected application; they do not cause target inference.

Database extraction must describe how a consistent view is obtained with the customer's existing supported isolation or backup/export facility. Read-only extraction must not silently enable SQL Server settings, create database objects, modify source data, or change grants. If a consistent snapshot cannot be established, record that limitation and reject acceptance as a reproducible accounting snapshot. Persist a completed snapshot only after extraction and validation complete; failure must not publish a partial snapshot.

DB and Excel adapters must produce equivalent canonical records when supplied equivalent facts. Preserve literal code text and leading zeros; any normalization requires a documented reversible rule and keeps raw values. Do not equate unknown/null with a wildcard. Source identity and canonical content hashing must distinguish legitimate separate records with equal amounts from accidental replay. Changes in source data create a new immutable snapshot rather than rewriting earlier evidence.

## Governed mapping model and workflow

### Identity and scope

A mapping has a stable Aram rule identifier within company/year, a versioned source predicate, and explicit target identifiers. Its predicate includes account identity, account level, applicable hierarchical dimensions, and any other customer-approved discriminator. Its target resolves to the same company's same fiscal year's permitted statement/section/note/subnote structure. A friendly exported target label is accompanied by a stable scoped identifier; import never guesses a target from a label or treats a foreign installation's raw database row ID as portable.

The full predicate and target are part of equality, change detection, audit, and approval. Define missing/exact/explicit-any semantics in a versioned contract. Do not choose most-specific, first-match, or another precedence policy to resolve overlaps without an approved accounting rule. Several explicitly approved rules may be legitimate; overlapping rules with unresolved precedence produce an ambiguity, not automatic classification. Account names are display evidence, not unique identity.

### One path for XLSX and manual edits

Initial/bulk XLSX import and manual create/edit submit the same canonical mapping proposal. To create an applicable proposal, the service validates the actor's company/year permissions and Draft-year state, validates the source predicate and target, reads the current active mapping revision, and computes a persisted preview before application. Separately authorized diagnostic comparison is permitted for Approved/Locked years, but it cannot issue an applicable approval token or become an applicable proposal. Source workbook fields such as `reviewer` or `approval_status` are historical evidence, not authentication or authority to approve inside Aram.

Each input row is classified as **new**, **unchanged**, **changed**, **conflicting duplicate**, or **invalid**, with original row locators and deterministic counts. Proposed no-op behavior is mandatory:

- Repeating a stored mapping with identical predicate and target leaves active mapping state and mapping version unchanged.
- Repeating the same identical mapping within one input is coalesced; report all repeated row locators and count them as unchanged/coalesced, with at most one prospective creation when the rule is new.
- Repeating an identity with different content within one input is a conflict. Show the competing rows and their differences; never choose first or last. No apply is allowed until the proposal is corrected.
- A changed stored mapping displays its complete old and proposed predicate/target, scope, and version. It requires explicit approval from an authorized user before application. Proposed design choice: require the same approval for new rows, including a new-only initial batch, so every nonempty delta has one reviewable meaning.
- Existing mappings absent from an input remain active and unchanged. Removal is a separate explicit, versioned, authorized action; an empty or partial file is never a request to delete existing mappings.

Preview stores a proposal ID, canonical input hash, actor and scope, source file/proposal provenance, relevant source snapshot and catalog revisions, baseline active-mapping revision, old/new values, validations and counts, and creation/expiry state. Persisting a preview does not change active mappings. Editing a preview creates a new proposal and invalidates its earlier approval.

Apply first rechecks authorization. For a proposal already successfully applied, return its recorded result without mutation, even if that application advanced the revision or the year later became protected; this is retrieval of an earlier outcome, not another application. For an unapplied proposal, recheck Draft state, proposal integrity, target/account validity, and every relevant baseline revision inside a transaction. Use an optimistic compare-and-set of the mapping revision together with the atomic write. A concurrent mapping edit, relevant catalog/predicate change, or year transition after preview makes the unapplied proposal stale: reject all changes and require a fresh diff and approval. Never refresh the preview invisibly under the previous approval. Use a consumed-proposal/idempotency key so retried application returns the same outcome without another version or event representing a new change.

Proposed batch behavior: a proposal with any invalid/conflicting row cannot apply. Approval covers the displayed nonempty delta exactly, and the transaction applies all approved changes or none. Unchanged rows do not create mapping versions. A separate audit event may record a no-op import attempt without changing mapping state.

### Audit, versions, and recovery

Persist an append-only record of proposal, approver identity/time, exact before/after state, company/year, active revision before/after, reason, source file/proposal hash, and relevant snapshot/catalog versions. Record failures and stale rejection without changing active state. Separate author and approver is configurable only if the customer's role policy calls for it; authenticated authorization and explicit change approval are required in all cases.

Keep superseded mapping versions and a clear active revision. Rollback is a new authorized proposal showing the current state and the historical state to restore; it creates a new auditable revision rather than deleting history or decrementing a version counter. It is subject to the same scope, target validity, stale-preview and protected-year rules. Historical outputs remain linked to the exact source snapshot and mapping revision used to produce them.

## Acceptance scenarios

Use isolated synthetic fixtures for behavioral tests; do not alter canonical XLSX/PDF, `data/`, customer databases, or financial source values. Real integration acceptance later requires customer-supplied evidence and an approved extraction contract.

| Scenario | Required observable outcome |
| --- | --- |
| Equivalent database and Excel facts | Both adapters yield the same scoped canonical facts and validation results; each retains its own source lineage and immutable snapshot provenance. |
| Customer database access | The account can read only approved objects and cannot write or perform DDL. Extraction executes only the documented reads; no settings, grants, or source objects change. |
| Snapshot changes during extraction | A supported consistent extraction produces one stated as-of snapshot, or extraction fails/reports inconsistency and no completed snapshot is published. |
| Same codes in company A/B or year 1403/1404 | Imports, lookups, notes, mappings, approvals, rollback, and outputs cannot cross scope. Unknown scope is rejected; no fallback occurs. |
| Same account, different hierarchy/detail | Distinct predicates remain distinct. Missing dimension, explicit-any and literal value do not collapse into the same predicate. Unresolved overlap is reported. |
| Leading-zero code and raw source text | Codes survive DB/Excel normalization and round-trip without numeric coercion; raw provenance is recoverable. |
| Exact stored replay | Zero active-state changes, zero additional mapping versions, unchanged active revision. |
| Repeated identical new rows inside XLSX | One proposed new mapping, repeated row locators reported, one mapping after apply. Reimport is a no-op. |
| Conflicting repeated identity | Every competing input row is identified, differences are visible, and the entire proposal cannot apply. |
| Existing target or predicate changes | Old/new values are visible before write; an unauthorized actor or missing approval cannot apply; authorized approval creates one new auditable revision. |
| Partial/empty input | No existing mapping is deleted or retired. A no-op/empty-result message is explicit. |
| Concurrent edit after preview | The older approval attempt is rejected as stale with zero partial changes; a new preview displays the current baseline. Test with two transactions. |
| Year approved/locked after preview | Apply rejects without mutation. Existing Approved/Locked years reject edits, additions, retirement and rollback. Read-only preview remains separately authorized. |
| One invalid row in a mixed batch | No active mapping changes survive; caller errors and retry cannot leave a partial import. |
| Lost response and apply retry | The same approved proposal returns its prior result, with one active revision and no duplicated application. |
| Explicit rollback | A new approved revision restores the chosen permitted historical state; intervening history, approval evidence, source snapshots and past output lineage remain intact. |
| Unknown account, target, or accounting rule | Precise actionable issue; no invented account, target, hierarchy or precedence. |
| Malformed/hostile XLSX | Deterministic bounded rejection of formulas, unexpected schema, unsupported/encrypted/malformed content, excessive size/rows/decompression, and invalid identifiers; no active-state changes. |

## Dependency order and deliverables

1. **P0 model isolation:** finish the separately assigned invariant fix and independent review. Cover direct foreign-key assignment, relationship assignment, reparenting, deletion, and old/new protected scopes. Mapping services must build on these model boundaries.
2. **Canonical and mapping contracts:** agree versioned record identities, hierarchy/null semantics, stable targets, active-version model, source snapshot provenance, and authorization boundaries. Reconcile the richer governed Pilot contract with #27's narrow interchange; do not silently replace the approved template or publish incompatible files under the same format version.
3. **Governed mapping backend:** reconcile/rebase #26/#27 against the verified base; add persisted diff proposals, identical-input deduplication, explicit conflict reporting, authorized approval, concurrency rejection, atomic idempotent apply, audit, and rollback. Prove behavior with the scenarios above before integration into UI.
4. **Manual editing and XLSX workflow:** both use that service; present counts, row issues, complete old/new diffs, active scope, approval controls, and recovery history. Unknown-account handling and any carry-forward are explicit proposals subject to the same approval and isolation rules.
5. **Peyvast contract discovery:** obtain the missing facts below. This read-only discovery can proceed alongside mapping work, but no real extraction adapter is represented as ready before its source contract is documented.
6. **Peyvast read-only adapter:** implement only the documented interface against a sanitized fixture/test installation, create immutable canonical snapshots, and compare with an equivalent customer Excel export. Run customer-approved reconciliation on an approved environment without changing source data.
7. **Independent acceptance:** review exact PR heads and required CI, verify protected-data boundaries, record known schema/version support and limits, and obtain accounting-owner acceptance of real reconciliation. Output/release acceptance remains a later gate; this note is not a release or merge authorization.

## Facts needed for real Peyvast integration

| Fact or decision | Evidence required / likely owner |
| --- | --- |
| Exact installation | Customer's Peyvast product/edition/build, installed modules/customizations, vendor/support contact, licensed extraction rights and supported interface documentation. |
| Database platform | Actual SQL Server edition/version/build, database and instance topology, compatibility level, collation/encoding, multi-company/year layout, and availability/maintenance constraints; customer DBA. |
| Supported source interface | Confirmation whether official views/API/export exist; documented schema/API version and change guarantees; vendor/customer technical owner. |
| Schema and identity | DDL/data dictionary or equivalent approved documentation, keys, joins, company/year discriminators, account hierarchy and floating-detail semantics, stable row keys and status fields, plus representative redacted rows; vendor/customer DBA. |
| Financial semantics | Fiscal calendar/period bounds, currency/unit/precision, sign conventions, source row grain, posted/draft/void/cancelled treatment, opening/closing handling, and authoritative reconciliation report/filters; accounting owner. Existing historic rules are not automatically generalized to Peyvast. |
| Extraction consistency | Approved snapshot/backup/export mechanism, as-of definition, transaction/isolation guarantees, concurrency behavior, expected data volume, timeout/window, and source revision/change detection; DBA/vendor. |
| Network and identity | Customer-approved host/instance/endpoint, port, DNS/network route/VPN if required, TLS certificate requirements, authentication method, least-privilege object grants, secret delivery/storage/rotation and connection-test authorization; customer IT. Do not put credentials in this note or the repository. |
| Scope and target authority | Authoritative source-to-Aram company/year mapping, account/dimension dictionaries, permitted statement/note/subnote catalog, explicit predicate/overlap rules, authorized editor/approver roles, and lifecycle controls; customer accounting owner. |
| Retention and recovery | Approved source-snapshot retention/location, permissible sensitive fields, audit retention, backup and restore verification, and operational ownership; customer owner/IT. |
| Acceptance fixture | A sanctioned sanitized database/export sample, its equivalent Excel output and exact filters/as-of time, approved expected row counts/totals with hashes, and named accounting reviewer. Expected values must come from supplied evidence, never be invented. |

Until these facts arrive, useful work is the shared contract, model invariants, governed mapping workflow, fixture-based adapter design, and precise discovery checklist. The live customer connector and accounting reconciliation remain explicitly unverified.

## Publication context

This proposed design and metadata-discovery aid are a separate documentation-only task stacked on unmerged safety [PR #32](https://github.com/davoodmehraban89/Aram/pull/32), at `28d1c57882ec20fc17c2c133bbe62ff56e12973f`. PR #32 has successful final-head CI but is not accepted. The accepted branch remains `7dc864fd032f0c4ae4d650d89304a01286a6d914`; do not treat this stack as accepted product functionality.

The companion [Persian discovery guide](../../integrations/PAYVAST_SQLSERVER_DISCOVERY.md) and [metadata-only SQL](../../integrations/payvast-schema-discovery.sql) are statically reviewed aids only. SQL Server execution, customer permissions, metadata completeness, compatibility and live financial extraction are NOT VERIFIED. No accounting data is read by the script; it queries only system metadata.
