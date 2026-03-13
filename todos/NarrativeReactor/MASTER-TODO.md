# MASTER TODO - NarrativeReactor

## P0 - Critical (Do Immediately)
- Migrate tenants.ts to use centralized SQLite db.ts singleton connection (replace better-sqlite3 with getDb)
- Replace SHA-256 API key hashing with scrypt, implement migration strategy
- Add helmet middleware for security headers in Express app
- Pin wildcard genkit dependencies to fixed versions in package.json
- Implement true HTTP integration tests using supertest for full Express app

## P1 - High Priority
- Add SQLite indexes on hot columns such as tenants(api_key_hash), content_drafts(brand_id), schedules(scheduled_at)
- Move @types/better-sqlite3 from dependencies to devDependencies
- Replace full lodash import with modular imports (e.g. lodash/merge)
- Introduce pino structured logging instead of console.log
- Add ESLint configuration in project root

## P2 - Medium Priority
- Implement LRU cache for AI content generation flows to reduce API costs
- Remove unreachable service trendpilotBridge or wire it to a valid route
- Implement pagination middleware for list endpoints
- Create video job queue system to avoid synchronous blocking video generation
- Add request audit logging middleware for tenant API usage tracking

## P3 - Low Priority
- Add Slack notifications for content approval/rejection
- Build content repurposing pipeline feature
- Create API key rotation UI with grace period for old keys
- Set up pre-commit hooks (husky) and renovate bot for dependency updates

