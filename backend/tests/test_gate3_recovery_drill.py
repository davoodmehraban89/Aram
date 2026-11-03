"""Synthetic, isolated Gate 3 backup and recovery evidence."""
import hashlib
from pathlib import Path

import pytest

from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingDecision, MappingWorkflowError


def test_sqlite_backup_restore_and_external_receipt_tamper_detection(tmp_path: Path):
    live = MappingStore(tmp_path / "live.db")
    workspace, revision = live.load("TEST", 1405)
    workspace.propose(MappingDecision("TEST-1", "TEST", 1405, "100", "BS", "Assets", "1", None, 1, "Draft", None, "Synthetic"), actor="test-maker")
    revision = live.save(workspace, revision)
    receipt = live.audit_receipt("TEST", 1405)
    assert receipt["revision"] == revision
    backup_path = tmp_path / "snapshot.db"
    live.backup_to(backup_path)
    snapshot_hash = hashlib.sha256(backup_path.read_bytes()).hexdigest()
    assert len(snapshot_hash) == 64
    restored = MappingStore(tmp_path / "restored.db")
    restored_path = Path(restored.path)
    restored_path.write_bytes(backup_path.read_bytes())
    restored.verify_integrity()
    restored.verify_external_receipt(receipt)
    assert restored.load("TEST", 1405)[0].decisions == workspace.decisions
    assert hashlib.sha256(restored_path.read_bytes()).hexdigest() == snapshot_hash
    with pytest.raises(MappingWorkflowError, match="destination must be new"):
        live.backup_to(backup_path)
    forged = dict(receipt, sha256="f" * 64)
    with pytest.raises(MappingWorkflowError, match="external anchor mismatch"):
        restored.verify_external_receipt(forged)