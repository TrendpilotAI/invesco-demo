import {
  parseCron,
  shouldRunNow,
  parseBackupFilename,
  selectBackupsToKeep,
  listBackups,
  RetentionConfig,
  BackupFile,
} from "../src/backup-scheduler";
import { mkdirSync, writeFileSync, rmSync, existsSync } from "fs";
import { join } from "path";

const TEST_DIR = join(__dirname, "test-snapshots");

function makeBackup(name: string, date: Date): BackupFile {
  return { name, path: join(TEST_DIR, name), date, size: 1024 };
}

beforeEach(() => {
  if (existsSync(TEST_DIR)) rmSync(TEST_DIR, { recursive: true });
  mkdirSync(TEST_DIR, { recursive: true });
});

afterAll(() => {
  if (existsSync(TEST_DIR)) rmSync(TEST_DIR, { recursive: true });
});

// Test 1: Cron parsing
describe("parseCron", () => {
  it("parses a standard daily cron expression", () => {
    const result = parseCron("30 2 * * *");
    expect(result.minute).toBe(30);
    expect(result.hour).toBe(2);
    expect(result.daysOfWeek).toBeUndefined();
  });

  it("parses day-of-week restrictions", () => {
    const result = parseCron("0 3 * * 1,5");
    expect(result.daysOfWeek).toEqual([1, 5]);
  });

  it("throws on invalid expression", () => {
    expect(() => parseCron("bad")).toThrow();
  });
});

// Test 2: shouldRunNow
describe("shouldRunNow", () => {
  it("returns true when current time matches cron", () => {
    const now = new Date("2026-02-17T02:30:00Z");
    expect(shouldRunNow("30 2 * * *", now)).toBe(true);
  });

  it("returns false when hour does not match", () => {
    const now = new Date("2026-02-17T03:30:00Z");
    expect(shouldRunNow("30 2 * * *", now)).toBe(false);
  });

  it("respects day-of-week filter", () => {
    // 2026-02-17 is a Tuesday (day 2)
    const now = new Date("2026-02-17T02:00:00Z");
    expect(shouldRunNow("0 2 * * 1", now)).toBe(false); // Monday only
    expect(shouldRunNow("0 2 * * 2", now)).toBe(true);  // Tuesday
  });
});

// Test 3: parseBackupFilename
describe("parseBackupFilename", () => {
  it("parses postgres backup filename", () => {
    const d = parseBackupFilename("backup-2026-02-17-023000.sql.gz");
    expect(d).toEqual(new Date(Date.UTC(2026, 1, 17, 2, 30, 0)));
  });

  it("parses redis backup filename", () => {
    const d = parseBackupFilename("redis-backup-2026-01-05-120000.rdb.gz");
    expect(d).toEqual(new Date(Date.UTC(2026, 0, 5, 12, 0, 0)));
  });

  it("returns null for invalid filename", () => {
    expect(parseBackupFilename("not-a-backup.txt")).toBeNull();
  });
});

// Test 4: Retention — keeps correct number of daily backups
describe("selectBackupsToKeep", () => {
  it("keeps only the N most recent daily backups", () => {
    const retention: RetentionConfig = { dailyKeep: 3, weeklyKeep: 0 };
    const backups: BackupFile[] = [];
    for (let i = 0; i < 10; i++) {
      const d = new Date(Date.UTC(2026, 1, 10 + i, 2, 0, 0));
      backups.push(makeBackup(`backup-2026-02-${10 + i}-020000.sql.gz`, d));
    }
    // Sort newest first
    backups.sort((a, b) => b.date.getTime() - a.date.getTime());

    const keep = selectBackupsToKeep(backups, retention);
    expect(keep.size).toBe(3);
    // Should keep the 3 newest
    expect(keep.has(backups[0].name)).toBe(true);
    expect(keep.has(backups[1].name)).toBe(true);
    expect(keep.has(backups[2].name)).toBe(true);
    expect(keep.has(backups[9].name)).toBe(false);
  });

  // Test 5: Retention — keeps weekly (Sunday) backups beyond daily window
  it("keeps weekly Sunday backups beyond daily retention", () => {
    const retention: RetentionConfig = { dailyKeep: 2, weeklyKeep: 2 };
    const backups: BackupFile[] = [];

    // Create 30 days of backups, one per day
    for (let i = 0; i < 30; i++) {
      const d = new Date(Date.UTC(2026, 0, 1 + i, 2, 0, 0));
      const dd = String(1 + i).padStart(2, "0");
      backups.push(makeBackup(`backup-2026-01-${dd}-020000.sql.gz`, d));
    }
    backups.sort((a, b) => b.date.getTime() - a.date.getTime());

    const keep = selectBackupsToKeep(backups, retention);

    // 2 daily + up to 2 weekly Sundays
    // Jan 2026: Sundays are 4, 11, 18, 25
    // Newest 2 are Jan 30, 29 (daily)
    // Then first Sunday found going backwards: Jan 25, Jan 18
    expect(keep.size).toBe(4); // 2 daily + 2 weekly
  });

  it("handles empty backup list", () => {
    const keep = selectBackupsToKeep([], { dailyKeep: 7, weeklyKeep: 4 });
    expect(keep.size).toBe(0);
  });
});

// Test 6: listBackups with real files
describe("listBackups", () => {
  it("lists and sorts backup files from directory", () => {
    writeFileSync(join(TEST_DIR, "backup-2026-02-15-020000.sql.gz"), "fake");
    writeFileSync(join(TEST_DIR, "backup-2026-02-16-020000.sql.gz"), "fake");
    writeFileSync(join(TEST_DIR, "backup-2026-02-17-020000.sql.gz"), "fake");
    writeFileSync(join(TEST_DIR, "unrelated.txt"), "ignore");

    const result = listBackups(TEST_DIR);
    expect(result).toHaveLength(3);
    expect(result[0].name).toBe("backup-2026-02-17-020000.sql.gz");
    expect(result[2].name).toBe("backup-2026-02-15-020000.sql.gz");
  });

  it("returns empty array for nonexistent directory", () => {
    expect(listBackups("/nonexistent/path")).toEqual([]);
  });
});
