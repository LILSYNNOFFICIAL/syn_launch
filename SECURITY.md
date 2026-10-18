[object Object]
## Evidence and reports

Compatibility declarations identify upstream packaging evidence and known blockers; they do not certify that a tool works. The compatibility report deliberately keeps catalog installability, PATH discovery, source metadata, bounded smoke tests, and device validation separate. `--smoke-test NAME_OR_ID` explicitly runs only a selected executable's bounded `--version`/`--help` probe; do not interpret a passing response as proof that other features work. Do not publish a report as proof of device compatibility unless the device/tool details and relevant test evidence are recorded.

Physical-device reports may include architecture, paths, installed runtime versions, and other local system details. Sanitize these details before public issue reports. Never attach API keys, session tokens, private targets, captured traffic, or unredacted assessment output.
