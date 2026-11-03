import os

import pytest
from fastapi.testclient import TestClient

from aram_backend.auth_api import (
    configure_local_auth_from_vault,
    configure_local_auth_service,
    reset_local_auth_service,
)
from aram_backend.local_auth import LocalSessionAuthority, create_credential
from aram_backend.main import app
from aram_backend.mapping_store import MappingStore
from aram_backend.windows_credential_vault import save_credential


def test_auth_api_fails_closed_until_explicit_configuration():
    reset_local_auth_service()
    client = TestClient(app)
    assert client.post("/api/v1/auth/login", json={"password": "correct horse battery staple"}).status_code == 503
    assert client.post("/api/v1/auth/logout", headers={"Authorization": "Bearer anything"}).status_code == 503


def test_auth_api_login_mapping_and_logout_end_to_end(tmp_path):
    credential = create_credential(
        "owner", "correct horse battery staple",
        frozenset({"001"}), frozenset({"maker"}),
    )
    authority = LocalSessionAuthority(credential)
    configure_local_auth_service(
        authority=authority, store=MappingStore(tmp_path / "auth-api.db")
    )
    client = TestClient(app)
    try:
        assert client.post("/api/v1/auth/login", json={"password": "incorrect password"}).status_code == 401
        response = client.post(
            "/api/v1/auth/login", json={"password": "correct horse battery staple"}
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        assert response.json()["token_type"] == "bearer"
        proposal = {
            "mapping_id": "AUTH-1", "account_full_code": "0010",
            "target_statement": "BS", "statement_section": "Assets",
            "note_number": "01",
        }
        headers = {"Authorization": "Bearer " + token}
        created = client.post("/api/v1/mapping/001/1405/proposals", json=proposal, headers=headers)
        assert created.status_code == 200
        logged_out = client.post("/api/v1/auth/logout", headers=headers)
        assert logged_out.status_code == 200
        assert logged_out.json() == {"revoked": True}
        rejected = client.post("/api/v1/mapping/001/1405/proposals", json={
            **proposal, "mapping_id": "AUTH-2",
        }, headers=headers)
        assert rejected.status_code == 403
    finally:
        reset_local_auth_service()

def test_auth_api_can_load_current_user_dpapi_vault(tmp_path):
    if os.name != "nt":
        pytest.skip("Windows DPAPI only")
    credential = create_credential(
        "owner", "correct horse battery staple",
        frozenset({"001"}), frozenset({"maker"}),
    )
    vault = tmp_path / "owner.dpapi"
    save_credential(vault, credential)
    configure_local_auth_from_vault(
        credential_path=str(vault), store=MappingStore(tmp_path / "vault-api.db")
    )
    client = TestClient(app)
    try:
        response = client.post(
            "/api/v1/auth/login", json={"password": "correct horse battery staple"}
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        assert client.post(
            "/api/v1/auth/logout", headers={"Authorization": "Bearer " + token}
        ).json() == {"revoked": True}
    finally:
        reset_local_auth_service()
