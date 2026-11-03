"""Fail-closed local authentication endpoints.

The application does not provision credentials at import/startup. An explicit
trusted composition root must configure the authority; otherwise login/logout
return 503. This volatile adapter is for controlled single-user local use only.
"""
from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from aram_backend.local_auth import LocalSessionAuthority
from aram_backend.mapping_api import configure_mapping_service, reset_mapping_service
from aram_backend.mapping_store import MappingStore
from aram_backend.windows_credential_vault import load_credential

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
_authority: LocalSessionAuthority | None = None


class LoginRequest(BaseModel):
    password: str = Field(min_length=1, max_length=1024)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LogoutResponse(BaseModel):
    revoked: bool


def configure_local_auth_service(
    *, authority: LocalSessionAuthority, store: MappingStore
) -> None:
    """Explicit server-side opt-in; never accept roles or scopes from HTTP."""
    global _authority
    _authority = authority
    configure_mapping_service(store=store, identity_resolver=authority.resolve)


def configure_local_auth_from_vault(
    *, credential_path: str, store: MappingStore
) -> None:
    """Load a CurrentUser-DPAPI credential; any failure leaves service disabled."""
    credential = load_credential(credential_path)
    configure_local_auth_service(
        authority=LocalSessionAuthority(credential), store=store
    )


def reset_local_auth_service() -> None:
    global _authority
    if _authority is not None:
        _authority.revoke_all()
    _authority = None
    reset_mapping_service()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    if _authority is None:
        raise HTTPException(status_code=503, detail="authentication service not configured")
    token = _authority.login(payload.password)
    if token is None:
        raise HTTPException(status_code=401, detail="invalid credentials or temporarily locked")
    return LoginResponse(
        access_token=token, expires_in=_authority.lifetime_seconds
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(authorization: str | None = Header(default=None)) -> LogoutResponse:
    if _authority is None:
        raise HTTPException(status_code=503, detail="authentication service not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer authentication required")
    token = authorization[7:]
    if not token or token != token.strip():
        raise HTTPException(status_code=401, detail="invalid bearer token")
    was_valid = _authority.resolve(token) is not None
    _authority.revoke(token)
    return LogoutResponse(revoked=was_valid)
