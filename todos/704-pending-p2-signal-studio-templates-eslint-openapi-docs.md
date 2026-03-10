---
id: 704
status: pending
repo: signal-studio-templates
priority: P2
effort: S
created: 2026-03-10
---

# TODO 704 — ESLint Config + OpenAPI Docs

**Repo:** signal-studio-templates  
**Priority:** P2 — Needed for dev experience and API consumers  
**Effort:** S (3-4 hours)

## Problem

1. **ESLint config missing** — `pnpm lint` runs `eslint src --ext .ts,.tsx` but there's no `.eslintrc.json`. The CI lint step likely fails or silently does nothing.
2. **No API documentation** — The Express router has no OpenAPI/Swagger spec. External teams integrating with the templates API have no contract documentation.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates:

### Part 1: ESLint Configuration

1. pnpm add -D @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint

2. Create .eslintrc.json:
   {
     "root": true,
     "parser": "@typescript-eslint/parser",
     "parserOptions": {
       "ecmaVersion": 2022,
       "sourceType": "module",
       "project": "./tsconfig.json"
     },
     "plugins": ["@typescript-eslint"],
     "extends": [
       "eslint:recommended",
       "plugin:@typescript-eslint/recommended"
     ],
     "rules": {
       "@typescript-eslint/no-explicit-any": "warn",
       "@typescript-eslint/explicit-module-boundary-types": "off",
       "no-console": "warn"
     },
     "ignorePatterns": ["dist/", "node_modules/", "jest.setup.js"]
   }

3. Update package.json lint script to cover all TS files, not just src/:
   "lint": "eslint . --ext .ts,.tsx --ignore-path .gitignore"

4. Fix any lint errors that surface (likely: some @typescript-eslint/no-explicit-any in template files).

### Part 2: OpenAPI Documentation

1. Create docs/openapi.yaml (or api/openapi.yaml):
   openapi: 3.0.3
   info:
     title: Signal Studio Templates API
     version: 1.0.0
     description: Pre-built signal templates for ForwardLane Signal Studio
   
   paths:
     /templates:
       get:
         summary: List all available templates
         parameters:
           - name: category
             in: query
             schema:
               type: string
               enum: [meeting-prep, sales-intelligence, risk-compliance, product-marketing, management]
           - name: id
             in: query
             schema:
               type: string
         responses:
           '200':
             description: List of signal templates
             content:
               application/json:
                 schema:
                   type: object
                   properties:
                     templates:
                       type: array
                       items:
                         $ref: '#/components/schemas/SignalTemplate'
     
     /templates/{id}/execute:
       post:
         summary: Execute a template and return signal data
         security:
           - bearerAuth: []
         parameters:
           - name: id
             in: path
             required: true
             schema:
               type: string
         requestBody:
           content:
             application/json:
               schema:
                 $ref: '#/components/schemas/ExecuteRequest'
         responses:
           '200':
             description: Execution result
             content:
               application/json:
                 schema:
                   $ref: '#/components/schemas/ExecutionResult'
           '400': { description: Validation error }
           '401': { description: Unauthorized }
           '404': { description: Template not found }
           '408': { description: Query timeout }
           '429': { description: Rate limit exceeded }
   
   components:
     securitySchemes:
       bearerAuth:
         type: http
         scheme: bearer
         bearerFormat: JWT
     schemas:
       (define SignalTemplate, ExecuteRequest, ExecutionResult based on TypeScript interfaces)

2. Add a GET /api-docs endpoint in api/templates.ts that serves the openapi.yaml as JSON (use js-yaml to parse).

3. Update README.md with API reference section pointing to /api-docs.
```

## Files

- `.eslintrc.json` (new)
- `package.json` (update lint script, add eslint devDeps)
- `docs/openapi.yaml` (new)
- `api/templates.ts` (add /api-docs endpoint)

## Acceptance Criteria

- `pnpm lint` succeeds with zero errors
- ESLint runs in CI without failing
- `GET /api-docs` returns valid OpenAPI 3.0 JSON
- All API endpoints documented with request/response schemas
