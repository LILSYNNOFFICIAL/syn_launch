# Wireless & Android Environment: Tool Guide

This page covers **10 catalog entries** in the SYN_LAUNCH **Wireless & Android Environment** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Utilities related to Android/Termux environment inspection and wireless capabilities. Hardware, permissions, root, and kernel restrictions may limit functionality.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Aircrack-ng

**What it is used for:** Wireless security auditing suite requiring compatible adapters, drivers, and often root access.

**How to start:**
```bash
aircrack-ng --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/aircrack-ng/aircrack-ng)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-root-packages/tree/06591fc024101b04095ec4417d51907512b46e3c/packages/aircrack-ng). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**Root requirement:** The catalog marks this entry as root-required. Confirm device support and understand the consequences; do not bypass Android protections.

**Hardware requirements:** Compatible wireless chipset/driver/firmware and any required external adapter for the intended capability..

---

### BlueZ tools

**What it is used for:** Bluetooth command-line utilities; Android's Bluetooth stack may not expose BlueZ interfaces.

**How to start:**
```bash
bluetoothctl --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/bluez/bluez)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/bluez/bluez/tree/fa6ba55020dee3c3183041c854c347b4582448be/tools). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**Hardware requirements:** Bluetooth adapter and OS stack exposing the expected BlueZ interfaces..

---

### iw

**What it is used for:** Linux wireless configuration utility; stock Android may not expose the required wireless interfaces.

**How to start:**
```bash
iw --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://wireless.wiki.kernel.org/en/users/documentation/iw)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-root-packages/tree/06591fc024101b04095ec4417d51907512b46e3c/packages/iw). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**Root requirement:** The catalog marks this entry as root-required. Confirm device support and understand the consequences; do not bypass Android protections.

**Hardware requirements:** Wireless chipset/driver/firmware exposing the requested nl80211 capabilities..

---

### Kismet

**What it is used for:** Wireless network detector and packet capture framework requiring supported hardware and permissions.

**How to start:**
```bash
kismet --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/kismetwireless/kismet)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/kismetwireless/kismet/blob/de2b100dcdb34e86eb1b3c1d559aac154ad315d9/README.md). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**Hardware requirements:** Supported wireless adapter/driver and capture interface for intended operation..

---

### Termux clipboard

**What it is used for:** Wireless or Android integration utility with kernel, permission, companion-app, or adapter dependencies.

**How to start:**
```bash
termux-clipboard-get --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-api`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-api). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

**External services / environment:** For Termux:API commands, the separate Termux:API Android companion app and requested Android permissions may be required..

---

### Termux location

**What it is used for:** Requests Android location with permission and user consent.

**How to start:**
```bash
termux-location --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-api`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-api). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

**External services / environment:** For Termux:API commands, the separate Termux:API Android companion app and requested Android permissions may be required..

---

### Termux Wi-Fi info

**What it is used for:** Wireless or Android integration utility with kernel, permission, companion-app, or adapter dependencies.

**How to start:**
```bash
termux-wifi-connectioninfo
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-api`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-api). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

**External services / environment:** For Termux:API commands, the separate Termux:API Android companion app and requested Android permissions may be required..

---

### Termux Wi-Fi scan

**What it is used for:** Wireless or Android integration utility with kernel, permission, companion-app, or adapter dependencies.

**How to start:**
```bash
termux-wifi-scaninfo --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-api`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-api). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

**External services / environment:** For Termux:API commands, the separate Termux:API Android companion app and requested Android permissions may be required..

---

### termux-info

**What it is used for:** Wireless or Android integration utility with kernel, permission, companion-app, or adapter dependencies.

**How to start:**
```bash
termux-info --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-tools`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-tools). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### termux-open

**What it is used for:** Wireless or Android integration utility with kernel, permission, companion-app, or adapter dependencies.

**How to start:**
```bash
termux-open --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-tools`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-tools). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
