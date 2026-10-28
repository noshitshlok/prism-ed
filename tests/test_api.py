import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_root_liveness(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"status": "PrismEd API running"}

def test_health_diagnostics(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "ai" in data
    assert "primaryConfigured" in data["ai"]
    # Verify no secret keys are leaked
    res_text = res.text
    assert "gsk_" not in res_text
    assert "AIza" not in res_text

def test_list_topics_and_filters(client):
    res = client.get("/api/v1/topics")
    assert res.status_code == 200
    topics = res.json()
    assert len(topics) >= 2
    for t in topics:
        assert t["status"] == "ready"

    res_all = client.get("/api/v1/topics?include_all=true")
    assert res_all.status_code == 200
    assert len(res_all.json()) >= 22

    # Filter by discipline
    res_elec = client.get("/api/v1/topics?discipline=Electrical Engineering")
    assert res_elec.status_code == 200
    elec_topics = res_elec.json()
    assert len(elec_topics) >= 1
    for t in elec_topics:
        assert t["discipline"] == "Electrical Engineering"

def test_get_topic_detail_and_404(client):
    # Valid topic
    res = client.get("/api/v1/topics/circuit-board")
    assert res.status_code == 200
    detail = res.json()
    assert detail["id"] == "circuit-board"
    assert len(detail["parts"]) >= 5

    # Unknown topic -> standard error shape
    res_404 = client.get("/api/v1/topics/non-existent-topic")
    assert res_404.status_code == 404
    err_body = res_404.json()
    assert "error" in err_body
    assert err_body["error"]["code"] == "NOT_FOUND"
    assert "requestId" in err_body["error"]

def test_quiz_public_masking_and_submission(client):
    # Public quiz questions must NOT expose correctAnswerIndex or explanation
    res = client.get("/api/v1/quiz/circuit-board")
    assert res.status_code == 200
    quiz_data = res.json()
    assert quiz_data["topicId"] == "circuit-board"
    questions = quiz_data["questions"]
    assert len(questions) >= 3

    for q in questions:
        assert "correctAnswerIndex" not in q
        assert "engineeringExplanation" not in q
        assert len(q["options"]) == 4

    # Submit quiz answers
    q1_id = questions[0]["id"]
    submit_res = client.post("/api/v1/quiz/submit", json={
        "topicId": "circuit-board",
        "answers": {q1_id: 1}  # Option index 1
    })
    assert submit_res.status_code == 200
    graded = submit_res.json()
    assert "score" in graded
    assert "total" in graded
    assert "percentage" in graded
    assert "feedback" in graded

def test_progress_session_validation(client):
    # Missing X-Session-Id header -> 400
    res_no_sess = client.post("/api/v1/progress/attempts", json={
        "topicId": "circuit-board",
        "score": 3,
        "total": 3
    })
    assert res_no_sess.status_code == 400
    assert res_no_sess.json()["error"]["code"] == "VALIDATION_ERROR"

    # Malformed X-Session-Id header -> 400
    res_bad_sess = client.post("/api/v1/progress/attempts",
        headers={"X-Session-Id": "invalid-uuid-1234"},
        json={"topicId": "circuit-board", "score": 3, "total": 3}
    )
    assert res_bad_sess.status_code == 400

    # Valid UUID -> 200
    valid_uuid = str(uuid.uuid4())
    res_ok = client.post("/api/v1/progress/attempts",
        headers={"X-Session-Id": valid_uuid},
        json={"topicId": "circuit-board", "score": 3, "total": 3}
    )
    assert res_ok.status_code == 200
    res_data = res_ok.json()
    assert res_data["sessionId"] == valid_uuid
    assert res_data["score"] == 3

    # Progress Summary
    sum_res = client.get("/api/v1/progress/summary", headers={"X-Session-Id": valid_uuid})
    assert sum_res.status_code == 200
    summary = sum_res.json()
    assert summary["sessionId"] == valid_uuid
    assert summary["totalAttempts"] >= 1
