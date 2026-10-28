# PrismEd Scanner Glimpse — Selected Marker Topics (v2)

**Specification:** `PRISMED_SCANNER_GLIMPSE_v2.md` (§2)  
**Status:** Approved for Live Demo  
**Selection Count:** 3 verified production topics with authentic CAD/physical models  

---

## 1. Topic Evaluation & Selection Methodology

Following `PRISMED_SCANNER_GLIMPSE_v2.md` §2, all candidate topics were filtered against the following criteria:
1. **Status `ready`:** Confirmed in `MODEL_REPORT.md` and verified in the WebGL viewer.
2. **Visual Feature Density:** Distinctive surface texture, multi-component silhouettes, and high contrast detail (matching requires ≥ 200 SIFT keypoints).
3. **Rigidity & Perspective Invariance:** Geometrically rigid mechanical/electrical specimen that preserves feature relationships from frontal and oblique angles (up to 30°–45°).
4. **Legibility & Printability:** Clearly identifiable when printed at standard A4 size or viewed on an auxiliary display screen.

---

## 2. Selected Topics and Verification Results

| # | Topic ID | Topic Name | Source & Licence | Highlight Part ID | SIFT Keypoints (1600px) | Reasons for Selection |
|---|---|---|---|---|---|---|
| 1 | `circuit-board` | Printed Circuit Board (PCB Assembly) | Sketchfab (Rowan Design), CC-BY-4.0 | `ic-chip` | **741 keypoints** | • High-density planar surface with microchips, capacitors, traces, resistor arrays, and solder joints.<br>• Excellent contrast against light background; highly robust to homography transformation.<br>• Unmodified project specimen per Hard Rule 1. |
| 2 | `differential-gearbox` | Automotive Differential Gearbox | Khronos glTF-Sample-Models, CC-BY-4.0 | `planetary-bevel-gears` | **419 keypoints** | • Intricate geometric interlocking gear teeth, spiral bevel pinion, differential cage, and axle shafts.<br>• Rigid automotive transmission CAD assembly.<br>• Crisp mechanical contours provide outstanding RANSAC inlier ratio under moderate rotation. |
| 3 | `four-stroke-engine` | Four-Stroke Internal Combustion Engine | Khronos glTF-Sample-Models, CC-BY-4.0 | `piston-assembly` | **470 keypoints** | • Dual-cylinder block with cooling fins, reciprocating pistons, connecting rods, counterweighted crankshaft, and valves.<br>• High-contrast CAD contours visible and distinct at A4 scale.<br>• Multi-scale mechanical features ensure reliable matching in varying lighting conditions. |

---

## 3. Reference Image Specifications

Per §3:
1. All reference images are rendered directly from PrismEd's own verified 3D models using the project's WebGL renderer on a clean light background (`#fbf9f5`).
2. Longest dimension is **1600 px** (1600 × 1200 px), ensuring sharp edge definitions.
3. Reference images are stored in `app/data/markers/images/<topic-id>.png`.
4. High-performance downsampled thumbnails (400 × 300 px) are stored in `app/data/markers/thumbnails/<topic-id>_thumb.png`.
5. Keypoint count on all three selected markers exceeds the 200-keypoint minimum threshold by **2.0× to 3.7×**.

