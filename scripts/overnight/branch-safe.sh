#!/usr/bin/env bash
# 2. Branch-Safe Workflow Enforcement
# Ensures overnight agents work on feature branches, never push directly to main/master.
# Usage: source this before any overnight repo work.

set -euo pipefail

OVERNIGHT_BRANCH_PREFIX="overnight"

# Create a safe feature branch for overnight work
create_overnight_branch() {
  local repo_path="$1"
  local repo_name="$2"
  local task_desc="${3:-coverage}"
  
  cd "$repo_path" || { echo "❌ Cannot cd to $repo_path"; return 1; }
  
  local date_stamp=$(date -u +%Y%m%d)
  local branch_name="${OVERNIGHT_BRANCH_PREFIX}/${date_stamp}-${task_desc}"
  
  # Ensure we're on latest default branch first
  local default_branch
  default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
  
  # Fetch latest
  git fetch origin "$default_branch" 2>/dev/null || true
  
  # Create and switch to overnight branch
  if git show-ref --verify --quiet "refs/heads/$branch_name" 2>/dev/null; then
    git checkout "$branch_name"
    echo "📌 Resumed existing branch: $branch_name"
  else
    git checkout -b "$branch_name" "origin/$default_branch" 2>/dev/null || \
    git checkout -b "$branch_name" "$default_branch" 2>/dev/null || \
    git checkout -b "$branch_name"
    echo "🌿 Created overnight branch: $branch_name"
  fi
  
  echo "$branch_name"
}

# Commit incrementally with descriptive messages
overnight_commit() {
  local repo_path="$1"
  local message="$2"
  
  cd "$repo_path" || return 1
  
  # Safety: verify we're NOT on main/master
  local current_branch
  current_branch=$(git branch --show-current)
  if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "🚨 BLOCKED: Cannot commit to $current_branch during overnight batch!"
    echo "   Create an overnight branch first with create_overnight_branch"
    return 1
  fi
  
  git add -A
  if git diff --cached --quiet; then
    echo "ℹ️ No changes to commit"
    return 0
  fi
  
  git commit -m "[overnight] $message" --no-verify
  echo "✅ Committed: [overnight] $message on $current_branch"
}

# Push overnight branch (never main/master)
overnight_push() {
  local repo_path="$1"
  
  cd "$repo_path" || return 1
  
  local current_branch
  current_branch=$(git branch --show-current)
  
  if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "🚨 BLOCKED: Will not push to $current_branch!"
    return 1
  fi
  
  git push origin "$current_branch" --set-upstream 2>/dev/null || \
  git push origin "$current_branch" 2>/dev/null || \
  echo "⚠️ Push failed (may need auth or remote setup)"
}

# Git hook installer — prevents direct commits to protected branches
install_branch_guard() {
  local repo_path="$1"
  local hook_path="$repo_path/.git/hooks/pre-commit"
  
  mkdir -p "$repo_path/.git/hooks"
  
  cat > "$hook_path" << 'HOOK'
#!/usr/bin/env bash
# Branch guard: block commits to main/master during overnight batch
branch=$(git branch --show-current)
if [[ "$branch" == "main" || "$branch" == "master" ]]; then
  if [[ "${OVERNIGHT_BATCH:-}" == "1" ]]; then
    echo "🚨 BLOCKED: Overnight batch cannot commit to $branch"
    echo "   Use create_overnight_branch first"
    exit 1
  fi
fi
exit 0
HOOK
  chmod +x "$hook_path"
  echo "🔒 Branch guard installed at $repo_path"
}

# CLI
case "${1:-}" in
  branch) create_overnight_branch "${2:-.}" "${3:-repo}" "${4:-coverage}" ;;
  commit) overnight_commit "${2:-.}" "${3:-overnight work}" ;;
  push) overnight_push "${2:-.}" ;;
  guard) install_branch_guard "${2:-.}" ;;
  *)
    echo "Usage: $0 {branch|commit|push|guard} [repo_path] [repo_name|message] [task_desc]"
    echo ""
    echo "  branch <path> <name> <task>  — Create overnight feature branch"
    echo "  commit <path> <message>      — Commit (blocked on main/master)"
    echo "  push <path>                  — Push overnight branch"
    echo "  guard <path>                 — Install pre-commit hook"
    ;;
esac
