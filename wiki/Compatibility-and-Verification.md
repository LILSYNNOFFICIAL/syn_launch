# Compatibility and verification model

SYN_LAUNCH reports distinct evidence levels to prevent overclaiming.

| Evidence | Meaning | Does not prove |
|---|---|---|
| Catalog entry | Metadata exists in `catalog.json` | Package exists or tool works |
| Catalog installable | An install method is configured | Install will succeed on this device |
| PATH match | An executable with the expected name is discoverable | It is the intended tool or functions |
| Source-documented declaration | Upstream documentation/package recipe supports the declared install route and caveats | Device compatibility or successful execution |
| Install metadata | Package manager reports package/version metadata | Functional correctness |
| Smoke test | A specific bounded command ran with recorded outcome | All features work |
| Device validation | A named tool/version was tested on a named device/OS/architecture | Universal support on other devices |

## Initial source-backed subset

Nine core Termux entries have structured metadata with HTTPS links to upstream Termux package recipes: Git, curl, wget, jq, ripgrep, OpenSSH, SQLite, Python, and Node.js. Their status is `source_documented_not_device_verified`. Architecture wording deliberately defers to the user's configured Termux repositories; it does not claim that every ABI is supported.

## Current report behavior

`python main.py --compatibility-report` reports compatibility metadata separately from smoke-test and device-validation evidence. Unless separately recorded, `smoke_test`, `device_validation`, and `verification` remain `not_run`. The report does not launch cataloged executables.

## Adding evidence

1. Prefer the project's official install documentation or the exact package recipe.
2. Link to the HTTPS source and state what it establishes.
3. Document architecture, root, hardware, external-service, and known-blocker details only when supported.
4. Keep the status `source_documented_not_device_verified` until real device evidence exists.
5. Record device model/OS, Termux source, architecture, tool/package version, command, exit status, and test limits for a smoke/device test.
