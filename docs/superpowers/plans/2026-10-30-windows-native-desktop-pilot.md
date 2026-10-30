# Windows native ARAM Pilot — implementation, test evidence and handoff

**Task:** continue development after owner confirms final delivery must be Windows `.exe`. Root `index.html` is explicitly quarantined; no real pilot GUI exists. [Issue #58](https://github.com/davoodmehraban89/Aram/issues/58) records previous 0 clickable controls. [Draft PR #59](https://github.com/davoodmehraban89/Aram/pull/59), exact unmerged parent #57 SHA `6b6aca8883ad4902574cbf954d739e1a3bcf3967`; original accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

1. [x] Inspected actual GitHub tree, accepted status, `AGENTS.md`, `docs/ACCEPTANCE_POLICY.md`, `backend/pyproject.toml`, `pilot_workbook.py`, backend CI and missing frontend. Chose real native Tkinter/ttk instead of reactivating disconnected HTML; this **pilot shell is not final toolkit decision**.
2. [x] Created exact-parent branch `codex/windows-native-pilot-shell-20261030`, and **tests FIRST** at SHA `13b00d75249e92b8a5ac901ecae8e350837aae4b`: independent read-only controller, file-byte stability, rejection of non-XLSX, missing/huge/changing files, reset of stale results, no workbook deletion, headless self-test, named action callback completeness. [Backend CI run 41120753977](https://github.com/davoodmehraban89/Aram/actions/runs/41120753977) scheduled as initial RED at that SHA; **do not declare expected failure observed unless run logs confirm it**.
3. [x] Added `desktop_pilot_core.py` strict read-only state machine, bounded 20MiB + 1-byte file read, 500-entry/128MiB declared uncompressed ZIP cap, symlink refusal; always uses canonical `preflight_pilot_workbook`, with no DB or network.
4. [x] Added `desktop_pilot.py` actual native Tk window; three notebook tabs; File and Help menus; 5 implemented actions; 3 real buttons; 5 keyboard shortcuts; disabled validation until selection; issue table with fields/sheet/row/code; explicit no-approval banner. `--self-test` tests headlessly, `--ui-smoke` runs a real Tk process and invokes every menu/button + all 3 tabs in synthetic fixture. Neither is genuine pixel-level accessibility or financial E2E coverage.
5. [x] Added `backend/desktop/aram_pilot_entry.py`, `build_windows_exe.ps1`, README and `.github/workflows/desktop-windows-ci.yml`. Windows x64 CI installs PyInstaller, tests controller, builds **unsigned, unreleased** `AramPilot-UNRELEASED.exe`, invokes frozen `--self-test` and `--ui-smoke`, uploads 7-day PR-only inspection artifact. **No Windows EXE success or downloadable artifact may be claimed before actual remote logs/artifact inspection.**
6. [x] Added synthetic tests for ZIP metadata expansion and invalid symlinks; improved Windows smoke to navigate **all three tabs**, check shortcut registration, press all 3 native buttons, invoke every File/Help action. Never call an inert placeholder a functional financial feature.
7. [ ] Verify all GitHub Actions actual exact-code-head test outcomes, diagnose and fix failing test/build/smoke, then update spec, project status/ADR/log/handoff, finally re-run exact-last-head CI. Validate allowlist and no unrelated changes.
8. [ ] Independent non-author technical, accounting and Windows QA review; actual clean Windows 10/11 VM install, MS UI automation full physical clicking/keyboard, DPI, RTL and screen readers, real production acceptance data/IdP, reconciled finance statement engine and safe signing/release path. No merger without real C1/C2/C3.

## Only allowed file changes

- NEW `backend/src/aram_backend/desktop_pilot_core.py`
- NEW `backend/src/aram_backend/desktop_pilot.py`
- NEW `backend/tests/test_desktop_pilot.py`
- NEW `backend/desktop/aram_pilot_entry.py`, `backend/desktop/build_windows_exe.ps1`, `backend/desktop/README.md`
- NEW `.github/workflows/desktop-windows-ci.yml` (explicit Windows tests and unsigned artifact)
- NEW focused spec/plan
- APPEND ONLY `PROJECT_STATUS.md`, `docs/DECISION_LOG.md`, `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`

No edits to root quarantined `index.html`, `data/`, samples/templates, canonical XLSX/PDF, production/customer DB, financial values, previous migrations, credentials, accepted branch, dependency constraints, binaries, ZIP or official release. PyInstaller is installed **only by Windows CI**, not committed binary and not a production signing process.

## Rollback and blocker

Before merge, close unmerged Draft #59. The new CI artifact has 7-day expiry and is unsigned/UNRELEASED; deleting artifact does not undo a repo merge. No DB migration added here. If ever merged after genuine reviewers, a separate documented revert removes new desktop modules/workflow without touching source data. End-user accounting features remain blocked until financial engines, identity/permissions and independent reviewer governance are accepted.
