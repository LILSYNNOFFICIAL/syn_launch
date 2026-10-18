"""Read-only local adapters for selected SYN_LAUNCH workflows.

No network access, subprocess execution, APK extraction, or package/device mutation.
"""
from __future__ import annotations

import hashlib
import os
import platform
import shutil
import stat
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ADAPTER_SCHEMA = 1
MAX_APK_BYTES = 256 * 1024 * 1024
MAX_APK_ENTRIES = 50_000


def _mode(path: Path) -> dict:
    try:
        info = path.stat()
    except OSError:
        return {"exists": False, "mode_octal": None, "owner_only": None}
    mode = stat.S_IMODE(info.st_mode)
    return {
        "exists": True,
        "mode_octal": oct(mode),
        "owner_only": (mode & 0o077) == 0,
    }


def run_device_configuration_audit(scope: str) -> dict:
    """Collect a small, local-only configuration snapshot without running commands."""
    if scope != "local-device":
        raise ValueError("device-configuration-audit scope must be exactly 'local-device'")
    home = Path.home()
    state_dir = Path(os.environ.get("SYN_LAUNCH_HOME", str(home / ".syn_launch"))).expanduser()
    prefix = os.environ.get("PREFIX", "")
    termux_marker = "com.termux" in prefix or Path("/data/data/com.termux/files/usr").is_dir()
    try:
        free_bytes = shutil.disk_usage(home).free
        disk_status = "available"
    except OSError:
        free_bytes = None
        disk_status = "unavailable"
    source_candidates = []
    if prefix:
        apt_dir = Path(prefix) / "etc" / "apt"
        source_candidates = [
            str(apt_dir / "sources.list"),
            str(apt_dir / "sources.list.d"),
        ]
    return {
        "adapter_schema": ADAPTER_SCHEMA,
        "workflow_id": "device-configuration-audit",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target_scope": "local-device",
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "termux_detected": termux_marker,
            "termux_prefix_configured": bool(prefix),
        },
        "available_runtime_commands": {
            name: shutil.which(name) is not None
            for name in ("python", "python3", "pkg", "dpkg-query", "git")
        },
        "storage": {
            "home_free_bytes": free_bytes,
            "status": disk_status,
        },
        "local_permissions": {
            "home": _mode(home),
            "syn_launch_state": _mode(state_dir),
        },
        "package_source_paths_present": {
            Path(path).name: Path(path).exists() for path in source_candidates
        },
        "execution": {
            "network_actions_executed": False,
            "subprocesses_executed": False,
            "catalog_tools_executed": False,
            "device_settings_changed": False,
            "packages_changed": False,
        },
        "device_validation": "not_run",
        "limitations": [
            "This is a read-only inventory, not a security certification or compatibility verdict.",
            "Presence of pkg or a package-source file does not prove repository reachability or package installability.",
            "Root access, ABI-specific package support, and individual tool behavior are not tested.",
        ],
    }


def run_mobile_apk_inventory(scope: str) -> dict:
    """Inventory an explicitly supplied APK without extracting or executing it."""
    candidate = Path(scope).expanduser()
    if candidate.suffix.lower() != ".apk":
        raise ValueError("mobile-app-review adapter requires a local .apk file path")
    try:
        path = candidate.resolve(strict=True)
        info = path.stat()
    except OSError as exc:
        raise ValueError("APK path does not resolve to a readable local file") from exc
    if not path.is_file():
        raise ValueError("APK path must identify a regular file")
    if info.st_size <= 0 or info.st_size > MAX_APK_BYTES:
        raise ValueError(f"APK size must be between 1 byte and {MAX_APK_BYTES} bytes")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    try:
        with zipfile.ZipFile(path, "r") as archive:
            entries = archive.infolist()
            if len(entries) > MAX_APK_ENTRIES:
                raise ValueError(f"APK contains more than {MAX_APK_ENTRIES} archive entries")
            manifest_present = False
            dex = []
            native_abis = set()
            signature_files = []
            signature_file_count = 0
            dex_count = 0
            bad_member = None
            for item in entries:
                name = item.filename
                if name == "AndroidManifest.xml":
                    manifest_present = True
                if (name == "classes.dex" or
                    (name.startswith("classes") and name.endswith(".dex") and name[7:-4].isdigit())):
                    dex_count += 1
                    if len(dex) < 100:
                        dex.append(name)
                parts = name.split("/")
                if name.startswith("lib/") and len(parts) >= 3 and parts[2].endswith(".so"):
                    if len(native_abis) < 100:
                        native_abis.add(parts[1])
                if (name.startswith("META-INF/") and
                    name.upper().endswith((".RSA", ".DSA", ".EC", ".SF", "MANIFEST.MF"))):
                    signature_file_count += 1
                    if len(signature_files) < 100:
                        signature_files.append(name)
                if bad_member is None and item.flag_bits & 0x1:
                    bad_member = name
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise ValueError("Input is not a readable APK/ZIP archive") from exc
    dex.sort()
    native_abis = sorted(native_abis)
    signature_files.sort()
    return {
        "adapter_schema": ADAPTER_SCHEMA,
        "workflow_id": "mobile-app-review",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_basename": path.name,
        "file_size_bytes": info.st_size,
        "sha256": digest.hexdigest(),
        "archive": {
            "valid_zip_container": True,
            "entry_count": len(entries),
            "android_manifest_present": manifest_present,
            "dex_files": dex,
            "dex_file_count": dex_count,
            "dex_file_names_truncated": dex_count > 100,
            "native_library_abis": native_abis,
            "signature_related_file_names": signature_files,
            "signature_related_name_count": signature_file_count,
            "signature_related_names_truncated": signature_file_count > 100,
            "encrypted_member_name": bad_member,
        },
        "execution": {
            "network_actions_executed": False,
            "subprocesses_executed": False,
            "apk_extracted": False,
            "apk_executed": False,
            "device_settings_changed": False,
        },
        "verification": "static_archive_inventory_only",
        "limitations": [
            "This does not decode the binary Android manifest, verify APK signatures, inspect code semantics, or execute the application.",
            "Signature-related file names are not proof of a valid signature.",
            "Review only APKs you own or are authorized to assess; treat the report as potentially sensitive.",
        ],
    }


def run_workflow_adapter(workflow_id: str, scope: str) -> dict:
    if workflow_id == "device-configuration-audit":
        return run_device_configuration_audit(scope)
    if workflow_id == "mobile-app-review":
        return run_mobile_apk_inventory(scope)
    raise ValueError(
        "No execution adapter is approved for this workflow yet; use --workflow-plan to create a dry-run plan."
    )
