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

Eighty-four Termux recipe-backed entries map to 66 distinct recipes or subpackage definitions: 82 are pinned to `termux-packages` revision `e85983636adcf748134c3feb1df27f44e78322e1`, and MTR/tcpdump are pinned to `termux-root-packages` revision `06591fc024101b04095ec4417d51907512b46e3c`. Six additional Python package entries (pip-audit, yamllint, dirsearch, Sherlock, Bandit, and detect-secrets) pin upstream `pyproject.toml` metadata and record declared Python requirements only. Each declaration carries a `source_revision` and `source_snapshot_url` so reviewers can inspect the exact evidence snapshot. This includes core utilities and selected networking, developer, and file-analysis tools. Metadata links to the actual recipe directory where possible (for example, curl uses `libcurl`, SQLite uses `libsqlite`, and OpenSSH keyscan uses the `openssh` recipe). Recent additions cover Nmap, ShellCheck, YARA, radare2, Tesseract OCR, ClamAV, OpenSSH keyscan, MTR, and tcpdump. MTR and tcpdump links point to the separate upstream `termux-root-packages` repository; capture and raw-socket permissions remain device-specific. The status remains `source_documented_not_device_verified`. Recipe presence does not prove the package is enabled for the current device ABI, installable from the configured repository, or functional.

## Current report behavior

`python main.py --compatibility-report` emits report schema 3. The report itself does not launch cataloged executables; it reads previously saved local smoke-test records. To deliberately test one entry, run `python main.py --smoke-test NAME_OR_ID`. The command tries bounded `--version`, `--help`, and `-h` probes, each capped at five seconds and 64 KiB. It stores only the outcome and metadata, not raw command output, in private `~/.syn_launch/smoke_tests.json`. A passing result means a probe produced output and exited with code 0; it does not test the tool's operational features. The report marks a record `stale_evidence` if the executable path or lightweight file identity changes since the probe. Device validation remains `not_run`.

## Adding evidence

1. Prefer the project's official install documentation or the exact package recipe.
2. Link to the HTTPS source and state what it establishes.
3. Document architecture, root, hardware, external-service, and known-blocker details only when supported.
4. Keep the status `source_documented_not_device_verified` until real device evidence exists.
5. For device validation, record device model/OS, Termux source, architecture, tool/package version, command, exit status, and test limits. Keep a bounded CLI smoke probe distinct from a device-level functional test.
