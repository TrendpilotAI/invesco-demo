#!/usr/bin/env bash
set -euo pipefail

# Postgres Backup Script
# Automated pg_dump with compression, timestamped filenames, and retention policy

BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/snapshots}"
LOG_FILE="${LOG_FILE:-$(dirname "$0")/backup.log}"
DATABASE_URL="${DATABASE_URL:-postgresql://postgres:BtFlrZjz4BV*QcOsd9u*glFKUhAAgqIw@postgres.railway.internal:5432/railway}"
DAILY_RETENTION="${DAILY_RETENTION:-7}"
WEEKLY_RETENTION="${WEEKLY_RETENTION:-4}"

log() {
  local msg="[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] $1"
  echo "$msg" | tee -a "$LOG_FILE"
}

mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date -u '+%Y-%m-%d-%H%M%S')
FILENAME="backup-${TIMESTAMP}.sql.gz"
FILEPATH="${BACKUP_DIR}/${FILENAME}"

log "Starting Postgres backup: ${FILENAME}"

if ! pg_dump "$DATABASE_URL" | gzip > "$FILEPATH"; then
  log "ERROR: pg_dump failed (exit code: $?)"
  rm -f "$FILEPATH"
  exit 1
fi

SIZE=$(stat -c%s "$FILEPATH" 2>/dev/null || stat -f%z "$FILEPATH" 2>/dev/null || echo "unknown")
log "Backup complete: ${FILENAME} (${SIZE} bytes)"

# Retention cleanup
cleanup_old_backups() {
  log "Running retention cleanup (daily=${DAILY_RETENTION}, weekly=${WEEKLY_RETENTION})"

  # Get all backups sorted newest first
  local all_backups
  all_backups=$(ls -1t "$BACKUP_DIR"/backup-*.sql.gz 2>/dev/null || true)
  [ -z "$all_backups" ] && return

  local keep_files=()
  local daily_count=0
  local weekly_dates=()

  while IFS= read -r file; do
    local basename
    basename=$(basename "$file")
    # Extract date from filename: backup-YYYY-MM-DD-HHMMSS.sql.gz
    local date_part
    date_part=$(echo "$basename" | sed 's/backup-\([0-9-]*\)-[0-9]*.sql.gz/\1/')
    local day_of_week
    day_of_week=$(date -d "$date_part" '+%u' 2>/dev/null || date -j -f '%Y-%m-%d' "$date_part" '+%u' 2>/dev/null || echo "1")

    local dominated=false

    # Keep last N daily backups
    if [ "$daily_count" -lt "$DAILY_RETENTION" ]; then
      keep_files+=("$file")
      daily_count=$((daily_count + 1))
      dominated=true
    fi

    # Keep weekly backups (Sunday = 7) beyond daily window
    if [ "$dominated" = false ] && [ "$day_of_week" = "7" ]; then
      if [ "${#weekly_dates[@]}" -lt "$WEEKLY_RETENTION" ]; then
        local dominated_weekly=false
        for wd in "${weekly_dates[@]+"${weekly_dates[@]}"}"; do
          [ "$wd" = "$date_part" ] && dominated_weekly=true
        done
        if [ "$dominated_weekly" = false ]; then
          keep_files+=("$file")
          weekly_dates+=("$date_part")
        fi
      fi
    fi
  done <<< "$all_backups"

  # Remove files not in keep list
  while IFS= read -r file; do
    [ -z "$file" ] && continue
    local should_keep=false
    for kf in "${keep_files[@]+"${keep_files[@]}"}"; do
      [ "$file" = "$kf" ] && should_keep=true
    done
    if [ "$should_keep" = false ]; then
      log "Removing old backup: $(basename "$file")"
      rm -f "$file"
    fi
  done <<< "$all_backups"
}

cleanup_old_backups
log "Backup process finished successfully"
exit 0
