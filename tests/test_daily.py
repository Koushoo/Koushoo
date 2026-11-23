import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from urllib.error import HTTPError, URLError
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import daily

NOW = datetime(2026, 11, 24, 10, tzinfo=timezone.utc)


def repository(name="example", fork=False):
    return {"name": name, "html_url": f"https://github.com/Koushoo/{name}", "language": "Python",
            "stargazers_count": 3, "forks_count": 2, "fork": fork, "archived": False}


class FakeApi:
    def __init__(self):
        self.calls = []

    def get(self, path):
        self.calls.append(path)
        if "/repos?" in path:
            return [repository(), repository("fork", True)]
        return {"login": "Koushoo", "followers": 4}


class DailyTests(unittest.TestCase):
    def test_collect_excludes_forks_from_star_totals(self):
        result = daily.collect(FakeApi(), "Koushoo", "2026-11-24")
        self.assertEqual((result["public_repositories"], result["original_repositories"], result["stars"]), (2, 1, 3))

    def test_pagination(self):
        api = FakeApi()
        def get(path):
            if "/repos?" not in path:
                return {"login": "Koushoo", "followers": 0}
            return [repository(str(i)) for i in range(100)] if path.endswith("&page=1") else [repository("last")]
        api.get = get
        self.assertEqual(daily.collect(api, "Koushoo", "2026-11-24")["public_repositories"], 101)

    def test_repeat_run_is_identical_and_does_not_refetch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            api = FakeApi()
            daily.run(root, "Koushoo", api, now=NOW)
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            daily.run(root, "Koushoo", api, now=NOW)
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            self.assertEqual(len(api.calls), 2)
            ET.fromstring((root / "assets/github-stats.svg").read_text())

    def test_next_day_creates_another_real_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            daily.run(root, "Koushoo", FakeApi(), now=NOW)
            daily.run(root, "Koushoo", FakeApi(), now=NOW.replace(day=25))
            self.assertEqual(len(list((root / "data/daily").glob("*.json"))), 2)

    def test_failure_preserves_previous_card_and_creates_no_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            daily.run(root, "Koushoo", FakeApi(), now=NOW)
            before = (root / "assets/github-stats.svg").read_bytes()
            with patch.object(FakeApi, "get", side_effect=RuntimeError("offline")):
                with self.assertRaises(RuntimeError):
                    daily.run(root, "Koushoo", FakeApi(), now=NOW.replace(day=25))
            self.assertEqual((root / "assets/github-stats.svg").read_bytes(), before)
            self.assertFalse((root / "data/daily/2026-11-25.json").exists())

    def test_lock_prevents_overlap(self):
        with tempfile.TemporaryDirectory() as temp:
            with daily.locked(Path(temp)):
                with self.assertRaises(RuntimeError):
                    with daily.locked(Path(temp)):
                        self.fail("Lock admitted overlapping runner")

    def test_username_validation_and_identity_mismatch(self):
        with self.assertRaises(ValueError):
            daily.collect(FakeApi(), "../bad", "2026-11-24")
        with self.assertRaises(ValueError):
            daily.collect(FakeApi(), "someone-else", "2026-11-24")

    def test_http_retries_and_token_not_in_error(self):
        calls = []
        def opener(req, timeout):
            calls.append(req)
            if len(calls) < 3:
                raise HTTPError(req.full_url, 503, "unavailable", {}, None)
            return io.BytesIO(b'{"login":"Koushoo"}')
        api = daily.Api("secret-test-only", opener=opener, sleep=lambda _: None)
        self.assertEqual(api.get("/users/Koushoo")["login"], "Koushoo")
        self.assertEqual(len(calls), 3)

    def test_auth_error_not_retried(self):
        def opener(req, timeout):
            raise HTTPError(req.full_url, 401, "secret-test-only", {}, None)
        with self.assertRaisesRegex(RuntimeError, "HTTP 401") as ctx:
            daily.Api("secret-test-only", opener=opener).get("/users/Koushoo")
        self.assertNotIn("secret-test-only", str(ctx.exception))

    def test_network_failure_is_bounded(self):
        with patch("daily.urllib.request.urlopen", side_effect=URLError("offline")) as op:
            with self.assertRaises(RuntimeError):
                daily.Api(opener=op, sleep=lambda _: None).get("/users/Koushoo")
        self.assertEqual(op.call_count, 3)

    def test_svg_escapes_account_text(self):
        snapshot = daily.collect(FakeApi(), "Koushoo", "2026-11-24")
        snapshot["username"] = '<script>alert("x")</script>'
        svg = daily.render(snapshot)
        ET.fromstring(svg)
        self.assertNotIn("<script>", svg)

    def test_publish_rejects_upstream_origin_and_dirty_checkout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            daily.git(root, "init", "-b", "main")
            daily.git(root, "remote", "add", "origin", "https://github.com/antonisloukis/minimal-github-stats.git")
            with self.assertRaisesRegex(RuntimeError, "Origin"):
                daily.prepare_publish(root, "Koushoo", "Koushoo", "")
            daily.git(root, "remote", "set-url", "origin", "https://github.com/Koushoo/Koushoo.git")
            (root / "notes.txt").write_text("Preserve user work")
            with self.assertRaisesRegex(RuntimeError, "uncommitted"):
                daily.prepare_publish(root, "Koushoo", "Koushoo", "")

    def test_publish_to_local_bare_remote_and_resume_failed_push(self):
        # Real Git integration; only account validation/fetch is replaced for the local test remote.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            remote = Path(temp) / "remote.git"
            root.mkdir()
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
            daily.git(root, "init", "-b", "main")
            daily.git(root, "config", "user.name", "Test")
            daily.git(root, "config", "user.email", "test@example.invalid")
            (root / ".gitignore").write_text(".daily.lock\n")
            (root / "README.md").write_text("Do not overwrite\n")
            daily.git(root, "add", ".gitignore", "README.md")
            daily.git(root, "commit", "-m", "Initial")
            daily.git(root, "remote", "add", "origin", str(remote))
            daily.git(root, "push", "origin", "main")
            with patch.object(daily, "prepare_publish"):
                real_git = daily.git
                def failing_push(checkout, *args, **kwargs):
                    if args[0] == "push":
                        raise RuntimeError("Simulated connection loss")
                    return real_git(checkout, *args, **kwargs)
                with patch.object(daily, "git", side_effect=failing_push):
                    with self.assertRaisesRegex(RuntimeError, "connection loss"):
                        daily.run(root, "Koushoo", FakeApi(), now=NOW, publish=True, author_email="test@example.invalid")
                count = daily.git(root, "rev-list", "--count", "HEAD").stdout.strip()
                daily.run(root, "Koushoo", FakeApi(), now=NOW, publish=True, author_email="test@example.invalid")
                self.assertEqual(count, daily.git(root, "rev-list", "--count", "HEAD").stdout.strip())
                self.assertEqual((root / "README.md").read_text(), "Do not overwrite\n")
                self.assertFalse(daily.git(root, "status", "--porcelain").stdout.strip())
                self.assertEqual(daily.git(root, "rev-parse", "HEAD").stdout,
                                 subprocess.run(["git", "--git-dir", str(remote), "rev-parse", "main"],
                                                text=True, capture_output=True, check=True).stdout)


if __name__ == "__main__":
    unittest.main()
