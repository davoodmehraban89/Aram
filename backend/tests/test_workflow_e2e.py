import os
import tempfile
import pytest
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    SourceDocument,
    NormalizedFinancialRecord,
    StatementSnapshot,
    WorkflowStatus,
    ReviewStatus,
    AuditLog,
)
from backend.app.services.protection import LockedFiscalYearError
from backend.app.workflow.service import (
    execute_end_to_end_workflow,
    approve_workflow_and_snapshot,
    update_workflow_status,
)


@pytest.fixture
def sample_csv_file():
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "e2e_ledger.csv")
    with open(file_path, "wb") as f:
        f.write(b"account_code,account_name,debit,credit\n1101,Cash,1000.0,0\n3101,Payables,0,1000.0")
    yield file_path


def test_scenario_1_e2e_workflow_execution(db_session, sample_csv_file):
    comp = Company(code="E2E_1", name="E2E Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    raw_rows = [
        {"account_code": "1101", "account_name": "Cash", "debit": "1000.0", "credit": "0"},
        {"account_code": "3101", "account_name": "Payables", "debit": "0", "credit": "1000.0"},
    ]

    fy_res, doc, snap = execute_end_to_end_workflow(
        db_session,
        year_id=fy.id,
        file_path=sample_csv_file,
        doc_type="ledger",
        raw_rows=raw_rows,
        username="e2e_auditor",
    )

    assert fy_res.workflow_status == WorkflowStatus.READY_FOR_REVIEW
    assert doc.id is not None
    assert doc.filename == "e2e_ledger.csv"
    assert snap.version == 1
    assert snap.status == ReviewStatus.DRAFT
    assert snap.snapshot_data["trial_balance"]["is_balanced"] is True


def test_scenario_2_workflow_approval(db_session, sample_csv_file):
    comp = Company(code="E2E_2", name="E2E Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    raw_rows = [
        {"account_code": "1101", "account_name": "Cash", "debit": "500.0", "credit": "0"},
        {"account_code": "3101", "account_name": "Payables", "debit": "0", "credit": "500.0"},
    ]

    fy_res, doc, snap = execute_end_to_end_workflow(
        db_session,
        year_id=fy.id,
        file_path=sample_csv_file,
        doc_type="ledger",
        raw_rows=raw_rows,
    )

    fy_approved, approved_snap = approve_workflow_and_snapshot(
        db_session,
        snapshot_id=snap.id,
        username="auditor_lead",
    )

    assert fy_approved.workflow_status == WorkflowStatus.APPROVED
    assert approved_snap.status == ReviewStatus.APPROVED


def test_scenario_3_source_and_snapshot_immutability(db_session, sample_csv_file):
    comp = Company(code="E2E_3", name="E2E Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    raw_rows = [{"account_code": "1101", "account_name": "Cash", "debit": "200.0", "credit": "0"}]

    fy_res, doc, snap = execute_end_to_end_workflow(
        db_session,
        year_id=fy.id,
        file_path=sample_csv_file,
        doc_type="ledger",
        raw_rows=raw_rows,
    )

    # Verify original file content was not modified
    with open(sample_csv_file, "rb") as f:
        content = f.read()
    assert b"1101,Cash" in content

    # Verify snapshot data frozen
    persisted_snap = db_session.query(StatementSnapshot).filter_by(id=snap.id).first()
    assert persisted_snap.snapshot_data["trial_balance"]["total_debit"] == 200.0


def test_scenario_4_audit_logs_recorded_across_workflow(db_session, sample_csv_file):
    comp = Company(code="E2E_4", name="E2E Corp 4")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    raw_rows = [{"account_code": "1101", "account_name": "Cash", "debit": "100.0", "credit": "0"}]

    execute_end_to_end_workflow(
        db_session,
        year_id=fy.id,
        file_path=sample_csv_file,
        doc_type="ledger",
        raw_rows=raw_rows,
    )

    logs = db_session.query(AuditLog).all()
    assert len(logs) >= 3


def test_scenario_5_locked_year_workflow_rejection(db_session, sample_csv_file):
    comp = Company(code="E2E_5", name="E2E Corp 5")
    db_session.add(comp)
    db_session.commit()

    fy_locked = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.LOCKED)
    db_session.add(fy_locked)
    db_session.commit()

    raw_rows = [{"account_code": "1101", "account_name": "Cash", "debit": "100.0", "credit": "0"}]

    with pytest.raises(LockedFiscalYearError):
        execute_end_to_end_workflow(
            db_session,
            year_id=fy_locked.id,
            file_path=sample_csv_file,
            doc_type="ledger",
            raw_rows=raw_rows,
        )


def test_scenario_6_workflow_status_transitions(db_session):
    comp = Company(code="E2E_6", name="E2E Corp 6")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    assert fy.workflow_status == WorkflowStatus.UPLOADED

    fy_updated = update_workflow_status(db_session, fy.id, WorkflowStatus.NORMALIZED)
    assert fy_updated.workflow_status == WorkflowStatus.NORMALIZED


def test_scenario_7_api_workflow_execute_endpoint(client, db_session, sample_csv_file):
    comp = Company(code="E2E_7", name="E2E Corp 7")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    raw_rows = [{"account_code": "1101", "account_name": "Cash", "debit": "300.0", "credit": "0"}]

    res = client.post(
        f"/api/v1/workflow/execute?year_id={fy.id}&file_path={sample_csv_file}&doc_type=ledger",
        json=raw_rows,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["workflow_status"] == "READY_FOR_REVIEW"
    assert data["snapshot_version"] == 1


def test_scenario_8_api_workflow_approve_endpoint(client, db_session, sample_csv_file):
    comp = Company(code="E2E_8", name="E2E Corp 8")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    raw_rows = [{"account_code": "1101", "account_name": "Cash", "debit": "400.0", "credit": "0"}]

    exec_res = client.post(
        f"/api/v1/workflow/execute?year_id={fy.id}&file_path={sample_csv_file}&doc_type=ledger",
        json=raw_rows,
    )
    snap_id = exec_res.json()["snapshot_id"]

    app_res = client.post(f"/api/v1/workflow/approve?snapshot_id={snap_id}")
    assert app_res.status_code == 200
    assert app_res.json()["workflow_status"] == "APPROVED"
    assert app_res.json()["snapshot_status"] == "APPROVED"


def test_scenario_9_fiscal_year_isolation_in_workflow(db_session, sample_csv_file):
    comp = Company(code="E2E_9", name="E2E Corp 9")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    raw_rows1402 = [{"account_code": "1101", "account_name": "Cash", "debit": "100.0", "credit": "0"}]
    raw_rows1403 = [{"account_code": "1101", "account_name": "Cash", "debit": "800.0", "credit": "0"}]

    _, _, snap1402 = execute_end_to_end_workflow(db_session, fy1402.id, sample_csv_file, "ledger", raw_rows1402)
    _, _, snap1403 = execute_end_to_end_workflow(db_session, fy1403.id, sample_csv_file, "ledger", raw_rows1403)

    assert snap1402.snapshot_data["trial_balance"]["total_debit"] == 100.0
    assert snap1403.snapshot_data["trial_balance"]["total_debit"] == 800.0


def test_scenario_10_existing_accounting_engine_unmodified_results(db_session, sample_csv_file):
    comp = Company(code="E2E_10", name="E2E Corp 10")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    raw_rows = [
        {"account_code": "1101", "account_name": "Cash", "debit": "1000.0", "credit": "0"},
        {"account_code": "7101", "account_name": "COGS", "debit": "400.0", "credit": "0"},
        {"account_code": "6101", "account_name": "Sales", "debit": "1400.0", "credit": "0"},
    ]

    _, _, snap = execute_end_to_end_workflow(db_session, fy.id, sample_csv_file, "ledger", raw_rows)
    tb = snap.snapshot_data["trial_balance"]
    income_stmt = snap.snapshot_data["income_statement"]

    assert tb["total_debit"] == 2800.0
    assert tb["total_credit"] == 0.0
    assert income_stmt["total_cost_of_sales"] == 400.0
