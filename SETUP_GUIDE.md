# PrismEd — Local Setup & Execution Guide

This comprehensive guide walks you through setting up and running **PrismEd** (Interactive 3D / AR Engineering Pedagogy & AI Tutoring Platform) from scratch on any computer (Windows, macOS, or Linux).

---

## 1. Prerequisites

Before starting, ensure your system has the following software installed:

| Requirement | Minimum Version | Check Installation Command | Download / Install Link |
|---|---|---|---|
| **Python** | 3.10+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ (LTS recommended) | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | `npm --version` | Bundled with Node.js |
| **Git** | 2.30+ | `git --version` | [git-scm.com](https://git-scm.com/) |

---

## 2. API Keys Required (Free Tier Available)

PrismEd utilizes a dual-tier AI architecture: **Groq** for high-speed streaming inference and **Google Gemini** as an automatic fallback provider. Both offer free API tiers.

### A. Groq API Key (Primary LLM Provider)
- **What it powers:** Real-time token-streaming AI Tutor (`/api/v1/tutor/stream` & `/api/v1/tutor/ask`) and Quiz explanations.
- **Cost:** Free tier available with generous rate limits.
- **How to get it:**
  1. Go to [Groq Console](https://console.groq.com/).
  2. Sign in with GitHub or Google.
  3. Navigate to **API Keys** in the sidebar.
  4. Click **Create API Key**, copy the key (starts with `gsk_...`), and save it securely.

### B. Google Gemini API Key (Automatic Fallback Provider)
- **What it powers:** High-reliability fallback if Groq encounters network timeouts, rate limits, or provider 5xx errors.
- **Cost:** Free tier available via Google AI Studio.
- **How to get it:**
  1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
  2. Sign in with your Google account.
  3. Click **Create API Key**.
  4. Copy the generated API key (starts with `AIzaSy...`) and save it securely.

> [!IMPORTANT]
> **Security Rule:** Never commit your `.env` file or API keys to GitHub. Keys must only be stored in your local `.env` file (which is automatically ignored by `.gitignore`).

---

## 3. Clone the Repository

Open your terminal or command prompt and clone the repository:

```bash
git clone https://github.com/noshitshlok/prism-ed.git
cd prism-ed
```

---

## 4. Environment Configuration

1. Create your environment configuration file from the provided template:
   ```bash
   # On Windows (PowerShell):
   Copy-Item .env.example app/.env

   # On macOS / Linux:
   cp .env.example app/.env
   ```

2. Open `app/.env` (or `.env` in the root folder) in your code editor and fill in your keys:

   ```ini
   ENVIRONMENT=development
   CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

   # --- AI Provider API Keys ---
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   GEMINI_API_KEY=AIzaSy_your_actual_gemini_api_key_here

   # --- Model Configurations ---
   GROQ_TUTOR_MODEL=qwen/qwen3.8-27b
   GROQ_QUIZ_MODEL=qwen/qwen3.8-27b
   GEMINI_MODEL=gemini-1.5-flash

   # --- System Parameters ---
   RATE_LIMIT_PER_MINUTE=20
   MAX_QUESTION_CHARS=500
   DATABASE_URL=sqlite:///./prismed.db
   ```

---

## 5. Backend Setup (FastAPI & Python)

### Step 5.1: Create a Virtual Environment (Recommended)

```bash
# Windows:
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate
```

### Step 5.2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5.3: Start the FastAPI Backend Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend server is now running at **`http://localhost:8000`**.
You can verify the backend health check by visiting [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) in your browser. You should receive:
```json
{"status":"healthy","service":"PrismEd API","version":"3.0.0", ...}
```

---

## 6. Frontend Setup (React 19 & Vite)

Open a **new terminal window** (keep the backend server running in the first terminal).

### Step 6.1: Install Node Dependencies

```bash
cd prism-ed
npm install
```

### Step 6.2: Start the Vite Development Server

```bash
npm run dev
```

The terminal will display:
```
  VITE v8.1.5 ready in ~300 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://...
```

Open **`http://localhost:5173`** in your browser to launch the application.

---

## 7. Verifying the Installation

To verify that your environment, 3D model assets, and AI pipelines are configured properly, run the automated test suite and content validator:

### A. Run Content & Schema Validator
```bash
python scripts/validate_content.py
```
*Expected output:* `Content validation completed successfully! [ALL 22 TOPICS GREEN]`

### B. Run Pytest Test Suite
```bash
python -m pytest tests/
```
*Expected output:* `22 passed in ~2.5s (100% passing)`

---

## 8. Exploring PrismEd Features

### 1. Interactive 3D Specimens & Hotspots
- Navigate to any topic from the homepage or `/showcase` gallery (e.g. **Circuit Board**, **Space Suit**, **B+ Tree Indexing**, or **Compiler Pipeline**).
- Click and drag to orbit in 3D, scroll to zoom, or right-click to pan.
- Click any glowing hotspot pin to select that component, inspect its physical function, and view its governing mathematical equations.

### 2. Grounded AI Tutor
- Located in the right-hand panel of each specimen page.
- **One-Click Ask:** Click the gold **"Ask"** button (or press `Enter`) to submit the suggested question immediately.
- **Custom Questions:** Type any engineering question in the input box (e.g. *"Why is this dielectric material chosen?"* or *"How does register allocation avoid spills?"*) and click **Ask**.
- The response will stream live directly underneath the input box in the **Tutor Response** card.

### 3. Optical Diagram Scanner
- Navigate to **Scanner** in the navigation bar (`/scan`).
- Point your webcam or upload a diagram to match against verified textbook diagrams via OpenCV SIFT keypoint extraction and RANSAC homography estimation.

### 4. Interactive Knowledge Quizzes
- Click **"Take Quiz"** on any topic page to test your engineering mastery with real-time feedback and distractor explanations.

---

## 9. Troubleshooting

### Port Already in Use
- **Port 8000 (Backend):** Run on another port:
  ```bash
  python -m uvicorn app.main:app --port 8001
  ```
  *(Remember to update `VITE_API_URL` or frontend proxy accordingly).*
- **Port 5173 (Frontend):** Vite automatically falls back to port `5174` or `5175` if `5173` is busy.

### "The tutor is unavailable right now" (503 Error)
- Check that your `GROQ_API_KEY` or `GEMINI_API_KEY` is pasted correctly into `app/.env` without surrounding quotes or whitespace.
- Test endpoint health directly: `http://localhost:8000/api/v1/health`.

### 3D Models Taking Long to Load
- All models are optimized glTF 2.0 binaries (`.glb`) stored under `public/models/`. Modern browsers cache them automatically after the initial load.
