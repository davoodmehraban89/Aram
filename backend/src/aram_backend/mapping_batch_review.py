"""Read-only Mapping batch classification: no writes, identities or approvals.

Rows here are canonical proposal entries supplied by a trusted future adapter,
not evidence that an XLSX is authorized. The module MUST NOT call save_mapping_rule.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from unicodedata import category

from sqlalchemy.orm import Session

from aram_backend.mapping_change_preview import (
    MappingChangePreview, MappingNoChange, _require_clean_mapping_state,
    preview_mapping_change,
)
from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import FiscalYear, FiscalYearStatus

MAX_BATCH_ROWS = 10_000
MAX_LOCATOR_LENGTH = 256


@dataclass(frozen=True)
class ProposedMappingRow:
    source_locator: str
    rule_key: str
    account_code: str
    target_note_id: int
    mapping_type: str
    expected_base_version: int


@dataclass(frozen=True)
class MappingBatchRowResult:
    source_locator: str
    rule_key: str
    status: str
    preview: MappingChangePreview | None = None
    duplicate_of: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class MappingBatchPreview:
    year_id: int
    rows: tuple[MappingBatchRowResult, ...]
    fingerprint: str
    # Exact submitted typed evidence, not an authentication token.
    # Required to replay and revalidate every row before later review.
    source_rows: tuple[ProposedMappingRow, ...]

    @property
    def counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.rows:
            counts[item.status] = counts.get(item.status, 0) + 1
        return counts

    @property
    def has_changes(self) -> bool:
        return any(item.status in ("new", "changed") for item in self.rows)

    @property
    def ready_for_review(self) -> bool:
        return self.has_changes and all(
            item.status in ("new", "changed", "unchanged", "coalesced")
            for item in self.rows
        )


def _row_content(row: ProposedMappingRow) -> tuple[object, ...]:
    # Python considers True == 1. Financial identity comparisons must not
    # coalesce malformed booleans with valid numeric IDs or versions.
    values = (row.account_code, row.target_note_id, row.mapping_type, row.expected_base_version)
    return tuple((type(value).__name__, value) for value in values)


def _validate_envelope(rows: object) -> tuple[ProposedMappingRow, ...]:
    if type(rows) not in (list, tuple) or not 0 < len(rows) <= MAX_BATCH_ROWS:
        raise MappingValidationError("mapping batch requires 1 to 10000 rows")
    locators: set[str] = set()
    for row in rows:
        if not isinstance(row, ProposedMappingRow):
            raise MappingValidationError("mapping batch entries must be typed proposals")
        locator = row.source_locator
        if (not isinstance(locator, str) or not locator or
                len(locator) > MAX_LOCATOR_LENGTH or locator != locator.strip()
                or any(category(char) in ("Cc", "Cf", "Cs") for char in locator)):
            raise MappingValidationError("invalid source locator")
        if locator in locators:
            raise MappingValidationError("duplicate source locator")
        locators.add(locator)
    return tuple(rows)


def preview_mapping_batch(
    session: Session, *, year_id: int, rows: list[ProposedMappingRow] | tuple[ProposedMappingRow, ...],
) -> MappingBatchPreview:
    """Classify every row; conflict/invalid entries block the WHOLE batch.

    A successful preview is *not* an approval token or a transaction lock.
    No mapping is automatically committed, and excluded source rules are not
    interpreted as removals. Explicit reviewer approval/apply is not built yet.
    """
    if type(year_id) is not int or year_id <= 0:
        raise MappingValidationError("year_id must be a positive integer")
    entries = _validate_envelope(rows)

    with session.no_autoflush:
        _require_clean_mapping_state(session)
        year = session.get(FiscalYear, year_id, populate_existing=True)
        if year is None or year.status is not FiscalYearStatus.DRAFT:
            raise MappingValidationError("fiscal year must exist and be Draft")

        by_key: dict[str, list[int]] = {}
        for index, entry in enumerate(entries):
            # Invalid key types are reported as invalid rows; they never
            # participate in accidental equality-based coalescing.
            if isinstance(entry.rule_key, str):
                by_key.setdefault(entry.rule_key, []).append(index)

        conflicting: set[int] = set()
        for group in by_key.values():
            if len(group) > 1 and any(
                _row_content(entries[position]) != _row_content(entries[group[0]])
                for position in group[1:]
            ):
                conflicting.update(group)

        first_by_key: dict[str, MappingBatchRowResult] = {}
        results: list[MappingBatchRowResult] = []
        for index, entry in enumerate(entries):
            source = entry.source_locator
            if index in conflicting:
                result = MappingBatchRowResult(
                    source, str(entry.rule_key), "conflict",
                    reason="conflicting source rows for the same rule key",
                )
            elif isinstance(entry.rule_key, str) and entry.rule_key in first_by_key:
                original = first_by_key[entry.rule_key]
                if original.status == "invalid":
                    result = MappingBatchRowResult(
                        source, entry.rule_key, "invalid",
                        reason=f"duplicate of invalid {original.source_locator}: {original.reason}",
                    )
                else:
                    result = MappingBatchRowResult(
                        source, entry.rule_key, "coalesced",
                        duplicate_of=original.source_locator,
                    )
            else:
                try:
                    preview = preview_mapping_change(
                        session, year_id=year_id, rule_key=entry.rule_key,
                        account_code=entry.account_code,
                        target_note_id=entry.target_note_id,
                        mapping_type=entry.mapping_type,
                        expected_base_version=entry.expected_base_version,
                        allow_unchanged=True,
                    )
                except MappingNoChange:
                    # Defensive compatibility: only the single-item API is
                    # expected to raise no-change with allow_unchanged=False.
                    result = MappingBatchRowResult(source, str(entry.rule_key), "invalid",
                                                   reason="missing unchanged state evidence")
                except MappingValidationError as exc:
                    result = MappingBatchRowResult(
                        source, str(entry.rule_key), "invalid", reason=str(exc),
                    )
                else:
                    unchanged = preview.before is not None and (
                        preview.before.account_code, preview.before.target_note_id,
                        preview.before.mapping_type,
                    ) == (
                        preview.proposed.account_code, preview.proposed.target_note_id,
                        preview.proposed.mapping_type,
                    )
                    result = MappingBatchRowResult(
                        source, entry.rule_key,
                        "unchanged" if unchanged else (
                            "new" if preview.before is None else "changed"
                        ),
                        # Keep full catalog and rule version snapshot even for
                        # unchanged rows so later changes cannot go unnoticed.
                        preview=preview,
                    )
            if isinstance(entry.rule_key, str):
                first_by_key.setdefault(entry.rule_key, result)
            results.append(result)

        stable = [
            {
                "source_locator": item.source_locator,
                "rule_key": item.rule_key,
                "status": item.status,
                "duplicate_of": item.duplicate_of,
                "reason": item.reason,
                "preview": asdict(item.preview) if item.preview is not None else None,
            }
            for item in results
        ]
        fingerprint = sha256(
            json.dumps(
                {"year_id": year_id, "rows": stable},
                sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            ).encode("utf-8")
        ).hexdigest()
        return MappingBatchPreview(
            year_id=year_id, rows=tuple(results), fingerprint=fingerprint,
            source_rows=entries,
        )


def verify_mapping_batch_current(session: Session, snapshot: MappingBatchPreview) -> None:
    """Fail closed if ANY source row, catalog or result changed after preview.

    Read-only verifier; it is neither authenticated approval nor authorization
    to write. Never replace a reviewed snapshot with a refreshed one silently.
    """
    if not isinstance(snapshot, MappingBatchPreview):
        raise MappingValidationError("invalid mapping batch snapshot")
    if not snapshot.ready_for_review:
        raise MappingValidationError("mapping batch is not ready for review")
    try:
        current = preview_mapping_batch(
            session, year_id=snapshot.year_id, rows=snapshot.source_rows,
        )
    except (MappingValidationError, TypeError, ValueError) as exc:
        raise MappingValidationError("mapping batch review is stale or invalid") from exc
    if current != snapshot or not current.ready_for_review:
        raise MappingValidationError("mapping batch review is stale or altered")

