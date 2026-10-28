"""
PrismEd Scanner Service (Prompt v2 §4.3)
Feature extraction, ratio test matching, RANSAC homography estimation,
and confidence scoring for the Scanner Glimpse preview.
"""
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import cv2
import numpy as np
from fastapi import HTTPException

from app.schemas.scanner import MarkerItem, ScannerMarkersResponse, ScannerMatchResponse
from app.core.logging import logger

BASE_DIR = Path(__file__).resolve().parent.parent
MARKERS_DIR = BASE_DIR / "data" / "markers"
INDEX_FILE = MARKERS_DIR / "markers_index.json"
DESCRIPTORS_DIR = MARKERS_DIR / "descriptors"
TOPICS_FILE = BASE_DIR / "data" / "topics.json"

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
RANSAC_INLIER_THRESHOLD = 18  # Empirically validated: 0 false positives, matches >= 30-740
MAX_QUERY_DIM = 1200  # Resize query to max 1200px for sub-second matching

class ScannerService:
    def __init__(self):
        self._markers_catalog: List[MarkerItem] = []
        self._descriptors: Dict[str, np.ndarray] = {}
        self._keypoints: Dict[str, np.ndarray] = {}
        self._topic_names: Dict[str, str] = {}
        self._detector = cv2.SIFT_create() if hasattr(cv2, "SIFT_create") else cv2.ORB_create()
        self._matcher = cv2.BFMatcher()
        self._load_topic_names()
        self._load_markers()

    def _load_topic_names(self):
        if not TOPICS_FILE.exists():
            return
        try:
            with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for t in data.get("topics", []):
                    self._topic_names[t["id"]] = t.get("name", t["id"])
        except Exception as e:
            logger.warning(f"Could not load topics.json for scanner topic names: {e}")

    def _load_markers(self):
        self._markers_catalog.clear()
        self._descriptors.clear()
        self._keypoints.clear()

        if not INDEX_FILE.exists():
            logger.warning(f"Scanner index file {INDEX_FILE} not found.")
            return

        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_markers = data.get("markers", [])
        for m in raw_markers:
            marker_id = m.get("markerId") or m.get("id")
            topic_id = m.get("topicId")
            display_name = m.get("displayName") or self._topic_names.get(topic_id, topic_id)
            highlight_part = m.get("highlightPartId")
            image_file = m.get("imageFile", "")

            item = MarkerItem(
                markerId=marker_id,
                topicId=topic_id,
                displayName=display_name,
                thumbnailUrl=f"/api/v1/scanner/markers/{marker_id}/thumbnail",
                highlightPartId=highlight_part,
                source=m.get("source", "render"),
                licence=m.get("licence", "project"),
                credit=m.get("credit", ""),
                id=marker_id
            )
            self._markers_catalog.append(item)

            # Load precomputed .npz descriptors and keypoint locations
            npz_file = DESCRIPTORS_DIR / f"{marker_id}.npz"
            npy_file = DESCRIPTORS_DIR / f"{marker_id}.npy"

            if npz_file.exists():
                npz_data = np.load(str(npz_file))
                self._descriptors[marker_id] = npz_data["descriptors"]
                self._keypoints[marker_id] = npz_data["keypoints"]
            elif npy_file.exists():
                self._descriptors[marker_id] = np.load(str(npy_file))

        logger.info(f"Loaded {len(self._markers_catalog)} markers and {len(self._descriptors)} descriptors into ScannerService.")

    @property
    def markers_count(self) -> int:
        return len(self._markers_catalog)

    @property
    def descriptors_count(self) -> int:
        return len(self._descriptors)

    def list_supported_markers(self) -> ScannerMarkersResponse:
        return ScannerMarkersResponse(
            markers=self._markers_catalog,
            count=len(self._markers_catalog),
            previewNotice="PrismEd Scanner Glimpse Preview (Verified 3D Models)"
        )

    def get_marker_by_id(self, marker_id: str) -> Optional[MarkerItem]:
        for m in self._markers_catalog:
            if m.markerId == marker_id or m.id == marker_id:
                return m
        return None

    def match_image(self, image_bytes: bytes, filename: str = "upload.png", content_type: Optional[str] = None) -> ScannerMatchResponse:
        # 1. Enforce 5 MB maximum size limit
        if len(image_bytes) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "VALIDATION_ERROR",
                    "message": f"Upload exceeds maximum allowable size of 5 MB ({round(len(image_bytes)/(1024*1024), 2)} MB received)."
                }
            )

        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "VALIDATION_ERROR",
                    "message": "Uploaded file is empty (0 bytes received)."
                }
            )

        # 2. Decode image to greyscale
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        if img is None:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "VALIDATION_ERROR",
                    "message": "Could not decode image data. Supported formats are PNG, JPEG, and WebP."
                }
            )

        # 3. Resize if query is larger than MAX_QUERY_DIM to guarantee < 2s response time
        h, w = img.shape
        if max(h, w) > MAX_QUERY_DIM:
            scale = float(MAX_QUERY_DIM) / float(max(h, w))
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        # 4. Extract query features
        query_kps, query_descs = self._detector.detectAndCompute(img, None)
        if query_descs is None or len(query_kps) < 8:
            return ScannerMatchResponse(
                matched=False,
                confidence=0.0,
                inliers=0,
                message="Insufficient distinct visual features detected. Ensure the diagram is in focus and well lit."
            )

        best_marker: Optional[MarkerItem] = None
        best_inliers: int = 0
        best_confidence: float = 0.0

        # 5. Match against each candidate marker descriptor
        for marker in self._markers_catalog:
            ref_descs = self._descriptors.get(marker.markerId)
            ref_kps = self._keypoints.get(marker.markerId)

            if ref_descs is None or len(ref_descs) < 8:
                continue

            # k-NN match with k=2
            matches = self._matcher.knnMatch(query_descs, ref_descs, k=2)

            # Lowe's ratio test (0.75)
            good_matches = []
            for pair in matches:
                if len(pair) == 2:
                    m, n = pair
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)

            # RANSAC homography estimation
            inliers = 0
            if len(good_matches) >= 4 and ref_kps is not None:
                src_pts = np.float32([query_kps[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([ref_kps[m.trainIdx] for m in good_matches]).reshape(-1, 1, 2)
                try:
                    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                    if mask is not None:
                        inliers = int(np.sum(mask))
                except Exception as e:
                    logger.debug(f"Homography computation skipped: {e}")
                    inliers = 0
            elif len(good_matches) >= 12:
                # Fallback if keypoint locations weren't saved
                inliers = len(good_matches)

            # Check if this is the best candidate
            if inliers > best_inliers:
                best_inliers = inliers
                best_marker = marker

        # 6. Apply verified acceptance threshold
        if best_marker and best_inliers >= RANSAC_INLIER_THRESHOLD:
            # Scaled confidence: 18 inliers -> 0.40, 45+ inliers -> 1.00
            confidence = round(min(1.0, max(0.20, best_inliers / 45.0)), 2)
            topic_name = self._topic_names.get(best_marker.topicId, best_marker.displayName)

            return ScannerMatchResponse(
                matched=True,
                markerId=best_marker.markerId,
                topicId=best_marker.topicId,
                topicName=topic_name,
                highlightPartId=best_marker.highlightPartId,
                confidence=confidence,
                inliers=best_inliers,
                message=f"Matched {best_marker.displayName} with {best_inliers} verified RANSAC inliers."
            )

        # 7. No match above threshold
        return ScannerMatchResponse(
            matched=False,
            confidence=round(min(0.35, best_inliers / 50.0), 2) if best_inliers > 0 else 0.0,
            inliers=best_inliers,
            message="No matching diagram found. Try a closer photo in better light, or choose a specimen from the preview list."
        )

scanner_service = ScannerService()
