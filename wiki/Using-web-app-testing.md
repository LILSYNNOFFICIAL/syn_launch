# Web App Testing: Tool Guide

This page covers **22 catalog entries** in the SYN_LAUNCH **Web App Testing** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools for examining web applications in a lab or explicitly authorized engagement.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Burp Suite

**What it is used for:** Web application testing proxy from PortSwigger; desktop Java support is normally required.

**How to start:**
```bash
See the official Burp Suite installation documentation.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://portswigger.net/burp)

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### Commix

**What it is used for:** Command-injection testing framework for controlled authorized assessments.

**How to start:**
```bash
python commix.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/commixproject/commix)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/commixproject/commix/blob/289ff2285ee25410e8f150f4ddf124a8e2ab2a7e/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Potentially executes commands on vulnerable targets; lab or written authorization only.

**External services / environment:** An explicitly authorized test application or lab target when the tool performs active assessment..

---

### Corsy

**What it is used for:** Check CORS configuration for common security misconfigurations.

**How to start:**
```bash
python corsy.py -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/s0md3v/Corsy)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/s0md3v/Corsy/blob/2985ae24da524ba6905d36bfbadca7fe71a9f199/requirements.txt). This documents source metadata, not verified device functionality.

**Important note:** Only test approved origins and endpoints.

**External services / environment:** An explicitly authorized test application or lab target when the tool performs active assessment..

---

### curlie

**What it is used for:** Web application assessment utility for authorized testing. Review request behavior and rate limits before active use.

**How to start:**
```bash
curlie --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `curlie`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/curlie). This documents source metadata, not verified device functionality.

**Important note:** Termux package recipe is documented at a pinned upstream revision; actual repository availability and device runtime remain unverified.

---

### dirsearch

**What it is used for:** Web application assessment utility for authorized testing. Review request behavior and rate limits before active use.

**How to start:**
```bash
dirsearch --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `dirsearch`.

**Upstream project / source:** [Open source](https://github.com/maurosoria/dirsearch)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/maurosoria/dirsearch/blob/b45e01bb891457d6846e6af0a3755e032f937d78/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Only the explicitly scoped target endpoint when the operator chooses to run the tool..

---

### Feroxbuster

**What it is used for:** Recursive content discovery for authorized web assessments.

**How to start:**
```bash
feroxbuster --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `feroxbuster`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/feroxbuster). This documents source metadata, not verified device functionality.

**Important note:** Termux package recipe is documented at a pinned upstream revision; actual repository availability and device runtime remain unverified.

---

### ffuf

**What it is used for:** Fast web fuzzer for authorized content and parameter discovery.

**How to start:**
```bash
ffuf --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/ffuf/ffuf/v2@latest`.

**Upstream project / source:** [Open source](https://github.com/ffuf/ffuf)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/ffuf/ffuf/blob/8d65e0373e5f223530174e5694285af849770078/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### Gobuster

**What it is used for:** Web application assessment utility for authorized testing. Review request behavior and rate limits before active use.

**How to start:**
```bash
gobuster --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/OJ/gobuster/v3@latest`.

**Upstream project / source:** [Open source](https://github.com/OJ/gobuster)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/OJ/gobuster/blob/c77583fbb8824058d74d38240896eff610683c8e/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### gowitness

**What it is used for:** Capture website screenshots for visual review of authorized web assets.

**How to start:**
```bash
gowitness --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/sensepost/gowitness@latest`.

**Upstream project / source:** [Open source](https://github.com/sensepost/gowitness)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/sensepost/gowitness/blob/601c84367aaf26eae7d1b5181b70633cb662cf66/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Browser dependencies and architecture support may be limited on Android; screenshots can contain sensitive data.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### hakrawler

**What it is used for:** Crawl links from authorized web applications.

**How to start:**
```bash
hakrawler -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/hakluke/hakrawler@latest`.

**Upstream project / source:** [Open source](https://github.com/hakluke/hakrawler)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/hakluke/hakrawler/blob/52a16fe61bd18b8f431b9d66058cba12e96e4451/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Crawling creates requests; limit it to approved hosts.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### JWT Tool

**What it is used for:** Inspect and test JSON Web Tokens in a controlled lab or authorized application.

**How to start:**
```bash
python jwt_tool.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/ticarpi/jwt_tool)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/ticarpi/jwt_tool/blob/3bc7407cf2222d6a821dcc19c776e5a1b1cb9a9b/requirements.txt). This documents source metadata, not verified device functionality.

**Important note:** Never paste production tokens into public services.

**External services / environment:** An explicitly authorized test application or lab target when the tool performs active assessment..

---

### Nikto

**What it is used for:** Web server misconfiguration and known-file checks for authorized targets.

**How to start:**
```bash
nikto -Help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/sullo/nikto)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/sullo/nikto/blob/312645d873478a77986627ab1fc8cffe595e85d4/program/nikto.pl). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**External services / environment:** Authorized target web servers; optional DNS and network services..

---

### OWASP ZAP

**What it is used for:** Web application security proxy and scanner; desktop/Java environment is normally required.

**How to start:**
```bash
See the official ZAP installation and automation documentation.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://www.zaproxy.org/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/zaproxy/zaproxy/blob/e06ba5ee209e27a9a81ff16e17696d6b59757d3a/build.gradle.kts). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### qsreplace

**What it is used for:** Replace query-string values in URL lists for controlled testing workflows.

**How to start:**
```bash
qsreplace --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/tomnomnom/qsreplace@latest`.

**Upstream project / source:** [Open source](https://github.com/tomnomnom/qsreplace)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/tomnomnom/qsreplace/blob/320475befaf66d986400aa8c3ed9b43e0b6b5a02/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Use only with URL lists collected within your authorized scope.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### Smuggler

**What it is used for:** Check for potential HTTP request-smuggling conditions in controlled environments.

**How to start:**
```bash
python smuggler.py -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/defparam/smuggler)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/defparam/smuggler/blob/2be871e6151ce85167a277fab21c74c851d8b20b/README.md). This documents source metadata, not verified device functionality.

**Important note:** Potentially disruptive protocol tests; use a staging target and written approval.

---

### sqlmap

**What it is used for:** Automate SQL injection testing only on explicitly authorized targets.

**How to start:**
```bash
sqlmap --version
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `sqlmap`.

**Upstream project / source:** [Open source](https://github.com/sqlmapproject/sqlmap)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/sqlmapproject/sqlmap/blob/9a1660aa120c526f68b637e5f232137722353522/README.md). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### tplmap

**What it is used for:** Server-side template injection testing for authorized applications.

**How to start:**
```bash
python tplmap.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/epinna/tplmap)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/epinna/tplmap/blob/616b0e527f62dd0930e6346ede6bef79e9bcf717/requirements.txt). This documents source metadata, not verified device functionality.

**Important note:** Potentially intrusive; use labs or approved scope.

**External services / environment:** An explicitly authorized test application or lab target when the tool performs active assessment..

---

### Wapiti

**What it is used for:** Web application assessment utility for authorized testing. Review request behavior and rate limits before active use.

**How to start:**
```bash
wapiti3 --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `wapiti3`.

**Upstream project / source:** [Open source](https://github.com/wapiti-scanner/wapiti)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/wapiti-scanner/wapiti/blob/1e816981319a974f250caab219c0eb19c028e990/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** The explicitly scoped web application target and configured external services.

---

### Wappalyzer

**What it is used for:** Identify web technologies and frameworks from supported page signals.

**How to start:**
```bash
See the upstream CLI documentation.
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/wappalyzer/wappalyzer)

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### Wfuzz

**What it is used for:** Web application assessment utility for authorized testing. Review request behavior and rate limits before active use.

**How to start:**
```bash
wfuzz --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `wfuzz`.

**Upstream project / source:** [Open source](https://github.com/xmendez/wfuzz)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/xmendez/wfuzz/blob/2263cd0932fef333118cd197656f709141bab615/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** The explicitly scoped web application target.

---

### WhatWeb

**What it is used for:** Web application assessment utility for authorized testing. Review request behavior and rate limits before active use.

**How to start:**
```bash
whatweb https://example.com
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `whatweb`.

**Upstream project / source:** [Open source](https://github.com/urbanadventurer/WhatWeb)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/urbanadventurer/WhatWeb/blob/d279d93042d034f3fd29d5a893d44ccc0595d3f8/README.md). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### XSStrike

**What it is used for:** XSS detection and context analysis for authorized web testing.

**How to start:**
```bash
python xsstrike.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/s0md3v/XSStrike)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/s0md3v/XSStrike/blob/ab27955d367432f944d8f29897e09c15356e76f7/requirements.txt). This documents source metadata, not verified device functionality.

**Important note:** Active probes can trigger application behavior.

**External services / environment:** An explicitly authorized test application or lab target when the tool performs active assessment..

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
