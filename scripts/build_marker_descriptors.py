"""
PrismEd Marker Descriptor Builder (Prompt v2 §4.2)
Extracts SIFT features (with ORB fallback) from reference marker images,
validates feature counts (≥ 200 keypoints), and serializes descriptors
and keypoint locations for homography RANSAC matching.
"""
import json
import sys
from pathlib import Path
import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
MARKERS_DIR = BASE_DIR / "app" / "data" / "markers"
INDEX_FILE = MARKERS_DIR / "markers_index.json"
IMAGES_DIR = MARKERS_DIR / "images"
DESCRIPTORS_DIR = MARKERS_DIR / "descriptors"

DESCRIPTORS_DIR.mkdir(parents=True, exist_ok=True)

def build_descriptors():
    if not INDEX_FILE.exists():
        print(f"Error: {INDEX_FILE} not found!")
        sys.exit(1)

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    markers = data.get("markers", [])
    if not markers:
        print("No markers found in index file!")
        sys.exit(1)

    # Use SIFT if available, else ORB
    if hasattr(cv2, "SIFT_create"):
        detector = cv2.SIFT_create()
        detector_name = "SIFT"
    else:
        detector = cv2.ORB_create(nfeatures=2000)
        detector_name = "ORB"

    print(f"Building descriptors using {detector_name} detector...")
    print(f"Total markers in catalogue: {len(markers)}\n")

    summary = []
    has_warning = False

    for marker in markers:
        marker_id = marker.get("markerId") or marker.get("id")
        image_name = marker.get("imageFile")
        img_path = IMAGES_DIR / image_name

        if not img_path.exists():
            print(f"ERROR: Image not found for {marker_id}: {img_path}")
            sys.exit(1)

        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"ERROR: Failed to load image {img_path}")
            sys.exit(1)

        keypoints, descriptors = detector.detectAndCompute(img, None)
        kps_count = len(keypoints) if keypoints is not None else 0

        # Flag marker if fewer than 200 keypoints
        status = "PASS"
        if kps_count < 200:
            status = "FLAGGED (fewer than 200 keypoints)"
            has_warning = True

        print(f"Marker: {marker_id:<28} | Keypoints: {kps_count:<5} | Status: {status}")

        if descriptors is not None:
            # Save both descriptors and keypoint coordinates (for RANSAC homography estimation)
            kps_pts = np.float32([kp.pt for kp in keypoints])
            
            # Save as compressed .npz archive
            out_npz = DESCRIPTORS_DIR / f"{marker_id}.npz"
            np.savez_compressed(
                str(out_npz),
                descriptors=descriptors,
                keypoints=kps_pts
            )
            # Also save raw descriptors as .npy for backwards compatibility
            out_npy = DESCRIPTORS_DIR / f"{marker_id}.npy"
            np.save(str(out_npy), descriptors)

        summary.append({
            "markerId": marker_id,
            "topicId": marker.get("topicId"),
            "keypoints": kps_count,
            "detector": detector_name,
            "status": status
        })

    print("\nDescriptor compilation finished.")
    if has_warning:
        print("WARNING: One or more markers had fewer than 200 keypoints.")
    else:
        print("All markers passed the 200-keypoint minimum threshold.")

    return summary

if __name__ == "__main__":
    build_descriptors()
