# OSINT & Recon: Tool Guide

This page covers **25 catalog entries** in the SYN_LAUNCH **OSINT & Recon** category. It describes each tool's purpose, how to get started, upstream source, install method, and known caveats.

Tools for gathering public information and mapping authorized assessment scope. Respect privacy, platform terms, and rate limits.

## Before using a tool

1. Start SYN_LAUNCH in Termux with `python main.py` from the repository directory.
2. Browse the category in the menu, search by name, or inspect an entry with `python main.py --tool "TOOL NAME"`.
3. Read the description, installation method, compatibility notes, and caveats before running anything.
4. Review install prompts; manual-only tools must be installed using upstream instructions.
5. Treat examples as starting points. Check upstream docs, understand each option, and use only your own lab or explicitly authorized scope.

> **Compatibility note:** Catalog presence and a source/package link do not prove that a tool installs or runs on every Android device. Architecture, native dependencies, root access, Android permissions, hardware, credentials, and external services may affect availability. See [Compatibility and verification](Compatibility-and-Verification.md).

## Tools in this category

### Amass

**What it is used for:** Attack-surface mapping and asset discovery for authorized domains.

**How to start:**
```bash
amass -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/owasp-amass/amass)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/owasp-amass/amass/blob/79299dce87b0085db0f2f4ef3e9c52cccb49f514/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### anew

**What it is used for:** Append unique lines to files for repeatable recon pipelines.

**How to start:**
```bash
anew --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/tomnomnom/anew@latest`.

**Upstream project / source:** [Open source](https://github.com/tomnomnom/anew)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/tomnomnom/anew/blob/d67d68db0d56469fdea7505c5a9209c0a465effa/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Review pipeline inputs before writing results to persistent files.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### assetfinder

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
assetfinder --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/tomnomnom/assetfinder@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/tomnomnom/assetfinder)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/tomnomnom/assetfinder/blob/4e95d8701aae8cff1c27af2626eb22ba110ad583/README.md). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

---

### dnstwist

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
dnstwist --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `dnstwist`.

**Upstream project / source:** [Open source](https://github.com/elceef/dnstwist)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/elceef/dnstwist/blob/341395377f40761fe4152f43fd18eea757b6069a/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** DNS and optional external domain/reputation services, depending on configuration.

---

### dnsx

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
dnsx --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/projectdiscovery/dnsx/cmd/dnsx@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/projectdiscovery/dnsx/cmd/dnsx)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/projectdiscovery/dnsx/blob/eab63beacfde09ea66b9383229b127f00befe7ce/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### email-validator

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
email_validator --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `email-validator`.

**Upstream project / source:** [Open source](https://pypi.org/project/email-validator/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/JoshData/python-email-validator/blob/4f3293942e624a7630083c66930127102433ccb1/setup.cfg). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** DNS resolution service if deliverability checks are enabled..

---

### gau

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
gau --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/lc/gau/v2/cmd/gau@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/lc/gau/v2/cmd/gau)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/lc/gau/blob/4eabace309877abb231def9eeb27b96c07ed3635/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### gauplus

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
gauplus --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/bp0lr/gauplus@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/bp0lr/gauplus)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/bp0lr/gauplus/blob/15a2900b88092da32ba45860e76527985421ec8e/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** External services or target systems may be contacted depending on the selected command and configuration..

---

### h8mail

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
h8mail --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `h8mail`.

**Upstream project / source:** [Open source](https://github.com/khast3x/h8mail)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/khast3x/h8mail/blob/ee31c8ff6d148580047ae5048fea2234decb5932/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Third-party breach-data sources and optional API services, depending on configuration..

---

### holehe

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
holehe --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `holehe`.

**Upstream project / source:** [Open source](https://pypi.org/project/holehe/)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/megadose/holehe/blob/14da70f588538936b20d238783c5e28a0772a2b3/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Third-party account/service endpoints queried by the tool.

---

### httpx

**What it is used for:** ProjectDiscovery's Go HTTP probe for scoped web assets, not Python httpx.

**How to start:**
```bash
httpx --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/projectdiscovery/httpx/cmd/httpx@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/projectdiscovery/httpx/cmd/httpx)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/projectdiscovery/httpx/blob/482ce7bc66584a678fa7fe89c906a9ccafa7bc92/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### katana

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
katana --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/projectdiscovery/katana/cmd/katana@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/projectdiscovery/katana/cmd/katana)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/projectdiscovery/katana/blob/3e650646252e4a763d0fc230aff8bf96a3d86303/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### Maigret

**What it is used for:** Username OSINT across supported websites.

**How to start:**
```bash
maigret --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `maigret`.

**Upstream project / source:** [Open source](https://github.com/soxoj/maigret)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/soxoj/maigret/blob/eaf820666d15bfd545129f3223e2261c27191e74/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Third-party websites queried during an operator-selected username search..

---

### naabu

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
naabu --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/projectdiscovery/naabu/v2/cmd/naabu@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/projectdiscovery/naabu/v2/cmd/naabu)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/projectdiscovery/naabu/blob/25d4a43927a5d4508a765b33b0b2659349f6d71e/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### OSRFramework

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
osrframework --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `osrframework`.

**Upstream project / source:** [Open source](https://github.com/i3visio/osrframework)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/osinter-project/osrframework/blob/82f9e4637a9ef3cdabe85b31f42bce9a5a880e1e/setup.py). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Third-party identity/search providers and APIs used by selected OSRFramework modules..

---

### PhoneInfoga

**What it is used for:** Phone-number format and public metadata OSINT; it does not reveal live GPS location.

**How to start:**
```bash
phoneinfoga --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/sundowndev/phoneinfoga/v2@latest`.

**Upstream project / source:** [Open source](https://github.com/sundowndev/phoneinfoga)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/sundowndev/phoneinfoga/blob/55807b05b753dab7bc6fe67403ca385668dda179/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### PureDNS

**What it is used for:** Resolve and validate large candidate domain lists for scoped reconnaissance.

**How to start:**
```bash
puredns --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/d3mondev/puredns/v2@latest`.

**Upstream project / source:** [Open source](https://github.com/d3mondev/puredns)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/d3mondev/puredns/blob/46bd4c963ec2b28c5241c03c161bdc41bb93fdc0/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Large resolver workloads can burden DNS infrastructure; use approved resolvers and conservative rates.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### recon-ng

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
recon-ng --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `recon-ng`.

**Upstream project / source:** [Open source](https://github.com/lanmaster53/recon-ng)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/lanmaster53/recon-ng/blob/32b08fe7b6993ca1f2d8f76ba8f5d23c7f34a11d/REQUIREMENTS). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

---

### Sherlock

**What it is used for:** Search supported public websites for a username's public profiles.

**How to start:**
```bash
sherlock --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `sherlock-project`.

**Upstream project / source:** [Open source](https://github.com/sherlock-project/sherlock)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/sherlock-project/sherlock/blob/e40a45ec2a074b90703b3b4b842c8a3adbd6ada3/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Third-party websites queried by the operator-selected search run..

---

### SpiderFoot

**What it is used for:** Automated OSINT collection and correlation; resource-intensive on some Android devices.

**How to start:**
```bash
sf.py --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `spiderfoot`.

**Upstream project / source:** [Open source](https://github.com/smicallef/spiderfoot)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/smicallef/spiderfoot/blob/0f815a203afebf05c98b605dba5cf0475a0ee5fd/requirements.txt). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** External websites, DNS, and service integrations selected by SpiderFoot modules.

---

### subfinder

**What it is used for:** Passive subdomain discovery for domains in your authorized scope.

**How to start:**
```bash
subfinder --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/projectdiscovery/subfinder/v2/cmd/subfinder)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/projectdiscovery/subfinder/blob/7d9038297953f6a953ba3eb009fb859993959d00/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

### theHarvester

**What it is used for:** Collect public-source domain, email, and host metadata for scoped reconnaissance.

**How to start:**
```bash
theHarvester -h
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Python package (isolated virtual environment where supported); package/module: `theHarvester`.

**Upstream project / source:** [Open source](https://github.com/laramies/theHarvester)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/laramies/theHarvester/blob/49a38f8d33c32336bbf6a111ea723ea223116265/pyproject.toml). This documents source metadata, not verified device functionality.

**Important note:** Python package installation can fail if upstream dependencies lack Android-compatible wheels.

**External services / environment:** Third-party search providers and APIs selected by the operator; API keys/rate limits may apply..

---

### unfurl

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
unfurl --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/tomnomnom/unfurl@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/tomnomnom/unfurl)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/tomnomnom/unfurl/blob/8f10d050f1b0be12e505053da174f3f39e8eed74/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

---

### urlcrazy

**What it is used for:** Generate domain permutations to support defensive typosquatting and lookalike-domain review.

**How to start:**
```bash
urlcrazy --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Manual setup (follow upstream documentation).

**Upstream project / source:** [Open source](https://github.com/urbanadventurer/urlcrazy)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/urbanadventurer/urlcrazy/blob/78bf6e855d6d83e387ae3b5c8ffc36f241b96f66/Gemfile). This documents source metadata, not verified device functionality.

**Important note:** Catalog entry only until a verified Termux-compatible install path is available.

---

### waybackurls

**What it is used for:** Reconnaissance utility for collecting public-source identity or asset metadata. Respect provider terms, privacy, and engagement scope.

**How to start:**
```bash
waybackurls --help
```

This is the catalog's example command, not a guarantee that it will work unchanged on Android. Check the tool's help, confirm paths and options, and only target systems or data you are authorized to use.

**Catalog install path:** Go module / binary; package/module: `github.com/tomnomnom/waybackurls@latest`.

**Upstream project / source:** [Open source](https://pkg.go.dev/github.com/tomnomnom/waybackurls)

**Packaging or compatibility evidence:** [Open source evidence](https://github.com/tomnomnom/waybackurls/blob/8d27cf3e3031de01179e8ba9127e968eb01008e9/go.mod). This documents source metadata, not verified device functionality.

**Important note:** Requires Go; upstream module/build compatibility must be checked for the selected release.

**External services / environment:** Target systems or external data providers depending on the selected command and configuration..

---

## Related pages

- [Using SYN_LAUNCH](Using-SYN-LAUNCH.md)
- [Installation and first run](Installation.md)
- [Catalog and tool lifecycle](Catalog-and-Tool-Lifecycle.md)
- [Compatibility and verification](Compatibility-and-Verification.md)
- [Security and responsible use](Security-and-Responsible-Use.md)
