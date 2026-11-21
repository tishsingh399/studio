# The atelier, a 360° room

2026-11-21 · capture: `capture.jpg` (a still) · full panorama: `panorama.webp` (3548 × 1774)
Write-up: none yet

![The atelier: a desk with a monitor, paper wireframes and pinned chair sketches](capture.jpg)

## What it is
My portfolio as a room you can stand in. You land at a desk, drag to turn around, and the things in the room open the sections of the site: design systems, case studies, AI work, about. It's one painted panorama drawn by a single WebGL shader, with HTML hotspots on top. Without JavaScript or WebGL it falls back to a plain list of the same links. Keyboard works and reduced motion is respected.

## The one thing I learned
A 360° panorama is a flat 2:1 image wrapped into a circle, so its left and right edges have to match or you see a hard seam every time you spin past the back wall. I fixed it by blending the outer band of pixels on each edge toward the other side.

## How to run
The room viewer is part of my portfolio site, not this repo. The panorama is here as `panorama.webp`, and the seam fix works on it or any other 2:1 image:

```bash
pip install pillow
python3 room-seam.py my-panorama.jpg my-panorama-wrapped.webp 40
```

The last number is how many pixels to blend on each edge (40 if you leave it off).
