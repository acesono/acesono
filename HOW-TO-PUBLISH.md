# Publishing to github.com/acesono/acesono

This is your **profile README** repo (repo name == username), so `README.md`
renders on your GitHub profile page.

```bash
cd "C:\Users\aceso\Desktop\acesono"
git add -A
git commit -m "Redesign profile README"
git push origin main
```

## Notes on the cards

- **Stats / top languages** use the community mirror
  `readme-stats-nu-nine.vercel.app` — the official
  `github-readme-stats.vercel.app` deployment is currently paused (HTTP 503),
  which is why the old cards showed broken images. If the mirror ever goes
  down, swap the host back to `github-readme-stats.vercel.app` or to another
  self-hosted instance; the query strings are identical.
- **Streak** uses `streak-stats.demolab.com`.
- **Banner / typing text** use `capsule-render.vercel.app` and
  `readme-typing-svg.demolab.com`.
- Accent colour is `#00F5D4` on a `#0d1117` background — change both
  everywhere if you want a different palette.

## Regenerating the panda

`assets/panda.svg` is built from the ANSI art in `tools/panda.txt`:

```bash
python tools/gen_panda.py
```

Edit `TITLE` near the top of `tools/gen_panda.py` to change the terminal
title-bar text. There is no speech bubble any more — the script renders the
art only.
