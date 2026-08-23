from backend.app.models import Company, FiscalYear, FiscalYearStatus, NoteDefinition, FinancialStatement, StatementType


def test_info_endpoint(client):
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json()["message"] == "Financial Reporting Platform API Foundation"


def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "financial-reporting-platform"}


def test_list_companies_endpoint(client, db_session):
    company = Company(code="API_C1", name="API Test Company")
    db_session.add(company)
    db_session.commit()

    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "API_C1"


def test_list_fiscal_years_endpoint(client, db_session):
    company = Company(code="API_C2", name="API Test Company 2")
    db_session.add(company)
    db_session.commit()

    fy = FiscalYear(company_id=company.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    response = client.get(f"/api/v1/fiscal-years?company_id={company.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["year"] == 1403
    assert data[0]["status"] == "Draft"


def test_list_notes_and_statements_endpoints(client, db_session):
    company = Company(code="API_C3", name="API Test Company 3")
    db_session.add(company)
    db_session.commit()

    fy = FiscalYear(company_id=company.id, year=1404, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    note = NoteDefinition(year_id=fy.id, note_number=1, title="General Note")
    stmt = FinancialStatement(year_id=fy.id, statement_type=StatementType.BS)
    db_session.add_all([note, stmt])
    db_session.commit()

    res_notes = client.get(f"/api/v1/notes?year_id={fy.id}")
    assert res_notes.status_code == 200
    assert len(res_notes.json()) == 1
    assert res_notes.json()[0]["title"] == "General Note"

    res_stmts = client.get(f"/api/v1/statements?year_id={fy.id}")
    assert res_stmts.status_code == 200
    assert len(res_stmts.json()) == 1
    assert res_stmts.json()[0]["statement_type"] == "BS"
