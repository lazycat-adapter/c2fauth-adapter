# 2FAuth LazyCat adapter

This repository packages stable GitHub releases of [2FAuth](https://github.com/Bubka/2FAuth) for the official LazyCat application store.

- Source tags are stable `vX.Y.Z` releases and use the matching `2fauth/2fauth:X.Y.Z` image.
- The existing application data path remains `/lzcapp/var/data`, mounted at `/2fauth`.
- `APP_KEY` is generated during installation and must be kept unchanged for upgrades.
- The workflow calls `lazycat-adapter/lazycat-action@v1` with organization secrets inherited through `secrets: inherit`.

Pushes and scheduled runs check only. Start a manual run with `dry-run` unchecked for image copy, LPK packaging, and review submission.
