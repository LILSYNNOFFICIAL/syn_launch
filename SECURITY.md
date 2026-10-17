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

SYN_LAUNCH is a launcher/catalog. It does not automatically scan targets, request root, or store target histories by default. Installer commands are invoked as argument arrays rather than through a shell. Catalog entries are validated before use. Package managers and upstream build scripts still execute third-party code, so review package provenance and only install tools you trust.
