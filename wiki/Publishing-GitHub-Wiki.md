# Publishing the GitHub Wiki

The repository's `wiki/` directory is the reviewable documentation source. The separate [published GitHub Wiki](https://github.com/LILSYNNOFFICIAL/syn_launch/wiki) is a different Git repository and does not update automatically when files in `wiki/` change.

## Preview changes first

From a local checkout of `LILSYNNOFFICIAL/syn_launch`, run:

```bash
bash scripts/sync_github_wiki.sh
```

The helper clones the wiki repository, copies Markdown pages, maps `wiki/README.md` to the wiki's `Home.md`, rewrites internal page links, keeps existing wiki-only pages, and prints a diff summary. The default mode does not commit or push anything.

## Publish

After reviewing the preview, run:

```bash
bash scripts/sync_github_wiki.sh --push
```

This commits and pushes the generated Markdown to the wiki remote. Git must already have credentials that can write to the repository's Wiki. Do not put a personal access token in the script, repository, shell history, or chat. If GitHub prompts for authentication, use the credential manager or an approved credential flow.

## Boundaries

- The script does not enable the Wiki feature or change repository settings.
- It does not delete pages that exist only in the published Wiki.
- It uses the current `main` branch's `wiki/` files and logo URL.
- Always inspect the dry-run output before publishing.
- Verify the published Home page and key links after pushing.
