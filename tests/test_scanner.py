import io
import json
from pathlib import Path
from fastapi.testclient import TestClient
import numpy as np
import cv2
from app.main import app

client = TestClient(app)
BASE_DIR = Path(__file__).resolve().parent.parent
MARKERS_INDEX = BASE_DIR / "app" / "data" / "markers" / "markers_index.json"
IMAGES_DIR = BASE_DIR / "app" / "data" / "markers" / "images"

def test_scanner_markers_list():
    res = client.get("/api/v1/scanner/markers")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 3
    assert len(data["markers"]) == 3
    for m in data["markers"]:
        assert "markerId" in m
        assert "topicId" in m
        assert "displayName" in m
        assert "thumbnailUrl" in m

def test_health_reports_scanner_markers():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert "scanner" in data
    assert data["scanner"]["markersLoaded"] == 3
    assert data["scanner"]["descriptorsLoaded"] == 3

def test_each_supported_marker_matches_itself():
    assert MARKERS_INDEX.exists()
    with open(MARKERS_INDEX, "r", encoding="utf-8") as f:
        meta = json.load(f)

    for marker in meta["markers"]:
        marker_id = marker["markerId"]
        topic_id = marker["topicId"]
        img_file = marker["imageFile"]
        img_path = IMAGES_DIR / img_file

        assert img_path.exists(), f"Image {img_path} missing for {marker_id}"
        with open(img_path, "rb") as f:
            content = f.read()

        res = client.post(
            "/api/v1/scanner/match",
            files={"file": (img_file, content, "image/png")}
        )
        assert res.status_code == 200, f"Match failed with status {res.status_code} for {marker_id}: {res.text}"
        data = res.json()
        assert data["matched"] is True, f"Failed to match self for {marker_id}"
        assert data["markerId"] == marker_id
        assert data["topicId"] == topic_id
        assert data["highlightPartId"] == marker.get("highlightPartId")
        assert data["confidence"] > 0.0
        assert data["inliers"] >= 18

def test_scanner_unrelated_image_no_match():
    # Random uniform noise image
    random_noise = np.random.randint(0, 256, (500, 500, 3), dtype=np.uint8)
    _, buffer = cv2.imencode(".png", random_noise)

    res = client.post(
        "/api/v1/scanner/match",
        files={"file": ("unrelated_noise.png", buffer.tobytes(), "image/png")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["matched"] is False
    assert data["confidence"] < 0.40

def test_scanner_corrupt_upload_returns_400():
    corrupt_bytes = b"NOT_A_VALID_IMAGE_HEADER_CORRUPTED_BYTES"
    res = client.post(
        "/api/v1/scanner/match",
        files={"file": ("corrupt.png", corrupt_bytes, "image/png")}
    )
    assert res.status_code == 400
    data = res.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_scanner_oversized_upload_returns_400():
    # 5.5 MB payload (exceeds 5 MB limit)
    oversized_bytes = b"0" * (5500 * 1024)
    res = client.post(
        "/api/v1/scanner/match",
        files={"file": ("huge.png", oversized_bytes, "image/png")}
    )
    assert res.status_code == 400
    data = res.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
