# STATUS

## What was built

A local-first Python CLI, `prompt-expander`, that expands `{{variables}} in prompt templates using records from a CSV or JSON data file and writes one ready-to-use prompt file per record.

- `prompt_expander/renderer.py` — `{{variable}}` expansion (whitespace inside braces allowed, missing variables left unchanged), variable detection, unresolved-variable reporting
- `prompt_expander/sources.py` — CSV (header row = variable names) and JSON (single object or list of objects) loaders
- `prompt_expander/cli.py` — argparse CLI: `--template`, `--data`, `--out`, `--dry-run`, `--ext`
- `prompt_expander/__main__.py` — `python -m prompt_expander` entry point
- `pyproject.toml` — packaging with `prompt-expander` console script, stdlib-only dependencies
- `tests/test_renderer.py`, `tests/test_cli.py` — 18 unittest tests, all passing
- `examples/template.txt`, `examples/data.csv`, `examples/data.json` — ready-to-run example files
- `README.md` — usage, examples, credits Asdale Dynamics, LLC
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `.gitignore` — excludes `__pycache__`, `*.pyc`, `output/`, `.env`
- `STATUS.md` — this file

## How to run

```bash
# From the repo root (nothing to install)
python3 -m prompt_expander --template template.txt --data data.csv --out output

# Try the included examples
python3 -m prompt_expander --template examples/template.txt --data examples/data.csv --dry-run
python3 -m prompt_expander --template examples/template.txt --data examples/data.csv --out output

# Or with JSON data
python3 -m prompt_expander --template examples/template.txt --data examples/data.json --out output

# Install for the prompt-expander command
pip install .
prompt-expander --template template.txt --data data.csv --out output
```

| Option | What it does |
|--------|--------------|
| `--template` | Prompt template file with `{{variables}}` (required) |
| `--data` | `.csv` or `.json` data file, one record per prompt (required) |
| `--out` | Output directory (default: `output`) |
| `--dry-run` | Preview what would be written without saving files |
| `--ext` | Output file extension (default: `.txt`) |

Local-first: standard library only, no network, no API keys, no secrets.

## Verification results

- `python3 -m compileall -q prompt_expander tests examples` — OK
- `python3 -m unittest discover -s tests -v` — 18 tests, OK
- Manual smoke test — CSV input (3 files), JSON list input (3 files), `--dry-run` (no files written), all output contents verified correct

## Known gaps

- No variable validation/fail-fast mode: unresolved `{{variables}}` are left unchanged in output rather than erroring
- CSV and JSON encoding is hard-coded to UTF-8
- Output filenames from `name`/`title` are sanitized but not uniquified; duplicate names overwrite
- No configuration file; CLI flags only
