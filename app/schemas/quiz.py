from typing import List, Dict, Optional
from pydantic import BaseModel, Field, model_validator

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str] = Field(..., min_length=2, max_length=5)
    correctAnswerIndex: int
    engineeringExplanation: Optional[str] = None

    @model_validator(mode="after")
    def check_correct_index(self):
        if not (0 <= self.correctAnswerIndex < len(self.options)):
            raise ValueError(
                f"correctAnswerIndex {self.correctAnswerIndex} is out of bounds for options length {len(self.options)}"
            )
        return self

class QuizQuestionPublic(BaseModel):
    id: str
    question: str
    options: List[str]

class QuizPublic(BaseModel):
    topicId: str
    questions: List[QuizQuestionPublic]

class QuizDetail(BaseModel):
    topicId: str
    questions: List[QuizQuestion]

class QuizSubmitRequest(BaseModel):
    topicId: str
    answers: Dict[str, int]  # questionId -> selectedOptionIndex

class QuizFeedbackItem(BaseModel):
    questionId: str
    question: str
    selectedOptionIndex: Optional[int]
    correctAnswerIndex: int
    isCorrect: bool
    explanation: Optional[str] = None

class QuizSubmitResponse(BaseModel):
    topicId: str
    score: int
    total: int
    percentage: float
    passed: bool
    feedback: List[QuizFeedbackItem]

class QuizGenerateRequest(BaseModel):
    topicId: str
