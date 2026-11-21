#!/usr/bin/env python3
"""Feather the left/right seam of an equirectangular panorama so it wraps in a 360 viewer.

Usage: python3 scripts/room-seam.py <in-image> <out.webp> [band_px]
Blends the outer band on each edge toward the opposite edge, so column 0 and column w-1 match.
"""
import sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
band = int(sys.argv[3]) if len(sys.argv) > 3 else 40
im = Image.open(src).convert("RGB")
w, h = im.size
assert abs(w - 2 * h) <= 2, f"not 2:1 equirectangular: {w}x{h}"
p = im.load()
orig = im.copy().load()
for x in range(band):
    t = 0.5 * (1 - x / band)  # 0.5 at the edge (meet in the middle) -> 0 inside
    for y in range(h):
        L, Rr = orig[x, y], orig[w - 1 - x, y]
        p[x, y] = tuple(round(a * (1 - t) + b * t) for a, b in zip(L, Rr))
        p[w - 1 - x, y] = tuple(round(b * (1 - t) + a * t) for a, b in zip(L, Rr))
im.save(out, "WEBP", quality=88, method=6)
q = Image.open(out).convert("RGB").load()
seam = sum(sum(abs(a - b) for a, b in zip(q[0, y], q[w - 1, y])) / 3 for y in range(h)) / h
print(f"{out}: {w}x{h}, seam diff after = {seam:.1f}")
assert seam < 4, "seam still visible"
