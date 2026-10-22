# Termux Core: Tool Guide

This page covers **25 catalog entries** in the SYN_LAUNCH **Termux Core** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Foundational command-line utilities for navigating files, editing text, scripting, downloading data, and managing code.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Clang

**What it is used for:** C/C++ compiler toolchain for native builds where Android dependencies permit.

**How to start:**
```bash
clang --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `clang`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/libllvm). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### curl

**What it is used for:** HTTP client for API testing, response headers, TLS troubleshooting, and downloads.

**How to start:**
```bash
curl -I https://example.com
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `curl`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/libcurl). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### fd

**What it is used for:** Fast file finder with sensible defaults and filtering.

**How to start:**
```bash
fd --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `fd`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/fd). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### file

**What it is used for:** Identify file types from file signatures and content.

**How to start:**
```bash
file --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `file`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/file/file/blob/4ee5ca8fb938c3168bcededd0ce7c2e03daea485/README.md). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### fzf

**What it is used for:** Interactive fuzzy finder for files, history, and command output.

**How to start:**
```bash
fzf --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `fzf`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/fzf). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### git

**What it is used for:** Distributed version control for source code, change history, and repository collaboration.

**How to start:**
```bash
git status
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `git`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/git). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Go

**What it is used for:** Go compiler and module toolchain for supported upstream command-line tools.

**How to start:**
```bash
go --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `golang`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/golang). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### jq

**What it is used for:** Parse, filter, and transform JSON from APIs, logs, and command-line pipelines.

**How to start:**
```bash
jq --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `jq`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/jq). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### less

**What it is used for:** Page through long command output and text files.

**How to start:**
```bash
less --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `less`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/less). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Make

**What it is used for:** Terminal, programming, file, and package-management utility for Termux workflows.

**How to start:**
```bash
make --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `make`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/make). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### nano

**What it is used for:** Simple terminal text editor for configuration and notes.

**How to start:**
```bash
nano --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `nano`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/nano). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Node.js

**What it is used for:** JavaScript runtime and npm ecosystem for developer and security tools.

**How to start:**
```bash
node --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `nodejs`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/nodejs). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### openssh

**What it is used for:** SSH client and key-management tools for authorized remote administration.

**How to start:**
```bash
ssh --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `openssh`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/openssh). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Perl

**What it is used for:** Perl runtime used by many classic command-line and security utilities.

**How to start:**
```bash
perl --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `perl`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/perl). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### PHP

**What it is used for:** PHP runtime for application testing and local development. Critical security update (2026-10-21): upgrade promptly; see the PHP security advisory in the project wiki.

**How to start:**
```bash
php --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `php`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/c2bb85d3f26d52ba4a4a159d14214a8ace706235/packages/php). This documents source metadata, not verified device functionality.

**Important note:** CRITICAL SECURITY UPDATE 2026-10-21: CVE-2026-109618 and CVE-2026-109619 allow unauthenticated remote code execution in affected PHP web-serving installations. Fixed upstream releases: 8.5.12, 8.4.27, 8.3.36, 8.2.35. Termux's upstream recipe now targets 8.5.12, but installed repository metadata may lag; refresh packages, update PHP, then verify with php -v. See wiki/PHP-Security-Update-2026-10-21.md.

---

### Python

**What it is used for:** Python runtime for scripts and Python-based security utilities.

**How to start:**
```bash
python --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `python`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/python). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### ripgrep

**What it is used for:** Fast recursive text search for source code, logs, and forensic notes.

**How to start:**
```bash
rg --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `ripgrep`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/ripgrep). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### rsync

**What it is used for:** Synchronize files and preserve metadata between local or remote paths.

**How to start:**
```bash
rsync --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `rsync`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/rsync). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Ruby

**What it is used for:** Ruby runtime for scripts and tools that depend on Ruby gems.

**How to start:**
```bash
ruby --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `ruby`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/ruby). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Rust

**What it is used for:** Rust compiler and Cargo package manager for native command-line utilities.

**How to start:**
```bash
rustc --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `rust`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/rust). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### sqlite3

**What it is used for:** Inspect and query SQLite databases from the terminal.

**How to start:**
```bash
sqlite3 --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `sqlite`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/libsqlite). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### tmux

**What it is used for:** Terminal multiplexer for persistent sessions and split panes.

**How to start:**
```bash
tmux --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `tmux`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/tmux). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### tree

**What it is used for:** Display directory structures as readable trees.

**How to start:**
```bash
tree --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `tree`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/tree). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### vim

**What it is used for:** Modal terminal text editor for code and configuration.

**How to start:**
```bash
vim --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `vim`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/vim). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### wget

**What it is used for:** Command-line file downloader with support for common HTTP and FTP workflows.

**How to start:**
```bash
wget --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `wget`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/wget). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
