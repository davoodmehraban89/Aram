"""Read-only change preview for explicit, human-reviewed Mapping decisions.

A preview and its fingerprint are NOT an approval, an authenticated identity,
a persisted audit event, or a race-free database write authorization.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from aram_backend.mapping_service import MappingValidationError


class MappingNoChange(MappingValidationError):
    """Preview is valid, but proposed Mapping content is unchanged."""
from aram_backend.models import (
    AccountVersion, FiscalYear, FiscalYearStatus, MappingRule, NoteDefinition,
)


@dataclass(frozen=True)
class RuleValues:
    id: int | None
    version: int
    account_code: str
    target_note_id: int
    mapping_type: str


@dataclass(frozen=True)
class MappingChangePreview:
    year_id: int
    company_id: int
    fiscal_year_number: int
    rule_key: str
    expected_base_version: int
    before: RuleValues | None
    proposed: RuleValues
    target_note_number: str
    target_note_version: int
    account_version_id: int
    account_version: int
    fingerprint: str


def _require_clean_mapping_state(session: Session) -> None:
    # A read-only DB snapshot cannot faithfully describe unflushed ORM edits.
    # Conservatively reject pending related edits (even to another year)
    # rather than use a misleading snapshot or trigger an implicit flush.
    touched = session.new | session.dirty | session.deleted
    if any(isinstance(item, (
        FiscalYear, MappingRule, NoteDefinition, AccountVersion
    )) for item in touched):
        raise MappingValidationError(
            "mapping preview requires a clean Session; flush or rollback pending edits first"
        )


def _validate_inputs(
    year_id: int, rule_key: str, account_code: str,
    target_note_id: int, mapping_type: str, expected_base_version: int,
) -> None:
    if type(year_id) is not int or year_id <= 0:
        raise MappingValidationError("year_id must be a positive integer")
    if type(target_note_id) is not int or target_note_id <= 0:
        raise MappingValidationError("target_note_id must be a positive integer")
    if type(expected_base_version) is not int or expected_base_version < 0:
        raise MappingValidationError("expected_base_version must be a nonnegative integer")
    for name, value, limit in (
        ("rule_key", rule_key, 128),
        ("account_code", account_code, 64),
        ("mapping_type", mapping_type, 32),
    ):
        if not isinstance(value, str) or not value or value.strip() != value or len(value) > limit:
            raise MappingValidationError(f"invalid {name}")


def preview_mapping_change(
    session: Session, *, year_id: int, rule_key: str, account_code: str,
    target_note_id: int, mapping_type: str, expected_base_version: int,
    allow_unchanged: bool = False,
) -> MappingChangePreview:
    """Describe a proposed NEXT version without writing or accepting it.

    expected_base_version=0 means no MappingRule exists for this rule_key/year.
    Otherwise it must equal the latest persisted rule version. An old version,
    non-current note, cross-year target or unchanged proposal is rejected.
    """
    if type(allow_unchanged) is not bool:
        raise MappingValidationError("allow_unchanged must be Boolean")
    _validate_inputs(
        year_id, rule_key, account_code, target_note_id, mapping_type,
        expected_base_version,
    )
    with session.no_autoflush:
        _require_clean_mapping_state(session)
        year = session.get(FiscalYear, year_id, populate_existing=True)
        if year is None or year.status is not FiscalYearStatus.DRAFT:
            raise MappingValidationError("fiscal year must exist and be Draft")

        previous_rule = session.scalar(
            select(MappingRule)
            .where(MappingRule.year_id == year_id, MappingRule.rule_key == rule_key)
            .order_by(MappingRule.version.desc(), MappingRule.id.desc())
            .limit(1)
            .execution_options(populate_existing=True)
        )
        prior_version = previous_rule.version if previous_rule is not None else 0
        if expected_base_version != prior_version:
            raise MappingValidationError("stale base mapping version; regenerate review preview")

        target = session.get(NoteDefinition, target_note_id, populate_existing=True)
        if target is None or target.year_id != year_id:
            raise MappingValidationError("target note must belong to the same fiscal year")
        latest_note = session.scalar(
            select(NoteDefinition).where(
                NoteDefinition.year_id == year_id,
                NoteDefinition.note_number == target.note_number,
            ).order_by(NoteDefinition.version.desc(), NoteDefinition.id.desc()).limit(1)
            .execution_options(populate_existing=True)
        )
        if latest_note is None or latest_note.id != target_note_id:
            raise MappingValidationError("target must reference latest note version")

        account = session.scalar(
            select(AccountVersion).where(
                AccountVersion.year_id == year_id, AccountVersion.account_code == account_code,
            ).order_by(AccountVersion.version.desc(), AccountVersion.id.desc()).limit(1)
            .execution_options(populate_existing=True)
        )
        if account is None:
            raise MappingValidationError("account code must exist in the same fiscal year")

        before = (
            RuleValues(
                previous_rule.id, previous_rule.version, previous_rule.account_code,
                previous_rule.target_note_id, previous_rule.mapping_type,
            )
            if previous_rule is not None else None
        )
        proposed = RuleValues(
            id=None, version=prior_version + 1, account_code=account_code,
            target_note_id=target_note_id, mapping_type=mapping_type,
        )
        is_unchanged = before is not None and (
            before.account_code, before.target_note_id, before.mapping_type
        ) == (
            proposed.account_code, proposed.target_note_id, proposed.mapping_type
        )

        data = {
            "year_id": year_id,
            "company_id": year.company_id,
            "fiscal_year_number": year.year,
            "rule_key": rule_key,
            "expected_base_version": expected_base_version,
            "before": asdict(before) if before is not None else None,
            "proposed": asdict(proposed),
            "target_note_number": target.note_number,
            "target_note_version": target.version,
            "account_version_id": account.id,
            "account_version": account.version,
        }
        fingerprint = sha256(
            json.dumps(data, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        preview = MappingChangePreview(
            year_id=year_id, company_id=year.company_id, fiscal_year_number=year.year,
            rule_key=rule_key, expected_base_version=expected_base_version,
            before=before, proposed=proposed,
            target_note_number=target.note_number,
            target_note_version=target.version,
            account_version_id=account.id, account_version=account.version,
            fingerprint=fingerprint,
        )
        if is_unchanged and not allow_unchanged:
            raise MappingNoChange("no mapping change to review")
        return preview


def verify_mapping_change_preview_current(
    session: Session, preview: MappingChangePreview,
) -> None:
    """Recheck a previously observed snapshot; this never saves or approves.

    A successful recheck is NOT a transaction lock, authenticated approval or
    authorization to skip version, audit and database-level race protections.
    """
    if not isinstance(preview, MappingChangePreview):
        raise MappingValidationError("invalid mapping preview")
    try:
        current = preview_mapping_change(
            session, year_id=preview.year_id, rule_key=preview.rule_key,
            account_code=preview.proposed.account_code,
            target_note_id=preview.proposed.target_note_id,
            mapping_type=preview.proposed.mapping_type,
            expected_base_version=preview.expected_base_version,
        )
    except MappingValidationError as exc:
        raise MappingValidationError("mapping review preview is stale or invalid") from exc
    if current != preview:
        raise MappingValidationError("mapping review preview is stale or altered")
