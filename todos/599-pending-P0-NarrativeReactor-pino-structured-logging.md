# TODO-599: Pino Structured Logging — NarrativeReactor

**Priority:** P0 (Foundation)
**Repo:** NarrativeReactor
**Effort:** 2-3 hours
**Dependencies:** None

## Problem
30+ `console.log`/`console.error` calls scattered across services with no log levels, no JSON output, no request correlation IDs. Impossible to grep or aggregate logs in production.

## Task
Install `pino` and `pino-http`. Create `src/lib/logger.ts` singleton. Replace all console.log/error/warn calls. Add request correlation IDs to every request log.

## Acceptance Criteria
- [ ] `pino` and `pino-http` installed
- [ ] `src/lib/logger.ts` exports `logger` singleton
- [ ] `pino-http` middleware added to Express (request/response logging)
- [ ] All console.log replaced with `logger.info/warn/error`
- [ ] Sensitive fields (api_key, token, password) redacted in logs via pino serializers
- [ ] Request ID header (`x-request-id`) generated and included in all log lines
- [ ] LOG_LEVEL env var controls log level (default: 'info')

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor:
1. Run: yarn add pino pino-http
2. Create src/lib/logger.ts:
   import pino from 'pino';
   export const logger = pino({
     level: process.env.LOG_LEVEL || 'info',
     serializers: { req: (req) => ({ method: req.method, url: req.url, id: req.id }), err: pino.stdSerializers.err },
     redact: ['req.headers["x-api-key"]', 'req.headers.authorization', '*.password', '*.token']
   });
3. Add pino-http middleware to src/index.ts before routes
4. Run: grep -r "console\." src/services/ src/flows/ src/middleware/ --include="*.ts" -l
5. For each file, replace console.log → logger.info, console.error → logger.error, console.warn → logger.warn
6. Import logger from '../lib/logger' in each file
7. Run: npm test to verify tests pass
```
