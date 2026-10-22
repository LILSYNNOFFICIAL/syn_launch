# Workflow Planning

SYN_LAUNCH creates reviewable JSON plans, supports read-only local adapters, and provides a bounded HTTPS HEAD review adapter. It is not a general-purpose assessment engine.

## Available plans

- `web-api-review`: review planning for an explicitly scoped web app or API.
- `mobile-app-review`: owner-provided mobile application and isolated test environment.
- `device-configuration-audit`: non-destructive review of the operator's own Android/Termux setup.
- `assessment-report`: validates and summarizes a local JSON evidence bundle.

## Usage

List workflows:

```bash
python main.py --workflow-list
```

Create a plan:

```bash
python main.py --workflow-plan web-api-review --target-scope "https://staging.example.test/api" --authorized
```

Run a local Termux/device configuration inventory. The scope must be exactly `local-device`:

```bash
python main.py --workflow-run device-configuration-audit --target-scope local-device --authorized
```

Perform a bounded HTTPS HEAD review against an explicitly authorized URL:

```bash
python main.py --workflow-run web-api-review --target-scope "https://staging.example.test/api/health" --authorized
```

This performs real network requests. It permits only HTTPS on port 443, rejects embedded credentials, query strings, fragments, wildcards, and parent-directory path segments, uses certificate-verified TLS with a three-second DNS-resolution budget and a five-second socket timeout, and never reads response bodies. It follows at most three redirects, only when the redirect stays on the exact same hostname over HTTPS; cross-host and unsafe redirect targets are recorded in sanitized form and not followed. Only an allowlist of response headers is retained. This is not a vulnerability scan.

Inventory an APK archive without extracting or executing it:

```bash
python main.py --workflow-run mobile-app-review --target-scope "$HOME/path/to/your-test.apk" --authorized
```

Validate and summarize an evidence JSON file without contacting the listed assets:

```bash
cp examples/assessment-evidence.example.json "$HOME/evidence.json"
# Edit the copy, replace placeholders, and redact sensitive data.
python main.py --workflow-run assessment-report --target-scope "$HOME/evidence.json" --authorized
```

The JSON root must contain a `findings` array. Each finding requires non-empty `title`, `severity`, `asset`, `evidence`, and `remediation` strings. The file is limited to 5 MiB and 500 findings. Never include live credentials or session tokens.

Reports are saved under `~/.syn_launch/workflow-runs/` with owner-only permissions. The APK report records the basename and SHA-256, not the full local path.

The target-scope value should identify the exact authorized assets or environment. Avoid wildcards and broad domains when the engagement scope is narrower.

## Safety behavior

- Both `--target-scope` and `--authorized` are required to generate a plan.
- The authorization flag is only the operator's declaration. It is not verified by the software and does not grant permission.
- Plans contain stop conditions and state `network_actions_executed: false` and `subprocesses_executed: false`.
- The planner does not invoke catalog executables, run scans, contact targets, change device state, or install packages.
- The device adapter reads local runtime/path/storage/permission metadata and checks for optional PRoot/NetHunter command and rootfs markers only. It does not call subprocesses, contact networks, change settings, or alter packages.
- The APK adapter hashes the selected file and reads ZIP entry names only. It does not extract, execute, decode the binary manifest, or validate the signature.
- Web/API review performs a bounded HEAD request and may follow up to three safe same-host HTTPS redirects. It is not a scanner and must be used only against the exact authorized URL. The evidence-report adapter only validates and summarizes local JSON input; it does not verify the findings.
- Plans are templates. They do not prove that a check was performed or that a target is secure.
- Future command adapters must receive a separate safety review, scope enforcement, bounded execution, and tests before they can run anything.

## Errors

The command exits with status 2 if the workflow is unknown, scope is missing or invalid, or the authorization declaration is absent. Use `--workflow-list` to retrieve the exact workflow IDs.

[executed on device: localhost (d2cc1207-90f0-4617-b081-86736c11e33d)]