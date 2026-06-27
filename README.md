# 🗣️ Second Voice

An accessible, free, tap-to-speak **AAC** (augmentative & alternative communication) web app for non-verbal and autistic users. Tap picture tiles to build a sentence, let **Gemini** turn the tiles into a natural first-person sentence, and hear it spoken aloud with an on-device **kokoro-onnx** voice. A phrase bank learns what's used most and floats it to the top.

Built for the **Youth Code x AI** hackathon — Track 03 (*AI That Actually Helps People*). No GPU required. Everything runs on free tiers.

| Light | Dark / high-contrast |
|---|---|
| ![light](frontend/e2e/shots/board-light.png) | ![dark](frontend/e2e/shots/board-dark.png) |

## Features

- **Picture + text tile board** across 7 categories (Quick, Needs, Feelings, People, Food, Places, Actions).
- **Tap to speak** — quick replies ("Yes", "I need help") speak instantly; other tiles build a sentence.
- **Gemini composition** — turns tapped keyword tiles into one natural sentence (with a plain-join fallback if offline/over quota).
- **Natural voice on CPU** — kokoro-onnx (the same engine Voicebox bundles), 10 selectable voices, adjustable speed. No GPU, no API key.
- **Phrase bank** — SQLite tracks usage so the most-used tiles surface first.
- **Accessibility** — high-contrast theme, adjustable text size, **scanning mode** for single-switch access, large tap targets, ARIA labels.
- **PWA** — installable full-screen on a phone or tablet (the real AAC form factor).

## Architecture

```
frontend (React + Vite + TS + Tailwind, PWA)
   |  /api  (vite proxy in dev, nginx proxy in prod)
   v
backend (FastAPI)
   ├─ /api/board, /api/tiles/{id}/use   -> SQLite phrase bank
   ├─ /api/compose                       -> Gemini (free tier) + fallback
   └─ /api/speak                         -> kokoro-onnx TTS (CPU) -> WAV
```

## Local development

**Prerequisites:** Python 3.12+ and Node.js 22+.

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # Windows  (use: source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python scripts/download_models.py  # downloads kokoro model (~350 MB) into backend/models/
uvicorn app.main:app --reload --port 8000
```

Create a `.env` (in the repo root or `backend/`) with:

```
GEMINI_API_KEY=your-gemini-api-key
HUGGINGFACE_TOKEN=your-hf-token   # reserved for future cloning/OCR features
```

> Without `GEMINI_API_KEY` the app still works — it just joins the tiles into a sentence instead of using Gemini.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173  (proxies /api -> localhost:8000)
```

## Testing

- **Backend smoke test** (server must be running): `python backend/scripts/smoke_test.py`
- **Frontend E2E** (Playwright, dev server + backend must be running):
  ```bash
  cd frontend
  # PLAYWRIGHT_BROWSERS_PATH=0 keeps the browser inside node_modules (stable across runs)
  $env:PLAYWRIGHT_BROWSERS_PATH="0"; npx playwright install chromium   # first time only
  $env:PLAYWRIGHT_BROWSERS_PATH="0"; npx playwright test
  ```
  On macOS/Linux use `PLAYWRIGHT_BROWSERS_PATH=0 npx playwright test`.

## Deployment (DigitalOcean)

The app is fully containerized. On a droplet with Docker + Compose:

```bash
git clone <your-repo> && cd second-voice
cd backend && python scripts/download_models.py && cd ..   # fetch models into backend/models/
cp .env.example .env   # then fill in GEMINI_API_KEY
docker compose up -d --build
```

`web` (nginx) serves the built frontend on port 80 and proxies `/api` to the `backend` service, so there are no cross-origin issues. Use a 2 GB+ droplet so the ONNX runtime has headroom. Add HTTPS with Caddy or Certbot in front for a public URL.

## Tech & credits

- **kokoro-onnx** — CPU text-to-speech (Kokoro 82M), the engine also bundled by Voicebox.
- **Google Gemini** (free tier) — sentence composition.
- FastAPI · React · Vite · Tailwind · SQLite · Playwright.

## Roadmap (Phase 2)

Personal voice cloning (free HF Space), "read-the-world" OCR via Unlimited-OCR, speech-to-text, caregiver accounts + board editor, multilingual support, and offline mode. See the full plan in `.cursor/plans/`.
