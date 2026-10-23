"""Read-only note-level mapping review; no financial amounts or inferred targets."""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import AccountVersion, FiscalYear, MappingRule, NoteDefinition


@dataclass(frozen=True)
class NoteMappingReview:
    note_id: int
    note_number: str
    note_title: str
    account_codes: tuple[str, ...]
    ambiguous_account_codes: tuple[str, ...]


@dataclass(frozen=True)
class NoteMappingOverview:
    year_id: int
    notes: tuple[NoteMappingReview, ...]
    unmapped_account_codes: tuple[str, ...]
    orphan_rule_keys: tuple[str, ...]
    stale_note_rule_keys: tuple[str, ...]


def review_note_mappings(session: Session, *, year_id: int) -> NoteMappingOverview:
    """Report current note assignments; reject stale note versions rather than guessing.

    Current = greatest version per account, rule key and note number. If an
    account has multiple distinct current targets, show it as ambiguous.
    Queries deliberately avoid flushing pending changes.
    """
    if type(year_id) is not int or year_id <= 0:
        raise MappingValidationError("year_id must be a positive integer")
    with session.no_autoflush:
        if session.get(FiscalYear, year_id) is None:
            raise MappingValidationError("fiscal year does not exist")

        accounts = session.scalars(select(AccountVersion).where(
            AccountVersion.year_id == year_id
        ).order_by(AccountVersion.account_code, AccountVersion.version.desc(), AccountVersion.id.desc())).all()
        current_accounts = {a.account_code for a in accounts}

        notes = session.scalars(select(NoteDefinition).where(
            NoteDefinition.year_id == year_id
        ).order_by(NoteDefinition.note_number, NoteDefinition.version.desc(), NoteDefinition.id.desc())).all()
        current_notes: dict[str, NoteDefinition] = {}
        for note in notes:
            current_notes.setdefault(note.note_number, note)
        current_note_by_id = {n.id: n for n in current_notes.values()}

        rules = session.scalars(select(MappingRule).where(
            MappingRule.year_id == year_id
        ).order_by(MappingRule.rule_key, MappingRule.version.desc(), MappingRule.id.desc())).all()
        current_rules: dict[str, MappingRule] = {}
        for rule in rules:
            current_rules.setdefault(rule.rule_key, rule)

        account_targets: dict[str, set[int]] = {code: set() for code in current_accounts}
        orphan: list[str] = []
        stale: list[str] = []
        for key, rule in current_rules.items():
            if rule.account_code not in current_accounts:
                orphan.append(key)
            elif rule.target_note_id not in current_note_by_id:
                stale.append(key)
            else:
                account_targets[rule.account_code].add(rule.target_note_id)

        ambiguous = {code for code, targets in account_targets.items() if len(targets) > 1}
        reviews = tuple(NoteMappingReview(
            note_id=note.id, note_number=note.note_number, note_title=note.title,
            account_codes=tuple(sorted(
                code for code, targets in account_targets.items()
                if note.id in targets and code not in ambiguous
            )),
            ambiguous_account_codes=tuple(sorted(
                code for code in ambiguous if note.id in account_targets[code]
            )),
        ) for note in sorted(current_notes.values(), key=lambda n: (n.note_number, n.id)))
        return NoteMappingOverview(
            year_id=year_id, notes=reviews,
            unmapped_account_codes=tuple(sorted(
                code for code, targets in account_targets.items() if not targets
            )),
            orphan_rule_keys=tuple(sorted(orphan)),
            stale_note_rule_keys=tuple(sorted(stale)),
        )
