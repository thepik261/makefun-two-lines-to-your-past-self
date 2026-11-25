#!/usr/bin/env python3
"""Two Lines to Your Past Self.

Writes one two-line warning to /output/entry.txt:
line 1 warns the past self about one specific moment (one sentence);
line 2 says in one sentence why that moment mattered and what changed.
Pure Python standard library, deterministic, no network, no input files.
"""

import os
import sys

ENTRY = (
    "When Dad calls from City General on the morning of 9 June and says "
    "'come now, son', don't tell him you'll finish the report first \u2014 "
    "leave your desk that minute.\n"
    "Those three hours beside his bed were the last words you ever heard "
    "from him, and the only ones you never regretted.\n"
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(text: str) -> None:
    """Gate: UTF-8 text of 1 to 280 characters, exactly two lines,
    each line a single sentence."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > 280:
        raise ValueError("entry is %d characters, over the 280 limit" % len(text))
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines, got %d" % len(lines))
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            raise ValueError("line %d is empty" % i)
        if not stripped.endswith((".", "!", "?")):
            raise ValueError("line %d does not end with sentence punctuation" % i)
        # Exactly one sentence: no other sentence-ending punctuation inside.
        body = stripped[:-1]
        for mark in (".", "!", "?"):
            if mark in body:
                raise ValueError("line %d contains more than one sentence" % i)


def main() -> int:
    validate(ENTRY)
    encoded = ENTRY.encode("utf-8")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Write to a temp file in the same directory, then move it into place
    # so a partial write never leaves a broken entry.txt behind.
    tmp_path = os.path.join(OUTPUT_DIR, ".entry.txt.tmp")
    try:
        with open(tmp_path, "wb") as fh:
            fh.write(encoded)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, OUTPUT_PATH)
    finally:
        # Never leave a stray temp file behind if the move failed.
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
    try:
        os.chmod(OUTPUT_PATH, 0o644)
    except OSError:
        pass
    print("wrote %s (%d characters, %d bytes)" % (OUTPUT_PATH, len(ENTRY), len(encoded)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
