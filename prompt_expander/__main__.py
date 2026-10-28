"""Module entry point: python -m prompt_expander --template ... --data ..."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
