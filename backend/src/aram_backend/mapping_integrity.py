"""Deterministic SHA-256 audit chain and externally anchored integrity evidence.

SHA-256 is not authentication. A privileged DB writer can recompute all hashes.
A trusted operator must retain the terminal digest outside the database.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from aram_backend.mapping_workflow import MappingAuditEvent, MappingWorkflowError

GENESIS = "0" * 64


def _canonical(event: MappingAuditEvent) -> bytes:
    return json.dumps(asdict(event), sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def audit_chain(events: tuple[MappingAuditEvent, ...]) -> tuple[str, ...]:
    previous = GENESIS
    digests = []
    for event in events:
        previous = hashlib.sha256(
            bytes.fromhex(previous) + _canonical(event)
        ).hexdigest()
        digests.append(previous)
    return tuple(digests)


def verify_audit_chain(
    events: tuple[MappingAuditEvent, ...], stored: tuple[str, ...],
    *, trusted_terminal_digest: str | None = None,
) -> str:
    expected = audit_chain(events)
    if expected != stored:
        raise MappingWorkflowError("audit hash chain mismatch")
    terminal = expected[-1] if expected else GENESIS
    if trusted_terminal_digest is not None and terminal != trusted_terminal_digest:
        raise MappingWorkflowError("audit external anchor mismatch")
    return terminal


def integrity_receipt(
    *, company_code: str, fiscal_year: int, revision: int,
    terminal_digest: str,
) -> dict[str, Any]:
    """Export receipt to an independent append-only system, not SQLite."""
    return {
        "company_code": company_code, "fiscal_year": fiscal_year,
        "revision": revision, "sha256": terminal_digest,
    }
