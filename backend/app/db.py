"""SQLite helpers for the Second Voice phrase bank."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator

from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    icon TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS tiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    symbol TEXT NOT NULL DEFAULT '',
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    use_count INTEGER NOT NULL DEFAULT 0,
    is_quick INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS phrases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    use_count INTEGER NOT NULL DEFAULT 0,
    last_used TEXT
);
CREATE INDEX IF NOT EXISTS idx_tiles_category ON tiles(category_id);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    conn = connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)
