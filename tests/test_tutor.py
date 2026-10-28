import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_ask_tutor_with_valid_topic_and_part():
    payload = {
        "topicId": "circuit-board",
        "partId": "capacitors",
        "question": "What is the function of electrolytic capacitors?"
    }
    res = client.post("/api/v1/tutor/ask", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 10
    assert data["topicId"] == "circuit-board"
    assert data["partId"] == "capacitors"
    # Ensure API keys are never exposed in response
    if settings.GROQ_API_KEY:
        assert settings.GROQ_API_KEY not in res.text
    if settings.GEMINI_API_KEY:
        assert settings.GEMINI_API_KEY not in res.text

def test_ask_tutor_topic_level_without_part_id():
    # Prompt v2 §4.1 & §4.2: partId is optional; tutor answers about the whole model
    payload = {
        "topicId": "circuit-board",
        "question": "What does this entire circuit board assembly do?"
    }
    res = client.post("/api/v1/tutor/ask", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert data["topicId"] == "circuit-board"
    assert data["partId"] is None
    assert len(data["answer"]) > 10

def test_ask_tutor_unknown_topic_returns_404():
    payload = {
        "topicId": "non-existent-quantum-engine-topic",
        "question": "How does this function?"
    }
    res = client.post("/api/v1/tutor/ask", json=payload)
    assert res.status_code == 404
    data = res.json()
    assert "error" in data
    assert data["error"]["code"] == "NOT_FOUND"

def test_ask_tutor_question_length_validation():
    # Question < 2 characters
    short_res = client.post("/api/v1/tutor/ask", json={
        "topicId": "circuit-board",
        "question": "?"
    })
    assert short_res.status_code == 422

    # Question > 500 characters
    long_res = client.post("/api/v1/tutor/ask", json={
        "topicId": "circuit-board",
        "question": "A" * 501
    })
    assert long_res.status_code == 422

def test_legacy_route_alias():
    # §4.1: POST /tutor/ or /tutor alias must work without breaking
    payload = {
        "topicId": "circuit-board",
        "partId": "capacitors",
        "question": "Explain capacitor dielectric breakdown."
    }
    res = client.post("/api/v1/tutor", json=payload)
    assert res.status_code == 200
    assert "answer" in res.json()

def test_api_keys_not_exposed_in_any_response():
    for endpoint in ["/api/v1/tutor/ask", "/api/v1/health"]:
        res = client.get(endpoint) if endpoint == "/api/v1/health" else client.post(endpoint, json={
            "topicId": "circuit-board",
            "question": "Testing security sanitization"
        })
        text = res.text
        if settings.GROQ_API_KEY:
            assert settings.GROQ_API_KEY not in text
        if settings.GEMINI_API_KEY:
            assert settings.GEMINI_API_KEY not in text

