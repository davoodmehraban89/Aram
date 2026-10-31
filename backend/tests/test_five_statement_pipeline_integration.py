"""End-to-end synthetic integration tests for all five ARAM statement engines."""
from __future__ import annotations

from dataclasses import asdict
from io import BytesIO
import json

import pytest
from openpyxl import Workbook

from aram_backend.balance_sheet_candidate import BalanceSheetLinePolicy
from aram_backend.cash_flow_direct_candidate import (
    CashAccountPolicy, CashCounterpartPolicy, CashFlowEntry,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.cross_statement_reconciliation import CashBalanceNoteSelection
from aram_backend.equity_changes_candidate import EquityMovementPolicy
from aram_backend.income_statement_candidate import IncomeStatementLinePolicy
from aram_backend.pilot_workbook import SHEET_HEADERS
from aram_backend.reconciliation_review import NoteReference
from aram_backend.five_statement_pipeline import build_five_statement_pipeline
from aram_backend.five_statement_pipeline_cli import main as pipeline_cli_main


COMPANY = "001"
YEAR = 1404


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


def build_pipeline(
    data: bytes | None = None, *, transactions=None, refs=None,
):
    source = source_workbook() if data is None else data
    return build_five_statement_pipeline(
        source, company_code=COMPANY, fiscal_year=YEAR,
        references=references() if refs is None else refs,
        balance_sheet_policies=(
            BalanceSheetLinePolicy(
                "Current assets", "C01", "", "ASSETS", 1,
                "Cash and cash equivalents", "SYNTH-POL-BS-CASH",
            ),
            BalanceSheetLinePolicy(
                "Current assets", "A01", "", "ASSETS", 1,
                "Trade receivables", "SYNTH-POL-BS-AR",
            ),
            BalanceSheetLinePolicy(
                "Current liabilities", "L01", "", "LIABILITIES", -1,
                "Trade payables", "SYNTH-POL-BS-AP",
            ),
            BalanceSheetLinePolicy(
                "Equity", "E01", "", "EQUITY", -1,
                "Total equity", "SYNTH-POL-BS-EQ",
            ),
        ),
        income_statement_policies=(
            IncomeStatementLinePolicy(
                "Revenue", "R01", "", "REVENUE", -1,
                "Revenue", "SYNTH-POL-IS-REV",
            ),
            IncomeStatementLinePolicy(
                "Cost of revenue", "X01", "", "COST_OF_REVENUE", 1,
                "Cost of revenue", "SYNTH-POL-IS-COST",
            ),
        ),
        equity_movement_policies=(
            EquityMovementPolicy(
                "Share capital", "E01", "", "SHARE_CAPITAL",
                "CAPITAL_CONTRIBUTION", -1, "Share capital",
                "SYNTH-POL-EQ-CAP",
            ),
            EquityMovementPolicy(
                "Current year result", "P01", "", "RETAINED_EARNINGS",
                "NET_PROFIT_LOSS", -1, "Current year profit",
                "SYNTH-POL-EQ-PROFIT",
            ),
        ),
        currency="IRR", unit="Rial",
        cash_accounts=(CashAccountPolicy("CASH", "SYNTH-CASH-SCOPE"),),
        counterpart_policies=(
            CashCounterpartPolicy("REV", "OPERATING", "SYNTH-REV-CLASS"),
            CashCounterpartPolicy("EXP", "OPERATING", "SYNTH-EXP-CLASS"),
        ),
        transactions=cash_transactions() if transactions is None else transactions,
        cash_balance_notes=(
            CashBalanceNoteSelection(
                "Current assets", "C01", "", "SYNTH-CASH-NOTE-SELECTION",
            ),
        ),
    )


def build_all(data: bytes | None = None, *, transactions=None):
    pipeline = build_pipeline(data, transactions=transactions)
    return (
        pipeline.balance_sheet, pipeline.income_statement,
        pipeline.equity_changes, pipeline.cash_flow,
        pipeline.trial_balance, pipeline.reconciliation,
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



def test_all_five_real_builders_reconcile_from_one_immutable_workbook():
    bs, income, equity, cash, trial, result = build_all()

    assert bs.eligible_for_analyst_review and not bs.findings
    assert income.eligible_for_analyst_review and not income.findings
    assert equity.eligible_for_analyst_review and not equity.findings
    assert cash.eligible_for_analyst_review and not cash.findings
    assert trial.balanced_for_analyst_review and not trial.findings
    assert len({item.source_sha256 for item in (bs, income, equity, cash, trial)}) == 1
    assert len({
        bs.note_references_sha256,
        income.note_references_sha256,
        equity.note_references_sha256,
    }) == 1

    assert bs.assets_total == "100"
    assert bs.liabilities_total == "10"
    assert bs.equity_total == "90"
    assert income.net_result == "20"
    assert equity.opening_equity_total == "70"
    assert equity.net_profit_loss_movements == "20"
    assert equity.closing_equity_total == "90"
    assert cash.opening_cash_and_equivalents == "40"
    assert cash.net_change_in_cash == "10"
    assert cash.closing_cash_and_equivalents == "50"
    assert trial.opening_debit_net_total == "0"
    assert trial.debit_turnover_total == "60"
    assert trial.credit_turnover_total == "60"
    assert trial.closing_debit_net_total == "0"

    assert result.eligible_for_analyst_review
    assert result.findings == ()
    assert result.balance_sheet_equity_difference == "0"
    assert result.net_profit_equity_difference == "0"
    assert result.balance_sheet_cash_difference == "0"
    assert result.cash_accounts_match_trial_balance
    assert result.cash_account_totals_valid
    assert not result.source_ledger_completeness_verified
    assert not result.accounting_policy_authorized
    assert not result.independently_reviewed
    assert not result.official_financial_statement
    assert not result.export_authorized
    assert not result.releasable


def test_missing_cash_transaction_blocks_real_five_statement_pipeline():
    bs, income, equity, cash, trial, result = build_all(
        transactions=cash_transactions()[:-1],
    )
    assert bs.eligible_for_analyst_review
    assert income.eligible_for_analyst_review
    assert equity.eligible_for_analyst_review
    assert trial.balanced_for_analyst_review
    assert not cash.eligible_for_analyst_review
    assert not result.eligible_for_analyst_review
    assert "CASH_FLOW_CANDIDATE_BLOCKED" in result.findings
    assert "CASH_FLOW_BRIDGE_INVALID" in result.findings or "CASH_ACCOUNT_TURNOVER_OR_TOTALS_INVALID" in result.findings


def test_pipeline_result_is_nonofficial_and_freezes_reference_collection():
    result = build_pipeline()
    payload = result.to_dict()
    assert result.eligible_for_analyst_review
    assert payload["kind"] == "UNAPPROVED_FIVE_STATEMENT_PIPELINE_CANDIDATE"
    assert payload["source_sha256"] == result.source_sha256
    for flag in (
        "source_ledger_completeness_verified", "accounting_policy_authorized",
        "independently_reviewed", "trusted_approvals",
        "official_financial_statement", "export_authorized", "releasable",
    ):
        assert payload[flag] is False

    with pytest.raises(CoverageError) as error:
        build_pipeline(refs=iter(references()))
    assert error.value.code == "INVALID_FIVE_STATEMENT_NOTE_REFERENCES"


def test_offline_pipeline_cli_emits_json_without_creating_output_files(tmp_path, capsys):
    workbook_path = tmp_path / "synthetic.xlsx"
    manifest_path = tmp_path / "pipeline.json"
    workbook_path.write_bytes(source_workbook())
    manifest_path.write_text(
        json.dumps(pipeline_manifest(), ensure_ascii=True),
        encoding="utf-8",
    )

    exit_code = pipeline_cli_main([
        "--file", str(workbook_path), "--manifest", str(manifest_path),
    ])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["eligible_for_analyst_review"] is True
    assert payload["kind"] == "UNAPPROVED_FIVE_STATEMENT_PIPELINE_CANDIDATE"
    assert payload["official_financial_statement"] is False
    assert payload["releasable"] is False
    assert {item.name for item in tmp_path.iterdir()} == {
        "synthetic.xlsx", "pipeline.json",
    }


def test_offline_pipeline_cli_returns_blocked_exit_for_incomplete_transactions(
    tmp_path, capsys,
):
    workbook_path = tmp_path / "synthetic.xlsx"
    manifest_path = tmp_path / "pipeline.json"
    workbook_path.write_bytes(source_workbook())
    manifest_path.write_text(
        json.dumps(pipeline_manifest(transactions=cash_transactions()[:-1])),
        encoding="utf-8",
    )

    exit_code = pipeline_cli_main([
        "--file", str(workbook_path), "--manifest", str(manifest_path),
    ])
    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 3
    assert payload["eligible_for_analyst_review"] is False
    assert "CASH_FLOW_CANDIDATE_BLOCKED" in payload["findings"]


def test_pipeline_manifest_rejects_duplicate_keys_and_nonfinite_numbers():
    from aram_backend.five_statement_pipeline_cli import parse_pipeline_manifest

    with pytest.raises(CoverageError) as duplicate:
        parse_pipeline_manifest(b'{"schema_version":1,"schema_version":1}')
    assert duplicate.value.code == "DUPLICATE_MANIFEST_KEY"

    document = pipeline_manifest()
    document["fiscal_year"] = float("nan")
    with pytest.raises(CoverageError) as nonfinite:
        parse_pipeline_manifest(json.dumps(document).encode("utf-8"))
    assert nonfinite.value.code == "PIPELINE_MANIFEST_NONFINITE_NUMBER"


def test_pipeline_manifest_rejects_unknown_fields_and_missing_cash_registry():
    from aram_backend.five_statement_pipeline_cli import parse_pipeline_manifest

    document = pipeline_manifest()
    document["unexpected"] = True
    with pytest.raises(CoverageError) as unknown:
        parse_pipeline_manifest(json.dumps(document).encode("utf-8"))
    assert unknown.value.code == "PIPELINE_MANIFEST_SCHEMA_INVALID"

    document = pipeline_manifest()
    document["cash_accounts"] = []
    with pytest.raises(CoverageError) as missing:
        parse_pipeline_manifest(json.dumps(document).encode("utf-8"))
    assert missing.value.code == "PIPELINE_MANIFEST_CASH_ACCOUNTS_INVALID"

