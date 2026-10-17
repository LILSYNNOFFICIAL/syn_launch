# Security Policy

## Supported project

Security reports for SYN_LAUNCH itself are welcome. Third-party tools listed in `catalog.json` are maintained by their respective upstream projects; report vulnerabilities in those tools to their maintainers.

## Reporting

Please use GitHub's private vulnerability reporting feature for this repository when it is enabled. Include:
- affected commit or release;
- steps to reproduce and expected versus actual behavior;
- impact and a safe proof of concept;
- any Android/Termux version, architecture, and package source involved.

Do not publish secrets, real user data, working credentials, or destructive exploit steps in a public issue.

## Security design

SYN_LAUNCH is a launcher/catalog. It does not automatically scan targets, request root, or store target histories by default. Installer commands are invoked as argument arrays rather than through a shell. Catalog entries are validated for unique IDs and display names, executable syntax, install-method/package syntax, boolean install flags, and well-formed HTTPS source URLs without embedded credentials. Installer subprocesses discard common environment variables that can redirect package sources or inject Python startup paths; pip uses isolated mode with the official PyPI index, Go uses the official proxy and checksum database, and npm uses the official registry with TLS verification. These controls reduce environment-based source redirection but do not eliminate supply-chain risk: third-party code still runs, and versions are not universally pinned. Viewing tool metadata does not execute the local binary; help/version probes require an explicit user action. Subprocess output is capped at 10 MiB per command to reduce log-flood and disk-exhaustion risk. Package managers and upstream build scripts still execute third-party code, so review package provenance and only install tools you trust.
