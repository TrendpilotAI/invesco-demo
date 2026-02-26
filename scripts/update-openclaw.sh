#!/usr/bin/env bash
set -euo pipefail

LOG="/data/workspace/memory/openclaw-update-$(date +%Y%m%d).log"
echo "=== OpenClaw Update Started: $(date -u) ===" | tee "$LOG"

# Pre-update: save current version
OLD_VERSION=$(openclaw --version 2>/dev/null | head -1)
echo "Current version: $OLD_VERSION" | tee -a "$LOG"

# Stop the Temporal worker gracefully
if [ -f /tmp/honey-temporal-worker.pid ] && kill -0 "$(cat /tmp/honey-temporal-worker.pid)" 2>/dev/null; then
    echo "Stopping Temporal worker..." | tee -a "$LOG"
    kill "$(cat /tmp/honey-temporal-worker.pid)" 2>/dev/null || true
    sleep 2
fi

# Run update
echo "Updating OpenClaw..." | tee -a "$LOG"
npm install -g openclaw@latest 2>&1 | tee -a "$LOG"

# Restart gateway
echo "Restarting gateway..." | tee -a "$LOG"
openclaw gateway restart 2>&1 | tee -a "$LOG" || true
sleep 5

# Post-update: verify
NEW_VERSION=$(openclaw --version 2>/dev/null | head -1)
echo "New version: $NEW_VERSION" | tee -a "$LOG"

# Restart Temporal worker
echo "Restarting Temporal worker..." | tee -a "$LOG"
cd /data/workspace/scripts/temporal
TEMPORAL_NAMESPACE=honey-agents TEMPORAL_HOST=temporal.railway.internal:7233 \
  nohup python3 worker.py > /tmp/honey-temporal-worker.log 2>&1 &
echo $! > /tmp/honey-temporal-worker.pid
echo "Temporal worker restarted (PID $!)" | tee -a "$LOG"

# Re-enable daily-cleanup cron
openclaw cron enable c25e58d5-1061-4dd2-9d0a-4061f015cd52 2>&1 | grep '"enabled"' | tee -a "$LOG"

echo "=== Update Complete: $OLD_VERSION → $NEW_VERSION ===" | tee -a "$LOG"
echo "UPDATE_SUCCESS"
