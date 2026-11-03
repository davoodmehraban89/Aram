"""Opt-in local password verification and bounded opaque sessions.

This remains a single-owner local adapter. It is not a production IdP and must
not be enabled until credential provisioning, DPAPI key custody, API wiring,
and deployment binding have been reviewed.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
import time
from dataclasses import dataclass

from aram_backend.mapping_access import AuthenticatedPrincipal

_PBKDF2_ITERATIONS = 600_000
_MAX_PASSWORD_LENGTH = 1024
_ALLOWED_ROLES = frozenset({"maker", "reviewer", "approver", "owner"})


@dataclass(frozen=True)
class LocalCredential:
    subject: str
    company_scopes: frozenset[str]
    roles: frozenset[str]
    salt: bytes
    password_hash: bytes


def create_credential(
    subject: str,
    password: str,
    companies: frozenset[str],
    roles: frozenset[str],
) -> LocalCredential:
    if (
        not isinstance(subject, str)
        or not subject.strip()
        or len(subject) > 200
        or not isinstance(password, str)
        or not 14 <= len(password) <= _MAX_PASSWORD_LENGTH
        or not companies
        or any(not isinstance(code, str) or not code.strip() or len(code) > 64 for code in companies)
        or not roles
        or not roles.issubset(_ALLOWED_ROLES)
    ):
        raise ValueError("invalid local credential configuration")
    salt = secrets.token_bytes(32)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return LocalCredential(subject.strip(), frozenset(companies), frozenset(roles), salt, digest)


class LocalSessionAuthority:
    """Volatile, single-credential session authority with bounded lockout.

    Restart revokes all sessions and clears lockout state. Persisted identity,
    multi-user account management, and cross-process rate limiting are out of
    scope; do not expose this adapter on a public network.
    """

    def __init__(
        self,
        credential: LocalCredential,
        *,
        lifetime_seconds: int = 900,
        max_failed_attempts: int = 5,
        lockout_seconds: int = 60,
        max_sessions: int = 8,
    ):
        if not 0 < lifetime_seconds <= 3600:
            raise ValueError("invalid session lifetime")
        if not 1 <= max_failed_attempts <= 20:
            raise ValueError("invalid failed-attempt limit")
        if not 1 <= lockout_seconds <= 3600:
            raise ValueError("invalid lockout duration")
        if not 1 <= max_sessions <= 64:
            raise ValueError("invalid session limit")
        self._credential = credential
        self._lifetime = lifetime_seconds
        self._max_failed_attempts = max_failed_attempts
        self._lockout_seconds = lockout_seconds
        self._max_sessions = max_sessions
        self._failed_attempts = 0
        self._locked_until = 0.0
        self._sessions: dict[bytes, float] = {}
        self._lock = threading.RLock()

    def login(self, password: str) -> str | None:
        if not isinstance(password, str) or len(password) > _MAX_PASSWORD_LENGTH:
            return None
        with self._lock:
            now = time.monotonic()
            if now < self._locked_until:
                return None
            candidate = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                self._credential.salt,
                _PBKDF2_ITERATIONS,
            )
            if not hmac.compare_digest(candidate, self._credential.password_hash):
                self._failed_attempts += 1
                if self._failed_attempts >= self._max_failed_attempts:
                    self._locked_until = now + self._lockout_seconds
                    self._failed_attempts = 0
                return None

            self._failed_attempts = 0
            self._locked_until = 0.0
            self._prune_expired(now)
            if len(self._sessions) >= self._max_sessions:
                return None
            token = secrets.token_urlsafe(32)
            self._sessions[hashlib.sha256(token.encode("utf-8")).digest()] = (
                now + self._lifetime
            )
            return token

    def resolve(self, token: str) -> AuthenticatedPrincipal | None:
        if not isinstance(token, str) or not token or len(token) > 256:
            return None
        key = hashlib.sha256(token.encode("utf-8")).digest()
        with self._lock:
            expires = self._sessions.get(key)
            if expires is None:
                return None
            if time.monotonic() >= expires:
                self._sessions.pop(key, None)
                return None
            return AuthenticatedPrincipal(
                self._credential.subject,
                self._credential.company_scopes,
                self._credential.roles,
            )

    def revoke(self, token: str) -> None:
        if isinstance(token, str) and len(token) <= 256:
            key = hashlib.sha256(token.encode("utf-8")).digest()
            with self._lock:
                self._sessions.pop(key, None)

    def revoke_all(self) -> None:
        with self._lock:
            self._sessions.clear()

    def _prune_expired(self, now: float) -> None:
        expired = [key for key, expires in self._sessions.items() if now >= expires]
        for key in expired:
            self._sessions.pop(key, None)
