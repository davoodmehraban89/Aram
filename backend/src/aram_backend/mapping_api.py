"""Protected mapping HTTP operations.

A deployment MUST supply a trusted identity resolver and an isolated MappingStore.
The API never accepts actor, roles, or company permissions from request bodies.
"""
from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from aram_backend.mapping_access import AuthenticatedPrincipal, MappingAccess
from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingDecision, MappingWorkflowError

router = APIRouter(prefix="/api/v1/mapping", tags=["mapping"])
_identity_resolver: Callable[[str], AuthenticatedPrincipal | None] | None = None
_store: MappingStore | None = None


def configure_mapping_service(
    *, store: MappingStore, identity_resolver: Callable[[str], AuthenticatedPrincipal | None]
) -> None:
    """Server-only composition root; never expose as a route."""
    global _identity_resolver, _store
    _store = store
    _identity_resolver = identity_resolver


def reset_mapping_service() -> None:
    """Explicitly disable service, including when a credential provider fails."""
    global _identity_resolver, _store
    _store = None
    _identity_resolver = None


def _service() -> tuple[MappingStore, MappingAccess]:
    if _store is None or _identity_resolver is None:
        raise HTTPException(status_code=503, detail="mapping service not configured")
    return _store, MappingAccess(_identity_resolver)


def _credential(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer authentication required")
    token = authorization[7:]
    if not token or token != token.strip():
        raise HTTPException(status_code=401, detail="invalid bearer token")
    return token


class Proposal(BaseModel):
    mapping_id: str = Field(min_length=1)
    account_full_code: str = Field(min_length=1)
    target_statement: str = Field(min_length=1)
    statement_section: str = Field(min_length=1)
    note_number: str = Field(min_length=1)
    subnote_code: str | None = None
    source: str = "Manual"


class Revision(BaseModel):
    target_statement: str = Field(min_length=1)
    statement_section: str = Field(min_length=1)
    note_number: str = Field(min_length=1)
    subnote_code: str | None = None


def _apply(company: str, year: int, token: str, action):
    store, access = _service()
    try:
        workspace, revision = store.load(company, year)
        result = action(access, workspace, token)
        store.save(workspace, revision)
        return result
    except MappingWorkflowError as exc:
        message = str(exc)
        if message in {"mapping access denied", "authenticated credential required"}:
            raise HTTPException(status_code=403, detail="access denied") from exc
        if "concurrent update" in message:
            raise HTTPException(status_code=409, detail="concurrent update") from exc
        raise HTTPException(status_code=422, detail=message) from exc


@router.post("/{company}/{year}/proposals", response_model=MappingDecision)
def propose(company: str, year: int, payload: Proposal, token: str = Depends(_credential)):
    def action(access, workspace, credential):
        return access.propose(credential, workspace, MappingDecision(
            payload.mapping_id, company, year, payload.account_full_code,
            payload.target_statement, payload.statement_section, payload.note_number,
            payload.subnote_code, 1, "Draft", None, payload.source,
        ))
    return _apply(company, year, token, action)


@router.post("/{company}/{year}/{mapping_id}/review", response_model=MappingDecision)
def review(company: str, year: int, mapping_id: str, token: str = Depends(_credential)):
    return _apply(company, year, token, lambda a, w, t: a.review(t, w, mapping_id))


@router.post("/{company}/{year}/{mapping_id}/approve", response_model=MappingDecision)
def approve(company: str, year: int, mapping_id: str, token: str = Depends(_credential)):
    return _apply(company, year, token, lambda a, w, t: a.approve(t, w, mapping_id))


@router.post("/{company}/{year}/{mapping_id}/revise", response_model=MappingDecision)
def revise(company: str, year: int, mapping_id: str, payload: Revision,
           token: str = Depends(_credential)):
    return _apply(company, year, token, lambda a, w, t: a.revise(
        t, w, mapping_id, target_statement=payload.target_statement,
        statement_section=payload.statement_section, note_number=payload.note_number,
        subnote_code=payload.subnote_code,
    ))
