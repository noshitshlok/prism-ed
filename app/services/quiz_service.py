import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Any
from sqlmodel import Session, select
from app.schemas.quiz import (
    QuizQuestion, QuizQuestionPublic, QuizPublic, QuizDetail,
    QuizSubmitResponse, QuizFeedbackItem
)
from app.models.progress import AICacheModel
from app.services.topic_service import topic_service
from app.services.ai_client import ai_client
from app.core.config import settings
from app.core.logging import logger

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "quiz.json"

class QuizService:
    def __init__(self):
        self._quiz_cache: Optional[Dict[str, QuizDetail]] = None
        self._load_quizzes()

    def _load_quizzes(self):
        if not DATA_FILE.exists():
            self._quiz_cache = {}
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            quizzes = data.get("quizzes", {})
            self._quiz_cache = {
                t_id: QuizDetail(**q_data) for t_id, q_data in quizzes.items()
            }

    def get_public_quiz(self, topic_id: str) -> Optional[QuizPublic]:
        if self._quiz_cache is None:
            self._load_quizzes()

        quiz_detail = self._quiz_cache.get(topic_id)
        if not quiz_detail:
            return None

        # Mask answers and explanations
        public_questions = [
            QuizQuestionPublic(
                id=q.id,
                question=q.question,
                options=q.options
            )
            for q in quiz_detail.questions
        ]
        return QuizPublic(topicId=topic_id, questions=public_questions)

    def submit_quiz(self, topic_id: str, answers: Dict[str, int]) -> Optional[QuizSubmitResponse]:
        if self._quiz_cache is None:
            self._load_quizzes()

        quiz_detail = self._quiz_cache.get(topic_id)
        if not quiz_detail:
            return None

        total = len(quiz_detail.questions)
        score = 0
        feedback_list: List[QuizFeedbackItem] = []

        for q in quiz_detail.questions:
            selected_idx = answers.get(q.id)
            is_correct = (selected_idx is not None and selected_idx == q.correctAnswerIndex)
            if is_correct:
                score += 1

            feedback_list.append(QuizFeedbackItem(
                questionId=q.id,
                question=q.question,
                selectedOptionIndex=selected_idx,
                correctAnswerIndex=q.correctAnswerIndex,
                isCorrect=is_correct,
                explanation=q.engineeringExplanation
            ))

        percentage = round((score / total) * 100, 1) if total > 0 else 0.0
        passed = percentage >= 60.0

        return QuizSubmitResponse(
            topicId=topic_id,
            score=score,
            total=total,
            percentage=percentage,
            passed=passed,
            feedback=feedback_list
        )

    async def generate_ai_quiz(self, topic_id: str, db_session: Optional[Session] = None) -> QuizPublic:
        """
        Generates 3 new quiz questions using Groq / Gemini with 7-day caching.
        Falls back to static quiz if validation or generation fails.
        """
        cache_key = f"quiz_gen:{topic_id}"
        now = datetime.now(timezone.utc)

        # 1. Check AI Cache in Database
        if db_session:
            try:
                cached = db_session.exec(
                    select(AICacheModel).where(
                        AICacheModel.key == cache_key,
                        AICacheModel.expires_at > now
                    )
                ).first()
                if cached:
                    cached_data = json.loads(cached.payload)
                    return QuizPublic(**cached_data)
            except Exception as e:
                logger.warning(f"AI cache read error: {e}")

        # 2. Topic lookup for grounding
        topic = topic_service.get_topic_by_id(topic_id)
        if not topic:
            # Fallback to static or error
            static = self.get_public_quiz(topic_id)
            if static:
                return static
            raise ValueError(f"Topic {topic_id} not found")

        # 3. Construct AI generation prompt
        parts_summary = "; ".join([f"{p.name}: {p.explanation[:80]}" for p in topic.parts[:5]])
        equations = ", ".join(topic.equationsCovered) if topic.equationsCovered else "Standard domain principles"

        prompt = (
            f"You are a rigorous engineering examination generator for PrismEd.\n"
            f"Generate 3 challenging multiple-choice questions for the undergraduate topic: '{topic.name}'.\n"
            f"Discipline: {topic.discipline}. Key equations: {equations}.\n"
            f"Parts covered: {parts_summary}.\n\n"
            "Respond strictly with a JSON object in this format:\n"
            "{\n"
            '  "questions": [\n'
            "    {\n"
            '      "id": "gen-q1",\n'
            '      "question": "Question text",\n'
            '      "options": ["Option A", "Option B", "Option C", "Option D"],\n'
            '      "correctAnswerIndex": 0,\n'
            '      "engineeringExplanation": "Detailed explanation of correct answer"\n'
            "    }\n"
            "  ]\n"
            "}\n"
        )

        messages = [
            {"role": "system", "content": "You are a professional engineering assessment developer. You only output valid JSON."},
            {"role": "user", "content": prompt}
        ]

        # 4. Attempt generation with 1 retry
        for attempt in range(2):
            try:
                ai_resp = await ai_client.complete(
                    messages=messages,
                    model=settings.GROQ_QUIZ_MODEL,
                    max_tokens=800,
                    temperature=0.4,
                    response_format={"type": "json_object"}
                )
                raw_json = json.loads(ai_resp["content"])
                questions_raw = raw_json.get("questions", [])

                validated_questions: List[QuizQuestion] = []
                for q_data in questions_raw:
                    q_obj = QuizQuestion(**q_data)
                    if len(q_obj.options) != 4:
                        raise ValueError("Must have exactly 4 options")
                    validated_questions.append(q_obj)

                if len(validated_questions) >= 3:
                    # Save to internal detail cache so submission can grade it
                    dynamic_detail = QuizDetail(topicId=topic_id, questions=validated_questions[:3])
                    if self._quiz_cache is not None:
                        self._quiz_cache[topic_id] = dynamic_detail

                    public_res = QuizPublic(
                        topicId=topic_id,
                        questions=[
                            QuizQuestionPublic(id=q.id, question=q.question, options=q.options)
                            for q in dynamic_detail.questions
                        ]
                    )

                    # Save to DB cache with 7 days expiration
                    if db_session:
                        try:
                            expires = now + timedelta(days=7)
                            cache_record = AICacheModel(
                                key=cache_key,
                                payload=public_res.model_dump_json(),
                                expires_at=expires
                            )
                            db_session.merge(cache_record)
                            db_session.commit()
                        except Exception as e_cache:
                            logger.warning(f"Failed to write AI cache: {e_cache}")

                    return public_res
            except Exception as e:
                logger.warning(f"AI quiz generation attempt {attempt + 1} failed: {e}")

        # Fallback to static quiz
        logger.info(f"Falling back to static quiz for topic '{topic_id}'")
        static_quiz = self.get_public_quiz(topic_id)
        if static_quiz:
            return static_quiz
        raise RuntimeError("Failed to generate AI quiz and no static quiz found")

quiz_service = QuizService()