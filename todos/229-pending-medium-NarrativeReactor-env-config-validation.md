# 229 · NarrativeReactor · Environment Config Validation & Secrets Management

**Status:** pending  
**Priority:** medium  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

NarrativeReactor uses scattered `process.env.X` calls throughout 30+ services with no validation at startup. Missing env vars cause silent failures or runtime errors deep in flows. Add Zod-based env validation at startup + a secrets checklist for deployment.

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/src/:

1. Install: npm i zod

2. Create src/lib/env.ts:
   import { z } from 'zod';

   const EnvSchema = z.object({
     // Core
     NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
     NR_PORT: z.string().default('3401'),
     API_KEY: z.string().min(16, 'API_KEY must be at least 16 chars'),
     JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 chars').optional(),
     
     // LLMs
     GOOGLE_API_KEY: z.string().optional(),
     ANTHROPIC_API_KEY: z.string().optional(),
     FAL_API_KEY: z.string().optional(),
     
     // Social
     BLOTATO_API_KEY: z.string().optional(),
     
     // Infrastructure
     REDIS_URL: z.string().url().optional(),
     
     // Firebase/Vertex
     GOOGLE_CLOUD_PROJECT: z.string().optional(),
   });

   export const env = EnvSchema.parse(process.env);
   export type Env = z.infer<typeof EnvSchema>;

3. Import env at the top of src/index.ts (before other imports) so startup fails fast.

4. Replace all direct process.env.X usages in services with import { env } from '../lib/env'
   (can be done progressively — at minimum update the 5 most critical services)

5. Create .env.example with all required/optional vars documented with descriptions.

6. Create docs/deployment/env-vars.md with:
   - Full variable reference table
   - Which are required vs optional
   - Where to get each value
   - Security recommendations (rotation schedule, min entropy)

7. Add startup validation log: "✅ Environment validated: 8/12 optional vars set"
```

---

## Dependencies

- None

## Effort Estimate

3–4 hours

## Acceptance Criteria

- [ ] App fails fast at startup with clear error if required vars missing
- [ ] All env vars documented in .env.example
- [ ] Zod validation catches type mismatches (e.g., invalid URL format)
- [ ] `env` object used in at least 10 services (replacing raw process.env)
- [ ] docs/deployment/env-vars.md committed
