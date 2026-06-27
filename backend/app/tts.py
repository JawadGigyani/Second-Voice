"""Text-to-speech via kokoro-onnx (CPU, no GPU).

The Kokoro engine is the same model Voicebox bundles; here we use the lightweight
ONNX runtime build so it runs on a plain CPU. The model is loaded lazily and kept
warm for the process lifetime.
"""
from __future__ import annotations

import io
import logging
import threading

import numpy as np
import soundfile as sf

from . import config

logger = logging.getLogger("second_voice.tts")

_kokoro = None
_lock = threading.Lock()

# Voices shipped in voices-v1.0.bin (subset surfaced to the UI).
AVAILABLE_VOICES = [
    "af_heart", "af_bella", "af_nicole", "af_sarah", "af_sky",
    "am_adam", "am_michael", "bf_emma", "bf_isabella", "bm_george",
]


class TTSUnavailable(RuntimeError):
    """Raised when the TTS model is not available."""


def model_files_present() -> bool:
    return config.KOKORO_MODEL.exists() and config.KOKORO_VOICES.exists()


def _load():
    global _kokoro
    if _kokoro is not None:
        return _kokoro
    with _lock:
        if _kokoro is not None:
            return _kokoro
        if not model_files_present():
            raise TTSUnavailable(
                "Kokoro model files missing. Run scripts/download_models.py."
            )
        from kokoro_onnx import Kokoro  # imported lazily to speed startup

        logger.info("Loading Kokoro model from %s", config.KOKORO_MODEL)
        _kokoro = Kokoro(str(config.KOKORO_MODEL), str(config.KOKORO_VOICES))
        logger.info("Kokoro model loaded")
    return _kokoro


def warm() -> bool:
    """Eagerly load the model at startup. Returns True on success."""
    try:
        _load()
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("TTS warm-up skipped: %s", exc)
        return False


def synth(text: str, voice: str | None = None, speed: float | None = None) -> bytes:
    """Synthesize text to WAV bytes."""
    text = (text or "").strip()
    if not text:
        raise ValueError("text is empty")
    voice = voice or config.DEFAULT_VOICE
    if voice not in AVAILABLE_VOICES:
        voice = config.DEFAULT_VOICE
    speed = float(speed or config.DEFAULT_SPEED)
    speed = max(0.5, min(2.0, speed))

    kokoro = _load()
    samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
    samples = np.asarray(samples, dtype=np.float32)

    buf = io.BytesIO()
    sf.write(buf, samples, sample_rate, format="WAV", subtype="PCM_16")
    return buf.getvalue()
