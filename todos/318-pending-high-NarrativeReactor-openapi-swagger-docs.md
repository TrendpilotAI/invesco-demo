# 318 · NarrativeReactor — OpenAPI / Swagger Documentation

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Effort:** ~5h  

---

## Task Description

No OpenAPI spec exists for the 32-service API. External integrators, the web-ui team, and future agents have no contract to code against. This task generates an OpenAPI 3.1 spec and hosts it via Swagger UI at `/docs`.

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/.

## Step 1 — Install dependencies
```bash
pnpm add swagger-ui-express swagger-jsdoc
pnpm add -D @types/swagger-ui-express @types/swagger-jsdoc
```

## Step 2 — Create src/lib/openapi.ts
```typescript
import swaggerJsdoc from 'swagger-jsdoc';

export const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: '3.1.0',
    info: {
      title: 'NarrativeReactor API',
      version: '1.0.0',
      description: 'AI-powered content generation platform — video, TTS, social publishing, campaigns, brand voice, and more.',
    },
    servers: [
      { url: 'http://localhost:3000', description: 'Local dev' },
      { url: 'https://your-railway-domain.railway.app', description: 'Production' },
    ],
    components: {
      securitySchemes: {
        ApiKeyAuth: {
          type: 'apiKey',
          in: 'header',
          name: 'X-API-Key',
        },
      },
    },
    security: [{ ApiKeyAuth: [] }],
  },
  apis: ['./src/routes/**/*.ts', './src/flows/**/*.ts'],
});
```

## Step 3 — Mount Swagger UI in src/index.ts
```typescript
import swaggerUi from 'swagger-ui-express';
import { swaggerSpec } from './lib/openapi';

// Before API routes, no auth required for docs
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
app.get('/docs.json', (_req, res) => res.json(swaggerSpec));
```

## Step 4 — Add JSDoc annotations to all route files
For each file in src/routes/:
- Add `@openapi` JSDoc blocks on every route handler
- Include: summary, description, tags, parameters, requestBody, responses
- Example for a content generation endpoint:
```typescript
/**
 * @openapi
 * /api/content/generate:
 *   post:
 *     tags: [Content]
 *     summary: Generate AI content
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [prompt, brandId]
 *             properties:
 *               prompt: { type: string }
 *               brandId: { type: string }
 *               format: { type: string, enum: [blog, social, video-script] }
 *     responses:
 *       200:
 *         description: Generated content
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 content: { type: string }
 *                 tokens: { type: integer }
 *       401:
 *         description: Invalid API key
 *       429:
 *         description: Rate limit exceeded
 */
```

Cover ALL routes in:
- src/routes/index.ts
- src/routes/pipeline.ts
- src/routes/webhooks.ts

## Step 5 — Export spec as static file
Add to package.json scripts:
```json
"docs:export": "node -e \"const s=require('./dist/lib/openapi'); require('fs').writeFileSync('docs/openapi.json', JSON.stringify(s.swaggerSpec, null, 2))\""
```

## Step 6 — Test
Write tests/api/openapi.test.ts:
- GET /docs returns 200 with HTML (Swagger UI)
- GET /docs.json returns valid JSON with openapi version field
```

## Dependencies
- 315 (README references docs URL)
- 317 (server must be runnable to verify /docs endpoint)

## Acceptance Criteria
- [ ] `GET /docs` returns Swagger UI HTML (200)
- [ ] `GET /docs.json` returns valid OpenAPI 3.1 JSON
- [ ] All routes in src/routes/ have `@openapi` annotations
- [ ] Spec includes authentication schema (X-API-Key)
- [ ] At least 15 routes documented with request/response schemas
- [ ] `pnpm build && pnpm test` pass
