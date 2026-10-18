#!/usr/bin/env bash
set -euo pipefail

# Publish versioned wiki/ Markdown pages to the separate GitHub Wiki git repository.
# Safe by default: inspect the diff only. Pass --push to commit and push.
MODE="\${1:-}"
if [[ "$MODE" != "" && "$MODE" != "--push" ]]; then
  echo "Usage: $0 [--push]" >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel)"
SOURCE="$ROOT/wiki"
REMOTE="\${SYN_LAUNCH_WIKI_REMOTE:-https://github.com/LILSYNNOFFICIAL/syn_launch.wiki.git}"
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
    content = page.read_text(encoding="utf-8")

    def rewrite_link(match):
        label, url = match.group(1), match.group(2)
        if url.startswith("../"):
            url = f"{repo}/blob/main/{url[3:]}"
        elif url.startswith("wiki/"):
            url = url[5:]
            if url.endswith(".md"):
                url = url[:-3]
        elif url == "README.md":
            url = "Home"
        elif url.endswith(".md") and not url.startswith(("http://", "https://")):
            url = url[:-3]
        return f"[{label}]({url})"

    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite_link, content)
    content = content.replace(
        'src="../img/file_00000000f48881fdb4a638a0643452e1.png"',
        'src="https://raw.githubusercontent.com/LILSYNNOFFICIAL/syn_launch/main/img/file_00000000f48881fdb4a638a0643452e1.png"',
    )
    (destination / target_name).write_text(content, encoding="utf-8")

print("Synced repository Markdown into the temporary wiki checkout. Wiki-only pages are preserved.")
PY

cd "$TMP/wiki"
git add -- '*.md'
if git diff --cached --quiet; then
  echo "Published wiki already matches repository wiki/ Markdown."
  exit 0
fi

git --no-pager diff --cached --stat
if [[ "$MODE" != "--push" ]]; then
  echo "Dry run only. Review changes, then rerun with --push to publish."
  exit 0
fi

git -c user.name="SYN_LAUNCH Wiki Sync" -c user.email="syn-launch-wiki-sync@users.noreply.github.com" commit -m "docs: sync published wiki from repository documentation"
git push origin HEAD
echo "Published wiki pages pushed successfully."
