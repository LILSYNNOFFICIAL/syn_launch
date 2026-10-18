# Workflow Planning

SYN_LAUNCH's workflow planner creates reviewable JSON plans. It is a preparation feature, not an assessment engine.

## Available plans

- `web-api-review`: review planning for an explicitly scoped web app or API.
- `mobile-app-review`: owner-provided mobile application and isolated test environment.
- `device-configuration-audit`: non-destructive review of the operator's own Android/Termux setup.
- `assessment-report`: evidence organization and remediation reporting.

## Usage

List workflows:

```bash
python main.py --workflow-list
```

Create a plan:

```bash
python main.py --workflow-plan web-api-review --target-scope "https://staging.example.test/api" --authorized
```

The target-scope value should identify the exact authorized assets or environment. Avoid wildcards and broad domains when the engagement scope is narrower.

## Safety behavior

- Both `--target-scope` and `--authorized` are required to generate a plan.
- The authorization flag is only the operator's declaration. It is not verified by the software and does not grant permission.
- Plans contain stop conditions and state `network_actions_executed: false` and `subprocesses_executed: false`.
- The planner does not invoke catalog executables, run scans, contact targets, change device state, or install packages.
- Plans are templates. They do not prove that a check was performed or that a target is secure.
- Future command adapters must receive a separate safety review, scope enforcement, bounded execution, and tests before they can run anything.

## Errors

The command exits with status 2 if the workflow is unknown, scope is missing or invalid, or the authorization declaration is absent. Use `--workflow-list` to retrieve the exact workflow IDs.
