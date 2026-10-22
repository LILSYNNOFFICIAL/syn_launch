# Forensics & File Analysis: Tool Guide

This page covers **21 catalog entries** in the SYN_LAUNCH **Forensics & File Analysis** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Utilities for inspecting files and evidence, identifying file types, extracting metadata, and supporting reproducible analysis. Preserve originals when evidence matters.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Binwalk

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
binwalk --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `binwalk`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/binwalk). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### bulk_extractor

**What it is used for:** Extract structured artifacts from forensic images without relying on filesystem layout.

**How to start:**
```bash
bulk_extractor -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/simsong/bulk_extractor)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/simsong/bulk_extractor/blob/e86383947ee016c825599887334cacf011736abf/Makefile.am). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### ExifTool

**What it is used for:** Read and inspect metadata in images, documents, and media files.

**How to start:**
```bash
exiftool photo.jpg
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `exiftool`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/exiftool). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### ffprobe

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
ffprobe --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `ffmpeg`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/ffmpeg). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Foremost

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
foremost --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `foremost`.

**Upstream project / source:** [Open source](https://github.com/korczis/foremost)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/korczis/foremost/blob/9b2ccf2a6d924e7a57971af6b92e6a287d28efb1/Makefile). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### GDB

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
gdb --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `gdb`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/gdb). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### hexdump

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
hexdump --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `util-linux`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/util-linux). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### ltrace

**What it is used for:** Trace dynamic library calls where supported by the platform and binary.

**How to start:**
```bash
ltrace --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `ltrace`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/ltrace). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### MediaInfo

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
mediainfo --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `mediainfo`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/mediainfo). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### objdump

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
objdump --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `binutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/binutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### pdfid

**What it is used for:** Inspect PDF token counts to triage potentially suspicious documents.

**How to start:**
```bash
pdfid.py -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/DidierStevens/DidierStevensSuite)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/DidierStevens/DidierStevensSuite/blob/7d625d0b05c4638b981a2a2cc9a8481d7b73e56d/pdfid.py). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### peepdf

**What it is used for:** Analyze PDF structure for suspicious objects and scripts.

**How to start:**
```bash
peepdf --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/jesparza/peepdf)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/jesparza/peepdf/blob/c74dc65c0ac7e506bae4f2582a2435ec50741f40/README.md). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### pngcheck

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
pngcheck --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `pngcheck`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/pnggroup/pngcheck/blob/bd33ad6490269df07cac81e5305f4ebf56c2b637/Makefile). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### radare2

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
r2 --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `radare2`.

**Upstream project / source:** [Open source](https://github.com/radareorg/radare2)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/radare2). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### readelf

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
readelf --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `binutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/binutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Sleuth Kit

**What it is used for:** Filesystem forensic tools for supported disk images and evidence copies.

**How to start:**
```bash
fls -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/sleuthkit/sleuthkit)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/sleuthkit/sleuthkit/blob/e08bdd2f9b74b319981144c03ee492e9287b9e0f/Makefile.am). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### strace

**What it is used for:** Trace system calls for debugging programs where Android ptrace restrictions allow it.

**How to start:**
```bash
strace -V
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `strace`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/strace). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### strings

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
strings --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `binutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/binutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Tesseract OCR

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
tesseract scan.png stdout
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `tesseract`.

**Upstream project / source:** [Open source](https://github.com/tesseract-ocr/tesseract)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/tesseract). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### xxd

**What it is used for:** Forensic or file-analysis utility. Work on copies of authorized evidence and protect sensitive output.

**How to start:**
```bash
xxd --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `vim`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/vim). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### YARA

**What it is used for:** Match files against defensive YARA rules.

**How to start:**
```bash
yara rules.yar sample.bin
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `yara`.

**Upstream project / source:** [Open source](https://github.com/VirusTotal/yara)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/yara). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
