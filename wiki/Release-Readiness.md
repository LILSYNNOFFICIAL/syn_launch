# SYN_LAUNCH Release Readiness

**Review date:** 2026-10-22  
**Repository:** [LILSYNNOFFICIAL/syn_launch](https://github.com/LILSYNNOFFICIAL/syn_launch)  
**Status:** Repository release candidate. Full catalog compatibility is not certified.

## Current repository gate

- The default branch is `main`; the latest branch inventory returned only `main`.
- Latest verified commit: [`a706ef74d609bde2d887beb8b6291bc41b55dedb`](https://github.com/LILSYNNOFFICIAL/syn_launch/commit/a706ef74d609bde2d887beb8b6291bc41b55dedb).
- The latest verified GitHub Actions run passed all Python matrix jobs on 3.10, 3.12, and 3.14: [run 39823202999](https://github.com/LILSYNNOFFICIAL/syn_launch/actions/runs/39823202999). The Python 3.12 job log records 144 passing tests.
- The catalog contains 269 entries across 19 categories. 267 entries have source-backed compatibility declarations. Burp Suite and Wappalyzer remain reference-only and unassessed for native Termux execution.
- The curated Phone Number OSINT + Android Pentest Top 75 is catalog-backed and covered by regression tests. It is a selection/profile, not a claim that all 75 tools install or work on stock Android.

## Device evidence and limitations

The last recorded device audit on 2026-10-22 was on one Android 16 / Termux ARM64 device. It recorded 41 catalog executable matches on PATH, 37 bounded smoke probes passed, and 29 reviewed local-only functional checks passed through the built-in evidence reporter. Four potentially side-effecting or network-oriented executables were excluded from generic smoke probing. Six packages were installed after package-manager dry-runs showed zero upgrades: ripgrep 15.2.0, fd 10.5.0, file 5.48-3, tree 2.3.2, iproute2 7.3.0, and Vim 9.2.1200 (with libsodium 1.0.22-1 as a dependency).

The first four tools also passed bounded local-fixture assertions; Vim passed its local file-edit assertion. iproute2 passed `ip -V`, but Android denied interface inspection through netlink. These are limited checks, not complete tool-feature tests. Catalog-wide device validation remains `not_run`, and the device audit has not been repeated as part of this GitHub-only release review.

## Explicitly retained limitations

| Item | Status | Decision |
|---|---|---|
| Burp Suite native Termux support | Unassessed; no supported Android/Termux claim | Keep manual/reference-only and non-installable by default. See [official system requirements](https://portswigger.net/burp/documentation/desktop/getting-started/system-requirements). |
| Wappalyzer native Termux support | Unassessed; public npm package is deprecated | Keep reference-only. Do not imply current official CLI or Termux support. See [npm package](https://www.npmjs.com/package/wappalyzer) and [HTTP Archive fork](https://github.com/HTTPArchive/wappalyzer). |
| Metasploit Framework | Cataloged, device installation not verified in this release audit | A catalog entry is not proof of installation or operation on Android. |
| Armitage GUI | No catalog entry found in the reviewed catalog | Treat as not included unless separately added and assessed. |
| External HTTPS staging adapter | Bounded check previously completed | An owner-authorized HTTPS HEAD check to `https://meepsheep.com/` followed a same-host 307 redirect and received 200 OK. No response body was read. This was not a vulnerability scan. |
| Full catalog runtime certification | Not performed | Do not claim all 269 entries are installable, compatible, or functional. |

## Release checklist

- [x] Confirm `main` is the only listed branch.
- [x] Confirm latest recorded GitHub Actions matrix is green for Python 3.10, 3.12, and 3.14.
- [x] Confirm the current regression suite is passing (144 tests recorded in the Python 3.12 job).
- [x] Document catalog size, evidence level, device-check results, and known unsupported/unassessed entries.
- [x] Document the difference between catalog presence, installation, smoke probes, local functional checks, and full device compatibility.
- [ ] Repeat the local device diagnostic suite on the target phone after this documentation change. The connected device was offline during this review, so this check cannot be truthfully marked complete here.
- [ ] Publish a versioned GitHub release if/when the owner wants a formal release artifact. No release tag or release asset is claimed by this checklist.

## Accurate release wording

“SYN_LAUNCH is a Termux-first Android security and developer-tool catalog with source-backed installation evidence for selected entries, bounded diagnostics, and a curated Phone Number OSINT + Android Pentest Top 75 profile. Its current GitHub Actions matrix passes on Python 3.10, 3.12, and 3.14, with 144 tests recorded in the Python 3.12 job. On one Android 16 / Termux ARM64 device, a prior bounded audit recorded 37 smoke probes and 29 local-only functional checks passing; iproute2 interface inspection remained blocked by Android permissions. These results do not certify the full 269-entry catalog. Burp Suite and Wappalyzer remain reference-only and unassessed for native Termux execution; Metasploit is cataloged but its device installation is unverified, and Armitage is not included in the reviewed catalog.”

Do not describe SYN_LAUNCH as fully device-verified or claim that every catalog entry works.
