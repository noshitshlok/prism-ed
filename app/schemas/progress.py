from typing import List
from pydantic import BaseModel

class AttemptRecordRequest(BaseModel):
    topicId: str
    score: int
    total: int

class AttemptRecordResponse(BaseModel):
    id: int
    sessionId: str
    topicId: str
    score: int
    total: int
    percentage: float
    createdAt: str

class TopicMasteryItem(BaseModel):
    topicId: str
    bestPercentage: float
    attempts: int

class ProgressSummaryResponse(BaseModel):
    sessionId: str
    totalAttempts: int
    mastery: List[TopicMasteryItem]
