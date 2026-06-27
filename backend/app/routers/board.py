"""Board, tiles, and usage-tracking endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..db import get_conn
from ..schemas import BoardResponse, Category, Tile, TileCreate, UseResponse

router = APIRouter(prefix="/api", tags=["board"])


@router.get("/board", response_model=BoardResponse)
def get_board() -> BoardResponse:
    with get_conn() as conn:
        cats = conn.execute(
            "SELECT id, name, icon, sort_order FROM categories ORDER BY sort_order, id"
        ).fetchall()
        tiles = conn.execute(
            "SELECT id, label, symbol, category_id, use_count, is_quick FROM tiles "
            "ORDER BY use_count DESC, label ASC"
        ).fetchall()
    return BoardResponse(
        categories=[Category(**dict(c)) for c in cats],
        tiles=[Tile(**{**dict(t), "is_quick": bool(t["is_quick"])}) for t in tiles],
    )


@router.post("/tiles/{tile_id}/use", response_model=UseResponse)
def use_tile(tile_id: int) -> UseResponse:
    with get_conn() as conn:
        row = conn.execute("SELECT id FROM tiles WHERE id = ?", (tile_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="tile not found")
        conn.execute(
            "UPDATE tiles SET use_count = use_count + 1 WHERE id = ?", (tile_id,)
        )
        new = conn.execute(
            "SELECT use_count FROM tiles WHERE id = ?", (tile_id,)
        ).fetchone()
    return UseResponse(id=tile_id, use_count=new["use_count"])


@router.post("/tiles", response_model=Tile, status_code=201)
def create_tile(payload: TileCreate) -> Tile:
    with get_conn() as conn:
        cat = conn.execute(
            "SELECT id FROM categories WHERE id = ?", (payload.category_id,)
        ).fetchone()
        if not cat:
            raise HTTPException(status_code=400, detail="category not found")
        cur = conn.execute(
            "INSERT INTO tiles (label, symbol, category_id, is_quick) "
            "VALUES (?, ?, ?, ?)",
            (payload.label, payload.symbol, payload.category_id, int(payload.is_quick)),
        )
        tid = cur.lastrowid
        row = conn.execute(
            "SELECT id, label, symbol, category_id, use_count, is_quick FROM tiles "
            "WHERE id = ?",
            (tid,),
        ).fetchone()
    return Tile(**{**dict(row), "is_quick": bool(row["is_quick"])})


@router.delete("/tiles/{tile_id}")
def delete_tile(tile_id: int) -> dict:
    with get_conn() as conn:
        conn.execute("DELETE FROM tiles WHERE id = ?", (tile_id,))
    return {"ok": True}
