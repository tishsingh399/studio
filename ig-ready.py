#!/usr/bin/env python3
"""Turn a phone photo of a print or block into a 1080x1350 Instagram image on a paper mat.

  python3 ig-ready.py photo.jpg out.jpg                 whole photo
  python3 ig-ready.py photo.jpg out.jpg x0 y0 x1 y1     crop to the piece first (pixels)
  python3 ig-ready.py --test                            self-check

Same mat, margin and shadow every time, so the feed reads as one body of work.
Needs Pillow: pip install pillow
"""
import sys
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

W, H, MARGIN = 1080, 1350, 90
PAPER = (244, 240, 232)  # warm off-white, close to printmaking paper


def ig_ready(src, box=None):
    im = ImageOps.exif_transpose(src).convert("RGB")
    if box:
        im = im.crop(box)
    im = ImageOps.autocontrast(im, cutoff=0.5, preserve_tone=True)  # lift flat phone light without a colour cast
    im = ImageEnhance.Color(im).enhance(1.06)
    s = min((W - 2 * MARGIN) / im.width, (H - 2 * MARGIN) / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    x, y = (W - im.width) // 2, (H - im.height) // 2
    out = Image.new("RGB", (W, H), PAPER)
    shadow = Image.new("L", (W, H), 0)
    shadow.paste(70, (x + 6, y + 10, x + im.width + 6, y + im.height + 10))
    out.paste((60, 50, 40), (0, 0), shadow.filter(ImageFilter.GaussianBlur(14)))
    out.paste(im, (x, y))
    return out


def test():
    out = ig_ready(Image.new("RGB", (665, 1182), (120, 30, 40)), (20, 100, 650, 1100))
    assert out.size == (W, H)
    assert out.getpixel((5, 5)) == PAPER                  # mat stays clean at the corner
    assert out.getpixel((W // 2, H // 2)) != PAPER        # piece sits in the middle
    print("ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--test"]:
        test()
    elif len(a) in (2, 6):
        box = tuple(int(v) for v in a[2:]) or None
        ig_ready(Image.open(a[0]), box).save(a[1], quality=92)
        print(f"saved {a[1]}")
    else:
        sys.exit(__doc__)
