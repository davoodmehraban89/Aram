"""Persistent, UNREVIEWED-only Mapping proposals; NOT an approval or apply API.

The proposal table has independent MetaData: the legacy initial Alembic
migration uses Base.metadata.create_all(), so the *later*, explicit migration
is solely responsible for creating this table. Never import it into Base.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from unicodedata import category

from sqlalchemy import (
    JSON, CheckConstraint, Column, DateTime, ForeignKey, Integer, MetaData,
    String, Table, UniqueConstraint, func, insert, select,
)
from sqlalchemy.orm import Session

from aram_backend.mapping_batch_review import (
    MappingBatchPreview, ProposedMappingRow, preview_mapping_batch,
    verify_mapping_batch_current,
)
from aram_backend.mapping_service import MappingValidationError
from aram_backend.mapping_change_preview import _require_clean_mapping_state
from aram_backend.models import FiscalYear

# Deliberately distinct from Base.metadata. Never create this table with the
# original "20260820_01" Base.metadata.create_all migration.
_proposal_metadata = MetaData()
mapping_review_drafts = Table(
    "mapping_review_drafts",
    _proposal_metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "year_id", Integer,
        ForeignKey(FiscalYear.__table__.c.id, ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("request_key", String(64), nullable=False),
    Column("payload_json", JSON, nullable=False),
    Column("payload_hash", String(64), nullable=False),
    Column("state", String(16), nullable=False, server_default="Unreviewed"),
    Column("created_at", DateTime(timezone=True), nullable=False,
           server_default=func.current_timestamp()),
    UniqueConstraint("year_id", "request_key", name="uq_mapping_review_drafts_year_request"),
    CheckConstraint("state = 'Unreviewed'", name="ck_mapping_review_drafts_unreviewed_only"),
)


@dataclass(frozen=True)
class StoredMappingDraft:
    """Passive persisted evidence. There are deliberately NO approval fields."""

    id: int
    year_id: int
    request_key: str
    checksum: str
    state: str
    created_at: object


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def _payload(snapshot: MappingBatchPreview) -> dict:
    return {"batch": json.loads(_canonical(asdict(snapshot)))}


def _digest(payload: dict) -> str:
    return sha256(_canonical(payload).encode("utf-8")).hexdigest()


def _valid_request_key(value: object) -> bool:
    return (
        isinstance(value, str) and bool(value)
        and value == value.strip() and len(value) <= 64
        and not any(category(ch) in ("Cc", "Cf", "Cs") for ch in value)
    )


def _from_row(row) -> StoredMappingDraft:
    return StoredMappingDraft(
        id=row["id"], year_id=row["year_id"], request_key=row["request_key"],
        checksum=row["payload_hash"], state=row["state"], created_at=row["created_at"],
    )


def _read_row(session: Session, *, draft_id: int, year_id: int):
    if type(draft_id) is not int or draft_id <= 0 or type(year_id) is not int or year_id <= 0:
        raise MappingValidationError("invalid draft or fiscal year identifier")
    row = session.execute(
        select(mapping_review_drafts).where(
            mapping_review_drafts.c.id == draft_id,
            mapping_review_drafts.c.year_id == year_id,
        )
    ).mappings().first()
    if row is None:
        raise MappingValidationError("unreviewed Mapping draft not found for fiscal year")
    if (row["state"] != "Unreviewed" or
            not isinstance(row["payload_json"], dict) or
            _digest(row["payload_json"]) != row["payload_hash"]):
        raise MappingValidationError("stored unreviewed Mapping draft corrupted")
    return row


def save_unreviewed_batch(
    session: Session, snapshot: MappingBatchPreview, *, request_key: str,
) -> StoredMappingDraft:
    """Stage an unapproved snapshot under caller-controlled transaction.

    Does not call save_mapping_rule, change any MappingRule, commit, create an
    approval identity, or authorize reuse of a preview for an APPLY action.
    """
    if not _valid_request_key(request_key):
        raise MappingValidationError("invalid proposal request key")
    if not isinstance(snapshot, MappingBatchPreview) or not snapshot.ready_for_review:
        raise MappingValidationError("mapping batch is not ready for unreviewed staging")
    with session.no_autoflush:
        _require_clean_mapping_state(session)
        verify_mapping_batch_current(session, snapshot)
        payload = _payload(snapshot)
        checksum = _digest(payload)
        existing = session.execute(
            select(mapping_review_drafts).where(
                mapping_review_drafts.c.year_id == snapshot.year_id,
                mapping_review_drafts.c.request_key == request_key,
            )
        ).mappings().first()
        if existing is not None:
            if (existing["state"] != "Unreviewed" or
                    _digest(existing["payload_json"]) != existing["payload_hash"]):
                raise MappingValidationError("stored idempotency request key is corrupted")
            if checksum != existing["payload_hash"] or payload != existing["payload_json"]:
                raise MappingValidationError("idempotency request key already used for another proposal")
            return _from_row(existing)
        result = session.execute(
            insert(mapping_review_drafts).values(
                year_id=snapshot.year_id, request_key=request_key,
                payload_json=payload, payload_hash=checksum, state="Unreviewed",
            )
        )
        # Caller owns transaction; uniqueness constraint rejects simultaneous
        # identical keys on independent DB connections. On IntegrityError the
        # caller must rollback; do not recover by unguarded replay.
        draft_id = result.inserted_primary_key[0]
        row = _read_row(session, draft_id=draft_id, year_id=snapshot.year_id)
        return _from_row(row)


def get_unreviewed_batch(
    session: Session, *, draft_id: int, year_id: int,
) -> StoredMappingDraft:
    """Read passive draft metadata scoped to a fiscal year; not authenticated."""
    with session.no_autoflush:
        return _from_row(_read_row(session, draft_id=draft_id, year_id=year_id))


def validate_unreviewed_batch_current(
    session: Session, *, draft_id: int, year_id: int,
) -> None:
    """Reevaluate stored source rows against current DB state, read-only.

    Even if this succeeds, another transaction can change facts afterwards:
    this is NOT a transaction lock, reviewer attestation, or write permission.
    """
    with session.no_autoflush:
        row = _read_row(session, draft_id=draft_id, year_id=year_id)
        try:
            batch = row["payload_json"]["batch"]
            source = tuple(ProposedMappingRow(**item) for item in batch["source_rows"])
            current = preview_mapping_batch(session, year_id=year_id, rows=source)
            if not current.ready_for_review:
                raise MappingValidationError("stored Mapping draft is stale")
            if _canonical(asdict(current)) != _canonical(batch):
                raise MappingValidationError("stored Mapping draft is stale")
        except (KeyError, ValueError, TypeError) as exc:
            raise MappingValidationError("stored Mapping draft is stale or malformed") from exc
