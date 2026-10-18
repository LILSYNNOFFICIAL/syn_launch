"""Integration regression tests for safe GitHub Wiki synchronization."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sync_github_wiki.sh"


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


class WikiSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source_repo = self.base / "source"
        self.source_repo.mkdir()
        git(self.source_repo, "init", "-q")
        git(self.source_repo, "config", "user.name", "Test")
        git(self.source_repo, "config", "user.email", "test@example.invalid")
        (self.source_repo / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.source_repo / "scripts" / SCRIPT.name)
        wiki_source = self.source_repo / "wiki"
        wiki_source.mkdir()
        (wiki_source / "README.md").write_text(
            '# Home\n\n[Next](New-Page.md)\n[Guide](wiki/Optional-Linux-Environments.md)\n'
            '[Source](../README.md)\n<img src="../img/file_00000000f48881fdb4a638a0643452e1.png">\n',
            encoding="utf-8",
        )
        (wiki_source / "New-Page.md").write_text("# Newly added page\n", encoding="utf-8")
        git(self.source_repo, "add", ".")
        git(self.source_repo, "commit", "-qm", "fixture source")

        self.remote = self.base / "wiki.git"
        subprocess.run(
            ["git", "init", "--bare", str(self.remote)], check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        checkout = self.base / "wiki-checkout"
        git(self.base, "clone", str(self.remote), str(checkout))
        git(checkout, "config", "user.name", "Test")
        git(checkout, "config", "user.email", "test@example.invalid")
        (checkout / "Home.md").write_text("# Published home\n", encoding="utf-8")
        (checkout / "Custom-Page.md").write_text("# Wiki-only page\n", encoding="utf-8")
        git(checkout, "add", ".")
        git(checkout, "commit", "-qm", "initial wiki")
        git(checkout, "push", "origin", "HEAD:master")
        self.initial_remote_head = git(self.remote, "rev-parse", "refs/heads/master")

        self.env = os.environ.copy()
        self.env["SYN_LAUNCH_WIKI_REMOTE"] = str(self.remote)

    def run_sync(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", str(self.source_repo / "scripts" / SCRIPT.name), *args],
            cwd=self.source_repo, env=self.env, check=False, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def verify_checkout(self) -> Path:
        checkout = self.base / "verify"
        git(self.base, "clone", str(self.remote), str(checkout))
        return checkout

    def test_dry_run_shows_diff_and_does_not_change_remote(self):
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertIn("New-Page.md", result.stdout)
        self.assertIn("Dry run only", result.stdout)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/master"), self.initial_remote_head)

    def test_push_publishes_new_page_and_preserves_wiki_only_page(self):
        result = self.run_sync("--push")
        self.assertEqual(result.returncode, 0, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertIn("Published wiki pages pushed successfully.", result.stdout)
        checkout = self.verify_checkout()
        home = (checkout / "Home.md").read_text(encoding="utf-8")
        self.assertIn("[Next](New-Page)", home)
        self.assertIn("[Guide](Optional-Linux-Environments)", home)
        self.assertIn("[Source](https://github.com/LILSYNNOFFICIAL/syn_launch/blob/main/README.md)", home)
        self.assertIn(
            'src="https://raw.githubusercontent.com/LILSYNNOFFICIAL/syn_launch/main/img/file_00000000f48881fdb4a638a0643452e1.png"',
            home,
        )
        self.assertEqual((checkout / "New-Page.md").read_text(encoding="utf-8"), "# Newly added page\n")
        self.assertEqual((checkout / "Custom-Page.md").read_text(encoding="utf-8"), "# Wiki-only page\n")
        self.assertNotEqual(git(self.remote, "rev-parse", "refs/heads/master"), self.initial_remote_head)

    def test_rejects_unknown_mode_without_touching_remote(self):
        result = self.run_sync("--force")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stderr)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/master"), self.initial_remote_head)


if __name__ == "__main__":
    unittest.main()
