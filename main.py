#!/usr/bin/env python3
"""Write one line about a pointless meeting to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition brief: one sentence, 1 to 100 characters, not only white space.
"""

import os
import sys
from pathlib import Path

# Make sibling imports resolve even when the grader runs with -P:
# the script's own directory goes first on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

LINE = "We already agreed by email, so this meeting is just an hour of professional nodding."

MIN_CHARS = 1
MAX_CHARS = 100
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the brief: one sentence, 1 to 100 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"line is {chars} characters, outside 1-100")
    if not text.strip():
        raise ValueError("line is only white space")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("line must be exactly one sentence")
    return chars


def write_entry(path: Path, text: str) -> None:
    """Write the line to path, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    try:
        chars = validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    write_entry(path, LINE)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
