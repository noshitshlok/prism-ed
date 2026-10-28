from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.quiz import (
    QuizPublic, QuizSubmitRequest, QuizSubmitResponse, QuizGenerateRequest
)
from app.services.quiz_service import quiz_service

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.get("/{topic_id}", response_model=QuizPublic)
def get_quiz(topic_id: str, request: Request):
    quiz = quiz_service.get_public_quiz(topic_id)
    if not quiz:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Quiz for topic '{topic_id}' not found",
                "requestId": req_id
            }
        )
    return quiz

@router.post("/submit", response_model=QuizSubmitResponse)
def submit_quiz(submission: QuizSubmitRequest, request: Request):
    result = quiz_service.submit_quiz(submission.topicId, submission.answers)
    if not result:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Cannot grade submission: topic '{submission.topicId}' not found",
                "requestId": req_id
            }
        )
    return result

@router.post("/generate", response_model=QuizPublic)
async def generate_quiz(
    body: QuizGenerateRequest,
    request: Request,
    db: Session = Depends(get_session)
):
    try:
        return await quiz_service.generate_ai_quiz(body.topicId, db_session=db)
    except Exception as e:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=503,
            detail={
                "code": "AI_UNAVAILABLE",
                "message": f"Quiz generation unavailable: {str(e)}",
                "requestId": req_id
            }
        )