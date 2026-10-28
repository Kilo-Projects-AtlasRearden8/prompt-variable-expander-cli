"""Command line interface for prompt variable expansion."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Dict

from .renderer import render, unresolved
from .sources import load_data

Result = Tuple[str, str, List[str]]


def _output_name(row: Dict[str, str], index: int, ext: str) -> str:
    """Pick a safe output filename for a data row."""
    for key in ("name", "title", "file", "filename"):
        value = (row.get(key) or "").strip()
        if value:
            safe = "".join(
                ch if ch.isalnum() or ch in "-_." else "_" for ch in value
            ).strip("_") or f"prompt_{index + 1:03d}"
            # Defang any path separators so output stays inside --out.
            safe = safe.replace("/", "_").replace("\\", "_")
            return safe + ext
    return f"prompt_{index + 1:03d}{ext}"


def expand(template_path, data_path, out_dir="output", dry_run=False, ext=".txt") -> List[Result]:
    """Render one prompt per data row.

    Returns a list of (filename, rendered_text, missing_variables) tuples.
    When dry_run is True, no files are written.
    """
    template = Path(template_path).read_text(encoding="utf-8")
    rows = load_data(data_path)

    results: List[Result] = []
    for index, row in enumerate(rows):
        rendered = render(template, row)
        missing = unresolved(template, row)
        filename = _output_name(row, index, ext)
        results.append((filename, rendered, missing))
        if not dry_run:
            target = Path(out_dir) / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")

    return results


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="prompt-expander",
        description="Expand {{variables}} in prompt templates from a CSV or JSON data file.",
    )
    parser.add_argument("--template", required=True, help="Path to the prompt template file.")
    parser.add_argument("--data", required=True, help="Path to .csv or .json data file.")
    parser.add_argument("--out", default="output", help="Output directory (default: output).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be produced without writing files.",
    )
    parser.add_argument(
        "--ext", default=".txt", help="Output file extension (default: .txt)."
    )
    args = parser.parse_args(argv)

    results = expand(
        template_path=args.template,
        data_path=args.data,
        out_dir=args.out,
        dry_run=args.dry_run,
        ext=args.ext,
    )

    mode = "DRY-RUN: would write" if args.dry_run else "Wrote"
    for filename, _rendered, missing in results:
        note = ""
        if missing:
            note = f"  (unresolved variables: {', '.join(missing)})"
        print(f"{mode} {args.out}/{filename}{note}")
    print(f"{len(results)} prompt(s) {'would be ' if args.dry_run else ''}produced.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
