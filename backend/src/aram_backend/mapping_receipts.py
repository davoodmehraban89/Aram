"""Experimental off-database audit receipt store.

The configured directory MUST reside on a separately administered, protected
volume for any security claim. A local directory is only a test double.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingWorkflowError


class ReceiptArchive:
    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        if not self.directory.is_dir():
            raise MappingWorkflowError("receipt archive directory must already exist")

    def _path(self, company: str, year: int, revision: int) -> Path:
        if not company.isalnum() or not isinstance(year, int) or not isinstance(revision, int):
            raise MappingWorkflowError("invalid receipt identity")
        if year <= 0 or revision < 0:
            raise MappingWorkflowError("invalid receipt version")
        return self.directory / f"{company}-{year}-{revision}.json"

    def record(self, store: MappingStore, company: str, year: int) -> Path:
        receipt = store.audit_receipt(company, year)
        path = self._path(company, year, receipt["revision"])
        data = (json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise MappingWorkflowError("receipt already exists; overwrite forbidden") from exc
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            path.unlink(missing_ok=True)
            raise
        return path

    def verify(self, store: MappingStore, company: str, year: int, revision: int) -> None:
        path = self._path(company, year, revision)
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise MappingWorkflowError("trusted audit receipt missing or invalid") from exc
        if (receipt.get("company_code"), receipt.get("fiscal_year"), receipt.get("revision")) != (
            company, year, revision
        ):
            raise MappingWorkflowError("trusted audit receipt identity mismatch")
        store.verify_external_receipt(receipt)
