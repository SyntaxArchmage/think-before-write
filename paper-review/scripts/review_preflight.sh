#!/usr/bin/env bash
# Pre-review gate: compile, page count, numbers, claims, anonymization.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"

TEX="paper/main.tex"
fail=0
pass() { echo "PASS: $1"; }
fail_check() { echo "FAIL: $1"; fail=1; }

echo "=== Review Preflight ==="

if (cd paper && tectonic main.tex >/dev/null 2>&1); then
  pass "compile (tectonic)"
else
  fail_check "compile (tectonic)"
fi

if [[ -f paper/main.pdf ]] && command -v pdfinfo >/dev/null 2>&1; then
  pages="$(pdfinfo paper/main.pdf 2>/dev/null | awk '/Pages:/ {print $2}')"
  if [[ -n "${pages:-}" ]] && (( pages <= 12 )); then
    pass "page count ($pages pages, limit 12 excl. refs — verify manually)"
  else
    fail_check "page count (${pages:-unknown}; target ≤12 excl. refs)"
  fi
else
  echo "SKIP: page count (pdfinfo or main.pdf unavailable)"
fi

NUM_SCRIPT=".cursor/skills/academic-writing/scripts/check-numbers.py"
if [[ -x "$NUM_SCRIPT" ]] || [[ -f "$NUM_SCRIPT" ]]; then
  if python3 "$NUM_SCRIPT" --tex "$TEX"; then
    pass "numbers manifest"
  else
    fail_check "numbers manifest"
  fi
else
  fail_check "numbers manifest (check-numbers.py missing)"
fi

CLAIM_SCRIPT=".cursor/skills/academic-writing/scripts/claim_audit.py"
if [[ -f "$CLAIM_SCRIPT" ]]; then
  if python3 "$CLAIM_SCRIPT" --tex "$TEX" --severity error; then
    pass "claim audit"
  else
    fail_check "claim audit"
  fi
else
  fail_check "claim audit (claim_audit.py missing)"
fi

anon_patterns='github\.com|gitlab\.com|Acknowledgment|Acknowledgement|@[a-z]+\.(edu|com)'
leaks="$(grep -Ein "$anon_patterns" "$TEX" 2>/dev/null || true)"
if [[ -n "$leaks" ]]; then
  echo "$leaks"
  fail_check "anonymization (possible author/repo/ack leak above)"
else
  pass "anonymization"
fi

if (( fail )); then echo "=== Preflight FAILED ==="; else echo "=== Preflight PASSED ==="; fi
exit "$fail"
