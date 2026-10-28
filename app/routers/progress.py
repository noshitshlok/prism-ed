from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import validate_session_id
from app.schemas.progress import (
    AttemptRecordRequest, AttemptRecordResponse, ProgressSummaryResponse
)
from app.services.progress_service import progress_service

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.post("/attempts", response_model=AttemptRecordResponse)
def record_quiz_attempt(
    body: AttemptRecordRequest,
    session_id: str = Depends(validate_session_id),
    db: Session = Depends(get_session)
):
    return progress_service.record_attempt(session_id, body, db)

@router.get("/summary", response_model=ProgressSummaryResponse)
def get_progress_summary(
    session_id: str = Depends(validate_session_id),
    db: Session = Depends(get_session)
):
    return progress_service.get_summary(session_id, db)
