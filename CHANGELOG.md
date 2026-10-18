# Changelog

Notable user-facing changes to SYN_LAUNCH are recorded here. This file tracks repository changes; it does not certify device compatibility.

## Unreleased

- Added eleven revision-pinned Python compatibility reviews for JWT Tool, Corsy, XSStrike, Commix, tplmap, RouterSploit, Ghauri, MobSF, Pacu, Metagoofil, and BloodHound.py, plus Go module metadata for Actionlint and Rust workspace metadata for Zizmor and YARA-X. Language metadata is evidence only, not Android/Termux support.

- Added 23 pinned recipe-backed compatibility reviews across two expansions: xh, feroxbuster, curlie, hping3, arp-scan, Gitleaks, cargo-audit, govulncheck, strace, ltrace, Docker CLI, kubectl, rclone, restic, RustScan, JADX, Apktool, SSLScan, ProxyChains-NG, gosec, Rizin, Crunch, and steghide. Updated catalog install paths where the main Termux package recipes exist; root-repository packet/wireless tools remain non-installable by default.
- Increased the source-backed compatibility declaration count from 95 to 121 and reduced the remaining unreviewed catalog entries from 174 to 148.
- Added pinned `termux-root-packages` recipe evidence for `iw`, Aircrack-ng, and TShark while retaining non-installable defaults.
- Added 21 pinned Python packaging reviews in this continuation across two batches, including holehe, dnstwist, Wapiti, Wfuzz, WAFW00F, Arjun, hashID, Passlib, bcrypt, ROPGadget, Ropper, mitmproxy, Semgrep, Safety, Checkov, Certbot, SSLyze, Ansible, pwntools, Impacket, Androguard, SpiderFoot, NetExec, Certipy, LDAPDomainDump, enum4linux-ng, Coercer, BloodyAD, Frida Tools, Objection, ApkLeaks, Prowler, ScoutSuite, Kube-Hunter, Volatility 3, Cloudsplaining, and APKiD; Android build/runtime support remains unverified.
- Added thirty pinned Go module reviews for subfinder, dnsx, httpx, naabu, gau, waybackurls, katana, unfurl, ffuf, gobuster, PhoneInfoga, Nuclei, Kiterunner, KXSS, CRLFuzz, Interactsh, Tlsx, MapCIDR, Uncover, ASNMap, anew, qsreplace, hakrawler, Chisel, Alterx, Shuffledns, PureDNS, gowitness, kubeaudit, kube-linter, gauplus, TruffleHog, OSV-Scanner, Kerbrute, CloudFox, kubeletctl, Cosign, Terrascan, staticcheck, and Dockle; the catalog's `@latest` install selectors remain unpinned.

### Compatibility evidence
- Expanded structured, source-linked compatibility declarations to 95 entries: 84 Termux recipe-backed declarations spanning 66 distinct recipe/subpackage directories, using pinned revisions of `termux-packages` and `termux-root-packages`, plus eleven pinned upstream Python packaging metadata reviews for pip-audit, yamllint, dirsearch, Sherlock, Bandit, detect-secrets, email-validator, ssh-audit, Maigret, h8mail, and theHarvester. Source links are pinned and evidence scope is explicit.
- Added an explicit evidence-scope field, pinned upstream source revisions and snapshot URLs, and CI checks for reproducible compatibility evidence.
- Kept recipe presence, catalog installability, PATH discovery, smoke-test outcome, and device validation as separate evidence states.

- Added `bash device_check.sh` to gather a private, read-only local diagnostic bundle including optional PRoot/NetHunter presence markers; CI exercises the script but does not substitute for Android/Termux testing.

### Authorized workflow planning
- Added dry-run JSON plans for web/API review, mobile-app review, local device/Termux configuration audit, and assessment reporting.
- Require an explicit scope and literal boolean authorization confirmation before a plan can be emitted.
- Plans include stop conditions and explicitly record that no network actions or subprocesses were executed.
- Added CLI integration and regression tests for authorization handling, invalid scopes, and dry-run behavior.
- Added read-only local device inventory, static APK archive inventory, and local JSON evidence-report adapters. APK inventory does not extract, execute, or verify signatures, and evidence summaries do not independently validate findings.
- Added a narrowly scoped HTTPS HEAD adapter with TLS certificate verification, strict URL validation, a five-second timeout, no redirects, no response-body reads, and allowlisted headers. It sends one real network request and still requires testing against an authorized staging endpoint.
- Added a sample JSON evidence bundle and regression coverage for the local report workflow.

### Bounded smoke testing
- Added `python main.py --smoke-test NAME_OR_ID` for one explicitly selected catalog entry.
- Probe order is `--version`, `--help`, then `-h`; each probe has a five-second timeout and a 64 KiB output cap.
- Saves only probe metadata/outcomes, not raw output, to private `~/.syn_launch/smoke_tests.json`.
- Records exit status, timeout, truncation, and per-probe attempts. A passing probe means a help/version response exited successfully, not that operational features work.
- Compatibility report schema 3 includes saved evidence and marks it stale when the current executable path or lightweight file identity differs.
- CI now runs the bounded Python probe and validates the resulting report while explicitly asserting that device-validation count remains zero.

### Documentation
- Updated the README, roadmap, contributor and security guidance, and repository-hosted wiki pages for the expanded metadata and smoke-test workflow.
- The wiki is versioned under `wiki/` in this repository. It is not the separate GitHub Wiki feature.

### Still requires physical-device verification
- The previous Android 16 / Termux / ARM64 baseline applies only to its recorded commit.
- The latest code has CI coverage on Python 3.10, 3.12, and 3.14, but still needs a fresh run on an actual Android/Termux device and validation across additional ABIs.
