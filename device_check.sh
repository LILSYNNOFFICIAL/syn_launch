#!/usr/bin/env bash
# Local, non-networked Termux diagnostics. This script does not install, update,
# uninstall, or actively test any cataloged security tool.
set -u
umask 077

if [[ ! -f main.py || ! -f catalog.json ]]; then
  echo "Run this script from the root of the SYN_LAUNCH checkout."
  exit 2
fi

PYTHON_BIN="${PYTHON:-python}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python was not found. No packages were installed."
  exit 2
fi

STATE_DIR="${SYN_LAUNCH_HOME:-$HOME/.syn_launch}"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="$STATE_DIR/device-check-$STAMP"
mkdir -p "$OUT"
chmod 700 "$OUT" 2>/dev/null || true
RESULTS="$OUT/results.txt"
: > "$RESULTS"
failures=0

run_check() {
  label="$1"
  logfile="$2"
  shift 2
  printf '[RUN ] %s\n' "$label"
  if "$@" >"$OUT/$logfile" 2>&1; then
    printf '[PASS] %s\n' "$label" | tee -a "$RESULTS"
  else
    code=$?
    printf '[FAIL] %s (exit %s; see %s)\n' "$label" "$code" "$logfile" | tee -a "$RESULTS"
    tail -n 60 "$OUT/$logfile" 2>/dev/null || true
    failures=$((failures + 1))
  fi
}

run_check "Python syntax" "python-syntax.log" "$PYTHON_BIN" -m py_compile main.py workflow_planner.py workflow_adapters.py
run_check "Installer shell syntax" "installer-syntax.log" bash -n install.sh
run_check "Device-check shell syntax" "device-check-syntax.log" bash -n device_check.sh
run_check "Catalog JSON syntax" "catalog-json.log" "$PYTHON_BIN" -m json.tool catalog.json
run_check "Unit and regression tests" "unit-tests.log" env SYN_LAUNCH_HOME="$OUT/test-state" "$PYTHON_BIN" -m unittest discover -s tests -v
run_check "Runtime check" "check.log" env SYN_LAUNCH_HOME="$STATE_DIR" "$PYTHON_BIN" main.py --check
run_check "Detailed diagnostics" "doctor.log" env SYN_LAUNCH_HOME="$STATE_DIR" "$PYTHON_BIN" main.py --doctor
run_check "Structured environment profile" "profile.json" env SYN_LAUNCH_HOME="$STATE_DIR" "$PYTHON_BIN" main.py --profile
run_check "Read-only local device and optional-environment audit" "device-audit.json" env SYN_LAUNCH_HOME="$STATE_DIR" "$PYTHON_BIN" main.py --workflow-run device-configuration-audit --target-scope local-device --authorized
run_check "Explicit bounded Python smoke test" "python-smoke-test.json" env SYN_LAUNCH_HOME="$STATE_DIR" "$PYTHON_BIN" main.py --smoke-test python
run_check "Compatibility report" "compatibility-report.json" env SYN_LAUNCH_HOME="$STATE_DIR" "$PYTHON_BIN" main.py --compatibility-report

if "$PYTHON_BIN" - "$OUT" <<'PY' >"$OUT/report-validation.log" 2>&1
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
report = json.loads((out / "compatibility-report.json").read_text(encoding="utf-8"))
smoke = json.loads((out / "python-smoke-test.json").read_text(encoding="utf-8"))
audit = json.loads((out / "device-audit.json").read_text(encoding="utf-8"))
assert audit["workflow_id"] == "device-configuration-audit", audit
assert audit["execution"]["network_actions_executed"] is False, audit
assert audit["execution"]["subprocesses_executed"] is False, audit
assert "optional_linux_environments" in audit, audit
assert report["report_schema"] == 3, report.get("report_schema")
assert report["summary"]["catalog_entries"] == 269, report["summary"]
assert report["summary"]["compatibility_assessed_entries"] >= 189, report["summary"]
assert report["summary"]["device_verified_entries"] == 0, report["summary"]
assert report["summary"]["smoke_tested_entries"] >= 1, report["summary"]
python_tool = next(tool for tool in report["tools"] if tool["id"] == "python")
assert python_tool["smoke_test"] == "passed", python_tool
assert python_tool["device_validation"] == "not_run", python_tool
assert smoke["status"] == "passed", smoke
assert smoke["tool_id"] == "python", smoke
print("Report schema, compatibility coverage, and Python smoke evidence validated.")
print("Device validation remains not_run. This script does not test all cataloged tools.")
PY
then
  printf '[PASS] Report invariants\n' | tee -a "$RESULTS"
else
  code=$?
  printf '[FAIL] Report invariants (exit %s; see report-validation.log)\n' "$code" | tee -a "$RESULTS"
  failures=$((failures + 1))
fi

cat >> "$RESULTS" <<EOF

Output directory: $OUT
Network actions: none
Cataloged security tools executed: none
Only explicit tool probe: Python --version/--help bounded smoke test
Device validation status: not_run (human review and device-specific evidence still required)
EOF
# umask 077 above keeps newly created files private (0600) and directories private (0700).
echo
cat "$RESULTS"
echo
echo "Private evidence bundle: $OUT"
echo "Share only the files you have reviewed; logs may contain local paths and environment details."
if (( failures > 0 )); then
  exit 1
fi
exit 0
