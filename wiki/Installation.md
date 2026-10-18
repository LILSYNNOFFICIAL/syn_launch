# Installation and first run

## Requirements

- Android device with a supported Termux installation.
- Termux installed from a maintained source. Do not mix Termux apps/plugins signed by incompatible sources.
- Git and Python available through Termux packages.

## Install

```bash
pkg update -y
pkg install -y git python
git clone https://github.com/LILSYNNOFFICIAL/syn_launch.git
cd syn_launch
bash install.sh
python main.py
```

Rich is optional; the app can use a plain-text interface without it.

## Useful commands

```bash
python main.py --check
python main.py --doctor
python main.py --profile
python main.py --list
python main.py --search nuclei
python main.py --category "Mobile App Security"
python main.py --tool Nmap
python main.py --compatibility-report > compatibility-report.json
python main.py --smoke-test python
```

The compatibility report is metadata/discovery output and never executes cataloged tools. `--smoke-test` explicitly probes one named entry's version/help response with time/output caps. It is not a full feature test. Review local paths, runtime details, and saved probe evidence before sharing reports.
