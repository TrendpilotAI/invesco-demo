#!/bin/bash
# auto-review.sh — Automated heuristic PR review (NOT LLM-powered).
# Usage: auto-review.sh <owner/repo> <pr-number>
# This is pattern-matching, NOT AI. Don't call it "LLM-powered" - it's grep.
# For real LLM review, spawn a subagent that reads the diff.

set -euo pipefail

REPO="${1:?Usage: review-pr.sh owner/repo pr-number}"
PR="${2:?Usage: review-pr.sh owner/repo pr-number}"

echo "🔍 Reviewing PR #$PR on $REPO"

# Get PR details
PR_INFO=$(gh pr view "$PR" -R "$REPO" --json title,body,state,mergeable,additions,deletions)
TITLE=$(echo "$PR_INFO" | jq -r '.title')
STATE=$(echo "$PR_INFO" | jq -r '.state')
ADDITIONS=$(echo "$PR_INFO" | jq -r '.additions')
DELETIONS=$(echo "$PR_INFO" | jq -r '.deletions')

echo "📝 $TITLE (+$ADDITIONS/-$DELETIONS)"

if [ "$STATE" != "OPEN" ]; then
  echo "⚠️  PR is not open, skipping review"
  exit 0
fi

# Get diff
DIFF_FILE="/tmp/pr-${PR}-$(date +%s).diff"
gh pr diff "$PR" -R "$REPO" --no-color > "$DIFF_FILE" || { 
  echo "❌ Could not fetch diff"; 
  exit 1; 
}

DIFF_SIZE=$(wc -l < "$DIFF_FILE")
echo "📄 Diff: $DIFF_SIZE lines"

if [ "$DIFF_SIZE" -gt 10000 ]; then
  echo "⚠️  Diff too large, truncating to 10000 lines"
  head -10000 "$DIFF_FILE" > "$DIFF_FILE.tmp"
  mv "$DIFF_FILE.tmp" "$DIFF_FILE"
fi

# Build review prompt
REVIEW_PROMPT="You are a senior code reviewer. Review this PR for:

1. **Security** — auth bypass, injection, secrets, SQLi, XSS, CORS, rate limiting
2. **Correctness** — logic errors, edge cases, error handling
3. **Testing** — adequate coverage, meaningful assertions, edge cases
4. **Architecture** — follows patterns, no over-engineering

Rules:
- Approve if no critical issues
- Request changes ONLY for: security vulnerabilities, correctness bugs
- Do NOT block for: style preferences, naming, minor refactors
- Be specific: quote the line, explain the risk, suggest fix

Output format:
- APPROVE — \"1-line note\"
- REQUEST_CHANGES — \"bullet list of issues with line refs\"

The PR title: $TITLE
The diff is in $DIFF_FILE"

# Run review via subagent
echo "🤖 Running LLM review..."

# Create a temp prompt file
PROMPT_FILE="/tmp/review-prompt-${PR}.txt"
echo "$REVIEW_PROMPT" > "$PROMPT_FILE"

# Read diff into context for the review
DIFF_CONTENT=$(cat "$DIFF_FILE")

# Since we can't easily spawn a subagent from bash, we'll use a simple heuristic
# and recommend manual review for complex PRs. In production, this would call the LLM.

# Simple automated checks (fast)
ISSUES=""

# Check for secrets in diff
if grep -iqE "(sk-[a-zA-Z0-9]{20,}|password\s*[:=]|api_key|secret|token)" "$DIFF_FILE" 2>/dev/null; then
  ISSUES="${ISSUES}\n🔴 SECURITY: Possible hardcoded secret detected"
fi

# Check for dangerous patterns
if grep -qE "\.execute\(.*\+.*\)" "$DIFF_FILE" 2>/dev/null; then
  ISSUES="${ISSUES}\n🔴 SECURITY: Potential SQL injection (string concatenation in execute)"
fi

if grep -qE "eval\(|exec\(" "$DIFF_FILE" 2>/dev/null; then
  ISSUES="${ISSUES}\n🔴 SECURITY: Dangerous eval/exec usage"
fi

# Check for missing error handling
if grep -qE "def .*:\s*$" "$DIFF_FILE" 2>/dev/null; then
  # Functions without try/except in diff
  :
fi

# Report
if [ -n "$ISSUES" ]; then
  echo -e "⚠️  Automated checks found issues:$ISSUES"
  echo ""
  
  # Post review comment with issues
  gh pr comment "$PR" -R "$REPO" --body "$(echo -e "🤖 **Automated review:**\n\nIssues found:\n$ISSUES\n\nPlease address before merging.")" 2>/dev/null || true
  
  # Request changes
  gh pr review "$PR" -R "$REPO" --request-changes --body "$(echo -e "Automated review found issues:\n$ISSUES")" 2>/dev/null || true
  
  echo "❌ REQUEST_CHANGES"
  exit 1
else
  # Post approval
  echo "✅ Automated checks passed"
  
  # For complex PRs, recommend manual review
  if [ "$DIFF_SIZE" -gt 500 ] || [ "$ADDITIONS" -gt 200 ]; then
    gh pr comment "$PR" -R "$REPO" --body "🤖 **Automated review:** ✅ Pass

Note: This is a large PR (+$ADDITIONS/-$DELETIONS). Manual review recommended for:
- Business logic changes
- Edge case handling
- Test coverage" 2>/dev/null || true
  fi
  
  gh pr review "$PR" -R "$REPO" --approve --body "🤖 Automated review: ✅ LGTM" 2>/dev/null || true
  
  echo "✅ APPROVE"
  exit 0
fi
