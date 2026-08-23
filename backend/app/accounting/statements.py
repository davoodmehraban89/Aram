from typing import List, Dict, Any
from backend.app.models.entities import NormalizedFinancialRecord
from backend.app.accounting.calculator import AccountingCalculator
from backend.app.accounting.rules import AccountingRuleConfig


class StatementGenerator:
    """Generates Trial Balance, Balance Sheet, and Income Statement structures."""
    def __init__(self, calculator: AccountingCalculator = None):
        self.calculator = calculator or AccountingCalculator()

    def generate_trial_balance(self, records: List[NormalizedFinancialRecord]) -> Dict[str, Any]:
        """Generates Trial Balance foundation."""
        aggregated = self.calculator.aggregate_records(records)
        rows = list(aggregated.values())

        total_debit = sum(r["total_debit"] for r in rows)
        total_credit = sum(r["total_credit"] for r in rows)
        net_difference = total_debit - total_credit

        return {
            "statement_type": "TB",
            "title": "Trial Balance",
            "rows": rows,
            "total_debit": round(total_debit, 2),
            "total_credit": round(total_credit, 2),
            "is_balanced": abs(net_difference) < 0.01,
            "net_difference": round(net_difference, 2),
        }

    def generate_balance_sheet(self, records: List[NormalizedFinancialRecord]) -> Dict[str, Any]:
        """Generates Balance Sheet foundation."""
        aggregated = self.calculator.aggregate_records(records)
        sections: Dict[str, Dict[str, float]] = {
            "Current Assets": {},
            "Non-Current Assets": {},
            "Current Liabilities": {},
            "Non-Current Liabilities": {},
            "Equity": {},
            "Other": {},
        }

        for code, data in aggregated.items():
            classification = self.calculator.classify_account(code, target_statement="BS")
            sec = classification["section"]
            group = classification["group_name"]

            if sec not in sections:
                sections[sec] = {}
            if group not in sections[sec]:
                sections[sec][group] = 0.0

            sections[sec][group] += data["net_balance"]

        total_assets = (
            sum(sections["Current Assets"].values()) +
            sum(sections["Non-Current Assets"].values())
        )
        total_liabilities = (
            sum(sections["Current Liabilities"].values()) +
            sum(sections["Non-Current Liabilities"].values())
        )
        total_equity = sum(sections["Equity"].values())

        return {
            "statement_type": "BS",
            "title": "Balance Sheet Foundation",
            "sections": sections,
            "total_assets": round(total_assets, 2),
            "total_liabilities": round(total_liabilities, 2),
            "total_equity": round(total_equity, 2),
            "is_balanced": abs(total_assets - (total_liabilities + total_equity)) < 0.01,
        }

    def generate_income_statement(self, records: List[NormalizedFinancialRecord]) -> Dict[str, Any]:
        """Generates Income Statement foundation."""
        aggregated = self.calculator.aggregate_records(records)
        sections: Dict[str, Dict[str, float]] = {
            "Revenues": {},
            "Cost of Sales": {},
            "Operating Expenses": {},
            "Finance Expenses": {},
            "Other": {},
        }

        for code, data in aggregated.items():
            classification = self.calculator.classify_account(code, target_statement="IS")
            sec = classification["section"]
            group = classification["group_name"]

            if sec not in sections:
                sections[sec] = {}
            if group not in sections[sec]:
                sections[sec][group] = 0.0

            sections[sec][group] += data["net_balance"]

        total_revenues = sum(sections["Revenues"].values())
        total_cos = sum(sections["Cost of Sales"].values())
        gross_profit = total_revenues - total_cos
        total_opex = sum(sections["Operating Expenses"].values())
        operating_profit = gross_profit - total_opex
        total_finance = sum(sections["Finance Expenses"].values())
        net_profit = operating_profit - total_finance

        return {
            "statement_type": "IS",
            "title": "Income Statement Foundation",
            "sections": sections,
            "total_revenues": round(total_revenues, 2),
            "total_cost_of_sales": round(total_cos, 2),
            "gross_profit": round(gross_profit, 2),
            "operating_profit": round(operating_profit, 2),
            "net_profit": round(net_profit, 2),
        }
