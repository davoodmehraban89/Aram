"""Single-owner local session adapter; not a substitute for an enterprise IdP.

Credentials use Argon2id. Imported PBKDF2 credentials are upgraded after a
successful login. Sessions and lockout state are process-local and fail closed
on restart; do not expose this adapter publicly without persistent controls.
"""
from __future__ import annotations

import hashlib
import secrets
import threading
import time
from dataclasses import dataclass, replace

from aram_backend.mapping_access import AuthenticatedPrincipal
from aram_backend.password_security import (
    encode_legacy_credential,
    hash_password,
    verify_password,
)

_MAX_PASSWORD_LENGTH = 1024
_ALLOWED_ROLES = frozenset({"maker", "reviewer", "approver", "owner"})


@dataclass(frozen=True)
class LocalCredential:
    subject: str
    company_scopes: frozenset[str]
    roles: frozenset[str]
    password_hash: str


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
    return LocalCredential(
        subject.strip(), frozenset(companies), frozenset(roles), hash_password(password)
    )


def import_legacy_credential(
    subject: str,
    companies: frozenset[str],
    roles: frozenset[str],
    salt: bytes,
    password_hash: bytes,
) -> LocalCredential:
    """Import old PBKDF2 material without receiving or storing plaintext."""
    if (
        not isinstance(subject, str) or not subject.strip() or len(subject) > 200
        or not companies or any(not isinstance(c, str) or not c.strip() or len(c) > 64 for c in companies)
        or not roles or not roles.issubset(_ALLOWED_ROLES)
    ):
        raise ValueError("invalid local credential configuration")
    encoded = encode_legacy_credential(salt, password_hash)
    return LocalCredential(subject.strip(), frozenset(companies), frozenset(roles), encoded)


class LocalSessionAuthority:
    """Volatile single-credential sessions with bounded lockout.

    Restart revokes all sessions and clears lockout. Lockout is process-local;
    persistent cross-process rate limiting and durable identity are not provided.
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

    @property
    def lifetime_seconds(self) -> int:
        return self._lifetime

    def login(self, password: str) -> str | None:
        if not isinstance(password, str) or len(password) > _MAX_PASSWORD_LENGTH:
            return None
        with self._lock:
            now = time.monotonic()
            if now < self._locked_until:
                return None
            verification = verify_password(password, self._credential.password_hash)
            if not verification.valid:
                self._failed_attempts += 1
                if self._failed_attempts >= self._max_failed_attempts:
                    self._locked_until = now + self._lockout_seconds
                    self._failed_attempts = 0
                return None

            if verification.upgraded_hash is not None:
                self._credential = replace(
                    self._credential, password_hash=verification.upgraded_hash
                )
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
