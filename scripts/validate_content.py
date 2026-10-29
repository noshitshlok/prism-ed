"""
PrismEd Content Validation Script
Validates topics.json, quiz.json, and public/models/<topicId>/license.txt
against strict Pydantic schemas and plan rules.
Exits with code 0 on success, or code 1 with exact file and field at fault.
"""
import sys
import json
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.schemas.topic import TopicDetail
from app.schemas.quiz import QuizQuestion

def validate_all_content():
    topics_path = BASE_DIR / "app" / "data" / "topics.json"
    quiz_path = BASE_DIR / "app" / "data" / "quiz.json"
    models_dir = BASE_DIR / "public" / "models"

    print(f"Checking {topics_path}...")
    if not topics_path.exists():
        print(f"ERROR: {topics_path} does not exist", file=sys.stderr)
        sys.exit(1)

    with open(topics_path, "r", encoding="utf-8") as f:
        try:
            raw_topics = json.load(f)
        except Exception as e:
            print(f"ERROR parsing JSON in {topics_path}: {e}", file=sys.stderr)
            sys.exit(1)

    topics_list = raw_topics.get("topics", [])
    if len(topics_list) < 22:
        print(f"ERROR: Expected at least 22 topics, found {len(topics_list)}", file=sys.stderr)
        sys.exit(1)

    validated_topic_ids = set()
    for idx, item in enumerate(topics_list):
        try:
            topic = TopicDetail(**item)
        except Exception as e:
            print(f"ERROR in {topics_path} [topic index {idx}, id={item.get('id')}]: {e}", file=sys.stderr)
            sys.exit(1)

        # Rule: Every topic has at least 5 parts
        if len(topic.parts) < 5:
            print(f"ERROR: Topic '{topic.id}' in {topics_path} has {len(topic.parts)} parts; minimum 5 required", file=sys.stderr)
            sys.exit(1)

        # Rule: Every model folder has a license.txt
        lic_file = models_dir / topic.id / "license.txt"
        if not lic_file.exists():
            print(f"ERROR: Missing license file for topic '{topic.id}' at {lic_file}", file=sys.stderr)
            sys.exit(1)
        
        # Check license file content
        lic_text = lic_file.read_text(encoding="utf-8").strip()
        if not lic_text or "Licence:" not in lic_text or "Source URL:" not in lic_text:
            print(f"ERROR: Incomplete license file for topic '{topic.id}' at {lic_file}", file=sys.stderr)
            sys.exit(1)

        # Rule (§1 & §9): For ready topics, modelUrl exists on disk and is under 8 MB
        if topic.status == "ready":
            clean_model_rel = topic.modelUrl.lstrip("/\\")
            model_file = BASE_DIR / "public" / clean_model_rel
            if not model_file.exists():
                # Try models_dir / topic.id / filename
                alt_model_file = models_dir / topic.id / Path(topic.modelUrl).name
                if alt_model_file.exists():
                    model_file = alt_model_file
                else:
                    print(f"ERROR: 3D model file for topic '{topic.id}' does not exist at {model_file}", file=sys.stderr)
                    sys.exit(1)

            size_bytes = model_file.stat().st_size
            max_size = 8 * 1024 * 1024
            if size_bytes > max_size:
                print(f"ERROR: 3D model file for topic '{topic.id}' exceeds 8MB limit: {size_bytes} bytes", file=sys.stderr)
                sys.exit(1)

        validated_topic_ids.add(topic.id)

    print(f"All {len(validated_topic_ids)} topics passed schema and license validation.")

    # Validate quizzes
    print(f"Checking {quiz_path}...")
    if not quiz_path.exists():
        print(f"ERROR: {quiz_path} does not exist", file=sys.stderr)
        sys.exit(1)

    with open(quiz_path, "r", encoding="utf-8") as f:
        try:
            raw_quiz = json.load(f)
        except Exception as e:
            print(f"ERROR parsing JSON in {quiz_path}: {e}", file=sys.stderr)
            sys.exit(1)

    quizzes_dict = raw_quiz.get("quizzes", {})
    for topic_id in validated_topic_ids:
        if topic_id not in quizzes_dict:
            print(f"ERROR: No quiz found for topic '{topic_id}' in {quiz_path}", file=sys.stderr)
            sys.exit(1)

        quiz_data = quizzes_dict[topic_id]
        questions = quiz_data.get("questions", [])
        if len(questions) < 3:
            print(f"ERROR: Topic '{topic_id}' has {len(questions)} quiz questions; minimum 3 required", file=sys.stderr)
            sys.exit(1)

        for q_idx, q in enumerate(questions):
            try:
                question_obj = QuizQuestion(**q)
            except Exception as e:
                print(f"ERROR in {quiz_path} [topic '{topic_id}', question {q_idx}]: {e}", file=sys.stderr)
                sys.exit(1)

            if len(question_obj.options) != 4:
                print(f"ERROR: Question '{question_obj.id}' in topic '{topic_id}' has {len(question_obj.options)} options; expected 4", file=sys.stderr)
                sys.exit(1)

    print(f"All {len(quizzes_dict)} quizzes passed schema and engineering validation.")
    print("Content validation completed successfully! [ALL 22 TOPICS GREEN]")

if __name__ == "__main__":
    validate_all_content()
