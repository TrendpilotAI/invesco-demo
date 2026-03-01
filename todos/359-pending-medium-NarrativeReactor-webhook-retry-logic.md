# 359 · NarrativeReactor — Webhook Retry Logic for Failed Publishes

**Priority:** medium  
**Effort:** M (1–3 days)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

The `blotatoPublisher` service sends posts to Blotato's publish API but has no retry logic. Transient failures (5xx, network timeouts) silently fail. Implement exponential-backoff retry with a delivery log so failed webhooks can be replayed or alerted on.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/src/services/:

1. Create src/lib/retryFetch.ts:

export interface RetryOptions {
  maxAttempts?: number;   // default 3
  baseDelayMs?: number;   // default 1000
  retryOn?: number[];     // HTTP status codes to retry, default [429, 500, 502, 503, 504]
}

export async function retryFetch(
  url: string,
  init: RequestInit,
  opts: RetryOptions = {}
): Promise<Response> {
  const { maxAttempts = 3, baseDelayMs = 1000, retryOn = [429, 500, 502, 503, 504] } = opts;
  let lastError: Error | undefined;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const res = await fetch(url, init);
      if (retryOn.includes(res.status) && attempt < maxAttempts) {
        const delay = baseDelayMs * Math.pow(2, attempt - 1);
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      return res;
    } catch (err) {
      lastError = err as Error;
      if (attempt < maxAttempts) {
        const delay = baseDelayMs * Math.pow(2, attempt - 1);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }
  throw lastError ?? new Error('retryFetch exhausted all attempts');
}

2. Update blotatoPublisher.ts (and any other publisher services):
   - Replace bare fetch() calls with retryFetch()
   - Log each attempt with attempt number and delay

3. Create src/lib/webhookDeliveryLog.ts — append-only log using SQLite:

interface DeliveryRecord {
  id: string;
  url: string;
  payload: string;
  attempts: number;
  lastStatus: number | null;
  success: boolean;
  createdAt: string;
  updatedAt: string;
}

- recordAttempt(url, payload, attempt, status): void
- getFailures(since?: Date): DeliveryRecord[]
- markSuccess(id): void

Use the existing SQLite connection (node:sqlite) already in the project.

4. Wire deliveryLog into blotatoPublisher.ts:
   - On each retry attempt, call recordAttempt()
   - On success, call markSuccess()
   - On final failure, log error + leave record as failed for alerting

5. Add GET /api/webhooks/failures endpoint (admin only) that returns getFailures().

6. Write tests in tests/unit/retryFetch.test.ts:
   - Mock fetch with first 2 calls returning 503, third returning 200 → resolves
   - Mock fetch always returning 503 → throws after maxAttempts
   - Test exponential delay values
```

---

## Dependencies

- SQLite already in project (per TODO.md completed items)
- blotatoPublisher.ts must be locatable

## Acceptance Criteria

- [ ] `retryFetch` implements exponential backoff with configurable attempts
- [ ] `blotatoPublisher` uses `retryFetch` instead of bare `fetch`
- [ ] Delivery log persists attempts to SQLite
- [ ] Unit tests for retry logic pass
- [ ] Failed deliveries queryable via admin endpoint
