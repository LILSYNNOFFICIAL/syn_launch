# Developer & Supply Chain Security: Tool Guide

This page covers **5 catalog entries** in the SYN_LAUNCH **Developer & Supply Chain Security** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools that help developers review dependencies, build inputs, code, and release integrity.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### actionlint

**What it is used for:** Lint GitHub Actions workflow files for syntax and common mistakes.

**How to start:**
```bash
actionlint -help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/rhysd/actionlint)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/rhysd/actionlint/blob/011a6d15e749bb3f2d771eed9c7aa0e7e3e10ee7/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Manual-only until Termux package/build compatibility is verified.

---

### Cosign

**What it is used for:** Verify and sign software artifacts using Sigstore-supported workflows.

**How to start:**
```bash
cosign version
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/sigstore/cosign/v2/cmd/cosign@latest`.

**Upstream project / source:** [Open source](https://github.com/sigstore/cosign)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/sigstore/cosign/blob/cfeaa4a435c9d42cf724b3e1aac20c1cc09c4be7/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Understand identity and trust policy before accepting artifact signatures.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### Gosec

**What it is used for:** Static security analysis for Go source code.

**How to start:**
```bash
gosec -help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `gosec`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/gosec). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### staticcheck

**What it is used for:** Static analysis and diagnostics for Go code, including bug-prone and inefficient patterns.

**How to start:**
```bash
staticcheck -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `honnef.co/go/tools/cmd/staticcheck@latest`.

**Upstream project / source:** [Open source](https://staticcheck.dev/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/dominikh/go-tools/blob/6ed650b396b48840c782b8d554eaded1299e42ae/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Analyze the intended module and review diagnostics; toolchain compatibility may vary.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### zizmor

**What it is used for:** Static analysis for GitHub Actions workflow security issues.

**How to start:**
```bash
See the official zizmor installation guide.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/zizmorcore/zizmor)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/zizmorcore/zizmor/blob/ea0f7ac34e131fe9491e946e81b3d8fbee2b5171/Cargo.toml). This documents source metadata, not verified device functionality.

**Important note:** Prebuilt binary availability and native builds vary by Android architecture.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
