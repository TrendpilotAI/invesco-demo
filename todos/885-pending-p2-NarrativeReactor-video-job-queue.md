# TODO-885: Async Video Job Queue

**Repo**: NarrativeReactor  
**Priority**: P2 — Performance  
**Effort**: 1 day  
**Status**: Pending  

## Problem

Video generation via Fal.ai blocks the HTTP response thread for 30-120 seconds. This:
1. Ties up an Express worker for minutes
2. Risks HTTP timeouts (Railway default: 60s)
3. Provides terrible UX (spinning indefinitely)

## Solution

SQLite-backed job queue with polling endpoint:

```typescript
// src/services/videoQueue.ts (new)
import { getDb } from '../lib/db';

export type VideoJobStatus = 'pending' | 'processing' | 'done' | 'failed';

export interface VideoJob {
  id: string;
  tenant_id: string;
  input: string;  // JSON
  status: VideoJobStatus;
  result: string | null;  // JSON
  error: string | null;
  created_at: string;
  completed_at: string | null;
}

export function enqueueVideoJob(tenantId: string, input: unknown): string {
  const db = getDb();
  const id = crypto.randomUUID();
  db.prepare(`
    INSERT INTO video_jobs (id, tenant_id, input, status, created_at)
    VALUES (?, ?, ?, 'pending', datetime('now'))
  `).run(id, tenantId, JSON.stringify(input));
  return id;
}

export function getVideoJob(id: string): VideoJob | null {
  const db = getDb();
  return db.prepare('SELECT * FROM video_jobs WHERE id = ?').get(id) as VideoJob | null;
}

export async function processVideoJobs(): Promise<void> {
  const db = getDb();
  const pending = db.prepare(`
    SELECT * FROM video_jobs WHERE status = 'pending' LIMIT 3
  `).all() as VideoJob[];
  
  for (const job of pending) {
    db.prepare('UPDATE video_jobs SET status = ? WHERE id = ?').run('processing', job.id);
    try {
      const result = await generateVideo(JSON.parse(job.input));
      db.prepare(`
        UPDATE video_jobs SET status='done', result=?, completed_at=datetime('now') WHERE id=?
      `).run(JSON.stringify(result), job.id);
    } catch (err) {
      db.prepare(`
        UPDATE video_jobs SET status='failed', error=? WHERE id=?
      `).run(String(err), job.id);
    }
  }
}
```

Routes:
```typescript
// POST /api/video/generate → returns { jobId }
// GET  /api/video/jobs/:id → returns job status + result when done
```

Worker: Add `setInterval(processVideoJobs, 5000)` to schedulerWorker.ts

## Files to Change

- `src/services/videoQueue.ts` — new queue service
- `src/lib/db.ts` — add `video_jobs` table migration
- `src/routes/pipeline.ts` — replace sync video endpoint with async version
- `src/services/schedulerWorker.ts` — add video job processor interval
- `src/__tests__/services/videoQueue.test.ts` — new tests

## Acceptance Criteria

- [ ] `POST /api/video/generate` returns `{ jobId }` immediately (< 100ms)
- [ ] `GET /api/video/jobs/:id` returns status: pending/processing/done/failed
- [ ] When done, job result contains video URL
- [ ] Worker processes pending jobs every 5 seconds
- [ ] Max 3 concurrent video jobs (configurable)
- [ ] Failed jobs include error message
- [ ] Jobs are tenant-scoped (can't poll other tenants' jobs)
