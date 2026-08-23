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
from backend.app.services.protection import LockedFiscalYearError
from backend.app.accounting.snapshot import (
    create_statement_snapshot,
    get_snapshots_for_year,
    update_snapshot_review_status,
)


def test_create_statement_snapshot_and_versioning(db_session):
    comp = Company(code="SNAP1", name="Snapshot Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger.csv", file_hash="h1", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    rec = NormalizedFinancialRecord(
        year_id=fy.id,
        source_document_id=doc.id,
        row_index=1,
        account_code="1101",
        account_name="Cash",
        debit=1000.0,
        credit=0.0,
        net_amount=1000.0,
    )
    db_session.add(rec)
    db_session.commit()

    snap1 = create_statement_snapshot(db_session, year_id=fy.id, notes="Initial run", created_by="auditor1")
    assert snap1.id is not None
    assert snap1.version == 1
    assert snap1.status == ReviewStatus.DRAFT
    assert snap1.snapshot_data["trial_balance"]["total_debit"] == 1000.0

    snap2 = create_statement_snapshot(db_session, year_id=fy.id, notes="Second run", created_by="auditor2")
    assert snap2.version == 2


def test_review_status_transitions(db_session):
    comp = Company(code="SNAP2", name="Snapshot Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    snap = create_statement_snapshot(db_session, year_id=fy.id)
    assert snap.status == ReviewStatus.DRAFT

    # Transition to UNDER_REVIEW
    updated = update_snapshot_review_status(db_session, snap.id, ReviewStatus.UNDER_REVIEW, notes="Submitted for review")
    assert updated.status == ReviewStatus.UNDER_REVIEW
    assert "Submitted for review" in updated.notes

    # Transition to APPROVED
    approved = update_snapshot_review_status(db_session, snap.id, ReviewStatus.APPROVED, notes="Looks good")
    assert approved.status == ReviewStatus.APPROVED


def test_snapshots_fiscal_year_isolation(db_session):
    comp = Company(code="SNAP3", name="Snapshot Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    snap1402 = create_statement_snapshot(db_session, year_id=fy1402.id)
    snap1403 = create_statement_snapshot(db_session, year_id=fy1403.id)

    snaps_1402 = get_snapshots_for_year(db_session, fy1402.id)
    snaps_1403 = get_snapshots_for_year(db_session, fy1403.id)

    assert len(snaps_1402) == 1
    assert snaps_1402[0].id == snap1402.id
    assert len(snaps_1403) == 1
    assert snaps_1403[0].id == snap1403.id


def test_immutability_of_normalized_source_records_during_snapshot(db_session):
    comp = Company(code="SNAP4", name="Snapshot Corp 4")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger.csv", file_hash="h4", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    rec = NormalizedFinancialRecord(
        year_id=fy.id,
        source_document_id=doc.id,
        row_index=1,
        account_code="1101",
        account_name="Cash",
        debit=500.0,
        credit=0.0,
        net_amount=500.0,
    )
    db_session.add(rec)
    db_session.commit()

    snap = create_statement_snapshot(db_session, year_id=fy.id)
    persisted_rec = db_session.query(NormalizedFinancialRecord).filter_by(id=rec.id).first()

    assert persisted_rec.debit == 500.0
    assert persisted_rec.account_code == "1101"


def test_locked_fiscal_year_snapshot_creation_protection(db_session):
    comp = Company(code="SNAP5", name="Snapshot Corp 5")
    db_session.add(comp)
    db_session.commit()

    fy_locked = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.LOCKED)
    db_session.add(fy_locked)
    db_session.commit()

    with pytest.raises(LockedFiscalYearError):
        create_statement_snapshot(db_session, year_id=fy_locked.id)


def test_locked_fiscal_year_snapshot_update_protection(db_session):
    comp = Company(code="SNAP6", name="Snapshot Corp 6")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    snap = create_statement_snapshot(db_session, year_id=fy.id)

    # Lock fiscal year
    fy.status = FiscalYearStatus.LOCKED
    db_session.commit()

    with pytest.raises(LockedFiscalYearError):
        update_snapshot_review_status(db_session, snap.id, ReviewStatus.APPROVED)


def test_non_existent_snapshot_update_handling(db_session):
    with pytest.raises(ValueError) as exc_info:
        update_snapshot_review_status(db_session, 99999, ReviewStatus.APPROVED)
    assert "99999" in str(exc_info.value)


def test_snapshot_rejection_workflow(db_session):
    comp = Company(code="SNAP7", name="Snapshot Corp 7")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    snap = create_statement_snapshot(db_session, year_id=fy.id)
    rejected = update_snapshot_review_status(db_session, snap.id, ReviewStatus.REJECTED, notes="Missing disclosures")

    assert rejected.status == ReviewStatus.REJECTED
    assert "Missing disclosures" in rejected.notes


def test_get_snapshots_ordered_by_version(db_session):
    comp = Company(code="SNAP8", name="Snapshot Corp 8")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    snap1 = create_statement_snapshot(db_session, year_id=fy.id)
    snap2 = create_statement_snapshot(db_session, year_id=fy.id)

    snaps = get_snapshots_for_year(db_session, fy.id)
    assert len(snaps) == 2
    assert snaps[0].version == 2
    assert snaps[1].version == 1


def test_snapshot_data_contains_statement_foundations(db_session):
    comp = Company(code="SNAP9", name="Snapshot Corp 9")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    snap = create_statement_snapshot(db_session, year_id=fy.id)
    assert "trial_balance" in snap.snapshot_data
    assert "balance_sheet" in snap.snapshot_data
    assert "income_statement" in snap.snapshot_data
