#!/usr/bin/env bash
# =============================================================================
# ci-quality-check.sh — Shared quality gate for ForwardLane / SignalHaus repos
#
# Usage:
#   source ./scripts/quality-gate/ci-quality-check.sh   # in-shell with env vars
#   bash   ./scripts/quality-gate/ci-quality-check.sh   # standalone
#
# Environment controls (all optional, defaults shown):
#   QG_LANG          = auto-detect | python | node
#   QG_FAIL_FAST     = 0 | 1      (exit on first failure)
#   QG_COVERAGE_MIN  = 50         (Python pytest cov threshold %)
#   QG_BANDIT_LEVEL  = high       (medium | high)
#   QG_AUDIT_LEVEL   = high       (moderate | high | critical)
#   QG_SKIP_LINT     = 0 | 1
#   QG_SKIP_TEST     = 0 | 1
#   QG_SKIP_SECURITY = 0 | 1
# =============================================================================

set -euo pipefail

# ── Colour helpers ─────────────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

pass()  { echo -e "${GREEN}✔  $*${RESET}"; }
fail()  { echo -e "${RED}✘  $*${RESET}"; }
info()  { echo -e "${CYAN}ℹ  $*${RESET}"; }
warn()  { echo -e "${YELLOW}⚠  $*${RESET}"; }
banner(){ echo -e "\n${BOLD}${CYAN}══ $* ══${RESET}"; }

# ── Defaults ──────────────────────────────────────────────────────────────
QG_LANG="${QG_LANG:-auto}"
QG_FAIL_FAST="${QG_FAIL_FAST:-0}"
QG_COVERAGE_MIN="${QG_COVERAGE_MIN:-50}"
QG_BANDIT_LEVEL="${QG_BANDIT_LEVEL:-high}"
QG_AUDIT_LEVEL="${QG_AUDIT_LEVEL:-high}"
QG_SKIP_LINT="${QG_SKIP_LINT:-0}"
QG_SKIP_TEST="${QG_SKIP_TEST:-0}"
QG_SKIP_SECURITY="${QG_SKIP_SECURITY:-0}"

FAILURES=()
WARNINGS=()

# ── Language detection ─────────────────────────────────────────────────────
detect_lang() {
  if [[ "$QG_LANG" != "auto" ]]; then
    echo "$QG_LANG"
    return
  fi
  if [[ -f "Pipfile" ]] || [[ -f "pyproject.toml" ]] || [[ -f "requirements.txt" ]]; then
    echo "python"
  elif [[ -f "package.json" ]]; then
    echo "node"
  else
    echo "unknown"
  fi
}

# ── Helper: command exists ─────────────────────────────────────────────────
has_cmd() { command -v "$1" &>/dev/null; }

# ── Record failure / warning ───────────────────────────────────────────────
record_failure() {
  FAILURES+=("$1")
  fail "$1"
  if [[ "$QG_FAIL_FAST" == "1" ]]; then
    echo -e "\n${RED}FAIL_FAST enabled — aborting.${RESET}"
    exit 1
  fi
}

record_warning() {
  WARNINGS+=("$1")
  warn "$1"
}

# =============================================================================
# PYTHON GATES
# =============================================================================
run_python_lint() {
  banner "Python Lint"

  if has_cmd ruff; then
    info "Running ruff..."
    if ruff check . --output-format=text; then
      pass "ruff: clean"
    else
      record_failure "ruff found lint errors"
    fi
  elif has_cmd flake8; then
    info "Running flake8..."
    if flake8 . --max-line-length=120 --exclude=.git,__pycache__,migrations,.tox; then
      pass "flake8: clean"
    else
      record_failure "flake8 found lint errors"
    fi
  else
    record_warning "No Python linter found (install ruff or flake8)"
  fi
}

run_python_test() {
  banner "Python Tests"

  local pytest_cmd="pytest --disable-warnings -v"

  # Add coverage if pytest-cov is available
  if python -c "import pytest_cov" 2>/dev/null; then
    pytest_cmd="$pytest_cmd --cov=. --cov-report=term-missing --cov-report=xml:coverage.xml --cov-fail-under=${QG_COVERAGE_MIN}"
  fi

  info "Running: $pytest_cmd"
  if eval "$pytest_cmd"; then
    pass "Tests passed"
  else
    record_failure "pytest tests failed"
  fi
}

run_python_security() {
  banner "Python Security"

  # bandit SAST
  if has_cmd bandit; then
    info "Running bandit (severity=${QG_BANDIT_LEVEL})..."
    if bandit -r . \
        --exclude ./.git,./.tox,./migrations,./node_modules \
        --severity-level "${QG_BANDIT_LEVEL}" \
        --confidence-level medium \
        -f json -o bandit-report.json; then
      pass "bandit: no ${QG_BANDIT_LEVEL}-severity issues"
    else
      record_failure "bandit found ${QG_BANDIT_LEVEL}-severity security issues"
    fi
  else
    record_warning "bandit not found — skipping SAST"
  fi

  # pip-audit dependency check
  local req_file=""
  if [[ -f "requirements.txt" ]]; then
    req_file="requirements.txt"
  elif has_cmd pipenv; then
    pipenv requirements > /tmp/qg-requirements.txt 2>/dev/null && req_file="/tmp/qg-requirements.txt"
  fi

  if has_cmd pip-audit && [[ -n "$req_file" ]]; then
    info "Running pip-audit..."
    if pip-audit -r "$req_file" --ignore-vuln GHSA-w596-4wvx-j9j6; then
      pass "pip-audit: no known vulnerabilities"
    else
      record_warning "pip-audit found vulnerabilities (non-blocking in shared gate)"
    fi
  elif has_cmd safety && [[ -n "$req_file" ]]; then
    info "Running safety check..."
    if safety check -r "$req_file" --ignore 70612; then
      pass "safety: no known vulnerabilities"
    else
      record_warning "safety found vulnerabilities (non-blocking in shared gate)"
    fi
  else
    record_warning "pip-audit/safety not found — skipping dependency audit"
  fi
}

# =============================================================================
# NODE / JS / TS GATES
# =============================================================================

# Detect package manager
detect_pkg_manager() {
  if [[ -f "pnpm-lock.yaml" ]] && has_cmd pnpm; then echo "pnpm"
  elif [[ -f "yarn.lock" ]] && has_cmd yarn;  then echo "yarn"
  elif [[ -f "bun.lock" ]] && has_cmd bun;    then echo "bun"
  else                                               echo "npm"
  fi
}

run_node_lint() {
  banner "Node Lint"
  local pm
  pm=$(detect_pkg_manager)

  # TypeScript
  if [[ -f "tsconfig.json" ]] && has_cmd npx; then
    info "TypeScript type-check..."
    if npx tsc --noEmit; then
      pass "tsc: no type errors"
    else
      record_failure "TypeScript type errors found"
    fi
  fi

  # ESLint
  local eslint_config
  eslint_config=$(ls .eslintrc* eslint.config.* 2>/dev/null | head -1 || true)
  if [[ -n "$eslint_config" ]]; then
    info "Running ESLint ($pm run lint)..."
    if $pm run lint; then
      pass "ESLint: clean"
    else
      record_failure "ESLint found errors"
    fi
  else
    record_warning "No ESLint config found — skipping"
  fi
}

run_node_test() {
  banner "Node Tests"
  local pm
  pm=$(detect_pkg_manager)

  local test_script="test:ci"
  # Fallback to 'test' if test:ci not defined
  if ! $pm run | grep -q "test:ci" 2>/dev/null; then
    test_script="test"
  fi

  info "Running: $pm run $test_script"
  if $pm run "$test_script" --passWithNoTests 2>/dev/null || $pm run "$test_script"; then
    pass "Tests passed"
  else
    record_failure "Node tests failed"
  fi
}

run_node_security() {
  banner "Node Security Audit"
  local pm
  pm=$(detect_pkg_manager)

  info "Running $pm audit (level=${QG_AUDIT_LEVEL})..."

  local audit_cmd
  case "$pm" in
    pnpm) audit_cmd="pnpm audit --audit-level=${QG_AUDIT_LEVEL}" ;;
    yarn) audit_cmd="yarn audit --level ${QG_AUDIT_LEVEL}" ;;
    bun)  audit_cmd="bun audit" ;;
    *)    audit_cmd="npm audit --audit-level=${QG_AUDIT_LEVEL}" ;;
  esac

  if $audit_cmd; then
    pass "No ${QG_AUDIT_LEVEL}-severity vulnerabilities"
  else
    record_failure "Security audit found ${QG_AUDIT_LEVEL}-severity vulnerabilities"
  fi

  # Save full report non-blocking
  $pm audit --json > audit-report.json 2>/dev/null || true
}

run_node_build() {
  banner "Node Build"
  local pm
  pm=$(detect_pkg_manager)

  if $pm run | grep -q "\"build\"" 2>/dev/null || [[ -f "next.config.*" ]] || [[ -f "vite.config.*" ]]; then
    info "Running: $pm run build"
    if $pm run build; then
      pass "Build succeeded"
    else
      record_failure "Build failed"
    fi
  else
    info "No build script detected — skipping"
  fi
}

# =============================================================================
# MAIN
# =============================================================================
main() {
  local lang
  lang=$(detect_lang)

  echo -e "\n${BOLD}🔍 Quality Gate — language: ${lang}${RESET}"
  echo -e "   Repo: $(pwd)"
  echo -e "   Date: $(date -u '+%Y-%m-%dT%H:%M:%SZ')\n"

  if [[ "$lang" == "unknown" ]]; then
    warn "Cannot detect project language. Set QG_LANG=python|node and retry."
    exit 1
  fi

  case "$lang" in
    python)
      [[ "$QG_SKIP_LINT"     != "1" ]] && run_python_lint
      [[ "$QG_SKIP_TEST"     != "1" ]] && run_python_test
      [[ "$QG_SKIP_SECURITY" != "1" ]] && run_python_security
      ;;
    node)
      [[ "$QG_SKIP_LINT"     != "1" ]] && run_node_lint
      [[ "$QG_SKIP_TEST"     != "1" ]] && run_node_test
      [[ "$QG_SKIP_SECURITY" != "1" ]] && run_node_security
      run_node_build
      ;;
  esac

  # ── Summary ──────────────────────────────────────────────────────────────
  echo ""
  banner "Quality Gate Summary"

  if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    warn "Warnings (${#WARNINGS[@]}):"
    for w in "${WARNINGS[@]}"; do echo "   ⚠  $w"; done
  fi

  if [[ ${#FAILURES[@]} -gt 0 ]]; then
    fail "FAILED (${#FAILURES[@]} checks):"
    for f in "${FAILURES[@]}"; do echo "   ✘  $f"; done
    echo -e "\n${RED}${BOLD}❌ Quality gate NOT met — fix the above before merging.${RESET}\n"
    exit 1
  else
    pass "All checks passed ✓"
    echo -e "\n${GREEN}${BOLD}✅ Quality gate met.${RESET}\n"
    exit 0
  fi
}

main "$@"
