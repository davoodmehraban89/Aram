"""End-to-end synthetic integration tests for all five ARAM statement engines."""
from __future__ import annotations

from io import BytesIO

import pytest
from openpyxl import Workbook

from aram_backend.balance_sheet_candidate import (
    BalanceSheetLinePolicy, build_balance_sheet_candidate,
)
from aram_backend.cash_flow_direct_candidate import (
    CashAccountPolicy, CashCounterpartPolicy, CashFlowEntry,
    build_direct_cash_flow_candidate,
)
from aram_backend.cross_statement_reconciliation import (
    CashBalanceNoteSelection, reconcile_cross_statements,
)
from aram_backend.equity_changes_candidate import (
    EquityMovementPolicy, build_equity_changes_candidate,
)
from aram_backend.income_statement_candidate import (
    IncomeStatementLinePolicy, build_income_statement_candidate,
)
from aram_backend.pilot_workbook import SHEET_HEADERS
from aram_backend.reconciliation_review import NoteReference
from aram_backend.trial_balance_diagnostic import analyze_trial_balance


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


def build_all(data: bytes | None = None, *, transactions=None):
    source = source_workbook() if data is None else data
    refs = references()
    balance_sheet = build_balance_sheet_candidate(
        source, company_code=COMPANY, fiscal_year=YEAR, references=refs,
        policies=(
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
    )
    income_statement = build_income_statement_candidate(
        source, company_code=COMPANY, fiscal_year=YEAR, references=refs,
        policies=(
            IncomeStatementLinePolicy(
                "Revenue", "R01", "", "REVENUE", -1,
                "Revenue", "SYNTH-POL-IS-REV",
            ),
            IncomeStatementLinePolicy(
                "Cost of revenue", "X01", "", "COST_OF_REVENUE", 1,
                "Cost of revenue", "SYNTH-POL-IS-COST",
            ),
        ),
    )
    equity_changes = build_equity_changes_candidate(
        source, company_code=COMPANY, fiscal_year=YEAR, references=refs,
        policies=(
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
    )
    cash_flow = build_direct_cash_flow_candidate(
        source, company_code=COMPANY, fiscal_year=YEAR,
        currency="IRR", unit="Rial",
        cash_accounts=(CashAccountPolicy("CASH", "SYNTH-CASH-SCOPE"),),
        counterpart_policies=(
            CashCounterpartPolicy("REV", "OPERATING", "SYNTH-REV-CLASS"),
            CashCounterpartPolicy("EXP", "OPERATING", "SYNTH-EXP-CLASS"),
        ),
        transactions=cash_transactions() if transactions is None else transactions,
    )
    trial_balance = analyze_trial_balance(
        source, company_code=COMPANY, fiscal_year=YEAR,
    )
    result = reconcile_cross_statements(
        balance_sheet=balance_sheet, income_statement=income_statement,
        equity_changes=equity_changes, cash_flow=cash_flow,
        trial_balance=trial_balance,
        cash_balance_notes=(
            CashBalanceNoteSelection(
                "Current assets", "C01", "", "SYNTH-CASH-NOTE-SELECTION",
            ),
        ),
    )
    return (
        balance_sheet, income_statement, equity_changes,
        cash_flow, trial_balance, result,
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
