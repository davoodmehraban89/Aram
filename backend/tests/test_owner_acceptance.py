import pytest

from aram_backend.mapping_store import MappingStore
from aram_backend.mapping_workflow import MappingDecision, MappingWorkflowError


def test_owner_exception_persists_reason_and_does_not_approve(tmp_path):
    store = MappingStore(tmp_path / "owner.db")
    space, revision = store.load("001", 1405)
    space.propose(MappingDecision("M1", "001", 1405, "100", "BS", "Assets", "1", None, 1, "Draft", None, "Manual"), actor="owner")
    with pytest.raises(MappingWorkflowError, match="reason"):
        space.owner_accept("M1", actor="owner", reason="too short")
    accepted = space.owner_accept("M1", actor="owner", reason="Owner knowingly accepts missing independent review")
    assert accepted.status == "OwnerAcceptedWithException"
    assert accepted.reviewer is None
    assert space.audit[-1].reason.startswith("Owner knowingly")
    store.save(space, revision)
    loaded, _ = store.load("001", 1405)
    assert loaded.decisions[0].status != "Approved"
    assert loaded.audit[-1].reason == space.audit[-1].reason
    store.verify_integrity()
    with pytest.raises(MappingWorkflowError, match="invalid mapping lifecycle"):
        loaded.transition("M1", "Approved", actor="owner")


def test_owner_exception_cannot_be_made_from_reviewed(tmp_path):
    store = MappingStore(tmp_path / "owner2.db")
    space, _ = store.load("001", 1405)
    space.propose(MappingDecision("M1", "001", 1405, "100", "BS", "Assets", "1", None, 1, "Draft", None, "Manual"), actor="maker")
    space.transition("M1", "Reviewed", actor="reviewer")
    with pytest.raises(MappingWorkflowError, match="unreviewed Draft"):
        space.owner_accept("M1", actor="maker", reason="I acknowledge missing independent approval")

def test_owner_http_is_scoped_and_never_independent_approval(tmp_path):
    from fastapi.testclient import TestClient

    from aram_backend.main import app
    from aram_backend.mapping_access import AuthenticatedPrincipal
    from aram_backend.mapping_api import (
        configure_mapping_service,
        reset_mapping_service,
    )

    people = {
        "owner-token": AuthenticatedPrincipal("owner", frozenset({"001"}), frozenset({"owner", "maker"})),
        "maker-token": AuthenticatedPrincipal("maker", frozenset({"001"}), frozenset({"maker"})),
        "foreign-token": AuthenticatedPrincipal("other", frozenset({"002"}), frozenset({"owner"})),
    }
    store = MappingStore(tmp_path / "http-owner.db")
    configure_mapping_service(store=store, identity_resolver=people.get)
    try:
        client = TestClient(app)
        base = "/api/v1/mapping/001/1405"
        def post(path, token, data):
            return client.post(base + path, headers={"Authorization": "Bearer " + token}, json=data)
        proposal = {"mapping_id": "M1", "account_full_code": "100", "target_statement": "BS", "statement_section": "Assets", "note_number": "1"}
        assert post("/proposals", "maker-token", proposal).status_code == 200
        path = "/M1/owner-accept"
        reason = {"reason": "Owner explicitly accepts the lack of independent review"}
        assert post(path, "maker-token", reason).status_code == 403
        assert post(path, "foreign-token", reason).status_code == 403
        assert post(path, "owner-token", {"reason": "short"}).status_code == 422
        result = post(path, "owner-token", reason)
        assert result.status_code == 200, result.text
        assert result.json()["status"] == "OwnerAcceptedWithException"
        assert post("/M1/approve", "owner-token", {}).status_code == 403
        store.verify_integrity()
        assert store.audit_log("001", 1405)[-1].reason == reason["reason"]
    finally:
        reset_mapping_service()

def test_owner_api_requires_trusted_owner_role(tmp_path):
    from fastapi.testclient import TestClient

    from aram_backend.main import app
    from aram_backend.mapping_access import AuthenticatedPrincipal
    from aram_backend.mapping_api import (
        configure_mapping_service,
        reset_mapping_service,
    )
    store = MappingStore(tmp_path / "owner-api.db")
    people = {
        "maker": AuthenticatedPrincipal("owner", frozenset({"001"}), frozenset({"maker"})),
        "owner": AuthenticatedPrincipal("owner", frozenset({"001"}), frozenset({"owner"})),
        "foreign": AuthenticatedPrincipal("other", frozenset({"002"}), frozenset({"owner"})),
    }
    configure_mapping_service(store=store, identity_resolver=people.get)
    client = TestClient(app)
    base = "/api/v1/mapping/001/1405"
    try:
        payload = {"mapping_id": "M1", "account_full_code": "100", "target_statement": "BS",
                   "statement_section": "Assets", "note_number": "1"}
        assert client.post(base + "/proposals", headers={"Authorization": "Bearer maker"}, json=payload).status_code == 200
        path = base + "/M1/owner-accept"
        body = {"reason": "Owner acknowledges missing independent review"}
        assert client.post(path, json=body).status_code == 401
        assert client.post(path, headers={"Authorization": "Bearer maker"}, json=body).status_code == 403
        assert client.post(path, headers={"Authorization": "Bearer foreign"}, json=body).status_code == 403
        assert client.post(path, headers={"Authorization": "Bearer owner"}, json={"reason": "short"}).status_code == 422
        result = client.post(path, headers={"Authorization": "Bearer owner"}, json=body)
        assert result.status_code == 200
        assert result.json()["status"] == "OwnerAcceptedWithException"
        assert store.load("001", 1405)[0].audit[-1].reason == body["reason"]
        assert client.post(base + "/M1/approve", headers={"Authorization": "Bearer owner"}).status_code == 403
    finally:
        reset_mapping_service()

def test_owner_acceptance_is_included_in_audit_hash(tmp_path):
    import sqlite3

    from aram_backend.mapping_integrity import audit_chain
    store = MappingStore(tmp_path / "hash-owner.db")
    space, revision = store.load("001", 1405)
    space.propose(MappingDecision("M1", "001", 1405, "100", "BS", "Assets", "1", None, 1, "Draft", None, "Manual"), actor="maker")
    space.owner_accept("M1", actor="owner", reason="Owner accepts the missing independent approval")
    store.save(space, revision)
    expected = audit_chain(store.audit_log("001", 1405))[-1]
    with sqlite3.connect(store.path) as conn:
        actual = conn.execute("SELECT digest FROM mapping_audit_hash ORDER BY sequence DESC LIMIT 1").fetchone()[0]
    assert actual == expected
    assert store.audit_receipt("001", 1405)["sha256"] == expected