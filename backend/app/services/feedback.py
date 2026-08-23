from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from backend.app.models.entities import (
    PilotFeedback,
    PilotValidationLog,
    COAMappingRule,
    FeedbackCategory,
)
from backend.app.services.protection import check_fiscal_year_mutable


def record_pilot_feedback(
    db: Session,
    year_id: int,
    user_id: Optional[int],
    category: FeedbackCategory,
    comments: str,
    account_code: Optional[str] = None,
    original_value: Optional[str] = None,
    corrected_value: Optional[str] = None,
) -> PilotFeedback:
    """Records user feedback, mapping corrections, or processing issues."""
    check_fiscal_year_mutable(db, year_id)

    feedback = PilotFeedback(
        year_id=year_id,
        user_id=user_id,
        category=category,
        account_code=account_code,
        original_value=original_value,
        corrected_value=corrected_value,
        comments=comments,
    )
    db.add(feedback)

    # If feedback is a mapping correction, auto-update or learn into COAMappingRule
    if category == FeedbackCategory.MAPPING_CORRECTION and account_code and corrected_value:
        rule = (
            db.query(COAMappingRule)
            .filter(COAMappingRule.year_id == year_id, COAMappingRule.account_code == account_code)
            .first()
        )
        if rule:
            rule.group_name = corrected_value
            rule.is_approved = True

    db.commit()
    db.refresh(feedback)
    return feedback


def log_pilot_validation_summary(
    db: Session,
    year_id: int,
    uploaded_filename: str,
    file_hash: str,
    record_count: int,
    mapping_decisions: Dict[str, Any],
    user_corrections_count: int = 0,
    processing_result: str = "SUCCESS",
) -> PilotValidationLog:
    """Logs uploaded file information, processing results, mapping decisions, and user corrections count."""
    v_log = PilotValidationLog(
        year_id=year_id,
        uploaded_filename=uploaded_filename,
        file_hash=file_hash,
        record_count=record_count,
        mapping_decisions=mapping_decisions,
        user_corrections_count=user_corrections_count,
        processing_result=processing_result,
    )
    db.add(v_log)
    db.commit()
    db.refresh(v_log)
    return v_log


def get_recurring_unknown_accounts(db: Session, year_id: int) -> List[Dict[str, Any]]:
    """Detects recurring unknown or unmapped accounts across feedback entries for a fiscal year."""
    feedbacks = (
        db.query(PilotFeedback)
        .filter(PilotFeedback.year_id == year_id, PilotFeedback.account_code.isnot(None))
        .all()
    )

    counts: Dict[str, int] = {}
    for f in feedbacks:
        code = f.account_code
        counts[code] = counts.get(code, 0) + 1

    return [{"account_code": code, "feedback_count": count} for code, count in counts.items() if count >= 1]
