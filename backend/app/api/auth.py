from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status


class User(Dict[str, Any]):
    pass


def get_current_user(x_api_key: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Placeholder authentication dependency.
    In development/test mode, allows requests while providing structured user metadata.
    Can be configured in production to enforce API key / OAuth2 JWT verification.
    """
    if x_api_key == "invalid_key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key authentication credentials."
        )

    return {
        "user_id": "auditor_01",
        "username": "auditor_user",
        "role": "AUDITOR",
        "is_authenticated": True,
    }
