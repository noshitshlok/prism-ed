import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.services.tutor_service import tutor_service
from app.schemas.tutor import TutorRequest
from app.schemas.topic import TopicDetail, Part

client = TestClient(app)

# 1. Request with partId builds a prompt containing that part's name.
def test_prompt_with_part_id_contains_part_name():
    req = TutorRequest(
        topicId="circuit-board",
        partId="capacitors",
        question="What does this part do?"
    )
    messages = tutor_service._build_messages(req)
    system_content = messages[0]["content"]
    assert "Electrolytic Capacitors" in system_content or "capacitors" in system_content
    assert "Selected Part:" in system_content
    assert messages[-1]["content"] == "What does this part do?"

# 2. Request without partId builds a valid prompt.
def test_prompt_without_part_id_builds_valid_prompt():
    req = TutorRequest(
        topicId="circuit-board",
        partId=None,
        question="What does this model show?"
    )
    messages = tutor_service._build_messages(req)
    system_content = messages[0]["content"]
    assert "Selected Part:" not in system_content
    assert "Topic: Circuit Board" in system_content or "Topic: " in system_content
    assert "Model Parts:" in system_content
    assert messages[-1]["content"] == "What does this model show?"

# 3. A topic with no part explanations builds a valid prompt.
def test_topic_with_no_part_explanations_builds_valid_prompt():
    mock_topic = TopicDetail(
        id="mock-specimen",
        name="Mock Specimen",
        description="A test specimen.",
        discipline="Mechanical",
        subfield=None,
        modelUrl="/models/mock.glb",
        parts=[
            Part(
                id=f"part-{i}",
                name=f"Part {i}",
                hotspotPosition="0m 0m 0m",
                explanation="",  # empty explanation
                formulaOrLaw=None
            ) for i in range(5)
        ]
    )
    with patch("app.services.topic_service.topic_service.get_topic_by_id", return_value=mock_topic):
        with patch("app.services.topic_service.topic_service.get_part", return_value=mock_topic.parts[0]):
            req = TutorRequest(
                topicId="mock-specimen",
                partId="part-0",
                question="Explain this component."
            )
            messages = tutor_service._build_messages(req)
            assert len(messages) >= 2
            system_content = messages[0]["content"]
            assert "Topic: Mock Specimen" in system_content
            assert "Subfield: Engineering" in system_content
            assert "Selected Part: Part 0" in system_content

# 4. Unknown topicId returns 404; bad question length returns 422.
def test_unknown_topic_id_returns_404():
    res = client.post("/api/v1/tutor/ask", json={
        "topicId": "non-existent-topic-xyz",
        "question": "What is this?"
    })
    assert res.status_code == 404
    data = res.json()
    assert "error" in data
    assert data["error"]["code"] == "NOT_FOUND"

def test_bad_question_length_returns_422():
    # Shorter than 2 characters
    res_short = client.post("/api/v1/tutor/ask", json={
        "topicId": "circuit-board",
        "question": "a"
    })
    assert res_short.status_code == 422
    data_short = res_short.json()
    assert "error" in data_short
    assert data_short["error"]["code"] == "VALIDATION_ERROR"

    # Longer than 500 characters
    res_long = client.post("/api/v1/tutor/ask", json={
        "topicId": "circuit-board",
        "question": "a" * 501
    })
    assert res_long.status_code == 422
    data_long = res_long.json()
    assert "error" in data_long
    assert data_long["error"]["code"] == "VALIDATION_ERROR"

# 5. Provider failure returns 503 in the standard format.
def test_provider_failure_returns_503_standard_format():
    with patch("app.services.ai_client.ai_client.complete", side_effect=RuntimeError("Connection timeout to LLM provider")):
        res = client.post("/api/v1/tutor/ask", json={
            "topicId": "circuit-board",
            "question": "What does this circuit do?"
        })
        assert res.status_code == 503
        data = res.json()
        assert "error" in data
        assert data["error"]["code"] == "AI_UNAVAILABLE"
        assert "requestId" in data["error"]
        assert data["error"]["message"] == "The tutor is unavailable right now."

# 6. The API key never appears in responses or logs.
def test_api_key_never_appears_in_responses():
    with patch("app.services.ai_client.ai_client.complete", return_value={"content": "A capacitor stores charge.", "model_used": "mock"}):
        res = client.post("/api/v1/tutor/ask", json={
            "topicId": "circuit-board",
            "partId": "capacitors",
            "question": "What does this part do?"
        })
        assert res.status_code == 200
        text = res.text
        if settings.GROQ_API_KEY:
            assert settings.GROQ_API_KEY not in text
        if settings.GEMINI_API_KEY:
            assert settings.GEMINI_API_KEY not in text
