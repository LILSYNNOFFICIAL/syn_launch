# Audit, SAST & Supply Chain: Tool Guide

This page covers **20 catalog entries** in the SYN_LAUNCH **Audit, SAST & Supply Chain** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools for reviewing source code, dependencies, packages, configuration, and software supply-chain risk.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Bandit

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
bandit --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `bandit`.

**Upstream project / source:** [Open source](https://github.com/PyCQA/bandit)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/PyCQA/bandit/blob/68ebe11ef79263be27ec223184b94a4fc394a622/setup.cfg). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

---

### cargo-audit

**What it is used for:** Check Rust dependency lockfiles against RustSec advisories.

**How to start:**
```bash
cargo audit --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `cargo-audit`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/cargo-audit). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### Checkov

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
checkov --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `checkov`.

**Upstream project / source:** [Open source](https://github.com/bridgecrewio/checkov)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/bridgecrewio/checkov/blob/7a6782e3d81e19f1bdd9213129f3138767691f5f/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Cloud APIs when scanning live cloud configurations or using configured integrations.

---

### checksec

**What it is used for:** Inspect binary security properties such as PIE, NX, canaries, and RELRO.

**How to start:**
```bash
checksec --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/slimm609/checksec.sh)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/slimm609/checksec/blob/0ee6a029b99be2f7d664b0b08881cfc7a83e5122/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### detect-secrets

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
detect-secrets --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `detect-secrets`.

**Upstream project / source:** [Open source](https://pypi.org/project/detect-secrets/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/Yelp/detect-secrets/blob/5e141933554a0b74e7341841f318be21e895339c/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

---

### Gitleaks

**What it is used for:** Detect secrets accidentally committed to repositories.

**How to start:**
```bash
gitleaks version
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `gitleaks`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/gitleaks). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### govulncheck

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
govulncheck --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `govulncheck`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/govulncheck). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### Grype

**What it is used for:** Scan container images and filesystems for known package vulnerabilities.

**How to start:**
```bash
grype --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/anchore/grype)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/anchore/grype/blob/8ea928e9f642c376b888a0ee63cb579f1bf47486/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### Hadolint

**What it is used for:** Lint Dockerfiles for common errors and best practices.

**How to start:**
```bash
hadolint --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/hadolint/hadolint)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/hadolint/hadolint/blob/8ae25c05945f030b1ad520f1802e4143e7d0055d/hadolint.cabal). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### Lynis

**What it is used for:** Audit Unix/Linux system configuration; Android's restricted environment limits coverage.

**How to start:**
```bash
lynis --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/CISOfy/lynis)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/CISOfy/lynis/blob/9319416fa0726369ab0a48f686155a90363f3f9c/README.md). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### npm audit

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
npm --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `nodejs`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/nodejs). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### OSV-Scanner

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
osv-scanner --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/google/osv-scanner/v2/cmd/osv-scanner@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/google/osv-scanner/v2/cmd/osv-scanner)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/google/osv-scanner/blob/f455353546889009663c1f8b640d5880a01c889a/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### pip-audit

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
pip-audit --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `pip-audit`.

**Upstream project / source:** [Open source](https://github.com/pypa/pip-audit)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/pypa/pip-audit/blob/828e77a4d4aa6bee8d315681db6928771d951a7c/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Configured vulnerability-data source and package metadata service, depending on audit configuration..

---

### Safety

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
safety --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `safety`.

**Upstream project / source:** [Open source](https://pypi.org/project/safety/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/pyupio/safety/blob/997602736a20c6f4d9fec8c2a5d479624b9ddb9a/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Safety vulnerability-data service depending on command and account configuration.

---

### Semgrep

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
semgrep --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `semgrep`.

**Upstream project / source:** [Open source](https://github.com/semgrep/semgrep)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/semgrep/semgrep/blob/51602ad27f09ef9342a5620601de5ef8f572fbc6/cli/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** External registry or rule sources depending on selected scan configuration.

---

### ShellCheck

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
shellcheck --version
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `shellcheck`.

**Upstream project / source:** [Open source](https://github.com/koalaman/shellcheck)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/shellcheck). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Syft

**What it is used for:** Generate software bills of materials from supported images and directories.

**How to start:**
```bash
syft --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/anchore/syft)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/anchore/syft/blob/a81193226ffdd07b71126dda04e753d6d2e22324/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### Trivy

**What it is used for:** Scan container images, filesystems, repositories, and supported infrastructure artifacts for risks.

**How to start:**
```bash
trivy --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/aquasecurity/trivy)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/aquasecurity/trivy/blob/9dd3e28d275544dd16463162e99471ac761eb9f0/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### TruffleHog

**What it is used for:** Search repositories and supported sources for exposed secrets.

**How to start:**
```bash
trufflehog --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/trufflesecurity/trufflehog/v3@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/trufflesecurity/trufflehog/v3)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/trufflesecurity/trufflehog/blob/048de9ff07098d943136cd5231a0e93fbb3ea443/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### yamllint

**What it is used for:** Security auditing or static-analysis utility for code, dependencies, infrastructure, or exposed secrets. Triage findings before acting.

**How to start:**
```bash
yamllint --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `yamllint`.

**Upstream project / source:** [Open source](https://github.com/adrienverge/yamllint)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/adrienverge/yamllint/blob/96246fb0d5fba8c8cba48747342de3351ea64bea/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
