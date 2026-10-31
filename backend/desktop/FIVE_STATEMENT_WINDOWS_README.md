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

## Try the application using a safe synthetic demonstration

No company information is needed. The Windows CI inspection artifact now contains three separately labeled companion demo files in `DEMO-SYNTHETIC-ONLY/`:

- `ARAM-SYNTHETIC-ONLY.xlsx` — six entirely artificial general ledger accounts and account-to-note mappings.
- `ARAM-SYNTHETIC-ONLY.json` — matching synthetic note controls, presentation and equity policies, cash account scope and paired cash transactions.
- `READ-ME-SYNTHETIC-ONLY.txt` — clear warning that this is neither a real company nor an approved financial statement.

Extract the GitHub Actions artifact ZIP. Run the unsigned `AramFivePilot-UNRELEASED.exe` only if you understand and accept the risks of an unsigned test build. Select the demo XLSX with **انتخاب اکسل**, select the JSON with **انتخاب تنظیمات**, then press **اجرای کنترل پنج صورت مالی**. Five candidates should show **قابل بررسی**; this means *synthetic arithmetic checks passed*, never that a real financial statement was approved.

Alternatively generate an identical *structural* demo locally using the backend source (the spreadsheet package metadata may differ between runs):

```powershell
python -m aram_backend.synthetic_five_statement_demo --output-dir "C:\\Temp\\ARAM-DEMO-SYNTHETIC-ONLY"
```

The target directory must **not already exist**. The generator never overwrites an existing directory or its contents. It writes exactly the labeled XLSX, JSON and notice and does not use external/customer data. The Windows pipeline tests both the generated inputs and the **frozen EXE** through the new `--ui-valid-smoke` flag.

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
python -m aram_backend.desktop_five_statement --ui-valid-smoke
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

## Read-only financial amounts tab

The new **خلاصه مبالغ** tab shows **28 unrounded monetary values** extracted directly from the five typed candidate objects and the cross-statement control: BS assets/liabilities/equity and balance difference; IS revenue, costs, operating/pretax/net results; EQ opening, movement, profit and closing; CF opening, activity net flows, cash change and closing; TB opening/turnover/closing; and the three cross-statement reconciliation differences. The company, fiscal year, currency and unit are displayed from the actual input pipeline.

The display is **not** an official statement template and makes no account classification claims beyond the user-supplied policies. Figures on a blocked result are visibly marked *diagnostic only / blocked*; they are never silently presented as approved. Exact Decimal values are formatted with thousands separators without rounding or sign changes.

Changing either selected file, clearing selections, or encountering a processing error clears both candidate statuses **and** the amounts tab. Both native Tk tests and the frozen-EXE `--ui-valid-smoke` verify the populated numbers and subsequent clearing.

## Read-only source-detail drill-down

The new **ریز اقلام** tab shows each output line and its traceable source details: balance-sheet and income-statement note lines; equity note movements and account-level opening/debit/credit/movement/closing; cash journal lines and per-cash-account turnover roll-forward; and all trial-balance account rows. The grid includes note/transaction/account IDs, source row, source exposure, evidence references and the supplied presentation/classification policy references. Amounts retain exact Decimal scale and signs.

Use the statement selector to isolate one of the five statements and the search box to find an account, note, transaction, description or evidence reference. Results are paginated at 200 rows and horizontally/vertically scrollable. The drill-down refuses more than 75,000 rows instead of silently dropping details. Detail construction, integrity checks, and text filtering run in background worker threads; Tk only renders the current 200-row page.

Before figures or details appear, the desktop integrity gate checks the typed candidate/reconciliation objects, their non-approval flags, source SHA-256 snapshot, company/year, shared note-reference snapshot and critical equity/profit/cash/trial-balance ties. This is an additional display-integrity guard, not an independent audit or proof that source ledgers are complete.

## Search responsiveness and limits

Filtering and text search are performed off the Tk event loop. While a search is running, only the search controls and page navigation are disabled; the main window remains responsive and shows a searching status. Search queries are limited to 256 characters, unsafe control/bidirectional characters are rejected, and the search worker validates the bounded row cells before matching. The Windows frozen-EXE smoke expands synthetic details to the exact 75,000-row limit, runs a statement filter, and exercises page navigation. This is an automated responsiveness-path check, not a performance guarantee for every corporate workbook or PC.
