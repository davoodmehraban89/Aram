# ARAM native Windows five-statement pilot — UNSIGNED AND UNRELEASED

This is a **nonofficial, local-only Tkinter/ttk Windows inspection UI** for the five-statement pipeline. It is separate from the older PR #59 preflight-only shell. It runs on the newer backend stack with the same XLSX+JSON validator as the CLI; it does not merge or reuse the unreviewed older desktop controller.

## What works

- Choose a local Pilot `.xlsx` and a policy/journal `.json` manifest.
- Run the actual shared-snapshot five-statement pipeline in a worker thread so the native window remains responsive.
- Display five candidate statuses and blocked reconciliation finding codes, in Persian.
- Show the workbook source digest prefix for inspection.
- Invalidate old results every time the selected file changes or is cleared.
- All enabled menu and button controls have real callbacks; shortcuts: Ctrl+O/M/R/L/Q and F1.
- A limited and explicitly visible findings list (at most 2,000 rows with an overflow count).

Selection checks file extensions, regular-file status, symlinks and size. Execution delegates to `safe_read_workbook` and `safe_read_cash_manifest` through the existing CLI function, which reopens local files with bounded reads and checks inode, modification and replacement. A failed input cannot leave a previous eligible result in view.

## Development mode

Install backend project dependencies and run:

```powershell
cd backend
python -m pip install -e ".[test]"
python -m aram_backend.desktop_five_statement
```

For offline diagnostics without opening a Tk window:

```powershell
python -m aram_backend.desktop_five_statement --self-test
python -m aram_backend.desktop_five_statement --ui-smoke
```

The UI smoke opens native widgets, exercises buttons/menu/shortcuts and runs an intentionally malformed synthetic manifest to verify blocked handling. It is **not** a human usability acceptance test.

## Unsigned EXE candidate

On Windows, with Python 3.12 and PyInstaller installed:

```powershell
cd backend
python -m pip install -e ".[test]" "pyinstaller>=6.10,<7"
.\desktop\build_five_statement_windows.ps1
```

The result is `backend/dist/AramFivePilot-UNRELEASED.exe`. GitHub's dedicated Windows workflow additionally runs the controller/integration tests, Tk native widget smoke, builds the unsigned one-file EXE, and runs both `--self-test` and `--ui-smoke` against the frozen executable before uploading the **7-day, unreleased inspection artifact**. No signed installer or official release/tag is created.

## Non-approval and privacy

The same manifest contract as `docs/FIVE_STATEMENT_PIPELINE_CLI.md` applies. It includes potentially confidential account and journal data; **do not commit real corporate manifest files to public GitHub**. The app does not upload files, write to a database, mutate XLSX/JSON, post accounting entries, save report files or generate an official PDF/Excel document.

Even a green result is only eligible for analyst review. There is no proof of source-ledger completeness, no authenticated accounting-policy or finance-owner signoff, no independent C1/C2/C3 approval, no signed Windows installer, no clean-machine deployment validation and no legally releasable financial statement. Review the actual security and accounting constraints before any production use.
