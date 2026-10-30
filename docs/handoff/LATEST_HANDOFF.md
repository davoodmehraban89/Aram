# Aram — Latest Handoff Prompt

> Durable accepted-state record with persistent role assignments and recovery workflow.
> GitHub remote evidence remains authoritative. Always fetch the live branch head and open PRs before acting; recorded SHAs are verified events, not perpetual current-head claims.

## Accepted repository state

- Repository: davoodmehraban89/Aram
- Canonical branch: source-data-cleanup
- Recorded accepted control event: [PR #18](https://github.com/davoodmehraban89/Aram/pull/18), reviewed head `fcbeb7387218e9ab294318ae462ed59de717fc95`, squash merge `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b` at `2026-08-25T06:46:16Z`.
- Durable post-merge record: [PR #19](https://github.com/davoodmehraban89/Aram/pull/19), reviewed head `b9059592409606a0a4f11a71c30778cff158b6b6`, squash merge `77f9f595ccfe67a87b11024ff0f6143629dba438` at `2026-08-25T06:57:02Z`.
- Earlier accepted work includes PR #1, #4, #6, #8, #10, #12, #13, and #15.
- PR #7, PR #9, PR #16, and PR #17 are closed without merge and contribute no accepted code.
- [Issue #14](https://github.com/davoodmehraban89/Aram/issues/14) is completed. [Issue #11](https://github.com/davoodmehraban89/Aram/issues/11) records Gate 3 as ready for a new focused task definition.
- No user-ready V1 release, tag, ZIP, EXE, or retained release artifact is accepted or proven.

## Accepted Gate 2A evidence

- PR: https://github.com/davoodmehraban89/Aram/pull/15
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Reviewed PR head: `74b6a6397a2a2c9199a5c7bcf818bb661b2ebe06`
- Squash merge: `4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4`
- Final GitHub Actions: https://github.com/davoodmehraban89/Aram/actions/runs/32712900800
- CI conclusion: success; 52 passed, 1 warning; Alembic upgrade/downgrade and compileall succeeded.
- Accepted capabilities: governed Pilot workbook v0.1 contract, approved blank template, reproducible generator, and deterministic read-only in-memory preflight.
- Template path: `samples/Aram_Pilot_Input_and_Mapping_Template_v0.1.xlsx`
- Independently recomputed SHA-256: `e14a7feb80a216d79ed9cb6dde2b0df3e55317f3da6b26efc77f7118f4702b6f`
- Protected boundary: PR #15 changed no canonical XLSX/PDF, `data/`, database, financial-source, workflow, migration, desktop/release, ZIP, or EXE path.

## Accepted PR #18 control evidence

- Base: `source-data-cleanup@4ab54f4a3cf666827fa1ed30c4e43259ea79f2d4`
- Reviewed head: `fcbeb7387218e9ab294318ae462ed59de717fc95`
- Squash merge: `f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`
- Exact changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`, `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Verification: complete remote four-file diff and metadata reviewed; append-only project-log behavior and protected-data boundary confirmed.
- GitHub Actions: none on the reviewed head; documentation-only paths did not trigger Backend CI.
- Artifacts/releases: `NONE`
- Protected boundary: no application code, tests, workflow, migration, dependency, workbook content, financial data, binary, ZIP, EXE, artifact, or release file changed.
- Acceptance authority: Davood explicitly authorized the merge after independent review.

## Accepted PR #19 control evidence

- Base: `source-data-cleanup@f213d321ff4cd7d3d6fa65ba78dc48f090ee846b`
- Reviewed head: `b9059592409606a0a4f11a71c30778cff158b6b6`
- Squash merge: `77f9f595ccfe67a87b11024ff0f6143629dba438`
- Exact changed files: `PROJECT_STATUS.md`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`
- Verification: complete remote three-file diff, append-only log, whitespace, protected-data boundary, and post-merge accepted-head state passed.
- GitHub Actions: none on the reviewed head; documentation-only paths did not trigger Backend CI.
- Artifacts/releases: `NONE`

## Durable role-based operating model

- Permanent source: `docs/handoff/MASTER_RECOVERY_PROMPT.md`
- Decision record: ADR-011 in `docs/DECISION_LOG.md`
- Introduced through: [PR #20](https://github.com/davoodmehraban89/Aram/pull/20)
- Davood is Project Owner and the accounting/product authority.
- ChatGPT chat is Operational Coordinator: recovery, task scoping, implementation prompts, first-pass review, and copy-ready handoffs.
- Jules is the primary Implementation Agent: exact-base focused implementation, tests, Draft PR, and evidence; it never merges its own PR.
- Codex Work is Senior Technical Supervisor, Independent Reviewer, and Authorized Maintainer: technical sequencing, remote evidence review, conflict resolution, exceptional critical fixes, acceptance decisions, and routine merges under standing delegation.
- GitHub is the evidence source of truth.
- Accounting ambiguity, material scope, protected-data changes, releases, destructive actions, credentials, and new external authority remain Davood escalation points.
- A repository mismatch pauses only the affected task without edits; it does not halt the project.

## Closed superseded work

- PR #16 was closed without merge on 2026-08-25.
- It duplicated accepted PR #15, used stale base `7c7533ee87146dc8fc78b46ebf423be55532c7eb`, was dirty, and recorded incorrect merge SHA `35d45c3f200672a6ef97f13a84cf7c823ecf1bb8`.
- No file or claim from PR #16 is accepted.

## Closed Gate 3 / Gate 2B reference

- PR: https://github.com/davoodmehraban89/Aram/pull/17
- Base: `source-data-cleanup@7c7533ee87146dc8fc78b46ebf423be55532c7eb`
- Head: `4f8648add0e2ed60f01753e979fa3fbe9ccf0f18`
- Final state: closed without merge on 2026-08-25; its code is not accepted.
- GitHub reports 12 changed files although the PR narrative names only 9.
- Backend CI run #31 succeeded with 51 tests on the stale branch head; that does not prove compatibility with accepted Gate 2A.
- Use PR #17 only as reference. Do not reopen, revive, or merge it.
- Comprehensive Mapping Excel import/export, carry-forward, unknown-account queue, note/sub-note mapping, management UI, reproducible Windows packaging, and end-to-end Pilot acceptance remain unimplemented.

## Governance and release reality

- GitHub remote evidence outranks this record and every agent report.
- The accepted branch is currently unprotected; explicit review discipline is mandatory.
- There are no accepted Git tags or GitHub Releases.
- Canonical financial XLSX/PDF and source data remain protected.
- Green CI on an unmerged PR is not acceptance evidence.
- No Gate 3 implementation candidate is accepted or active.

## Active V1-01 safety-gate candidate

- Verified base: `source-data-cleanup@b1ddee87d31ee73b3a5aeac8f9953d0a604c206a`
- Working branch: `codex/v1-01-safety-gate-hardening`
- Draft PR: [#21](https://github.com/davoodmehraban89/Aram/pull/21)
- Independently reviewed implementation head: `700d800dbd9c657f6bd510faafedcbde4847fafd`.
- Earlier exact-head candidate: `aba10b61c770ce319b1b67d960a4f0a1057e25f6`; [Backend CI #36](https://github.com/davoodmehraban89/Aram/actions/runs/32989551021) succeeded.
- A later documentation-triggered [Backend CI #38](https://github.com/davoodmehraban89/Aram/actions/runs/33015151139) exposed a flaky message-specific reparent assertion: protection fired correctly, but through the equally valid parent-company invariant.
- Stabilized candidate: `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`; the single test assertion now accepts either valid `cannot be mutated` protection message without changing product behavior.
- Latest verified CI: [Backend CI #39](https://github.com/davoodmehraban89/Aram/actions/runs/33015277194), success on `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`; 67 tests passed, migration upgrade/downgrade and compile succeeded.
- Purpose: close the independently reproduced protected-year deletion/mutation and Pilot-preflight false-negative defects before any Mapping/UI expansion.
- Planned changed files: `index.html`, `PROJECT_STATUS.md`, `backend/src/aram_backend/models.py`, `backend/src/aram_backend/pilot_workbook.py`, `backend/tests/test_models.py`, `backend/tests/test_pilot_workbook.py`, `docs/PROJECT_LOG.md`, `docs/handoff/LATEST_HANDOFF.md`.
- Local evidence at preparation: 67 pytest tests passed; isolated Alembic upgrade/downgrade and compileall passed; focused Ruff and mypy checks passed.
- Protected boundary: no canonical financial data, workbook, PDF, database, financial value, binary, ZIP, EXE, tag, or release is in scope.
- Independent-review decision: code, scope, diff, and protected-data boundary passed. CI #38 later revealed only a nondeterministic error-message assertion; CI #39 passed after the one-line assertion stabilization.
- Status: `IN_PROGRESS`; this durable-document reconciliation records the complete CI sequence. The resulting documentation-only head must be re-fetched and compared with `b3dc8b3a18934ffe63f615e4f650248be21a5f9c` before Ready/Squash Merge.

## Single next action

Publish this requested two-document reconciliation on PR #21 and route the resulting documentation-only head back to the independent reviewer. The reviewer must confirm that only `PROJECT_STATUS.md` and `docs/handoff/LATEST_HANDOFF.md` changed after the CI-verified stabilized head `b3dc8b3a18934ffe63f615e4f650248be21a5f9c`, verify the final workflow result, then Ready/Squash Merge. Do not begin Gate 3 Mapping until V1-01 is accepted.


## Gate 3 mapping core handoff (2026-10-23)
- Exact base: source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914; branch codex/gate3-mapping-core; Draft PR https://github.com/davoodmehraban89/Aram/pull/26.
- Implementation: explicit year-scoped mapping service and regression tests; no financial targets inferred. CI run https://github.com/davoodmehraban89/Aram/actions/runs/39869553320 reports 87 passed, migration round-trip and compile succeeded on implementation head 6cdd5e88960f3759995dfb475ae8a5e534e00d6c.
- Subsequent documentation commits require exact-head verification. No protected data changes or release. Independent review and acceptance pending; do not merge automatically.
- Remaining scope: Mapping Excel import/export, carry-forward, unknown-account queue, notes and UI, financial output, Windows package and real-user acceptance.

## 2026-10-30 — Gate 3 Mapping review-preparation candidate, Draft PR #50

- Accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged; child [PR #50](https://github.com/davoodmehraban89/Aram/pull/50) is stacked on Draft parent PR #26 exact `185e47f031902a8918c93c8dbb420122e7408403`.
- [RED CI 41070855173](https://github.com/davoodmehraban89/Aram/actions/runs/41070855173): 2 expected failures (obsolete note-target persistence), 88 passes. Fix adds latest-note check **before idempotent replay**.
- Added `mapping_change_preview.py` for read-only old/new snapshots, expected version, current account/note checks and stale-preview fingerprint; no actual mapping approval, actor identity, audit write or authorization.
- [GREEN CI 41071138346](https://github.com/davoodmehraban89/Aram/actions/runs/41071138346) on pre-docs code head: 117 passed, 1 warning. **Verify final docs-head CI** before citing as final evidence.
- No canonical financial file/customer database, schema migration, workflow, dependency, release or accepted branch was changed. C1/C2/C3 actual independent reviewer identities and source-to-statement financial reconciliation remain blocked; Gate 3 not accepted. Future work in [Issue #49](https://github.com/davoodmehraban89/Aram/issues/49).

## 2026-10-30 — Parallel-Session stale-review fix, Draft PR #50

- A second synthetic adversarial scenario found the preview validator reused SQLAlchemy identity-map objects after separate Session updates to MappingRule or FiscalYear. [RED CI 41071505361](https://github.com/davoodmehraban89/Aram/actions/runs/41071505361): 2 expected failures, 117 passed.
- `populate_existing` refreshes scoped persisted objects on each preview/verify call. [GREEN CI 41071670008](https://github.com/davoodmehraban89/Aram/actions/runs/41071670008): 119 passed, 1 warning; migration/compile passed. Confirm final docs-head CI after this append.
- No actual approval, signed token, human reviewer, immutable audit, provider-level transaction lock or production DB guarantees. [PR #50](https://github.com/davoodmehraban89/Aram/pull/50) stays Draft on unmerged #26; Issue #49 Gate 3 completion work and independent C1/C2/C3 review remain outstanding.

## 2026-10-30 — Gate 3 bulk Mapping review preflight, Draft PR #51

- [PR #51](https://github.com/davoodmehraban89/Aram/pull/51) is a scoped child of still-unmerged [PR #50](https://github.com/davoodmehraban89/Aram/pull/50) exact parent `f79947a8624adbd8e84c3f8247ac3ca4a7bd4240`; #50 depends on unmerged #26. Accepted source-data-cleanup remains `7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- New read-only batch classifier separates new/changed/unchanged, repeated-identical/coalesced, repeated-conflicting, invalid, with stable source locators and next-version mapping diffs. Invalid/conflicting row blocks entire batch readiness; **no apply, mutation or authenticated approval method**.
- Regression evidence: [RED 41081238728](https://github.com/davoodmehraban89/Aram/actions/runs/41081238728) missing module → [GREEN 41081481135](https://github.com/davoodmehraban89/Aram/actions/runs/41081481135) 138 passes; [RED 41081877772](https://github.com/davoodmehraban89/Aram/actions/runs/41081877772) six security failures for True/1 coalescing and audit locator controls → [GREEN 41082029761](https://github.com/davoodmehraban89/Aram/actions/runs/41082029761) **144 passed, one warning**, migrations and compile success. Recheck **final doc SHA CI** after this update.
- Existing XLSX import path still saves directly; adapters/authenticated review, immutable audit, transactional CAS, actual account hierarchy/subnote mapping, verified true reviewer IDs and real source financial reconciliation are **NOT** completed. Issues #49/#39/#43 remain open, no C1/C2/C3 signoffs.
- Protected XLSX/PDF, `data/`, customer DB, migrations, dependencies, workflows, binaries, releases and accepted branch untouched. Keep Draft/unmerged. Rollback: close Draft; after explicit authorized acceptance, separate reviewed revert.

## 2026-10-30 — Gate 3 whole-batch staleness preflight, Draft PR #52

- New read-only [PR #52](https://github.com/davoodmehraban89/Aram/pull/52), stacked on unmerged #51 `d022ac48e78d06eb3c17ec820435ccbaac7a6a9c`, upstream unmerged #50/#26. No accepted main/source-data-cleanup modifications.
- `verify_mapping_batch_current` rechecks original complete proposal rows against fresh session-visible account, note, rule and fiscal-year facts, including previously unchanged rows. Rejects changed source, snapshot, checksum, version, catalog, year approval, invalid/conflict and all-noop-only cases. **No writes or human approval.**
- [RED CI 41083365885](https://github.com/davoodmehraban89/Aram/actions/runs/41083365885) missing-function collection error; [GREEN CI 41083623835](https://github.com/davoodmehraban89/Aram/actions/runs/41083623835): **159 passed, 1 warning**, migrations and compile successful on code/test SHA `70760f33026c7cb7f2ad6ac6be164de708f93d41`. Verify new final docs SHA CI.
- Important: no authenticated Draft→Reviewed→Approved, immutable audit, transactional comparison-and-swap/lock, real XLSX write gating, SQL Server test or actual canonical ledger reconciliation; Issues #49/#39/#43 and qualified independent C1/C2/C3 reviews BLOCKED. Keep Draft/unmerged; no production data or source changes.

## 2026-10-30 — Gate 3 inert Unreviewed Mapping draft persistence, Draft PR #53

- [Draft PR #53](https://github.com/davoodmehraban89/Aram/pull/53) on unmerged parent #52 SHA `1063431b08a9e03e022aa9b8e6c5ed90bfb05395`, inherited Drafts #51/#50/#26. Accepted `source-data-cleanup` head unchanged.
- Deliberately records only **Unreviewed** batch evidence, no user/approver identity, audit decision, review approval or MappingRule apply. DB table `mapping_review_drafts` is isolated from `Base.metadata`, added by explicit Alembic `20261030_02`, and constrained by year FK, unique year/request key and Unreviewed-only CHECK.
- Initial missing-module [RED CI 41086027866](https://github.com/davoodmehraban89/Aram/actions/runs/41086027866), next [FAILED CI 41086255707](https://github.com/davoodmehraban89/Aram/actions/runs/41086255707) fixture teardown FK issue, then [GREEN CI 41086542121](https://github.com/davoodmehraban89/Aram/actions/runs/41086542121) 179 passed. Additional synthetic integrity regressions [CI 41086774270](https://github.com/davoodmehraban89/Aram/actions/runs/41086774270): **182 passed, 1 warning**, migration upgrade/downgrade and compile passed. Reverify final documentation SHA CI.
- No financial XLSX/PDF, `data/`, real customer/production DB, existing migration or release modified. Real authentication, human C1/C2/C3 approval, immutable audit, trusted apply CAS and financial reconciliation remain open. Upstream parent acceptance and PR #25 migration history reconciliation mandatory before any release. Keep Draft.

## 2026-10-30 — Gate 3 SQLite system staging audit, Draft PR #54

- Candidate [Draft #54](https://github.com/davoodmehraban89/Aram/pull/54) on unmerged Draft #53 exact `3f089d03ca134cd73082dd0db8ba2461e1e6bc7c`, upstream #52/#51/#50/#26 still Draft; accepted source-data-cleanup remains `7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- Independent SQLAlchemy Core `mapping_draft_events` + SQLite-only `20261030_03` migration; check-limited `DraftStaged`, unique per draft, FK and UPDATE/DELETE blocking triggers. Existing Unreviewed proposal and event insert share caller transaction; read checks event/hash; retries add none.
- Evidence [RED missing module 41088848958](https://github.com/davoodmehraban89/Aram/actions/runs/41088848958) → [GREEN 41089095498](https://github.com/davoodmehraban89/Aram/actions/runs/41089095498) 190 passed. [RED pre-DDL upgrade guard 41089408299](https://github.com/davoodmehraban89/Aram/actions/runs/41089408299) one expected failure → [GREEN 41089569653](https://github.com/davoodmehraban89/Aram/actions/runs/41089569653) **193 passed, one warning**, migration 01→02→03 and down, compileall succeeded. **Verify final docs HEAD CI.**
- `20261030_03` refuses to upgrade if old `20261030_02` draft table contains any rows; retrospective provenance must not be invented. Non-SQLite dialect also rejected before DDL. Both require separately reviewed migration/backup plans. Triggers are not tamper-proof against privileged DB administrator.
- This is *system staging evidence only*, no authenticated actor, human review, Approved transition, immutable legally compliant financial audit, authorized SQL provider, locked CAS, rule apply, canonical ledger reconciliation or production writes. C1/C2/C3 independent reviews remain absent; Issues #39/#49/#43 still OPEN; no merge or release.

## 2026-10-30 — Gate 3 read-only RSA authenticated principal, Draft PR #55

- New [Draft PR #55](https://github.com/davoodmehraban89/Aram/pull/55) stacked on unmerged #54 exact `c5e3fb7f8917433a1075ece8ad1ee95a1695dad5`; inherited Draft #53/#52/#51/#50/#26; accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.
- New `GET /api/v1/auth/me` with strict RS256 signed-access-token verification, pinned 2048+ RSA public key, issuer/audience/subject/iat/nbf/exp and 15-minute max lifetime; exactly one signed `mapping_proposer` or `mapping_reviewer` role. No authentication by client X-User/role headers, unsigned or HMAC tokens, wrong signer, or forged payload. Default auth configuration EMPTY/disabled; missing actual enterprise IdP yields HTTP 503. New `PyJWT[crypto]` dependency.
- Tests-only [RED CI 41109024753](https://github.com/davoodmehraban89/Aram/actions/runs/41109024753) **34 expected missing-route failures**, 193 passes; [GREEN CI 41109205928](https://github.com/davoodmehraban89/Aram/actions/runs/41109205928) 227 passes; added adversarial verification and [GREEN CI 41109398796](https://github.com/davoodmehraban89/Aram/actions/runs/41109398796) **231 passes, 2 warnings**, Alembic 01→02→03 round-trip and compileall successful. **Confirm final docs SHA CI separately.**
- No actual enterprise principal or finance reviewer identity is configured. Existing Unreviewed proposal records have no authenticated author and cannot prove self-approval separation; role claims are not finance authorization. No approve/apply API; no real user accounts, OAuth login, JWKS rotation, revocation, year/company grants, signed financial decision or rule write CAS. Real source financial reconciliation and C1/C2/C3 independent human reviews still missing. Keep Issue #49/#39/#43 OPEN and PR Draft/unmerged; do not claim deployment/completion.

## 2026-10-30 — Gate 3 signed fiscal company/year/role authorization, Draft PR #56

- [Draft PR #56](https://github.com/davoodmehraban89/Aram/pull/56) child of unmerged #55 exact parent `8d82f1e7be9653bac467101234a62029bdfa3178`; original accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged, upstream Drafts still unmerged.
- Auth JWT now accepts **strict signed `aram_scopes`** only: each scope exact company code, fiscal-year business number and same role as signed token. Missing scopes authenticate but authorize no fiscal year. Bad scopes are invalid 401, valid token with no exact grant gets 403; never trust headers or broad wildcard/admin claims.
- New `mapping_year_authorization.require_year_access` checks current DB Company/FiscalYear Draft and exact grant under `Session.no_autoflush` with `populate_existing`. Read-only `GET /api/v1/auth/year-access/{year_id}` uses signed-principal dependency. No proposal/write/approval route activated; real company/year grant assignment and IdP connection are NOT configured.
- Tests-only [RED 41110810775](https://github.com/davoodmehraban89/Aram/actions/runs/41110810775) 28 intentional missing-behavior failures. Initial [CI 41110973867](https://github.com/davoodmehraban89/Aram/actions/runs/41110973867) 2 test expectation failures/257 passes; invalid signed role should be 401, not 403. Corrected assertions and added direct cross-role denial at SHA `59cb141cad81add6523f4fea7a127c8180d080e5`. **Verify final exact SHA GitHub CI, all migration round-trips and reviewer status.**
- Real authenticated user approval, independently established C1/C2/C3 reviewers, persisted identity on drafts, non-self-approval, locked compare-and-set apply, Excel importer closure, source account hierarchy and financial reconciliation still open (Issues #49/#39/#43). Keep Draft/unmerged; no operational acceptance.
