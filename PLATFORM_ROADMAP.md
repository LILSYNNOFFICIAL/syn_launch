# SYN-LAUNCH Platform Roadmap

This document tracks the staged evolution from a Termux catalog/installer into a mobile-first security platform. It is a plan, not a claim that every capability already exists.

## Stage 1: Device and runtime intelligence

- [x] Detect OS, raw CPU machine string, normalized architecture family, Android/Termux signals, available runtimes, storage headroom, and process UID status.
- [x] Expose a stable, versioned JSON profile for future compatibility automation.
- [x] Explain that container/proot UID 0 is not proof of Android host root.
- [x] Add regression tests for architecture normalization and the CLI profile.
- [x] Run a baseline smoke test on one physical Android 16 / Termux / ARM64 device with Python 3.14.6 (commit `e81f9e58eba5b71e8aa8b18f6b6ac0cdce6a0f5e`); the test does not validate individual cataloged tools.
- [ ] Run `bash device_check.sh` on the physical Android/Termux device, inspect the private evidence bundle, then perform human-reviewed device validation; validate 32-bit/other supported architectures separately.

## Stage 2: Compatibility metadata

- [x] Maintain 172 source-backed declarations: 103 Termux package-recipe entries from revision `e85983636adcf748134c3feb1df27f44e78322e1`, seven root-packages recipe entries from revision `06591fc024101b04095ec4417d51907512b46e3c`, 22 pinned Python packaging-metadata reviews, and forty pinned Go module reviews. Each records evidence scope and blockers; none is device verification.
- [x] Review and pin upstream Python packaging metadata for 22 tools, recording declared Python requirements or the absence of an explicit minimum, dependencies, and known service/build caveats without implying Android support. The additional reviews include holehe, dnstwist, Wapiti, Wfuzz, WAFW00F, Arjun, hashID, Passlib, bcrypt, ROPGadget, and Ropper.
- [x] Add pinned recipe evidence for xh, feroxbuster, curlie, hping3, and arp-scan; move xh, feroxbuster, and curlie to Termux `pkg` installation paths where the main Termux recipe exists. Keep hping3 and arp-scan non-installable by default because their recipes live in the separate root-packages repository.
- [x] Add 18 more pinned main-repository recipe reviews for Gitleaks, cargo-audit, govulncheck, strace, ltrace, Docker CLI, kubectl, rclone, restic, RustScan, JADX, Apktool, SSLScan, ProxyChains-NG, gosec, Rizin, Crunch, and steghide; expose their package-manager paths while retaining explicit runtime, permission, and active-use caveats.
- [x] Add pinned root-repository recipe evidence for `iw`, Aircrack-ng, and TShark while leaving them non-installable by default pending repository and device-capability verification.
- [x] Add forty pinned Go module metadata reviews for subfinder, dnsx, httpx, naabu, gau, waybackurls, katana, unfurl, ffuf, gobuster, PhoneInfoga, Nuclei, Kiterunner, KXSS, CRLFuzz, Interactsh, Tlsx, MapCIDR, Uncover, ASNMap, anew, qsreplace, hakrawler, Chisel, Alterx, Shuffledns, PureDNS, gowitness, kubeaudit, kube-linter, gauplus, TruffleHog, OSV-Scanner, Kerbrute, CloudFox, kubeletctl, Cosign, Terrascan, staticcheck, and Dockle; record the Go directive and keep the unpinned `@latest` installer caveat explicit.
- [ ] Continue reviewing the remaining 97 catalog entries without compatibility declarations; prioritize exact upstream recipe or packaging evidence and keep unknown Android support explicitly unverified.
- [x] Keep unknown compatibility explicitly unknown; never infer "works" merely because a package exists or an executable is in PATH.
- [x] Add a report that separates catalog installability, PATH evidence, compatibility assessment, smoke-test evidence, and device-validation evidence.
- [x] Expand the curated subset using the live upstream Termux repository tree; the schema labels entries `source_documented_not_device_verified`, requires HTTPS evidence URLs, and validates the evidence-scope field.
- [x] Add source-backed metadata for Termux-packaged network, forensics, developer, and core utilities where a matching upstream recipe or subpackage definition was found.
- [ ] Review upstream runtime/platform documentation for tools not distributed by the Termux package recipes; do not infer support from install commands alone.

## Stage 3: Reliable tool lifecycle

- [x] Record batch operation outcomes separately from before/after PATH matches, and label functional verification as not run.
- [x] Capture the most recent installer subprocess command, exit code, timeout/launch error, timestamps, and output bounds in batch summaries; entries that never launched a subprocess retain a null exit code.
- [x] Record requested package specs and explicit Go module version requests in each batch result; mark unpinned packages and unresolved versions honestly.
- [x] Collect resolved-version metadata for Termux packages (`dpkg-query`) and isolated Python packages (`importlib.metadata`), with explicit query status and no inferred version when evidence is absent.
- [x] Extend resolved-version collection to Go build metadata, Cargo install metadata, and global npm package metadata without launching cataloged tool executables.
- [x] Reconcile explicit Go version requests against resolved metadata with exact-match, mismatch, unresolved, unpinned/not-comparable, and floating-request states; do not infer semantic equivalence.
- [x] Add bounded metadata-only post-install checks using package-manager records and PATH discovery, with explicit status and no execution of cataloged tool binaries.
- [x] Add explicitly confirmed single-package uninstall for Termux, isolated pip, Cargo, and global npm, with before/after metadata and private audit records; leave Go/manual/root uninstall unsupported until package ownership can be established safely.
- [x] Add explicitly confirmed single-package updates for Termux, isolated pip, Go, Cargo, and global npm with before/after metadata and private audit records; update operations are not automatically reversible and do not claim compatibility.
- [x] Add advisory dependency/runtime and disk-space preflight checks before bulk installs; missing `pkg` blocks package batches, while other warnings require explicit continuation. Exact package sizes and tool functionality remain unverified.

## Stage 4: Authorized assessment workflows

- [x] Add scope-bound, dry-run workflow plans for web/API review, mobile-app review, local device/Termux configuration audit, and assessment reporting.
- [x] Require an explicit target-scope string and operator authorization declaration to emit a plan; validate printable scope length and reject unknown workflow IDs.
- [x] Include stop conditions and explicit no-network/no-subprocess execution fields in every plan.
- [x] Add reviewed adapters for local Termux/device inventory, static APK archive inventory, and local JSON evidence-report generation; these do not make network requests or execute catalog tools.
- [x] Add a narrowly scoped HTTPS adapter that sends one certificate-verified HEAD request with a five-second timeout, no redirect following, no body read, URL scope validation, and allowlisted response headers.
- [x] Add adapter regression tests for scope rejection, invalid APKs, archive/resource limits, evidence schema/severity validation, authorization gates, and private report persistence.
- [ ] Test the HTTPS HEAD adapter against an explicitly authorized staging endpoint. Current automated tests mock the connection and do not count as real staging verification.
- [ ] Add further remote web/API adapters only after per-tool safety review, explicit per-step confirmation, bounded requests, output limits, stop conditions, and authorized staging tests.
- [ ] Add signature-aware APK analysis only after a reviewed parser/verifier implementation; current inventory does not verify signatures or decode the binary manifest.
- Do not launch scans automatically or treat a discovered host as permission to test it.

## Stage 5: Optional Linux environments

- [x] Review upstream PRoot-Distro capabilities and limitations; document that simulated root is not host root and kernel-dependent features remain unavailable: [PRoot-Distro](https://github.com/termux/proot-distro).
- [x] Review official Kali NetHunter editions and requirements; document Rootless, Lite, and full NetHunter as distinct capability profiles: [NetHunter overview](https://www.kali.org/docs/nethunter/) and [Rootless guide](https://www.kali.org/docs/nethunter/nethunter-rootless/).
- [x] Document hardware, kernel, root, and ABI caveats without implying a userspace image grants kernel features or Android host root.
- [x] Add read-only presence indicators for PRoot, PRoot-Distro, and NetHunter launchers/rootfs markers to the local audit; do not enter containers or infer privileges.
- [ ] Validate those indicators on the physical Android/Termux device and document its actual environment. No environment is installed, reset, or flashed automatically.

## Release gates

- CI validates Python syntax, shell syntax, catalog schema, and unit/regression tests.
- Device compatibility claims require actual device evidence and must name the tested Android version, Termux source, architecture, and tool version.
- Security changes require tests for unsafe input, untrusted environment overrides, subprocess timeouts, and failure paths.

## Documentation and evidence maintenance

- [x] Add [Optional Linux Environments](wiki/Optional-Linux-Environments.md) with upstream PRoot-Distro and Kali NetHunter sources, edition differences, and support boundaries.

- [x] Add a repository-hosted wiki under `wiki/` with installation, compatibility, lifecycle, security, troubleshooting, and contributor pages.
- [x] Document the physical-device test as a historical baseline tied to its exact commit, not a current release guarantee.
- [x] Add an explicit single-tool bounded `--smoke-test NAME_OR_ID` mode, privately persist probe outcomes, and expose saved evidence in report schema 3 without changing device-validation status.
- [x] Add CI coverage for the bounded Python runtime smoke test and schema-3 compatibility report.
- [x] Re-run the full test suite and CLI/report checks after the documentation, workflow, and smoke-evidence changes; GitHub Actions passed on Python 3.10, 3.12, and 3.14, including the bounded smoke test and schema-3 report assertions.
- [ ] Repeat physical-device checks after the compatibility validator and smoke-test/report changes. CI on a desktop runner cannot substitute for Android/Termux evidence.
