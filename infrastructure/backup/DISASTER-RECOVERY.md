# Disaster Recovery Plan

> **Last updated:** 2026-02-17
> **Owner:** Infrastructure Team

## RTO / RPO Targets

| Service    | RPO (max data loss) | RTO (max downtime) |
|------------|--------------------|--------------------|
| Postgres   | 24 hours           | 1 hour             |
| Redis      | 24 hours           | 30 minutes         |
| Railway    | N/A (stateless)    | 15 minutes         |

## Backup Schedule

- **Postgres**: Daily at 02:00 UTC via `postgres-backup.sh`
- **Redis**: Daily at 02:15 UTC via `redis-backup.sh`
- **Retention**: 7 daily + 4 weekly backups

## Recovery Procedures

### 1. Postgres Recovery

**Scenario:** Database corruption, accidental deletion, or service failure.

```bash
# 1. List available backups
ls -la infrastructure/backup/snapshots/backup-*.sql.gz

# 2. Validate the backup (dry run)
bash infrastructure/backup/restore.sh --dry-run snapshots/backup-YYYY-MM-DD-HHMMSS.sql.gz

# 3. Restore
export DATABASE_URL="postgresql://postgres:PASSWORD@HOST:5432/railway"
bash infrastructure/backup/restore.sh snapshots/backup-YYYY-MM-DD-HHMMSS.sql.gz
```

**Notes:**
- Restore overwrites existing data — take a fresh backup first if possible
- For partial recovery, manually extract specific tables from the SQL dump
- Connection string uses Railway internal networking; use external proxy for remote restore

### 2. Redis Recovery

**Scenario:** Cache loss, data corruption, or Redis restart with empty state.

```bash
# 1. List available Redis backups
ls -la infrastructure/backup/snapshots/redis-backup-*.rdb.gz

# 2. Restore
export REDIS_HOST=redis.railway.internal
export REDIS_PORT=6379
bash infrastructure/backup/restore.sh snapshots/redis-backup-YYYY-MM-DD-HHMMSS.rdb.gz
```

**Notes:**
- Redis restore requires stopping the Redis server briefly
- After replacing the RDB file, restart the Redis service
- If Redis is used only as cache, consider if restore is necessary vs warm-up

### 3. Railway Redeployment

**Scenario:** Service crash, bad deploy, or infrastructure issue.

#### Rollback to Previous Deploy
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select the affected service
3. Go to **Deployments** tab
4. Click the last known good deployment → **Redeploy**

#### Full Redeployment from Scratch
1. Ensure environment variables are set (check `TOOLS.md` for credentials)
2. Connect GitHub repo or use Railway CLI:
   ```bash
   railway login
   railway link
   railway up
   ```
3. Verify services are healthy via Railway dashboard
4. Check Postgres and Redis connectivity

#### Environment Variables Checklist
- `DATABASE_URL` — Postgres connection string
- `REDIS_URL` — Redis connection string
- All service-specific env vars (check Railway dashboard > Variables)

### 4. Complete Infrastructure Recovery

If everything is down:

1. **Railway services** — Redeploy from GitHub (15 min)
2. **Postgres** — Will auto-provision on Railway; restore data from backup (30 min)
3. **Redis** — Will auto-provision on Railway; restore or let cache rebuild (15 min)
4. **Verify** — Check all services, run health checks
5. **DNS/Networking** — Verify custom domains if any

## Monitoring & Alerts

- Check `infrastructure/backup/status.json` for last backup status
- Check `infrastructure/backup/backup.log` for detailed logs
- Scheduler reports: `npm run scheduler:now` in backup directory

## Contact & Escalation

| Role               | Contact               | When                        |
|--------------------|-----------------------|-----------------------------|
| Primary On-Call    | (configure)           | First responder             |
| Infrastructure     | (configure)           | Railway/DB issues           |
| Railway Support    | support@railway.app   | Platform-level outages      |

## Testing Recovery

**Monthly drill checklist:**
- [ ] Verify backups exist and are recent
- [ ] Run `restore.sh --dry-run` on latest backup
- [ ] Test restore to a staging database
- [ ] Verify Railway redeploy from dashboard
- [ ] Update this document with any changes

## File Locations

| File                    | Purpose                          |
|------------------------|----------------------------------|
| `postgres-backup.sh`   | Automated Postgres backup        |
| `redis-backup.sh`      | Automated Redis backup           |
| `restore.sh`           | One-command restore              |
| `src/backup-scheduler.ts` | Cron-like backup scheduler    |
| `snapshots/`           | Backup storage directory         |
| `status.json`          | Last backup status               |
| `backup.log`           | Backup operation logs            |
