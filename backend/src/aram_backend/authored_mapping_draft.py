"""Author evidence bound to an authenticated, scoped UNREVIEWED staging request.

An actual FastAPI request MUST get principal from verified RSA-bearer Depends.
A user-constructed VerifiedPrincipal Python object is not authentication.
This is neither a human reviewer attestation nor financial approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

from fastapi import HTTPException
from sqlalchemy import (
    CheckConstraint, Column, DateTime, ForeignKey, Integer, String,
    Table, UniqueConstraint, func, insert, select,
)
from sqlalchemy.orm import Session

from aram_backend.authenticated_identity import VerifiedPrincipal
from aram_backend.mapping_batch_review import MappingBatchPreview
from aram_backend.mapping_draft_store import (
    _proposal_metadata, mapping_review_drafts,
    save_unreviewed_batch, get_unreviewed_batch,
)
from aram_backend.mapping_service import MappingValidationError
from aram_backend.mapping_year_authorization import require_year_access


class MappingAuthorConflict(MappingValidationError):
    """A request key has legacy, missing or different-author attribution."""


mapping_draft_authors = Table(
    "mapping_draft_authors", _proposal_metadata,
    Column("id", Integer, primary_key=True),
    Column("draft_id", Integer, ForeignKey(
        mapping_review_drafts.c.id, ondelete="RESTRICT",
    ), nullable=False),
    Column("year_id", Integer, nullable=False),
    Column("issuer", String(512), nullable=False),
    Column("subject", String(128), nullable=False),
    Column("role", String(32), nullable=False),
    Column("company_code", String(64), nullable=False),
    Column("fiscal_year", Integer, nullable=False),
    Column("payload_hash", String(64), nullable=False),
    Column("author_hash", String(64), nullable=False),
    Column("created_at", DateTime(timezone=True),
           nullable=False, server_default=func.current_timestamp()),
    UniqueConstraint("draft_id", name="uq_mapping_draft_authors_draft"),
    CheckConstraint("role = 'mapping_proposer'", name="ck_mapping_draft_authors_proposer"),
)

SQLITE_AUTHOR_GUARD_DDL = (
    """CREATE TRIGGER mapping_draft_authors_no_update
       BEFORE UPDATE ON mapping_draft_authors
       BEGIN SELECT RAISE(ABORT, 'Mapping author evidence is insert-only'); END""",
    """CREATE TRIGGER mapping_draft_authors_no_delete
       BEFORE DELETE ON mapping_draft_authors
       BEGIN SELECT RAISE(ABORT, 'Mapping author evidence is insert-only'); END""",
)


@dataclass(frozen=True)
class DraftAuthor:
    draft_id: int
    year_id: int
    issuer: str
    subject: str
    role: str
    company_code: str
    fiscal_year: int
    payload_hash: str


def _canonical(value: dict[str, object]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _author_digest(values: dict[str, object]) -> str:
    return sha256(_canonical(values).encode("utf-8")).hexdigest()


def _values(
    *, draft_id: int, year_id: int, issuer: str, subject: str,
    company_code: str, fiscal_year: int, payload_hash: str,
) -> dict[str, object]:
    return {
        "draft_id": draft_id, "year_id": year_id,
        "issuer": issuer, "subject": subject, "role": "mapping_proposer",
        "company_code": company_code, "fiscal_year": fiscal_year,
        "payload_hash": payload_hash,
    }


def _insert_author_evidence(session: Session, values: dict[str, object]) -> None:
    session.execute(
        insert(mapping_draft_authors).values(
            **values, author_hash=_author_digest(values),
        )
    )


def get_draft_author(
    session: Session, *, draft_id: int, year_id: int,
) -> DraftAuthor:
    """Read verified same-year author binding; legacy unbound drafts DENIED."""
    with session.no_autoflush:
        saved = get_unreviewed_batch(session, draft_id=draft_id, year_id=year_id)
        row = session.execute(select(mapping_draft_authors).where(
            mapping_draft_authors.c.draft_id == draft_id,
            mapping_draft_authors.c.year_id == year_id,
        )).mappings().first()
        if row is None:
            raise MappingAuthorConflict("unattributed Mapping draft cannot be claimed")
        values = _values(
            draft_id=row["draft_id"], year_id=row["year_id"],
            issuer=row["issuer"], subject=row["subject"],
            company_code=row["company_code"], fiscal_year=row["fiscal_year"],
            payload_hash=row["payload_hash"],
        )
        if (
            row["role"] != "mapping_proposer"
            or row["payload_hash"] != saved.checksum
            or row["author_hash"] != _author_digest(values)
        ):
            raise MappingAuthorConflict("Mapping author evidence corrupted")
        return DraftAuthor(**values)


def stage_authored_unreviewed_batch(
    session: Session, *, snapshot: MappingBatchPreview, request_key: str,
    principal: VerifiedPrincipal,
):
    """Caller-managed transaction; binding, draft and system event all atomic.

    Only use after FastAPI Depends(require_verified_principal). Nothing here
    grants a finance reviewer an approval right or saves MappingRule.
    """
    if not isinstance(snapshot, MappingBatchPreview):
        raise MappingValidationError("invalid Mapping batch")
    grant = require_year_access(
        session, principal=principal, year_id=snapshot.year_id,
        required_role="mapping_proposer",
    )
    # Refuse retroactive authorship on legacy proposals. A draft may have
    # existed before the authenticated staging request, so identifying its ID
    # *after* the saver would allow a caller to take ownership of history.
    existing = session.execute(select(mapping_review_drafts.c.id).where(
        mapping_review_drafts.c.year_id == snapshot.year_id,
        mapping_review_drafts.c.request_key == request_key,
    )).scalar_one_or_none()
    if existing is not None:
        previous_author = get_draft_author(
            session, draft_id=existing, year_id=snapshot.year_id,
        )
        if (previous_author.issuer, previous_author.subject) != (
            principal.issuer, principal.subject,
        ):
            raise MappingAuthorConflict(
                "Mapping draft request key belongs to another author"
            )
    saved = save_unreviewed_batch(session, snapshot, request_key=request_key)
    values = _values(
        draft_id=saved.id, year_id=snapshot.year_id,
        issuer=principal.issuer, subject=principal.subject,
        company_code=grant.company_code, fiscal_year=grant.fiscal_year,
        payload_hash=saved.checksum,
    )
    current = session.execute(select(mapping_draft_authors).where(
        mapping_draft_authors.c.draft_id == saved.id,
    )).mappings().first()
    if current is not None:
        author = get_draft_author(session, draft_id=saved.id, year_id=snapshot.year_id)
        if (author.issuer, author.subject, author.company_code,
                author.fiscal_year) != (
            principal.issuer, principal.subject, grant.company_code,
            grant.fiscal_year,
        ):
            raise MappingAuthorConflict("Mapping draft request key belongs to another author")
        return saved
    # The request-key lookup above proved this is a new record; do not
    # retrofit authenticated authorship onto legacy unbound drafts.
    _insert_author_evidence(session, values)
    return saved


def check_independent_mapping_reviewer(
    session: Session, *, draft_id: int, year_id: int,
    reviewer: VerifiedPrincipal,
) -> None:
    """Read-only *eligibility* check, NEVER an Approved state transition."""
    require_year_access(
        session, principal=reviewer, year_id=year_id,
        required_role="mapping_reviewer",
    )
    author = get_draft_author(session, draft_id=draft_id, year_id=year_id)
    if (author.issuer, author.subject) == (reviewer.issuer, reviewer.subject):
        raise HTTPException(status_code=403, detail="Author cannot review own Mapping")
