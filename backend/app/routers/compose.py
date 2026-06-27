"""Keyword-to-sentence composition endpoint."""
from __future__ import annotations

from fastapi import APIRouter

from ..gemini import compose as gemini_compose
from ..schemas import ComposeRequest, ComposeResponse

router = APIRouter(prefix="/api", tags=["compose"])


@router.post("/compose", response_model=ComposeResponse)
def compose(payload: ComposeRequest) -> ComposeResponse:
    text, source = gemini_compose(payload.tiles)
    return ComposeResponse(text=text, source=source)
