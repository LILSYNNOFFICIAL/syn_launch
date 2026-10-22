# Cloud & Container Security: Tool Guide

This page covers **12 catalog entries** in the SYN_LAUNCH **Cloud & Container Security** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools for reviewing cloud identities, configurations, container images, and cloud resources. Prefer test accounts and least privilege.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### CloudFox

**What it is used for:** Cloud asset and permission enumeration for authorized security reviews.

**How to start:**
```bash
cloudfox --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/BishopFox/cloudfox@latest`.

**Upstream project / source:** [Open source](https://github.com/BishopFox/cloudfox)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/BishopFox/cloudfox/blob/d44899f21302269fc5e7743c662edafe15c7575c/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Cloud credentials and reports are sensitive.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### Cloudsplaining

**What it is used for:** Identify risky AWS IAM permissions from IAM policy data for defensive cloud reviews.

**How to start:**
```bash
cloudsplaining --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `cloudsplaining`.

**Upstream project / source:** [Open source](https://github.com/salesforce/cloudsplaining)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/salesforce/cloudsplaining/blob/f2ed0ba2ddf6457143203d46971c91ba236b6597/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Handle policy exports as sensitive data; findings need review against actual role usage.

**External services / environment:** AWS APIs or exported IAM policy data depending on the workflow.

---

### Dockle

**What it is used for:** Check container images for common security and configuration best-practice issues.

**How to start:**
```bash
dockle --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/goodwithtech/dockle@latest`.

**Upstream project / source:** [Open source](https://github.com/goodwithtech/dockle)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/goodwithtech/dockle/blob/35171ccb9b247592269f5c84be69331ef0ad6c19/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Image support and native dependencies vary; scan only images you are permitted to inspect.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### Kube-Bench

**What it is used for:** Check Kubernetes configuration against CIS benchmarks.

**How to start:**
```bash
kube-bench --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/aquasecurity/kube-bench)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/aquasecurity/kube-bench/blob/e278a5915a982f2756026de6e2f9ca77077ef9f9/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Usually requires host/cluster context unavailable on stock Android.

---

### Kube-Hunter

**What it is used for:** Kubernetes security assessment for authorized clusters.

**How to start:**
```bash
kube-hunter --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `kube-hunter`.

**Upstream project / source:** [Open source](https://github.com/aquasecurity/kube-hunter)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/aquasecurity/kube-hunter/blob/bc47f08e88ea2a5fb059bf3b8a8edb1aefb4c6cc/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Active probes can affect services; confirm scope.

**External services / environment:** Kubernetes API and node endpoints explicitly selected by the operator.

---

### kube-linter

**What it is used for:** Lint Kubernetes YAML and Helm charts for security and production-readiness issues.

**How to start:**
```bash
kube-linter --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `golang.stackrox.io/kube-linter/cmd/kube-linter@latest`.

**Upstream project / source:** [Open source](https://github.com/stackrox/kube-linter)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/stackrox/kube-linter/blob/ead88f5c9d49e600a58eae2c7121deef82e378f7/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Static checks do not replace cluster configuration review; Go builds may be resource-intensive.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### KubeAudit

**What it is used for:** Audit Kubernetes workload configuration for common security issues.

**How to start:**
```bash
kubeaudit --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/Shopify/kubeaudit@latest`.

**Upstream project / source:** [Open source](https://github.com/Shopify/kubeaudit)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/Shopify/kubeaudit/blob/92c3147139a73eab8f6c9cbf9a1ee4d9c4196bd8/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires manifests or authorized cluster access.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### Kubeletctl

**What it is used for:** Cloud/container security audit utility. Use authorized credentials, least privilege, and approved scope.

**How to start:**
```bash
kubeletctl --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/cyberark/kubeletctl@latest`.

**Upstream project / source:** [Open source](https://github.com/cyberark/kubeletctl)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/cyberark/kubeletctl/blob/2ea775d00d600db5ae9556739056f009bbd5286f/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Only target clusters you administer or are authorized to assess.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### Pacu

**What it is used for:** AWS cloud security testing framework for authorized assessment and lab exercises.

**How to start:**
Follow the [upstream installation and usage documentation](https://github.com/RhinoSecurityLabs/pacu) for supported setup steps and current command syntax. SYN_LAUNCH does not automatically install this entry.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/RhinoSecurityLabs/pacu)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/RhinoSecurityLabs/pacu/blob/e597f23ecfb88b82f706c5f0cac9d4577c2af262/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Contains high-impact cloud testing modules; use a dedicated lab account and explicit written authorization.

**External services / environment:** An explicitly authorized cloud, mobile-app, or directory environment when the tool is used for assessment..

---

### Prowler

**What it is used for:** Cloud security posture assessment for supported cloud providers.

**How to start:**
```bash
prowler --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `prowler`.

**Upstream project / source:** [Open source](https://github.com/prowler-cloud/prowler)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/prowler-cloud/prowler/blob/f45173997b8331e6cba3deac78bc2e1043b9281d/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Use authorized cloud credentials and least-privilege roles.

**External services / environment:** Cloud provider APIs and Kubernetes APIs depending on selected provider and checks.

---

### ScoutSuite

**What it is used for:** Multi-cloud security auditing and configuration review.

**How to start:**
```bash
scout --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `scoutsuite`.

**Upstream project / source:** [Open source](https://github.com/nccgroup/ScoutSuite)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/nccgroup/ScoutSuite/blob/7909f2fc6186063e5c9e7ddef8c4d7d1072c8f3d/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Cloud credentials and reports are sensitive.

**External services / environment:** Cloud provider APIs depending on configured credentials and selected provider.

---

### Terrascan

**What it is used for:** Static analysis for infrastructure-as-code security and compliance issues.

**How to start:**
```bash
terrascan --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/tenable/terrascan@latest`.

**Upstream project / source:** [Open source](https://github.com/tenable/terrascan)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/tenable/terrascan/blob/dafb3e0ad72812fbecfc36d33e8bd4347f12b114/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Policy coverage and Android build compatibility vary.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
