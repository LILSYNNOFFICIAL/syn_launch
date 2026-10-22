# Forensics & Reverse Engineering: Tool Guide

This page covers **7 catalog entries** in the SYN_LAUNCH **Forensics & Reverse Engineering** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Utilities for static inspection, reverse engineering, and forensic review. Work from copies and document evidence handling.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### angr

**What it is used for:** Python framework for binary analysis and symbolic execution in research labs.

**How to start:**
```bash
See the official angr documentation.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/angr/angr)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/angr/angr/blob/ae9f5786fd94410ca400063bf21719aa8b564d3e/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Heavy dependencies; prefer a supported Linux environment for complex analyses.

---

### LIEF

**What it is used for:** Parse and inspect executable formats including ELF, PE, and Mach-O.

**How to start:**
```bash
See LIEF's official Python and native API documentation.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/lief-project/LIEF)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/lief-project/LIEF/blob/15777f106f6220046cf26ee99940d1f56751325e/CMakeLists.txt). This documents source metadata, not verified device functionality.

**Important note:** Native dependency and wheel support on Android is unverified.

---

### Plaso/log2timeline

**What it is used for:** Build forensic timelines from supported evidence sources.

**How to start:**
```bash
log2timeline.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/log2timeline/plaso)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/log2timeline/plaso/blob/76c02d9f3341bbbe4da8c21e944ee1516d069668/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Dependency-heavy; best suited to a supported Linux workstation.

---

### Rizin

**What it is used for:** Reverse-engineering framework for binary inspection.

**How to start:**
```bash
rizin -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `rizin`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/rizin). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### steghide

**What it is used for:** Inspect and work with supported steganography formats during forensic analysis.

**How to start:**
```bash
See upstream command-line documentation.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `steghide`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/steghide). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### Volatility 3

**What it is used for:** Memory-forensics framework for supported memory images.

**How to start:**
```bash
vol --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `volatility3`.

**Upstream project / source:** [Open source](https://github.com/volatilityfoundation/volatility3)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/volatilityfoundation/volatility3/blob/77ff0b1932d77527f850c8ced01d85805ea7bf97/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Use legally obtained images and compatible symbols/plugins.

---

### YARA-X

**What it is used for:** Modern YARA-compatible pattern-matching engine for defensive triage.

**How to start:**
```bash
yr --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/VirusTotal/yara-x)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/VirusTotal/yara-x/blob/649cd3bb08e1c4ecc1524cc016c7aa27a75d2193/Cargo.toml). This documents source metadata, not verified device functionality.

**Important note:** Separate project from classic YARA; Termux recipe not verified.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
