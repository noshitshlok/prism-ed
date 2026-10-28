import uuid
from typing import Optional
from fastapi import Request, HTTPException, Header
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

def get_session_or_ip_key(request: Request) -> str:
    session_id = request.headers.get("X-Session-Id")
    if session_id:
        return f"session:{session_id}"
    return f"ip:{get_remote_address(request)}"

limiter = Limiter(
    key_func=get_session_or_ip_key,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"]
)

def validate_session_id(x_session_id: Optional[str] = Header(None, alias="X-Session-Id")) -> str:
    if not x_session_id:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Missing required header: X-Session-Id"
            }
        )
    try:
        # Validate that it is a valid UUID format
        val = uuid.UUID(x_session_id)
        return str(val)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Malformed X-Session-Id. Must be a valid UUID string"
            }
        )
