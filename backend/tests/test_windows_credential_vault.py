import os

import pytest

from aram_backend.local_auth import create_credential
from aram_backend.windows_credential_vault import load_credential, save_credential

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows DPAPI only")


def test_dpapi_vault_round_trip_and_tamper_detection(tmp_path):
    path = tmp_path / "owner.credential.dpapi"
    credential = create_credential(
        "owner", "correct horse battery staple",
        frozenset({"001", "002"}), frozenset({"maker", "owner"}),
    )
    save_credential(path, credential)
    assert path.read_bytes() != credential.password_hash.encode()
    restored = load_credential(path)
    assert restored == credential
    encrypted = bytearray(path.read_bytes())
    encrypted[-1] ^= 0x01
    path.write_bytes(encrypted)
    with pytest.raises(OSError):
        load_credential(path)


def test_dpapi_vault_requires_absolute_path():
    credential = create_credential(
        "owner", "correct horse battery staple",
        frozenset({"001"}), frozenset({"owner"}),
    )
    with pytest.raises(ValueError):
        save_credential("relative.dpapi", credential)
