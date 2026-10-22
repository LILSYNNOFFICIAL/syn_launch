# Using SYN_LAUNCH: Practical User Guide

SYN_LAUNCH is a menu-driven catalog and installer for command-line tools, with diagnostics and compatibility reporting for Termux on Android. This guide explains how to launch the app, find tools, interpret their entries, install carefully, and use tools responsibly.

## 1. Start the application

From the repository directory in Termux:

```bash
cd ~/syn_launch
python main.py
```

If it is not installed yet, follow [Installation and first run](Installation.md). The main menu lets you browse categories, search the catalog, inspect tool details, manage custom entries and favorites, and use supported install workflows.

## 2. Find a tool

```bash
python main.py --list
python main.py --search nmap
python main.py --category "Network & DNS"
python main.py --tool curl
python main.py --check
```

- **List** displays catalog entries.
- **Search** finds matching tools by name and supported metadata.
- **Category** filters by the configured category.
- **Tool** displays the selected entry's description, install path, example, source, and caveats.
- **Check** validates the catalog and reports a concise runtime summary.

Use the exact category spelling shown in the menu or catalog.

## 3. Understand a catalog entry

Each entry includes its purpose, installation method, example command, upstream source, and caveats where known. Compatibility metadata may also identify source revisions, platform notes, root or hardware requirements, external services, and known blockers.

These states are different:
- **Cataloged:** an entry exists.
- **Installable:** an install method is declared; success is not guaranteed.
- **Detected:** an executable or runtime was found; functionality is not proven.
- **Source-documented:** upstream source or packaging evidence was reviewed for a limited claim.
- **Smoke-tested / functionally checked:** a bounded test covered a specific capability.
- **Device-verified:** direct evidence exists for the relevant device and operation.

See [Compatibility and verification](Compatibility-and-Verification.md).

## 4. Install carefully

SYN_LAUNCH supports declared installation methods such as Termux packages, Python packages, Go modules, Cargo packages, and npm packages. Some entries are manual-only or have platform constraints. Review prompts and the selected tools before confirming individual or batch installs.

Native dependencies, CPU architecture, Android version, root requirements, hardware, and permissions may block installation or features. An installer completing successfully is not proof the tool runs correctly. For manual-only entries, follow the upstream project's current instructions.

## 5. Read and adapt example commands

Catalog examples teach basic syntax; they may not be a complete workflow. Before running one:

1. Read the linked upstream documentation and check the installed version's help output.
2. Understand arguments, file changes, network traffic, and possible remote-state changes.
3. Use only hosts, paths, accounts, and identifiers you own or are explicitly authorized to assess.
4. Prefer local files, labs, and non-destructive/read-only options where possible.
5. Store output securely and never expose credentials, tokens, personal data, or assessment results.

Do not copy commands blindly or run network assessments against third-party targets without explicit authorization.

## 6. Tool guides by category

The catalog has **19 categories and 269 entries**. Each category guide explains what every listed tool is used for, provides the catalog example when available, and links to upstream sources and relevant packaging evidence.

- [Termux Core](Using-termux-core.md) — 25 tools
- [Network & DNS](Using-network-and-dns.md) — 23 tools
- [OSINT & Recon](Using-osint-and-recon.md) — 25 tools
- [Web App Testing](Using-web-app-testing.md) — 22 tools
- [Audit, SAST & Supply Chain](Using-audit-sast-and-supply-chain.md) — 20 tools
- [Forensics & File Analysis](Using-forensics-and-file-analysis.md) — 21 tools
- [Cryptography & Password Hygiene](Using-cryptography-and-password-hygiene.md) — 12 tools
- [Wireless & Android Environment](Using-wireless-and-android-environment.md) — 10 tools
- [Cloud, Containers & Misc](Using-cloud-containers-and-misc.md) — 26 tools
- [Advanced Pentest & Exploit Research](Using-advanced-pentest-and-exploit-research.md) — 26 tools
- [Web & API Assessment](Using-web-and-api-assessment.md) — 1 tools
- [Active Directory & Windows](Using-active-directory-and-windows.md) — 12 tools
- [Mobile App Security](Using-mobile-app-security.md) — 10 tools
- [Cloud & Container Security](Using-cloud-and-container-security.md) — 12 tools
- [Network & TLS Assessment](Using-network-and-tls-assessment.md) — 8 tools
- [Developer & Supply Chain Security](Using-developer-and-supply-chain-security.md) — 5 tools
- [Forensics & Reverse Engineering](Using-forensics-and-reverse-engineering.md) — 7 tools
- [Privacy & Metadata](Using-privacy-and-metadata.md) — 1 tools
- [Password & Authentication Auditing](Using-password-and-authentication-auditing.md) — 3 tools

## 7. Diagnostics and compatibility

```bash
python main.py --doctor
python main.py --profile
python main.py --compatibility-report > compatibility-report.json
bash device_check.sh
```

- `--doctor` reports detected platform/runtime information and install-method counts.
- `--profile` produces a machine-readable runtime profile.
- `--compatibility-report` separates declarations from evidence.
- `device_check.sh` runs project checks and bounded diagnostics. Review output before sharing it.

Diagnostics do not prove that every cataloged tool works; test the specific feature you need on the target device.

## 8. Custom tools and favorites

Use custom-tool and favorite options in the main menu to save personal metadata and find frequent entries. Custom entries do not install software or validate compatibility. Removing an entry does not uninstall software.

## 9. Safety, privacy, and scope

Use tools only on systems, applications, accounts, networks, and data you own or are explicitly authorized to assess. Prefer isolated labs and least-privilege credentials. Review possible impact before using scanners, exploit research tools, cloud utilities, directory collectors, password-auditing tools, or tools that modify remote state.

Keep reports private and redact secrets before sharing logs. Read [Security and responsible use](Security-and-Responsible-Use.md) and [Workflow planning](Workflow-Planning.md).

## Further reading

- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Troubleshooting](Troubleshooting.md)
- [Workflow planning](Workflow-Planning.md)
- [Published GitHub Wiki](https://github.com/LILSYNNOFFICIAL/syn_launch/wiki)
