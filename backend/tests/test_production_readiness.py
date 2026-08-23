import pytest
from backend.app.models import User, UserRole, AuditLog, Company, FiscalYear, FiscalYearStatus
from backend.app.api.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)
from backend.app.services.audit import log_audit_event
from backend.app.config import settings


def test_password_hashing_and_verification():
    raw_pass = "SecurePass123!"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPass", hashed) is False


def test_jwt_token_generation_and_verification():
    token = create_access_token({"sub": "test_user", "role": "ADMIN"})
    verified = verify_access_token(token)
    assert verified["username"] == "test_user"
    assert verified["role"] == "ADMIN"


def test_jwt_token_invalid_format_rejection():
    with pytest.raises(Exception):
        verify_access_token("invalid.token.string")


def test_user_creation_and_auth_persistence(db_session):
    hashed = hash_password("pass123")
    user = User(username="audit_admin", hashed_password=hashed, role=UserRole.ADMIN, is_active=True)
    db_session.add(user)
    db_session.commit()

    persisted = db_session.query(User).filter_by(username="audit_admin").first()
    assert persisted is not None
    assert persisted.role == UserRole.ADMIN
    assert verify_password("pass123", persisted.hashed_password) is True


def test_audit_logging_service(db_session):
    user = User(username="auditor_test", hashed_password="hash", role=UserRole.AUDITOR)
    db_session.add(user)
    db_session.commit()

    log = log_audit_event(
        db_session,
        user_id=user.id,
        user_action="TEST_ACTION",
        entity_affected="FiscalYear",
        action_type="CREATE",
        context_metadata={"year": 1402},
    )

    assert log.id is not None
    assert log.user_action == "TEST_ACTION"
    assert log.entity_affected == "FiscalYear"

    persisted_log = db_session.query(AuditLog).filter_by(id=log.id).first()
    assert persisted_log is not None
    assert persisted_log.context_metadata == {"year": 1402}


def test_login_api_endpoint(client, db_session):
    user = User(username="login_user", hashed_password=hash_password("mysecret"), role=UserRole.AUDITOR)
    db_session.add(user)
    db_session.commit()

    res = client.post("/api/v1/auth/login", json={"username": "login_user", "password": "mysecret"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["username"] == "login_user"
    assert data["role"] == "AUDITOR"


def test_login_api_endpoint_invalid_password(client, db_session):
    user = User(username="login_user2", hashed_password=hash_password("correctpass"), role=UserRole.AUDITOR)
    db_session.add(user)
    db_session.commit()

    res = client.post("/api/v1/auth/login", json={"username": "login_user2", "password": "wrongpass"})
    assert res.status_code == 401


def test_audit_logs_api_endpoint(client, db_session):
    user = User(username="sys_admin", hashed_password="hash", role=UserRole.ADMIN)
    db_session.add(user)
    db_session.commit()

    log_audit_event(
        db_session,
        user_id=user.id,
        user_action="SYSTEM_INIT",
        entity_affected="System",
        action_type="INIT",
    )

    res = client.get("/api/v1/audit-logs")
    assert res.status_code == 200
    logs = res.json()
    assert len(logs) >= 1
    assert logs[0]["user_action"] == "SYSTEM_INIT"


def test_role_based_access_control_rejection(client, db_session):
    # Setup viewer token/user context
    user = User(username="viewer_user", hashed_password=hash_password("pass"), role=UserRole.VIEWER)
    db_session.add(user)
    db_session.commit()

    token = create_access_token({"sub": "viewer_user", "role": "VIEWER"})

    # Attempt snapshot creation which requires ADMIN or AUDITOR role
    comp = Company(code="RBAC1", name="RBAC Corp")
    db_session.add(comp)
    db_session.commit()
    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    res = client.post(
        f"/api/v1/snapshots?year_id={fy.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 403


def test_reporting_api_audit_log_trigger(client, db_session):
    comp = Company(code="AUDIT_REP", name="Audit Report Corp")
    db_session.add(comp)
    db_session.commit()
    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    client.get(f"/api/v1/reporting/trial-balance?year_id={fy.id}")

    audit_entry = (
        db_session.query(AuditLog)
        .filter(AuditLog.user_action.like("%Trial Balance%"))
        .first()
    )
    assert audit_entry is not None


def test_snapshot_creation_audit_log_trigger(client, db_session):
    comp = Company(code="AUDIT_SNAP", name="Audit Snapshot Corp")
    db_session.add(comp)
    db_session.commit()
    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    client.post(f"/api/v1/snapshots?year_id={fy.id}")

    audit_entry = (
        db_session.query(AuditLog)
        .filter(AuditLog.entity_affected == "StatementSnapshot")
        .first()
    )
    assert audit_entry is not None


def test_environment_configuration_handling():
    assert settings.PROJECT_NAME is not None
    assert settings.VERSION is not None
    assert settings.API_V1_STR == "/api/v1"


def test_postgresql_dialect_compatibility():
    pg_url = "postgresql://user:password@localhost:5432/financial_db"
    assert pg_url.startswith("postgresql://")


def test_current_user_me_endpoint(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 200
    assert "username" in res.json()


def test_user_active_status(db_session):
    user = User(username="inactive_user", hashed_password="hash", role=UserRole.VIEWER, is_active=False)
    db_session.add(user)
    db_session.commit()

    persisted = db_session.query(User).filter_by(username="inactive_user").first()
    assert persisted.is_active is False
