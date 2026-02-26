---
status: pending
priority: medium
issue_id: "018"
tags: [signal-builder-backend, documentation, openapi, fastapi, developer-experience]
dependencies: []
---

# TODO 018 — API Documentation Enhancements

**Status:** pending  
**Priority:** medium  
**Repo:** signal-builder-backend  
**Effort:** S (0.5-1 day)

## Problem Statement

The FastAPI auto-generated OpenAPI docs are the primary API documentation, but they are currently incomplete:

- Route handlers lack docstrings (endpoint descriptions are blank in Swagger UI)
- Request/response schemas are missing `description` and `example` fields
- No versioning metadata in the OpenAPI spec
- Error response schemas are not declared (no 401, 403, 422, 500 response examples)
- Signal node tree schema is complex — no examples make it hard to use
- `/docs` and `/redoc` are accessible in production (security + info leak risk)

## Findings

- `api.py` creates the FastAPI app via `get_application()`
- Router files are in `apps/*/routers/` and `apps/*/routers_v1.py`
- Pydantic schemas in `apps/*/schemas/` and `core/schemas/`
- `core/__init__.py` exports `get_application`
- No existing docstrings on route handlers

## Coding Prompt

```
You are enhancing the API documentation for signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: FastAPI 0.92, Pydantic v1, Python 3.11

TASK: Add comprehensive API documentation to all route handlers and schemas.

1. Update core/internals/__init__.py (or wherever get_application is defined):
   
   Configure FastAPI app metadata:
   fast_api = FastAPI(
       title="Signal Builder API",
       description="""
       ## Signal Builder Backend API
       
       Provides signal management, SQL translation, and analytical database sync.
       
       ### Authentication
       All endpoints require a valid JWT Bearer token except `/auth/login` and `/health`.
       
       ### Rate Limiting  
       See individual endpoints for rate limit headers.
       """,
       version="1.0.0",
       contact={"name": "ForwardLane Engineering", "email": "engineering@forwardlane.com"},
       license_info={"name": "Proprietary"},
       docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
       redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
       openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
   )

2. Add docstrings to ALL route handlers.
   For each router file in apps/*/routers/:
   
   @router.post(
       "/translate",
       summary="Translate Signal Nodes to SQL",
       description="Converts a signal node tree (JSON) into executable SQL for the analytical database.",
       response_description="Generated SQL query string",
       responses={
           200: {"description": "SQL generated successfully"},
           400: {"model": ErrorDetails, "description": "Invalid signal node tree structure"},
           401: {"model": ErrorDetails, "description": "Authentication required"},
           422: {"model": ErrorDetails, "description": "Validation error in request body"},
       },
       tags=["Signals"],
   )
   async def translate_signal(...):
       """
       Translate a signal node tree into SQL.
       
       The signal tree is a nested JSON structure where each node represents
       a data operation (filter, grouping, ordering, dataset join).
       
       Example node tree:
       ```json
       {
         "$target": {
           "advisor": {
             "$data_node": {"$table": "t_clients"},
             "$filters": {"$property": "age", "$operator": "greater", "$param": 18}
           }
         }
       }
       ```
       """

3. Add examples to Pydantic schemas:
   
   For complex schemas in apps/translators/schemas/ and apps/signals/schemas/:
   
   class SignalNodeTree(BaseModel):
       target: dict = Field(
           ...,
           description="Root target node containing the advisor and dataset definitions",
           example={
               "$target": {
                   "advisor": {
                       "$data_node": {"$table": "t_clients"},
                       "$filters": {"$property": "age", "$operator": "greater", "$param": 18}
                   }
               }
           }
       )
   
   class Config:
       schema_extra = {
           "example": {...}  # Full request example
       }

4. Add error response schemas for all routes:
   In core/schemas/__init__.py or core/schemas/error.py:
   
   class ErrorDetails(BaseModel):
       error: str = Field(..., example="validation_error")
       detail: str = Field(..., example="field 'org_id' is required")
       request_id: Optional[str] = Field(None, example="req_abc123")
   
   class HTTPValidationError(BaseModel):
       detail: List[ErrorDetails]

5. Add OpenAPI tags with descriptions:
   In get_application():
   tags_metadata = [
       {"name": "Auth", "description": "Authentication and token management"},
       {"name": "Signals", "description": "Signal CRUD and SQL translation"},
       {"name": "Analytical DB", "description": "Analytical database sync operations"},
       {"name": "Health", "description": "Service health and readiness checks"},
   ]
   FastAPI(..., openapi_tags=tags_metadata)

6. Tag all existing routes with appropriate tags:
   @router.get("/signals", tags=["Signals"])
   @router.post("/auth/login", tags=["Auth"])
   etc.

7. Disable /docs and /redoc in production:
   docs_url = "/docs" if os.getenv("ENVIRONMENT") != "production" else None

8. Generate and commit OpenAPI spec:
   python -c "
   import json
   from api import fast_api
   with open('docs/openapi.json', 'w') as f:
       json.dump(fast_api.openapi(), f, indent=2)
   "
   Add docs/openapi.json to version control.

9. Create docs/API.md with:
   - Authentication guide (how to get and use JWT tokens)
   - Signal node tree format reference
   - Common error codes and meanings
   - Rate limit documentation

10. Verify: python api.py → http://localhost:8000/docs
    - All endpoints have descriptions
    - All have request/response examples  
    - Error responses documented
    - Tags correctly categorize routes

Constraints:
- /docs and /redoc must be disabled in ENVIRONMENT=production
- Do NOT expose internal implementation details in descriptions
- All examples must use realistic (not test/dummy) data shapes
- Keep descriptions concise — max 3 sentences per endpoint
```

## Acceptance Criteria

- [ ] FastAPI app has title, description, version, contact metadata
- [ ] `/docs` and `/redoc` disabled when `ENVIRONMENT=production`
- [ ] All route handlers have `summary` and `description`
- [ ] All routes tagged with appropriate OpenAPI tags
- [ ] Complex schemas (signal node tree) have `schema_extra` examples
- [ ] Error responses (401, 403, 422, 500) documented on all routes
- [ ] `ErrorDetails` Pydantic schema created and used in error responses
- [ ] `docs/openapi.json` generated and committed
- [ ] `docs/API.md` created with authentication guide and node tree reference

## Dependencies

None — standalone documentation work. Can execute independently.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Identified blank Swagger UI descriptions as developer-experience gap
- Security risk: /docs exposed in production reveals API structure
- Signal node tree schema needs worked examples — it's the core API contract

**Learnings:**
- FastAPI docs_url=None disables Swagger UI (important for production)
- Pydantic schema_extra examples appear in Swagger UI — high value for complex schemas
