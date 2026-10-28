import re
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app

BASE_DIR = Path(__file__).resolve().parent.parent

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_all_22_topics_content_schema_and_models(client):
    # Verify default returns ready topics
    res_ready = client.get("/api/v1/topics")
    assert res_ready.status_code == 200
    ready_topics = res_ready.json()
    assert len(ready_topics) >= 2
    for t in ready_topics:
        assert t["status"] == "ready"

    # Verify all 22 topics with include_all=true
    res = client.get("/api/v1/topics?include_all=true")
    assert res.status_code == 200
    topics_list = res.json()
    assert len(topics_list) >= 22

    for t_item in topics_list:
        topic_id = t_item["id"]
        # 1. Topic detail loads from /topics/{id}
        res_detail = client.get(f"/api/v1/topics/{topic_id}")
        assert res_detail.status_code == 200
        detail = res_detail.json()

        # 2. modelSource and status are valid
        assert detail.get("modelSource") in {"scan", "cad", "uploaded", "generated", "analogue"}
        assert detail.get("status") in {"ready", "not_in_demo"}

        # 3. modelUrl exists on disk and is under 8 MB
        model_url = detail["modelUrl"].lstrip("/\\")
        model_file = BASE_DIR / "public" / model_url
        if not model_file.exists():
            model_file = BASE_DIR / "public" / "models" / topic_id / Path(detail["modelUrl"]).name
        assert model_file.exists(), f"Model file missing for topic '{topic_id}' at {model_file}"

        file_size = model_file.stat().st_size
        assert file_size <= 8 * 1024 * 1024, f"Model file for '{topic_id}' exceeds 8 MB: {file_size} bytes"

        # 4. Each hotspotPosition and hotspotNormal parses
        parts = detail["parts"]
        assert len(parts) >= 5, f"Topic '{topic_id}' must have at least 5 parts"
        part_ids = []

        for p in parts:
            part_ids.append(p["id"])
            pos = p["hotspotPosition"]
            nums = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", pos)
            assert len(nums) >= 3, f"Invalid hotspotPosition in {topic_id} part {p['id']}: {pos}"

            if "hotspotNormal" in p and p["hotspotNormal"]:
                norm_nums = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", p["hotspotNormal"])
                assert len(norm_nums) >= 3, f"Invalid hotspotNormal in {topic_id}: {p['hotspotNormal']}"

        # 5. Part IDs are unique within each topic
        assert len(part_ids) == len(set(part_ids)), f"Duplicate part IDs in '{topic_id}': {part_ids}"

        # 6. license.txt exists in model folder
        lic_file = BASE_DIR / "public" / "models" / topic_id / "license.txt"
        assert lic_file.exists(), f"Missing license.txt for topic '{topic_id}'"
