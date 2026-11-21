# Studio

Things I make, one folder each, with what I learned making them. Creative code, 3D experiments, and the occasional bridge to my lettering and lino work. This is separate from my portfolio; longer write-ups go on Medium and get linked here.

## Builds

| Build | What I learned | Write-up |
|---|---|---|
| [The atelier, a 360° room](builds/atelier-360/) | A panorama's left and right edges must match, or the seam shows every time you turn | soon |
| [Marble Loop](builds/marble-loop/) | Each piece has to start a little lower than the last, or marbles stall on invisible lips | soon |
| [Tarot Stars](builds/tarot-stars/) | Head-on beats clever: the angled view hid the picture | soon |
| [Major Arcana](builds/major-arcana/) | Code-drawn art hits a ceiling; real illustration needs real art | soon |

## What's in a build folder

- `README.md`: what it is, the one thing I learned, how to run it
- `capture.jpg` or `capture.mp4`: a still, or a 10 to 15 second screen recording
- `post.md`: two caption drafts, one for my lettering + lino account and one for UX with intent
- any code you need to run it yourself
- a Medium link at the top of the README, once there's a write-up

## Adding a build

```bash
python3 new-build.py my-new-thing
```

That creates `builds/my-new-thing/README.md`. Fill in the three sections, drop in a capture, then run the same command again to draft `post.md` from the README. It won't overwrite a `post.md` you've edited unless you add `--force`.

Nothing posts automatically. [POSTING.md](POSTING.md) covers what auto-posting to Instagram would need and when it's worth it.

## License

Code is [MIT](LICENSE). The atelier panorama and the captures are mine. The Major Arcana card art is Pamela Colman Smith's 1909 deck, public domain.
