"""Synthetic RSA token checks only; NOT a connected real enterprise IdP."""
from datetime import UTC, datetime
from time import time

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from aram_backend.config import Settings, get_settings
from aram_backend.main import app

ISSUER = "https://synthetic-identity.example.invalid/"
AUDIENCE = "aram-mapping-api"


@pytest.fixture(scope="module")
def keys():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private, public, other


@pytest.fixture
def auth_client(keys):
    private, public, other = keys
    app.dependency_overrides[get_settings] = lambda: Settings(
        auth_issuer=ISSUER, auth_audience=AUDIENCE,
        auth_public_key_pem=public,
    )
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_settings, None)


def claims(**extra):
    now = int(time())
    data = {
        "iss": ISSUER, "aud": AUDIENCE, "sub": "employee-108",
        "exp": now + 300, "iat": now - 10, "nbf": now - 10,
        "token_use": "access", "aram_roles": ["mapping_proposer"],
    }
    data.update(extra)
    return data


def token(private, **extra):
    return jwt.encode(claims(**extra), private, algorithm="RS256")


def request(client, bearer, **headers):
    return client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {bearer}", **headers},
    )


def test_valid_rs256_access_token_returns_verified_subject_and_role(auth_client, keys):
    response = request(auth_client, token(keys[0]))
    assert response.status_code == 200
    body = response.json()
    assert body["issuer"] == ISSUER
    assert body["subject"] == "employee-108"
    assert body["roles"] == ["mapping_proposer"]
    assert body["expires_at"] > int(time())
    assert "token" not in body
    assert "private_key" not in body


def test_missing_bearer_or_forged_identity_headers_are_not_authentication(auth_client):
    response = auth_client.get(
        "/api/v1/auth/me",
        headers={"X-User": "admin", "X-ARAM-Roles": "mapping_reviewer"},
    )
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_wrong_key_signed_token_cannot_impersonate_user(auth_client, keys):
    response = request(
        auth_client,
        token(keys[2], sub="finance-director", aram_roles=["mapping_reviewer"]),
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid bearer token"


@pytest.mark.parametrize("overrides", [
    {"iss": "https://attacker.invalid/"},
    {"aud": "not-aram"},
    {"exp": 1},
    {"nbf": int(time()) + 10000},
    {"iat": int(time()) + 10000},
    {"exp": int(time()) + 20000},
    {"sub": ""},
    {"sub": " invalid "},
    {"sub": 123},
    {"token_use": "id"},
    {"aram_roles": "mapping_reviewer"},
    {"aram_roles": ["system_administrator"]},
    {"aram_roles": ["mapping_reviewer", "mapping_reviewer"]},
    {"aram_roles": ["mapping_proposer", "mapping_reviewer"]},
    {"aram_roles": []},
    {"aram_roles": [123]},
])
def test_invalid_or_overprivileged_claims_are_rejected(auth_client, keys, overrides):
    assert request(auth_client, token(keys[0], **overrides)).status_code == 401


@pytest.mark.parametrize("missing", [
    "iss", "aud", "sub", "exp", "iat", "nbf", "token_use", "aram_roles",
])
def test_required_claims_cannot_be_omitted(auth_client, keys, missing):
    data = claims()
    del data[missing]
    assert request(
        auth_client, jwt.encode(data, keys[0], algorithm="RS256")
    ).status_code == 401


def test_unsigned_and_hmac_algorithms_are_never_accepted(auth_client, keys):
    unsigned = jwt.encode(claims(), key="", algorithm="none")
    hmac_signed = jwt.encode(claims(), key="untrusted", algorithm="HS256")
    assert request(auth_client, unsigned).status_code == 401
    assert request(auth_client, hmac_signed).status_code == 401


def test_roles_must_come_from_signed_claims_not_http_headers(auth_client, keys):
    response = request(
        auth_client, token(keys[0]),
        **{"X-ARAM-Roles": "mapping_reviewer", "X-Approver-ID": "boss"},
    )
    assert response.status_code == 200
    assert response.json()["roles"] == ["mapping_proposer"]


def test_unconfigured_identity_is_closed_and_never_bypasses(auth_client, keys):
    app.dependency_overrides[get_settings] = lambda: Settings()
    response = request(auth_client, token(keys[0]))
    assert response.status_code == 503
    assert "not configured" in response.json()["detail"].lower()


def test_private_key_misconfiguration_is_rejected(auth_client, keys):
    secret_pem = keys[0].private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    app.dependency_overrides[get_settings] = lambda: Settings(
        auth_issuer=ISSUER, auth_audience=AUDIENCE,
        auth_public_key_pem=secret_pem,
    )
    assert request(auth_client, token(keys[0])).status_code == 503


def test_only_bearer_scheme_allowed(auth_client, keys):
    response = auth_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Basic abc"},
    )
    assert response.status_code == 401


def test_long_bearer_token_is_rejected(auth_client):
    response = request(auth_client, "x" * 9000)
    assert response.status_code == 401


def test_only_a_read_only_identity_endpoint_is_exposed(auth_client, keys):
    assert auth_client.post(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token(keys[0])}"}
    ).status_code == 405
    assert auth_client.get("/api/v1/health").status_code == 200


def test_signed_reviewer_role_is_accepted_but_no_approval_action_exists(auth_client, keys):
    response = request(
        auth_client, token(keys[0], sub="independent-reviewer-22",
                           aram_roles=["mapping_reviewer"]),
    )
    assert response.status_code == 200
    assert response.json()["roles"] == ["mapping_reviewer"]
    assert auth_client.post(
        "/api/v1/mapping/approve",
        headers={"Authorization": f"Bearer {token(keys[0], aram_roles=['mapping_reviewer'])}"},
    ).status_code == 404


def test_token_payload_tampering_invalidates_signature(auth_client, keys):
    import base64
    import json
    signed = token(keys[0])
    header, payload, signature = signed.split(".")
    decoded = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    decoded["aram_roles"] = ["mapping_reviewer"]
    tampered_payload = base64.urlsafe_b64encode(
        json.dumps(decoded, separators=(",", ":")).encode()
    ).rstrip(b"=").decode()
    assert request(auth_client, f"{header}.{tampered_payload}.{signature}").status_code == 401


def test_weak_rsa_verification_key_is_not_accepted(auth_client, keys):
    weak = rsa.generate_private_key(public_exponent=65537, key_size=1024)
    weak_public_pem = weak.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")
    app.dependency_overrides[get_settings] = lambda: Settings(
        auth_issuer=ISSUER, auth_audience=AUDIENCE,
        auth_public_key_pem=weak_public_pem,
    )
    assert request(auth_client, token(keys[0])).status_code == 503


def test_invalid_or_non_rsa_public_key_disables_identity(auth_client, keys):
    app.dependency_overrides[get_settings] = lambda: Settings(
        auth_issuer=ISSUER, auth_audience=AUDIENCE,
        auth_public_key_pem="not a PEM public key",
    )
    assert request(auth_client, token(keys[0])).status_code == 503
