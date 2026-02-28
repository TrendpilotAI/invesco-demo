# 320 — Production Integration: npm Publish + Postgres Analytical DB + OpenAI Talking Points

**Priority:** MEDIUM  
**Effort:** M  
**Status:** pending

---

## Task Description

Three production wiring tasks that should ship together as one integration sprint:
1. Publish `@forwardlane/signal-studio-templates` to Bitbucket/npm registry so Signal Studio (Next.js) can install it as a proper dependency
2. Wire `TemplateEngine.DataProvider` to the actual Postgres Analytical DB (Railway)
3. Wire `talkingPointsPrompt` through OpenAI API with structured output — currently the prompt exists but is never called

---

## Autonomous Coding Prompt

```
REPO: /data/workspace/projects/signal-studio-templates

TASK: Wire up npm publishing, real Postgres DataProvider, and OpenAI talking points.

PART 1 — npm Package Setup:

1. Update package.json:
   - name: "@forwardlane/signal-studio-templates"
   - version: "1.0.0"
   - main: "dist/index.js"
   - types: "dist/index.d.ts"
   - files: ["dist"]
   - publishConfig: { "registry": "https://registry.npmjs.org", "access": "public" }
     (or Bitbucket registry URL if private)

2. Ensure pnpm build generates dist/ with:
   - CJS output (require-compatible)
   - Type declarations (.d.ts)
   - Source maps

3. Add .npmignore:
   src/, tests/, *.test.ts, tsconfig.json, .husky/, node_modules/

4. Test publish dry-run: pnpm publish --dry-run --no-git-checks
   Verify dist/ contains all expected exports.

PART 2 — Postgres Analytical DataProvider:

5. Create src/providers/PostgresDataProvider.ts:
   - Implement DataProvider interface
   - Use node-postgres (pg) connection pool
   - Read connection from process.env.ANALYTICAL_DATABASE_URL
   - Implement execute(sql: string, values: unknown[]): Promise<Row[]>
   - Handle connection errors, query timeouts (30s default)
   - Export createPostgresDataProvider(config?) factory

   Connection string for Railway Postgres Analytical:
   Use ANALYTICAL_DATABASE_URL env var — do NOT hardcode credentials.
   (The actual URL is in TOOLS.md under Railway ForwardLane Signal Studio Project)

6. Update src/index.ts to export PostgresDataProvider
7. Update README: document ANALYTICAL_DATABASE_URL env var requirement

PART 3 — OpenAI Talking Points:

8. Install: pnpm add openai

9. Create src/providers/OpenAIProvider.ts:
   - Implement AIProvider interface (whatever is defined for talkingPointsPrompt)
   - Use openai SDK: new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
   - Call chat.completions.create with:
     * model: "gpt-4o-mini" (cost-effective for talking points)
     * response_format: { type: "json_object" }
     * system: "You are a financial advisor assistant. Return structured JSON."
     * user: the talkingPointsPrompt string from the template
   - Return parsed JSON as TalkingPoints type
   - Graceful degradation: if OPENAI_API_KEY not set, return null (don't throw)
   - Timeout: 15s
   - Export createOpenAIProvider() factory

10. Update TemplateEngine to use both providers:
    - Accept DataProvider and AIProvider in constructor/factory
    - Execute talking points in parallel with SQL query (Promise.all)

11. Export a createProductionTemplateEngine() convenience factory that wires
    PostgresDataProvider + OpenAIProvider together using env vars.

12. Update README with OPENAI_API_KEY env var docs.

ACCEPTANCE: pnpm publish --dry-run succeeds. 
Integration test (with test DB creds) runs a template and returns rows + talkingPoints.
```

---

## Dependencies

- **315** (parameterized queries — DataProvider must use them)
- **316** (JWT auth — production engine needs auth)
- **317** (CI — publish step in pipeline)
- **318** (tests — DataProvider should have integration tests)
- **319** (types — DataProvider/AIProvider interfaces should be strict)

---

## Acceptance Criteria

- [ ] `package.json` has correct scope, version, and publishConfig
- [ ] `pnpm publish --dry-run` succeeds, dist/ contains JS + `.d.ts` files
- [ ] `PostgresDataProvider` created, uses connection pool, reads from `ANALYTICAL_DATABASE_URL`
- [ ] `OpenAIProvider` created, returns structured JSON talking points
- [ ] `createProductionTemplateEngine()` factory exported from `src/index.ts`
- [ ] Graceful degradation when `OPENAI_API_KEY` not set (returns `null` talkingPoints, no crash)
- [ ] README documents all required env vars
