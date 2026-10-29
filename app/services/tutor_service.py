import asyncio
from typing import List, Dict, AsyncGenerator, Optional
from app.schemas.tutor import TutorRequest, TutorResponse
from app.services.topic_service import topic_service
from app.services.ai_client import ai_client
from app.core.config import settings
from app.core.logging import logger

# §3.2: One single system instruction for all topics. Lives in one place.
SYSTEM_INSTRUCTION = (
    "You are a tutor for the topic named in the context.\n"
    "Answer any question about this model, its parts, and the subject it teaches.\n"
    "Answer in 2–5 sentences unless the student asks for more.\n"
    "If a part is selected, explain that part first.\n"
    "Give formulas in plain text where they apply.\n"
    "If the question is unrelated to the model or its subject, politely redirect to the model.\n"
    "If unsure, say so rather than guess."
)

class TutorService:
    def _build_context(self, topic_id: str, part_id: Optional[str] = None) -> str:
        """
        §3.1 Topic context (built dynamically from topics.json, not written per topic).
        Builds context containing:
        - name, discipline, subfield (defaults to 'Engineering' if missing), description;
        - each part's name and explanation (omitted if missing);
        - the selected part, if partId is given;
        - equationsCovered, if present.
        Missing fields are left out. A missing field never stops the request.
        """
        topic = topic_service.get_topic_by_id(topic_id)
        if not topic:
            return f"Topic ID: {topic_id}"

        name = topic.name
        discipline = topic.discipline if topic.discipline else "Engineering"
        subfield = topic.subfield if topic.subfield else "Engineering"

        context_blocks = [
            f"Topic: {name}",
            f"Discipline: {discipline}",
            f"Subfield: {subfield}",
        ]

        if topic.description:
            context_blocks.append(f"Description: {topic.description}")

        # Each part's name and explanation (omit if missing)
        if topic.parts:
            part_lines = []
            for p in topic.parts:
                expl = f": {p.explanation}" if getattr(p, "explanation", None) else ""
                part_lines.append(f"- {p.name}{expl}")
            if part_lines:
                context_blocks.append("Model Parts:\n" + "\n".join(part_lines))

        # Selected part, if partId is given
        if part_id:
            part = topic_service.get_part(topic_id, part_id)
            if part:
                sel_block = f"Selected Part: {part.name}"
                if getattr(part, "explanation", None):
                    sel_block += f"\nSelected Part Explanation: {part.explanation}"
                if getattr(part, "formulaOrLaw", None):
                    sel_block += f"\nSelected Part Formula / Law: {part.formulaOrLaw}"
                context_blocks.append(sel_block)
            else:
                context_blocks.append(f"Selected Part ID: {part_id}")

        # equationsCovered, if present
        if topic.equationsCovered:
            eqs = ", ".join(topic.equationsCovered)
            context_blocks.append(f"Equations Covered: {eqs}")

        return "\n\n".join(context_blocks)

    def _build_messages(self, req: TutorRequest) -> List[Dict[str, str]]:
        context = self._build_context(req.topicId, req.partId)
        full_system_prompt = f"{SYSTEM_INSTRUCTION}\n\n=== TOPIC CONTEXT ===\n{context}"

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": full_system_prompt}
        ]

        # Optional conversation history (last 8 messages kept)
        if req.history:
            for msg in req.history[-8:]:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": req.question})
        return messages

    async def ask(self, req: TutorRequest) -> TutorResponse:
        messages = self._build_messages(req)
        # Provider calls (§3.4): Primary Groq, fallback Gemini with 20s timeout
        res = await ai_client.complete(
            messages=messages,
            model=settings.GROQ_TUTOR_MODEL,
            max_tokens=350,
            temperature=0.5
        )
        return TutorResponse(
            answer=res["content"],
            topicId=req.topicId,
            partId=req.partId,
            modelUsed=res.get("model_used")
        )

    async def stream(self, req: TutorRequest) -> AsyncGenerator[str, None]:
        messages = self._build_messages(req)
        async for chunk in ai_client.stream(
            messages=messages,
            model=settings.GROQ_TUTOR_MODEL,
            max_tokens=350,
            temperature=0.5
        ):
            yield chunk["token"]

tutor_service = TutorService()
