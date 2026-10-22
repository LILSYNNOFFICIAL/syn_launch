# Compatibility and verification model

SYN_LAUNCH reports distinct evidence levels to prevent overclaiming.

| Evidence | Meaning | Does not prove |
|---|---|---|
| Catalog entry | Metadata exists in `catalog.json` | Package exists or tool works |
| Catalog installable | An install method is configured | Install will succeed on this device |
| PATH match | An executable with the expected name is discoverable | It is the intended tool or functions |
| Source-documented declaration | Upstream documentation/package recipe supports the declared install route and caveats | Device compatibility or successful execution |
| Install metadata | Package manager reports package/version metadata | Functional correctness |
| Smoke test | A specific bounded command ran with recorded outcome | All features work |
| Device validation | A named tool/version was tested on a named device/OS/architecture | Universal support on other devices |

## Current source-backed subset

The catalog now has 267 source-backed declarations. One hundred ten recipe-backed entries map to 92 distinct recipes or subpackage definitions: 103 are pinned to `termux-packages` revision `e85983636adcf748134c3feb1df27f44e78322e1`, and seven are pinned to `termux-root-packages` revision `06591fc024101b04095ec4417d51907512b46e3c`. Sixty-seven Python packaging/dependency or runtime-documentation entries (pip-audit, yamllint, dirsearch, Sherlock, Bandit, detect-secrets, email-validator, ssh-audit, Maigret, h8mail, and theHarvester, plus holehe, dnstwist, Wapiti, Wfuzz, WAFW00F, Arjun, hashID, Passlib, bcrypt, ROPGadget, and Ropper) pin upstream packaging metadata and record declared Python requirements only. Each declaration carries a `source_revision` and `source_snapshot_url` so reviewers can inspect the exact evidence snapshot. This includes core utilities and selected networking, developer, and file-analysis tools. Metadata links to the actual recipe directory where possible (for example, curl uses `libcurl`, SQLite uses `libsqlite`, and OpenSSH keyscan uses the `openssh` recipe). Recent additions cover xh, feroxbuster, curlie, hping3, arp-scan, Nmap, ShellCheck, YARA, radare2, Tesseract OCR, ClamAV, OpenSSH keyscan, MTR, and tcpdump. xh, feroxbuster, and curlie now use main-repository `pkg` installation paths. hping3 and arp-scan remain non-installable by default because their recipes require the separate root-packages repository and raw-packet capabilities. MTR and tcpdump links point to the separate upstream `termux-root-packages` repository; capture and raw-socket permissions remain device-specific. The status remains `source_documented_not_device_verified`. Recipe presence does not prove the package is enabled for the current device ABI, installable from the configured repository, or functional.

## Current report behavior

`python main.py --compatibility-report` emits report schema 4. The report itself does not launch cataloged executables; it reads previously saved evidence. `python main.py --smoke-test NAME_OR_ID` performs bounded tool-specific help/version probes, each capped at five seconds and 64 KiB. It stores outcome and metadata in private `~/.syn_launch/smoke_tests.json`; a passing probe is not a feature test. `python main.py --functional-check NAME_OR_ID` runs one explicitly selected, reviewed local-only adapter when available. These adapters use fixed argument arrays, temporary directories, five-second per-command timeouts, and a combined 64 KiB stdout/stderr cap enforced while the child runs. Checks include local JSON/copy/database/archive/hash/compiler/Git operations, curl against a `file://` URL, offline npm package metadata, a temporary make target, SSH configuration expansion without connecting, and scoped `ps`/`lsof` inspection of the current process and a temporary file. No network requests or package/device-setting changes are made by these adapters. Unsupported executables are not run and return a nonzero CLI exit status so automation cannot mistake an unexecuted check for a pass. Network/probing tools (`wget`, `ping`, `telnet`, `ssh-keyscan`), interactive tools (`nano`, `less`, `watch`), device-state-changing tools (`termux-wake-lock`), app-launching tools (`termux-open`), and environment-reporting tools (`termux-info`, `ifconfig`) intentionally have no functional adapter. Functional results are stored separately in `~/.syn_launch/functional_checks.json`; a result becomes `stale_evidence` when its executable path or lightweight file identity changes. A pass means only the specific named assertion passed, not full tool compatibility, security, or complete feature verification. Device validation remains `not_run`.

## Outstanding manual-entry assessments

Two entries are intentionally reference-only and remain unassessed for native Termux execution:

- **Burp Suite:** PortSwigger's published desktop system requirements list Windows, Linux (Intel/ARM 64-bit), and macOS, but do not list Android/Termux. No native Termux installation path or runtime evidence is recorded. See the [official system requirements](https://portswigger.net/burp/documentation/desktop/getting-started/system-requirements).
- **Wappalyzer:** the public [npm package](https://www.npmjs.com/package/wappalyzer) is deprecated and says it is no longer maintained. The [HTTP Archive repository](https://github.com/HTTPArchive/wappalyzer) is a fork of the last open-source version; that does not establish current official CLI support or Termux execution. See also the [current Wappalyzer API](https://www.wappalyzer.com/api/).

These entries remain `installable: false` and manual-only. Do not add source-backed compatibility declarations merely because a project or archived source exists. Reassess only if an authoritative, current install path and evidence for the claimed environment become available.

## External HTTPS adapter validation

The `web-api-review` adapter sends one initial HTTPS `HEAD` request and follows at most three redirects that remain on the exact same hostname. It records each hop's status, normalized host/path, and allowlisted response headers, without reading response bodies or retaining raw `Location` values. Redirects to a different hostname are recorded as out of scope and are not followed. The adapter rejects credentials, query strings, fragments, non-default ports, parent-directory path segments, and hostnames resolving to non-public IP addresses. This is an active network check, not a local-only diagnostic.

After an authorized staging URL is supplied, run this from the repository root in Termux, replacing the placeholder with a URL you own or have explicit written permission to test:

```bash
python main.py --workflow-run web-api-review --target-scope "https://YOUR-AUTHORIZED-STAGING-HOST/" --authorized
```

Do not run the placeholder literally. Save the report privately and review the status, redirect chain, and allowlisted response headers. A response proves only that the bounded request chain received a response; it does not prove application security or full API functionality. An initial check against the owner-authorized scope `https://meepsheep.com/` returned `307 Temporary Redirect`. The redirect destination was not captured by the earlier one-request adapter version; rerun the check with the current bounded-redirect implementation to establish whether the destination stays on the authorized hostname.
## Adding evidence

1. Prefer the project's official install documentation or the exact package recipe.
2. Link to the HTTPS source and state what it establishes.
3. Document architecture, root, hardware, external-service, and known-blocker details only when supported.
4. Keep the status `source_documented_not_device_verified` until real device evidence exists.
5. For device validation, record device model/OS, Termux source, architecture, tool/package version, command, exit status, and test limits. Keep a bounded CLI smoke probe distinct from a device-level functional test.


The latest pinned recipe reviews cover `xh`, `feroxbuster`, `curlie`, `hping3`, and `arp-scan`. The first three now use Termux `pkg` install paths backed by the main Termux package repository. `hping3` and `arp-scan` are documented against the separate root-packages repository but remain disabled for automated installation by default. All five remain unverified on a physical device.


Additional pinned main-repository recipe reviews now cover Gitleaks, cargo-audit, govulncheck, strace, ltrace, Docker CLI, kubectl, rclone, restic, RustScan, JADX, Apktool, SSLScan, ProxyChains-NG, gosec, Rizin, Crunch, and steghide. Their catalog install paths use Termux `pkg`; this records a source-backed install route, not successful installation or runtime support on a particular Android device. Docker CLI still needs a usable daemon, tracing depends on Android kernel restrictions, and network scanners must only be used against authorized targets.


Three additional pinned root-repository recipe reviews cover `iw`, Aircrack-ng, and TShark. These remain non-installable by default: `iw` and Aircrack-ng depend on wireless driver/firmware and privilege capabilities, while TShark packet capture depends on interface access and permissions. Recipe presence is not evidence that these capabilities work on stock Android.


Forty-eight Go module metadata reviews have been added for subfinder, dnsx, httpx, naabu, gau, waybackurls, katana, unfurl, ffuf, gobuster, PhoneInfoga, Nuclei, Kiterunner, KXSS, CRLFuzz, Interactsh, Tlsx, MapCIDR, Uncover, ASNMap, anew, qsreplace, hakrawler, Chisel, Alterx, Shuffledns, PureDNS, gowitness, kubeaudit, kube-linter, gauplus, TruffleHog, OSV-Scanner, Kerbrute, CloudFox, kubeletctl, Cosign, Terrascan, staticcheck, and Dockle, plus Trivy, Grype, Syft, kube-bench, and Ligolo-ng. Each records the pinned `go.mod` revision and declared Go version. Several recent projects require Go 1.26+; their toolchain requirements and large dependency graphs may exceed the device's installed Go version or build resources. The catalog's `@latest` install selectors remain unpinned, and module metadata does not prove that the current Termux toolchain or dependencies build on the device.

Nineteen other native/runtime reviews cover massdns (C11/Make), Lynis (Unix shell audit), ZMap (CMake/native networking), file/libmagic, pngcheck/zlib, Foremost, stress-ng, Hadolint, LIEF, chkrootkit, and assetfinder's runtime README, OWASP ZAP's Gradle build metadata, Hashcat, John the Ripper, bulk_extractor, Sleuth Kit, and Hydra, apk-mitm (Node.js >=14), and testssl.sh (Bash/OpenSSL). Six Ruby runtime reviews now cover Evil-WinRM, WPScan, Metasploit Framework, WhatWeb, urlcrazy, and CeWL. Assetfinder has no root go.mod in the pinned snapshot, so its exact Go version is unknown. These source files do not establish Termux package availability, Android support, raw-packet permissions, or successful native builds. ZAP also depends on Java/Gradle, while the native scanners and forensic tools have platform-specific build and privilege requirements. Stress tests may destabilize a phone, so use conservative limits.

Four Ruby runtime reviews cover Evil-WinRM, WPScan, Metasploit Framework, and WhatWeb. WPScan declares Ruby >=3.3 and Metasploit Framework >=3.2; Evil-WinRM declares >=2.3; WhatWeb's README does not specify a minimum. Native gem dependencies, WinRM access, packet capture, and scanner behavior remain unverified on Android/Termux.

Five Rust package/workspace reviews cover Zizmor, YARA-X, age-plugin-yubikey, pwninit, and RustHound-CE. Their pinned Cargo manifests document Rust 1.97.0, 1.95.0, 1.70, no explicit minimum, and 1.85 respectively. YubiKey hardware access, native dependencies, and directory-network capabilities are not verified on Android/Termux.


Ten more Python packaging reviews have been pinned for mitmproxy, Semgrep, Safety, Checkov, Certbot, SSLyze, Ansible, pwntools, Impacket, and Androguard. The source metadata identifies declared Python requirements and notable native dependencies or operational limits, but it does not establish Android/Termux installability. Examples include cryptography/maturin, capstone, rustworkx, and Rust extensions.


Seven more pinned Python packaging/dependency reviews cover SpiderFoot, NetExec, Certipy, LDAPDomainDump, enum4linux-ng, Coercer, and BloodyAD. SpiderFoot's source evidence is a requirements manifest rather than a formal package metadata declaration; it includes an older cryptography version range that may not install cleanly on current Python. The Active Directory tools are source-reviewed only and remain unverified on Android/Termux.


Nine more pinned Python packaging reviews cover Frida Tools, Objection, ApkLeaks, Prowler, ScoutSuite, Kube-Hunter, Volatility 3, Cloudsplaining, and APKiD. These packages include native components or depend on external mobile, cloud, or Kubernetes environments; the metadata review is not a device/runtime test.

Eleven additional pinned reviews cover JWT Tool, Corsy, XSStrike, Commix, tplmap, RouterSploit, Ghauri, MobSF, Pacu, Metagoofil, and BloodHound.py. These source files range from dependency manifests to setup metadata. Several are active web, embedded-device, cloud, or directory assessment tools; packaging evidence does not authorize use or establish Android/Termux functionality. Four further reviews cover Responder, pwndbg, angr, and Plaso/log2timeline. Their native network, debugger, symbolic-execution, and forensic dependencies make Android/Termux build and runtime checks especially important. Four additional source reviews cover recon-ng, sqlmap, peepdf, and Smuggler. These include external-service reconnaissance, SQL injection testing, legacy PDF-analysis dependencies, and active HTTP request-smuggling probes; none is device-verified.