"""Current-user Windows DPAPI credential vault.

DPAPI CurrentUser protects a credential record at rest for the Windows user
profile that provisioned it. It is not an independent disaster-recovery copy:
profile loss can make the record unrecoverable. Store the vault on a local,
user-controlled NTFS directory with restrictive ACLs.
"""
from __future__ import annotations

import ctypes
import json
import os
import tempfile
from ctypes import wintypes
from pathlib import Path

from aram_backend.local_auth import LocalCredential

_ENTROPY = b"Aram.LocalCredentialVault.v1"
_UI_FORBIDDEN = 0x1


class _DataBlob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def _dpapi_transform(data: bytes, *, protect: bool) -> bytes:
    if os.name != "nt":
        raise OSError("Windows DPAPI is available only on Windows")
    if not isinstance(data, bytes) or not data or len(data) > 1_048_576:
        raise ValueError("invalid credential vault payload")
    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    crypt32.CryptProtectData.argtypes = [ctypes.POINTER(_DataBlob), wintypes.LPCWSTR, ctypes.POINTER(_DataBlob), ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(_DataBlob)]
    crypt32.CryptProtectData.restype = wintypes.BOOL
    crypt32.CryptUnprotectData.argtypes = [ctypes.POINTER(_DataBlob), ctypes.POINTER(wintypes.LPWSTR), ctypes.POINTER(_DataBlob), ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(_DataBlob)]
    crypt32.CryptUnprotectData.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    kernel32.LocalFree.restype = ctypes.c_void_p

    def blob(raw: bytes):
        buffer = ctypes.create_string_buffer(raw)
        return _DataBlob(len(raw), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_byte))), buffer

    source, source_buffer = blob(data)
    entropy, entropy_buffer = blob(_ENTROPY)
    output = _DataBlob()
    if protect:
        ok = crypt32.CryptProtectData(
            ctypes.byref(source), "Aram credential vault",
            ctypes.byref(entropy), None, None, _UI_FORBIDDEN,
            ctypes.byref(output),
        )
    else:
        ok = crypt32.CryptUnprotectData(
            ctypes.byref(source), None, ctypes.byref(entropy),
            None, None, _UI_FORBIDDEN, ctypes.byref(output),
        )
    if not ok:
        raise OSError(ctypes.get_last_error(), "Windows DPAPI operation failed")
    try:
        return ctypes.string_at(output.pbData, output.cbData)
    finally:
        kernel32.LocalFree(output.pbData)
        del source_buffer, entropy_buffer


def protect_current_user(data: bytes) -> bytes:
    return _dpapi_transform(data, protect=True)


def unprotect_current_user(data: bytes) -> bytes:
    return _dpapi_transform(data, protect=False)


def save_credential(path: str | Path, credential: LocalCredential) -> None:
    target = Path(path)
    if not target.is_absolute():
        raise ValueError("credential vault path must be absolute")
    payload = json.dumps({
        "version": 1,
        "subject": credential.subject,
        "company_scopes": sorted(credential.company_scopes),
        "roles": sorted(credential.roles),
        "password_hash": credential.password_hash,
    }, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    encrypted = protect_current_user(payload)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(encrypted)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_credential(path: str | Path) -> LocalCredential:
    target = Path(path)
    if not target.is_absolute() or not target.is_file():
        raise ValueError("credential vault is unavailable")
    encrypted = target.read_bytes()
    payload = unprotect_current_user(encrypted)
    if len(payload) > 1_048_576:
        raise ValueError("invalid credential vault payload")
    try:
        record = json.loads(payload)
        if record.get("version") != 1:
            raise ValueError("unsupported credential vault version")
        subject = record["subject"]
        companies = frozenset(record["company_scopes"])
        roles = frozenset(record["roles"])
        password_hash = record["password_hash"]
        if (
            not isinstance(subject, str) or not subject.strip() or len(subject) > 200
            or not companies or any(not isinstance(x, str) or not x.strip() or len(x) > 64 for x in companies)
            or not roles or not roles.issubset({"maker", "reviewer", "approver", "owner"})
            or not isinstance(password_hash, str) or len(password_hash) > 1024
        ):
            raise ValueError("invalid credential vault record")
        return LocalCredential(subject, companies, roles, password_hash)
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid credential vault record") from exc
