#!/usr/bin/env bash
set -euo pipefail

# Restore Script — One-command restore for Postgres and Redis backups

DATABASE_URL="${DATABASE_URL:-postgresql://postgres:BtFlrZjz4BV*QcOsd9u*glFKUhAAgqIw@postgres.railway.internal:5432/railway}"
LOG_FILE="${LOG_FILE:-$(dirname "$0")/backup.log}"
DRY_RUN=false
BACKUP_FILE=""

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS] <backup-file>

Restore a Postgres or Redis backup.

Options:
  --dry-run     Validate backup without restoring
  --db-url URL  Override DATABASE_URL
  -h, --help    Show this help

Examples:
  $(basename "$0") snapshots/backup-2026-02-17-130000.sql.gz
  $(basename "$0") --dry-run snapshots/backup-2026-02-17-130000.sql.gz
  $(basename "$0") snapshots/redis-backup-2026-02-17-130000.rdb.gz
EOF
  exit 0
}

log() {
  local msg="[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] [restore] $1"
  echo "$msg" | tee -a "$LOG_FILE"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --db-url) DATABASE_URL="$2"; shift 2 ;;
    -h|--help) usage ;;
    -*) echo "Unknown option: $1"; exit 1 ;;
    *) BACKUP_FILE="$1"; shift ;;
  esac
done

if [ -z "$BACKUP_FILE" ]; then
  echo "Error: No backup file specified"
  usage
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: File not found: $BACKUP_FILE"
  exit 1
fi

# Detect backup type
BASENAME=$(basename "$BACKUP_FILE")
if [[ "$BASENAME" == redis-backup-* ]]; then
  BACKUP_TYPE="redis"
elif [[ "$BASENAME" == backup-* ]]; then
  BACKUP_TYPE="postgres"
else
  echo "Error: Unrecognized backup filename pattern: $BASENAME"
  exit 1
fi

# Validate file
log "Validating ${BACKUP_TYPE} backup: ${BASENAME}"
if [[ "$BACKUP_FILE" == *.gz ]]; then
  if ! gzip -t "$BACKUP_FILE" 2>/dev/null; then
    log "ERROR: File is not a valid gzip archive"
    exit 1
  fi
  log "Gzip validation passed"
fi

if [ "$DRY_RUN" = true ]; then
  log "DRY RUN: ${BACKUP_TYPE} backup is valid and ready to restore"
  if [ "$BACKUP_TYPE" = "postgres" ]; then
    log "DRY RUN: Would restore to database via: $DATABASE_URL"
    LINES=$(gunzip -c "$BACKUP_FILE" | wc -l)
    log "DRY RUN: Backup contains ${LINES} SQL lines"
  fi
  exit 0
fi

# Restore
if [ "$BACKUP_TYPE" = "postgres" ]; then
  log "Restoring Postgres backup: ${BASENAME}"
  log "WARNING: This will overwrite data in the target database!"
  
  if ! gunzip -c "$BACKUP_FILE" | psql "$DATABASE_URL"; then
    log "ERROR: Postgres restore failed"
    exit 1
  fi
  log "Postgres restore completed successfully"

elif [ "$BACKUP_TYPE" = "redis" ]; then
  REDIS_HOST="${REDIS_HOST:-redis.railway.internal}"
  REDIS_PORT="${REDIS_PORT:-6379}"
  REDIS_PASSWORD="${REDIS_PASSWORD:-n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E}"
  REDIS_RDB_PATH="${REDIS_RDB_PATH:-/data/dump.rdb}"

  log "Restoring Redis backup: ${BASENAME}"
  TEMP_RDB="/tmp/restore-$$.rdb"
  gunzip -c "$BACKUP_FILE" > "$TEMP_RDB"

  # Stop Redis, replace RDB, restart
  log "Stopping Redis for RDB replacement"
  redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" --no-auth-warning SHUTDOWN NOSAVE 2>/dev/null || true
  cp "$TEMP_RDB" "$REDIS_RDB_PATH"
  rm -f "$TEMP_RDB"
  log "Redis RDB replaced. Redis needs to be restarted to load the new dump."
fi

exit 0
