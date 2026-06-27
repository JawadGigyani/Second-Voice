"""Download Kokoro ONNX model + voices into backend/models/.

Usage: python scripts/download_models.py
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

BASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
FILES = {
    "kokoro-v1.0.onnx": BASE + "kokoro-v1.0.onnx",
    "voices-v1.0.bin": BASE + "voices-v1.0.bin",
}

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


def _progress(block: int, block_size: int, total: int) -> None:
    if total > 0:
        pct = min(100, block * block_size * 100 // total)
        sys.stdout.write(f"\r  {pct:3d}%")
        sys.stdout.flush()


def main() -> int:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        dest = MODELS_DIR / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"[skip] {name} already present ({dest.stat().st_size} bytes)")
            continue
        print(f"[download] {name}")
        urllib.request.urlretrieve(url, dest, _progress)
        print(f"\n[done] {name} -> {dest.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
