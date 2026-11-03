"""Passphrase-encrypted offline recovery envelope for a local credential.

The envelope is portable across Windows profiles. Its passphrase must be stored
separately and never placed beside the envelope. This module does not upload
anything to cloud storage or prove that an external copy exists.
"""
from __future__ import annotations

import base64
import json
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from aram_backend.local_auth import LocalCredential

_VERSION = 1
_SCRYPT_N = 1 << 15
_SCRYPT_R = 8
_SCRYPT_P = 1


def _derive(passphrase: str, salt: bytes) -> bytes:
    if not isinstance(passphrase, str) or not 16 <= len(passphrase) <= 1024:
        raise ValueError("recovery passphrase must be 16 to 1024 characters")
    return Scrypt(salt=salt, length=32, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P).derive(
        passphrase.encode("utf-8")
    )


def export_recovery_envelope(credential: LocalCredential, passphrase: str) -> bytes:
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = _derive(passphrase, salt)
    payload = json.dumps({
        "subject": credential.subject,
        "company_scopes": sorted(credential.company_scopes),
        "roles": sorted(credential.roles),
        "password_hash": credential.password_hash,
    }, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, payload, b"Aram.CredentialRecovery.v1")
    envelope = {
        "version": _VERSION,
        "kdf": "scrypt-32768-8-1",
        "salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }
    return json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode("ascii")


def import_recovery_envelope(envelope: bytes, passphrase: str) -> LocalCredential:
    if not isinstance(envelope, bytes) or not 1 <= len(envelope) <= 1_048_576:
        raise ValueError("invalid recovery envelope")
    try:
        record = json.loads(envelope)
        if record.get("version") != _VERSION or record.get("kdf") != "scrypt-32768-8-1":
            raise ValueError("unsupported recovery envelope")
        salt = base64.b64decode(record["salt"], validate=True)
        nonce = base64.b64decode(record["nonce"], validate=True)
        ciphertext = base64.b64decode(record["ciphertext"], validate=True)
        if len(salt) != 16 or len(nonce) != 12 or not 16 <= len(ciphertext) <= 65536:
            raise ValueError("invalid recovery envelope")
        key = _derive(passphrase, salt)
        payload = AESGCM(key).decrypt(
            nonce, ciphertext, b"Aram.CredentialRecovery.v1"
        )
        data = json.loads(payload)
        subject = data["subject"]
        companies = frozenset(data["company_scopes"])
        roles = frozenset(data["roles"])
        password_hash = data["password_hash"]
        if (
            not isinstance(subject, str) or not subject.strip() or len(subject) > 200
            or not companies or any(not isinstance(x, str) or not x.strip() or len(x) > 64 for x in companies)
            or not roles or not roles.issubset({"maker", "reviewer", "approver", "owner"})
            or not isinstance(password_hash, str) or len(password_hash) > 1024
        ):
            raise ValueError("invalid recovered credential")
        return LocalCredential(subject, companies, roles, password_hash)
    except (KeyError, TypeError, json.JSONDecodeError, base64.binascii.Error) as exc:
        raise ValueError("invalid recovery envelope") from exc
