"""Governed, year-isolated mapping persistence; never infer financial targets."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from aram_backend.models import AccountVersion, FiscalYear, FiscalYearStatus, MappingRule, NoteDefinition


class MappingValidationError(ValueError):
    """Mapping would violate a fiscal-year or explicit-review boundary."""


def save_mapping_rule(
    session: Session, *, year_id: int, rule_key: str, account_code: str,
    target_note_id: int, mapping_type: str, version: int = 1,
) -> MappingRule:
    """Persist an explicit mapping for a draft year, leaving commit to the caller.

    Repeated identical requests are idempotent; conflicting versions are rejected.
    No account, note, or mapping target is guessed from ledger data.
    """
    if isinstance(year_id, bool) or not isinstance(year_id, int) or year_id <= 0:
        raise MappingValidationError("year_id must be a positive integer")
    if isinstance(version, bool) or not isinstance(version, int) or version <= 0:
        raise MappingValidationError("version must be a positive integer")
    for label, value, limit in (
        ("rule_key", rule_key, 128), ("account_code", account_code, 64),
        ("mapping_type", mapping_type, 32),
    ):
        if not isinstance(value, str) or not value or value != value.strip() or len(value) > limit:
            raise MappingValidationError(f"{label} must be nonempty, trimmed and at most {limit} characters")
    if isinstance(target_note_id, bool) or not isinstance(target_note_id, int) or target_note_id <= 0:
        raise MappingValidationError("target_note_id must be a positive integer")

    year = session.get(FiscalYear, year_id)
    if year is None or year.status is not FiscalYearStatus.DRAFT:
        raise MappingValidationError("fiscal year must exist and be Draft")
    note = session.get(NoteDefinition, target_note_id)
    if note is None or note.year_id != year_id:
        raise MappingValidationError("target note must belong to the same fiscal year")
    account = session.scalar(select(AccountVersion.id).where(
        AccountVersion.year_id == year_id, AccountVersion.account_code == account_code,
    ).limit(1))
    if account is None:
        raise MappingValidationError("account code must exist in the same fiscal year")

    existing = session.scalar(select(MappingRule).where(
        MappingRule.year_id == year_id,
        MappingRule.rule_key == rule_key,
        MappingRule.version == version,
    ))
    if existing is not None:
        if (existing.account_code, existing.target_note_id, existing.mapping_type) != (
            account_code, target_note_id, mapping_type
        ):
            raise MappingValidationError("mapping version conflicts with an existing rule")
        return existing

    rule = MappingRule(year_id=year_id, rule_key=rule_key, version=version,
                       account_code=account_code, target_note_id=target_note_id,
                       mapping_type=mapping_type)
    session.add(rule)
    session.flush()
    return rule
