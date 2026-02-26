#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:?Usage: deploy.sh <project-name>}"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PROJECT_DIR="$REPO_ROOT/projects/$PROJECT"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ Project not found: $PROJECT_DIR"
  exit 1
fi

cd "$PROJECT_DIR"
echo "📦 Installing dependencies for $PROJECT..."
npm ci

echo "🔨 Building $PROJECT..."
npm run build

# Deploy based on project type
case "$PROJECT" in
  Second-Opinion)
    echo "🚀 Deploying $PROJECT via Firebase..."
    npx firebase deploy --only hosting
    ;;
  NarrativeReactor)
    echo "🚀 Deploying $PROJECT via Firebase Functions..."
    npx firebase deploy --only functions
    ;;
  flip-my-era|Trendpilot)
    echo "🚀 Deploying $PROJECT via Railway..."
    if command -v railway &>/dev/null; then
      railway up
    else
      echo "⚠️  Railway CLI not installed. Install: npm i -g @railway/cli"
      exit 1
    fi
    ;;
  *)
    echo "⚠️  No deploy target configured for $PROJECT"
    exit 1
    ;;
esac

echo "✅ $PROJECT deployed successfully!"
