"""Text-to-speech endpoint returning WAV audio."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from .. import tts
from ..schemas import SpeakRequest

router = APIRouter(prefix="/api", tags=["speak"])


@router.get("/voices")
def voices() -> dict:
    return {"voices": tts.AVAILABLE_VOICES, "available": tts.model_files_present()}


@router.post("/speak")
def speak(payload: SpeakRequest) -> Response:
    try:
        audio = tts.synth(payload.text, voice=payload.voice, speed=payload.speed)
    except tts.TTSUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return Response(content=audio, media_type="audio/wav")
