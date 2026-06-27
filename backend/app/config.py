"""Application configuration loaded from environment / .env."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load the workspace-root .env (two levels up: backend/ -> second-voice/ -> repo root)
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BACKEND_DIR.parent
REPO_ROOT = PROJECT_DIR.parent

for candidate in (BACKEND_DIR / ".env", PROJECT_DIR / ".env", REPO_ROOT / ".env"):
    if candidate.exists():
        load_dotenv(candidate, override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "").strip()

# Data + model locations
DATA_DIR = Path(os.getenv("SV_DATA_DIR", BACKEND_DIR / "data"))
MODELS_DIR = Path(os.getenv("SV_MODELS_DIR", BACKEND_DIR / "models"))
DB_PATH = Path(os.getenv("SV_DB_PATH", DATA_DIR / "second_voice.db"))

KOKORO_MODEL = MODELS_DIR / "kokoro-v1.0.onnx"
KOKORO_VOICES = MODELS_DIR / "voices-v1.0.bin"

DEFAULT_VOICE = os.getenv("SV_DEFAULT_VOICE", "af_heart")
DEFAULT_SPEED = float(os.getenv("SV_DEFAULT_SPEED", "1.0"))

GEMINI_MODEL = os.getenv("SV_GEMINI_MODEL", "gemini-2.5-flash")
# Gemini enforces a minimum 10s request deadline; this is a max, not a fixed wait.
GEMINI_TIMEOUT_S = float(os.getenv("SV_GEMINI_TIMEOUT_S", "15.0"))

# CORS: comma-separated origins; "*" allows all (fine for the hackathon demo)
ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("SV_ALLOWED_ORIGINS", "*").split(",") if o.strip()
]

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
