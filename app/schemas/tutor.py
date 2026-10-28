from typing import List, Optional
from pydantic import BaseModel, Field

class TutorMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str = Field(..., max_length=1000)

class TutorRequest(BaseModel):
    topicId: str
    question: str = Field(..., min_length=2, max_length=500)
    partId: Optional[str] = None
    history: Optional[List[TutorMessage]] = Field(default=None, max_length=8)

class TutorResponse(BaseModel):
    answer: str
    topicId: str
    partId: Optional[str] = None
    modelUsed: Optional[str] = None
