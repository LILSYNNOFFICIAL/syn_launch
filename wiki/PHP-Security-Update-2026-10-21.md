# Critical PHP security update: 21 October 2026

**Priority: update PHP immediately if any installed PHP runtime serves web requests.**

Official PHP security guidance published on 21 October 2026 says two critical vulnerabilities can allow unauthenticated remote code execution. The PHP team says updating is the only complete mitigation. See the [official advisory](https://www.php.net/archive/2026.php#2026-10-21-5).

## Fixed releases

| PHP branch | Fixed release |
|---|---:|
| 8.5 | 8.5.12 |
| 8.4 | 8.4.27 |
| 8.3 | 8.3.36 |
| 8.2 | 8.2.35 |

The vulnerabilities are [CVE-2026-109618](https://github.com/advisories/GHSA-w8hw-w9fx-j79w) and [CVE-2026-109619](https://github.com/advisories/GHSA-6wmf-4rv5-p3rp). PHP identifies web-serving installations as affected, including PHP-FPM, Apache with mod_php, php-cgi, FrankenPHP, and LiteSpeed. The advisory describes the highest risk as Apache mod_php, where an unauthenticated request can reach the vulnerable path before application code runs.

PHP 8.1 and older no longer receive updates from the PHP project. Some operating-system vendors may backport fixes, so verify the package vendor's advisory; otherwise upgrade to a supported PHP branch. PHP 8.2 reaches end of life on 31 December 2026.

## Termux / SYN_LAUNCH

The upstream Termux PHP package recipe was updated on 21 October 2026 to target PHP 8.5.12 in commit [`c2bb85d3f26d52ba4a4a159d14214a8ace706235`](https://github.com/termux/termux-packages/commit/c2bb85d3f26d52ba4a4a159d14214a8ace706235). This is packaging-source evidence, not proof that a particular device's configured repository has synchronized or that PHP is installed.

If you use PHP in Termux:

```bash
pkg update
pkg upgrade php
php -v
```

SYN_LAUNCH also has a read-only package-metadata check:

```bash
python main.py --php-security-check
```

It returns a JSON status and nonzero exit code when an update or manual review is needed. It does not make network requests, execute PHP, or update packages, and it cannot prove that a web server uses the same PHP installation.

Check that the reported version is fixed for its branch. If the package manager says no update is available but your installed version is below the fixed release, refresh repository metadata and check the configured Termux repository/mirror before relying on the runtime. Do not assume that a successful package-manager command alone proves the version changed.

For PHP running as a web server or service elsewhere, use the operating system/vendor's patched package and restart every PHP worker/service as directed by that vendor. Check the PHP version used by the actual service, not only the interactive CLI: CLI PHP and the web-serving PHP runtime can be different installations.

## If you cannot update immediately

The PHP advisory lists temporary measures that can reduce exposure to particular attack paths, but explicitly says they do **not** make an installation safe. Configuration changes are not a substitute for the fixed release. Prioritize updating, verify the runtime version, and restart affected workers.

## How this relates to SYN_LAUNCH

SYN_LAUNCH is implemented in Python and does not use PHP as its application runtime. PHP is nevertheless present in the catalog as an optional Termux package for application testing and local development, so its catalog entry now carries this time-sensitive warning. No PHP package was installed or updated on a device by this documentation change.

**Last reviewed:** 21 October 2026. Re-check the official advisory and package vendor before applying changes later.
