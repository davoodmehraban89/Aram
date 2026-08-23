import pytest
from backend.app.models import Company, FiscalYear, FiscalYearStatus, User, UserRole
from backend.app.api.auth import hash_password, create_access_token


def test_desktop_login_flow_integration(client, db_session):
    user = User(username="pilot_accountant", hashed_password=hash_password("pilot_pass"), role=UserRole.AUDITOR)
    db_session.add(user)
    db_session.commit()

    res = client.post("/api/v1/auth/login", json={"username": "pilot_accountant", "password": "pilot_pass"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["role"] == "AUDITOR"


def test_desktop_upload_workflow_initiation(client, db_session, tmp_path):
    comp = Company(code="DESK_01", name="Desktop Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    file_path = tmp_path / "ledger.csv"
    file_path.write_text("account_code,account_name,debit,credit\n1101,Cash,1000,0")

    raw_rows = [{"account_code": "1101", "account_name": "Cash", "debit": "1000", "credit": "0"}]

    res = client.post(
        f"/api/v1/workflow/execute?year_id={fy.id}&file_path={str(file_path)}&doc_type=ledger",
        json=raw_rows,
    )
    assert res.status_code == 200
    assert res.json()["workflow_status"] == "READY_FOR_REVIEW"


def test_desktop_report_retrieval(client, db_session):
    comp = Company(code="DESK_02", name="Desktop Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    res = client.get(f"/api/v1/reporting/trial-balance?year_id={fy.id}")
    assert res.status_code == 200
    assert res.json()["statement_type"] == "TB"


def test_desktop_role_permission_restrictions(client, db_session):
    user = User(username="viewer_user", hashed_password=hash_password("pass"), role=UserRole.VIEWER)
    db_session.add(user)
    db_session.commit()

    viewer_token = create_access_token({"sub": "viewer_user", "role": "VIEWER"})

    comp = Company(code="DESK_03", name="Desktop Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    res = client.post(
        f"/api/v1/snapshots?year_id={fy.id}",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert res.status_code == 403
