# Daily GitHub snapshots

This is Koushoo's profile repository and a small VPS automation project. It saves one dated snapshot of public GitHub repository data each UTC day, along with a static SVG for the profile. It does not backdate commits, create empty commits, or invent contribution numbers.

Based on [Antonis Loukis's minimal-github-stats](https://github.com/antonisloukis/minimal-github-stats), commit `babe10a5d2debf8d09ef0ae56d161488b0bb42c5`. The MIT license, source history, original generator, tests, and original README are retained. `scripts/daily.py` reuses its HTML escaping helper and adds a separate public REST collector and window-style renderer. The original GraphQL generator remains available separately.

## Changes

- Public API collection works without a token; follows repository pagination and excludes private data.
- Stars/forks are counted for original public repos only. Language is the repository's primary language, not a claim about the author's skill or code ownership.
- One immutable snapshot per UTC date. A repeat run reuses it and makes no extra commit.
- OS locking prevents overlapping jobs and releases automatically after process termination.
- Atomic file replacement avoids half-written output. API failure preserves the last successful output.
- Bounded API retries, timeout limits, and errors that do not print tokens.
- Publishing checks the expected origin, main branch, and clean checkout before doing anything. It only stages `data/daily/<date>.json` and `assets/github-stats.svg`. It fast-forwards from the remote and never force-pushes.
- A committed snapshot whose push fails is retried on the next run. Unexpected local edits stop publishing for review.
- Daily systemd timer, catch-up after downtime, bounded service retries, dedicated unprivileged service account.
- Original scheduled GitHub Actions updater is retained as an inactive example to avoid competing writers.

## Local use

Python 3.10+ and Git are required. No pip install is needed.

```console
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/daily.py --output work/preview
```

The preview reads the real public API and writes only into `work/preview`. Unit tests use simulated API responses and a temporary bare Git repository; they do not publish test data.

```console
python scripts/daily.py --publish
```

Publishing requires a clean `main` checkout whose origin is `Koushoo/Koushoo`, with Git authentication configured. The default author address is the account's GitHub noreply address. GitHub's own attribution rules still apply; graph updates can be delayed. A failure to run or publish means a day may have no contribution.

## VPS

The deployment directory is `/opt/koushoo-profile`. Run as `profilebot` with Git configured to use a repository-specific SSH deploy key, or provide a fine-grained PAT in `/etc/koushoo-profile.env`. Token access should be restricted to Contents read/write for this repository. Never commit tokens or private keys.

The unit files in `deploy/` run at 03:15 UTC (08:45 India time), with up to two minutes of jitter. The service retries on failure every 15 minutes, with a four-start limit over two hours. It does not expose a network port. `Persistent=true` catches up once after downtime; it cannot recreate missed days.

```console
sudo systemctl start koushoo-profile.service
sudo systemctl status koushoo-profile.service
sudo systemctl list-timers koushoo-profile.timer
sudo journalctl -u koushoo-profile.service -n 30 --no-pager
```

To stop scheduling: `sudo systemctl disable --now koushoo-profile.timer`.

Do not edit the managed checkout directly while it is scheduled. Deploy reviewed commits from the repository; unexpected edits intentionally stop the publisher instead of discarding your work. A non-fast-forward push is not overwritten; resolve concurrent changes before retrying.
