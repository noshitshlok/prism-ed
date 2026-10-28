import json
import re
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent

def test_topics_json_validity():
    topics_file = BASE_DIR / "app" / "data" / "topics.json"
    assert topics_file.exists(), "topics.json must exist"

    with open(topics_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", [])
    assert len(topics) >= 22, f"Expected at least 22 topics, found {len(topics)}"

    models_dir = BASE_DIR / "public" / "models"

    for t in topics:
        assert "id" in t and t["id"], "Topic must have a non-empty id"
        assert "name" in t and t["name"], "Topic must have a non-empty name"
        assert "discipline" in t and t["discipline"], "Topic must have a discipline"
        assert "parts" in t, f"Topic {t['id']} must have parts"
        assert len(t["parts"]) >= 5, f"Topic {t['id']} must have at least 5 parts"

        # Check coordinates
        for p in t["parts"]:
            pos = p.get("hotspotPosition", "")
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", pos)
            assert len(numbers) >= 3, f"Part {p.get('id')} in {t['id']} must have 3 coordinates: {pos}"
            assert p.get("explanation"), f"Part {p.get('id')} in {t['id']} must have an explanation"

        # Check license file
        lic_file = models_dir / t["id"] / "license.txt"
        assert lic_file.exists(), f"Missing license.txt for topic {t['id']}"
        lic_text = lic_file.read_text(encoding="utf-8")
        assert "Licence:" in lic_text or "license" in lic_text.lower(), f"License text missing licence info in {lic_file}"

def test_quiz_json_validity():
    quiz_file = BASE_DIR / "app" / "data" / "quiz.json"
    assert quiz_file.exists(), "quiz.json must exist"

    with open(quiz_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    quizzes = data.get("quizzes", {})
    assert len(quizzes) >= 22, f"Expected at least 22 quizzes, found {len(quizzes)}"

    for topic_id, q_data in quizzes.items():
        questions = q_data.get("questions", [])
        assert len(questions) >= 3, f"Topic {topic_id} must have at least 3 quiz questions"

        for q in questions:
            assert "question" in q and q["question"], f"Question missing text in {topic_id}"
            options = q.get("options", [])
            assert len(options) == 4, f"Question {q.get('id')} in {topic_id} must have exactly 4 options"
            idx = q.get("correctAnswerIndex")
            assert isinstance(idx, int) and 0 <= idx < len(options), (
                f"Question {q.get('id')} in {topic_id} has invalid correctAnswerIndex: {idx}"
            )
            assert q.get("engineeringExplanation"), f"Question {q.get('id')} in {topic_id} must have an explanation"
