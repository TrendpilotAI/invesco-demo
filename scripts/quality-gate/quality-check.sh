#!/bin/bash
# quality-check.sh — Minimal viable quality gate.
# Usage: quality-check.sh [repo-path]
# Exit 0 = ship it. Exit 1 = fix it.

set -e

REPO="${1:-.}"
cd "$REPO" || exit 1

echo "═══════════════════════════════════════"
echo " QUALITY CHECK: $(basename "$(pwd)")"
echo "═══════════════════════════════════════"

PASS=0
FAIL=0
SECRETS_PASS=0
LINT_PASS=0
TESTS_PASS=0

# ── Stage 1: Secrets (grep-based, fast) ────────────────────────

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  FILES=$(git diff --cached --name-only 2>/dev/null | grep -v '\.test\.\|\.spec\.\|\.md$' | head -50)
else
  FILES=$(find . -type f -name "*.py" -o -name "*.ts" -o -name "*.js" 2>/dev/null | grep -v node_modules | head -50)
fi

if echo "$FILES" | xargs grep -lE "sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}" 2>/dev/null | grep -v ".example" | grep -v "test" >/dev/null; then
  echo "❌ FAIL: Possible secrets in staged files"
  FAIL=$((FAIL+1))
  SECRETS_PASS=0
else
  echo "✅ secrets: clean"
  PASS=$((PASS+1))
  SECRETS_PASS=1
fi

# ── Stage 2: Lint (fastest first) ────────────────────────────

# Python: ruff
if command -v ruff >/dev/null 2>&1 && (find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" -quit 2>/dev/null); then
  if ruff check . --quiet 2>/dev/null; then
    echo "✅ ruff: clean"
    PASS=$((PASS+1))
    LINT_PASS=1
  else
    echo "❌ FAIL: ruff found issues"
    FAIL=$((FAIL+1))
    LINT_PASS=0
  fi
fi

# TypeScript: eslint
if [ -f "node_modules/.bin/eslint" ]; then
  if npx eslint . --quiet --max-warnings 0 2>/dev/null; then
    echo "✅ eslint: clean"
    PASS=$((PASS+1))
    LINT_PASS=1
  else
    echo "❌ FAIL: eslint found issues"
    FAIL=$((FAIL+1))
    LINT_PASS=0
  fi
fi

# TypeScript: tsc
if [ -f "tsconfig.json" ] && [ -f "node_modules/.bin/tsc" ]; then
  if npx tsc --noEmit 2>/dev/null; then
    echo "✅ tsc: no type errors"
    PASS=$((PASS+1))
    LINT_PASS=1
  else
    echo "❌ FAIL: tsc found type errors"
    FAIL=$((FAIL+1))
    LINT_PASS=0
  fi
fi

# ── Stage 3: Tests (expensive, run last) ────────────────────────

# Python: pytest
if (find . -name "test_*.py" -not -path "./.venv/*" -not -path "./venv/*" -quit 2>/dev/null); then
  if command -v pytest >/dev/null 2>&1; then
    if pytest -x --tb=short -q 2>/dev/null; then
      echo "✅ pytest: all passing"
      PASS=$((PASS+1))
      TESTS_PASS=1
    else
      echo "❌ FAIL: pytest failed"
      FAIL=$((FAIL+1))
      TESTS_PASS=0
    fi
  fi
fi

# TypeScript: vitest / npm test
if [ -f "node_modules/.bin/vitest" ]; then
  if npx vitest run --reporter=dot 2>/dev/null; then
    echo "✅ vitest: all passing"
    PASS=$((PASS+1))
    TESTS_PASS=1
  else
    echo "❌ FAIL: vitest failed"
    FAIL=$((FAIL+1))
    TESTS_PASS=0
  fi
elif [ -f "package.json" ] && grep -q '"test"' package.json 2>/dev/null; then
  if npm test -- --silent 2>/dev/null; then
    echo "✅ npm test: all passing"
    PASS=$((PASS+1))
    TESTS_PASS=1
  else
    echo "❌ FAIL: npm test failed"
    FAIL=$((FAIL+1))
    TESTS_PASS=0
  fi
fi

# ── Metrics JSON ───────────────────────────────────────────

METRICS=$(cat << EOF
{
  "repo": "$(basename "$(pwd)")",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "result": "$([ $FAIL -gt 0 ] && echo "fail" || echo "pass")",
  "pass": $PASS,
  "fail": $FAIL,
  "checks": {
    "secrets": $([ "$SECRETS_PASS" = "1" ] && echo "pass" || echo "fail"),
    "lint": $([ "$LINT_PASS" = "1" ] && echo "pass" || echo "fail"),
    "tests": $([ "$TESTS_PASS" = "1" ] && echo "pass" || echo "fail")
  }
}
EOF
)

echo "$METRICS" > /tmp/quality-metrics.json
echo "$METRICS"

# ── Result ────────────────────────────────────────────────────

echo "───────────────────────────────────────"

if [ $FAIL -gt 0 ]; then
  echo " RESULT: ❌ FAIL ($FAIL failed, $PASS passed)"
  echo "═══════════════════════════════════════"
  exit 1
else
  echo " RESULT: ✅ PASS ($PASS passed)"
  echo "═══════════════════════════════════════"
  exit 0
fi
