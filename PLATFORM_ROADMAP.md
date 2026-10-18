# SYN-LAUNCH Platform Roadmap

This document tracks the staged evolution from a Termux catalog/installer into a mobile-first security platform. It is a plan, not a claim that every capability already exists.

## Stage 1: Device and runtime intelligence

- [x] Detect OS, raw CPU machine string, normalized architecture family, Android/Termux signals, available runtimes, storage headroom, and process UID status.
- [x] Expose a stable, versioned JSON profile for future compatibility automation.
- [x] Explain that container/proot UID 0 is not proof of Android host root.
- [x] Add regression tests for architecture normalization and the CLI profile.
- [x] Run a baseline smoke test on one physical Android 16 / Termux / ARM64 device with Python 3.14.6 (commit `e81f9e58eba5b71e8aa8b18f6b6ac0cdce6a0f5e`); the test does not validate individual cataloged tools.
- [ ] Re-run device validation on the latest code and validate 32-bit/other supported architectures.

## Stage 2: Compatibility metadata

- [ ] Add reviewed per-tool support declarations: native Termux, Android ABI constraints, root/hardware requirements, external service/API needs, and known blockers.
- [x] Keep unknown compatibility explicitly unknown; never infer "works" merely because a package exists or an executable is in PATH.
- [x] Add a report that separates catalog installability, PATH evidence, compatibility assessment, smoke-test evidence, and device-validation evidence.
- [ ] Populate compatibility declarations only from upstream documentation or repeatable tests; a declaration is not device verification.

## Stage 3: Reliable tool lifecycle

- [x] Record batch operation outcomes separately from before/after PATH matches, and label functional verification as not run.
- [x] Capture the most recent installer subprocess command, exit code, timeout/launch error, timestamps, and output bounds in batch summaries; entries that never launched a subprocess retain a null exit code.
- [x] Record requested package specs and explicit Go module version requests in each batch result; mark unpinned packages and unresolved versions honestly.
- [x] Collect resolved-version metadata for Termux packages (`dpkg-query`) and isolated Python packages (`importlib.metadata`), with explicit query status and no inferred version when evidence is absent.
- [x] Extend resolved-version collection to Go build metadata, Cargo install metadata, and global npm package metadata without launching cataloged tool executables.
- [ ] Reconcile resolved versions with requested specs, including mismatches and floating requests.
- [x] Add bounded metadata-only post-install checks using package-manager records and PATH discovery, with explicit status and no execution of cataloged tool binaries.
- [x] Add explicitly confirmed single-package uninstall for Termux, isolated pip, Cargo, and global npm, with before/after metadata and private audit records; leave Go/manual/root uninstall unsupported until package ownership can be established safely.
- [ ] Add package-manager-aware updates with requested/resolved version reconciliation and rollback limits documented.
- [x] Add advisory dependency/runtime and disk-space preflight checks before bulk installs; missing `pkg` blocks package batches, while other warnings require explicit continuation. Exact package sizes and tool functionality remain unverified.

## Stage 4: Authorized assessment workflows

- Compose curated reconnaissance, web/API assessment, configuration audit, mobile-app analysis, and reporting workflows.
- Require the operator to confirm authorization and target scope before active network actions.
- Use safe defaults, rate limits, stop conditions, and clear impact warnings.
- Do not launch scans automatically or treat a discovered host as permission to test it.

## Stage 5: Optional Linux environments

- Evaluate proot-based userland support separately from native Termux operation.
- Investigate Kali NetHunter/other supported environments only as optional integrations.
- Document hardware, kernel, root, and ABI requirements per capability. Never imply that a userspace image grants kernel features or Android host root.

## Release gates

- CI validates Python syntax, shell syntax, catalog schema, and unit/regression tests.
- Device compatibility claims require actual device evidence and must name the tested Android version, Termux source, architecture, and tool version.
- Security changes require tests for unsafe input, untrusted environment overrides, subprocess timeouts, and failure paths.
