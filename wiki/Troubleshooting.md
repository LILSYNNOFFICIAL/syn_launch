# Troubleshooting

## `bash install.sh` fails

- Confirm you are inside the cloned `syn_launch` repository.
- Check network access and the configured Termux repositories.
- Avoid mixing Termux packages from incompatible signing sources.
- Read the full error before retrying; do not repeatedly run partial installation commands without understanding their effects.

## A tool is listed but will not install

A catalog entry may be manual-only, unavailable in the configured repository, unsupported by the device ABI, or dependent on native libraries that do not build on Android. Review the install method, upstream source, and caveat.

## A PATH match appears

A PATH match only means an executable name was discovered. It is not proof that the file belongs to the expected project or that the tool functions. Use explicit Help probing only when you choose it, and treat the result as bounded best-effort evidence.

## Compatibility report says `not_assessed`

That entry has no structured compatibility declaration yet. Do not infer compatibility from category, install method, or PATH status.

## Test or JSON validation fails

```bash
python -m py_compile main.py
bash -n install.sh
python -m json.tool catalog.json > /dev/null
python -m unittest discover -s tests -v
python main.py --check
python main.py --compatibility-report > compatibility-report.json
```

Inspect the first failing assertion/error and preserve the full output. Review generated reports for private paths and runtime details before sharing.
