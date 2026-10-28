from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class SessionModel(SQLModel, table=True):
    __tablename__ = "sessions"

    id: str = Field(primary_key=True)  # UUID string
    created_at: datetime = Field(default_factory=utc_now)
    last_seen_at: datetime = Field(default_factory=utc_now)

class QuizAttemptModel(SQLModel, table=True):
    __tablename__ = "quiz_attempts"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(index=True)
    topic_id: str = Field(index=True)
    score: int
    total: int
    created_at: datetime = Field(default_factory=utc_now)

class TopicMasteryModel(SQLModel, table=True):
    __tablename__ = "topic_mastery"

    session_id: str = Field(primary_key=True, index=True)
    topic_id: str = Field(primary_key=True, index=True)
    best_percentage: float = Field(default=0.0)
    attempts: int = Field(default=0)

class AICacheModel(SQLModel, table=True):
    __tablename__ = "ai_cache"

    key: str = Field(primary_key=True)
    payload: str  # JSON-serialized cache item
    expires_at: datetime
