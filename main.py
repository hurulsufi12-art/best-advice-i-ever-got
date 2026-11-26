#!/usr/bin/env python3
"""The Best Advice I Ever Got.

Writes a single sentence about the best advice the writer ever
received to /output/entry.txt. Stdlib only, deterministic, no
network, no model.
"""
import os
import sys

MAX_CHARS = 200

# The sentence as data: one word per item, joined with single spaces.
# Keeping it a tuple makes the word count visible at a glance.
WORDS = (
    "My", "grandfather", "said:", "never", "borrow", "money", "to",
    "impress", "people", "who", "would", "not", "lend", "you", "theirs.",
)


def build_sentence(words):
    """Join the word tuple into the single entry sentence."""
    return " ".join(words)


def verify_advice(text):
    """Return (ok, errors): ok is True only when every gate passes."""
    errors = []
    if not isinstance(text, str):
        return False, ["entry must be text"]
    if not text.strip():
        errors.append("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        errors.append("entry must be a single line")
    if len(text) > MAX_CHARS:
        errors.append("entry is %d chars, over the %d limit"
                      % (len(text), MAX_CHARS))
    # One sentence: exactly one terminal period, at the end, and no
    # other sentence-ending punctuation anywhere in the line.
    if text.count(".") != 1 or not text.endswith("."):
        errors.append("entry must be exactly one sentence")
    if "!" in text or "?" in text:
        errors.append("entry must be exactly one sentence")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        errors.append("entry is not valid UTF-8 text")
    return (not errors), errors


def main():
    from pathlib import Path
    text = build_sentence(WORDS)
    ok, errors = verify_advice(text)
    if not ok:
        for error in errors:
            print("gate failed: %s" % error, file=sys.stderr)
        return 1
    out_path = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
