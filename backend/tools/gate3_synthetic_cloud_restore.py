"""Synthetic-only encrypted backup and isolated restore via Drive mount.

This verifies the mounted copy, NOT an independent cloud API download.
No real data, persistent key, or credential is used.
"""
import hashlib
import json
import os
import secrets
import tempfile
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingDecision


def main():
    drive = Path("E:/My Drive/Aram-Gate3-Synthetic-Backup")
    if not drive.is_dir():
        raise RuntimeError("Google Drive mount not available")
    with tempfile.TemporaryDirectory(prefix="aram-gate3-") as directory:
        root = Path(directory)
        source = MappingStore(root / "source.db")
        workspace, revision = source.load("SYNTH", 1405)
        workspace.propose(
            MappingDecision("RESTORE-TEST", "SYNTH", 1405, "100", "BS",
                            "Assets", "1", None, 1, "Draft", None, "Synthetic"),
            actor="synthetic-test",
        )
        source.save(workspace, revision)
        receipt = source.audit_receipt("SYNTH", 1405)
        snapshot = root / "snapshot.db"
        source.backup_to(snapshot)
        plaintext = snapshot.read_bytes()
        key = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)
        associated_data = b"aram-gate3-synthetic-restore-v1"
        encrypted = nonce + AESGCM(key).encrypt(nonce, plaintext, associated_data)
        filename = "gate3-restore-" + secrets.token_hex(8) + ".aesgcm"
        remote = drive / filename
        with remote.open("xb") as handle:
            handle.write(encrypted)
        readback = remote.read_bytes()
        if hashlib.sha256(readback).digest() != hashlib.sha256(encrypted).digest():
            raise RuntimeError("mounted readback digest mismatch")
        decrypted = AESGCM(key).decrypt(readback[:12], readback[12:], associated_data)
        if hashlib.sha256(decrypted).digest() != hashlib.sha256(plaintext).digest():
            raise RuntimeError("decrypted database digest mismatch")
        restored = MappingStore(root / "restored.db")
        Path(restored.path).write_bytes(decrypted)
        restored.verify_integrity()
        restored.verify_external_receipt(receipt)
        if restored.load("SYNTH", 1405)[0].decisions != workspace.decisions:
            raise RuntimeError("restored mapping mismatch")
        tampered = bytearray(readback)
        tampered[-1] ^= 1
        try:
            AESGCM(key).decrypt(tampered[:12], tampered[12:], associated_data)
        except InvalidTag:
            pass
        else:
            raise RuntimeError("tamper detection failed")
        print(json.dumps({
            "status": "PASS",
            "file": filename,
            "ciphertext_sha256": hashlib.sha256(readback).hexdigest(),
            "sqlite_integrity": True,
            "audit_receipt": True,
            "tamper_rejected": True,
            "independent_cloud_download": False,
            "real_financial_data": False,
        }))


if __name__ == "__main__":
    main()
