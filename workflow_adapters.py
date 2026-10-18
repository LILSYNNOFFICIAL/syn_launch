"""Scope-limited workflow adapters for SYN_LAUNCH.

Local adapters are read-only. The web adapter performs one explicit HTTPS HEAD request.
No adapter executes catalog tools, extracts APKs, or mutates package/device state.
"""
from __future__ import annotations

import hashlib
import http.client
import ipaddress
import json
import os
import platform
import shutil
import socket
import ssl
import stat
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ADAPTER_SCHEMA = 1
MAX_APK_BYTES = 256 * 1024 * 1024
MAX_APK_ENTRIES = 50_000
MAX_EVIDENCE_JSON_BYTES = 5 * 1024 * 1024
MAX_FINDINGS = 500
SEVERITIES = {"critical", "high", "medium", "low", "info", "unknown"}
WEB_HEADER_ALLOWLIST = {"strict-transport-security", "content-security-policy", "x-content-type-options", "x-frame-options", "referrer-policy", "permissions-policy", "content-type", "cache-control"}


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
    runtime_commands = {
        name: shutil.which(name) is not None
        for name in ("python", "python3", "pkg", "dpkg-query", "git", "proot", "proot-distro", "nethunter", "nh")
    }
    proot_rootfs = Path(prefix) / "var" / "lib" / "proot-distro" / "installed-rootfs" if prefix else None
    home_rootfs_markers = [home / "kali-arm64", home / "kali-fs"]
    nethunter_launcher = runtime_commands["nethunter"] or runtime_commands["nh"]
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
        "available_runtime_commands": runtime_commands,
        "optional_linux_environments": {
            "proot_available": runtime_commands["proot"],
            "proot_distro_available": runtime_commands["proot-distro"],
            "installed_proot_rootfs_directory_present": bool(proot_rootfs and proot_rootfs.is_dir()),
            "nethunter_launcher_available": nethunter_launcher,
            "nethunter_rootfs_marker_present": any(path.exists() for path in home_rootfs_markers),
            "interpretation": "Presence indicators only. No container was entered, no root privileges were tested, and no kernel capabilities were checked.",
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
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ValueError("APK could not be read for hashing") from exc
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




class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS connection pinned to a previously validated public IP address."""

    def __init__(self, host: str, pinned_ip: str, timeout: float, context: ssl.SSLContext):
        super().__init__(host, port=443, timeout=timeout, context=context)
        self._pinned_ip = pinned_ip

    def connect(self) -> None:
        # Avoid a second DNS lookup after validation, which could enable DNS rebinding.
        raw = socket.create_connection((self._pinned_ip, self.port), self.timeout, self.source_address)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except BaseException:
            raw.close()
            raise


def run_web_api_review(scope: str) -> dict:
    """Perform one bounded HTTPS HEAD request; never follows redirects or reads a body."""
    from urllib.parse import urlsplit

    if not isinstance(scope, str) or len(scope) > 2048 or any(ord(ch) < 32 or ch.isspace() for ch in scope):
        raise ValueError("web-api-review scope must be a single HTTPS URL without whitespace or control characters")
    if "*" in scope or "\\" in scope:
        raise ValueError("web-api-review does not accept wildcard or backslash URL scopes")
    try:
        parts = urlsplit(scope)
        host = parts.hostname
        port = parts.port
    except ValueError as exc:
        raise ValueError("web-api-review scope is not a valid URL") from exc
    if parts.scheme.lower() != "https" or not host:
        raise ValueError("web-api-review requires an explicit HTTPS URL")
    if parts.username is not None or parts.password is not None:
        raise ValueError("web-api-review URL must not contain embedded credentials")
    if parts.query or parts.fragment:
        raise ValueError("web-api-review URL must not contain a query string or fragment")
    if port not in (None, 443):
        raise ValueError("web-api-review only permits the default HTTPS port 443")
    if any(segment == ".." for segment in parts.path.split("/")):
        raise ValueError("web-api-review path must not contain parent-directory segments")
    try:
        host = host.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise ValueError("web-api-review hostname is invalid") from exc
    path = parts.path or "/"
    report = {
        "adapter_schema": ADAPTER_SCHEMA,
        "workflow_id": "web-api-review",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target_host": host,
        "target_path": path,
        "request": {"method": "HEAD", "timeout_seconds": 5, "redirects_followed": False, "response_body_read": False},
        "response": None,
        "request_status": "request_failed",
        "execution": {
            "network_actions_executed": True,
            "subprocesses_executed": False,
            "catalog_tools_executed": False,
            "request_count": 1,
        },
        "limitations": [
            "This makes exactly one HTTPS HEAD request to the supplied host and path. It is an active network request and requires explicit authorization.",
            "Redirects are not followed and response bodies are not read. A server may handle HEAD differently from GET.",
            "This is not a vulnerability scan, API schema review, authentication test, or security certification.",
            "Only an allowlist of response headers is retained; the report does not independently prove application behavior.",
        ],
    }
    connection = None
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        resolved = []
        for address in addresses:
            ip_text = address[4][0].split("%", 1)[0]
            try:
                parsed_ip = ipaddress.ip_address(ip_text)
            except ValueError:
                continue
            if not parsed_ip.is_global:
                raise ValueError("web-api-review refuses hostnames that resolve to non-public IP addresses")
            if ip_text not in resolved:
                resolved.append(ip_text)
        if not resolved:
            raise OSError("hostname did not resolve to a public IP address")
        # Prefer IPv4 for broader mobile-network compatibility; TLS still validates the hostname.
        pinned_ip = next((item for item in resolved if ipaddress.ip_address(item).version == 4), resolved[0])
        connection = _PinnedHTTPSConnection(
            host, pinned_ip=pinned_ip, timeout=5, context=ssl.create_default_context()
        )
        connection.request("HEAD", path, headers={"User-Agent": "SYN_LAUNCH/1.0"})
        response = connection.getresponse()
        headers = {}
        for name, value in response.getheaders():
            key = name.lower()
            if key in WEB_HEADER_ALLOWLIST and key not in headers:
                headers[key] = value[:512]
        report["response"] = {
            "status_code": int(response.status),
            "reason": str(response.reason or "")[:128],
            "headers": headers,
            "redirect_response_not_followed": 300 <= int(response.status) < 400,
        }
        report["request_status"] = "response_received"
    except (OSError, ssl.SSLError, http.client.HTTPException, TimeoutError) as exc:
        report["error_type"] = type(exc).__name__
    finally:
        if connection is not None:
            try:
                connection.close()
            except OSError:
                pass
    return report


def run_assessment_report(scope: str) -> dict:
    """Validate and summarize a local JSON evidence bundle without contacting targets."""
    candidate = Path(scope).expanduser()
    if candidate.suffix.lower() != ".json":
        raise ValueError("assessment-report adapter requires a local .json evidence file")
    try:
        path = candidate.resolve(strict=True)
        info = path.stat()
    except OSError as exc:
        raise ValueError("Evidence JSON path does not resolve to a readable local file") from exc
    if not path.is_file():
        raise ValueError("Evidence path must identify a regular file")
    if info.st_size <= 0 or info.st_size > MAX_EVIDENCE_JSON_BYTES:
        raise ValueError(f"Evidence JSON must be between 1 byte and {MAX_EVIDENCE_JSON_BYTES} bytes")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError("Evidence JSON could not be read") from exc
    digest = hashlib.sha256(raw).hexdigest()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Evidence file must be valid UTF-8 JSON") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("findings"), list):
        raise ValueError("Evidence JSON must be an object containing a findings list")
    findings = payload["findings"]
    if len(findings) > MAX_FINDINGS:
        raise ValueError(f"Evidence JSON may contain at most {MAX_FINDINGS} findings")
    normalized = []
    counts = {severity: 0 for severity in sorted(SEVERITIES)}
    required = ("title", "severity", "asset", "evidence", "remediation")
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValueError(f"Finding {index + 1} must be an object")
        item = {}
        for key in required:
            value = finding.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Finding {index + 1} requires non-empty string field '{key}'")
            if len(value) > 4000:
                raise ValueError(f"Finding {index + 1} field '{key}' exceeds 4000 characters")
            item[key] = value.strip()
        severity = item["severity"].lower()
        if severity not in SEVERITIES:
            raise ValueError(f"Finding {index + 1} severity must be one of: {', '.join(sorted(SEVERITIES))}")
        item["severity"] = severity
        counts[severity] += 1
        normalized.append(item)
    return {
        "adapter_schema": ADAPTER_SCHEMA,
        "workflow_id": "assessment-report",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_basename": path.name,
        "input_sha256": digest,
        "finding_count": len(normalized),
        "severity_counts": counts,
        "findings": normalized,
        "execution": {
            "network_actions_executed": False,
            "subprocesses_executed": False,
            "catalog_tools_executed": False,
            "evidence_file_modified": False,
        },
        "verification": "input_schema_validated_only",
        "limitations": [
            "This report organizes supplied evidence; it does not independently verify the findings or their severity.",
            "Do not include live credentials, session tokens, or personal data in evidence fields.",
            "Protect the source file and report as potentially sensitive assessment material.",
        ],
    }


def run_workflow_adapter(workflow_id: str, scope: str) -> dict:
    if workflow_id == "web-api-review":
        return run_web_api_review(scope)
    if workflow_id == "device-configuration-audit":
        return run_device_configuration_audit(scope)
    if workflow_id == "mobile-app-review":
        return run_mobile_apk_inventory(scope)
    if workflow_id == "assessment-report":
        return run_assessment_report(scope)
    raise ValueError(
        "No execution adapter is approved for this workflow yet; use --workflow-plan to create a dry-run plan."
    )
