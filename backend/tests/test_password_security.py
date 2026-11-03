"""Security tests: correct, invalid, malformed, migration and boundary paths."""
import hashlib
import secrets

import pytest

from aram_backend.password_security import (
    encode_legacy_credential,
    hash_password,
    verify_password,
)

PASSWORD = "correct horse battery staple"


def test_argon2id_round_trip_and_wrong_password():
    encoded = hash_password(PASSWORD)
    assert encoded.startswith("$argon2id$")
    assert verify_password(PASSWORD, encoded).valid
    assert verify_password(PASSWORD, encoded).upgraded_hash is None
    assert not verify_password("incorrect password", encoded).valid


def test_legacy_migration_and_no_plaintext_storage():
    salt = secrets.token_bytes(32)
    digest = hashlib.pbkdf2_hmac("sha256", PASSWORD.encode(), salt, 600_000)
    encoded = encode_legacy_credential(salt, digest)
    assert PASSWORD not in encoded
    result = verify_password(PASSWORD, encoded)
    assert result.valid and result.upgraded_hash.startswith("$argon2id$")
    assert verify_password(PASSWORD, result.upgraded_hash).valid
    assert not verify_password("incorrect password", encoded).valid


@pytest.mark.parametrize("encoded", ["", "garbage", "$argon2id$bad", "pbkdf2_sha256$600000$00$00",
                                     "pbkdf2_sha256$1$00$00", None])
def test_malformed_hashes_fail_closed(encoded):
    assert not verify_password(PASSWORD, encoded).valid


@pytest.mark.parametrize("password", ["", "short", "x" * 1025, None])
def test_invalid_provisioning(password):
    with pytest.raises((ValueError, TypeError)):
        hash_password(password)


def test_password_unicode_and_boundary():
    password = "رمز-آرام-" + "a" * 14
    assert verify_password(password, hash_password(password)).valid
    assert verify_password("x" * 1025, hash_password(PASSWORD)).valid is False


def test_reject_bad_legacy_material():
    with pytest.raises(ValueError):
        encode_legacy_credential(b"x", b"y")
