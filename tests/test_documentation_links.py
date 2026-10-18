"""Catch broken repository-local Markdown links without requiring network access."""
from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,}).*$", re.MULTILINE)


def markdown_files():
    return sorted(
        path for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "node_modules" not in path.parts
    )


def strip_fenced_code(text: str) -> str:
    lines = text.splitlines()
    output = []
    fence_char = None
    fence_len = 0
    for line in lines:
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char = marker[0]
                fence_len = len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_len:
                fence_char = None
                fence_len = 0
                continue
        if fence_char is None:
            output.append(line)
    return "\n".join(output)


class DocumentationLinkTests(unittest.TestCase):
    def test_repository_local_markdown_links_resolve(self):
        missing = []
        for markdown in markdown_files():
            try:
                content = markdown.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                missing.append(f"{markdown.relative_to(ROOT)}: not UTF-8")
                continue
            content = strip_fenced_code(content)
            for destination in LINK_RE.findall(content):
                destination = destination.strip()
                if destination.startswith("<") and destination.endswith(">"):
                    destination = destination[1:-1]
                parsed = urlsplit(destination)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                path_text = unquote(parsed.path)
                if path_text.startswith("/"):
                    target = ROOT / path_text.lstrip("/")
                else:
                    target = markdown.parent / path_text
                if not target.exists():
                    missing.append(
                        f"{markdown.relative_to(ROOT)} -> {destination}"
                    )
        self.assertEqual(missing, [], "Broken local Markdown links:\\n" + "\\n".join(missing))


if __name__ == "__main__":
    unittest.main()
