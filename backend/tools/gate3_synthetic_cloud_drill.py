"""One-time synthetic encrypted Drive sync drill. No real data, no key on Drive."""
import hashlib
import json
import os
import secrets
from pathlib import Path
from tempfile import TemporaryDirectory

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingDecision

remote = Path(r"E:\My Drive\Aram-Gate3-Synthetic-Backup")
if not remote.is_dir():
    raise RuntimeError("Drive destination unavailable")
with TemporaryDirectory(prefix="aram-gate3-") as td:
    temp = Path(td)
    store = MappingStore(temp / "source.db")
    ws, rev = store.load("SYNTH", 1405)
    ws.propose(MappingDecision("TEST", "SYNTH", 1405, "100", "BS", "Assets", "1", None, 1, "Draft", None, "Synthetic"), actor="test-maker")
    store.save(ws, rev)
    receipt = store.audit_receipt("SYNTH", 1405)
    snapshot = temp / "snapshot.db"
    store.backup_to(snapshot)
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aad = b"aram-gate3-synthetic-cloud-drill-v1"
    ciphertext = nonce + AESGCM(key).encrypt(nonce, snapshot.read_bytes(), aad)
    name = "gate3-synthetic-" + secrets.token_hex(8) + ".aesgcm"
    target = remote / name
    if target.exists():
        raise RuntimeError("Refusing overwrite")
    target.write_bytes(ciphertext)
    print(json.dumps({"file":name,"encrypted_size":len(ciphertext),"sha256":hashlib.sha256(ciphertext).hexdigest(),"receipt":receipt,"status":"encrypted_uploaded_to_windows_drive_mount; cloud_readback_not_yet_verified"}))
    # Deliberately do not save the ephemeral key or financial plaintext to Drive.