#!/usr/bin/env python3
"""Flag high-risk claims in paper/main.tex (superlatives, scope, abstract/eval gaps)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TEX_DEFAULT = ROOT / "paper/main.tex"

SUPER = re.compile(r"\b(first|only|novel|unique)\b", re.I)
SUPER_OK = re.compile(
    r"first-pass|first-class|first-shot|first attempt|first non-library|"
    r"First[,;.]|only\s+(the|a|an|when|if|at|in|on|after|before|under)|"
    r"configuration\s+only|register-only|configuration-only|-only\b",
    re.I,
)
NOT_ONLY = re.compile(r"\bnot\b(?:\s+\w+){0,4}\s+only\b", re.I)
QUAL = re.compile(r"to our knowledge|in our evaluation|we are not aware", re.I)
AUTO = re.compile(r"without human|fully autonomous|template-free", re.I)
DEFINED = re.compile(r"\\define|definition|we define|we call|template-free vs", re.I)
CONTRIB = re.compile(r"\\item\s+\\textbf\{")
EVIDENCE = re.compile(r"\\ref\{sec:(?:eval|dsl|compiler|tuning)", re.I)


def slice_block(tex: str, start: str, end: str) -> tuple[str, int]:
    m = re.search(rf"{start}(.*?){end}", tex, re.S)
    if not m:
        return "", 0
    return m.group(1), tex[: m.start()].count("\n") + 1


def report(line: int, sev: str, text: str, fix: str, errors: list[str], *, show_warn: bool = True) -> None:
    if sev == "WARN" and not show_warn:
        return
    snippet = text.strip().replace("\n", " ")[:100]
    print(f"{sev:5} L{line}: {snippet}")
    print(f"      fix: {fix}")
    if sev == "ERROR":
        errors.append(snippet)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", type=Path, default=TEX_DEFAULT)
    ap.add_argument("--severity", choices=["error", "warn", "all"], default="all")
    args = ap.parse_args()
    tex = args.tex.read_text(encoding="utf-8")
    errors: list[str] = []
    abstract, abs_line = slice_block(tex, r"\\begin\{abstract\}", r"\\end\{abstract\}")
    abs_end = abs_line + abstract.count("\n")
    eval_body, _ = slice_block(tex, r"\\section\{Evaluation\}", r"\\section\{Related Work\}")

    print("=== Claim Audit ===")
    show_warn = args.severity != "error"
    in_keywords = False
    for i, line in enumerate(tex.splitlines(), 1):
        if "\\keywords{" in line:
            in_keywords = True
        if in_keywords:
            if "}" in line:
                in_keywords = False
            continue
        if line.strip().startswith("%"):
            continue

        if (
            SUPER.search(line)
            and not SUPER_OK.search(line)
            and not NOT_ONLY.search(line)
            and not QUAL.search(line)
        ):
            report(i, "WARN", line, 'Add "to our knowledge" or "in our evaluation"', errors, show_warn=show_warn)

        if AUTO.search(line):
            if re.search(r"\\keywords\{|We define|we define", line, re.I):
                continue
            prior_text = "\n".join(tex.splitlines()[: i - 1])
            if not DEFINED.search(prior_text):
                sev = "WARN" if abs_line <= i <= abs_end else "ERROR"
                report(i, sev, line, "Define term before use (§1 or §2)", errors, show_warn=show_warn)

    abs_nums = set(re.findall(r"\d+(?:\.\d+)?", abstract))
    eval_nums = set(re.findall(r"\d+(?:\.\d+)?", eval_body))
    for num in sorted(abs_nums, key=float):
        if float(num) < 2:
            continue
        if num not in eval_nums and num not in {"2026", "12", "10"}:
            report(abs_line, "WARN", f"abstract number {num}",
                   f"Ensure {num} appears in §4 Evaluation", errors, show_warn=show_warn)

    contrib = re.search(r"This paper makes four contributions:(.*?)\\end\{enumerate\}", tex, re.S)
    if contrib:
        for m in CONTRIB.finditer(contrib.group(1)):
            block = contrib.group(1)[m.start(): m.start() + 400]
            if not EVIDENCE.search(block):
                line = tex[: contrib.start() + m.start()].count("\n") + 1
                report(line, "ERROR", block[:120],
                       "Contribution bullet should cite §3/§4 evidence (\\ref{sec:...})", errors, show_warn=show_warn)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
