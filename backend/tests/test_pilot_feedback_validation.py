import pytest
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    PilotFeedback,
    PilotValidationLog,
    COAMappingRule,
    FeedbackCategory,
    StatementType,
    User,
    UserRole,
)
from backend.app.services.feedback import (
    record_pilot_feedback,
    log_pilot_validation_summary,
    get_recurring_unknown_accounts,
)
from backend.app.services.protection import LockedFiscalYearError


def test_record_pilot_feedback_capture(db_session):
    comp = Company(code="FB_1", name="Feedback Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    user = User(username="accountant1", hashed_password="hash", role=UserRole.AUDITOR)
    db_session.add(user)
    db_session.commit()

    fb = record_pilot_feedback(
        db_session,
        year_id=fy.id,
        user_id=user.id,
        category=FeedbackCategory.USER_SUGGESTION,
        comments="Great UI performance on reports.",
    )

    assert fb.id is not None
    assert fb.category == FeedbackCategory.USER_SUGGESTION
    assert fb.comments == "Great UI performance on reports."


def test_mapping_correction_feedback_auto_learns_mapping_rule(db_session):
    comp = Company(code="FB_2", name="Feedback Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    rule = COAMappingRule(
        year_id=fy.id,
        account_code="110101",
        account_name="Cash",
        target_statement=StatementType.BS,
        statement_section="Current Assets",
        group_name="Old Cash Group",
        is_approved=False,
    )
    db_session.add(rule)
    db_session.commit()

    fb = record_pilot_feedback(
        db_session,
        year_id=fy.id,
        user_id=None,
        category=FeedbackCategory.MAPPING_CORRECTION,
        account_code="110101",
        original_value="Old Cash Group",
        corrected_value="Cash and Cash Equivalents",
        comments="Corrected group classification",
    )

    db_session.refresh(rule)
    assert rule.group_name == "Cash and Cash Equivalents"
    assert rule.is_approved is True


def test_pilot_validation_summary_logging(db_session):
    comp = Company(code="FB_3", name="Feedback Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    v_log = log_pilot_validation_summary(
        db_session,
        year_id=fy.id,
        uploaded_filename="trial_balance_1402.xlsx",
        file_hash="hash_summary_1402",
        record_count=150,
        mapping_decisions={"auto_mapped": 140, "unmapped": 10},
        user_corrections_count=3,
        processing_result="SUCCESS",
    )

    assert v_log.id is not None
    assert v_log.record_count == 150
    assert v_log.user_corrections_count == 3
    assert v_log.mapping_decisions["auto_mapped"] == 140


def test_recurring_unknown_account_detection(db_session):
    comp = Company(code="FB_4", name="Feedback Corp 4")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    record_pilot_feedback(
        db_session,
        year_id=fy.id,
        user_id=None,
        category=FeedbackCategory.PROCESSING_ISSUE,
        account_code="990101",
        comments="Unknown account code",
    )
    record_pilot_feedback(
        db_session,
        year_id=fy.id,
        user_id=None,
        category=FeedbackCategory.MAPPING_CORRECTION,
        account_code="990101",
        comments="Second issue report for 990101",
    )

    recurring = get_recurring_unknown_accounts(db_session, fy.id)
    assert len(recurring) == 1
    assert recurring[0]["account_code"] == "990101"
    assert recurring[0]["feedback_count"] == 2


def test_locked_year_feedback_rejection(db_session):
    comp = Company(code="FB_5", name="Feedback Corp 5")
    db_session.add(comp)
    db_session.commit()

    fy_locked = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.LOCKED)
    db_session.add(fy_locked)
    db_session.commit()

    with pytest.raises(LockedFiscalYearError):
        record_pilot_feedback(
            db_session,
            year_id=fy_locked.id,
            user_id=None,
            category=FeedbackCategory.USER_SUGGESTION,
            comments="Feedback on locked year",
        )


def test_api_submit_pilot_feedback(client, db_session):
    comp = Company(code="API_FB1", name="API Feedback Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    payload = {
        "category": "MAPPING_CORRECTION",
        "account_code": "1101",
        "original_value": "Wrong Group",
        "corrected_value": "Cash Equivalents",
        "comments": "Fixed mapping via UI",
    }

    res = client.post(f"/api/v1/pilot/feedback?year_id={fy.id}", json=payload)
    assert res.status_code == 200
    assert res.json()["account_code"] == "1101"


def test_api_list_pilot_feedback(client, db_session):
    comp = Company(code="API_FB2", name="API Feedback Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    record_pilot_feedback(db_session, fy.id, None, FeedbackCategory.USER_SUGGESTION, "Test comment")

    res = client.get(f"/api/v1/pilot/feedback?year_id={fy.id}")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_api_list_validation_logs(client, db_session):
    comp = Company(code="API_FB3", name="API Feedback Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    log_pilot_validation_summary(
        db_session,
        year_id=fy.id,
        uploaded_filename="test.csv",
        file_hash="hash_test",
        record_count=10,
        mapping_decisions={},
    )

    res = client.get(f"/api/v1/pilot/validation-logs?year_id={fy.id}")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_api_list_recurring_unknowns(client, db_session):
    comp = Company(code="API_FB4", name="API Feedback Corp 4")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    record_pilot_feedback(db_session, fy.id, None, FeedbackCategory.PROCESSING_ISSUE, "Issue", account_code="8801")

    res = client.get(f"/api/v1/pilot/recurring-unknowns?year_id={fy.id}")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["account_code"] == "8801"


def test_processing_issue_feedback_recording(db_session):
    comp = Company(code="FB_PROC", name="Proc Issue Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    fb = record_pilot_feedback(
        db_session,
        year_id=fy.id,
        user_id=None,
        category=FeedbackCategory.PROCESSING_ISSUE,
        comments="Column shift detected on row 12",
    )
    assert fb.category == FeedbackCategory.PROCESSING_ISSUE


def test_feedback_isolation_between_companies(db_session):
    comp1 = Company(code="ISO_FB1", name="Iso FB Corp 1")
    comp2 = Company(code="ISO_FB2", name="Iso FB Corp 2")
    db_session.add_all([comp1, comp2])
    db_session.commit()

    fy1 = FiscalYear(company_id=comp1.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy2 = FiscalYear(company_id=comp2.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1, fy2])
    db_session.commit()

    record_pilot_feedback(db_session, fy1.id, None, FeedbackCategory.USER_SUGGESTION, "Comp1 feedback")

    fb_c2 = db_session.query(PilotFeedback).filter_by(year_id=fy2.id).all()
    assert len(fb_c2) == 0


def test_feedback_isolation_between_fiscal_years(db_session):
    comp = Company(code="ISO_FY_FB", name="Iso FY FB Corp")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    record_pilot_feedback(db_session, fy1402.id, None, FeedbackCategory.USER_SUGGESTION, "1402 feedback")

    fb_1403 = db_session.query(PilotFeedback).filter_by(year_id=fy1403.id).all()
    assert len(fb_1403) == 0


def test_validation_log_persistence_with_corrections(db_session):
    comp = Company(code="VLOG_PERS", name="VLog Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    vlog = log_pilot_validation_summary(
        db_session,
        year_id=fy.id,
        uploaded_filename="ledger_full.csv",
        file_hash="hash_full",
        record_count=500,
        mapping_decisions={"auto": 480, "manual": 20},
        user_corrections_count=5,
        processing_result="COMPLETED_WITH_CORRECTIONS",
    )

    assert vlog.processing_result == "COMPLETED_WITH_CORRECTIONS"
    assert vlog.user_corrections_count == 5


def test_recurring_unknown_empty_when_no_feedbacks(db_session):
    comp = Company(code="EMPTY_UNK", name="Empty Unknown Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    recurring = get_recurring_unknown_accounts(db_session, fy.id)
    assert len(recurring) == 0


def test_feedback_audit_log_integration(client, db_session):
    comp = Company(code="FB_AUDIT", name="FB Audit Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    payload = {"category": "USER_SUGGESTION", "comments": "Audit logging test"}
    client.post(f"/api/v1/pilot/feedback?year_id={fy.id}", json=payload)

    logs = client.get("/api/v1/audit-logs").json()
    assert any("PilotFeedback" in l["entity_affected"] for l in logs)
