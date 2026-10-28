# STATUS

## What was built

A local-first Python CLI, `prompt-expander`, that expands `{{variables}}` in prompt templates using records from a CSV or JSON data file and writes one ready-to-use prompt file per record.

- `prompt_expander/renderer.py` — `{{variable}}` expansion (whitespace inside braces allowed, missing variables left unchanged), variable detection, unresolved-variable reporting
- `prompt_expander/sources.py` — CSV (header row = variable names) and JSON (single object or list of objects) loaders
- `prompt_expander/cli.py` — argparse CLI: `--template`, `--data`, `--out`, `--dry-run`, `--ext`
- `prompt_expander/__main__.py` — `python -m prompt_expander` entry point
- `pyproject.toml` — packaging with `prompt-expander` console script, stdlib-only dependencies
- `tests/test_renderer.py`, `tests/test_cli.py` — 18 unittest tests, all passing
- `README.md` — usage, examples, credits Asdale Dynamics, LLC
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `STATUS.md` — this file

## How to run

```bash
# From the repo root
python3 -m prompt_expander --template template.txt --data leads.csv --out prompts

# Dry run (preview, no files written)
python3 -m prompt_expander --template template.txt --data leads.json --dry-run

# Custom extension
python3 -m prompt_expander --template template.txt --data data.csv --out output --ext .md

# Or install locally first
pip install .
prompt-expander --template template.txt --data data.csv --out output
```

Template example:

```
Hi {{name}},

Thanks for your interest in {{product}}.
```

Data example (CSV):

```
name,product
Dylan,The Massive AI Manual
Sam,The Massive AI Manual
```

Records with a `name`/`title` column produce files named after that value; otherwise `prompt_001.txt`, `prompt_002.txt`, ...

Local-first: standard library only, no network, no API keys, no secrets.

## Verification results

- `python3 -m compileall -q prompt_expander tests` — OK
- `python3 -m unittest discover -s tests -v` — 18 tests, OK
- Manual smoke test — CSV input (2 files), JSON input (single object + list), `--dry-run` (no files written), all output contents verified correct

## Known gaps

- No variable validation/fail-fast mode: unresolved `{{variables}}` are left unchanged in output rather than erroring
- CSV encoding is hard-coded to UTF-8
- Output filenames from `name`/`title` are sanitized but not uniquified; duplicate names overwrite
- No configuration file; CLI flags only
