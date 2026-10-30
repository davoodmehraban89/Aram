"""Synthetic identity-bound proposal staging; never a finance approval."""
from dataclasses import replace
from time import time

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from aram_backend.authenticated_identity import verify_access_token
from aram_backend.authored_mapping_draft import (
    mapping_draft_authors, SQLITE_AUTHOR_GUARD_DDL,
    stage_authored_unreviewed_batch, get_draft_author,
    check_independent_mapping_reviewer,
)
from aram_backend.config import Settings, get_settings
from aram_backend.database import get_session
from aram_backend.main import app
from aram_backend.mapping_batch_review import ProposedMappingRow, preview_mapping_batch
from aram_backend.mapping_draft_store import mapping_review_drafts, get_unreviewed_batch
from aram_backend.mapping_draft_audit import (
    mapping_draft_events, SQLITE_AUDIT_GUARD_DDL,
)
from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import (
    AccountVersion, Company, FiscalYear, FiscalYearStatus, MappingRule,
    NoteDefinition,
)

ISSUER = "https://synthetic-authorship.example.invalid/"
AUDIENCE = "aram-mapping-api"


@pytest.fixture(scope="module")
def rsa_pair():
    signer = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = signer.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return signer, public


@pytest.fixture
def bound_environment(session, rsa_pair):
    engine = session.get_bind()
    mapping_review_drafts.create(engine)
    mapping_draft_events.create(engine)
    mapping_draft_authors.create(engine)
    with engine.begin() as conn:
        for ddl in (*SQLITE_AUDIT_GUARD_DDL, *SQLITE_AUTHOR_GUARD_DDL):
            conn.exec_driver_sql(ddl)
    company = Company(code="FIN-LEGAL", name="Synthetic reporting company")
    other_company = Company(code="FIN-OTHER", name="Other synthetic")
    year = FiscalYear(company=company, year=1404)
    other_year = FiscalYear(company=other_company, year=1404)
    session.add_all([year, other_year])
    session.flush()
    note = NoteDefinition(year_id=year.id, note_number="1", title="Cash", version=1)
    account = AccountVersion(
        year_id=year.id, account_code="001", account_name="Cash", version=1,
    )
    session.add_all([note, account])
    session.commit()
    config = Settings(auth_issuer=ISSUER, auth_audience=AUDIENCE,
                      auth_public_key_pem=rsa_pair[1])
    app.dependency_overrides[get_settings] = lambda: config

    def isolated_session():
        with Session(engine, expire_on_commit=False) as request_db:
            yield request_db
    app.dependency_overrides[get_session] = isolated_session
    try:
        with TestClient(app) as client:
            yield client, session, year, other_year, note, config
    finally:
        app.dependency_overrides.pop(get_session, None)
        app.dependency_overrides.pop(get_settings, None)
        session.rollback()
        mapping_draft_authors.drop(engine)
        mapping_draft_events.drop(engine)
        mapping_review_drafts.drop(engine)


def signed_token(rsa_pair, *, subject="employee-author-01", role="mapping_proposer",
                 company="FIN-LEGAL", year=1404, include_scope=True):
    now = int(time())
    claims = {
        "iss": ISSUER, "aud": AUDIENCE, "sub": subject,
        "iat": now - 5, "nbf": now - 5, "exp": now + 250,
        "token_use": "access", "aram_roles": [role],
    }
    if include_scope:
        claims["aram_scopes"] = [{
            "company_code": company, "fiscal_year": year, "role": role,
        }]
    return jwt.encode(claims, rsa_pair[0], algorithm="RS256")


def posted_rows(note_id):
    return [{
        "source_locator": "Mapping!2", "rule_key": "cash",
        "account_code": "001", "target_note_id": note_id,
        "mapping_type": "manual", "expected_base_version": 0,
    }]


def stage(client, key, year_id, token, note_id):
    return client.post(
        "/api/v1/mapping/unreviewed-drafts",
        json={
            "year_id": year_id, "request_key": key,
            "rows": posted_rows(note_id),
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def test_signed_proposer_stages_exactly_one_authored_draft_and_system_event(
    bound_environment, rsa_pair,
):
    client, session, year, _, note, _ = bound_environment
    response = stage(client, "author-a1", year.id, signed_token(rsa_pair), note.id)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["draft_id"] > 0
    assert data["year_id"] == year.id
    assert data["state"] == "Unreviewed"
    assert set(data) == {"draft_id", "year_id", "state", "request_key"}
    author = get_draft_author(session, draft_id=data["draft_id"], year_id=year.id)
    assert author.subject == "employee-author-01"
    assert author.issuer == ISSUER
    assert author.company_code == "FIN-LEGAL"
    assert author.fiscal_year == 1404
    assert author.role == "mapping_proposer"
    assert session.execute(select(mapping_draft_authors)).all()
    assert len(session.execute(select(mapping_draft_events)).all()) == 1
    assert len(session.execute(select(mapping_review_drafts)).all()) == 1
    assert session.scalars(select(MappingRule)).all() == []


def test_repeated_request_by_same_author_is_idempotent(bound_environment, rsa_pair):
    client, session, year, _, note, _ = bound_environment
    jwt_token = signed_token(rsa_pair)
    first = stage(client, "author-a2", year.id, jwt_token, note.id)
    second = stage(client, "author-a2", year.id, jwt_token, note.id)
    assert first.status_code == second.status_code == 201
    assert first.json() == second.json()
    assert len(session.execute(select(mapping_draft_authors)).all()) == 1
    assert len(session.execute(select(mapping_draft_events)).all()) == 1


def test_same_idempotency_key_cannot_be_claimed_by_another_author(
    bound_environment, rsa_pair,
):
    client, session, year, _, note, _ = bound_environment
    first = stage(client, "author-a3", year.id, signed_token(rsa_pair), note.id)
    second = stage(client, "author-a3", year.id, signed_token(
        rsa_pair, subject="other-employee",
    ), note.id)
    assert first.status_code == 201
    assert second.status_code == 409
    assert len(session.execute(select(mapping_draft_authors)).all()) == 1
    original = get_draft_author(session, draft_id=first.json()["draft_id"],
                                year_id=year.id)
    assert original.subject == "employee-author-01"


@pytest.mark.parametrize("role,company,include_scope", [
    ("mapping_reviewer", "FIN-LEGAL", True),
    ("mapping_proposer", "FIN-OTHER", True),
    ("mapping_proposer", "FIN-LEGAL", False),
])
def test_signed_role_or_company_scope_is_required(
    bound_environment, rsa_pair, role, company, include_scope,
):
    client, session, year, _, note, _ = bound_environment
    response = stage(client, "auth-denied", year.id, signed_token(
        rsa_pair, role=role, company=company, include_scope=include_scope,
    ), note.id)
    assert response.status_code == 403
    assert session.execute(select(mapping_review_drafts)).all() == []
    assert session.execute(select(mapping_draft_authors)).all() == []


def test_cross_year_and_locked_year_cannot_stage(bound_environment, rsa_pair):
    client, session, year, other_year, note, _ = bound_environment
    token = signed_token(rsa_pair)
    assert stage(client, "wrong-company", other_year.id, token, note.id).status_code == 403
    session.execute(update(FiscalYear).where(FiscalYear.id == year.id).values(
        status=FiscalYearStatus.APPROVED,
    ))
    session.commit()
    assert stage(client, "approved", year.id, token, note.id).status_code == 403
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_missing_bearer_and_forged_author_headers_do_not_stage(
    bound_environment, rsa_pair,
):
    client, session, year, _, note, _ = bound_environment
    payload = {"year_id": year.id, "request_key": "unauth",
               "rows": posted_rows(note.id)}
    assert client.post(
        "/api/v1/mapping/unreviewed-drafts", json=payload,
        headers={"X-User": "director", "X-ARAM-Roles": "mapping_proposer"},
    ).status_code == 401
    wrong_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    signed_wrong = jwt.encode({
        "iss": ISSUER, "aud": AUDIENCE, "sub": "fake-director",
        "iat": int(time()) - 3, "nbf": int(time()) - 3,
        "exp": int(time()) + 100, "token_use": "access",
        "aram_roles": ["mapping_proposer"], "aram_scopes": [{
            "company_code": "FIN-LEGAL", "fiscal_year": 1404,
            "role": "mapping_proposer",
        }],
    }, wrong_key, algorithm="RS256")
    assert stage(client, "wrong-sig", year.id, signed_wrong, note.id).status_code == 401
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_existing_unattributed_draft_cannot_be_retroactively_claimed(
    bound_environment, rsa_pair,
):
    from aram_backend.mapping_draft_store import save_unreviewed_batch
    client, session, year, _, note, _ = bound_environment
    snapshot = preview_mapping_batch(session, year_id=year.id, rows=(
        ProposedMappingRow("Mapping!2", "cash", "001", note.id, "manual", 0),
    ))
    original = save_unreviewed_batch(
        session, snapshot, request_key="legacy-unattributed",
    )
    session.commit()
    assert stage(client, "legacy-unattributed", year.id,
                 signed_token(rsa_pair), note.id).status_code == 409
    assert original.id > 0
    assert session.execute(select(mapping_draft_authors)).all() == []


def test_author_binding_is_insert_only_on_sqlite(bound_environment, rsa_pair):
    client, session, year, _, note, _ = bound_environment
    response = stage(client, "author-lock", year.id, signed_token(rsa_pair), note.id)
    assert response.status_code == 201
    author = get_draft_author(
        session, draft_id=response.json()["draft_id"], year_id=year.id,
    )
    with pytest.raises(IntegrityError):
        session.execute(update(mapping_draft_authors)
                        .values(subject="impersonator"))
    session.rollback()
    with pytest.raises(IntegrityError):
        session.execute(delete(mapping_draft_authors))
    session.rollback()
    assert get_draft_author(
        session, draft_id=response.json()["draft_id"], year_id=year.id,
    ) == author


def test_bound_draft_and_events_atomic_rollback_on_binding_failure(
    bound_environment, rsa_pair, monkeypatch,
):
    import aram_backend.authored_mapping_draft as module
    client, session, year, _, note, _ = bound_environment
    def unavailable(*args, **kwargs):
        raise RuntimeError("synthetic author evidence insert failed")
    monkeypatch.setattr(module, "_insert_author_evidence", unavailable)
    # The route must rollback staging+event when author evidence insert fails.
    with pytest.raises(RuntimeError, match="synthetic author"):
        stage(client, "atomic-rollback", year.id, signed_token(rsa_pair), note.id)
    session.expire_all()
    assert session.execute(select(mapping_review_drafts)).all() == []
    assert session.execute(select(mapping_draft_events)).all() == []


def test_reviewer_separation_is_read_only_and_never_self_approves(
    bound_environment, rsa_pair,
):
    from fastapi import HTTPException
    client, session, year, _, note, config = bound_environment
    response = stage(client, "review-separation", year.id,
                     signed_token(rsa_pair), note.id)
    assert response.status_code == 201
    draft_id = response.json()["draft_id"]
    author_as_reviewer = verify_access_token(signed_token(
        rsa_pair, subject="employee-author-01", role="mapping_reviewer",
    ), settings=config)
    with pytest.raises(HTTPException) as same:
        check_independent_mapping_reviewer(
            session, draft_id=draft_id, year_id=year.id,
            reviewer=author_as_reviewer,
        )
    assert same.value.status_code == 403
    distinct = verify_access_token(signed_token(
        rsa_pair, subject="employee-reviewer-02", role="mapping_reviewer",
    ), settings=config)
    assert check_independent_mapping_reviewer(
        session, draft_id=draft_id, year_id=year.id, reviewer=distinct,
    ) is None
    assert get_unreviewed_batch(session, draft_id=draft_id,
                                year_id=year.id).state == "Unreviewed"
    assert session.scalars(select(MappingRule)).all() == []


def test_reviewer_missing_grant_or_proposer_role_never_passes_preflight(
    bound_environment, rsa_pair,
):
    from fastapi import HTTPException
    client, session, year, _, note, config = bound_environment
    response = stage(client, "review-grants", year.id, signed_token(rsa_pair), note.id)
    assert response.status_code == 201
    draft_id = response.json()["draft_id"]
    for token_value in [
        signed_token(rsa_pair, subject="other", role="mapping_reviewer",
                     include_scope=False),
        signed_token(rsa_pair, subject="other", role="mapping_proposer"),
    ]:
        person = verify_access_token(token_value, settings=config)
        with pytest.raises(HTTPException) as denied:
            check_independent_mapping_reviewer(
                session, draft_id=draft_id, year_id=year.id, reviewer=person,
            )
        assert denied.value.status_code == 403


def test_unconfigured_identity_does_not_create_authored_drafts(
    bound_environment, rsa_pair,
):
    client, session, year, _, note, _ = bound_environment
    app.dependency_overrides[get_settings] = lambda: Settings()
    assert stage(client, "unconfigured", year.id, signed_token(rsa_pair),
                 note.id).status_code == 503
    assert session.execute(select(mapping_review_drafts)).all() == []


def test_proposal_body_cannot_supply_actor_and_bad_rows_never_stage(
    bound_environment, rsa_pair,
):
    client, session, year, _, note, _ = bound_environment
    bearer = signed_token(rsa_pair)
    base = {"year_id": year.id, "request_key": "bad-body",
            "rows": posted_rows(note.id)}
    assert client.post(
        "/api/v1/mapping/unreviewed-drafts",
        json={**base, "author_subject": "fake-director"},
        headers={"Authorization": f"Bearer {bearer}"},
    ).status_code == 422
    assert client.post(
        "/api/v1/mapping/unreviewed-drafts",
        json={**base, "rows": [
            {**posted_rows(note.id)[0], "expected_base_version": True},
        ]},
        headers={"Authorization": f"Bearer {bearer}"},
    ).status_code == 422
    assert session.execute(select(mapping_review_drafts)).all() == []
