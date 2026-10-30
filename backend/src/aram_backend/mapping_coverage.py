"""Read-only fiscal-year mapping coverage and exception queue.

No financial amounts, target guesses, or persistence operations are performed.
"""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import AccountVersion, FiscalYear, MappingRule, NoteDefinition


@dataclass(frozen=True)
class MappingCoverage:
    year_id: int
    total_accounts: int
    mapped_accounts: tuple[str, ...]
    unmapped_accounts: tuple[str, ...]
    ambiguous_accounts: tuple[str, ...]
    orphan_rule_keys: tuple[str, ...]
    # (rule_key, account_code, failure reason), stable sorted order.
    # Keeping a dedicated queue means invalid targets are never hidden behind
    # a valid rule for the same account.
    invalid_target_rules: tuple[tuple[str, str, str], ...] = ()


def inspect_mapping_coverage(session: Session, *, year_id: int) -> MappingCoverage:
    """Return deterministic account queues for a single year without modifying it.

    Only latest version per account and per mapping rule key is considered.
    Multiple current rules pointing one account to distinct notes are ambiguous,
    not silently assigned to a note.
    """
    if type(year_id) is not int or year_id <= 0:
        raise MappingValidationError("year_id must be a positive integer")
    # A diagnostic must not flush unrelated pending writes in the caller's Session.
    with session.no_autoflush:
        if session.get(FiscalYear, year_id) is None:
            raise MappingValidationError("fiscal year does not exist")

        accounts = session.scalars(
            select(AccountVersion)
            .where(AccountVersion.year_id == year_id)
            .order_by(AccountVersion.account_code, AccountVersion.version.desc(), AccountVersion.id.desc())
        ).all()
        current_accounts: dict[str, AccountVersion] = {}
        for account in accounts:
            current_accounts.setdefault(account.account_code, account)

        rules = session.scalars(
            select(MappingRule)
            .where(MappingRule.year_id == year_id)
            .order_by(MappingRule.rule_key, MappingRule.version.desc(), MappingRule.id.desc())
        ).all()
        current_rules: dict[str, MappingRule] = {}
        for rule in rules:
            current_rules.setdefault(rule.rule_key, rule)

        # Resolve every currently referenced note in one bounded query and
        # compute the latest version *within this year*. A cross-year or stale
        # note reference must never count toward successful coverage.
        note_ids = {r.target_note_id for r in current_rules.values()}
        referenced_notes = {
            note.id: note for note in session.scalars(
                select(NoteDefinition).where(NoteDefinition.id.in_(note_ids))
            )
        }
        year_notes = session.scalars(
            select(NoteDefinition).where(NoteDefinition.year_id == year_id)
            .order_by(NoteDefinition.note_number, NoteDefinition.version.desc(), NoteDefinition.id.desc())
        ).all()
        latest_notes: dict[str, NoteDefinition] = {}
        for note in year_notes:
            latest_notes.setdefault(note.note_number, note)

        targets: dict[str, set[int]] = {code: set() for code in current_accounts}
        orphan_keys: list[str] = []
        invalid: list[tuple[str, str, str]] = []
        invalid_accounts: set[str] = set()
        for key, rule in current_rules.items():
            if rule.account_code not in targets:
                orphan_keys.append(key)
                continue
            note = referenced_notes.get(rule.target_note_id)
            if note is None:
                reason = "target_note_missing"
            elif note.year_id != year_id:
                reason = "target_note_wrong_year"
            elif latest_notes[note.note_number].id != note.id:
                reason = "target_note_stale"
            else:
                reason = None
            if reason is not None:
                invalid.append((key, rule.account_code, reason))
                invalid_accounts.add(rule.account_code)
            else:
                targets[rule.account_code].add(rule.target_note_id)

        # A partially valid account still needs human review, not a green
        # "mapped" classification. Put it in the unmapped/action queue and
        # expose precise invalid rules separately.
        mapped = tuple(sorted(
            code for code, notes in targets.items()
            if code not in invalid_accounts and len(notes) == 1
        ))
        unmapped = tuple(sorted(
            code for code, notes in targets.items()
            if code in invalid_accounts or not notes
        ))
        ambiguous = tuple(sorted(
            code for code, notes in targets.items()
            if code not in invalid_accounts and len(notes) > 1
        ))
        return MappingCoverage(
            year_id=year_id, total_accounts=len(current_accounts),
            mapped_accounts=mapped, unmapped_accounts=unmapped,
            ambiguous_accounts=ambiguous, orphan_rule_keys=tuple(sorted(orphan_keys)),
            invalid_target_rules=tuple(sorted(invalid)),
        )
