"""Read-only fiscal-year mapping coverage and exception queue.

No financial amounts, target guesses, or persistence operations are performed.
"""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import AccountVersion, FiscalYear, MappingRule


@dataclass(frozen=True)
class MappingCoverage:
    year_id: int
    total_accounts: int
    mapped_accounts: tuple[str, ...]
    unmapped_accounts: tuple[str, ...]
    ambiguous_accounts: tuple[str, ...]
    orphan_rule_keys: tuple[str, ...]


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

        targets: dict[str, set[int]] = {code: set() for code in current_accounts}
        orphan_keys: list[str] = []
        for key, rule in current_rules.items():
            if rule.account_code not in targets:
                orphan_keys.append(key)
            else:
                targets[rule.account_code].add(rule.target_note_id)

        mapped = tuple(sorted(code for code, notes in targets.items() if len(notes) == 1))
        unmapped = tuple(sorted(code for code, notes in targets.items() if not notes))
        ambiguous = tuple(sorted(code for code, notes in targets.items() if len(notes) > 1))
        return MappingCoverage(
            year_id=year_id, total_accounts=len(current_accounts),
            mapped_accounts=mapped, unmapped_accounts=unmapped,
            ambiguous_accounts=ambiguous, orphan_rule_keys=tuple(sorted(orphan_keys)),
        )
