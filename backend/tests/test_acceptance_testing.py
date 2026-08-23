import pytest
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    WorkflowStatus,
    ReviewStatus,
    SourceDocument,
    NormalizedFinancialRecord,
    StatementSnapshot,
)
from backend.app.workflow.service import execute_end_to_end_workflow, approve_workflow_and_snapshot


def test_acceptance_scenario_complete_user_journey(client, db_session, tmp_path):
    # 1. Create Company
    company = Company(code="ACCEPT_01", name="Acceptance Corp PLC")
    db_session.add(company)
    db_session.commit()
    assert company.id is not None

    # 2. Create Fiscal Year
    fy = FiscalYear(company_id=company.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()
    assert fy.id is not None
    assert fy.workflow_status == WorkflowStatus.UPLOADED

    # 3. Create raw financial source file
    source_file = tmp_path / "financial_ledger_1403.csv"
    source_file.write_text("account_code,account_name,debit,credit\n1101,Cash in Hand,2500000.00,0\n3101,Trade Payables,0,2500000.00")

    raw_rows = [
        {"account_code": "1101", "account_name": "Cash in Hand", "debit": "2500000.00", "credit": "0"},
        {"account_code": "3101", "account_name": "Trade Payables", "debit": "0", "credit": "2500000.00"},
    ]

    # 4. Execute E2E workflow via API (Ingest -> Normalize -> Calculate -> Snapshot)
    exec_res = client.post(
        f"/api/v1/workflow/execute?year_id={fy.id}&file_path={str(source_file)}&doc_type=ledger",
        json=raw_rows,
    )
    assert exec_res.status_code == 200
    exec_data = exec_res.json()
    assert exec_data["workflow_status"] == "READY_FOR_REVIEW"
    snap_id = exec_data["snapshot_id"]

    # 5. Query Trial Balance report via API
    tb_res = client.get(f"/api/v1/reporting/trial-balance?year_id={fy.id}")
    assert tb_res.status_code == 200
    tb_data = tb_res.json()
    assert tb_data["total_debit"] == 2500000.00
    assert tb_data["is_balanced"] is True

    # 6. Query Balance Sheet report via API
    bs_res = client.get(f"/api/v1/reporting/balance-sheet?year_id={fy.id}")
    assert bs_res.status_code == 200
    bs_data = bs_res.json()
    assert bs_data["total_assets"] == 2500000.00

    # 7. Approve Review Snapshot & Workflow
    app_res = client.post(f"/api/v1/workflow/approve?snapshot_id={snap_id}")
    assert app_res.status_code == 200
    assert app_res.json()["workflow_status"] == "APPROVED"
    assert app_res.json()["snapshot_status"] == "APPROVED"

    # 8. Export CSV Report
    csv_res = client.get(f"/api/v1/export/csv?year_id={fy.id}&statement_type=TB")
    assert csv_res.status_code == 200
    assert "2500000" in csv_res.text

    # 9. Export PDF Structure
    pdf_res = client.get(f"/api/v1/export/pdf-structure?year_id={fy.id}&statement_type=TB")
    assert pdf_res.status_code == 200
    assert pdf_res.json()["formatted_totals"]["total_debit"] == "2,500,000.00"
