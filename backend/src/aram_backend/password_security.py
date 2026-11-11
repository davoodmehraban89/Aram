"""Argon2id password hashing with explicit legacy PBKDF2 verification.

Only hashes are stored. Legacy verification is read-only; successful authentication
returns a replacement Argon2id hash for the caller to persist atomically.
"""
from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

from argon2 import PasswordHasher, Type
from argon2.exceptions import InvalidHashError, VerificationError

_HASHER = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2,
                         hash_len=32, salt_len=16, type=Type.ID)
_MAX_PASSWORD_BYTES = 4096
_LEGACY_ITERATIONS = 600_000


@dataclass(frozen=True)
class PasswordVerification:
    valid: bool
    upgraded_hash: str | None = None


def _encode_password(password: str) -> bytes:
    """Encode a password strictly; reject lone surrogates as invalid input."""
    if not isinstance(password, str):
        raise TypeError("invalid password")
    try:
        return password.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("invalid password") from exc


def _validate_password(password: str) -> bytes:
    raw = _encode_password(password)
    if not 14 <= len(password) <= 1024 or len(raw) > _MAX_PASSWORD_BYTES:
        raise ValueError("invalid password")
    return raw


def hash_password(password: str) -> str:
    _validate_password(password)
    return _HASHER.hash(password)


def verify_password(password: str, encoded: str) -> PasswordVerification:
    if not isinstance(password, str) or not isinstance(encoded, str):
        return PasswordVerification(False)
    try:
        raw = _encode_password(password)
    except (TypeError, ValueError):
        return PasswordVerification(False)
    if len(password) > 1024 or len(raw) > _MAX_PASSWORD_BYTES:
        return PasswordVerification(False)
    if encoded.startswith("$argon2id$"):
        try:
            valid = _HASHER.verify(encoded, password)
            return PasswordVerification(valid, _HASHER.hash(password) if valid and _HASHER.check_needs_rehash(encoded) else None)
        except (InvalidHashError, VerificationError, ValueError):
            return PasswordVerification(False)
    # Explicit legacy format: pbkdf2_sha256$600000$<hex salt>$<hex digest>.
    parts = encoded.split("$")
    if len(parts) != 4 or parts[0] != "pbkdf2_sha256" or parts[1] != str(_LEGACY_ITERATIONS):
        return PasswordVerification(False)
    try:
        salt = bytes.fromhex(parts[2])
        expected = bytes.fromhex(parts[3])
        if len(salt) != 32 or len(expected) != 32:
            return PasswordVerification(False)
        candidate = hashlib.pbkdf2_hmac("sha256", raw, salt, _LEGACY_ITERATIONS)
        if not hmac.compare_digest(candidate, expected):
            return PasswordVerification(False)
        return PasswordVerification(True, hash_password(password))
    except ValueError:
        return PasswordVerification(False)


def encode_legacy_credential(salt: bytes, digest: bytes) -> str:
    """Serialize existing credential hashes without ever exposing the password."""
    if not isinstance(salt, bytes) or len(salt) != 32 or not isinstance(digest, bytes) or len(digest) != 32:
        raise ValueError("invalid legacy credential")
    return "pbkdf2_sha256$" + str(_LEGACY_ITERATIONS) + "$" + salt.hex() + "$" + digest.hex()
