# Development and contributing

## Local checks

```bash
python -m py_compile main.py
bash -n install.sh
python -m json.tool catalog.json > /dev/null
python -m unittest discover -s tests -v
python main.py --check
python main.py --doctor
python main.py --compatibility-report > compatibility-report.json
python main.py --smoke-test python
```

GitHub Actions runs the repository's automated checks on supported Python versions. CI on a desktop runner does not establish Android/Termux compatibility. CI runs a bounded Python version probe to verify the smoke-test path, but that still is not an Android device test.

## Catalog contributions

- Use a specific description and safe example.
- Provide an HTTPS upstream source and honest caveats.
- Use manual-only when a reliable Termux install route is not known.
- Validate package/module syntax and avoid shell command strings.
- Add compatibility metadata only when supported by an upstream source or repeatable test.
- Never describe a package recipe or PATH match as a successful functional test.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed requirements and [PLATFORM_ROADMAP.md](../PLATFORM_ROADMAP.md) for pending work.
