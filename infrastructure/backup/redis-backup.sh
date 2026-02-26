#!/usr/bin/env bash
set -euo pipefail

# Redis Backup Script
# Triggers BGSAVE, exports and compresses RDB dump

BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/snapshots}"
LOG_FILE="${LOG_FILE:-$(dirname "$0")/backup.log}"
REDIS_HOST="${REDIS_HOST:-redis.railway.internal}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_PASSWORD="${REDIS_PASSWORD:-n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E}"
REDIS_RDB_PATH="${REDIS_RDB_PATH:-/data/dump.rdb}"

log() {
  local msg="[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] [redis] $1"
  echo "$msg" | tee -a "$LOG_FILE"
}

REDIS_CLI="redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD --no-auth-warning"

mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date -u '+%Y-%m-%d-%H%M%S')
FILENAME="redis-backup-${TIMESTAMP}.rdb.gz"
FILEPATH="${BACKUP_DIR}/${FILENAME}"

log "Triggering Redis BGSAVE"

if ! $REDIS_CLI BGSAVE; then
  log "ERROR: BGSAVE command failed"
  exit 1
fi

# Wait for BGSAVE to complete
log "Waiting for BGSAVE to finish..."
MAX_WAIT=120
WAITED=0
while [ "$WAITED" -lt "$MAX_WAIT" ]; do
  LASTSAVE=$($REDIS_CLI LASTSAVE 2>/dev/null | tr -d '[:space:]')
  BG_STATUS=$($REDIS_CLI INFO persistence 2>/dev/null | grep rdb_bgsave_in_progress | tr -d '[:space:]' | cut -d: -f2)
  if [ "${BG_STATUS:-1}" = "0" ]; then
    log "BGSAVE completed"
    break
  fi
  sleep 2
  WAITED=$((WAITED + 2))
done

if [ "$WAITED" -ge "$MAX_WAIT" ]; then
  log "WARNING: BGSAVE may not have completed within ${MAX_WAIT}s, proceeding anyway"
fi

# Copy and compress RDB file
if [ -f "$REDIS_RDB_PATH" ]; then
  gzip -c "$REDIS_RDB_PATH" > "$FILEPATH"
elif $REDIS_CLI --rdb /tmp/redis-dump-$$.rdb 2>/dev/null; then
  gzip -c /tmp/redis-dump-$$.rdb > "$FILEPATH"
  rm -f /tmp/redis-dump-$$.rdb
else
  log "ERROR: Could not export RDB dump"
  exit 1
fi

SIZE=$(stat -c%s "$FILEPATH" 2>/dev/null || stat -f%z "$FILEPATH" 2>/dev/null || echo "unknown")
log "Redis backup complete: ${FILENAME} (${SIZE} bytes)"
exit 0
