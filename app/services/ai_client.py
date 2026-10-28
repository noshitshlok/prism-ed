import json
from typing import AsyncGenerator, List, Dict, Any, Optional
from groq import AsyncGroq
from app.core.config import settings
from app.core.logging import logger

class AIClient:
    def __init__(self):
        self._groq_client: Optional[AsyncGroq] = None
        self._gemini_client = None

    def get_groq(self) -> Optional[AsyncGroq]:
        if not self._groq_client and settings.active_groq_key:
            self._groq_client = AsyncGroq(api_key=settings.active_groq_key)
        return self._groq_client

    def get_gemini(self):
        if not self._gemini_client and settings.GEMINI_API_KEY:
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                logger.warning(f"Could not initialize Gemini client: {e}")
        return self._gemini_client

    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 400,
        temperature: float = 0.5,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes completion with Groq as primary and Gemini as fallback.
        Returns dict with {"content": str, "model_used": str, "provider": str}.
        """
        groq_model = model or settings.GROQ_TUTOR_MODEL
        groq_cli = self.get_groq()

        if groq_cli:
            try:
                kwargs: Dict[str, Any] = {
                    "model": groq_model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "timeout": 15.0
                }
                if response_format:
                    kwargs["response_format"] = response_format

                resp = await groq_cli.chat.completions.create(**kwargs)
                content = resp.choices[0].message.content or ""
                logger.info(f"AI response served by Groq model: {groq_model}")
                return {
                    "content": content,
                    "model_used": groq_model,
                    "provider": "groq"
                }
            except Exception as e:
                logger.warning(f"Groq API call failed ({e}); attempting Gemini fallback...")

        # Gemini Fallback
        gemini_cli = self.get_gemini()
        if gemini_cli:
            try:
                # Merge messages into prompt format for Gemini
                prompt_parts = []
                for m in messages:
                    role = m.get("role", "user")
                    content = m.get("content", "")
                    prompt_parts.append(f"{role.upper()}: {content}")
                full_prompt = "\n\n".join(prompt_parts)

                gemini_model = settings.GEMINI_MODEL
                resp = gemini_cli.models.generate_content(
                    model=gemini_model,
                    contents=full_prompt
                )
                answer_text = resp.text or ""
                logger.info(f"AI response served by Gemini fallback: {gemini_model}")
                return {
                    "content": answer_text,
                    "model_used": gemini_model,
                    "provider": "gemini"
                }
            except Exception as e2:
                logger.error(f"Gemini fallback also failed: {e2}")

        # If both fail or no keys provided
        raise RuntimeError("AI services currently unavailable (both Groq and Gemini failed or keys not set)")

    async def stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 400,
        temperature: float = 0.5
    ) -> AsyncGenerator[Dict[str, str], None]:
        """
        Streams completion tokens as an async generator.
        Yields dict with {"token": chunk_str, "model_used": str}.
        """
        groq_model = model or settings.GROQ_TUTOR_MODEL
        groq_cli = self.get_groq()

        if groq_cli:
            try:
                stream_resp = await groq_cli.chat.completions.create(
                    model=groq_model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=True,
                    timeout=20.0
                )
                async for chunk in stream_resp:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield {"token": delta, "model_used": groq_model}
                return
            except Exception as e:
                logger.warning(f"Groq stream call failed ({e}); attempting fallback complete...")

        # Fallback to non-streaming complete if stream fails
        fallback_res = await self.complete(messages, model=model, max_tokens=max_tokens, temperature=temperature)
        yield {"token": fallback_res["content"], "model_used": fallback_res["model_used"]}

ai_client = AIClient()
