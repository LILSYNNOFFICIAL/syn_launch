# SYN-LAUNCH Platform Roadmap

This document tracks the staged evolution from a Termux catalog/installer into a mobile-first security platform. It is a plan, not a claim that every capability already exists.

## Stage 1: Device and runtime intelligence

- [x] Detect OS, raw CPU machine string, normalized architecture family, Android/Termux signals, available runtimes, storage headroom, and process UID status.
- [x] Expose a stable, versioned JSON profile for future compatibility automation.
- [x] Explain that container/proot UID 0 is not proof of Android host root.
- [x] Add regression tests for architecture normalization and the CLI profile.
- [ ] Validate the profile on physical Termux devices across arm64 and 32-bit/other supported architectures.

## Stage 2: Compatibility metadata

- Add per-tool support declarations: native Termux, Android ABI constraints, root/hardware requirements, external service/API needs, and known blockers.
- Keep unknown compatibility as unknown. Never infer "works" merely because a package exists or an executable is in PATH.
- Add a report that separates installable, installed, smoke-tested, and device-verified states.

## Stage 3: Reliable tool lifecycle

- Record the requested package/version and installer result.
- Add bounded post-install checks that do not run arbitrary commands from catalog metadata.
- Make updates and uninstall behavior explicit, reversible where possible, and auditable.
- Add dependency and disk-space preflight checks before bulk installs.

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
