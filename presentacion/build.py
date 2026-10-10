#!/usr/bin/env python3
"""Embebe las figuras de defensa.src.html como data URI y escribe defensa.html."""
import base64
import mimetypes
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "defensa.src.html"
OUT = HERE / "defensa.html"


def inline(match: re.Match) -> str:
    rel = match.group(1)
    path = (HERE / rel).resolve()
    if not path.exists():
        raise SystemExit(f"falta la figura: {rel}")
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'src="data:{mime};base64,{data}"'


html = SRC.read_text(encoding="utf-8")
html, n = re.subn(r'src="(\.\./[^"]+)"', inline, html)
OUT.write_text(html, encoding="utf-8")
print(f"{OUT.name}: {n} figuras embebidas, {OUT.stat().st_size / 1024:.0f} KB")
