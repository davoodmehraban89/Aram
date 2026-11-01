from aram_backend.main import app
from aram_backend.mapping_access import AuthenticatedPrincipal
from aram_backend.mapping_api import configure_mapping_service, reset_mapping_service
from aram_backend.mapping_store import MappingStore
from fastapi.testclient import TestClient


def test_mapping_http_fail_closed_and_three_party_approval(tmp_path):
    client = TestClient(app)
    base = "/api/v1/mapping/001/1405"
    proposal = {
        "mapping_id": "M1", "account_full_code": "0010",
        "target_statement": "BS", "statement_section": "Assets", "note_number": "01",
    }
    reset_mapping_service()
    assert client.post(base + "/proposals", json=proposal).status_code == 401
    assert client.post(base + "/proposals", json=proposal,
                       headers={"Authorization": "Bearer invalid"}).status_code == 503
    people = {
        "token-m": AuthenticatedPrincipal("maker", frozenset({"001"}), frozenset({"maker", "approver"})),
        "token-r": AuthenticatedPrincipal("reviewer", frozenset({"001"}), frozenset({"reviewer"})),
        "token-a": AuthenticatedPrincipal("approver", frozenset({"001"}), frozenset({"approver"})),
        "token-f": AuthenticatedPrincipal("foreign", frozenset({"002"}), frozenset({"maker"})),
    }
    store = MappingStore(tmp_path / "api.db")
    configure_mapping_service(store=store, identity_resolver=people.get)
    try:
        def post(path, token, data=None):
            return client.post(base + path, headers={"Authorization": "Bearer " + token},
                               json=data)
        assert post("/proposals", "token-f", proposal).status_code == 403
        assert post("/proposals", "unknown", proposal).status_code == 403
        assert post("/proposals", "token-m", {**proposal, "actor": "approver"}).status_code == 200
        assert post("/M1/review", "token-m").status_code == 403
        assert post("/M1/approve", "token-a").status_code == 422
        assert post("/M1/review", "token-r").status_code == 200
        assert post("/M1/approve", "token-m").status_code == 422
        assert post("/M1/approve", "token-a").status_code == 200
        assert store.load("001", 1405)[0].decisions[0].status == "Approved"
        assert [e.actor for e in store.audit_log("001", 1405)] == [
            "maker", "reviewer", "approver",
        ]
        assert post("/M1/revise", "token-r", {
            "target_statement": "IS", "statement_section": "Revenue",
            "note_number": "02",
        }).status_code == 403
    finally:
        reset_mapping_service()


def test_mapping_http_does_not_trust_header_actor_or_roles(tmp_path):
    store = MappingStore(tmp_path / "scope.db")
    configure_mapping_service(store=store, identity_resolver=lambda _: None)
    try:
        client = TestClient(app)
        response = client.post(
            "/api/v1/mapping/001/1405/proposals",
            headers={"Authorization": "Bearer fake", "X-Actor": "admin",
                     "X-Roles": "approver", "X-Company": "001"},
            json={"mapping_id": "M1", "account_full_code": "0010",
                  "target_statement": "BS", "statement_section": "Assets",
                  "note_number": "01"},
        )
        assert response.status_code == 403
        assert store.load("001", 1405)[0].decisions == ()
    finally:
        reset_mapping_service()
