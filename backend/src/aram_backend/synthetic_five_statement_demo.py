"""Clearly synthetic demo data; NEVER company data or an official report.

This is intentionally shared with integration tests to prevent fixture drift.
Writing to disk is opt-in, exclusively inside a brand-new user-specified
directory; no existing files are overwritten.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from io import BytesIO
import json
from pathlib import Path

from openpyxl import Workbook

from aram_backend.cash_flow_direct_candidate import CashFlowEntry
from aram_backend.pilot_workbook import SHEET_HEADERS
from aram_backend.reconciliation_review import NoteReference

COMPANY = "001"
YEAR = 1404
DEMO_WORKBOOK = "ARAM-SYNTHETIC-ONLY.xlsx"
DEMO_MANIFEST = "ARAM-SYNTHETIC-ONLY.json"
DEMO_NOTICE = "READ-ME-SYNTHETIC-ONLY.txt"


def source_workbook() -> bytes:
    """One debit-net balanced ledger shared by every candidate builder."""
    book = Workbook()
    book.remove(book.active)
    for name, headers in SHEET_HEADERS.items():
        book.create_sheet(name).append(list(headers))

    def add(sheet: str, **values: object) -> None:
        book[sheet].append([values.get(column) for column in SHEET_HEADERS[sheet]])

    add(
        "Company", company_code=COMPANY, company_name="Synthetic integration only",
        fiscal_year=YEAR, currency="IRR", unit="Rial", prepared_by="Test fixture",
        status="Draft",
    )
    ledger = (
        # code, name, opening, debit, credit, closing
        ("CASH", "Cash", "40", "30", "20", "50"),
        ("AR", "Receivables", "50", "0", "0", "50"),
        ("AP", "Payables", "-20", "10", "0", "-10"),
        ("CAP", "Share capital", "-70", "0", "0", "-70"),
        ("REV", "Revenue", "0", "0", "40", "-40"),
        ("EXP", "Cost of revenue", "0", "20", "0", "20"),
    )
    for index, (code, name, opening, debit, credit, closing) in enumerate(ledger, 101):
        add(
            "Accounts", company_code=COMPANY, fiscal_year=YEAR,
            general_code=code, general_name=name, account_full_code=code,
            account_name=name, opening=opening, debit=debit, credit=credit,
            closing=closing, source_row=index, row_status="Draft",
            closing_delta="0",
        )

    notes = (
        ("BS", "Current assets", "C01", "Cash"),
        ("BS", "Current assets", "A01", "Receivables"),
        ("BS", "Current liabilities", "L01", "Payables"),
        ("BS", "Equity", "E01", "Equity"),
        ("IS", "Revenue", "R01", "Revenue"),
        ("IS", "Cost of revenue", "X01", "Cost of revenue"),
        ("EQ", "Share capital", "E01", "Share capital"),
        ("EQ", "Current year result", "P01", "Current year result"),
    )
    for statement, section, note, title in notes:
        add(
            "Notes", company_code=COMPANY, fiscal_year=YEAR,
            statement=statement, statement_section=section,
            note_number=note, note_title=title, subnote_code="",
            subnote_title="",
        )

    mappings = (
        ("CASH", "BS", "Current assets", "C01"),
        ("AR", "BS", "Current assets", "A01"),
        ("AP", "BS", "Current liabilities", "L01"),
        ("CAP", "BS", "Equity", "E01"),
        ("CAP", "EQ", "Share capital", "E01"),
        ("REV", "IS", "Revenue", "R01"),
        ("REV", "BS", "Equity", "E01"),
        ("REV", "EQ", "Current year result", "P01"),
        ("EXP", "IS", "Cost of revenue", "X01"),
        ("EXP", "BS", "Equity", "E01"),
        ("EXP", "EQ", "Current year result", "P01"),
    )
    for index, (account, statement, section, note) in enumerate(mappings, 1):
        add(
            "Mapping", mapping_id=f"SYNTH-M-{index:02d}",
            company_code=COMPANY, fiscal_year=YEAR,
            account_full_code=account, account_level="General",
            general_code=account, target_statement=statement,
            statement_section=section, note_number=note, subnote_code="",
            mapping_version=1, approval_status="Approved",
            reviewer="Synthetic fixture only", review_date="2026-10-31",
            source="Synthetic test", notes="Not an authenticated approval",
            validation_status="Valid",
        )

    output = BytesIO()
    book.save(output)
    book.close()
    return output.getvalue()


def references() -> tuple[NoteReference, ...]:
    return (
        NoteReference("BS", "Current assets", "C01", "", "50", "SYNTH-BS-CASH"),
        NoteReference("BS", "Current assets", "A01", "", "50", "SYNTH-BS-AR"),
        NoteReference("BS", "Current liabilities", "L01", "", "-10", "SYNTH-BS-AP"),
        NoteReference("BS", "Equity", "E01", "", "-90", "SYNTH-BS-EQ"),
        NoteReference("IS", "Revenue", "R01", "", "-40", "SYNTH-IS-REV"),
        NoteReference("IS", "Cost of revenue", "X01", "", "20", "SYNTH-IS-COST"),
        NoteReference("EQ", "Share capital", "E01", "", "-70", "SYNTH-EQ-CAP"),
        NoteReference("EQ", "Current year result", "P01", "", "-20", "SYNTH-EQ-PROFIT"),
    )


def cash_transactions() -> tuple[CashFlowEntry, ...]:
    return (
        CashFlowEntry(
            company_code=COMPANY, fiscal_year=YEAR, line_id="CF-L1",
            transaction_id="CF-V1", posting_date="1404-01-01",
            cash_account_code="CASH", counterpart_account_code="REV",
            cash_debit="30", cash_credit="0", counterpart_debit="0",
            counterpart_credit="30", evidence_ref="SYNTH-TXN-1",
        ),
        CashFlowEntry(
            company_code=COMPANY, fiscal_year=YEAR, line_id="CF-L2",
            transaction_id="CF-V2", posting_date="1404-01-02",
            cash_account_code="CASH", counterpart_account_code="EXP",
            cash_debit="0", cash_credit="20", counterpart_debit="20",
            counterpart_credit="0", evidence_ref="SYNTH-TXN-2",
        ),
    )


def pipeline_manifest(*, transactions=None):
    return {
        "schema_version": 1,
        "company_code": COMPANY,
        "fiscal_year": YEAR,
        "currency": "IRR",
        "unit": "Rial",
        "references": [asdict(item) for item in references()],
        "balance_sheet_policies": [
            {
                "statement_section": "Current assets", "note_number": "C01",
                "subnote_code": "", "category": "ASSETS", "sign_multiplier": 1,
                "line_label": "Cash and cash equivalents",
                "policy_evidence_ref": "SYNTH-POL-BS-CASH",
            },
            {
                "statement_section": "Current assets", "note_number": "A01",
                "subnote_code": "", "category": "ASSETS", "sign_multiplier": 1,
                "line_label": "Trade receivables", "policy_evidence_ref": "SYNTH-POL-BS-AR",
            },
            {
                "statement_section": "Current liabilities", "note_number": "L01",
                "subnote_code": "", "category": "LIABILITIES", "sign_multiplier": -1,
                "line_label": "Trade payables", "policy_evidence_ref": "SYNTH-POL-BS-AP",
            },
            {
                "statement_section": "Equity", "note_number": "E01",
                "subnote_code": "", "category": "EQUITY", "sign_multiplier": -1,
                "line_label": "Total equity", "policy_evidence_ref": "SYNTH-POL-BS-EQ",
            },
        ],
        "income_statement_policies": [
            {
                "statement_section": "Revenue", "note_number": "R01",
                "subnote_code": "", "category": "REVENUE", "sign_multiplier": -1,
                "line_label": "Revenue", "policy_evidence_ref": "SYNTH-POL-IS-REV",
            },
            {
                "statement_section": "Cost of revenue", "note_number": "X01",
                "subnote_code": "", "category": "COST_OF_REVENUE", "sign_multiplier": 1,
                "line_label": "Cost of revenue", "policy_evidence_ref": "SYNTH-POL-IS-COST",
            },
        ],
        "equity_movement_policies": [
            {
                "statement_section": "Share capital", "note_number": "E01",
                "subnote_code": "", "equity_component": "SHARE_CAPITAL",
                "movement_category": "CAPITAL_CONTRIBUTION", "sign_multiplier": -1,
                "line_label": "Share capital", "policy_evidence_ref": "SYNTH-POL-EQ-CAP",
            },
            {
                "statement_section": "Current year result", "note_number": "P01",
                "subnote_code": "", "equity_component": "RETAINED_EARNINGS",
                "movement_category": "NET_PROFIT_LOSS", "sign_multiplier": -1,
                "line_label": "Current year profit", "policy_evidence_ref": "SYNTH-POL-EQ-PROFIT",
            },
        ],
        "cash_accounts": [
            {"account_code": "CASH", "evidence_ref": "SYNTH-CASH-SCOPE"},
        ],
        "counterpart_policies": [
            {"account_code": "REV", "activity": "OPERATING", "evidence_ref": "SYNTH-REV-CLASS"},
            {"account_code": "EXP", "activity": "OPERATING", "evidence_ref": "SYNTH-EXP-CLASS"},
        ],
        "transactions": [
            asdict(item) for item in (
                cash_transactions() if transactions is None else transactions
            )
        ],
        "cash_balance_notes": [
            {
                "statement_section": "Current assets", "note_number": "C01",
                "subnote_code": "", "evidence_ref": "SYNTH-CASH-NOTE-SELECTION",
            },
        ],
    }


def write_demo_bundle(output_dir: str | Path) -> tuple[Path, Path]:
    """Write labeled, entirely artificial files into one NEW directory only.

    Do not silently replace or modify an existing location, including a
    symlink. The caller must specify the directory and opt in explicitly.
    """
    directory = Path(output_dir)
    if directory.exists() or directory.is_symlink():
        raise FileExistsError("DEMO_OUTPUT_DIRECTORY_MUST_NOT_EXIST")
    directory.mkdir(parents=True, exist_ok=False)
    workbook_path = directory / DEMO_WORKBOOK
    manifest_path = directory / DEMO_MANIFEST
    workbook_path.write_bytes(source_workbook())
    manifest_path.write_text(
        json.dumps(
            pipeline_manifest(), sort_keys=True, ensure_ascii=True, indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    (directory / DEMO_NOTICE).write_text(
        "ARAM SYNTHETIC TEST DATA ONLY.\n"
        "NOT A REAL COMPANY, FINANCIAL STATEMENT, APPROVAL OR SOURCE LEDGER.\n"
        "All accounts, amounts, policy references and journal lines are artificial.\n"
        "The demo result may show eligible_for_analyst_review=true only for\n"
        "software arithmetic testing. Never use it for accounting decisions.\n",
        encoding="utf-8",
    )
    return workbook_path, manifest_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an ARAM entirely synthetic Windows inspection demo"
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="New directory for synthetic XLSX, JSON and warning notice",
    )
    args = parser.parse_args(argv)
    try:
        workbook, manifest = write_demo_bundle(args.output_dir)
    except (OSError, ValueError) as exc:
        parser.exit(2, "ARAM_SYNTHETIC_DEMO_REFUSED: " + str(exc) + "\n")
    print("SYNTHETIC ONLY; not company data, financial approval or release.")
    print("Workbook:", workbook)
    print("Manifest:", manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
