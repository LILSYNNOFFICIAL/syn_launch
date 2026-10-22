# Privacy & Metadata: Tool Guide

This page covers **1 catalog entries** in the SYN_LAUNCH **Privacy & Metadata** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools for understanding privacy-relevant metadata and reducing unintended disclosure.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Metagoofil

**What it is used for:** Collect metadata from public documents for authorized reconnaissance.

**How to start:**
```bash
python metagoofil.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/opsdisk/metagoofil)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/opsdisk/metagoofil/blob/8d50624f1534e63c8bb64ee132d8c2298dba6724/requirements.txt). This documents source metadata, not verified device functionality.

**Important note:** Search-provider terms and compatibility change; manual-only.

**External services / environment:** An explicitly authorized cloud, mobile-app, or directory environment when the tool is used for assessment..

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
