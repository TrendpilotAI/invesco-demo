# 321 · NarrativeReactor — Error Monitoring (Sentry)

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Effort:** ~3h  

---

## Task Description

NarrativeReactor runs 32 services and orchestrates multiple external APIs (Fal.ai, Fish Audio, Blotato, Vertex AI). There is zero error monitoring — failures are invisible until users report them. This task integrates Sentry for Node.js with source maps, performance tracing, and alerting.

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/.

## Step 1 — Install Sentry
```bash
pnpm add @sentry/node @sentry/profiling-node
```

## Step 2 — Create src/lib/sentry.ts
```typescript
import * as Sentry from '@sentry/node';
import { nodeProfilingIntegration } from '@sentry/profiling-node';

export function initSentry() {
  if (!process.env.SENTRY_DSN) {
    console.warn('[Sentry] SENTRY_DSN not set — error monitoring disabled');
    return;
  }

  Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV ?? 'development',
    release: process.env.npm_package_version,
    integrations: [
      nodeProfilingIntegration(),
    ],
    tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    profilesSampleRate: 0.1,
    beforeSend(event) {
      // Scrub sensitive data
      if (event.request?.headers) {
        delete event.request.headers['x-api-key'];
        delete event.request.headers['authorization'];
      }
      return event;
    },
  });
}
```

## Step 3 — Initialize early in src/index.ts
```typescript
import { initSentry } from './lib/sentry';
import * as Sentry from '@sentry/node';

// Must be called before anything else
initSentry();

// ... existing app setup ...

// Sentry request handler (before routes)
app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

// ... routes ...

// Sentry error handler (after routes, before custom error handler)
app.use(Sentry.Handlers.errorHandler());
```

## Step 4 — Custom error handler with Sentry
Add to src/middleware/errorHandler.ts:
```typescript
import { Request, Response, NextFunction } from 'express';
import * as Sentry from '@sentry/node';

export interface AppError extends Error {
  statusCode?: number;
  isOperational?: boolean;
}

export function errorHandler(
  err: AppError,
  req: Request,
  res: Response,
  _next: NextFunction
) {
  const statusCode = err.statusCode ?? 500;
  
  // Only capture unexpected errors (not operational 4xx)
  if (statusCode >= 500 || !err.isOperational) {
    Sentry.captureException(err, {
      extra: {
        path: req.path,
        method: req.method,
        userId: (req as any).userId,
      },
    });
  }

  console.error(`[${statusCode}] ${req.method} ${req.path}:`, err.message);

  res.status(statusCode).json({
    error: statusCode >= 500 ? 'Internal server error' : err.message,
    ...(process.env.NODE_ENV !== 'production' && { stack: err.stack }),
  });
}
```

## Step 5 — Service-level error capture
In services that call external APIs (falAi, fishAudio, blotatoPublisher), wrap calls:
```typescript
import * as Sentry from '@sentry/node';

async function callExternalApi() {
  return await Sentry.startSpan(
    { name: 'fal-ai.generate-video', op: 'http.client' },
    async () => {
      // ... actual API call
    }
  );
}
```

## Step 6 — Update env.ts and .env.example
Add optional `SENTRY_DSN` (warn if missing, don't throw).

Add to .env.example:
```
# Error monitoring (get DSN from sentry.io)
SENTRY_DSN=
```

## Step 7 — Source maps for production
Update tsconfig.json:
```json
{
  "compilerOptions": {
    "sourceMap": true,
    "inlineSources": true,
    "sourceRoot": "/"
  }
}
```

Add to package.json scripts:
```json
"sentry:upload": "sentry-cli releases files $npm_package_version upload-sourcemaps ./dist --rewrite"
```
```

## Dependencies
- 316 (security hardening — error handler shouldn't leak stack traces in prod)
- 317 (production deployment where Sentry is most valuable)

## Acceptance Criteria
- [ ] `@sentry/node` initialized at startup when SENTRY_DSN is set
- [ ] App starts normally and logs a warning when SENTRY_DSN is absent
- [ ] Unhandled exceptions in routes are captured by Sentry
- [ ] API key headers are scrubbed from Sentry events (beforeSend)
- [ ] Custom error handler returns `{ error: "..." }` JSON (no stack in prod)
- [ ] Source maps enabled in tsconfig
- [ ] `.env.example` has SENTRY_DSN entry
- [ ] `pnpm build && pnpm test` pass
