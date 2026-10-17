# Contributing to SYN_LAUNCH

Thank you for helping improve Termux compatibility and security-tool coverage.

## Adding or updating a catalog entry

Every entry must include:
- stable lowercase kebab-case `id`;
- unique display name and category;
- executable name;
- install method (`pkg`, `pip`, `go`, `cargo`, `npm`, `manual`, or `root`);
- package/module name for automated methods;
- specific description, safe example/help command, HTTPS upstream source, and honest Termux compatibility caveat;
- correct `installable` flag.

Use the official upstream repository or package documentation where possible. Do not label a tool automatically installable unless its package/module identifier is valid and its install path is known. Avoid invented links, undocumented binary names, and claims of Android support without evidence. For tools that need root, external Wi-Fi adapters, desktop Linux, cloud credentials, or a companion Android app, say so.

## Installer safety

- Never use `shell=True` or concatenate user-controlled input into a shell command.
- Validate any new package/module syntax.
- Keep installs opt-in and explain when third-party build scripts execute.
- Do not run scans or payloads automatically.
- Avoid collecting credentials, targets, or private reports in logs.
- Preserve timeouts and graceful failure reporting.

## Before submitting

~~~bash
python -m py_compile main.py
bash -n install.sh
python -m unittest discover -s tests -v
python main.py --check
python main.py --search Nuclei
~~~

CI success on Ubuntu is not evidence that a package works on Android. Record real Termux/architecture results separately.
