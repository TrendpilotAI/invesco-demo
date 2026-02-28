# TODO-313: Replace console.log with Pino Structured Logger

**Repo:** signal-studio
**Priority:** P1
**Effort:** M (2-4 hours)
**Status:** pending

## Description
90 console.log statements found in production code (app/, lib/, components/).
These spam production logs and may leak sensitive data (SQL queries, user data, API responses).
Replace with pino structured logger.

## Acceptance Criteria
- `pino` installed as dependency
- `lib/logger.ts` created as central logger singleton
- All console.log in app/ and lib/ replaced with logger.debug/info/warn/error
- console.log in components/ removed (UI components shouldn't log)
- Zero console.log remaining in production code paths

## Coding Prompt
```
1. Install pino:
   cd /data/workspace/projects/signal-studio && pnpm add pino pino-pretty

2. Create lib/logger.ts:
   import pino from 'pino'
   
   const logger = pino({
     level: process.env.LOG_LEVEL || 'info',
     ...(process.env.NODE_ENV === 'development' && {
       transport: { target: 'pino-pretty' }
     })
   })
   
   export default logger

3. Find all console.log in production code:
   grep -rn "console\.log" app/ lib/ components/ --include="*.ts" --include="*.tsx" | grep -v __tests__ | grep -v node_modules

4. For API routes (app/api/): replace with logger.info/debug
   For lib/ utilities: replace with logger.debug
   For components/: REMOVE (UI components shouldn't log to server)

5. For sensitive data (SQL, credentials): use logger.debug (not logged in production)
```

## Dependencies
- None (can do in parallel with 311, 312)

## Notes
AUDIT.md QUALITY-001
