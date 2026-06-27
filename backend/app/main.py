"""Second Voice backend - FastAPI application entrypoint."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config, tts
from .db import init_db
from .routers import board, compose, speak
from .seed import seed_if_empty

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("second_voice")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_if_empty()
    tts.warm()
    logger.info("Second Voice backend ready")
    yield


app = FastAPI(title="Second Voice API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(board.router)
app.include_router(compose.router)
app.include_router(speak.router)


@app.get("/api/health")
def health() -> dict:
    return {
        "ok": True,
        "tts_available": tts.model_files_present(),
        "gemini": bool(config.GEMINI_API_KEY),
    }
