import { execSync, exec } from "child_process";
import { readdirSync, statSync, existsSync, mkdirSync, writeFileSync, readFileSync } from "fs";
import { join, dirname } from "path";

// --- Types ---

export interface BackupStatus {
  lastBackup: string | null;
  lastSize: number | null;
  lastSuccess: boolean;
  lastError: string | null;
  totalBackups: number;
}

export interface RetentionConfig {
  dailyKeep: number;
  weeklyKeep: number;
}

export interface SchedulerConfig {
  backupDir: string;
  scriptsDir: string;
  cronExpression: string; // e.g. "0 2 * * *" = daily 2am
  retention: RetentionConfig;
  statusFile: string;
}

// --- Cron Parser (minimal) ---

export function parseCron(expression: string): { hour: number; minute: number; daysOfWeek?: number[] } {
  const parts = expression.trim().split(/\s+/);
  if (parts.length < 5) throw new Error(`Invalid cron expression: ${expression}`);
  const [min, hour, , , dow] = parts;
  return {
    minute: min === "*" ? 0 : parseInt(min, 10),
    hour: hour === "*" ? 0 : parseInt(hour, 10),
    daysOfWeek: dow === "*" ? undefined : dow.split(",").map(Number),
  };
}

export function shouldRunNow(expression: string, now: Date = new Date()): boolean {
  const cron = parseCron(expression);
  if (now.getUTCHours() !== cron.hour) return false;
  if (now.getUTCMinutes() !== cron.minute) return false;
  if (cron.daysOfWeek && !cron.daysOfWeek.includes(now.getUTCDay())) return false;
  return true;
}

// --- Retention Logic ---

export interface BackupFile {
  name: string;
  path: string;
  date: Date;
  size: number;
}

export function parseBackupFilename(filename: string): Date | null {
  // backup-YYYY-MM-DD-HHMMSS.sql.gz or redis-backup-YYYY-MM-DD-HHMMSS.rdb.gz
  const match = filename.match(/(\d{4})-(\d{2})-(\d{2})-(\d{2})(\d{2})(\d{2})/);
  if (!match) return null;
  const [, y, mo, d, h, mi, s] = match;
  return new Date(Date.UTC(+y, +mo - 1, +d, +h, +mi, +s));
}

export function listBackups(dir: string, prefix = "backup-"): BackupFile[] {
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.startsWith(prefix) && f.endsWith(".gz"))
    .map((name) => {
      const path = join(dir, name);
      const date = parseBackupFilename(name);
      if (!date) return null;
      const size = statSync(path).size;
      return { name, path, date, size };
    })
    .filter(Boolean)
    .sort((a, b) => b!.date.getTime() - a!.date.getTime()) as BackupFile[];
}

export function selectBackupsToKeep(backups: BackupFile[], retention: RetentionConfig): Set<string> {
  const keep = new Set<string>();
  let dailyCount = 0;
  const weeklyDates = new Set<string>();

  // Sorted newest first
  for (const b of backups) {
    // Daily: keep the N most recent
    if (dailyCount < retention.dailyKeep) {
      keep.add(b.name);
      dailyCount++;
      continue;
    }

    // Weekly: keep Sunday backups beyond daily window
    if (b.date.getUTCDay() === 0 && weeklyDates.size < retention.weeklyKeep) {
      const dateKey = b.date.toISOString().slice(0, 10);
      if (!weeklyDates.has(dateKey)) {
        keep.add(b.name);
        weeklyDates.add(dateKey);
      }
    }
  }

  return keep;
}

export function cleanupBackups(dir: string, retention: RetentionConfig, prefix = "backup-"): string[] {
  const backups = listBackups(dir, prefix);
  const keep = selectBackupsToKeep(backups, retention);
  const removed: string[] = [];

  for (const b of backups) {
    if (!keep.has(b.name)) {
      try {
        execSync(`rm -f "${b.path}"`);
        removed.push(b.name);
      } catch {}
    }
  }

  return removed;
}

// --- Status ---

export function loadStatus(statusFile: string): BackupStatus {
  if (existsSync(statusFile)) {
    try {
      return JSON.parse(readFileSync(statusFile, "utf-8"));
    } catch {}
  }
  return { lastBackup: null, lastSize: null, lastSuccess: false, lastError: null, totalBackups: 0 };
}

export function saveStatus(statusFile: string, status: BackupStatus): void {
  mkdirSync(dirname(statusFile), { recursive: true });
  writeFileSync(statusFile, JSON.stringify(status, null, 2));
}

// --- Runner ---

export function runBackup(config: SchedulerConfig): BackupStatus {
  const status = loadStatus(config.statusFile);

  try {
    console.log(`[${new Date().toISOString()}] Running postgres backup...`);
    execSync(`bash ${join(config.scriptsDir, "postgres-backup.sh")}`, {
      env: { ...process.env, BACKUP_DIR: config.backupDir },
      stdio: "inherit",
    });

    const backups = listBackups(config.backupDir);
    const latest = backups[0];

    status.lastBackup = new Date().toISOString();
    status.lastSize = latest?.size ?? null;
    status.lastSuccess = true;
    status.lastError = null;
    status.totalBackups = backups.length;

    // Cleanup
    const removed = cleanupBackups(config.backupDir, config.retention);
    if (removed.length) console.log(`Cleaned up ${removed.length} old backups`);
    status.totalBackups -= removed.length;
  } catch (err: any) {
    status.lastBackup = new Date().toISOString();
    status.lastSuccess = false;
    status.lastError = err.message || String(err);
  }

  saveStatus(config.statusFile, status);
  return status;
}

// --- Main Loop ---

if (require.main === module) {
  const SCRIPTS_DIR = __dirname + "/..";
  const config: SchedulerConfig = {
    backupDir: join(SCRIPTS_DIR, "snapshots"),
    scriptsDir: SCRIPTS_DIR,
    cronExpression: process.env.BACKUP_CRON || "0 2 * * *",
    retention: {
      dailyKeep: parseInt(process.env.DAILY_RETENTION || "7", 10),
      weeklyKeep: parseInt(process.env.WEEKLY_RETENTION || "4", 10),
    },
    statusFile: join(SCRIPTS_DIR, "status.json"),
  };

  console.log("Backup scheduler started");
  console.log(`  Cron: ${config.cronExpression}`);
  console.log(`  Retention: ${config.retention.dailyKeep} daily, ${config.retention.weeklyKeep} weekly`);

  // Check every minute
  setInterval(() => {
    if (shouldRunNow(config.cronExpression)) {
      runBackup(config);
    }
  }, 60_000);

  // Also run immediately if --now flag
  if (process.argv.includes("--now")) {
    runBackup(config);
  }
}
