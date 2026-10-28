# prompt-expander

A friendly, local-first Python CLI that fills in `{{variables}}` in prompt templates using information from a CSV or JSON file, and saves one ready-to-use prompt per row.

Built and maintained by **Asdale Dynamics, LLC** (Indiana) — beginner-friendly AI education, books, guides, and practical open-source tools you can run on your own computer.

## What it does

Imagine you have a prompt template like this:

```
Hi {{name}},

Thanks for your interest in {{product}}. We'll be in touch by {{deadline}}.
```

And a data file with one person per row:

```csv
name,product,deadline
Dylan,The Massive AI Manual,Friday
Sam,The Massive AI Manual,Monday
```

`prompt-expander` combines them and writes one file per person:

- `Dylan.txt` — `Hi Dylan, Thanks for your interest in The Massive AI Manual. We'll be in touch by Friday.`
- `Sam.txt` — `Hi Sam, Thanks for your interest in The Massive AI Manual. We'll be in touch by Monday.`

No data leaves your computer. No API keys. No accounts. Just plain files you made, staying local.

## Try it right away

There are example files in the `examples/` folder so you can run the tool immediately without creating anything:

```bash
# See what would be produced (nothing is written to disk)
python3 -m prompt_expander --template examples/template.txt --data examples/data.csv --dry-run

# Actually write the prompt files into the output/ folder
python3 -m prompt_expander --template examples/template.txt --data examples/data.csv --out output

# Or use the JSON data file instead
python3 -m prompt_expander --template examples/template.txt --data examples/data.json --out output
```

## Install

Run straight from this folder (nothing to install):

```bash
python3 -m prompt_expander --template template.txt --data data.csv --out output
```

Or install it so the `prompt-expander` command is available everywhere:

```bash
pip install .
prompt-expander --template template.txt --data data.csv --out output
```

## Usage

```
prompt-expander --template TEMPLATE --data DATA [--out DIR] [--dry-run] [--ext .txt]
```

| Option | What it does |
|--------|--------------|
| `--template` | Your prompt template file containing `{{variables}}` (required) |
| `--data` | A `.csv` or `.json` file, one record per prompt (required) |
| `--out` | Folder to write the finished prompts into (default: `output`) |
| `--dry-run` | Preview what would be written without saving any files |
| `--ext` | File extension for the output prompts (default: `.txt`) |

### Naming output files

If your data has a `name`, `title`, `file`, or `filename` column, that value is used for the output filename (spaces and odd characters become underscores). Otherwise files are named `prompt_001.txt`, `prompt_002.txt`, and so on.

### Missing variables

If a template references `{{something}}` but your data doesn't include it, the `{{something}}` is left as-is in the output. Nothing is silently deleted or overwritten.

## Features

- `{{variable}}` expansion, with flexible spacing (`{{  name  }}` works the same as `{{name}}`)
- CSV input (the first row names the variables)
- JSON input (a single object, or a list of objects)
- `--dry-run` to preview before writing
- Standard library only — nothing to install beyond Python itself
- No network, no API keys, no secrets, no personal data collected
- MIT licensed

## Tests

Tests use Python's built-in `unittest`, so nothing extra is needed:

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC is Dylan Asdale's Indiana LLC. Dylan is a registered nurse turned AI author and founder. His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending.

The LLC focuses on beginner-friendly AI education, practical open-source tools, small-business and author resources, accessible life-admin helpers, healthcare-worker AI aids (education only, never medical advice), and fun extras like gaming and chess tools.

Local-first, plain English, never condescending.
