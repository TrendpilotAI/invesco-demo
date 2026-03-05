# TODO-587: Replace 204 console.* calls with pino structured logger

**Repo:** signal-studio
**Priority:** P0
**Effort:** M (half day)
**Status:** pending

## Problem
204 raw `console.log/error/warn` calls found in `lib/` and `app/api/`. In a financial platform:
- Unstructured logs can't be queried or filtered in Railway's log drain
- May leak sensitive data: connection strings, SQL queries, user IDs, Oracle wallet paths
- No log levels → debug noise in production

## Task
1. Install `pino` and `pino-pretty` (dev dependency)
2. Create `lib/logger.ts` singleton with appropriate log levels per env
3. Run `grep -rn "console\." lib/ app/api/` to find all 204 callsites
4. Migrate to `logger.info()`, `logger.error()`, `logger.debug()` etc.
5. Ensure sensitive fields (passwords, wallet paths) are redacted

## Coding Prompt
```
In /data/workspace/projects/signal-studio:
1. Run: cd /data/workspace/projects/signal-studio && npm install pino pino-pretty
2. Create lib/logger.ts:
   import pino from 'pino'
   const logger = pino({
     level: process.env.LOG_LEVEL || (process.env.NODE_ENV === 'production' ? 'info' : 'debug'),
     redact: ['password', 'connectionString', 'walletPassword', 'token', 'secret'],
   })
   export default logger
3. Find all console.* calls: grep -rn "console\." lib/ app/api/ --include="*.ts"
4. Replace each: console.log → logger.info, console.error → logger.error, console.warn → logger.warn
5. For oracle-service.ts specifically, ensure wallet path and connection details are at debug level
```

## Acceptance Criteria
- [ ] `lib/logger.ts` created with pino
- [ ] Zero `console.log` calls in `lib/` and `app/api/`
- [ ] Sensitive fields (password, connectionString) are redacted in log output
- [ ] `npm run build` succeeds

## Dependencies
- TODO-585 (fix ignoreBuildErrors first to surface any type issues)
