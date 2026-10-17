# SYN_LAUNCH

[![Termux](https://img.shields.io/badge/platform-Termux%20%2F%20Android-00BCD4?logo=android&logoColor=white)](https://termux.dev/)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Catalog](https://img.shields.io/badge/catalog-178%2B%20entries-brightgreen)](catalog.json)
[![Use](https://img.shields.io/badge/use-authorized%20testing-orange)](#responsible-use)

**A catalog-first security, OSINT, networking, forensics, developer-audit, and Android utility launcher for Termux.**

SYN_LAUNCH provides numbered category menus, search, command examples, upstream links, install-method labels, compatibility caveats, install logs, and a progress display. The catalog intentionally contains more tools than can be installed on every Android device.

> **Reality check:** Termux is not desktop Linux. Android permissions, kernel features, CPU architecture, repositories, Python wheels, external hardware, and root access vary. A catalog entry does not mean the tool is installed or guaranteed to work. SYN_LAUNCH distinguishes Termux packages, Python/Go installs, manual-only entries, and root/hardware-dependent tools.

## Quick start

Install Termux from a maintained source such as [F-Droid](https://f-droid.org/packages/com.termux/) or the [official Termux GitHub](https://github.com/termux/termux-app). Do not mix Termux apps and plugins from incompatible signing sources.

~~~bash
pkg update -y
pkg install -y git python
git clone https://github.com/LILSYNNOFFICIAL/syn_launch.git
cd syn_launch
bash install.sh
~~~

Or run directly:

~~~bash
python main.py
python main.py --check
~~~

Rich is optional. If unavailable, SYN_LAUNCH falls back to plain terminal output.

## Features

- **178 catalog entries** across 9 categories.
- Numbered menus and search designed for small screens.
- Tool purpose, install method, source link, compatibility note, and example command.
- When a command is installed, selecting it probes standard version/help flags and shows output from that installed executable (bounded by time and line limits).
- Detects whether an executable appears in PATH. This is a hint, not a full version/self-test.
- Termux package installation through pkg, Python tools in an isolated virtual environment, and Go builds through go install.
- Manual/root/hardware entries are labelled instead of pretending to install.
- Progress bar, action output, timestamped logs, and last-run summary.
- Catalog checks through `python main.py --check`.
- No silent root escalation or automatic target scanning.

## Categories

- Termux Core
- Network & DNS
- OSINT & Recon
- Web App Testing
- Audit, SAST & Supply Chain
- Forensics & File Analysis
- Cryptography & Password Hygiene
- Wireless & Android Environment
- Cloud, Containers & Misc

## Installer behavior

- **Install all Termux packages:** attempts every distinct package name marked as a Termux package. Some names may not exist for a particular architecture or repository. Failures are reported.
- **Install one selected tool:** uses the catalog's declared method.
- **Install Python and Go runtimes:** bootstraps toolchains needed for Python/Go-based catalog entries.
- **Python tools:** use `~/.syn_launch/venv` to avoid polluting Termux's system Python.
- **Go tools:** can require large downloads and compilation; module compatibility may change.
- **Manual/root/hardware tools:** are catalog-only until a verified compatible method exists.

The progress bar counts completed tool/package attempts. It does not pretend to know download-byte percentages. Logs are stored in `~/.syn_launch/logs/`.

| Label | Meaning |
|---|---|
| INSTALLED | Executable with expected name appears in PATH; not a version/self-test. |
| TERMUX PKG | Attempts the named package using pkg. |
| PYTHON/PIP | Installs in an isolated virtual environment; dependency compatibility varies. |
| GO BUILD | Attempts go install using the listed upstream module. |
| MANUAL | No verified automatic Termux install recipe. |
| ROOT/HW | Needs root, kernel permissions, adapters, or other hardware. |

## Responsible use

Use scanning, fuzzing, proxying, enumeration, and auditing only against systems, apps, accounts, and networks you own or have explicit permission to test. Confirm scope and rate limits before active tests. Do not use the catalog to invade privacy, access accounts without permission, disrupt services, or collect data unlawfully. PhoneInfoga and similar tools do **not** reveal live GPS location merely from a phone number.

SYN_LAUNCH does not automatically launch scans against targets. Review example commands and replace placeholders only with authorized test values.

## Credits and upstream projects

SYN_LAUNCH is a launcher/catalog, not the author of the listed utilities. Respect each upstream project's license, attribution, API rules, and terms of service. Each entry includes a source field pointing to its project, package index, or a repository search when a definitive upstream link has not been verified.

Notable projects include [Nmap](https://nmap.org/), [PhoneInfoga](https://github.com/sundowndev/phoneinfoga), [theHarvester](https://github.com/laramies/theHarvester), [Sherlock](https://github.com/sherlock-project/sherlock), [Maigret](https://github.com/soxoj/maigret), [SpiderFoot](https://github.com/smicallef/spiderfoot), [ProjectDiscovery](https://github.com/projectdiscovery), [OWASP ZAP](https://www.zaproxy.org/), [sqlmap](https://github.com/sqlmapproject/sqlmap), [ffuf](https://github.com/ffuf/ffuf), [Gitleaks](https://github.com/gitleaks/gitleaks), [YARA](https://github.com/VirusTotal/yara), [radare2](https://github.com/radareorg/radare2), and [Termux packages](https://github.com/termux/termux-packages).

## Development checks

~~~bash
python -m unittest discover -s tests -v
python -m py_compile main.py
python main.py --check
~~~

GitHub Actions runs syntax and catalog checks. Those checks do not claim to install or execute every upstream tool.

## Roadmap

- Verify package names against current Termux repositories and ARM64 builds.
- Add per-tool version checks and upstream release verification.
- Add favorites/history and exportable audit notes.
- Consider a GUI after the CLI catalog and installation paths are reliable.

## License

SYN_LAUNCH code is released under the MIT License. Third-party tools retain their own licenses and terms.
