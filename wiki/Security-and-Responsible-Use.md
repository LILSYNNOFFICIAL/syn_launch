# Security and responsible use

Use scanners, fuzzers, proxies, reconnaissance, password-auditing tools, and exploitation frameworks only on systems and accounts you own or have explicit permission to assess. Confirm scope, rate limits, test windows, and stop conditions before active testing.

SYN_LAUNCH does not launch scans automatically, silently request root, or treat a discovered target as permission to test it. Some cataloged tools can lock accounts, disrupt services, change cloud/directory state, or collect sensitive data. Read each tool's caveats before use.

## Supply-chain considerations

Termux, Python, Go, Cargo, and npm installers may execute third-party code or build scripts. Verify the package identity and upstream project before installation. This repository does not independently audit every upstream release.

## Protect local data

Reports may expose executable paths and runtime details. Logs may contain command output. Protect tokens, hashes, captured traffic, cloud policies, directory exports, and assessment reports. Redact sensitive details before sharing bug reports.

Report security issues privately through GitHub's security reporting feature when available. See [SECURITY.md](../SECURITY.md).

## Time-sensitive runtime advisory

PHP is an optional catalog package, not the SYN_LAUNCH application runtime. On 21 October 2026, the PHP project published fixed releases for two critical unauthenticated remote-code-execution vulnerabilities. If PHP is installed, especially if it serves web requests, follow the [PHP security update guide](PHP-Security-Update-2026-10-21.md) and verify the version used by the actual service. The catalog's PHP entry records the upstream Termux package recipe revision, but this does not prove your device's installed version is patched.
