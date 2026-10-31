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
from aram_backend.synthetic_five_statement_demo import (
    COMPANY, YEAR, cash_transactions, pipeline_manifest,
    references, source_workbook,
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

