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

One hundred ten recipe-backed entries map to 92 distinct recipes or subpackage definitions: 103 are pinned to `termux-packages` revision `e85983636adcf748134c3feb1df27f44e78322e1`, and seven are pinned to `termux-root-packages` revision `06591fc024101b04095ec4417d51907512b46e3c`. Sixty-three Python packaging/dependency entries (pip-audit, yamllint, dirsearch, Sherlock, Bandit, detect-secrets, email-validator, ssh-audit, Maigret, h8mail, and theHarvester, plus holehe, dnstwist, Wapiti, Wfuzz, WAFW00F, Arjun, hashID, Passlib, bcrypt, ROPGadget, and Ropper) pin upstream packaging metadata and record declared Python requirements only. Each declaration carries a `source_revision` and `source_snapshot_url` so reviewers can inspect the exact evidence snapshot. This includes core utilities and selected networking, developer, and file-analysis tools. Metadata links to the actual recipe directory where possible (for example, curl uses `libcurl`, SQLite uses `libsqlite`, and OpenSSH keyscan uses the `openssh` recipe). Recent additions cover xh, feroxbuster, curlie, hping3, arp-scan, Nmap, ShellCheck, YARA, radare2, Tesseract OCR, ClamAV, OpenSSH keyscan, MTR, and tcpdump. xh, feroxbuster, and curlie now use main-repository `pkg` installation paths. hping3 and arp-scan remain non-installable by default because their recipes require the separate root-packages repository and raw-packet capabilities. MTR and tcpdump links point to the separate upstream `termux-root-packages` repository; capture and raw-socket permissions remain device-specific. The status remains `source_documented_not_device_verified`. Recipe presence does not prove the package is enabled for the current device ABI, installable from the configured repository, or functional.

## Current report behavior

`python main.py --compatibility-report` emits report schema 3. The report itself does not launch cataloged executables; it reads previously saved local smoke-test records. To deliberately test one entry, run `python main.py --smoke-test NAME_OR_ID`. The command tries bounded `--version`, `--help`, and `-h` probes, each capped at five seconds and 64 KiB. It stores only the outcome and metadata, not raw command output, in private `~/.syn_launch/smoke_tests.json`. A passing result means a probe produced output and exited with code 0; it does not test the tool's operational features. The report marks a record `stale_evidence` if the executable path or lightweight file identity changes since the probe. Device validation remains `not_run`.

## Adding evidence

1. Prefer the project's official install documentation or the exact package recipe.
2. Link to the HTTPS source and state what it establishes.
3. Document architecture, root, hardware, external-service, and known-blocker details only when supported.
4. Keep the status `source_documented_not_device_verified` until real device evidence exists.
5. For device validation, record device model/OS, Termux source, architecture, tool/package version, command, exit status, and test limits. Keep a bounded CLI smoke probe distinct from a device-level functional test.


The latest pinned recipe reviews cover `xh`, `feroxbuster`, `curlie`, `hping3`, and `arp-scan`. The first three now use Termux `pkg` install paths backed by the main Termux package repository. `hping3` and `arp-scan` are documented against the separate root-packages repository but remain disabled for automated installation by default. All five remain unverified on a physical device.


Additional pinned main-repository recipe reviews now cover Gitleaks, cargo-audit, govulncheck, strace, ltrace, Docker CLI, kubectl, rclone, restic, RustScan, JADX, Apktool, SSLScan, ProxyChains-NG, gosec, Rizin, Crunch, and steghide. Their catalog install paths use Termux `pkg`; this records a source-backed install route, not successful installation or runtime support on a particular Android device. Docker CLI still needs a usable daemon, tracing depends on Android kernel restrictions, and network scanners must only be used against authorized targets.


Three additional pinned root-repository recipe reviews cover `iw`, Aircrack-ng, and TShark. These remain non-installable by default: `iw` and Aircrack-ng depend on wireless driver/firmware and privilege capabilities, while TShark packet capture depends on interface access and permissions. Recipe presence is not evidence that these capabilities work on stock Android.


Forty-six Go module metadata reviews have been added for subfinder, dnsx, httpx, naabu, gau, waybackurls, katana, unfurl, ffuf, gobuster, PhoneInfoga, Nuclei, Kiterunner, KXSS, CRLFuzz, Interactsh, Tlsx, MapCIDR, Uncover, ASNMap, anew, qsreplace, hakrawler, Chisel, Alterx, Shuffledns, PureDNS, gowitness, kubeaudit, kube-linter, gauplus, TruffleHog, OSV-Scanner, Kerbrute, CloudFox, kubeletctl, Cosign, Terrascan, staticcheck, and Dockle, plus Trivy, Grype, Syft, kube-bench, and Ligolo-ng. Each records the pinned `go.mod` revision and declared Go version. Several recent projects require Go 1.26+; their toolchain requirements and large dependency graphs may exceed the device's installed Go version or build resources. The catalog's `@latest` install selectors remain unpinned, and module metadata does not prove that the current Termux toolchain or dependencies build on the device.

Two Rust workspace reviews cover Zizmor and YARA-X. Their pinned Cargo manifests declare minimum Rust versions 1.97.0 and 1.95.0 respectively. These modern toolchain requirements, multi-crate dependency trees, and native build behavior are not verified on Android/Termux.


Ten more Python packaging reviews have been pinned for mitmproxy, Semgrep, Safety, Checkov, Certbot, SSLyze, Ansible, pwntools, Impacket, and Androguard. The source metadata identifies declared Python requirements and notable native dependencies or operational limits, but it does not establish Android/Termux installability. Examples include cryptography/maturin, capstone, rustworkx, and Rust extensions.


Seven more pinned Python packaging/dependency reviews cover SpiderFoot, NetExec, Certipy, LDAPDomainDump, enum4linux-ng, Coercer, and BloodyAD. SpiderFoot's source evidence is a requirements manifest rather than a formal package metadata declaration; it includes an older cryptography version range that may not install cleanly on current Python. The Active Directory tools are source-reviewed only and remain unverified on Android/Termux.


Nine more pinned Python packaging reviews cover Frida Tools, Objection, ApkLeaks, Prowler, ScoutSuite, Kube-Hunter, Volatility 3, Cloudsplaining, and APKiD. These packages include native components or depend on external mobile, cloud, or Kubernetes environments; the metadata review is not a device/runtime test.

Eleven additional pinned reviews cover JWT Tool, Corsy, XSStrike, Commix, tplmap, RouterSploit, Ghauri, MobSF, Pacu, Metagoofil, and BloodHound.py. These source files range from dependency manifests to setup metadata. Several are active web, embedded-device, cloud, or directory assessment tools; packaging evidence does not authorize use or establish Android/Termux functionality. Four further reviews cover Responder, pwndbg, angr, and Plaso/log2timeline. Their native network, debugger, symbolic-execution, and forensic dependencies make Android/Termux build and runtime checks especially important.
