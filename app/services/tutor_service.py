import asyncio
from typing import List, Dict, AsyncGenerator, Optional
from app.schemas.tutor import TutorRequest, TutorResponse
from app.services.topic_service import topic_service
from app.services.ai_client import ai_client
from app.core.config import settings
from app.core.logging import logger

class TutorService:
    def _build_messages(self, req: TutorRequest) -> List[Dict[str, str]]:
        topic = topic_service.get_topic_by_id(req.topicId)
        topic_name = topic.name if topic else req.topicId
        discipline = topic.discipline if topic else "Engineering"
        desc = topic.description if topic else ""

        if req.partId:
            part = topic_service.get_part(req.topicId, req.partId)
            part_name = part.name if part else req.partId
            explanation = part.explanation if part else "Component of the 3D model"
            formula = part.formulaOrLaw if (part and part.formulaOrLaw) else "Relevant physical and engineering laws"

            system_prompt = (
                f"You are the PrismEd AI Engineering Tutor for '{topic_name}' ({discipline}).\n"
                f"The student is examining the 3D component: '{part_name}'.\n"
                f"Explanation the student already read: \"{explanation}\"\n"
                f"Key formula / principle: \"{formula}\"\n\n"
                "Pedagogical Rules:\n"
                "1. Answer in exactly 2 to 4 concise, clear sentences.\n"
                "2. Ground the answer directly in this component and engineering discipline.\n"
                "3. Build on the explanation they have already read.\n"
                "4. State a relevant formula in plain text where one exists.\n"
                "5. If the question is completely off-topic or unrelated to this model/component, politely redirect them back to the 3D model."
            )
        else:
            # Topic-level question (no part selected)
            parts_summary = ""
            if topic and topic.parts:
                parts_summary = ", ".join(f"{p.name}: {p.explanation}" for p in topic.parts)

            system_prompt = (
                f"You are the PrismEd AI Engineering Tutor for '{topic_name}' ({discipline}).\n"
                f"The student is examining the whole 3D model (no single part is selected).\n"
                f"Model Overview: \"{desc}\"\n"
                f"Components in this model: {parts_summary}\n\n"
                "Pedagogical Rules:\n"
                "1. Answer in exactly 2 to 4 concise, clear sentences.\n"
                "2. Ground the answer directly in this engineering model and its components.\n"
                "3. Answer any question related to the topic, guiding the student to relevant components where appropriate.\n"
                "4. If the question is completely off-topic (e.g. general chit-chat, weather, movies), politely redirect them back to this 3D engineering model."
            )

        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

        # Append conversation history if provided (up to 8 messages)
        if req.history:
            for msg in req.history[-8:]:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": req.question})
        return messages

    def _generate_grounded_fallback(self, req: TutorRequest) -> str:
        """
        High-fidelity grounded pedagogical fallback synthesized from verified curriculum
        data in topics.json when external AI APIs are unreachable or offline.
        """
        topic = topic_service.get_topic_by_id(req.topicId)
        topic_name = topic.name if topic else req.topicId
        discipline = topic.discipline if topic else "Engineering"
        desc = topic.description if topic else ""
        q_lower = req.question.lower()

        # Handle unrelated questions gracefully (§4.2)
        unrelated_keywords = ["weather", "movie", "song", "who are you", "joke", "recipe", "president"]
        if any(w in q_lower for w in unrelated_keywords) and not any(k in q_lower for k in [topic_name.lower(), "model", "engineering", "part"]):
            return (
                f"I am the PrismEd engineering tutor for {topic_name}. "
                f"I can only answer questions related to this 3D specimen and its physical components. "
                f"Please ask about the mechanisms, principles, or formulas of this model."
            )

        # Part-level question fallback
        if req.partId:
            part = topic_service.get_part(req.topicId, req.partId)
            part_name = part.name if part else req.partId
            explanation = part.explanation if part else ""
            formula = part.formulaOrLaw if (part and part.formulaOrLaw) else ""

            if any(w in q_lower for w in ["formula", "equation", "law", "calculate", "math"]):
                if formula:
                    return (
                        f"In {topic_name}, the operation of {part_name} is governed by the principle: {formula}. "
                        f"This mathematical relationship dictates how energy and physical states transform across this component. "
                        f"As you can see in the 3D model, its geometric arrangement is calibrated specifically to satisfy these design parameters."
                    )
                else:
                    return (
                        f"For {part_name} within {topic_name}, the operational dynamics relate directly to: {explanation}. "
                        f"Its physical behavior maintains the operational tolerances of the overall system."
                    )

            if any(w in q_lower for w in ["why", "purpose", "reason", "need"]):
                return (
                    f"{part_name} is essential in {topic_name} because {explanation.lower().rstrip('.')}."
                    + (f" Its behavior is governed by {formula}." if formula else "")
                    + f" Without this component properly positioned in the assembly, the system cannot function reliably under working loads."
                )

            if any(w in q_lower for w in ["how", "work", "function", "operate"]):
                return (
                    f"{part_name} operates within {topic_name} by {explanation.lower().rstrip('.')}."
                    + (f" Mechanically and physically, this relates to {formula}." if formula else "")
                    + f" In the 3D viewer, notice how its connections interface with adjacent parts to maintain system equilibrium."
                )

            # General part grounded tutor answer
            base = f"Regarding {part_name} in {topic_name}: {explanation}."
            if formula:
                base += f" The key physical principle governing this is {formula}."
            base += f" This component is engineered specifically to ensure optimal performance within the overall assembly."
            return base

        # Topic-level question fallback (no partId)
        parts_list = [p.name for p in topic.parts] if (topic and topic.parts) else []
        parts_str = ", ".join(parts_list[:4])

        if any(w in q_lower for w in ["what does this", "what is this", "overview", "summary", "explain this"]):
            return (
                f"{topic_name} is an engineering assembly in {discipline}. "
                f"{desc} "
                f"It comprises key functional components including {parts_str}. "
                f"You can select any component pin on the 3D model to inspect its detailed mechanical role and governing formulas."
            )

        if any(w in q_lower for w in ["parts", "components", "list"]):
            return (
                f"This specimen of {topic_name} includes {len(parts_list)} calibrated engineering components: {', '.join(parts_list)}. "
                f"Click any numbered marker on the 3D specimen to isolate that part and ask specific technical questions."
            )

        return (
            f"Regarding the {topic_name} model: {desc} "
            f"It functions through the coordinated action of components such as {parts_str}. "
            f"Select any numbered part on the 3D model to investigate its specific engineering equations."
        )

    async def ask(self, req: TutorRequest) -> TutorResponse:
        messages = self._build_messages(req)
        try:
            res = await ai_client.complete(
                messages=messages,
                model=settings.GROQ_TUTOR_MODEL,
                max_tokens=300,
                temperature=0.5
            )
            return TutorResponse(
                answer=res["content"],
                topicId=req.topicId,
                partId=req.partId,
                modelUsed=res.get("model_used")
            )
        except Exception as e:
            logger.warning(f"External AI completion failed ({e}); serving grounded curriculum tutor answer.")
            fallback_ans = self._generate_grounded_fallback(req)
            return TutorResponse(
                answer=fallback_ans,
                topicId=req.topicId,
                partId=req.partId,
                modelUsed="grounded-curriculum-tutor"
            )

    async def stream(self, req: TutorRequest) -> AsyncGenerator[str, None]:
        messages = self._build_messages(req)
        try:
            async for chunk in ai_client.stream(
                messages=messages,
                model=settings.GROQ_TUTOR_MODEL,
                max_tokens=300,
                temperature=0.5
            ):
                yield chunk["token"]
        except Exception as e:
            logger.warning(f"External AI streaming failed ({e}); streaming grounded curriculum tutor answer.")
            fallback_ans = self._generate_grounded_fallback(req)
            words = fallback_ans.split(" ")
            for idx, word in enumerate(words):
                prefix = " " if idx > 0 else ""
                yield prefix + word
                await asyncio.sleep(0.015)

tutor_service = TutorService()
