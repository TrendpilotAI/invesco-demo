# TODO-353: Replace console.log with Pino Structured Logger

**Priority:** P0
**Effort:** M
**Repo:** signal-studio
**Status:** pending

## Description
94 `console.log` statements found in app/, lib/, components/. This spams production logs and risks leaking sensitive financial data (query results, user info, API responses).

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Install pino: pnpm add pino pino-pretty

2. Create /data/workspace/projects/signal-studio/lib/logger.ts:
```typescript
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || (process.env.NODE_ENV === 'production' ? 'info' : 'debug'),
  transport: process.env.NODE_ENV !== 'production' ? {
    target: 'pino-pretty',
    options: { colorize: true }
  } : undefined,
})

export default logger
export const { info, warn, error, debug } = logger
```

3. Find all console.log in server-side code (app/api/, lib/):
   grep -rn "console\.log" app/api/ lib/ --include="*.ts" --include="*.tsx"
   
4. Replace each with appropriate logger call:
   - console.log('msg', data) → logger.info({ data }, 'msg')
   - console.error('err', e) → logger.error({ err: e }, 'msg')
   - console.warn('msg') → logger.warn('msg')
   
5. For client-side console.logs (components/), remove debug ones, keep only critical error logging

6. Run pnpm build and verify no issues

7. Commit: "feat(logging): replace 94 console.log with pino structured logger"
```

## Dependencies
None

## Acceptance Criteria
- `grep -rn "console\.log" app/api/ lib/` returns 0 results
- `lib/logger.ts` exists and exports pino instance
- `pnpm build` succeeds
- Production logs are structured JSON
