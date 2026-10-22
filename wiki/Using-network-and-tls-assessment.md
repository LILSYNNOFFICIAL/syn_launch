# Network & TLS Assessment: Tool Guide

This page covers **8 catalog entries** in the SYN_LAUNCH **Network & TLS Assessment** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Utilities for reviewing TLS configuration, certificates, network services, and related exposure within approved scope.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Chisel

**What it is used for:** TCP/UDP tunnel for authorized lab connectivity and troubleshooting.

**How to start:**
```bash
chisel --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/jpillora/chisel@latest`.

**Upstream project / source:** [Open source](https://github.com/jpillora/chisel)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/jpillora/chisel/blob/5ee6c74d60d96a75afb18bc866eb19327170aeed/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Tunneling can bypass network controls; network-owner approval required.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### Ligolo-ng

**What it is used for:** Tunneling framework used in authorized network assessment labs.

**How to start:**
```bash
See the official Ligolo-ng documentation.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/nicocha30/ligolo-ng)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/nicocha30/ligolo-ng/blob/e543732f4be6dc899096ae322ae620bf010bfbfc/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Advanced routing and privileges may be required; manual-only.

---

### OpenSSH keyscan

**What it is used for:** Collect SSH host public keys for inventory and known_hosts maintenance.

**How to start:**
```bash
ssh-keyscan --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `openssh`.

**Upstream project / source:** [Open source](https://github.com/openssh/openssh-portable)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/openssh). This documents source metadata, not verified device functionality.

**Important note:** Use only on systems where you are authorized to inventory SSH host keys.

---

### ProxyChains-NG

**What it is used for:** Route compatible applications through configured proxy chains; does not guarantee anonymity.

**How to start:**
```bash
proxychains4 --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `proxychains-ng`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/proxychains-ng). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### ssh-audit

**What it is used for:** Audit SSH server/client configuration and algorithm support.

**How to start:**
```bash
ssh-audit --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `ssh-audit`.

**Upstream project / source:** [Open source](https://github.com/jtesta/ssh-audit)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/jtesta/ssh-audit/blob/1df77bfbb664ec435cd662b938c1080012df3354/setup.cfg). This documents source metadata, not verified device functionality.

**Important note:** Audit only SSH services you own or have permission to assess.

**External services / environment:** The explicitly scoped SSH server when the operator chooses to run an audit..

---

### SSLScan

**What it is used for:** Probe TLS protocol and cipher configuration for authorized hosts.

**How to start:**
```bash
sslscan --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `sslscan`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/sslscan). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### TShark

**What it is used for:** Command-line packet analysis utility.

**How to start:**
```bash
tshark --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://www.wireshark.org/docs/man-pages/tshark.html)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-root-packages/tree/06591fc024101b04095ec4417d51907512b46e3c/packages/tshark). This documents source metadata, not verified device functionality.

**Important note:** Capture permissions and Android kernel support vary.

**Root requirement:** The catalog marks this entry as root-required. Confirm device support and understand the consequences; do not bypass Android protections.

**Hardware requirements:** Compatible network interface and packet-capture permissions for the intended capture mode..

---

### ZMap

**What it is used for:** Internet-scale network measurement scanner for tightly scoped audits.

**How to start:**
```bash
zmap --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/zmap/zmap)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/zmap/zmap/blob/7268b1a2204bc9231efefa27ba7cb2fa56717979/CMakeLists.txt). This documents source metadata, not verified device functionality.

**Important note:** High-impact scanner; no broad public scanning without explicit authorization.

**Root requirement:** The catalog marks this entry as root-required. Confirm device support and understand the consequences; do not bypass Android protections.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
