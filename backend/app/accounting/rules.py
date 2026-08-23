from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class AccountGroupRule(BaseModel):
    group_name: str
    code_prefix: Optional[str] = None
    account_codes: Optional[List[str]] = None
    target_statement: str  # TB, BS, IS
    statement_section: str  # e.g., Current Assets, Non-Current Assets, Revenues, Expenses


class AccountingRuleConfig(BaseModel):
    version: str = "1.0"
    group_rules: List[AccountGroupRule] = []


DEFAULT_ACCOUNTING_RULES = AccountingRuleConfig(
    group_rules=[
        # Balance Sheet - Assets
        AccountGroupRule(group_name="Cash and Cash Equivalents", code_prefix="11", target_statement="BS", statement_section="Current Assets"),
        AccountGroupRule(group_name="Trade Receivables", code_prefix="12", target_statement="BS", statement_section="Current Assets"),
        AccountGroupRule(group_name="Inventories", code_prefix="13", target_statement="BS", statement_section="Current Assets"),
        AccountGroupRule(group_name="Property, Plant & Equipment", code_prefix="21", target_statement="BS", statement_section="Non-Current Assets"),
        # Balance Sheet - Liabilities & Equity
        AccountGroupRule(group_name="Trade Payables", code_prefix="31", target_statement="BS", statement_section="Current Liabilities"),
        AccountGroupRule(group_name="Short-term Loans", code_prefix="32", target_statement="BS", statement_section="Current Liabilities"),
        AccountGroupRule(group_name="Long-term Debt", code_prefix="41", target_statement="BS", statement_section="Non-Current Liabilities"),
        AccountGroupRule(group_name="Share Capital", code_prefix="51", target_statement="BS", statement_section="Equity"),
        AccountGroupRule(group_name="Retained Earnings", code_prefix="52", target_statement="BS", statement_section="Equity"),
        # Income Statement
        AccountGroupRule(group_name="Operating Revenue", code_prefix="61", target_statement="IS", statement_section="Revenues"),
        AccountGroupRule(group_name="Cost of Goods Sold", code_prefix="71", target_statement="IS", statement_section="Cost of Sales"),
        AccountGroupRule(group_name="Administrative Expenses", code_prefix="81", target_statement="IS", statement_section="Operating Expenses"),
        AccountGroupRule(group_name="Finance Costs", code_prefix="91", target_statement="IS", statement_section="Finance Expenses"),
    ]
)
