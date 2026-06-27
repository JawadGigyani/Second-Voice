"""Smoke-test all Second Voice endpoints against a running server."""
from __future__ import annotations

import sys

import requests

BASE = "http://127.0.0.1:8000"


def main() -> int:
    ok = True

    h = requests.get(f"{BASE}/api/health", timeout=10).json()
    print("health:", h)
    ok &= h.get("ok") is True

    board = requests.get(f"{BASE}/api/board", timeout=10).json()
    n_cat = len(board["categories"])
    n_tiles = len(board["tiles"])
    print(f"board: {n_cat} categories, {n_tiles} tiles")
    ok &= n_cat >= 6 and n_tiles >= 60

    comp = requests.post(
        f"{BASE}/api/compose", json={"tiles": ["I want", "water"]}, timeout=30
    ).json()
    print("compose:", comp)
    ok &= bool(comp.get("text"))

    use = requests.post(f"{BASE}/api/tiles/1/use", timeout=10).json()
    print("use tile 1:", use)
    ok &= use.get("use_count", 0) >= 1

    r = requests.post(
        f"{BASE}/api/speak",
        json={"text": "Hello, I want some water please."},
        timeout=60,
    )
    print("speak:", r.status_code, r.headers.get("content-type"), len(r.content), "bytes")
    ok &= r.status_code == 200 and r.content[:4] == b"RIFF" and len(r.content) > 5000
    with open("scripts/_speak_sample.wav", "wb") as f:
        f.write(r.content)

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
