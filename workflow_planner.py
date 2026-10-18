"""Authorization-gated, dry-run workflow planning for SYN_LAUNCH.

This module never executes tools or sends network traffic. It emits a scope-bound
plan that an operator can review before any future assessment integration.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

PLAN_SCHEMA = 1

WORKFLOWS = {
    "web-api-review": {
        "title": "Web application and API review",
        "purpose": "Plan a permissioned review of an explicitly scoped web application or API.",
        "steps": [
            "Confirm written authorization, owner, environment, and in-scope hostnames or API base URLs.",
            "Review public documentation, authentication boundaries, and provided test accounts.",
            "Inspect security headers, TLS configuration, and documented API behavior using approved methods.",
            "Record findings with minimal evidence, impact, and remediation guidance.",
        ],
        "stop_conditions": [
            "Stop if the target is not explicitly listed in the approved scope.",
            "Stop if testing risks production data, availability, or third-party systems.",
            "Stop if credentials, rate limits, or rules of engagement are unclear.",
        ],
    },
    "mobile-app-review": {
        "title": "Mobile application review",
        "purpose": "Plan a review of an app package and test environment supplied by the owner.",
        "steps": [
            "Record package identifier, version, signing identity, and source of the test build.",
            "Review permissions, exported components, network security configuration, and local data handling.",
            "Separate static observations from behavior confirmed on the authorized test device.",
            "Document reproducible findings and remediation recommendations.",
        ],
        "stop_conditions": [
            "Use only an owner-provided build or a build you are authorized to assess.",
            "Do not extract or access another person's data or credentials.",
            "Stop before interacting with production accounts or services outside the approved scope.",
        ],
    },
    "device-configuration-audit": {
        "title": "Device and Termux configuration audit",
        "purpose": "Plan a local, non-destructive review of the operator's own Android/Termux environment.",
        "steps": [
            "Record Android version, Termux source, architecture, package-manager availability, and storage headroom.",
            "Review installed package metadata and explicitly selected executable version/help output.",
            "Check file permissions, shell startup configuration, and package-source overrides.",
            "Record findings without changing packages or device settings.",
        ],
        "stop_conditions": [
            "Do not request root privileges solely to complete the checklist.",
            "Do not remove, upgrade, or reconfigure packages during an audit-only run.",
            "Stop if a check would expose secrets or modify user data.",
        ],
    },
    "assessment-report": {
        "title": "Assessment reporting",
        "purpose": "Prepare a report from evidence already collected under an approved engagement.",
        "steps": [
            "Map each finding to its evidence source, affected asset, and confidence level.",
            "Separate observed facts, inferred risk, and unverified hypotheses.",
            "Prioritize remediation by impact and realistic exploitability.",
            "Record scope limitations, checks not performed, and retest criteria.",
        ],
        "stop_conditions": [
            "Do not invent evidence or represent unperformed checks as passed.",
            "Remove secrets, personal data, and unrelated third-party information from the report.",
            "Do not expand the approved scope while writing findings.",
        ],
    },
}

_SCOPE_RE = re.compile(r"[^\\x00-\\x1f\\x7f]{1,500}\\Z")


def build_workflow_plan(name: str, target_scope: str, authorized: bool) -> dict:
    """Return a reviewable plan. Never launches subprocesses or performs network I/O."""
    if name not in WORKFLOWS:
        raise ValueError("unknown workflow; use --workflow-list to see available plans")
    if not isinstance(target_scope, str) or not _SCOPE_RE.fullmatch(target_scope.strip()):
        raise ValueError("target scope must be 1 to 500 printable characters")
    if not authorized:
        raise ValueError("explicit authorization confirmation is required")
    workflow = WORKFLOWS[name]
    return {
        "plan_schema": PLAN_SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workflow_id": name,
        "title": workflow["title"],
        "purpose": workflow["purpose"],
        "mode": "dry_run_plan_only",
        "authorized_by_operator": True,
        "target_scope": target_scope.strip(),
        "network_actions_executed": False,
        "subprocesses_executed": False,
        "steps": list(workflow["steps"]),
        "stop_conditions": list(workflow["stop_conditions"]),
        "disclaimer": "This is a planning document only. It does not run tools, validate authorization, or grant permission to test assets.",
    }
