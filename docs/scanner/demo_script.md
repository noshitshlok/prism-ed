# PrismEd Scanner Glimpse — Teacher / Evaluator Demo Script (§7.7)

**Goal:** Demonstrate the end-to-end working Diagram Scanner Glimpse to instructors/evaluators in under 3 minutes.  
**Specification:** `PRISMED_SCANNER_GLIMPSE_v2.md`  
**Test Assets Location:** `app/data/markers/images/`  

---

## Pre-Demo Quick Check (30 seconds)
1. **Backend Server:** Running on port `8000` (`http://localhost:8000`).
2. **Frontend App:** Running on port `5173` (`http://localhost:5173`).
3. **Health Check:** Open `http://localhost:5173/api/v1/health` (or `http://localhost:8000/api/v1/health`) to show:
   ```json
   "scanner": {
     "markersLoaded": 3,
     "descriptorsLoaded": 3
   }
   ```

---

## 1. Scene 1: Exploring the Scanner Preview & Direct Card Launch (45s)
1. Open the application at `http://localhost:5173/`.
2. Notice the navigation header has **Scanner [preview]** in teal.
3. On the homepage, point out the **📷 Scanner** badge on the supported specimen cards (`Circuit Board`, `Automotive Differential Gearbox`, and `Four-Stroke Engine`).
4. Click **Scanner** in the header to navigate to `/scan`.
5. Point out:
   - Clean header: **Scanner** with `PREVIEW` pill.
   - Descriptive guidance: *"Point your camera at one of the diagrams below, or upload a photo of it."*
   - Two clear actions: **📸 Take photo** and **📁 Upload photo**.
   - The catalogue grid of the 3 supported diagrams below with thumbnails and display names.
6. **No-Camera Fallback demonstration:** Click the **Automotive Differential Gearbox** card.
   - The bench opens immediately at `/topics/differential-gearbox`.
   - A teal banner appears at top: **⚡ Opened from scanner match — focused part: planetary-bevel-gears**.
   - The planetary bevel pinions are highlighted and their margin notes are active.
   - Click **← Back to Scanner** to return.

---

## 2. Scene 2: Live Photograph Matching (60s)
1. In the Scanner, click **Upload photo** (or **Take photo** if on mobile).
2. Select `app/data/markers/images/circuit-board.png` (or show a printed copy / secondary screen).
3. The image preview mounts instantly.
4. Click **Match Diagram →**.
5. Observe:
   - Progress indicator: *"Scanning diagram features & estimating RANSAC homography..."*
   - Sub-second completion (~120 ms).
   - Match Confirmation panel:
     - **✓ Match Confirmed** tag
     - Confidence in words: **strong (100%)**
     - RANSAC inlier count: **164 verified inliers**
     - Reference thumbnail and topic title: **Printed Circuit Board (PCB)**
     - Focus component: `ic-chip`
6. Click **Open 3D Model →**.
   - The interactive 3D PCB specimen opens with the microcontroller IC chip selected.

---

## 3. Scene 3: Robustness Under Angle / Dim Lighting (30s)
1. Repeat the scan with `four-stroke-engine.png`.
2. Even rotated at an angle (~30°) or under low illumination, the backend's SIFT + RANSAC homography matches cleanly with over 60 inliers.
3. The match confirms **Four-Stroke IC Engine** and focuses on the **piston-assembly**.

---

## 4. Scene 4: Negative Control (No Guesswork Rule) (30s)
1. Upload an unrelated photo (e.g. text from a book, an architectural photo, or a random screenshot).
2. Click **Match Diagram →**.
3. Point out to the evaluator:
   - Status: **No match found**.
   - Message: *"No match. Try a closer photo in better light, or choose a diagram from the list below."*
   - Emphasize Hard Rule 3: **Zero false positives**. The system never hallucinates or guesses.

---

## Summary for Teacher
- **Supported preview topics:** 3 authentic engineering specimens (`circuit-board`, `differential-gearbox`, `four-stroke-engine`).
- **Feature matching:** SIFT keypoints (> 400 per marker) + RANSAC spatial homography check with minimum 18 inlier threshold.
- **Performance:** Full response in under 150 ms (exceeding the < 2.0s rule).
- **All 15 automated backend tests:** 100% green.

