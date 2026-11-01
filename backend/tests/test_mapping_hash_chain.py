import sqlite3

import pytest
from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingDecision, MappingWorkflowError


def decision():
    return MappingDecision("M1", "001", 1405, "0010", "BS", "Assets",
                           "01", None, 1, "Draft", None, "Manual")


def test_audit_hash_chain_receipt_and_restore(tmp_path):
    store = MappingStore(tmp_path / "original.db")
    workspace, revision = store.load("001", 1405)
    workspace.propose(decision(), actor="maker")
    revision = store.save(workspace, revision)
    workspace.transition("M1", "Reviewed", actor="reviewer")
    store.save(workspace, revision)
    receipt = store.audit_receipt("001", 1405)
    assert len(receipt["sha256"]) == 64
    store.verify_external_receipt(receipt)
    store.backup_to(tmp_path / "backup.db")
    restored = MappingStore(tmp_path / "backup.db")
    restored.verify_external_receipt(receipt)
    with pytest.raises(MappingWorkflowError, match="external anchor"):
        store.verify_external_receipt({**receipt, "sha256": "f" * 64})


def test_detects_tampered_chain_and_missing_digest(tmp_path):
    path = tmp_path / "tamper.db"
    store = MappingStore(path)
    workspace, revision = store.load("001", 1405)
    workspace.propose(decision(), actor="maker")
    store.save(workspace, revision)
    with sqlite3.connect(path) as db:
        db.execute("UPDATE mapping_audit_hash SET digest=?", ("f" * 64,))
    with pytest.raises(MappingWorkflowError, match="hash chain mismatch"):
        store.verify_integrity()
    with sqlite3.connect(path) as db:
        db.execute("DELETE FROM mapping_audit_hash")
    with pytest.raises(MappingWorkflowError, match="missing event digest"):
        store.verify_integrity()
