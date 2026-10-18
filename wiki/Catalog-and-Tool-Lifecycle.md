# Catalog and tool lifecycle

## Catalog fields

The catalog describes each tool's name, category, executable name, install method, package/module specification, upstream source, example, and compatibility/safety caveat. Some entries are manual-only when a dependable Termux installation route is not established.

The optional `compatibility` object is validated when present. It requires a status, platform, HTTPS evidence URL, evidence kind, architecture policy, root requirement, hardware and external-service lists, known blockers, and review date.

## Installation

- Termux package installs use `pkg`.
- Python packages use the app's isolated virtual environment under `~/.syn_launch/venv`.
- Go binaries are installed under `~/.local/bin`.
- Cargo and npm use their configured package managers.
- Manual/root entries do not pretend to install automatically.

Bulk installs require confirmation; individual third-party installs require typing `INSTALL`. Package-manager success is not functional verification.

## Updates and removal

Single-tool update/removal options are limited to supported package managers and require explicit confirmation. Actions may change dependencies and are not automatically reversible. Go/manual/root uninstall remains unsupported where package ownership cannot be safely established.

Private lifecycle logs and summaries are stored under `~/.syn_launch/`. Keep them private; they may reveal package versions, commands, paths, or runtime information.

## Bounded smoke-test evidence

Use `python main.py --smoke-test NAME_OR_ID` only for one entry you intentionally choose. SYN_LAUNCH tries `--version`, `--help`, and `-h` with a five-second timeout and 64 KiB output cap per attempt. The raw output is not saved in the evidence record. It records the selected flag, exit code, timeout/truncation flags, observed-output status, and a lightweight executable file identity in `~/.syn_launch/smoke_tests.json`.

The compatibility report reads these records but never launches tools itself. If the executable path or recorded file identity no longer matches the current executable, the report labels the evidence `stale_evidence`. Even a current `passed` result proves only that one help/version probe returned output and exited with code 0; it does not certify functional behavior or device compatibility.
