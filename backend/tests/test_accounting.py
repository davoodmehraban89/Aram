import pytest
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    SourceDocument,
    NormalizedFinancialRecord,
)
from backend.app.accounting.rules import AccountingRuleConfig, AccountGroupRule
from backend.app.accounting.calculator import AccountingCalculator
from backend.app.accounting.statements import StatementGenerator
from backend.app.accounting.service import generate_financial_statements


def test_debit_credit_aggregation():
    records = [
        NormalizedFinancialRecord(account_code="1101", account_name="Cash", debit=500.0, credit=0.0, net_amount=500.0),
        NormalizedFinancialRecord(account_code="1101", account_name="Cash", debit=300.0, credit=100.0, net_amount=200.0),
    ]
    calc = AccountingCalculator()
    aggregated = calc.aggregate_records(records)

    assert "1101" in aggregated
    assert aggregated["1101"]["total_debit"] == 800.0
    assert aggregated["1101"]["total_credit"] == 100.0
    assert aggregated["1101"]["net_balance"] == 700.0


def test_account_grouping():
    calc = AccountingCalculator()
    classification = calc.classify_account("1101", target_statement="BS")
    assert classification["group_name"] == "Cash and Cash Equivalents"
    assert classification["section"] == "Current Assets"


def test_trial_balance_generation():
    records = [
        NormalizedFinancialRecord(account_code="1101", account_name="Cash", debit=1000.0, credit=0.0, net_amount=1000.0),
        NormalizedFinancialRecord(account_code="3101", account_name="Payables", debit=0.0, credit=1000.0, net_amount=-1000.0),
    ]
    generator = StatementGenerator()
    tb = generator.generate_trial_balance(records)

    assert tb["statement_type"] == "TB"
    assert tb["total_debit"] == 1000.0
    assert tb["total_credit"] == 1000.0
    assert tb["is_balanced"] is True


def test_balance_sheet_generation():
    records = [
        NormalizedFinancialRecord(account_code="1101", account_name="Cash", debit=500.0, credit=0.0, net_amount=500.0),
        NormalizedFinancialRecord(account_code="3101", account_name="Payables", debit=0.0, credit=300.0, net_amount=300.0),
        NormalizedFinancialRecord(account_code="5101", account_name="Capital", debit=0.0, credit=200.0, net_amount=200.0),
    ]
    generator = StatementGenerator()
    bs = generator.generate_balance_sheet(records)

    assert bs["statement_type"] == "BS"
    assert bs["total_assets"] == 500.0
    assert bs["total_liabilities"] == 300.0
    assert bs["total_equity"] == 200.0
    assert bs["is_balanced"] is True


def test_income_statement_generation():
    records = [
        NormalizedFinancialRecord(account_code="6101", account_name="Sales", debit=0.0, credit=1000.0, net_amount=1000.0),
        NormalizedFinancialRecord(account_code="7101", account_name="COGS", debit=400.0, credit=0.0, net_amount=400.0),
        NormalizedFinancialRecord(account_code="8101", account_name="Rent", debit=100.0, credit=0.0, net_amount=100.0),
    ]
    generator = StatementGenerator()
    is_stmt = generator.generate_income_statement(records)

    assert is_stmt["statement_type"] == "IS"
    assert is_stmt["total_revenues"] == 1000.0
    assert is_stmt["total_cost_of_sales"] == 400.0
    assert is_stmt["gross_profit"] == 600.0
    assert is_stmt["operating_profit"] == 500.0


def test_invalid_data_handling():
    records = [
        NormalizedFinancialRecord(account_code=None, account_name=None, debit=None, credit=None, net_amount=None),
    ]
    calc = AccountingCalculator()
    aggregated = calc.aggregate_records(records)

    assert "UNKNOWN" in aggregated
    assert aggregated["UNKNOWN"]["total_debit"] == 0.0
    assert aggregated["UNKNOWN"]["total_credit"] == 0.0


def test_fiscal_year_isolation_in_accounting_service(db_session):
    comp = Company(code="ACC1", name="Accounting Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    doc1402 = SourceDocument(year_id=fy1402.id, filename="ledger1402.csv", file_hash="h1402", doc_type="ledger")
    doc1403 = SourceDocument(year_id=fy1403.id, filename="ledger1403.csv", file_hash="h1403", doc_type="ledger")
    db_session.add_all([doc1402, doc1403])
    db_session.commit()

    rec1402 = NormalizedFinancialRecord(
        year_id=fy1402.id,
        source_document_id=doc1402.id,
        row_index=1,
        account_code="1101",
        account_name="Cash 1402",
        debit=100.0,
        credit=0.0,
        net_amount=100.0,
    )
    rec1403 = NormalizedFinancialRecord(
        year_id=fy1403.id,
        source_document_id=doc1403.id,
        row_index=1,
        account_code="1101",
        account_name="Cash 1403",
        debit=500.0,
        credit=0.0,
        net_amount=500.0,
    )
    db_session.add_all([rec1402, rec1403])
    db_session.commit()

    res1402 = generate_financial_statements(db_session, year_id=fy1402.id)
    res1403 = generate_financial_statements(db_session, year_id=fy1403.id)

    assert res1402["record_count"] == 1
    assert res1402["trial_balance"]["total_debit"] == 100.0

    assert res1403["record_count"] == 1
    assert res1403["trial_balance"]["total_debit"] == 500.0


def test_custom_accounting_rules():
    custom_rules = AccountingRuleConfig(
        group_rules=[
            AccountGroupRule(
                group_name="Custom Group",
                account_codes=["SPECIAL_CODE"],
                target_statement="BS",
                statement_section="Current Assets",
            )
        ]
    )
    calc = AccountingCalculator(custom_rules)
    classification = calc.classify_account("SPECIAL_CODE", target_statement="BS")
    assert classification["group_name"] == "Custom Group"


def test_unclassified_account_fallback():
    calc = AccountingCalculator()
    classification = calc.classify_account("999999", target_statement="BS")
    assert classification["group_name"] == "Unclassified"
    assert classification["section"] == "Other"


def test_balanced_statement_tolerances():
    records = [
        NormalizedFinancialRecord(account_code="1101", account_name="Cash", debit=100.004, credit=0.0, net_amount=100.004),
        NormalizedFinancialRecord(account_code="3101", account_name="Payable", debit=0.0, credit=100.001, net_amount=-100.001),
    ]
    generator = StatementGenerator()
    tb = generator.generate_trial_balance(records)
    assert tb["is_balanced"] is True
