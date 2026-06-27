"""Pydantic request/response models."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Tile(BaseModel):
    id: int
    label: str
    symbol: str
    category_id: int
    use_count: int
    is_quick: bool


class Category(BaseModel):
    id: int
    name: str
    icon: str
    sort_order: int


class BoardResponse(BaseModel):
    categories: list[Category]
    tiles: list[Tile]


class ComposeRequest(BaseModel):
    tiles: list[str] = Field(default_factory=list)


class ComposeResponse(BaseModel):
    text: str
    source: str  # "gemini" or "fallback"


class SpeakRequest(BaseModel):
    text: str
    voice: str | None = None
    speed: float | None = None


class UseResponse(BaseModel):
    id: int
    use_count: int


class TileCreate(BaseModel):
    label: str
    symbol: str = ""
    category_id: int
    is_quick: bool = False
