# PrismEd Ask Tutor — Diagnosis Report (§3)

**Specification:** `PRISMED_FIX_ASK_TUTOR.md` (§3)  
**Date:** 2026-10-28  
**Target:** Ask Tutor Component & Backend Endpoint  

---

## 1. Reproduction Steps

1. Launch backend (`python -m uvicorn app.main:app --port 8000`) and frontend (`npm run dev`).
2. Navigate to `http://localhost:5173/topics/circuit-board`.
3. In the right-hand margin panel, note the "Ask about this part" box.
4. Enter question: *"Why does Electrolytic Capacitors work this way?"*.
5. Click **Ask**.

### Observed Behaviors:
- **Network Request:** `POST /api/v1/tutor/stream` followed by `POST /api/v1/tutor/ask`.
- **Backend Response:** Prior to fix, returned `503 AI_UNAVAILABLE` due to deprecated model name (`llama-3.3-70b-versatile` returned `404 model_not_found` from Groq).
- **UI State Loss:** When a user clicked outside a pin or if no part was selected, `MarginNotes.jsx` completely unmounted `<TutorBox />` because it was wrapped in `{selectedPart ? ... : ...}`, reverting the entire right panel to the empty placeholder: *"Select a numbered point on the 3D model..."*.
- **Topic-Level Block:** Asking a question without selecting a part was impossible because the input was hidden, and the backend schema strictly required `partId: str` (returning `422 Unprocessable Entity` or `404 NOT_FOUND` if `partId` was omitted).

---

## 2. Investigation Matrix (§3.4)

| # | Hypothesized Cause | Evaluation Method | Result | Finding & Resolution |
|---|---|---|---|---|
| **A** | **Route mismatch** | Compared `src/api/tutor.js` with `app/routers/tutor.py` | **Partial** | Frontend called `/api/v1/tutor/ask` and `/api/v1/tutor/stream`. Routes aligned, but `POST /tutor/` alias was needed to preserve legacy compatibility per §4.1. |
| **B** | **Environment variable mismatch** | Checked `.env` against `app/core/config.py` | **CONFIRMED** | Root `.env` was missing. Loaded `.env.example` had deprecated model `llama-3.3-70b-versatile`. Updated to active model `qwen/qwen3.8-27b`. |
| **C** | **Backend exception** | Inspected server tracebacks on `/api/v1/tutor/ask` | **CONFIRMED** | Missing keys/deprecated model raised `503`. Resolved by adding curriculum-grounded fallback synthesized directly from `topics.json`. |
| **D** | **Selection cleared** | Inspected `MarginNotes.jsx` and `ModelViewer.jsx` event propagation | **CONFIRMED (Primary UI Root Cause)** | `MarginNotes.jsx` conditionally unmounted `TutorBox` when `!selectedPart`, resetting panel to empty state. Background canvas clicks cleared selection. Fixed by mounting `TutorBox` persistently at the topic level and preventing canvas click leaks. |
| **E** | **Missing context** | Examined `TutorRequest` schema in `app/schemas/tutor.py` | **CONFIRMED** | `partId: str` was mandatory. When `partId` was omitted or `None`, FastAPI raised `422` and route handler raised `404`. Fixed by making `partId: Optional[str] = None`. |
| **F** | **Response shape mismatch** | Compared `TutorResponse` against §4.1 | **CONFIRMED** | Response was missing `topicId` and `partId`. Updated schema to `{ answer, topicId, partId }`. |
| **G** | **Model-specific failure** | Tested across multiple topics (`circuit-board`, `space-suit`, `differential-gearbox`) | **Negative** | The failure was systemic across all 22 models due to Causes B, D, and E. |

---

## 3. Summary of Root Causes
1. **Schema & Route:** `partId` was mandatory in `TutorRequest`, blocking topic-level questions. Response schema lacked `topicId` and `partId`.
2. **UI Unmounting:** `MarginNotes.jsx` hid the tutor box when `selectedPart` was null, preventing general model inquiries and discarding state.
3. **AI Model & Fallback:** Groq model identifier was outdated and there was no offline curriculum fallback.

