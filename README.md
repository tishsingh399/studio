# Studio

Things I make, one folder each, with what I learned making them. Creative code, 3D experiments, and the occasional bridge to my lettering and lino work.

## Builds

| Build | What I learned |
|---|---|
| [The atelier, a 360° room](builds/atelier-360/) | A panorama's left and right edges must match, or the seam shows every time you turn |

## What's in a build folder

- `README.md`: what it is, the one thing I learned, how to run it
- `capture.jpg` or `capture.mp4`: a still, or a 10 to 15 second screen recording
- `post.md`: two caption drafts, one for my lettering + lino account and one for UX with intent
- any code you need to run it yourself

## Adding a build

```bash
python3 new-build.py my-new-thing
```

That creates `builds/my-new-thing/README.md`. Fill in the three sections, drop in a capture, then run the same command again to draft `post.md` from the README. It won't overwrite a `post.md` you've edited unless you add `--force`.

Nothing posts automatically. [POSTING.md](POSTING.md) covers what auto-posting to Instagram would need and when it's worth it.
