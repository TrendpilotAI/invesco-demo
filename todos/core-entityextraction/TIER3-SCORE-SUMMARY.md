# core-entityextraction — Score Summary
> Scored: 2026-03-15 | Category: CORE (ForwardLane)

## Dimension Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code Quality** | 4.5/10 | Off-by-one bug, dead code remnants (services/, seeds/, utils/logger.py), duplicated constants, DRY violations in error handling |
| **Test Coverage** | 0.5/10 | ZERO test files. Production NLP service with no safety net. |
| **Security** | 5.5/10 | ✅ Rate limiting (slowapi) + input validation (50k max) added. ❌ No CORS, single non-rotatable API key, no dep scan |
| **Documentation** | 2/10 | README references Flask/SQLite/Python 3.6.5. .env.example is Flask-era. No API docs. |
| **Architecture** | 5.5/10 | ✅ asyncpg migration done. Clean FastAPI structure. ❌ Pattern recompilation per-request, sync model loading blocks event loop, no batch endpoints |
| **Business Value** | 8/10 | Semantic spine of ForwardLane. Financial NER differentiator vs generic LLM extraction. Directly enables product quality. |

## Composite Score: 4.3/10

## Recent Improvements (since last audit)
- ✅ Migrated persistence.py from sync psycopg2 → async asyncpg (CRITICAL fix)
- ✅ Added slowapi rate limiting
- ✅ Added Pydantic input size validation (max_length=50k)
- ✅ Deleted dead Flask files (app.py, uswgi.py, extensions.py, app_context.py)

## CRITICAL Issues (2)
1. **🐛 Off-by-one bug** in `ExcludeRules.is_start_of_sentence` — `range(start_index, 1, -1)` should be `range(start_index - 1, 0, -1)`. Causes incorrect entity extraction in production.
2. **🧪 ZERO test coverage** — Production NLP service with no automated tests.

## High Priority Items (5)
1. Add CORS middleware (XS effort, security blocker for browser clients)
2. Delete remaining dead code (utils/logger.py, services/, seeds/)
3. Cache compiled regex patterns (S effort, 10-50x perf improvement)
4. Rewrite README.md and .env.example (stale Flask-era docs)
5. Add CI test/lint/security gates

## Strategic Notes
- This service is ForwardLane's **financial NLP moat** — domain-specific precision that generic LLMs can't match at scale
- Multi-tenancy and entity versioning are next major architectural milestones
- spaCy fine-tuning pipeline is the long-term competitive differentiator
- Potential standalone API product under SignalHaus.AI brand
