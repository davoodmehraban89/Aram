# Gate 3 — Package 5 acceptance matrix and Gate 4 handoff

Date: 2026-11-01. Branch: feat/gate3-governed-mapping-20261101.
Approved base: source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914.
Starting candidate: b25ce454ff182f1d3c611b872f44b78c0d8c0fe1.
PR: https://github.com/davoodmehraban89/Aram/pull/82 (Draft).

## Review A — financial correctness (self-audit, not independent)
- Checked company/year isolation, three-party workflow, conservative account ambiguity classification, mapping notes and account hierarchy in Excel roundtrip.
- No authorized real-ledger sample supplied. The synthetic test suite is not proof of correctness of financial statement mapping.
- No imported workbook approval can be treated as independently authenticated approval.

## Review B — security/architecture (self-audit, not independent)
- New API router exposes guarded propose/review/approve/revise endpoints, registered on FastAPI app.
- The only actor used is the subject returned by server-configured identity resolver. Bearer tokens and untrusted header/body role claims cannot directly set actor or permissions. Unconfigured resolver returns 503 (fail closed). Company and role scopes enforced by MappingAccess.
- No production IdP/OIDC configuration, signing-key trust chain, token expiry/audience verification, or deployment secret management was available. Trusted resolver must be installed by deployment operators. No claim of production identity integration.
- SHA-256 hash chain added for audit events, stored in separate mapping_audit_hash table. External terminal-digest receipts can be exported and checked. No secure external receipt repository was available; a privileged DB writer can rewrite the entire DB and recalculate hashes. This is detection with a trusted external anchor, not independent tamper-proofing.
- Existing databases with pre-chain events require an explicit reviewed migration/backfill plan; the implementation does not silently rewrite existing historical audit events.

## Review C — adversarial/recovery (self-audit, not independent)
- HTTP tests cover missing/forged token, unauthorized role/company, maker reviewing/approving own mapping, independent approval and persistence.
- Hash chain tests cover digest tamper, missing digest, external receipt mismatch and verified SQLite online backup/restore.
- Existing tests cover stale writers, scope and Excel roundtrip. No full production crash/power-loss or operational disaster-recovery drill performed.

## Acceptance matrix

| Criterion | Evidence | Result |
| --- | --- | --- |
| Approved base and isolated branch | git refs / PR #82 | PASS |
| Protected mapping HTTP endpoints | mapping_api.py, test_mapping_api.py | PASS in isolated tests |
| Production IdP with validated bearer tokens | External deployment credentials not provided | BLOCKED |
| Scoped role segregation | mapping_access.py and HTTP tests | PASS in isolated tests |
| Audit SHA-256 chain and external anchor verification API | mapping_integrity.py, mapping_store.py and tests | PASS in isolated tests |
| Privileged-DB tamper resistance with separately protected anchor | External trusted storage not connected | BLOCKED |
| Company/year and duplicate/ambiguous financial mapping | mapping_quality.py, workflow and tests | PASS in synthetic tests |
| Authorized real-ledger reconciliation and financial signoff | No authorized sample or signed decision | BLOCKED |
| Excel roundtrip / review evidence | mapping_workflow.py and tests | PASS in synthetic tests |
| SQLite backup, restore and tamper injection | test_mapping_recovery_quality.py, test_mapping_hash_chain.py | PASS in isolated tests |
| Production operational recovery drill | No production or staging operational authorization | BLOCKED |
| Three independent reviewer approvals | Three self-audits only; independent reviewer identities absent | BLOCKED |
| Final-head CI and test evidence | Must record URL and conclusion on PR after push | PENDING |

Decision: **NO-GO / CHANGES REQUESTED**. Gate 3 is NOT accepted. PR remains Draft. Do not merge, release or start Gate 4 implementation.

## Gate 4 handoff — preparation only
- Use reviewed approved mappings as sole input to financial statements; never infer approval from Excel.
- Production prerequisite: external IdP/OIDC or equivalent verified identity resolver, role/company claims and revocation policy.
- Audit prerequisite: independent immutable/WORM or signed off-DB anchor receipt repository with periodic verification and retention.
- Finance prerequisite: owner-approved real-ledger reconciliation, unresolved mapping queue disposition, source hashes and signed financial mapping decision.
- Operations prerequisite: staging backup/restore with recovery time/recovery point targets and incident evidence.
- Governance prerequisite: independent reviewer records exact SHA, diff, tests, risks, identity and decision in PR.

Rollback: revert isolated feature-branch commits; no production financial data or canonical workbook changed.
