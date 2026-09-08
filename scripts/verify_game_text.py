#!/usr/bin/env python3
"""Compare reviewed plaintext blocks with decoded text exported from a game.

This checks exact text equality only. It does not assess prose, node bindings,
branch logic, placeholder values, or rendering. No third-party dependencies.
"""

import argparse
import json
import re
import sys
from pathlib import Path


class VerificationError(ValueError):
    pass


def parse_source(path):
    lines = Path(path).read_text(encoding="utf-8-sig").split("\n")
    entries = {}
    current = None
    body = None
    completed = False
    for number, line in enumerate(lines, 1):
        if body is not None:
            if line == "~~~~":
                entries[current] = "\n".join(body)
                body = None
                completed = True
            else:
                body.append(line)
            continue
        if line.startswith("## "):
            if current is not None and not completed:
                raise VerificationError(f"Missing text block for {current}")
            identifier = line[3:].strip()
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", identifier):
                raise VerificationError(f"Invalid ID at line {number}: {identifier}")
            if identifier in entries:
                raise VerificationError(f"Duplicate source ID: {identifier}")
            current, completed = identifier, False
        elif line == "~~~~text":
            if current is None or completed:
                raise VerificationError(f"Unexpected text block at line {number}")
            body = []
        elif line == "~~~~":
            raise VerificationError(f"Unexpected text boundary at line {number}")
    if body is not None:
        raise VerificationError(f"Unclosed text block for {current}")
    if current is not None and not completed:
        raise VerificationError(f"Missing text block for {current}")
    if not entries:
        raise VerificationError("No source entries found")
    return entries


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"Duplicate exported ID: {key}")
        result[key] = value
    return result


def load_actual(path):
    result = json.loads(
        Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object
    )
    if not isinstance(result, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in result.items()
    ):
        raise VerificationError("Export must be an object mapping IDs to decoded strings")
    return result


def compare(expected, actual):
    issues = []
    for key in sorted(expected.keys() - actual.keys()):
        issues.append(f"Missing: {key}")
    for key in sorted(actual.keys() - expected.keys()):
        issues.append(f"Unexpected: {key}")
    for key in sorted(expected.keys() & actual.keys()):
        if expected[key] != actual[key]:
            issues.append(f"Text differs: {key}")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Reviewed Markdown text blocks")
    parser.add_argument("--actual", required=True, help="Decoded ID-to-text JSON export")
    args = parser.parse_args()
    try:
        expected = parse_source(args.source)
        issues = compare(expected, load_actual(args.actual))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    if issues:
        print("FAIL\n" + "\n".join(issues), file=sys.stderr)
        return 1
    print(f"PASS: {len(expected)} entries match exactly. Bindings and rendering require separate checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
