#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:?Usage: rollback.sh <project-name> [commit-sha]}"
COMMIT="${2:-HEAD~1}"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PROJECT_DIR="$REPO_ROOT/projects/$PROJECT"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ Project not found: $PROJECT_DIR"
  exit 1
fi

cd "$PROJECT_DIR"

CURRENT=$(git rev-parse --short HEAD)
TARGET=$(git rev-parse --short "$COMMIT")

echo "⏪ Rolling back $PROJECT"
echo "   From: $CURRENT"
echo "   To:   $TARGET"
read -p "Continue? [y/N] " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  git revert --no-edit HEAD
  echo "✅ Reverted to $TARGET. Run deploy.sh to redeploy."
else
  echo "Cancelled."
fi
