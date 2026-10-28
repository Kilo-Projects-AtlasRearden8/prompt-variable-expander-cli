"""Data source loaders for CSV and JSON files."""

import csv
import json
from pathlib import Path
from typing import List, Dict


def load_csv(path: Path) -> List[Dict[str, str]]:
    """Load a CSV file as a list of row dicts (header row = variable names)."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def load_json(path: Path) -> List[Dict[str, str]]:
    """Load a JSON file as a list of row dicts.

    Accepts a single object (one row) or a list of objects.
    """
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        rows = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("JSON list items must be objects")
            rows.append(item)
        return rows
    raise ValueError("JSON data must be an object or a list of objects")


def load_data(path) -> List[Dict[str, str]]:
    """Load rows from a .csv or .json file based on file extension."""
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".csv":
        return load_csv(p)
    if suffix == ".json":
        return load_json(p)
    raise ValueError(f"Unsupported data file: {p} (expected .csv or .json)")
