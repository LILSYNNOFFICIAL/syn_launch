# SYN_LAUNCH

[![Termux](https://img.shields.io/badge/platform-Termux%20%2F%20Android-00BCD4?logo=android&logoColor=white)](https://termux.dev/)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Catalog](https://img.shields.io/badge/catalog-269%2B%20entries-brightgreen)](catalog.json)
[![Use](https://img.shields.io/badge/use-authorized%20testing-orange)](#responsible-use)

**A mobile-first security platform foundation for Termux: searchable tool catalog, installer, and device/runtime diagnostics.**

SYN_LAUNCH groups security and developer tools into numbered menus. Select a tool to see its purpose, installation method, compatibility caveats, upstream source, and example command. Local version/help probes are available only after you explicitly choose Help. The installer can attempt supported Termux packages and opt-in Python, Go, and Cargo installs.

> **Important:** cataloged does not mean installed, compatible, or verified on every phone. Termux is not desktop Linux. Android permissions, kernel features, CPU architecture, package repositories, Python wheels, native libraries, external adapters, and root access all affect compatibility. The app reports install attempts and does not claim a tool works until it is actually detected in PATH.

## Quick start

Install Termux from a maintained source such as [F-Droid](https://f-droid.org/packages/com.termux/) or the [official Termux GitHub](https://github.com/termux/termux-app). Do not mix Termux apps/plugins from incompatible signing sources.

~~~bash
pkg update -y
pkg install -y git python
git clone https://github.com/LILSYNNOFFICIAL/syn_launch.git
cd syn_launch
bash install.sh
~~~

Start the app:

~~~bash
python main.py
~~~

Rich is optional; without it the app uses a plain-text interface.

## Command-line modes

~~~bash
python main.py --check
python main.py --list
python main.py --search nuclei
python main.py --category "Mobile App Security"
python main.py --tool Nmap
~~~

- `--check` validates the catalog and reports a concise runtime summary.
- `--doctor` reports architecture, Android/Termux signals, process UID, free storage, available runtimes, and catalog install-method counts.
- `--profile` prints a machine-readable JSON runtime profile. Detection signals do not certify individual tools as compatible.
- `--list` lists the catalog and current PATH-based status.
- `--search` searches tool names, categories, and descriptions.
- `--category` lists tools from a category.
- `--tool` displays a tool's metadata without executing the local binary. In the interactive menu, choose Help to request bounded help/version probing.

## Personal catalog and favorites

Use **Custom tools / favorites** in the main menu to add a tool entry without editing the project files, browse or remove your custom entries, and favorite frequently used tools. Personal entries are stored separately in `~/.syn_launch/custom_tools.json`; favorites are stored in `~/.syn_launch/favorites.json`. These files are user-local and are not committed to the GitHub repository. Custom entries go through the same ID, HTTPS-source, install-method, and package syntax checks as the built-in catalog. Adding an entry saves metadata only; it does not install the tool. Removing an entry does not uninstall its software.

## What's included

**269 catalog entries across 19 categories.** Coverage includes:

- **Termux Core**
- **Network & DNS**
- **OSINT & Recon**
- **Web App Testing**
- **Audit, SAST & Supply Chain**
- **Forensics & File Analysis**
- **Cryptography & Password Hygiene**
- **Wireless & Android Environment**
- **Cloud, Containers & Misc**
- **Advanced Pentest & Exploit Research**
- **Web & API Assessment**
- **Active Directory & Windows**
- **Mobile App Security**
- **Cloud & Container Security**
- **Network & TLS Assessment**
- **Developer & Supply Chain Security**
- **Forensics & Reverse Engineering**
- **Privacy & Metadata**
- **Password & Authentication Auditing**

Advanced entries include Nuclei, Dalfox, Ghauri, RustScan, Kiterunner, ffuf, Gobuster, Subfinder, dnsx, Katana, Naabu, Uncover, PureDNS, gau, gospider, Hakrawler, Gitleaks, OSV-Scanner, Checkov, Bandit, pip-audit, Syft, Grype, Cosign, Terrascan, Semgrep, Trivy, mitmproxy, SSLyze, testssl.sh, YARA, capa, Apktool, APKiD, JADX, angr, pwndbg, RustHound-CE, Cloudsplaining, kube-linter, Dockle, staticcheck, gowitness, steghide, and Pacu. Some entries are intentionally manual-only where a reliable Termux install path is not established.

Some high-impact or desktop-focused projects such as Metasploit, Responder, Hydra, Hashcat, masscan, JADX, and MobSF are explicitly marked manual-only or compatibility-limited. SYN_LAUNCH does not silently root the phone or claim these work on stock Android.

## Installation behavior

The Installer menu provides:

1. **Termux packages:** attempts each distinct package name in the catalog using `pkg`. Some package names may not exist for your repository or architecture.
2. **One tool:** installs one selected tool using its declared method.
3. **Toolchain prerequisites:** attempts Python, Go, Rust, and Node.js runtime packages where cataloged.
4. **Python/Go/Cargo/npm batch:** opt-in attempt of all declared third-party installs. This can consume substantial bandwidth/storage, compile for a long time, and fail when upstream dependencies are incompatible with Android.
5. **Last install summary:** shows successful attempts and failures from the last batch.

Each bulk action requires an explicit confirmation. Individual third-party installs require typing `INSTALL`. Manual/root entries do not pretend to install automatically.

| Status | Meaning |
|---|---|
| INSTALLED | An executable with the expected name is present in PATH. This is not a full self-test. |
| TERMUX PKG | The installer can attempt the named Termux package. |
| PYTHON/PIP | Installs into an isolated virtual environment under `~/.syn_launch/venv`. |
| GO BUILD | Uses `go install` and places generated binaries in `~/.local/bin`. |
| CARGO BUILD | Uses `cargo install --locked`; native compilation may fail on Android. |
| NPM PACKAGE | Uses the configured npm package name if a catalog entry uses this method. |
| MANUAL | No verified automatic Termux install path is provided. |
| ROOT/HW | Requires root, kernel permissions, special hardware, or another environment constraint. |

The progress bar counts completed attempts, not downloaded bytes. Command output is capped at 10 MiB per subprocess to limit log growth; remaining output is drained without being retained. Output is logged under `~/.syn_launch/logs/`; log files are restricted to the current user where Android filesystem permissions allow it. The app does not store target lists or run scans automatically.

## Security and supply-chain safeguards

- Uses argument arrays rather than shell command strings for package installation.
- Validates package/module syntax inside the catalog itself, not just at install time.
- Removes environment-based package-source overrides before installer subprocesses. Python installs use pip isolated mode and the official PyPI index; Go installs use the official Go proxy/checksum database; npm installs pin the official registry and require TLS verification.
- Duplicate display names are rejected to keep catalog selection unambiguous.
- The bootstrap verifies the official HTTPS Git origin, requires a clean checkout on `main`, disables Git hooks during repository operations, and installs Python dependencies through isolated pip against the official PyPI index.
- Validates upstream links as HTTPS URLs with a hostname and rejects embedded URL credentials.
- Validates executable names, boolean install flags, and metadata lengths before a catalog entry is accepted.
- Browsing a tool no longer executes its local binary. Version/help probing occurs only after the user explicitly chooses Help.
- Caps displayed and logged installer output at 10 MiB, and caps explicit help/version probe output at 64 KiB, while continuing to drain process pipes. This reduces log-flood and memory/disk-exhaustion risk.
- Validates catalog IDs, install methods, HTTPS source links, and package/module syntax before use.
- Uses an isolated Python virtual environment instead of installing Python security packages into Termux's system Python.
- Installs Go binaries into a dedicated user bin directory.
- Applies timeouts to subprocess operations and terminates timed-out process groups where supported.
- Stores install logs and summaries with restrictive file permissions where supported.
- Requires explicit confirmation for third-party package/build installation.
- Does not request root, execute a scan on startup, or automatically act on a discovered target.
- Does not treat a PATH match as proof that a tool works. Local help/version probing is best-effort and bounded by time/output limits.

**Supply-chain note:** Python, Go, Cargo, npm, and Termux package managers execute third-party code or build scripts. Confirm the package name, maintainer, and project source before installing. This repository links upstream projects but does not independently audit every release. For high-assurance use, review and pin versions/commits before installing in a sensitive environment.

## Responsible use

Use reconnaissance, scanners, fuzzers, proxies, password-auditing tools, and exploitation frameworks only on systems, apps, accounts, and networks you own or have explicit written permission to assess. Confirm target scope, rate limits, test windows, and stop conditions. Avoid actions that disrupt services or expose real user data.

Some tools can trigger account lockouts, execute commands on vulnerable systems, change cloud/directory state, or capture sensitive traffic. They are labeled with specific caveats. Protect reports, logs, tokens, hashes, and collected directory data. PhoneInfoga and similar services **do not reveal live GPS location merely from a phone number**.

## Platform roadmap

See [PLATFORM_ROADMAP.md](PLATFORM_ROADMAP.md) for the staged plan covering compatibility metadata, verified tool lifecycle, authorized assessment workflows, and optional Linux environments.

## Development and verification

Run these checks locally:

~~~bash
python -m py_compile main.py
bash -n install.sh
python -m unittest discover -s tests -v
python main.py --check
~~~

GitHub Actions runs syntax, bootstrap-shell, JSON, catalog-integrity, CLI, bootstrap-security and regression checks on pushes and pull requests. CI success on Ubuntu does not prove that a package installs or runs on Android/Termux. Real device testing is still required for Termux compatibility.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for catalog requirements, package-safety rules, testing, and upstream attribution. Report security issues privately using GitHub's security reporting feature when available; see [SECURITY.md](SECURITY.md).

## Credits and licenses

SYN_LAUNCH is a launcher/catalog, not the author of the listed tools. The catalog links each entry to a project or documentation source where known. Each upstream project retains its own license, trademark, API terms, and attribution requirements. Verify license and distribution conditions before bundling or redistributing any third-party software.

## License

SYN_LAUNCH code is released under the MIT License. Third-party tools retain their own licenses and terms.
