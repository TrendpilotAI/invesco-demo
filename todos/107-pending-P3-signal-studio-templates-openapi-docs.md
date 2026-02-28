# TODO 107 — OpenAPI/Swagger Documentation (P3)

**Repo:** signal-studio-templates  
**Priority:** P3  
**Effort:** S (4 hours)  
**Status:** pending

---

## Autonomous Coding Prompt

```
Add OpenAPI 3.0 spec to /data/workspace/projects/signal-studio-templates/

1. Create openapi.yaml in repo root documenting all 4 API routes:
   - GET /templates (with query param filters)
   - GET /templates/{id}
   - POST /templates/{id}/execute (with body schema)
   - POST /templates/{id}/customize (with whitelist of allowed fields)

2. Add swagger-ui-express to devDependencies for local dev preview.

3. In api/templates.ts, add optional GET /docs route when NODE_ENV=development:
   Serves swagger UI pointing at openapi.yaml

4. Document all response schemas using $ref to reusable components:
   - SignalTemplateSummary (list response)
   - SignalTemplateDetail (full template)
   - ExecutionResult (execute response)
   - ValidationError (400 response)

5. Add "Try it out" examples for each endpoint using the dormant-relationships template
   as the canonical demo template.

6. Update README with link to /docs when running locally.
```

## Acceptance Criteria
- [ ] openapi.yaml covers all 4 endpoints
- [ ] /docs serves Swagger UI in development
- [ ] All request/response schemas documented
- [ ] README updated

## Dependencies
- TODO 101 (auth scheme must be documented in OpenAPI securitySchemes)
