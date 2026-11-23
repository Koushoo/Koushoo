"""Daily public GitHub snapshots. Standard library only; no empty commits."""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

from generate_stats import esc

ROOT = Path(__file__).resolve().parents[1]
LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?")


class Api:
    def __init__(self, token="", opener=urllib.request.urlopen, sleep=time.sleep):
        self.token, self.opener, self.sleep = token, opener, sleep

    def get(self, path):
        if not path.startswith("/users/"):
            raise ValueError("Only public user API endpoints are supported")
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "koushoo-daily-profile",
                   "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        for attempt in range(3):
            try:
                req = urllib.request.Request("https://api.github.com" + path, headers=headers)
                with self.opener(req, timeout=30) as response:
                    return json.load(response)
            except urllib.error.HTTPError as error:
                # Never log response bodies or authorization headers.
                if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise RuntimeError(f"GitHub HTTP {error.code}; no snapshot published") from None
                delay = min(60, max(1, int(error.headers.get("Retry-After", "2"))))
                self.sleep(delay * (attempt + 1))
            except (urllib.error.URLError, TimeoutError):
                if attempt == 2:
                    raise RuntimeError("GitHub connection failed; no snapshot published") from None
                self.sleep(2 ** attempt)
        raise RuntimeError("Unreachable retry state")


def collect(api, username, day):
    if not LOGIN.fullmatch(username):
        raise ValueError("Invalid GitHub username")
    profile = api.get(f"/users/{username}")
    if str(profile.get("login", "")).lower() != username.lower():
        raise ValueError("GitHub returned an unexpected account")
    repos = []
    for page in range(1, 101):
        batch = api.get(f"/users/{username}/repos?type=owner&sort=full_name&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Invalid repository response")
        repos.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise RuntimeError("Pagination safety limit exceeded")
    # The public /users/.../repos endpoint excludes private data.
    repos = [r for r in repos if not r.get("private", False)]
    original = [r for r in repos if not r.get("fork", False)]
    return {
        "schema_version": 1, "date_utc": day, "username": profile["login"],
        "scope": "public repositories; stars and forks exclude forked repositories",
        "public_repositories": len(repos), "original_repositories": len(original),
        "stars": sum(int(r["stargazers_count"]) for r in original),
        "forks": sum(int(r["forks_count"]) for r in original),
        "followers": int(profile["followers"]),
        "repositories": sorted([
            {"name": r["name"], "url": r["html_url"], "language": r.get("language"),
             "stars": int(r["stargazers_count"]), "fork": bool(r["fork"]),
             "archived": bool(r["archived"])} for r in repos
        ], key=lambda r: r["name"].lower()),
    }


def render(snapshot):
    metrics = [("Repositories", snapshot["public_repositories"]), ("Original projects", snapshot["original_repositories"]),
               ("Stars", snapshot["stars"]), ("Followers", snapshot["followers"])]
    cells = []
    for index, (label, value) in enumerate(metrics):
        x = 56 + index * 220
        cells.append(f'<text x="{x}" y="135" font-size="35" font-weight="600">{value}</text>'
                     f'<text x="{x}" y="169" font-size="15" fill="#6c6c75">{label}</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="960" height="240" viewBox="0 0 960 240" '
            'role="img" aria-labelledby="title desc">'
            f'<title id="title">{esc(snapshot["username"])} — public GitHub snapshot</title>'
            '<desc id="desc">Daily public repository statistics. Stars exclude forked repositories.</desc>'
            '<rect x="1" y="1" width="958" height="238" rx="16" fill="#f6f6f8" stroke="#d9d9df"/>'
            '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" fill="#242428">'
            '<circle cx="26" cy="26" r="5" fill="#ff5f57"/><circle cx="44" cy="26" r="5" fill="#febc2e"/>'
            '<circle cx="62" cy="26" r="5" fill="#28c840"/>'
            '<text x="480" y="31" text-anchor="middle" font-size="12" fill="#777780">github · daily snapshot</text>'
            '<path d="M1 51H959" stroke="#dedee4"/>' + ''.join(cells) +
            f'<text x="56" y="213" font-size="12" fill="#777780">Public data · {esc(snapshot["date_utc"])} UTC</text>'
            '</g></svg>\n')


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=".daily-", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locked(root):
    """OS advisory lock: automatically released if the process crashes."""
    root.mkdir(parents=True, exist_ok=True)
    path = root / ".daily.lock"
    with path.open("a+b") as handle:
        if path.stat().st_size == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise RuntimeError("Another daily run is already active") from None
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def git(root, *args, token="", check=True):
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GCM_INTERACTIVE"] = "never"
    if token:
        auth = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        env.update(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="http.https://github.com/.extraheader",
                   GIT_CONFIG_VALUE_0=f"Authorization: Basic {auth}")
    result = subprocess.run(["git", *args], cwd=root, env=env, text=True, capture_output=True, timeout=120)
    if check and result.returncode:
        # git errors can include remote URLs; don't print credentials or arbitrary stderr.
        raise RuntimeError(f"git {args[0]} failed (exit {result.returncode}); inspect the checkout")
    return result


def prepare_publish(root, username, repository, token):
    allowed = {f"https://github.com/{username}/{repository}.git", f"git@github.com:{username}/{repository}.git"}
    if git(root, "remote", "get-url", "origin").stdout.strip() not in allowed:
        raise RuntimeError("Origin does not match the configured account and repository")
    if git(root, "branch", "--show-current").stdout.strip() != "main":
        raise RuntimeError("Publishing requires the main branch")
    if git(root, "status", "--porcelain").stdout.strip():
        raise RuntimeError("Checkout has uncommitted files; preserve them before publishing")
    git(root, "fetch", "origin", "main", token=token)
    git(root, "merge", "--ff-only", "origin/main")


def run(root, username, api, now=None, publish=False, repository="Koushoo", token="", author_email=""):
    now = now or datetime.now(timezone.utc)
    day = now.astimezone(timezone.utc).date().isoformat()
    with locked(root):
        if publish:
            if not author_email:
                raise ValueError("An account-associated author email is required")
            prepare_publish(root, username, repository, token)
        target = root / "data" / "daily" / f"{day}.json"
        svg = root / "assets" / "github-stats.svg"
        if target.exists():
            existing = json.loads(target.read_text(encoding="utf-8"))
            if existing.get("username", "").lower() != username.lower() or existing.get("date_utc") != day:
                raise ValueError("Existing snapshot belongs to another account or date")
            snapshot = existing
        else:
            snapshot = collect(api, username, day)
        # Collect and render successfully before touching either managed output.
        content = render(snapshot)
        atomic_write(svg, content)
        if not target.exists():
            atomic_write(target, json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
        files = [target.relative_to(root).as_posix(), svg.relative_to(root).as_posix()]
        if publish:
            git(root, "add", "--", *files)
            if git(root, "diff", "--cached", "--quiet", check=False).returncode == 1:
                git(root, "-c", f"user.name={username}", "-c", f"user.email={author_email}",
                    "commit", "-m", f"Record public GitHub snapshot for {day}")
            # Also retries a previously committed but unpushed snapshot.
            git(root, "push", "origin", "main", token=token)
        return {"date_utc": day, "username": username, "files": files, "published": publish}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="Koushoo")
    parser.add_argument("--output", type=Path, default=ROOT)
    parser.add_argument("--publish", action="store_true", help="Commit managed outputs and push to origin/main")
    parser.add_argument("--repository", default="Koushoo")
    parser.add_argument("--author-email", default="192865284+Koushoo@users.noreply.github.com")
    args = parser.parse_args()
    try:
        token = os.environ.get("GITHUB_TOKEN", "").strip()
        result = run(args.output.resolve(), args.username, Api(token), publish=args.publish,
                     repository=args.repository, token=token, author_email=args.author_email)
        print(json.dumps(result))
        return 0
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Daily run failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
