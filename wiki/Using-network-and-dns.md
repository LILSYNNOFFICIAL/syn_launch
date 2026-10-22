# Network & DNS: Tool Guide

This page covers **23 catalog entries** in the SYN_LAUNCH **Network & DNS** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Utilities for understanding network paths, DNS behavior, ports, services, and connectivity. Use only on systems you own or are authorized to assess.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### arp-scan

**What it is used for:** Network diagnostics or protocol utility for inspecting connectivity, DNS, routes, or traffic. Use only on networks you own or are authorized to test.

**How to start:**
```bash
arp-scan --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Root-dependent or manual setup.

**Upstream project / source:** [Open source](https://github.com/royhills/arp-scan)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-root-packages/tree/06591fc024101b04095ec4417d51907512b46e3c/packages/arp-scan). This documents source metadata, not verified device functionality.

**Important note:** Root or special kernel/network capabilities required; not expected to work on stock Android.

**Root requirement:** The catalog marks this entry as root-required. Confirm device support and understand the consequences; do not bypass Android protections.

**Hardware requirements:** A compatible local network interface and permissions for ARP/raw packet operations..

---

### DNS utils

**What it is used for:** DNS query utilities including dig and nslookup for name-resolution troubleshooting.

**How to start:**
```bash
dig example.com A
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `dnsutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/dnsutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### hping3

**What it is used for:** Network diagnostics or protocol utility for inspecting connectivity, DNS, routes, or traffic. Use only on networks you own or are authorized to test.

**How to start:**
```bash
hping3 --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/antirez/hping)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-root-packages/tree/06591fc024101b04095ec4417d51907512b46e3c/packages/hping3). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**Root requirement:** The catalog marks this entry as root-required. Confirm device support and understand the consequences; do not bypass Android protections.

**Hardware requirements:** Suitable raw packet/network privileges for the intended operation..

---

### HTTPie

**What it is used for:** Human-friendly HTTP client for API requests and response inspection.

**How to start:**
```bash
http --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `httpie`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/httpie). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### inetutils

**What it is used for:** Network utilities including tools such as telnet and ftp clients.

**How to start:**
```bash
telnet --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `inetutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/inetutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### iperf3

**What it is used for:** Measure network throughput between endpoints you control.

**How to start:**
```bash
iperf3 --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `iperf3`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/iperf3). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### iproute2

**What it is used for:** Modern IP address, link, and route inspection utilities.

**How to start:**
```bash
ip --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `iproute2`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/iproute2). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### mitmproxy

**What it is used for:** Interactive HTTP(S) proxy for debugging your own apps and test traffic.

**How to start:**
```bash
mitmproxy --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `mitmproxy`.

**Upstream project / source:** [Open source](https://pypi.org/project/mitmproxy/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/mitmproxy/mitmproxy/blob/77355977e5ea540b51ed029a40ed1dc2f1c2ba7b/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Applications and endpoints intentionally routed through the proxy.

---

### MTR

**What it is used for:** Combine route tracing and repeated latency/loss measurements.

**How to start:**
```bash
mtr --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `mtr`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-root-packages/tree/06591fc024101b04095ec4417d51907512b46e3c/packages/mtr). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Ncat

**What it is used for:** Network diagnostics or protocol utility for inspecting connectivity, DNS, routes, or traffic. Use only on networks you own or are authorized to test.

**How to start:**
```bash
ncat --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `nmap`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/nmap). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### net-tools

**What it is used for:** Legacy network utilities such as ifconfig and netstat.

**How to start:**
```bash
ifconfig --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `net-tools`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/net-tools). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Netcat

**What it is used for:** Network diagnostics or protocol utility for inspecting connectivity, DNS, routes, or traffic. Use only on networks you own or are authorized to test.

**How to start:**
```bash
nc --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `netcat-openbsd`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/netcat-openbsd). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Nmap

**What it is used for:** Network discovery, service identification, and port auditing. Scan only authorized hosts.

**How to start:**
```bash
nmap -sV 192.0.2.10
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `nmap`.

**Upstream project / source:** [Open source](https://nmap.org/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/nmap). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### OpenSSL

**What it is used for:** TLS client, certificate inspection, and cryptographic command-line utilities.

**How to start:**
```bash
openssl s_client -connect example.com:443 -servername example.com
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `openssl`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/openssl). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### ping

**What it is used for:** Check reachability and latency where Android permissions permit ICMP.

**How to start:**
```bash
ping --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `inetutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/inetutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### socat

**What it is used for:** Bidirectional data relay for authorized networking and troubleshooting.

**How to start:**
```bash
socat --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `socat`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/socat). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### tcpdump

**What it is used for:** Capture and inspect packets when device permissions and kernel support allow it.

**How to start:**
```bash
tcpdump --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `tcpdump`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-root-packages/tree/06591fc024101b04095ec4417d51907512b46e3c/packages/tcpdump). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

**Root requirement:** The catalog marks this entry as root-required. Confirm device support and understand the consequences; do not bypass Android protections.

**Hardware requirements:** Capture privileges and suitable kernel/network-interface access for the intended capture mode..

---

### Termux API

**What it is used for:** Android integration commands require the Termux:API companion app.

**How to start:**
```bash
termux-battery-status --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-api`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-api). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

**External services / environment:** For Termux:API commands, the separate Termux:API Android companion app and requested Android permissions may be required..

---

### Termux services

**What it is used for:** Manage supported Termux background services using runit.

**How to start:**
```bash
sv --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-services`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-services). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Termux wake lock

**What it is used for:** Keep the device awake during a user-requested long-running Termux task.

**How to start:**
```bash
termux-wake-lock --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `termux-tools`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/termux-tools). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Traceroute

**What it is used for:** Inspect network paths and hop behavior toward a destination.

**How to start:**
```bash
traceroute --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `traceroute`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/traceroute). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Whois

**What it is used for:** Query domain and IP registration records from supported registry services.

**How to start:**
```bash
whois example.com
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `whois`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/whois). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### xh

**What it is used for:** Fast HTTP client inspired by HTTPie, useful for API troubleshooting.

**How to start:**
```bash
xh --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `xh`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/xh). This documents source metadata, not verified device functionality.

**Important note:** Termux package recipe is documented at a pinned upstream revision; actual repository availability and device runtime remain unverified.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
