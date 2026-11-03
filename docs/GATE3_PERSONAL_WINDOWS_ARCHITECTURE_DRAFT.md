# Gate 3 - Personal Windows Deployment Decision (DRAFT)

Status: PROPOSED / NOT ACCEPTED. This document does not waive the existing acceptance policy.

## Verified environment (2026-11-02)
- Windows 10.0.22631; Python 3.12.10 installed at user-local Python312 path.
- Isolated environment: backend/.venv, Python 3.12.10, pip 25.0.1.
- Standard pip install -e '.[test]' failed on uvicorn[standard] dependency resolution; pinned uvicorn attempt failed resolving websockets from available package index.
- Installing required backend dependencies with plain uvicorn (without standard extras) succeeded; backend tests on Windows passed (pytest exit 0).
- Existing Ubuntu CI on head 9d346f098a0a2159d96080715322879b08d9a1f8: SUCCESS (run 41339488244).
- No live identity resolver, independent receipt store, financial reconciliation or operational recovery evidence established.

## Threat model and boundaries
- Intended initial deployment: one authorized operator, Windows personal computer, local-only API binding to 127.0.0.1; no LAN or public exposure by default.
- Threats: stolen Windows session, malicious local process, unauthorized local file changes, lost device, ransomware, disk failure, accidental financial mapping mistakes.
- Same-host administrator can alter application/database/receipts. A local hash chain or directory cannot guarantee privileged tamper resistance. Independent protected offline/off-host receipts and backup are required for such a claim.
- No corporate identity provider, organization infrastructure or corporate access is assumed.

## Owner acceptance vs independent approval
- Current mapping workflow requires distinct maker/reviewer/approver identities. Never create fictitious users or reuse the same person under multiple identities.
- Proposed future owner-acceptance mode MUST be a distinct explicitly labeled decision (e.g., OwnerAcceptedWithException), NOT a fabricated Reviewed/Approved transition.
- A financial mapping accepted solely by its maker must remain marked as lacking independent review, with risk acknowledgement, reason, timestamp, source hash and append-only audit event.
- Existing Approved-only financial export rules must not be silently bypassed; any changed downstream contract requires dedicated tests and explicit owner signoff.
- GitHub independent code review remains a separate acceptance requirement under docs/ACCEPTANCE_POLICY.md until explicitly and defensibly revised.

## Required acceptance evidence
1. Windows reproducible install with version constraints and successful pytest + smoke tests.
2. Verified local authentication/session management and negative authorization tests.
3. Trusted independent receipt/backup location and tamper drill, with limitations documented.
4. Authorized source-ledger hashes, full reconciliation and exception disposition.
5. Isolated recovery drill with measured RPO/RTO and integrity checks.
6. Independent review of exact remote SHA, diff, tests, risks and documented decision.

## Explicit restrictions
- NO-GO until evidence above is verified; no Merge, Release or Gate 4 implementation.
- Never modify canonical data/, samples/ XLSX/PDF or original ledgers as part of setup.
- No acceptance of fake independence or weakening controls merely to achieve a GO label.
## Implementation update (2026-11-02; uncommitted)
- Added `OwnerAcceptedWithException` as an explicitly non-Approved mapping status, with reason on the audit event and persistent-store transition validation; tests cover persistence, forbidden conversion to Approved and rejection of invalid acceptance.
- Added opt-in `local_auth.py` password hashing (PBKDF2-HMAC-SHA256, random salt, 600,000 iterations), opaque short-lived in-memory sessions, revocation and tests. NOT connected to API or provisioned with a real owner credential. This is a prototype security component, NOT an authenticated deployment.
- Local auth still requires persistent secure credential provisioning, rate limiting, logout/session lifecycle, OS storage permissions, localhost-only deployment enforcement and security review before enablement.
- Owner acceptance is not exposed through HTTP until a verified owner role, secure resolver and complete audit controls are in place. Existing independent approval flow remains unchanged.
- The audit reason is persisted but the current receipt hash chain must be reviewed for coverage and external anchoring. Do not treat local DB integrity as protection against privileged tampering.
- Full backend test suite passed on Windows after changes. Gate 3 remains NO-GO.
## Google Drive destination and verification boundary (2026-11-02)
- User-designated remote destination: Aram / Gate3-Encrypted-Backup-And-Receipts (Drive folder ID `18iJA_5eYmAGTCakS64regINrrW4bP9K7`). Folder creation confirmed via connected Google Drive.
- No source ledger, financial workbook, unencrypted DB, credential, key, or real receipt has been uploaded.
- Drive folder existence does NOT establish independent immutable retention or tested recovery. Operator deletion and modification remain possible without additional controls.
- Current connector upload requires a materializable connector file reference; remote Desktop Commander paths are not automatically connector file references. The Windows Drive sync client was not detected. Transport must be validated before claiming an uploaded backup.
- For future real backups: create an isolated SQLite snapshot, encrypt before upload, keep decryption secret outside Drive, upload a versioned file, read back and verify digest, then perform an isolated restore drill. Do not export canonical source ledgers by default.
- Owner-accept API is available only when a trusted resolver is explicitly configured. A maker or outsider cannot self-assert owner privileges through request bodies or headers. It is NOT an independent approval and must not unlock Approved-only exports.
## Owner exception API update
- HTTP route POST `/api/v1/mapping/{company}/{year}/{mapping_id}/owner-accept` added behind the existing trusted resolver and company-scope authorization. Requires explicit `owner` role, reason length 15-2000, and stores `OwnerAcceptedWithException` (not `Approved`).
- Verified unauthorized maker/foreign-company requests fail, weak reason fails, legitimate mock owner succeeds, reason is persisted, and reason is covered by the terminal audit hash/receipt. Tests use synthetic data only.
- Do not mistake test identities for production authentication: no live owner account has been provisioned. Real local identity provisioning, login rate limits, credential storage and secure startup are still required before enabling mapping service.
- Single-host local backup remains a recovery test only, not independent or immutable off-host protection. No Gate 3 GO.
## Synthetic recovery drill and Drive mount check (2026-11-02)
- GoogleDriveFS process verified running; Windows E: drive volume name `Google Drive`, with `E:\My Drive` mounted.
- Connected Google Drive account contains `Aram` folder and the new Gate3 folder, but these folders were NOT present in the local E: My Drive enumeration. Do not assume both connections represent the same account or that the folder is synced; no blind copy to E: was performed.
- Added `test_gate3_recovery_drill.py`: synthetic mapping -> SQLite consistent snapshot -> separate restore -> DB/hash-chain verification -> external receipt check -> overwrite rejection -> forged receipt rejection. Test passed on Windows.
- Full backend pytest suite now 105 tests passed, exit 0. This is a synthetic local DR exercise, not remote Drive restore, and no real financial dataset was used.
- Still NO-GO: encrypted remote upload/readback, off-host tamper protection, real owner provisioning, independent review and authorized financial reconciliation outstanding.
## Verified Google Drive sync transport (2026-11-02)
- User confirmed the Windows Google Drive and connected ChatGPT Google Drive account are the same.
- Windows `GoogleDriveFS` running; E: mounted as Google Drive.
- Created non-sensitive 66-byte probe `E:\My Drive\Gate3-Sync-Probe-Aram-20261102.txt`, subsequently observed by Google Drive connector (ID `1lowDeB-DcY8erRjt0Fy_mFYv9KN4fxAx`). This verifies Windows-to-cloud sync for a harmless text file.
- Created `E:\My Drive\Aram-Gate3-Synthetic-Backup`, subsequently observed in Google Drive (folder ID `1n6xN_2Cj-mRrNpryWI5I14CH6r8pPoSF`). This is a separate Windows-synced folder; do not confuse it with the connector-created Aram/Gate3 folder.
- Attempt to install `cryptography` in isolated backend venv failed with `files.pythonhosted.org` read timeout (exit 2); no encryption or cloud DB upload claimed. No unencrypted DB was copied to Drive.
- Before real backup: install a vetted authenticated-encryption implementation; ensure keys remain off Drive; test encryption, tamper rejection, cloud upload/download and isolated restore. Existing cloud folder alone is not immutable evidence.
## Verified encrypted synthetic cloud round-trip (2026-11-02 evening)
- `cryptography>=44,<47` installed successfully into isolated backend venv (pip exit 0). Added AES-256-GCM synthetic encryption and tamper-rejection test.
- Synthetic-only encrypted SQLite file `gate3-synthetic-983822252fea33db.aesgcm` uploaded via Windows E: mount. Google Drive direct file metadata verified ID `1gHK6nDMJs7fj0HQycNyMROnigLspjsC_`, parent `1n6xN_2Cj-mRrNpryWI5I14CH6r8pPoSF`, size 28700 bytes.
- Fetched file independently through connected Google Drive and verified downloaded bytes SHA-256 `b05a3b8510b8855b00bf3db84f935a8b6802a315c992853d529c56c70811e9b0` equals original Windows hash. Cloud transfer + readback integrity PASS.
- IMPORTANT: original one-off cloud drill script generated an ephemeral in-memory key and discarded it after process exit; this particular cloud ciphertext cannot be decrypted for a restore drill. Local AES-256-GCM decrypt/restore and tamper rejection are tested independently. Next end-to-end drill must retain the key in process while performing independent cloud readback; real backups require user-managed recovery keys and documented custody.
- Full backend test suite 106 tests PASS (exit 0); existing StarletteDeprecationWarning only. Still Gate 3 NO-GO: no independently verified cloud-to-decrypt-to-restore drill, owner credential provisioning, independent review or immutable receipt storage.
## Synthetic encrypted recovery evidence (2026-11-02; uncommitted)
- Added `backend/tools/gate3_synthetic_cloud_restore.py` using vetted cryptography AES-256-GCM with a process-ephemeral key, unique nonce and fixed AAD. It uses only synthetic mapping data; plaintext and key are not written to Google Drive.
- Windows script completed PASS: mount-file readback SHA-256, authenticated decryption, isolated SQLite restore, integrity check, audit receipt verification, mapping equality and ciphertext tamper rejection.
- Google Drive file ID `1qu7IRVoQYVRqhNJCqtJI-WuUZY6AdcSi`, 28,700 bytes, independently downloaded via connected Drive; SHA-256 `c86477e6970d1fa28a3d4d4839abb9f749f5469135426796ab19cc5b3a53034d` matches Windows output.
- LIMITATION: independent cloud-downloaded bytes were not fed into the decrypt/restore process while its ephemeral key was alive. Thus separate cloud download verification and local restore are proven, but a single independent cloud-to-restore transaction remains unproven.
- Operational backup remains blocked pending persistent user-controlled key custody/recovery, secure production owner provisioning and authorization, immutable/off-host audit evidence, authorized reconciliation, and independent reviewer sign-off. Gate 3 NO-GO. No production data, release or merge was touched.
