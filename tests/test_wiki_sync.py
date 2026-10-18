"""Regression tests for the GitHub Wiki sync preview using an isolated local remote."""
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
    def test_dry_run_includes_new_pages_and_preserves_wiki_only_pages(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source_repo = base / "source"
            source_repo.mkdir()
            git(source_repo, "init", "-q")
            git(source_repo, "config", "user.name", "Test")
            git(source_repo, "config", "user.email", "test@example.invalid")
            (source_repo / "scripts").mkdir()
            shutil.copy2(SCRIPT, source_repo / "scripts" / SCRIPT.name)
            (source_repo / "wiki").mkdir()
            (source_repo / "wiki" / "README.md").write_text("# Home\\n", encoding="utf-8")
            (source_repo / "wiki" / "New-Page.md").write_text("# Newly added page\\n", encoding="utf-8")
            git(source_repo, "add", ".")
            git(source_repo, "commit", "-qm", "fixture source")

            remote = base / "wiki.git"
            subprocess.run(["git", "init", "--bare", str(remote)], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            checkout = base / "wiki-checkout"
            git(base, "clone", str(remote), str(checkout))
            git(checkout, "config", "user.name", "Test")
            git(checkout, "config", "user.email", "test@example.invalid")
            (checkout / "Home.md").write_text("# Published home\\n", encoding="utf-8")
            (checkout / "Custom-Page.md").write_text("# Wiki-only page\\n", encoding="utf-8")
            git(checkout, "add", ".")
            git(checkout, "commit", "-qm", "initial wiki")
            git(checkout, "push", "origin", "HEAD:master")
            initial_remote_head = git(remote, "rev-parse", "refs/heads/master")

            env = os.environ.copy()
            env["SYN_LAUNCH_WIKI_REMOTE"] = str(remote)
            result = subprocess.run(
                ["bash", str(source_repo / "scripts" / SCRIPT.name)],
                cwd=source_repo, env=env, check=True, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )

            self.assertIn("New-Page.md", result.stdout)
            self.assertIn("Dry run only", result.stdout)
            self.assertEqual(git(remote, "rev-parse", "refs/heads/master"), initial_remote_head)
            self.assertTrue((checkout / "Custom-Page.md").exists())


if __name__ == "__main__":
    unittest.main()
