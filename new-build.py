#!/usr/bin/env python3
"""Scaffold a build folder, then draft its post.md from the README.

  python3 new-build.py <slug>           1st run: creates builds/<slug>/README.md to fill in
                                        2nd run: drafts builds/<slug>/post.md from that README
  python3 new-build.py <slug> --force   redraft post.md even if it exists
  python3 new-build.py --test           self-check
"""
import re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).parent / "builds"
SECTIONS = ("What it is", "The one thing I learned", "How to run")
README = """# {title}

{date} · capture: `capture.jpg` (a still) or `capture.mp4` (10 to 15 seconds)
Write-up: none yet (add the Medium link here when there is one)

## What it is
TODO

## The one thing I learned
TODO

## How to run
TODO
"""
POST = """# Post drafts: {title}

Starting points pulled from the README. Rewrite in your own words, or ask Claude to redraft them with the tina-writing skill. Nothing here is posted automatically.

## Lettering + lino account

{what}

{learned}

Notes and code are in my studio repo, link in bio.

## UX with intent

{what}

The one thing I learned: {learned_lc}

How it works, and how to run it yourself, is in my studio repo. Link in bio.
"""


def sections(text):
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    found = {k: v.strip() for k, v in zip(parts[1::2], parts[2::2])}
    missing = [s for s in SECTIONS if found.get(s, "TODO") in ("", "TODO")]
    return found, missing


def run(slug, force=False, root=ROOT, today="today"):
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit(f"slug must be lowercase-with-dashes, got {slug!r}")
    d = root / slug
    readme, post = d / "README.md", d / "post.md"
    if not readme.exists():
        d.mkdir(parents=True, exist_ok=True)
        readme.write_text(README.format(title=slug.replace("-", " ").capitalize(), date=today))
        return f"created {readme}. Fill it in, add a capture, then run again."
    found, missing = sections(readme.read_text())
    if missing:
        sys.exit(f"fill these README sections first: {', '.join(missing)}")
    if post.exists() and not force:  # never clobber captions Tina has edited
        sys.exit(f"{post} exists; pass --force to redraft it")
    title = readme.read_text().splitlines()[0].lstrip("# ").strip()
    learned = found["The one thing I learned"]
    post.write_text(POST.format(title=title, what=found["What it is"], learned=learned,
                                learned_lc=learned[:1].lower() + learned[1:]))
    return f"drafted {post}"


def test():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        assert "created" in run("demo", root=root)
        for bad in ("Demo", "../x"):
            try: run(bad, root=root); raise AssertionError(bad)
            except SystemExit: pass
        try: run("demo", root=root); raise AssertionError("drafted from empty README")
        except SystemExit as e: assert "What it is" in str(e)
        r = root / "demo" / "README.md"
        r.write_text(r.read_text().replace("TODO", "Seams matter.", 3))
        assert "drafted" in run("demo", root=root)
        assert "seams matter." in (root / "demo" / "post.md").read_text()
        try: run("demo", root=root); raise AssertionError("overwrote post.md")
        except SystemExit: pass
        assert "drafted" in run("demo", force=True, root=root)
    print("ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--test"]:
        test()
    elif args and not args[0].startswith("-"):
        from datetime import date
        print(run(args[0], force="--force" in args, today=date.today().isoformat()))
    else:
        sys.exit(__doc__)
