# MASTER TODO - forwardlane_advisor

## P0 - Critical
- Remove all Watson dead code artifacts (TODO-838)
- Add streaming LLM dialog features (TODO-876)

## P1 - High Priority
- Upgrade Sequelize ORM from v3 to v6 with migration testing (TODO-836)
- Upgrade AWS SDK from v2 to v3 (TODO-837)
- Implement Redis session store for scalable session handling (TODO-840)
- Achieve 40%+ test coverage with integration tests for critical modules (TODO-839)
- Setup CI/CD pipeline for automation (TODO-454, TODO-571)
- Audit and fix N+1 database query patterns (TODO-455)

## P2 - Medium Priority
- Merge duplicate Morningstar integration directories
- Add rate limiting on LLM API endpoints (TODO-575)
- Add health check endpoints `/health` and `/ready`
- Implement LLM response caching with Redis

## P3 - Low Priority
- Frontend modernization with React or Hotwire/components
- Salesforce/CRM Integration
- Improve CORS origin whitelist configuration
- Add Content Security Policy headers
