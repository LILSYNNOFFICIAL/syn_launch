# Cryptography & Password Hygiene: Tool Guide

This page covers **12 catalog entries** in the SYN_LAUNCH **Cryptography & Password Hygiene** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Utilities for inspecting cryptographic settings, validating hashes, and improving password handling. Never test credentials without authorization.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### age

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
age --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `age`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/age). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### age-keygen

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
age-keygen --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `age`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/age). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### bcrypt

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
bcrypt --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `bcrypt`.

**Upstream project / source:** [Open source](https://pypi.org/project/bcrypt/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/pyca/bcrypt/blob/1218b62796709e72121046458c3c1f046a6b1e5d/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

---

### Certbot

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
certbot --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `certbot`.

**Upstream project / source:** [Open source](https://github.com/certbot/certbot)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/certbot/certbot/blob/990a59a814c8d4c53cc896f3c376c1c14e6c099c/certbot/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** ACME certificate authority and DNS providers depending on challenge/plugin configuration.

---

### GnuPG

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
gpg --version
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `gnupg`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/gnupg). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Hashcat

**What it is used for:** Offline password-hash auditing and recovery; compatible GPU/OpenCL support is generally absent on stock Android.

**How to start:**
```bash
hashcat --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/hashcat/hashcat)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/hashcat/hashcat/blob/5ec006d303bf3d55bc8a6afe1b67b858682457e7/src/Makefile). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### hashid

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
hashid --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `hashid`.

**Upstream project / source:** [Open source](https://pypi.org/project/hashid/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/psypanda/hashID/blob/7e8473a823060e56d4b6090a98591e252bd9505e/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

---

### John the Ripper

**What it is used for:** Offline password-hash auditing for hashes you are authorized to examine.

**How to start:**
```bash
john --list=formats
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/openwall/john)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/openwall/john/blob/5184bc0b8c105f8c5978b112e723d65b2de3e63e/README.md). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### Passlib

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
passlib --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `passlib`.

**Upstream project / source:** [Open source](https://pypi.org/project/passlib/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/glic3rinu/passlib/blob/3f6b5c1f683b2b29780deda81a3eea7960c6409f/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

---

### ssh-keygen

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
ssh-keygen --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `openssh`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/openssh). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### SSLyze

**What it is used for:** Cryptography or password-auditing utility. Only use keys and hashes you own or are authorized to examine.

**How to start:**
```bash
sslyze --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `sslyze`.

**Upstream project / source:** [Open source](https://github.com/nabla-c0d3/sslyze)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/nabla-c0d3/sslyze/blob/3bd5094dec1dfbaac1a03957c35ba5e487f5b890/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** TLS endpoints explicitly selected for assessment.

---

### testssl.sh

**What it is used for:** Probe TLS/SSL configuration for authorized services using a shell-based test suite.

**How to start:**
```bash
testssl.sh --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/testssl/testssl.sh)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/testssl/testssl.sh/blob/9bd7e16df96a8e4e36c89f6c55443eceb9e36c71/Readme.md). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
