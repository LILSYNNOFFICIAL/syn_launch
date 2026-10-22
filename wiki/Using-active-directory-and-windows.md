# Active Directory & Windows: Tool Guide

This page covers **12 catalog entries** in the SYN_LAUNCH **Active Directory & Windows** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools for assessing Windows and directory environments. Protect credentials and collected identity data.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### BloodHound Python Collector

**What it is used for:** Collect Active Directory relationship data for authorized domain audits.

**How to start:**
```bash
bloodhound-python --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `bloodhound`.

**Upstream project / source:** [Open source](https://github.com/dirkjanm/BloodHound.py)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/dirkjanm/BloodHound.py/blob/fd3f322e066d66314bfb31d4ae6f497df5872177/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Collected directory data is sensitive.

**External services / environment:** An explicitly authorized cloud, mobile-app, or directory environment when the tool is used for assessment..

---

### BloodyAD

**What it is used for:** Active Directory administration and security testing utility; some operations modify directory state.

**How to start:**
```bash
bloodyAD --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `bloodyAD`.

**Upstream project / source:** [Open source](https://github.com/CravateRouge/bloodyAD)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/CravateRouge/bloodyAD/blob/48df0a8ee5bd0bad66fca21a2088449b48dc4ed0/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Some operations modify directory state; review each action.

**External services / environment:** Active Directory and LDAP endpoints explicitly selected by the operator.

---

### Certipy

**What it is used for:** Audit Active Directory Certificate Services in authorized domains.

**How to start:**
```bash
certipy-ad -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `certipy-ad`.

**Upstream project / source:** [Open source](https://github.com/ly4k/Certipy)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/ly4k/Certipy/blob/3ae34426c58d266a1979ff9607514c3d7fe1aa21/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Certificate abuse paths are sensitive; restrict use to approved domains.

**External services / environment:** Active Directory Certificate Services and directory endpoints explicitly selected by the operator.

---

### Coercer

**What it is used for:** Assess Windows authentication coercion exposure in controlled environments.

**How to start:**
```bash
coercer --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `coercer`.

**Upstream project / source:** [Open source](https://github.com/p0dalirius/Coercer)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/p0dalirius/Coercer/blob/6024441c708e330582ffc8e4eccc80b931807194/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Can trigger authentication traffic; explicit authorization required.

**External services / environment:** Windows/Active Directory services explicitly selected by the operator.

---

### enum4linux-ng

**What it is used for:** SMB and Windows domain enumeration for authorized assessments.

**How to start:**
```bash
enum4linux-ng --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `enum4linux-ng`.

**Upstream project / source:** [Open source](https://github.com/cddmp/enum4linux-ng)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/cddmp/enum4linux-ng/blob/288826fd9ee89b61d846e59f17b77bae4fb671ee/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Enumeration may disclose directory information.

**External services / environment:** SMB and related network services explicitly selected by the operator.

---

### Evil-WinRM

**What it is used for:** WinRM client for authorized Windows lab assessments.

**How to start:**
```bash
evil-winrm --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/Hackplayers/evil-winrm)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/Hackplayers/evil-winrm/blob/64d8e0f962d239643c4efadacce9f716bd5cb775/evil-winrm.gemspec). This documents source metadata, not verified device functionality.

**Important note:** Credentialed remote shell access; manual-only.

---

### Impacket

**What it is used for:** Python protocol toolkit for network protocol testing and Windows domain labs.

**How to start:**
```bash
impacket-smbclient --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `impacket`.

**Upstream project / source:** [Open source](https://github.com/fortra/impacket)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/fortra/impacket/blob/75938fcb0145b476250940d740f71394676288cb/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Credentialed actions are sensitive; use approved lab accounts.

**External services / environment:** Network services or directory environments explicitly selected for protocol operations.

---

### Kerbrute

**What it is used for:** Kerberos user enumeration and testing for controlled AD labs.

**How to start:**
```bash
kerbrute -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/ropnop/kerbrute@latest`.

**Upstream project / source:** [Open source](https://github.com/ropnop/kerbrute)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/ropnop/kerbrute/blob/9cfb81e4fab8037acb44c678773ca3f93bc2b39c/go.mod). This documents source metadata, not verified device functionality.

**Important note:** May trigger account lockouts; password spraying requires explicit approval.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### LDAPDomainDump

**What it is used for:** Export LDAP directory information for authorized domain auditing.

**How to start:**
```bash
ldapdomaindump --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `ldapdomaindump`.

**Upstream project / source:** [Open source](https://github.com/dirkjanm/ldapdomaindump)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/dirkjanm/ldapdomaindump/blob/d559463eb29857f2660bf3867bfb9f8610d1ddb1/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Treat output as confidential.

**External services / environment:** LDAP and DNS services explicitly selected by the operator.

---

### NetExec

**What it is used for:** Network service assessment toolkit for authorized internal testing.

**How to start:**
```bash
nxc --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `netexec`.

**Upstream project / source:** [Open source](https://github.com/Pennyw0rth/NetExec)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/Pennyw0rth/NetExec/blob/0615464f7aed3daa64a3ebe414d1fd7dc830db0b/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Credentialed checks can affect systems; stay within approved scope.

**External services / environment:** Network services and identity infrastructure explicitly selected by the operator.

---

### Responder

**What it is used for:** Network protocol analysis and poisoning tool for isolated labs; can intercept credentials and disrupt networks.

**How to start:**
```bash
python Responder.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/lgandx/Responder)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/lgandx/Responder/blob/424fbe53d6a61824e3c7685fe5f69668721b821e/requirements.txt). This documents source metadata, not verified device functionality.

**Important note:** Poisoning can intercept credentials or disrupt networks; lab-only.

---

### RustHound-CE

**What it is used for:** Collect Active Directory relationship data for authorized BloodHound assessments.

**How to start:**
Follow the [upstream installation and usage documentation](https://github.com/g0h4n/RustHound-CE) for supported setup steps and current command syntax. SYN_LAUNCH does not automatically install this entry.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/g0h4n/RustHound-CE)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/g0h4n/RustHound-CE/blob/bb9e7522106726b85f9bf5f7ca2d598f9dc87ce8/Cargo.toml). This documents source metadata, not verified device functionality.

**Important note:** Directory collection accesses sensitive identity data; obtain explicit scope and protect output files.

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
