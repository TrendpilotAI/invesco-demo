# 374 — Replace console.log with Structured Logger (pino/winston)

## Task Description
Multiple production code paths use `console.log` including one in `src/lib/fal.ts` that may log full API response JSON (potential data leak). Replace all production `console.log` calls with a structured logger gated by `LOG_LEVEL` env var.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

**Step 1: Install pino**
```bash
npm install pino pino-pretty
npm install --save-dev @types/pino  # if needed
```

**Step 2: Create `src/lib/logger.ts`**
```typescript
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || (process.env.NODE_ENV === 'production' ? 'info' : 'debug'),
  transport: process.env.NODE_ENV !== 'production'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
  redact: {
    paths: ['*.token', '*.access_token', '*.refresh_token', '*.password', '*.key'],
    censor: '[REDACTED]'
  }
});
```

**Step 3: Replace all console.log in production code paths**

Files to fix (from AUDIT.md findings):
- `src/index.ts` lines 132, 134 — server start messages
- `src/services/schedulerWorker.ts` lines 34, 38, 61, 74 — scheduler events
- `src/lib/db.ts` lines 123, 244, 313 — migration/import events
- `src/lib/fal.ts` lines 26, 31, 85 — **PRIORITY: line 31 logs full JSON response**

Replace pattern:
- `console.log('message', data)` → `logger.info({ data }, 'message')`
- `console.error('message', err)` → `logger.error({ err }, 'message')`
- `console.warn('message')` → `logger.warn('message')`

**Step 4: Gate Fal.ai debug logging**
```typescript
// fal.ts line 31 equivalent
if (logger.level === 'debug') {
  logger.debug({ resultKeys: Object.keys(result) }, '[Fal.ai] Image result received');
  // Do NOT log full result — log only keys or metadata
}
```

**Step 5: Run a full grep to catch any missed console.log in src/**
```bash
grep -rn "console\.log\|console\.error\|console\.warn" src/ --include="*.ts" | grep -v "__tests__"
```
Replace any remaining occurrences.

**Step 6: Do NOT replace console.log in test files** — those are fine.

Run `npm test` to confirm all tests pass.

## Dependencies
None (can run in parallel with other tasks)

## Estimated Effort
M

## Acceptance Criteria
- [ ] `src/lib/logger.ts` created with pino logger
- [ ] Zero `console.log/error/warn` in `src/` outside of `__tests__/`
- [ ] Fal.ai debug logging (`fal.ts:31`) no longer logs full JSON response
- [ ] Logger respects `LOG_LEVEL` env var
- [ ] Sensitive fields (tokens, keys, passwords) are redacted via pino `redact`
- [ ] `NODE_ENV=development` shows pretty-printed logs
- [ ] All existing tests pass
- [ ] `LOG_LEVEL` documented in README environment variables section
