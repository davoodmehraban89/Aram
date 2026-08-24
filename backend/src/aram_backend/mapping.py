from sqlalchemy import select
from sqlalchemy.orm import Session
from aram_backend.models import (
    MappingRule, MappingStatus, AccountVersion, NoteDefinition, FiscalYear, FiscalYearStatus
)

class MappingValidationError(ValueError):
    """Raised when a mapping rule cannot be safely validated."""

def create_mapping_rule(
    session: Session,
    *,
    year_id: int,
    rule_key: str,
    account_code: str,
    target_note_id: int,
    mapping_type: str,
    version: int = 1
) -> MappingRule:
    # Validate year exists
    year = session.get(FiscalYear, year_id)
    if not year:
        raise MappingValidationError(f"Fiscal year {year_id} does not exist.")
    if year.status != FiscalYearStatus.DRAFT:
         raise MappingValidationError(f"Fiscal year {year_id} is {year.status.value.lower()} and cannot accept mapping changes.")

    # Validate account exists
    account = session.scalar(
        select(AccountVersion).where(
            AccountVersion.year_id == year_id,
            AccountVersion.account_code == account_code
        )
    )
    if not account:
        raise MappingValidationError(f"Account {account_code} does not exist in year {year_id}.")

    # Validate target note exists and is for same year
    note = session.get(NoteDefinition, target_note_id)
    if not note or note.year_id != year_id:
        raise MappingValidationError(f"Target note {target_note_id} is invalid for year {year_id}.")

    # Validate duplicates
    existing = session.scalar(
        select(MappingRule).where(
            MappingRule.year_id == year_id,
            MappingRule.rule_key == rule_key,
            MappingRule.version == version
        )
    )
    if existing:
        raise MappingValidationError(f"Mapping rule {rule_key} version {version} already exists.")

    mapping_rule = MappingRule(
        year_id=year_id,
        rule_key=rule_key,
        account_code=account_code,
        target_note_id=target_note_id,
        mapping_type=mapping_type,
        version=version,
        status=MappingStatus.DRAFT
    )

    session.add(mapping_rule)
    session.flush()
    return mapping_rule
