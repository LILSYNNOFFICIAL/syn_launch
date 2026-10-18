#!/usr/bin/env bash
set -euo pipefail

# Publish versioned wiki/ Markdown pages to the separate GitHub Wiki git repository.
# Safe by default: inspect the diff only. Pass --push to commit and push.
MODE="${1:-}"
if [[ "$MODE" != "" && "$MODE" != "--push" ]]; then
  echo "Usage: $0 [--push]" >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel)"
SOURCE="$ROOT/wiki"
REMOTE="${SYN_LAUNCH_WIKI_REMOTE:-https://github.com/LILSYNNOFFICIAL/syn_launch.wiki.git}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if [[ ! -d "$SOURCE" ]]; then
  echo "Expected documentation source directory at $SOURCE" >&2
  exit 2
fi

git clone "$REMOTE" "$TMP/wiki"
python3 - "$SOURCE" "$TMP/wiki" <<'PY'
from pathlib import Path
import re
import sys

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
repo = "https://github.com/LILSYNNOFFICIAL/syn_launch"

for page in sorted(source.glob("*.md")):
    target_name = "Home.md" if page.name == "README.md" else page.name
    text = page.read_text(encoding="utf-8")

    # GitHub Wiki uses page slugs for internal links. Keep links to repository
    # documents and assets as stable absolute URLs.
    def replace_link(match):
        label, url = match.group(1), match.group(2)
        if url.startswith("../"):
            path = url[3:]
            return f"]({repo}/blob/main/{path})"
        if url.startswith("wiki/"):
            return f"]({url[5:].removesuffix('.md')})"
        if url.endswith(".md") and not url.startswith(("http://", "https://")):
            return f"]({url[:-3]})"
        return match.group(0)

    text = re.sub(r"\]\(([^)]+)\)", lambda m: replace_link(re.match(r"(.*)", m.group(0)) and type("M", (), {"group": lambda self, n: (m.group(0)[2:m.group(0).find("](")] if n == 1 else m.group(0)[m.group(0).find("](")+2:-1)})()) , text)
    text = text.replace(
        'src="../img/file_00000000f48881fdb4a638a0643452e1.png"',
        'src="https://raw.githubusercontent.com/LILSYNNOFFICIAL/syn_launch/main/img/file_00000000f48881fdb4a638a0643452e1.png"',
    )
    (destination / target_name).write_text(text, encoding="utf-8")

print("Synced local Markdown into the temporary wiki checkout. Existing wiki-only pages are preserved.")
PY

cd "$TMP/wiki"
if git diff --quiet; then
  echo "Published wiki already matches repository wiki/ Markdown."
  exit 0
fi

git --no-pager diff --stat
if [[ "$MODE" != "--push" ]]; then
  echo "Dry run only. Review changes, then rerun with --push to publish."
  exit 0
fi

git add -- '*.md'
if git diff --cached --quiet; then
  echo "No Markdown changes to publish."
  exit 0
fi
git -c user.name="SYN_LAUNCH Wiki Sync" -c user.email="syn-launch-wiki-sync@users.noreply.github.com" commit -m "docs: sync published wiki from repository documentation"
git push origin HEAD
echo "Published wiki pages pushed successfully."
