from datetime import datetime, timezone
from typing import List
from sqlmodel import Session, select
from app.models.progress import SessionModel, QuizAttemptModel, TopicMasteryModel
from app.schemas.progress import (
    AttemptRecordRequest, AttemptRecordResponse, TopicMasteryItem, ProgressSummaryResponse
)

class ProgressService:
    def record_attempt(
        self,
        session_id: str,
        req: AttemptRecordRequest,
        db: Session
    ) -> AttemptRecordResponse:
        now = datetime.now(timezone.utc)

        # 1. Update or create session
        session_obj = db.exec(select(SessionModel).where(SessionModel.id == session_id)).first()
        if not session_obj:
            session_obj = SessionModel(id=session_id, created_at=now, last_seen_at=now)
            db.add(session_obj)
        else:
            session_obj.last_seen_at = now
            db.add(session_obj)

        # 2. Record Quiz Attempt
        percentage = round((req.score / req.total) * 100, 1) if req.total > 0 else 0.0
        attempt = QuizAttemptModel(
            session_id=session_id,
            topic_id=req.topicId,
            score=req.score,
            total=req.total,
            created_at=now
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        # 3. Update Topic Mastery
        mastery = db.exec(
            select(TopicMasteryModel).where(
                TopicMasteryModel.session_id == session_id,
                TopicMasteryModel.topic_id == req.topicId
            )
        ).first()

        if not mastery:
            mastery = TopicMasteryModel(
                session_id=session_id,
                topic_id=req.topicId,
                best_percentage=percentage,
                attempts=1
            )
            db.add(mastery)
        else:
            mastery.attempts += 1
            if percentage > mastery.best_percentage:
                mastery.best_percentage = percentage
            db.add(mastery)

        db.commit()

        return AttemptRecordResponse(
            id=attempt.id or 0,
            sessionId=attempt.session_id,
            topicId=attempt.topic_id,
            score=attempt.score,
            total=attempt.total,
            percentage=percentage,
            createdAt=attempt.created_at.isoformat()
        )

    def get_summary(self, session_id: str, db: Session) -> ProgressSummaryResponse:
        mastery_records = db.exec(
            select(TopicMasteryModel).where(TopicMasteryModel.session_id == session_id)
        ).all()

        total_attempts = sum(m.attempts for m in mastery_records)

        mastery_items = [
            TopicMasteryItem(
                topicId=m.topic_id,
                bestPercentage=m.best_percentage,
                attempts=m.attempts
            )
            for m in mastery_records
        ]

        return ProgressSummaryResponse(
            sessionId=session_id,
            totalAttempts=total_attempts,
            mastery=mastery_items
        )

progress_service = ProgressService()
