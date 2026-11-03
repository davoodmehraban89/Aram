# Package 9.1 — Security execution evidence (2026-11-03)

## Decision
**PARTIAL / NO-GO for Gate 3.** The Argon2id login path, FastAPI login/logout integration, DPAPI CurrentUser credential vault, and passphrase-encrypted portable recovery-envelope primitives are implemented and locally tested. This is not yet an operational multi-user identity service and does not satisfy independent recovery evidence or independent review.

## Baseline and branch
- Repository: davoodmehraban89/Aram
- Parent PR: #89, draft, base SHA `a0b72be87720b1ff08361298b903ba57dd4fb408`
- Working branch: `feat/gate3-package9-1-security-20261103`
- Parent commit before this implementation: `f3f37ee8fb4894006d4faa866dfa140926b1d96a`
- Worktree: `C:\Users\Davood\Documents\Aram-Gate3-Package9-1-Security`
- Canonical financial data not modified. No merge or release performed.

## Implemented
1. `LocalSessionAuthority` now provisions Argon2id hashes and verifies passwords through the dedicated security module.
2. Legacy PBKDF2 credentials can be imported without plaintext; on successful login the hash is upgraded to Argon2id in memory. Wrong passwords do not trigger migration.
3. FastAPI `/api/v1/auth/login` and `/logout` routes are added. Mapping API uses the resulting opaque session token through the trusted server-side resolver; actor/role/company headers remain untrusted.
4. Startup can opt into a DPAPI vault using `ARAM_CREDENTIAL_VAULT_PATH`; mapping database path is configurable with `ARAM_MAPPING_STORE_PATH`. With no vault configured, authentication stays fail-closed (503).
5. Windows DPAPI CurrentUser encrypted credential vault supports atomic save/load and detects ciphertext tampering.
6. Portable recovery envelope uses Scrypt + AES-256-GCM with a separate passphrase; tests verify round-trip, wrong passphrase, tampering and malformed input. No cloud upload or off-device copy was performed.
7. Regression tests added for API login/logout, bearer token revocation, PBKDF2 migration, DPAPI round-trip/tamper, and portable recovery.

## Verification
- Full backend test suite: **136 tests passed** (including Windows DPAPI tests on the connected Windows host).
- Ruff: PASS.
- compileall: PASS.
- pip check: PASS.
- git diff --check: PASS.
- One existing Starlette/httpx TestClient deprecation warning remains.
- Test run is local on Aram; this is not remote CI proof for the new candidate until GitHub Actions completes on the final SHA.

## Three review passes (sequential self-review, not independent)
### Reviewer 1 — Functional QA
- Confirmed successful Argon2id login, PBKDF2 upgrade after successful login only, API login/logout, mapping API session use, and fail-closed behavior when not configured.
- 136/136 local tests passed.

### Reviewer 2 — Security and architecture
- Confirmed DPAPI CurrentUser protection and authenticated tamper detection, passphrase-encrypted recovery envelope, no credential plaintext in the vault, and explicit opt-in configuration.
- Findings still open: session/lockout state is process-memory only; one local credential identity is supported; there is no cross-process throttling, account lifecycle, MFA, enterprise IdP, account recovery workflow/UI, independent cloud escrow, or proof of restrictive NTFS ACL on deployment path. DPAPI recovery is tied to the Windows user profile; portable envelope passphrase must be separately retained.

### Reviewer 3 — Adversarial and misuse
- Tested malformed stored hashes, wrong passwords, oversized passwords, bad recovery passphrases, ciphertext tampering, malformed recovery envelope, unconfigured API, unknown bearer tokens, logout/replay, and company-scope rejection.
- Remaining adversarial gap: multi-user/concurrent worker behavior and process restart/session invalidation were not tested as production deployment behavior.

## Critical limitations / acceptance blockers
- This local adapter supports one credential/subject per authority. It cannot by itself provide independent maker, reviewer, and approver identities. A trusted multi-user IdP or a properly designed multi-account authority is required before workflow deployment.
- PBKDF2 migration updates the active in-memory credential only. Persisting the upgraded hash back into the DPAPI vault atomically is not yet wired; a restart before that persistence would require another PBKDF2 verification.
- The portable recovery envelope is a tested library primitive, not yet part of an attended backup procedure. Its passphrase must be stored separately; no independent cloud copy or restore witness exists.
- DPAPI vault is CurrentUser-bound. Loss of the Windows profile may prevent DPAPI unprotect; portable envelope is the recovery route but has not been copied to an independent destination or tested on a second Windows profile/device.
- No independent reviewer has approved the candidate.
- CI must pass on the final SHA before the code-quality gate can pass.

## Safe boundaries
- No real financial data was accessed or modified.
- No production login credential was changed.
- No merge, release or force push.
- The app remains fail-closed if no DPAPI vault is configured.
- Gate 3 remains **NO-GO** until the blockers above and the other Gate 3 financial/audit/DR requirements have evidence.
