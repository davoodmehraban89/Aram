from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.entities import AuditLog


def log_audit_event(
    db: Session,
    user_id: Optional[int],
    user_action: str,
    entity_affected: str,
    action_type: str,
    context_metadata: Optional[Dict[str, Any]] = None,
) -> AuditLog:
    """Logs an audit record for administrative, security, or financial operations."""
    audit_entry = AuditLog(
        user_id=user_id,
        user_action=user_action,
        entity_affected=entity_affected,
        action_type=action_type,
        context_metadata=context_metadata,
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return audit_entry
