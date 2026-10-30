"""Read-only, explicit-review preview for carrying mapping decisions into a new year.

Never infers target notes or writes rules. The caller must explicitly review and
save each proposed mapping using the governed mapping service.
"""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import AccountVersion, FiscalYear, FiscalYearStatus, MappingRule, NoteDefinition


@dataclass(frozen=True)
class CarryForwardCandidate:
    rule_key: str
    account_code: str
    source_note_number: str
    target_note_id: int
    mapping_type: str
    source_version: int


@dataclass(frozen=True)
class CarryForwardPreview:
    source_year_id: int
    target_year_id: int
    candidates: tuple[CarryForwardCandidate, ...]
    skipped: tuple[tuple[str, str], ...]


def preview_mapping_carry_forward(
    session: Session, *, source_year_id: int, target_year_id: int,
) -> CarryForwardPreview:
    """Preview mapping candidates for the same company's later Draft year.

    Match target notes by *exact* note_number only when unique at their latest
    version. Missing accounts/notes and existing target rules are skipped with
    reasons, never auto-created. No changes are flushed or committed.
    """
    for label, value in (("source_year_id", source_year_id), ("target_year_id", target_year_id)):
        if type(value) is not int or value <= 0:
            raise MappingValidationError(f"{label} must be a positive integer")
    if source_year_id == target_year_id:
        raise MappingValidationError("source and target fiscal years must differ")

    with session.no_autoflush:
        source = session.get(FiscalYear, source_year_id)
        target = session.get(FiscalYear, target_year_id)
        if source is None or target is None:
            raise MappingValidationError("both fiscal years must exist")
        if source.company_id != target.company_id:
            raise MappingValidationError("fiscal years must belong to the same company")
        if source.year >= target.year:
            raise MappingValidationError("target fiscal year must be later than source")
        if target.status is not FiscalYearStatus.DRAFT:
            raise MappingValidationError("target fiscal year must be Draft")

        source_rules = session.scalars(
            select(MappingRule).where(MappingRule.year_id == source_year_id)
            .order_by(MappingRule.rule_key, MappingRule.version.desc(), MappingRule.id.desc())
        ).all()
        latest_rules: dict[str, MappingRule] = {}
        for rule in source_rules:
            latest_rules.setdefault(rule.rule_key, rule)

        # Only the latest version of a source note number can authorize
        # carry-forward. An old MappingRule target is not the current note,
        # even when the note number happens to remain unchanged.
        source_note_rows = session.scalars(
            select(NoteDefinition).where(NoteDefinition.year_id == source_year_id)
            .order_by(NoteDefinition.note_number, NoteDefinition.version.desc(), NoteDefinition.id.desc())
        ).all()
        source_notes = {note.id: note for note in source_note_rows}
        latest_source_notes: dict[str, NoteDefinition] = {}
        for note in source_note_rows:
            latest_source_notes.setdefault(note.note_number, note)
        target_notes = session.scalars(
            select(NoteDefinition).where(NoteDefinition.year_id == target_year_id)
            .order_by(NoteDefinition.note_number, NoteDefinition.version.desc(), NoteDefinition.id.desc())
        ).all()
        latest_target_notes: dict[str, NoteDefinition] = {}
        for note in target_notes:
            latest_target_notes.setdefault(note.note_number, note)

        target_accounts = set(session.scalars(
            select(AccountVersion.account_code).where(AccountVersion.year_id == target_year_id)
        ))
        target_rule_keys = set(session.scalars(
            select(MappingRule.rule_key).where(MappingRule.year_id == target_year_id)
        ))

        candidates: list[CarryForwardCandidate] = []
        skipped: list[tuple[str, str]] = []
        for key, rule in sorted(latest_rules.items()):
            source_note = source_notes.get(rule.target_note_id)
            if source_note is None:
                skipped.append((key, "source_note_missing"))
            elif latest_source_notes[source_note.note_number].id != source_note.id:
                skipped.append((key, "source_note_stale"))
            elif rule.account_code not in target_accounts:
                skipped.append((key, "target_account_missing"))
            elif source_note.note_number not in latest_target_notes:
                skipped.append((key, "target_note_missing"))
            elif key in target_rule_keys:
                skipped.append((key, "target_rule_exists"))
            else:
                candidates.append(CarryForwardCandidate(
                    rule_key=key, account_code=rule.account_code,
                    source_note_number=source_note.note_number,
                    target_note_id=latest_target_notes[source_note.note_number].id,
                    mapping_type=rule.mapping_type, source_version=rule.version,
                ))
        return CarryForwardPreview(
            source_year_id=source_year_id, target_year_id=target_year_id,
            candidates=tuple(candidates), skipped=tuple(skipped),
        )
