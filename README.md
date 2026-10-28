# prompt-expander

Local-first Python CLI that expands `{{variables}}` in prompt templates using data from a CSV or JSON file, producing ready-to-use prompt files saved locally.

Built and maintained by **Asdale Dynamics, LLC** (Indiana) — beginner-friendly AI education, books, guides, and practical open-source tools.

## What it does

Given a template like:

```
Dear {{name}},

Thanks for your interest in {{product}}. Reply to this email by {{deadline}}.
```

and a CSV file:

```csv
name,product,deadline
Dylan,The Massive AI Manual,Friday
Sam,The Massive AI Manual,Monday
```

run:

```bash
python -m prompt_expander --template template.txt --data leads.csv --out prompts
```

and get one file per row: `Dylan.txt`, `Sam.txt`, with the variables filled in.

## Features

- `{{variable}}` expansion with optional inner whitespace (`{{  name  }}`)
- CSV input (first row is the header of variable names)
- JSON input (a single object or a list of objects)
- Optional `name`/`title` column to name output files; otherwise `prompt_001.txt`, `prompt_002.txt`, ...
- `--dry-run` previews what would be written without touching the disk
- Standard library only — no dependencies, no network, no API keys, no secrets
- MIT licensed

## Install

```bash
pip install .
```

or run directly:

```bash
python -m prompt_expander --template template.txt --data data.csv --out output
```

A `prompt-expander` console script is also installed with `pip install .`.

## Usage

```
prompt-expander --template TEMPLATE --data DATA [--out DIR] [--dry-run] [--ext .txt]
```

- `--template` — prompt template file containing `{{variables}}` (required)
- `--data` — `.csv` or `.json` data file, one record per prompt (required)
- `--out` — output directory (default: `output`)
- `--dry-run` — print what would be produced without writing files
- `--ext` — output file extension (default: `.txt`)

## Example: dry run

```bash
python -m prompt_expander --template template.txt --data leads.csv --dry-run
```

## Tests

Tests use Python's built-in `unittest` — nothing to install:

```bash
python -m unittest discover -s tests -v
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About

Asdale Dynamics, LLC is Dylan Asdale's Indiana LLC: beginner-friendly AI education, books (including *The Massive AI Manual*), guides, and practical tools you can run locally. Learn more at dylanasdale.github.io. Local-first, plain English, never condescending.
