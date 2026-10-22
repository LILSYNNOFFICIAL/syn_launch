# Cloud, Containers & Misc: Tool Guide

This page covers **26 catalog entries** in the SYN_LAUNCH **Cloud, Containers & Misc** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

General cloud, container, automation, and infrastructure utilities. Review account scope and state-changing actions.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### age-plugin-yubikey

**What it is used for:** Use supported YubiKey PIV keys with age encryption; requires compatible hardware.

**How to start:**
```bash
age-plugin-yubikey --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/str4d/age-plugin-yubikey)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/str4d/age-plugin-yubikey/blob/cafbc75fbd309e6f7ab62749052f98a91a89764e/Cargo.toml). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**Hardware requirements:** YubiKey or supported PIV hardware token.

---

### Ansible

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
ansible --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `ansible-core`.

**Upstream project / source:** [Open source](https://github.com/ansible/ansible)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/ansible/ansible/blob/f7319e09448e13fa2bc407a1afcd8990f47040fb/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Managed hosts and services defined by the operator's inventory and playbooks.

---

### base64

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
base64 --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `coreutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/coreutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### chkrootkit

**What it is used for:** Rootkit checks for supported Unix/Linux hosts; not a reliable stock-Android integrity check.

**How to start:**
```bash
chkrootkit -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/Magentron/chkrootkit)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/Magentron/chkrootkit/blob/c00b5a40f61cc969e56fa2fe3375741c4164c896/README). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### ClamAV

**What it is used for:** Scan accessible files; signature updates and storage need setup.

**How to start:**
```bash
clamscan --version
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `clamav`.

**Upstream project / source:** [Open source](https://github.com/Cisco-Talos/clamav)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/clamav). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

**External services / environment:** Signature database update source, if current signatures are required..

---

### Docker CLI

**What it is used for:** Docker client for connecting to a reachable Docker Engine; the daemon is not provided by stock Termux.

**How to start:**
```bash
docker --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `docker-cli`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/docker-cli). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### FreshClam

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
freshclam --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `clamav`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/clamav). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### GNU Parallel

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
parallel --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `parallel`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/parallel). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### gzip

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
gzip --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `gzip`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/gzip). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### htop

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
htop --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `htop`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/htop). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### kubectl

**What it is used for:** Kubernetes CLI for clusters you administer or are authorized to assess.

**How to start:**
```bash
kubectl version --client
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `kubectl`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/kubectl). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### lsof

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
lsof --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `lsof`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/lsof). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Podman

**What it is used for:** Container engine and CLI; Android kernel and namespace support can prevent normal operation.

**How to start:**
```bash
podman --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/containers/podman)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/podman-container-tools/podman/blob/8dd1367b23419bec0f4bc37c6c56f87965184375/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**External services / environment:** Container image registries and optional remote container services depending on configuration..

---

### ps

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
ps --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `procps`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/procps). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### rclone

**What it is used for:** Manage file transfers and backups across supported storage providers.

**How to start:**
```bash
rclone version
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `rclone`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/rclone). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### restic

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
restic --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `restic`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/restic). This documents source metadata, not verified device functionality.

**Important note:** Pinned upstream Termux recipe is documented; actual repository availability and device runtime remain unverified.

---

### rkhunter

**What it is used for:** Rootkit and configuration checks for supported Unix/Linux systems; limited relevance on stock Android.

**How to start:**
```bash
rkhunter --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/Rootkit-Hunter/rootkit_hunter)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/Rootkit-Hunter/rkhunter/blob/016a77924ef4311fa7cac3737b7460452349b6ca/files/rkhunter). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

**External services / environment:** Optional update/mirror endpoints used to retrieve signatures and data files..

---

### sha256sum

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
sha256sum --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `coreutils`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/coreutils). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### stress-ng

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
stress-ng --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `stress-ng`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/ColinIanKing/stress-ng/blob/9beb21e28c727a5e02572ee2031977f23587d7e7/README.md). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### tar

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
tar --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `tar`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/tar). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### Terraform

**What it is used for:** Infrastructure-as-code workflow for cloud resources you control.

**How to start:**
```bash
terraform -help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/hashicorp/terraform)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/hashicorp/terraform/blob/44fcc1316e98d4a03cc348c05e6d5ba8e36bf51c/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### unzip

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
unzip --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `unzip`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/unzip). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### watch

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
watch --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `procps`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/procps). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### xmlstarlet

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
xmlstarlet --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `xmlstarlet`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/xmlstarlet). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### yq

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
yq --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `yq`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/yq). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

### zip

**What it is used for:** Cloud, container, system administration, or developer utility. Protect credentials and use least-privilege access.

**How to start:**
```bash
zip --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Termux package (`pkg`); package/module: `zip`.

**Upstream project / source:** [Open source](https://github.com/termux/termux-packages)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/termux/termux-packages/tree/e85983636adcf748134c3feb1df27f44e78322e1/packages/zip). This documents source metadata, not verified device functionality.

**Important note:** Package availability differs by Termux repository, architecture, and release.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
