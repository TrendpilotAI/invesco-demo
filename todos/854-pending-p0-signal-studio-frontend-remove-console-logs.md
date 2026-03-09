# Remove console.log from Production API Routes

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** S (30 min)

## Description
`app/api/chat/ai-sdk/route.ts` logs full request body and message history to stdout (lines 45-49). This exposes potentially sensitive financial data and user chat content in production logs.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend:
1. Find all console.log in API routes: grep -rn "console.log" app/api/ --include="*.ts"
2. Create lib/logger.ts:
   const isDev = process.env.NODE_ENV === 'development'
   export const logger = {
     debug: (...args: unknown[]) => isDev && console.log('[DEBUG]', ...args),
     info: (...args: unknown[]) => console.log('[INFO]', ...args),
     warn: (...args: unknown[]) => console.warn('[WARN]', ...args),
     error: (...args: unknown[]) => console.error('[ERROR]', ...args),
   }
3. In app/api/chat/ai-sdk/route.ts: Remove lines 45-49 (console.log of body/messages/model)
4. In app/api/chat/insights/route.ts: Replace console.log with logger.debug (debug-only)
5. In lib/oracle-service.ts: Replace verbose console.log with logger.info/error
6. Commit: "security: remove console.log leaking request data, add structured logger"
```

## Acceptance Criteria
- [ ] No `console.log` of request bodies or message content in API routes
- [ ] `lib/logger.ts` created
- [ ] Build passes

## Dependencies
None
