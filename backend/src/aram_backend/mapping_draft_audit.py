"""Database-local SYSTEM staging evidence only; NOT authenticated finance audit.

SQLite-only triggers deny updates and deletes to event rows. A privileged DB
operator can still drop triggers, insert fake rows or replace the DB file:
this is NOT a signed/WORM/externally anchored immutable audit ledger.
"""
from __future__ import annotations

from hashlib import sha256
import json

from sqlalchemy import (
    CheckConstraint, Column, DateTime, ForeignKey, Integer, String,
    Table, UniqueConstraint, func, insert, select,
)
from sqlalchemy.orm import Session

from aram_backend.mapping_draft_store import (
    _proposal_metadata, mapping_review_drafts,
)
from aram_backend.mapping_service import MappingValidationError


mapping_draft_events = Table(
    "mapping_draft_events", _proposal_metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "draft_id", Integer,
        ForeignKey(mapping_review_drafts.c.id, ondelete="RESTRICT"), nullable=False,
    ),
    Column("year_id", Integer, nullable=False),
    Column("event_type", String(32), nullable=False, server_default="DraftStaged"),
    Column("payload_hash", String(64), nullable=False),
    Column("event_hash", String(64), nullable=False),
    Column(
        "created_at", DateTime(timezone=True),
        server_default=func.current_timestamp(), nullable=False,
    ),
    UniqueConstraint("draft_id", name="uq_mapping_draft_events_draft"),
    CheckConstraint(
        "event_type = 'DraftStaged'", name="ck_mapping_draft_events_staging_only",
    ),
)


SQLITE_AUDIT_GUARD_DDL = (
    """CREATE TRIGGER mapping_draft_events_no_update
       BEFORE UPDATE ON mapping_draft_events
       BEGIN SELECT RAISE(ABORT, 'Mapping staging event is insert-only'); END""",
    """CREATE TRIGGER mapping_draft_events_no_delete
       BEFORE DELETE ON mapping_draft_events
       BEGIN SELECT RAISE(ABORT, 'Mapping staging event is insert-only'); END""",
)


def _event_digest(*, draft_id: int, year_id: int, request_key: str, payload_hash: str) -> str:
    values = dict(
        draft_id=draft_id, year_id=year_id, request_key=request_key,
        payload_hash=payload_hash, event_type="DraftStaged",
    )
    encoded = json.dumps(
        values, sort_keys=True, ensure_ascii=True, separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def record_draft_staging_event(
    session: Session, *, draft_id: int, year_id: int, request_key: str,
    payload_hash: str,
) -> None:
    """Insert a single SYSTEM event in the *caller's* staging transaction.

    Do not call this for a replay. The DB unique(draft_id) is the final guard
    against a double event, and the outer transaction rolls back both records.
    """
    if (type(draft_id) is not int or draft_id <= 0 or
            type(year_id) is not int or year_id <= 0):
        raise MappingValidationError("invalid staging event draft/year identifiers")
    session.execute(
        insert(mapping_draft_events).values(
            draft_id=draft_id, year_id=year_id, event_type="DraftStaged",
            payload_hash=payload_hash,
            event_hash=_event_digest(
                draft_id=draft_id, year_id=year_id,
                request_key=request_key, payload_hash=payload_hash,
            ),
        )
    )


def verify_draft_staging_event(
    session: Session, *, draft_id: int, year_id: int,
) -> None:
    """Read-only crosscheck of draft and event; does not authorize approval."""
    if type(draft_id) is not int or draft_id <= 0 or type(year_id) is not int or year_id <= 0:
        raise MappingValidationError("invalid staging event identifiers")
    with session.no_autoflush:
        draft = session.execute(
            select(mapping_review_drafts).where(
                mapping_review_drafts.c.id == draft_id,
                mapping_review_drafts.c.year_id == year_id,
            )
        ).mappings().first()
        if draft is None:
            raise MappingValidationError("unreviewed Mapping draft not found for fiscal year")
        event = session.execute(
            select(mapping_draft_events).where(
                mapping_draft_events.c.draft_id == draft_id,
                mapping_draft_events.c.year_id == year_id,
            )
        ).mappings().first()
        if (
            event is None
            or draft["state"] != "Unreviewed"
            or event["event_type"] != "DraftStaged"
            or event["payload_hash"] != draft["payload_hash"]
            or event["event_hash"] != _event_digest(
                draft_id=draft_id, year_id=year_id,
                request_key=draft["request_key"], payload_hash=draft["payload_hash"],
            )
        ):
            raise MappingValidationError("Mapping draft staging audit is missing or corrupted")
