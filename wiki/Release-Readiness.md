# SYN_LAUNCH Release Readiness

**Reviewed:** 2026-10-22  
**Repository:** [LILSYNNOFFICIAL/syn_launch](https://github.com/LILSYNNOFFICIAL/syn_launch)  
**Status:** Core repository checks pass. This is not a certification that every cataloged tool works on every Android device.

## Verified repository status

- Default branch: `main`.
- Latest validation run checked during this review: [GitHub Actions run 39847749102](https://github.com/LILSYNNOFFICIAL/syn_launch/actions/runs/39847749102).
- All three CI matrix jobs completed successfully: Python 3.10, 3.12, and 3.14.
- The preceding feature/test baseline recorded 144 passing tests in its Python 3.12 job.
- The catalog contains 269 entries across 19 categories; 267 have source-documented compatibility declarations.
- The curated Phone Number OSINT + Android Pentest Top 75 is catalog-backed and covered by regression tests. It is a curated list, not a promise that all 75 tools install or run on stock Android.

## Device evidence and limits

The last recorded local audit was on one Android 16 / Termux ARM64 device. It reported 41 catalog executable matches on PATH, 37 bounded smoke probes passed, and 29 reviewed local-only functional checks passed. Four potentially side-effecting or network-oriented executables were excluded from generic smoke probing.

That audit also recorded six packages installed after package-manager dry-runs showed zero upgrades: ripgrep 15.2.0, fd 10.5.0, file 5.48-3, tree 2.3.2, iproute2 7.3.0, and Vim 9.2.1200, with libsodium 1.0.22-1 as a dependency. Local-fixture checks passed for ripgrep, fd, file, and tree; Vim passed a local file-edit assertion. iproute2 passed `ip -V`, but Android denied interface inspection through netlink.

These are bounded checks, not comprehensive feature tests. The device audit was not repeated during this GitHub-only review. The device compatibility summary remains `not_run` for the catalog as a whole.

## Known limitations

| Component | Verified status | Release handling |
|---|---|---|
| Burp Suite | Native Termux compatibility unassessed | Keep reference-only and non-installable by default. See [system requirements](https://portswigger.net/burp/documentation/desktop/getting-started/system-requirements). |
| Wappalyzer | Public npm package is deprecated; native Termux compatibility unassessed | Keep reference-only. See [npm package](https://www.npmjs.com/package/wappalyzer) and [HTTP Archive fork](https://github.com/HTTPArchive/wappalyzer). |
| Metasploit Framework | Cataloged as manual/reference-only; Android installation and runtime not verified | Do not imply it is installed or operational on the user's phone. The pinned upstream gemspec requires Ruby >= 3.2 and lists a large dependency tree including native components. |
| Armitage GUI | No entry in the reviewed catalog | Not included in the current catalog. It is separate from Metasploit Framework. |
| Full 269-entry runtime compatibility | Not tested | Do not claim every catalog entry installs, is compatible, or functions. |
| Authorized external HTTPS staging check | Previously completed bounded HEAD request to `https://meepsheep.com/` | A same-host 307 redirect led to 200 OK. No response body was read. This was not a vulnerability scan. |

## Release checklist

- [x] Latest reviewed CI matrix is green on Python 3.10, 3.12, and 3.14.
- [x] Test baseline recorded 144 passing tests.
- [x] Documented catalog size and evidence boundaries.
- [x] Documented device smoke-test and local functional-check scope.
- [x] Documented known unverified tools and the distinction between Metasploit and Armitage.
- [ ] Run `bash device_check.sh` on the target phone after pulling the latest `main` branch. The device was offline during this review, so this cannot be marked complete remotely.
- [ ] Create a versioned GitHub Release only if a formal release artifact is desired. No release tag or asset is claimed here.

## Accurate project description

SYN_LAUNCH is a Termux-first Android security and developer-tool catalog with installation metadata, diagnostics, compatibility evidence, and a curated Phone Number OSINT + Android Pentest Top 75 profile. The latest reviewed CI matrix passes on Python 3.10, 3.12, and 3.14. A prior bounded audit on one Android 16 / Termux ARM64 device recorded 37 passing smoke probes and 29 passing local-only functional checks. Those results do not certify the full catalog. Metasploit is listed but not verified as installed or working on the phone; Armitage is not included in the reviewed catalog.
