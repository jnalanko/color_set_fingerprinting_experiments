#!/usr/bin/env python3
"""
Parse concatenated 'stats for <record>' blocks into a TSV.

Usage:
  python parse_stats.py input.txt output.tsv

Notes:
- Creates one row per record (e.g., salmonella_2).
- Creates one column per stat key (e.g., "Number of k-mers").
- Converts integers/floats, and percent values like "3.37%" -> 3.37 (numeric).
"""

import re
import sys
import csv
from pathlib import Path


BLOCK_RE = re.compile(r"^\s*stats\s+for\s+(?P<name>\S+)\s*$", re.IGNORECASE)
KV_RE = re.compile(r"^\s*(?P<key>[^:]+?)\s*:\s*(?P<val>.+?)\s*$")


def coerce_value(raw: str):
    s = raw.strip()
    # Percent -> float without "%"
    if s.endswith("%"):
        num = s[:-1].strip()
        try:
            return float(num)
        except ValueError:
            return raw

    # Int or float
    try:
        if re.fullmatch(r"-?\d+", s):
            return int(s)
        if re.fullmatch(r"-?\d*\.\d+|-?\d+\.\d*", s):
            return float(s)
        # Also allow scientific notation
        if re.fullmatch(r"-?\d+(?:\.\d+)?[eE][+-]?\d+", s):
            return float(s)
    except ValueError:
        pass

    return raw


def parse_blocks(text: str):
    """
    Returns:
      rows: list[dict] where each dict has 'record' + stat keys
      key_order: list[str] keys in first-seen order (for stable TSV column order)
    """
    rows = []
    key_order = []

    current = None  # dict for current record

    for line in text.splitlines():
        m = BLOCK_RE.match(line)
        if m:
            # start new block
            if current is not None:
                rows.append(current)
            current = {"record": m.group("name")}
            continue

        if current is None:
            # ignore lines before first "stats for ..."
            continue

        kv = KV_RE.match(line)
        if not kv:
            continue

        key = kv.group("key").strip()
        val = coerce_value(kv.group("val"))

        if key not in key_order:
            key_order.append(key)
        current[key] = val

    if current is not None:
        rows.append(current)

    return rows, key_order


def write_csv(rows, key_order, out_path: Path):
    cols = ["record"] + key_order

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=",", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            # Ensure all columns exist; DictWriter will fill missing with ""
            w.writerow(r)


def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_stats.py input.txt output.csv", file=sys.stderr)
        sys.exit(2)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    text = in_path.read_text(encoding="utf-8", errors="replace")
    rows, key_order = parse_blocks(text)

    if not rows:
        print("No records found. Expected lines like: 'stats for salmonella_2'", file=sys.stderr)
        sys.exit(1)

    write_csv(rows, key_order, out_path)
    print(f"Wrote {len(rows)} records to {out_path}")


if __name__ == "__main__":
    main()

