# TODO 101 — Add API Authentication Middleware (P1)

**Repo:** signal-studio-templates  
**Priority:** P1 — Before any production deployment  
**Effort:** M (1 day)  
**Status:** pending

---

## Problem

`createTemplateRouter` exposes template execution with no authentication. The `/execute` endpoint runs SQL queries. The `/customize` endpoint accepts arbitrary SQL overrides via `req.body`.

---

## Autonomous Coding Prompt

```
Add authentication and input validation to /data/workspace/projects/signal-studio-templates/api/templates.ts

CHANGES:

1. Add auth middleware parameter to createTemplateRouter:
   export function createTemplateRouter(
     dataProvider: DataProvider,
     aiProvider?: AIProvider,
     options?: { authMiddleware?: RequestHandler }
   ): Router

   If authMiddleware provided, apply it to all routes:
   router.use(options.authMiddleware)

2. Whitelist allowed fields in customize endpoint:
   const ALLOWED_CUSTOMIZE_FIELDS = ['name', 'description', 'parameters', 'defaultConfig', 'outputSchema', 'tags'];
   const safeOverrides = Object.fromEntries(
     Object.entries(req.body).filter(([k]) => ALLOWED_CUSTOMIZE_FIELDS.includes(k))
   );
   const customized = engine.customize(req.params.id, safeOverrides);
   
   Never allow: sqlTemplate, visualBuilderNodes, requiredDataSources overrides from API callers.

3. Add request size limit to execute endpoint:
   Validate req.body.parameters is a plain object (not array, not string).
   Reject if parameter count > 20.

4. Add tests in __tests__/api.test.ts:
   - Test that routes return 401 when authMiddleware rejects
   - Test that customize rejects sqlTemplate override
   - Test parameter count limit

5. Update README.md with auth setup instructions.
```

## Acceptance Criteria
- [ ] authMiddleware option accepted and applied
- [ ] customize endpoint rejects sqlTemplate override
- [ ] Tests pass

## Dependencies
- TODO 100 (fix SQL bug first)
