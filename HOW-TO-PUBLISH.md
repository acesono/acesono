# Publishing this to github.com/acesono/acesono

This is your **profile README** repo (repo name == username), so its README.md
shows on your GitHub profile page.

```bash
cd "C:\Users\aceso\Desktop\github-profile"
git init
git add .
git commit -m "Redesign profile README with cowsay panda"
git branch -M main
git remote add origin https://github.com/acesono/acesono.git
git push -u origin main --force
```

`--force` overwrites what's there now. Drop it if you want to merge instead.

## Regenerating the panda

Edit the `MSG` list near the top of `tools/gen_panda.py`, then:

```bash
python tools/gen_panda.py
```

That rewrites `assets/panda.svg` from `tools/panda.txt`.
