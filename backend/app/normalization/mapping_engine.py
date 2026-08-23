from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

from backend.app.models.entities import (
    COAMappingRule,
    NormalizedFinancialRecord,
    StatementType,
)
from backend.app.services.protection import check_fiscal_year_mutable
from backend.app.accounting.calculator import AccountingCalculator


class COAMappingEngine:
    """Engine for Chart of Accounts mapping, template reuse, unmapped account detection, and review workflows."""

    def __init__(self, db: Session, year_id: int):
        self.db = db
        self.year_id = year_id

    def detect_unmapped_accounts(self) -> List[Dict[str, Any]]:
        """Identifies normalized records whose account codes do not have an approved COAMappingRule."""
        check_fiscal_year_mutable(self.db, self.year_id)

        approved_rules = (
            self.db.query(COAMappingRule)
            .filter(COAMappingRule.year_id == self.year_id, COAMappingRule.is_approved.is_(True))
            .all()
        )
        approved_codes = {r.account_code for r in approved_rules}

        records = (
            self.db.query(NormalizedFinancialRecord)
            .filter(NormalizedFinancialRecord.year_id == self.year_id)
            .all()
        )

        unmapped = []
        seen_codes = set()
        for rec in records:
            if rec.account_code not in approved_codes and rec.account_code not in seen_codes:
                seen_codes.add(rec.account_code)
                calc = AccountingCalculator()
                auto_class = calc.classify_account(rec.account_code, target_statement="BS")
                unmapped.append({
                    "account_code": rec.account_code,
                    "account_name": rec.account_name,
                    "suggested_statement": auto_class["group_name"],
                    "suggested_section": auto_class["section"],
                })

        return unmapped

    def save_mapping_rule(
        self,
        account_code: str,
        account_name: str,
        target_statement: StatementType,
        statement_section: str,
        group_name: str,
        is_approved: bool = True,
    ) -> COAMappingRule:
        """Saves or updates a COAMappingRule for a specific fiscal year."""
        check_fiscal_year_mutable(self.db, self.year_id)

        rule = (
            self.db.query(COAMappingRule)
            .filter(COAMappingRule.year_id == self.year_id, COAMappingRule.account_code == account_code)
            .first()
        )
        if not rule:
            rule = COAMappingRule(
                year_id=self.year_id,
                account_code=account_code,
                account_name=account_name,
                target_statement=target_statement,
                statement_section=statement_section,
                group_name=group_name,
                is_approved=is_approved,
            )
            self.db.add(rule)
        else:
            rule.account_name = account_name
            rule.target_statement = target_statement
            rule.statement_section = statement_section
            rule.group_name = group_name
            rule.is_approved = is_approved

        self.db.commit()
        self.db.refresh(rule)
        return rule

    def copy_template_from_year(self, source_year_id: int) -> int:
        """Copies approved COAMappingRules from a previous fiscal year (e.g., 1402 to 1403) for template reuse."""
        check_fiscal_year_mutable(self.db, self.year_id)

        source_rules = (
            self.db.query(COAMappingRule)
            .filter(COAMappingRule.year_id == source_year_id, COAMappingRule.is_approved.is_(True))
            .all()
        )

        copied_count = 0
        for s in source_rules:
            existing = (
                self.db.query(COAMappingRule)
                .filter(COAMappingRule.year_id == self.year_id, COAMappingRule.account_code == s.account_code)
                .first()
            )
            if not existing:
                new_rule = COAMappingRule(
                    year_id=self.year_id,
                    account_code=s.account_code,
                    account_name=s.account_name,
                    target_statement=s.target_statement,
                    statement_section=s.statement_section,
                    group_name=s.group_name,
                    is_approved=True,
                )
                self.db.add(new_rule)
                copied_count += 1

        self.db.commit()
        return copied_count
