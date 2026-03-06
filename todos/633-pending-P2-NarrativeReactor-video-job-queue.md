# TODO-633: Async Video Job Queue

**Repo:** NarrativeReactor  
**Priority:** P2  
**Effort:** 1 day  
**Status:** pending

## Description
Video generation currently blocks the HTTP thread for minutes. Implement a SQLite-backed job queue that processes video jobs asynchronously and returns a job ID for polling.

## Acceptance Criteria
- [ ] POST /api/video/generate returns immediately with { jobId, status: "queued" }
- [ ] GET /api/video/jobs/:id returns current status + result URL when done
- [ ] Background worker polls queue every 10s and processes jobs
- [ ] Failed jobs retry up to 3 times with exponential backoff
- [ ] Completed jobs cleaned up after 24h

## Coding Prompt
```
In /data/workspace/projects/NarrativeReactor:

1. Create src/services/videoQueue.ts
   - Table: video_jobs(id, status, payload, result, attempts, created_at, updated_at, error)
   - Methods: enqueue(payload), getJob(id), processNext(), markComplete(id, result), markFailed(id, error)

2. Create src/workers/videoWorker.ts
   - setInterval every 10s to call videoQueue.processNext()
   - On job: call existing videoStitcher/fal.ai pipeline
   - Retry logic: if attempts < 3, re-enqueue with delay

3. Modify video generation route in src/index.ts:
   - Instead of await-ing video generation, call videoQueue.enqueue(payload)
   - Return { jobId, status: 'queued', pollUrl: '/api/video/jobs/' + jobId }

4. Add GET /api/video/jobs/:id endpoint

5. Start videoWorker in src/index.ts on app startup

6. Add tests for queue operations
```

## Dependencies
- TODO-632 (DB singleton) — videoQueue should use shared db
