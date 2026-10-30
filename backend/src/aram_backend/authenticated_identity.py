"""Fail-closed public-key verification of identity-provider access tokens.

Only the operator-configured public RSA key can verify a token; no client
headers, unsigned JWTs, HS256 shared secrets or user-supplied public keys can
create a verified principal. This module has NO finance approve/apply action.
"""
from __future__ import annotations

from dataclasses import dataclass
from time import time
from unicodedata import category

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from aram_backend.config import Settings, get_settings

MAX_TOKEN_LENGTH = 8192
MAX_LIFETIME_SECONDS = 900
MAX_SIGNED_YEAR_SCOPES = 32
TRUSTED_ROLES = frozenset(("mapping_proposer", "mapping_reviewer"))
bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class SignedYearScope:
    """Exact signed company, fiscal-year and role boundary; no wildcards."""

    company_code: str
    fiscal_year: int
    role: str


@dataclass(frozen=True)
class VerifiedPrincipal:
    """Identity from successfully validated RS256 issuer/audience claims only."""

    issuer: str
    subject: str
    roles: tuple[str, ...]
    expires_at: int
    # Older valid tokens with no explicit grants may authenticate, but can
    # NEVER authorize year-specific Mapping operations.
    year_scopes: tuple[SignedYearScope, ...] = ()


def _fail_invalid() -> None:
    raise HTTPException(
        status_code=401, detail="Invalid bearer token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _is_safe_string(value: object, limit: int) -> bool:
    return (
        isinstance(value, str) and 0 < len(value) <= limit
        and value == value.strip()
        and not any(category(char) in ("Cc", "Cf", "Cs") for char in value)
    )


def _validated_signed_scopes(raw: object, *, permitted_role: str) -> tuple[SignedYearScope, ...]:
    if type(raw) is not list or len(raw) > MAX_SIGNED_YEAR_SCOPES:
        _fail_invalid()
    seen: set[SignedYearScope] = set()
    result: list[SignedYearScope] = []
    for item in raw:
        if type(item) is not dict or set(item) != {"company_code", "fiscal_year", "role"}:
            _fail_invalid()
        code, year, role = item["company_code"], item["fiscal_year"], item["role"]
        if (
            not _is_safe_string(code, 64)
            or "*" in code or "?" in code
            or type(year) is not int or year <= 0 or year > 9999
            or type(role) is not str or role != permitted_role
        ):
            _fail_invalid()
        scope = SignedYearScope(company_code=code, fiscal_year=year, role=role)
        if scope in seen:
            _fail_invalid()
        seen.add(scope)
        result.append(scope)
    return tuple(result)


def _trusted_public_key(settings: Settings) -> RSAPublicKey:
    if (
        not _is_safe_string(settings.auth_issuer, 512)
        or not settings.auth_issuer.startswith("https://")
        or not _is_safe_string(settings.auth_audience, 256)
        or not settings.auth_public_key_pem
    ):
        raise HTTPException(status_code=503, detail="Identity provider is not configured")
    try:
        key = serialization.load_pem_public_key(
            settings.auth_public_key_pem.encode("ascii"),
        )
    except (ValueError, TypeError, UnicodeError) as exc:
        raise HTTPException(
            status_code=503, detail="Identity provider is not configured",
        ) from exc
    if not isinstance(key, RSAPublicKey) or key.key_size < 2048:
        raise HTTPException(status_code=503, detail="Identity provider is not configured")
    return key


def verify_access_token(token: str, *, settings: Settings) -> VerifiedPrincipal:
    """Verify a short-lived RSA-signed access token, fail closed on all claims.

    Static public-key pinning is intentional here; rotating/jwks validation and
    a deployed enterprise IdP must be separately configured and reviewed.
    """
    key = _trusted_public_key(settings)
    if not isinstance(token, str) or not token or len(token) > MAX_TOKEN_LENGTH:
        _fail_invalid()
    try:
        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.auth_audience,
            issuer=settings.auth_issuer,
            leeway=0,
            options={
                "require": [
                    "iss", "aud", "sub", "exp", "iat", "nbf",
                    "token_use", "aram_roles",
                ],
            },
        )
    except (jwt.InvalidTokenError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=401, detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    roles = claims.get("aram_roles")
    exp = claims.get("exp")
    iat = claims.get("iat")
    nbf = claims.get("nbf")
    if (
        claims.get("token_use") != "access"
        or not _is_safe_string(claims.get("sub"), 128)
        or type(exp) is not int or type(iat) is not int or type(nbf) is not int
        or exp <= iat or exp - iat > MAX_LIFETIME_SECONDS
        or nbf > exp
        or not isinstance(roles, list) or not roles
        or any(type(role) is not str or role not in TRUSTED_ROLES for role in roles)
        or len(set(roles)) != len(roles)
        or len(roles) > 1
    ):
        _fail_invalid()
    scopes = _validated_signed_scopes(
        claims.get("aram_scopes", []), permitted_role=roles[0],
    )
    return VerifiedPrincipal(
        issuer=claims["iss"], subject=claims["sub"],
        roles=tuple(sorted(roles)), expires_at=exp, year_scopes=scopes,
    )


def require_verified_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> VerifiedPrincipal:
    """FastAPI dependency; never trust X-User / X-Role headers."""
    # Misconfigured deployment cannot accidentally become authenticated.
    _trusted_public_key(settings)
    if credentials is None or credentials.scheme.lower() != "bearer":
        _fail_invalid()
    return verify_access_token(credentials.credentials, settings=settings)
