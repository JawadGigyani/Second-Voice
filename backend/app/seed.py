"""Seed default AAC categories and tiles (idempotent)."""
from __future__ import annotations

from .db import get_conn

# (category name, icon emoji, [(label, symbol), ...])
CATEGORIES: list[tuple[str, str, list[tuple[str, str]]]] = [
    ("Quick", "\u26a1", [
        ("Yes", "\u2705"), ("No", "\u274c"), ("Please", "\U0001f64f"),
        ("Thank you", "\U0001f495"), ("I need help", "\U0001f198"),
        ("Stop", "\u270b"), ("More", "\u2795"), ("All done", "\U0001f3c1"),
        ("Wait", "\u23f3"), ("Maybe", "\U0001f937"),
    ]),
    ("Needs", "\U0001f6df", [
        ("I want", "\U0001f449"), ("I need", "\u2757"), ("water", "\U0001f4a7"),
        ("food", "\U0001f37d\ufe0f"), ("bathroom", "\U0001f6bd"), ("rest", "\U0001f6cf\ufe0f"),
        ("medicine", "\U0001f48a"), ("a break", "\u23f8\ufe0f"), ("my phone", "\U0001f4f1"),
        ("help", "\U0001f91d"),
    ]),
    ("Feelings", "\U0001f60a", [
        ("happy", "\U0001f604"), ("sad", "\U0001f622"), ("tired", "\U0001f634"),
        ("hungry", "\U0001f37d\ufe0f"), ("thirsty", "\U0001f964"), ("sick", "\U0001f912"),
        ("scared", "\U0001f628"), ("angry", "\U0001f620"), ("excited", "\U0001f929"),
        ("okay", "\U0001f44c"),
    ]),
    ("People", "\U0001f465", [
        ("I", "\U0001f9d1"), ("you", "\U0001f9d1\u200d\U0001f91d\u200d\U0001f9d1"),
        ("Mom", "\U0001f469"), ("Dad", "\U0001f468"), ("friend", "\U0001f46b"),
        ("teacher", "\U0001f9d1\u200d\U0001f3eb"), ("doctor", "\U0001f9d1\u200d\u2695\ufe0f"),
        ("nurse", "\U0001f3e5"), ("family", "\U0001f46a"), ("someone", "\U0001f464"),
    ]),
    ("Food", "\U0001f34e", [
        ("apple", "\U0001f34e"), ("bread", "\U0001f35e"), ("milk", "\U0001f95b"),
        ("juice", "\U0001f9c3"), ("snack", "\U0001f36a"), ("pizza", "\U0001f355"),
        ("rice", "\U0001f35a"), ("banana", "\U0001f34c"), ("candy", "\U0001f36c"),
        ("coffee", "\u2615"),
    ]),
    ("Places", "\U0001f3e0", [
        ("home", "\U0001f3e0"), ("school", "\U0001f3eb"), ("outside", "\U0001f333"),
        ("store", "\U0001f3ea"), ("park", "\U0001f3de\ufe0f"), ("car", "\U0001f697"),
        ("here", "\U0001f4cd"), ("there", "\u27a1\ufe0f"), ("bedroom", "\U0001f6cf\ufe0f"),
        ("hospital", "\U0001f3e5"),
    ]),
    ("Actions", "\U0001f3c3", [
        ("go", "\U0001f6b6"), ("come", "\U0001f44b"), ("eat", "\U0001f374"),
        ("drink", "\U0001f964"), ("play", "\U0001f3ae"), ("sleep", "\U0001f4a4"),
        ("look", "\U0001f440"), ("listen", "\U0001f442"), ("open", "\U0001f513"),
        ("give me", "\U0001f932"),
    ]),
]


def seed_if_empty() -> None:
    with get_conn() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM categories").fetchone()["c"]
        if count:
            return
        for order, (name, icon, tiles) in enumerate(CATEGORIES):
            cur = conn.execute(
                "INSERT INTO categories (name, icon, sort_order) VALUES (?, ?, ?)",
                (name, icon, order),
            )
            cat_id = cur.lastrowid
            is_quick = 1 if name == "Quick" else 0
            for label, symbol in tiles:
                conn.execute(
                    "INSERT INTO tiles (label, symbol, category_id, is_quick) "
                    "VALUES (?, ?, ?, ?)",
                    (label, symbol, cat_id, is_quick),
                )
