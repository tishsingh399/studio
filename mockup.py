#!/usr/bin/env python3
"""Place a print photo into a mockup scene's blank area (a frame window, a blank sheet).

  python3 mockup.py mockups/scenes/frame-wall.png builds/hummingbird-print/fixed.jpg builds/hummingbird-print/mockup-frame.jpg
  python3 mockup.py --test

The blank area is found by flood-filling from the middle of the scene, so scenes must be
front-facing with the blank area over the centre. The print is only scaled to fit (contain):
never warped, recoloured or cropped.
Needs Pillow: pip install pillow
"""
import sys
from PIL import Image, ImageDraw

MARK = (255, 0, 255)


def blank_area(scene, tolerance=24):
    probe = scene.copy()
    ImageDraw.floodfill(probe, (scene.width // 2, scene.height // 2), MARK, thresh=tolerance)
    mask = Image.new("L", scene.size, 0)
    px, mp = probe.load(), mask.load()
    for y in range(scene.height):
        for x in range(scene.width):
            if px[x, y] == MARK:
                mp[x, y] = 255
    return mask.getbbox()


def place(scene, art, inset=0.04):
    scene = scene.convert("RGB")
    x0, y0, x1, y1 = blank_area(scene)
    # sanity: the area must be a real chunk of the scene, not a leak or a speck
    area = (x1 - x0) * (y1 - y0) / (scene.width * scene.height)
    assert 0.05 < area < 0.8, f"blank area looks wrong ({area:.0%} of scene); check the scene"
    bw, bh = (x1 - x0) * (1 - 2 * inset), (y1 - y0) * (1 - 2 * inset)
    s = min(bw / art.width, bh / art.height)
    art = art.convert("RGB").resize((round(art.width * s), round(art.height * s)), Image.LANCZOS)
    out = scene.copy()
    out.paste(art, (x0 + (x1 - x0 - art.width) // 2, y0 + (y1 - y0 - art.height) // 2))
    return out


def test():
    scene = Image.new("RGB", (400, 500), (120, 90, 60))
    ImageDraw.Draw(scene).rectangle((100, 120, 300, 380), fill=(250, 250, 248))
    assert blank_area(scene) == (100, 120, 301, 381)
    out = place(scene, Image.new("RGB", (50, 100), (20, 20, 20)))
    assert out.getpixel((200, 250)) == (20, 20, 20)   # art in the middle of the blank area
    assert out.getpixel((10, 10)) == (120, 90, 60)    # scene untouched outside it
    print("ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--test"]:
        test()
    elif len(a) == 3:
        place(Image.open(a[0]), Image.open(a[1])).save(a[2], quality=92)
        print(f"saved {a[2]}")
    else:
        sys.exit(__doc__)
