from typing import List, Dict, Any
from backend.app.models.entities import NormalizedFinancialRecord
from backend.app.accounting.rules import AccountingRuleConfig, DEFAULT_ACCOUNTING_RULES


class AccountingCalculator:
    """Calculates aggregates and group totals from normalized financial records."""
    def __init__(self, rule_config: AccountingRuleConfig = None):
        self.config = rule_config or DEFAULT_ACCOUNTING_RULES

    def aggregate_records(self, records: List[NormalizedFinancialRecord]) -> Dict[str, Dict[str, Any]]:
        """Aggregates debit/credit and net totals grouped by unique account_code."""
        aggregated: Dict[str, Dict[str, Any]] = {}

        for rec in records:
            code = rec.account_code or "UNKNOWN"
            if code not in aggregated:
                aggregated[code] = {
                    "account_code": code,
                    "account_name": rec.account_name or "",
                    "total_debit": 0.0,
                    "total_credit": 0.0,
                    "net_balance": 0.0,
                    "t1": rec.t1,
                    "t2": rec.t2,
                    "t3": rec.t3,
                    "t4": rec.t4,
                    "record_count": 0,
                }

            debit_val = float(rec.debit) if rec.debit is not None else 0.0
            credit_val = float(rec.credit) if rec.credit is not None else 0.0
            net_val = float(rec.net_amount) if rec.net_amount is not None else (debit_val - credit_val)

            aggregated[code]["total_debit"] += debit_val
            aggregated[code]["total_credit"] += credit_val
            aggregated[code]["net_balance"] += net_val
            aggregated[code]["record_count"] += 1

        return aggregated

    def classify_account(self, account_code: str, target_statement: str) -> Dict[str, str]:
        """Classifies an account code into a statement section using rules config."""
        for rule in self.config.group_rules:
            if rule.target_statement == target_statement:
                if rule.account_codes and account_code in rule.account_codes:
                    return {"group_name": rule.group_name, "section": rule.statement_section}
                if rule.code_prefix and account_code.startswith(rule.code_prefix):
                    return {"group_name": rule.group_name, "section": rule.statement_section}
        return {"group_name": "Unclassified", "section": "Other"}
