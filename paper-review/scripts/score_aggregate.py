#!/usr/bin/env python3
"""Aggregate Tier A reviewer scores with persona sigma offsets."""
from __future__ import annotations

import argparse
import json
import sys

WEIGHTS = ["contribution", "technical", "evaluation", "clarity", "reproducibility"]
MAX_TOTAL = 46
OFFSETS = {"R1": -1.84, "R2": 0.0, "R3": +0.92}


def band(score: float) -> str:
    if score >= 38:
        return "Accept"
    if score >= 32:
        return "Borderline"
    if score >= 26:
        return "Weak Reject"
    return "Reject"


def load_scores(path: str | None) -> dict:
    if path in (None, "-"):
        raw = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("ERROR: invalid JSON input", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict):
        print(f"ERROR: expected JSON object, got {type(data).__name__}", file=sys.stderr)
        sys.exit(2)
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", help="JSON file (default: stdin)")
    args = ap.parse_args()
    data = load_scores(args.input)
    if not data:
        print("ERROR: empty input", file=sys.stderr)
        return 2

    rows = []
    adjusted = []
    print("=== Tier A Score Aggregate ===\n")
    print(f"{'Reviewer':<8} {'Raw':>5} {'Adj':>6}  Dimensions")
    print("-" * 60)
    for persona in sorted(data):
        dims = data[persona]
        missing = [k for k in WEIGHTS if k not in dims]
        if missing:
            print(f"WARN: {persona} missing dimensions: {', '.join(missing)}", file=sys.stderr)
        raw = sum(int(dims.get(k, 0)) for k in WEIGHTS)
        off = OFFSETS.get(persona, 0.0)
        adj = max(0, min(MAX_TOTAL, round(raw + off, 1)))
        rows.append((persona, raw, adj, dims))
        adjusted.append(adj)
        dim_str = " ".join(f"{k[:3]}={dims.get(k, 0)}" for k in WEIGHTS)
        print(f"{persona:<8} {raw:>5} {adj:>6.1f}  {dim_str} (σ{off:+.2f})")

    adjusted.sort()
    median = adjusted[len(adjusted) // 2]
    print("-" * 60)
    print(f"Median adjusted total: {median:.1f} / {MAX_TOTAL}")
    print(f"Recommendation band:   {band(median)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
