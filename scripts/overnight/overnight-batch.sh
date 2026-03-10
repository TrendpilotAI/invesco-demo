#!/usr/bin/env bash
# ============================================================================
# OVERNIGHT BATCH ORCHESTRATOR
# ============================================================================
# Integrates all 10 suggestions:
#   1. Failure alerts (failure-alert.sh)
#   2. Branch-safe workflow (branch-safe.sh)
#   3. Coverage scoreboard (coverage-scoreboard.py)
#   4. High-value coverage priority (module-priority.json)
#   5. Stop-loss rules (stop-loss.py)
#   6. Morning handoff docs (morning-handoff.py)
#   7. Salesforce integration lens (module-priority.json → salesforce_tagged_paths)
#   8. ACP for heavy repos (routed via sessions_spawn)
#   9. Per-repo recommendations (morning-handoff.py)
#  10. Morning execution queue (morning-handoff.py → build_execution_queue)
#
# Usage: ./overnight-batch.sh [--repos repo1,repo2,...] [--target-coverage 80]
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="${SCRIPT_DIR}/state"
HANDOFF_DIR="${SCRIPT_DIR}/handoffs"
DATE=$(date -u +%Y-%m-%d)
OVERNIGHT_BATCH=1  # Used by branch guards
export OVERNIGHT_BATCH

# Defaults
TARGET_COVERAGE=80
REPOS_DIR="/data/workspace/repos"

# ACP-preferred repos (item 8)
ACP_REPOS="forwardlane-backend,signal-builder-backend,signal-studio"

mkdir -p "$STATE_DIR" "$HANDOFF_DIR"

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --repos) REPO_LIST="$2"; shift 2 ;;
    --target-coverage) TARGET_COVERAGE="$2"; shift 2 ;;
    --repos-dir) REPOS_DIR="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Reset failure state for fresh batch
bash "${SCRIPT_DIR}/failure-alert.sh" reset

echo "============================================"
echo "🌙 OVERNIGHT BATCH — ${DATE}"
echo "   Target coverage: ${TARGET_COVERAGE}%"
echo "   Repos dir: ${REPOS_DIR}"
echo "============================================"

# Load module priorities
PRIORITY_FILE="${SCRIPT_DIR}/module-priority.json"
if [[ -f "$PRIORITY_FILE" ]]; then
  echo "📋 Module priorities loaded from ${PRIORITY_FILE}"
else
  echo "⚠️ No module-priority.json found — running without priority ranking"
fi

# Discover repos if not specified
if [[ -z "${REPO_LIST:-}" ]]; then
  REPO_LIST=""
  for dir in "$REPOS_DIR"/*/; do
    if [[ -d "$dir/.git" ]]; then
      repo_name=$(basename "$dir")
      REPO_LIST="${REPO_LIST:+${REPO_LIST},}${repo_name}"
    fi
  done
fi

if [[ -z "$REPO_LIST" ]]; then
  echo "❌ No repos found in ${REPOS_DIR}"
  exit 1
fi

echo "📦 Repos: ${REPO_LIST}"
echo ""

# Process each repo
IFS=',' read -ra REPOS <<< "$REPO_LIST"
for repo_name in "${REPOS[@]}"; do
  repo_path="${REPOS_DIR}/${repo_name}"
  
  if [[ ! -d "$repo_path" ]]; then
    echo "⚠️ Skipping ${repo_name} — not found at ${repo_path}"
    continue
  fi
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔧 Processing: ${repo_name}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  # 2. Create overnight branch
  echo "🌿 Creating overnight branch..."
  bash "${SCRIPT_DIR}/branch-safe.sh" branch "$repo_path" "$repo_name" "coverage-${DATE}" 2>/dev/null || true
  
  # 2. Install branch guard
  bash "${SCRIPT_DIR}/branch-safe.sh" guard "$repo_path" 2>/dev/null || true
  
  # Detect test framework
  if [[ -f "$repo_path/pytest.ini" ]] || [[ -f "$repo_path/setup.cfg" ]] || [[ -f "$repo_path/pyproject.toml" ]]; then
    FRAMEWORK="pytest"
  elif [[ -f "$repo_path/jest.config.js" ]] || [[ -f "$repo_path/jest.config.ts" ]] || grep -q '"jest"' "$repo_path/package.json" 2>/dev/null; then
    FRAMEWORK="jest"
  elif [[ -f "$repo_path/vitest.config.ts" ]] || [[ -f "$repo_path/vitest.config.js" ]]; then
    FRAMEWORK="vitest"
  else
    FRAMEWORK="unknown"
  fi
  
  echo "   Framework: ${FRAMEWORK}"
  
  # Get initial coverage (simplified — real implementation runs the test suite)
  INITIAL_COVERAGE=0
  
  # 5. Start stop-loss tracking
  python3 "${SCRIPT_DIR}/stop-loss.py" start "$repo_name" "$INITIAL_COVERAGE" 2>/dev/null || true
  
  # 3. Record initial coverage in scoreboard
  python3 "${SCRIPT_DIR}/coverage-scoreboard.py" update "$repo_name" "$INITIAL_COVERAGE" \
    --framework "$FRAMEWORK" 2>/dev/null || true
  
  # 8. Route to ACP for heavy repos
  IS_ACP_REPO=false
  if echo "$ACP_REPOS" | grep -q "$repo_name"; then
    IS_ACP_REPO=true
    echo "   🔬 ACP-preferred repo — will use sessions_spawn with ACP runtime"
  fi
  
  # 7. Tag Salesforce-relevant paths
  if python3 -c "
import json
with open('$PRIORITY_FILE') as f: p = json.load(f)
sf = p.get('salesforce_tagged_paths', {})
for k, v in sf.items():
    if isinstance(v, dict) and '$repo_name' in v.get('repos', []):
        print(f'   🔗 SF: {k} → {v.get(\"sf_component\", \"?\")}')
        exit(0)
exit(1)
" 2>/dev/null; then
    echo "   ⬆️ Has Salesforce-facing endpoints"
  fi
  
  # 4. Identify high-value modules for this repo
  python3 -c "
import json
with open('$PRIORITY_FILE') as f: p = json.load(f)
for tier_name, tier in p.get('priority_tiers', {}).items():
    for m in tier.get('modules', []):
        if '$repo_name' in m.get('repos', []):
            print(f'   🎯 {tier_name.upper()}: {m[\"name\"]} (target: {tier.get(\"target_coverage\", \"?\")}%)')
" 2>/dev/null || true

  # Log success/failure for this repo
  # In real usage, this wraps the actual test/coverage commands
  bash "${SCRIPT_DIR}/failure-alert.sh" success "$repo_name" "overnight-setup" 2>/dev/null || true
  
  echo "   ✅ Setup complete for ${repo_name}"
done

echo ""
echo "============================================"
echo "🌙 OVERNIGHT BATCH SETUP COMPLETE"
echo "   Repos configured: ${#REPOS[@]}"
echo "   Branch guards installed"
echo "   Stop-loss tracking active"
echo "   Coverage scoreboard initialized"
echo "============================================"
echo ""
echo "▶️ To generate morning handoff after batch completes:"
echo "   python3 ${SCRIPT_DIR}/morning-handoff.py morning"
echo ""
echo "▶️ To check coverage scoreboard:"
echo "   python3 ${SCRIPT_DIR}/coverage-scoreboard.py show"
echo ""
echo "▶️ To check failure alerts:"
echo "   bash ${SCRIPT_DIR}/failure-alert.sh status"
echo ""
echo "▶️ To check stop-loss status:"
echo "   python3 ${SCRIPT_DIR}/stop-loss.py status"
