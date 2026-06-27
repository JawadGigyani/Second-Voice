"""Gemini-powered keyword-to-sentence composition (free tier), with a safe fallback."""
from __future__ import annotations

import logging
import re

from . import config

logger = logging.getLogger("second_voice.gemini")

_client = None
_client_failed = False

_PROMPT = (
    "You help a non-speaking person communicate using an AAC board. "
    "Combine the following word tiles into ONE short, natural, polite first-person "
    "sentence that keeps their intent. Do not add new ideas. "
    "Output ONLY the sentence, no quotes, no explanation.\n"
    "Tiles: {tiles}"
)


def _join_fallback(tiles: list[str]) -> str:
    text = " ".join(t.strip() for t in tiles if t and t.strip())
    if not text:
        return ""
    text = text[0].upper() + text[1:]
    if text[-1] not in ".!?":
        text += "."
    return text


def _get_client():
    global _client, _client_failed
    if _client is not None or _client_failed:
        return _client
    if not config.GEMINI_API_KEY:
        _client_failed = True
        return None
    try:
        from google import genai

        _client = genai.Client(api_key=config.GEMINI_API_KEY)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Gemini client init failed: %s", exc)
        _client_failed = True
        _client = None
    return _client


def compose(tiles: list[str]) -> tuple[str, str]:
    """Return (sentence, source) where source is 'gemini' or 'fallback'."""
    tiles = [t.strip() for t in tiles if t and t.strip()]
    if not tiles:
        return "", "fallback"

    client = _get_client()
    if client is None:
        return _join_fallback(tiles), "fallback"

    try:
        from google.genai import types

        resp = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=_PROMPT.format(tiles=", ".join(tiles)),
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=120,
                # Disable "thinking" so the short answer isn't starved of tokens.
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                http_options=types.HttpOptions(
                    timeout=int(config.GEMINI_TIMEOUT_S * 1000)
                ),
            ),
        )
        text = (resp.text or "").strip()
        text = re.sub(r"^[\"']|[\"']$", "", text).strip()
        if text:
            return text, "gemini"
    except Exception as exc:  # noqa: BLE001
        logger.warning("Gemini compose failed, using fallback: %s", exc)

    return _join_fallback(tiles), "fallback"
