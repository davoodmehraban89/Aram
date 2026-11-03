import pytest
from cryptography.exceptions import InvalidTag

from aram_backend.credential_recovery import (
    export_recovery_envelope,
    import_recovery_envelope,
)
from aram_backend.local_auth import create_credential


def test_recovery_envelope_round_trip_and_wrong_passphrase():
    credential = create_credential(
        "owner", "correct horse battery staple",
        frozenset({"001", "002"}), frozenset({"owner", "maker"}),
    )
    envelope = export_recovery_envelope(credential, "separate recovery passphrase")
    assert b"correct horse battery staple" not in envelope
    assert import_recovery_envelope(envelope, "separate recovery passphrase") == credential
    with pytest.raises(InvalidTag):
        import_recovery_envelope(envelope, "incorrect recovery passphrase")


def test_recovery_envelope_rejects_tampering_and_malformed_input():
    credential = create_credential(
        "owner", "correct horse battery staple",
        frozenset({"001"}), frozenset({"owner"}),
    )
    envelope = bytearray(export_recovery_envelope(credential, "separate recovery passphrase"))
    envelope[-3] ^= 1
    with pytest.raises(ValueError):
        import_recovery_envelope(bytes(envelope), "separate recovery passphrase")
    with pytest.raises(ValueError):
        import_recovery_envelope(b"not-json", "separate recovery passphrase")


@pytest.mark.parametrize("passphrase", ["short", "", None])
def test_recovery_envelope_requires_strong_passphrase(passphrase):
    credential = create_credential(
        "owner", "correct horse battery staple",
        frozenset({"001"}), frozenset({"owner"}),
    )
    with pytest.raises(ValueError):
        export_recovery_envelope(credential, passphrase)
