import pytest
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    SourceDocument,
    NormalizedFinancialRecord,
    StatementSnapshot,
    ReviewStatus,
)


def test_api_trial_balance_report(client, db_session):
    comp = Company(code="API1", name="API Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger.csv", file_hash="hash_api1", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    rec = NormalizedFinancialRecord(
        year_id=fy.id,
        source_document_id=doc.id,
        row_index=1,
        account_code="1101",
        account_name="Cash",
        debit=1500.0,
        credit=0.0,
        net_amount=1500.0,
    )
    db_session.add(rec)
    db_session.commit()

    response = client.get(f"/api/v1/reporting/trial-balance?year_id={fy.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["statement_type"] == "TB"
    assert data["total_debit"] == 1500.0


def test_api_balance_sheet_report(client, db_session):
    comp = Company(code="API2", name="API Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    response = client.get(f"/api/v1/reporting/balance-sheet?year_id={fy.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["statement_type"] == "BS"


def test_api_income_statement_report(client, db_session):
    comp = Company(code="API3", name="API Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    response = client.get(f"/api/v1/reporting/income-statement?year_id={fy.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["statement_type"] == "IS"


def test_api_create_and_get_snapshot(client, db_session):
    comp = Company(code="API4", name="API Corp 4")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    # Create snapshot via POST
    post_res = client.post(f"/api/v1/snapshots?year_id={fy.id}&notes=API+snapshot")
    assert post_res.status_code == 200
    snap_data = post_res.json()
    assert snap_data["version"] == 1
    assert snap_data["status"] == "DRAFT"

    # List snapshots
    list_res = client.get(f"/api/v1/snapshots?year_id={fy.id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # Get snapshot by ID
    get_res = client.get(f"/api/v1/snapshots/{snap_data['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == snap_data["id"]


def test_api_update_snapshot_review_status(client, db_session):
    comp = Company(code="API5", name="API Corp 5")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    post_res = client.post(f"/api/v1/snapshots?year_id={fy.id}")
    snap_id = post_res.json()["id"]

    patch_res = client.patch(f"/api/v1/snapshots/{snap_id}/status?new_status=APPROVED&notes=Review+approved")
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "APPROVED"


def test_api_read_only_access_to_approved_snapshot(client, db_session):
    comp = Company(code="API6", name="API Corp 6")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    post_res = client.post(f"/api/v1/snapshots?year_id={fy.id}")
    snap_id = post_res.json()["id"]
    client.patch(f"/api/v1/snapshots/{snap_id}/status?new_status=APPROVED")

    # Read-only GET access remains fully functional
    get_res = client.get(f"/api/v1/snapshots/{snap_id}")
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "APPROVED"


def test_api_snapshot_not_found_handling(client):
    response = client.get("/api/v1/snapshots/99999")
    assert response.status_code == 404


def test_api_authentication_placeholder_rejection(client):
    response = client.get("/api/v1/reporting/trial-balance?year_id=1", headers={"x-api-key": "invalid_key"})
    assert response.status_code == 401


def test_api_fiscal_year_isolation_across_endpoints(client, db_session):
    comp = Company(code="API7", name="API Corp 7")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    client.post(f"/api/v1/snapshots?year_id={fy1402.id}")

    res_1402 = client.get(f"/api/v1/snapshots?year_id={fy1402.id}")
    res_1403 = client.get(f"/api/v1/snapshots?year_id={fy1403.id}")

    assert len(res_1402.json()) == 1
    assert len(res_1403.json()) == 0
