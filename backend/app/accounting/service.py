from typing import Dict, Any, List
from sqlalchemy.orm import Session

from backend.app.models.entities import NormalizedFinancialRecord
from backend.app.services.protection import check_fiscal_year_mutable
from backend.app.accounting.calculator import AccountingCalculator
from backend.app.accounting.statements import StatementGenerator
from backend.app.accounting.rules import AccountingRuleConfig


def generate_financial_statements(
    db: Session,
    year_id: int,
    rule_config: AccountingRuleConfig = None,
) -> Dict[str, Any]:
    """
    Fetches NormalizedFinancialRecord rows for the specified year_id,
    and calculates Trial Balance, Balance Sheet, and Income Statement foundations.
    Enforces fiscal year lookup and returns isolated statement calculations.
    """
    records = db.query(NormalizedFinancialRecord).filter(NormalizedFinancialRecord.year_id == year_id).all()

    calculator = AccountingCalculator(rule_config)
    generator = StatementGenerator(calculator)

    tb = generator.generate_trial_balance(records)
    bs = generator.generate_balance_sheet(records)
    statement_is = generator.generate_income_statement(records)

    return {
        "year_id": year_id,
        "record_count": len(records),
        "trial_balance": tb,
        "balance_sheet": bs,
        "income_statement": statement_is,
    }
