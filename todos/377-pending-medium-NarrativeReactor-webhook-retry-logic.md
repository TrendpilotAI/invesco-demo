# 377 — Add Webhook Retry Logic for Failed Publishes

## Task Description
`publisher.ts` currently fires-and-forgets publishing attempts. Failed publishes are lost. Add a retry queue in SQLite with exponential backoff so transient failures (network timeout, rate limit from social API) are automatically retried.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

### Step 1: Webhook Attempts Table
Add to `src/lib/db.ts` migrations:
```sql
CREATE TABLE IF NOT EXISTS publish_attempts (
  id TEXT PRIMARY KEY,
  scheduled_post_id TEXT,
  platform TEXT NOT NULL,
  payload TEXT NOT NULL,        -- JSON: content, media urls, etc.
  attempt_number INTEGER NOT NULL DEFAULT 1,
  next_retry_at INTEGER,        -- unixepoch, null if terminal
  status TEXT NOT NULL DEFAULT 'pending',  -- pending | success | failed | dead
  error_message TEXT,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE INDEX IF NOT EXISTS idx_publish_attempts_next_retry ON publish_attempts(next_retry_at, status);
CREATE INDEX IF NOT EXISTS idx_publish_attempts_status ON publish_attempts(status);
```

### Step 2: Retry Logic Utility
Create `src/lib/retryQueue.ts`:
```typescript
const BACKOFF_DELAYS_MS = [
  30 * 1000,       // 30 seconds
  2 * 60 * 1000,   // 2 minutes
  10 * 60 * 1000,  // 10 minutes
  60 * 60 * 1000,  // 1 hour
  // after 4 attempts: mark as 'dead'
];

export function calculateNextRetry(attemptNumber: number): number | null {
  const delayMs = BACKOFF_DELAYS_MS[attemptNumber - 1];
  if (!delayMs) return null; // no more retries → dead letter
  return Math.floor(Date.now() / 1000) + Math.floor(delayMs / 1000);
}

export function createAttempt(db, postId, platform, payload): string { /* insert row */ }
export function markSuccess(db, attemptId): void { /* update status */ }
export function markFailed(db, attemptId, error: string): void {
  // increment attempt_number, calculate next_retry_at or mark dead
}
export function getDueRetries(db): PublishAttempt[] {
  // SELECT WHERE status='pending' AND next_retry_at <= unixepoch()
}
```

### Step 3: Update Publisher
In `src/services/publisher.ts` (or equivalent):
- On publish attempt: create a `publish_attempts` row via `retryQueue.createAttempt()`
- On success: call `retryQueue.markSuccess()`
- On failure: call `retryQueue.markFailed()` — this auto-schedules the next retry

### Step 4: Scheduler Worker Integration
In `src/services/schedulerWorker.ts`, add to the poll loop:
```typescript
// Process due retries
const dueRetries = retryQueue.getDueRetries(db);
for (const attempt of dueRetries) {
  try {
    await publishContent(attempt.platform, JSON.parse(attempt.payload));
    retryQueue.markSuccess(db, attempt.id);
  } catch (err) {
    retryQueue.markFailed(db, attempt.id, err.message);
  }
}
```

### Step 5: Dead Letter Monitoring
Add `GET /api/admin/dead-letters` endpoint that returns all `status='dead'` attempts for monitoring.

### Step 6: Tests
Add `src/__tests__/lib/retryQueue.test.ts`:
- `calculateNextRetry(1)` returns ~30 seconds from now
- `calculateNextRetry(5)` returns null (dead letter)
- `getDueRetries` returns only rows with `next_retry_at <= now`
- After 4 failed `markFailed` calls, status becomes 'dead'

## Dependencies
370 (DB indexes — same migration file)

## Estimated Effort
M

## Acceptance Criteria
- [ ] `publish_attempts` table in SQLite with indexes
- [ ] Exponential backoff: 30s → 2m → 10m → 1h → dead
- [ ] `retryQueue.ts` utility with create/markSuccess/markFailed/getDueRetries
- [ ] Publisher creates attempt rows and updates on result
- [ ] Scheduler worker polls and processes due retries
- [ ] Dead-letter endpoint returns failed-final attempts
- [ ] Retry queue tests pass (no external API calls)
- [ ] All existing tests pass
