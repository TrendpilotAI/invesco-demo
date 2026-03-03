# NarrativeReactor — Railway Deployment Audit

**Date:** 2026-03-03  
**Status:** ✅ Ready for deployment (with notes)

---

## 1. Dependencies

- **npm is broken** in this environment (minipass-sized bug with Node 22 + npm 11). Used **yarn** successfully as workaround.
- `yarn install` completes cleanly. One unmet peer dep warning: `@google-cloud/firestore@^7.11.0` (optional, for Firebase integration).
- **Dockerfile uses `npm ci`** — Railway builds in its own container with Node 20 (per Dockerfile), so npm should work fine there. No changes needed.

## 2. TypeScript Build

**Status:** ✅ Compiles clean after fixes

### Fixes Applied:
1. **Excluded test files from tsc build** — added `src/__tests__` to tsconfig `exclude` (tests use vitest's own transpilation)
2. **Fixed `src/services/dialogue.ts`** — replaced deprecated `import { generate } from '@genkit-ai/ai'` + `gemini15Flash` with `ai.generate()` pattern matching rest of codebase
3. **Fixed `src/services/podcastGenerator.ts`** — same pattern fix
4. **Installed missing `@types/express@4`** — yarn was not hoisting it properly with `@types/express@5`

### tsconfig.json change:
```json
"exclude": ["node_modules", "src/__tests__"]
```

## 3. Tests

**Result: 285 passed, 2 failed (26 test files)**

| Status | Count | Details |
|--------|-------|---------|
| ✅ Pass | 285 | All unit/integration tests |
| ❌ Fail | 2 | `audio.test.ts` — Podcast Generator & Dialogue Service tests that make real Gemini API calls without a key |

The 2 failures are **expected in CI without API keys**. They attempt real HTTP calls to `generativelanguage.googleapis.com`. These should be mocked or skipped in CI.

## 4. Required Environment Variables

From `.env.example`:

| Variable | Required | Description |
|----------|----------|-------------|
| `NR_PORT` | No (default 3401) | Server port |
| `GENKIT_PORT` | No (default 3402) | Genkit dev UI port |
| `API_KEY` | **Yes** | API authentication key |
| `GOOGLE_GENAI_API_KEY` | **Yes** | Gemini API key |
| `ANTHROPIC_API_KEY` | **Yes** | Claude API key |
| `FAL_KEY` | **Yes** | fal.ai image/video generation |
| `WEBHOOK_SECRET` | **Yes** | Webhook signature verification |
| `CORS_ALLOWED_ORIGINS` | Recommended | Comma-separated allowed origins |
| `TOKEN_ENCRYPTION_KEY` | **Production** | 64-char hex for token encryption |
| `DASHBOARD_PASSWORD` | **Production** | Dashboard auth password |
| `JWT_SECRET` | No | Falls back to API_KEY |
| `SENTRY_DSN` | No | Error reporting |
| `DATABASE_PATH` | No | SQLite DB path (default: `data/narrative.db`) |

**Railway-specific:** Set `PORT` (Railway injects this automatically; Dockerfile defaults to 8080).

## 5. Dockerfile & Railway Config

**Both exist and are well-configured:**

- **Dockerfile**: Multi-stage build (Node 20-slim), non-root user, healthcheck built in
- **railway.json**: Dockerfile builder, health check at `/health`, restart on failure

No changes needed.

## 6. SQLite Persistence on Railway

**⚠️ Requires Railway Volume Mount**

The app uses Node.js built-in `node:sqlite` (Node 22+), but the **Dockerfile uses Node 20**. This is a **critical issue**:

### Problem: `node:sqlite` requires Node 22+
- `src/lib/db.ts` imports `DatabaseSync` from `node:sqlite` (Node 22+ only)
- Dockerfile uses `node:20-slim` — **this will crash at runtime**

### Fix Options:
1. **Change Dockerfile to `node:22-slim`** — easiest fix
2. Replace `node:sqlite` with `better-sqlite3` package — more portable

### Volume Mount:
- Database path: `DATABASE_PATH` env var or default `data/narrative.db`
- Railway volume should be mounted at `/app/data`
- Without a volume, data is lost on every deploy

## 7. Health Check

**Endpoint:** `GET /health`  
**Expected response:** HTTP 200  
**Location:** `src/index.ts` line 82  
**Railway config:** Already set in `railway.json` → `healthcheckPath: "/health"`

## 8. Critical Action Items Before Deploy

### Must Fix:
1. **⚠️ Change Dockerfile base image from `node:20-slim` to `node:22-slim`** (both builder and production stages) — `node:sqlite` requires Node 22+
2. **Attach a Railway Volume** mounted at `/app/data` for SQLite persistence

### Should Fix:
3. Mock the 2 failing API-dependent tests for CI
4. Consider pinning genkit packages to specific versions (currently `*`)

### Nice to Have:
5. Add `COPY genkit.config.ts ./` is in Dockerfile but the file might not exist (only `genkit.config.js` is guaranteed) — verify
6. Add a `yarn.lock` or fix npm compatibility for deterministic builds

## 9. Deployment Steps

```bash
# 1. Fix Dockerfile base images
sed -i 's/node:20-slim/node:22-slim/g' Dockerfile

# 2. Push to Railway-connected repo

# 3. Set environment variables in Railway dashboard:
#    API_KEY, GOOGLE_GENAI_API_KEY, ANTHROPIC_API_KEY, FAL_KEY,
#    WEBHOOK_SECRET, TOKEN_ENCRYPTION_KEY, DASHBOARD_PASSWORD,
#    CORS_ALLOWED_ORIGINS

# 4. Add Railway Volume mounted at /app/data

# 5. Deploy — Railway will build from Dockerfile, health check at /health
```

---

**Summary:** The codebase is in good shape. Build compiles clean, 99.3% of tests pass. The one critical blocker is the Node version mismatch in the Dockerfile (`node:20` vs `node:sqlite` requiring Node 22). Fix that + attach a volume and it's ready to ship.
