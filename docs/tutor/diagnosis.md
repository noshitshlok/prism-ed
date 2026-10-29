# PrismEd Ask Tutor — Diagnosis Report (§2)

**Specification:** `PRISMED_FINAL_TUTOR_PROMPT.md` (§2)  
**Date:** 2026-10-29  
**Target:** Ask Tutor Component & AI Backend Integration  

---

## 1. Reproduction and Findings

### Reproduction Steps:
1. Start backend (`python -m uvicorn app.main:app --port 8000`) and frontend (`npm run dev`).
2. Open `circuit-board` at `http://localhost:5173/topics/circuit-board`.
3. Select part (`capacitors`), type "What does this part do?", and click **Ask**.
4. Observed:
   - Browser request: `POST /api/v1/tutor/ask` with JSON `{ "topicId": "circuit-board", "partId": "capacitors", "question": "..." }`.
   - Result: LLM generated grounded pedagogical response in 2-4 sentences.

---

## 2. Investigation Matrix (D1–D7)

| # | Cause | How Checked | Result | Finding & Fix |
|---|---|---|---|---|
| **D1** | **Route mismatch** | Compared `src/api/tutor.js` (`POST /api/v1/tutor/ask`) with routes in `app/routers/tutor.py` | **Matched / Aliased** | Target route `POST /api/v1/tutor/ask` is primary. Maintained `POST /tutor` and `POST /tutor/ask` as backward-compatibility aliases in `app/routers/tutor.py` and `app/main.py`. |
| **D2** | **Key name mismatch** | Listed env var names in `app/.env` without logging values | **Verified** | `GROQ_API_KEY` is present and formatted with standard `gsk_` prefix from groq.com. `GEMINI_API_KEY` is present. Code in `app/core/config.py` explicitly reads `GROQ_API_KEY`. |
| **D3** | **Provider rejects request** | Inspected API provider calls and error traces for retired models | **Confirmed & Fixed** | Legacy Groq model `llama-3.3-70b-versatile` returned `404 model_not_found`. Updated `GROQ_TUTOR_MODEL` in config and `app/.env` to `qwen/qwen3.8-27b`. Legacy Gemini model `gemini-1.5-flash` returned `404 NOT_FOUND`; updated `GEMINI_MODEL` in config and `app/.env` to `gemini-3.5-flash`. Both models verified live with 200 OK. |
| **D4** | **Selected part cleared on Ask or Enter** | Inspected click and form handlers in `TutorBox.jsx` and `TopicPage.jsx` | **Confirmed & Fixed** | Form submission now explicitly executes `e.preventDefault()` and `e.stopPropagation()`. In `MarginNotes.jsx` and `TopicPage.jsx`, `selectedPartId` state is maintained without unmounting or resetting during Ask or Enter. |
| **D5** | **Request missing fields** | Inspected `TutorRequest` schema in `app/schemas/tutor.py` | **Confirmed & Fixed** | Schema previously required `partId: str`, rejecting model-level questions without a selected part (`422 Unprocessable Entity`). Fixed by declaring `partId: Optional[str] = None`. |
| **D6** | **Response field mismatch** | Compared backend response with frontend expectations | **Confirmed & Fixed** | Backend response schema standardized to `{ "answer": str, "topicId": str, "partId": Optional[str], "modelUsed": Optional[str] }`. `src/api/tutor.js` extracts `res.data.answer` and `TutorBox.jsx` updates `answer` state. |
| **D7** | **Unhandled exception returns raw 500** | Simulated LLM provider failure and timeout | **Confirmed & Fixed** | In `app/routers/tutor.py`, provider exceptions are caught and returned as HTTP 503: `{ "error": { "code": "AI_UNAVAILABLE", "message": "The tutor is unavailable right now.", "requestId": "..." } }`. No raw 500s, no silent failures, and no internal tracebacks or API keys are leaked. |

---

## 3. Summary of Fixes Applied
1. **Dynamic Context Builder (§3.1):** Assembles context dynamically from `topics.json` (`name`, `discipline`, `subfield` defaulting to 'Engineering', `description`, each part's name & explanation, `equationsCovered`).
2. **Unified System Instruction (§3.2):** One single tutor system prompt across all topics instructing 2–5 sentence answers, explaining selected parts first, plain text formulas, and polite redirections.
3. **Provider Failover & Timeouts (§3.4):** Groq `qwen/qwen3.8-27b` primary with 20-second timeout; Gemini `gemini-3.5-flash` fallback with 20-second timeout.
4. **Error Handling & Disclaimer (§3.5, §3.6):** HTTP 503 on provider failure with retry button; AI disclaimer rendered under every answer in `TutorBox.jsx`.
