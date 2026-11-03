"""Synthetic encrypted backup transport: AES-256-GCM, no real ledger data."""
import hashlib
import os
from pathlib import Path

import pytest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingDecision


def test_encrypted_snapshot_restore_and_tamper_rejection(tmp_path: Path):
    store = MappingStore(tmp_path / "source.db")
    ws, rev = store.load("SYNTH", 1405)
    ws.propose(MappingDecision("S1", "SYNTH", 1405, "100", "BS", "Assets", "1", None, 1, "Draft", None, "Synthetic"), actor="synthetic-maker")
    store.save(ws, rev)
    snapshot = tmp_path / "snapshot.db"
    store.backup_to(snapshot)
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aad = b"aram-gate3-synthetic-backup-v1"
    encrypted = nonce + AESGCM(key).encrypt(nonce, snapshot.read_bytes(), aad)
    uploaded = tmp_path / "cloud-copy.enc"
    uploaded.write_bytes(encrypted)
    assert hashlib.sha256(uploaded.read_bytes()).digest() == hashlib.sha256(encrypted).digest()
    decrypted = AESGCM(key).decrypt(uploaded.read_bytes()[:12], uploaded.read_bytes()[12:], aad)
    recovered_path = tmp_path / "restored.db"
    recovered_path.write_bytes(decrypted)
    recovered = MappingStore(recovered_path)
    recovered.verify_integrity()
    assert recovered.load("SYNTH", 1405)[0].decisions == ws.decisions
    tampered = bytearray(encrypted)
    tampered[-1] ^= 1
    with pytest.raises(InvalidTag):
        AESGCM(key).decrypt(tampered[:12], tampered[12:], aad)