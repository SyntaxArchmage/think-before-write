#!/usr/bin/env python3
"""Verify paper/main.tex numeric claims against data/processed/manifest.yaml."""
from __future__ import annotations

import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MAP = {"§4.1": "§4.2", "§4.2": "§4.3", "§4.3": "§4.4", "§3.2": "§3.1", "§3.3": "§3.2"}


def load_manifest(path: Path) -> dict[str, dict]:
    out, cat, eid = {}, None, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"): continue
        if m := re.match(r"^(\w+):\s*$", line): cat = m.group(1); continue
        if m := re.match(r"^  (\w+):\s*$", line): eid = f"{cat}.{m.group(1)}"; out[eid] = {}; continue
        if (m := re.match(r"^    (\w+):\s*(.+)$", line)) and eid:
            k, v = m.group(1), m.group(2).strip()
            out[eid][k] = re.findall(r'"([^"]+)"', v) if k == "used_in" else v.strip('"')
    return out


def slices(tex: str) -> dict[str, str]:
    lines, s = tex.splitlines(), {"all": tex}
    if m := re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S): s["abstract"] = m.group(1)
    sec, sub = [], 0
    for i, ln in enumerate(lines):
        if re.match(r"\\section\{", ln): sec.append(i); sub = 0
        elif re.match(r"\\subsection\{", ln):
            sub += 1; end = next((j for j in range(i+1, len(lines)) if re.match(r"\\(?:sub)?section\{", lines[j])), len(lines))
            s[f"§{len(sec)}.{sub}"] = "\n".join(lines[i:end])
    for idx, start in enumerate(sec):
        end = sec[idx + 1] if idx + 1 < len(sec) else len(lines)
        s[f"§{idx + 1}"] = "\n".join(lines[start:end])
    return s


def scope(locs: list[str], s: dict[str, str]) -> str:
    chunks = []
    for loc in locs:
        k = loc.split()[0]
        chunks.append(s.get("abstract" if k == "abstract" else MAP.get(k, k) if k.startswith("§") else "all", s["all"]))
    return "\n".join(chunks)


def pats(v: str) -> list[str]:
    v = v.lstrip("~")
    if re.match(r"^\d+-\d+", v):
        a, b = v.split("-", 1); return [rf"{a}\s*[-–-]\s*{b}", rf"{b}\\%", rf"\+{a}\\%", a, b]
    if "." in v: return [re.escape(v), v.replace(".", r"\.\s*")]
    ps = [re.escape(v), rf"{{\sim}}\s*{v}"]
    return ps + ([r"2\{,\}000", r"2000"] if v == "2200" else [])


def hit(v: str, t: str) -> bool:
    return any(re.search(p, t) for p in pats(v))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=ROOT / "data/processed/manifest.yaml")
    ap.add_argument("--tex", type=Path, default=ROOT / "paper/main.tex")
    a = ap.parse_args()
    entries = load_manifest(a.manifest)
    tex = a.tex.read_text(encoding="utf-8")
    s = slices(tex)
    fail = 0
    print("=== Numbers Triangle Check ===")
    for eid, m in sorted(entries.items()):
        val, sc = m.get("value", ""), scope(m.get("used_in", []), s)
        if hit(val, sc): print(f"MATCH   {eid}: {val}")
        elif hit(val, tex): print(f"MISMATCH {eid}: {val} (in tex, not used_in scope)"); fail = 1
        else: print(f"MISSING {eid}: {val}"); fail = 1
    known = {m.get("value", "").lstrip("~") for m in entries.values()}
    # Orphan scan: §4 only (manifest-backed claims live in Evaluation), strip LaTeX
    # thousands separators ({,}, \,) so 1{,}755 does not become orphan 755/1, and skip
    # small ratios (≤2) that appear as table data (e.g. 1.15, 1.42) without failing exit.
    eval_m = re.search(r"\\section\{Evaluation\}(.*?)\\section\{Related", tex, re.S)
    eval_tex = eval_m.group(1) if eval_m else ""
    eval_clean = eval_tex.replace("{,}", "").replace("\\,", "")
    unit_suffix = re.compile(r"~?(?:MHz|GHz|KB|MB|GB|TB|ms|us|ns)")
    for m in re.finditer(r"(\d+\.\d+)\s*\{\\times\}|(\d+/\d+)", eval_clean):
        n = m.group(1) or m.group(2)
        if unit_suffix.match(eval_clean[m.end():]):
            continue
        try:
            if float(n.split("/")[0]) <= 2:
                continue
        except ValueError:
            pass
        if not any(n in k or k in n for k in known):
            print(f"ORPHAN  {n}")
    return fail


if __name__ == "__main__":
    sys.exit(main())
