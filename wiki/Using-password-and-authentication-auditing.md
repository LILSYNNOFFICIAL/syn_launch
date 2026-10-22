# Password & Authentication Auditing: Tool Guide

This page covers **3 catalog entries** in the SYN_LAUNCH **Password & Authentication Auditing** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools for reviewing authentication controls and password security in an authorized lab or assessment.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### CeWL

**What it is used for:** Generate wordlists from authorized website content for password-policy audits.

**How to start:**
```bash
cewl --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/digininja/CeWL)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/digininja/CeWL/blob/ca01aeae1c77bb086ef757611dea6377b8d1168b/Gemfile). This documents source metadata, not verified device functionality.

**Important note:** Use only approved targets.

---

### Crunch

**What it is used for:** Generate custom test wordlists for offline password-auditing labs.

**How to start:**
```bash
crunch --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `crunch`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/crunch). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### Hydra

**What it is used for:** Network login auditing for controlled password-policy tests; can lock accounts and disrupt services.

**How to start:**
```bash
hydra -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/vanhauser-thc/thc-hydra)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/vanhauser-thc/thc-hydra/blob/17b52613320257a620ce3b5611b2e8196eb6e7fc/Makefile.am). This documents source metadata, not verified device functionality.

**Important note:** Can lock accounts and disrupt services; manual-only and explicit authorization required.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
