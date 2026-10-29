# PrismEd — Interactive 3D / AR Engineering Pedagogy & AI Tutor

[![CI Test Suite](https://github.com/noshitshlok/prism-ed/actions/workflows/ci.yml/badge.svg)](https://github.com/noshitshlok/prism-ed)
[![License: CC-BY-4.0 / MIT](https://img.shields.io/badge/License-CC--BY--4.0%20%2F%20MIT-blue.svg)](MODEL_REPORT.md)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](requirements.txt)
[![React: 19](https://img.shields.io/badge/React-19-61dafb.svg)](package.json)
[![Tests: 21 Passed](https://img.shields.io/badge/Tests-21%20Passed%20(100%25)-success.svg)](tests/)

**PrismEd** is an engineering learning platform that replaces static 2D textbook figures with interactive, real-time 3D specimens, coordinate-anchored spatial hotspots, an engineering-grounded AI tutor, and computer-vision diagram scanning.

---

## Key Features

- **22 Authentic 3D Engineering Specimens:** Real CAD assemblies and clinical scans spanning 9 engineering disciplines (Mechanical, Electrical, Aerospace, Biomedical, Systems, AI/ML, Computing, Robotics, Civil).
- **Spatial Hotspot Navigation & Part Isolation:** Click coordinate-calibrated 3D mesh pins to inspect mechanical mechanisms, isolate components, or view animations.
- **Grounded AI Engineering Tutor:** Real-time token streaming grounded in the specific component's physics and governing equations, with automatic curriculum fallback for offline evaluations.
- **Computer-Vision Diagram Scanner:** Snap a photo of a textbook diagram with your smartphone to recognize the diagram using OpenCV SIFT feature extraction and RANSAC homography estimation, opening the 3D model with the matched component highlighted.
- **Integrated Knowledge Checks:** 22 interactive technical quizzes with instant grading and distractor rationale explanations.
- **Specimen Showcase Gallery:** Complete interactive turntable gallery grouped by discipline.

---

## Quick Start

> For a complete step-by-step setup walkthrough including API keys and troubleshooting, check out the [**SETUP_GUIDE.md**](SETUP_GUIDE.md).

### 1. Backend Setup (FastAPI)
```bash
# Clone the repository
git clone https://github.com/noshitshlok/prism-ed.git
cd prism-ed

# Install Python dependencies
pip install -r requirements.txt

# Create environment configuration
cp .env.example .env

# Run FastAPI backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup (React 19 + Vite 8)
```bash
# In a new terminal:
npm install

# Start Vite development server
npm run dev
```

Visit **`http://localhost:5173`** in your browser.

---

## Tech Stack

- **Frontend:** React 19, `@google/model-viewer` 4.3, React Router v7, Axios, Vite 8, Oxlint
- **Backend:** FastAPI, Starlette, Uvicorn, SlowAPI, SQLite, SQLAlchemy 2.0, Pydantic 2.13
- **Computer Vision:** OpenCV (`cv2` 5.0), NumPy (SIFT keypoint extraction & RANSAC homography)
- **AI Tutoring:** Groq SDK (`qwen/qwen3.8-27b`), Google GenAI (`gemini-1.5/3.8-flash`)

---

## Testing & Quality Assurance

```bash
# Run automated backend test suite (21 / 21 tests)
python -m pytest tests/

# Run strict content validator across all 22 topics & quizzes
python scripts/validate_content.py

# Run frontend linter (0 errors, 0 warnings)
npm run lint

# Build production bundle
npm run build
```

---

## Documentation

- [`PROJECT_REPORT.md`](PROJECT_REPORT.md): Full technical specification, architectural diagrams, and project report.
- [`MODEL_REPORT.md`](MODEL_REPORT.md): Complete specimen inventory with triangle counts, file sizes, and upstream licenses.
- [`docs/scanner/test_results.md`](docs/scanner/test_results.md): Environmental testing matrix for the computer-vision diagram scanner.
- [`docs/tutor/diagnosis.md`](docs/tutor/diagnosis.md): Grounded AI tutor architectural analysis and test results.

---

## License

Code is licensed under the MIT License. 3D specimen models retain their respective open-source licenses (CC-BY-4.0, MIT, NASA Public Domain, KiCad GPL+exception) as documented in [`MODEL_REPORT.md`](MODEL_REPORT.md) and each model's `license.txt`.

