# Security and responsible use

Use scanners, fuzzers, proxies, reconnaissance, password-auditing tools, and exploitation frameworks only on systems and accounts you own or have explicit permission to assess. Confirm scope, rate limits, test windows, and stop conditions before active testing.

SYN_LAUNCH does not launch scans automatically, silently request root, or treat a discovered target as permission to test it. Some cataloged tools can lock accounts, disrupt services, change cloud/directory state, or collect sensitive data. Read each tool's caveats before use.

## Supply-chain considerations

Termux, Python, Go, Cargo, and npm installers may execute third-party code or build scripts. Verify the package identity and upstream project before installation. This repository does not independently audit every upstream release.

## Protect local data

Reports may expose executable paths and runtime details. Logs may contain command output. Protect tokens, hashes, captured traffic, cloud policies, directory exports, and assessment reports. Redact sensitive details before sharing bug reports.

Report security issues privately through GitHub's security reporting feature when available. See [SECURITY.md](../SECURITY.md).
