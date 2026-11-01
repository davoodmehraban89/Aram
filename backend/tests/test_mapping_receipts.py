import sqlite3

import pytest
from aram_backend.mapping_access import MappingAccess
from aram_backend.mapping_receipts import ReceiptArchive
from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import (
    MappingDecision,
    MappingWorkflowError,
    MappingWorkspace,
)


def decision():
    return MappingDecision("M1", "001", 1405, "0010", "BS", "Assets",
                           "01", None, 1, "Draft", None, "Manual")


def test_separate_receipt_archive_backup_and_tamper(tmp_path):
    store = MappingStore(tmp_path / "state.db")
    workspace, revision = store.load("001", 1405)
    workspace.propose(decision(), actor="maker")
    store.save(workspace, revision)
    directory = tmp_path / "separate-archive"
    directory.mkdir()
    archive = ReceiptArchive(directory)
    path = archive.record(store, "001", 1405)
    archive.verify(store, "001", 1405, 1)
    with pytest.raises(MappingWorkflowError, match="overwrite forbidden"):
        archive.record(store, "001", 1405)
    backup = tmp_path / "restored.db"
    store.backup_to(backup)
    archive.verify(MappingStore(backup), "001", 1405, 1)
    with sqlite3.connect(store.path) as db:
        db.execute("UPDATE mapping_audit_hash SET digest=?", ("f" * 64,))
    with pytest.raises(MappingWorkflowError, match="hash chain mismatch"):
        archive.verify(store, "001", 1405, 1)
    path.write_text('{"broken":true}', encoding="utf-8")
    with pytest.raises(MappingWorkflowError, match="identity mismatch"):
        archive.verify(MappingStore(backup), "001", 1405, 1)


def test_receipt_archive_rejects_traversal_and_missing_directory(tmp_path):
    with pytest.raises(MappingWorkflowError, match="already exist"):
        ReceiptArchive(tmp_path / "absent")
    directory = tmp_path / "receipts"
    directory.mkdir()
    archive = ReceiptArchive(directory)
    with pytest.raises(MappingWorkflowError, match="invalid receipt identity"):
        archive._path("../other", 1405, 1)


def test_resolver_error_fails_closed():
    def unavailable(_):
        raise RuntimeError("identity service unavailable")

    with pytest.raises(MappingWorkflowError, match="access denied"):
        MappingAccess(unavailable).propose("token", MappingWorkspace("001", 1405), decision())
