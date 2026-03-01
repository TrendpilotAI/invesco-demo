# TODO 361: Add OpenAPI Schema + Swagger/Redoc Docs

**Repo:** forwardlane-backend  
**Priority:** MEDIUM  
**Effort:** M (2-4 hours)  
**Dependencies:** 351 (dj-rest-auth migration)

## Description

The backend has no auto-generated API documentation. Invesco and future partners need a machine-readable API contract. DRF has built-in schema generation; `drf-yasg` is already installed but not configured.

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/.

Task: Configure OpenAPI schema generation and expose Swagger/Redoc docs endpoints.

1. Check if drf-yasg is in Pipfile (it is: drf-yasg = "==1.21.*"). Update to latest:
   drf-yasg = ">=1.21,<2.0"

2. Add drf_yasg to INSTALLED_APPS in settings (check settings.py.example).

3. In forwardlane/urls.py (or api/urls.py), add the schema view:
   
   from drf_yasg.views import get_schema_view
   from drf_yasg import openapi
   from rest_framework import permissions
   
   schema_view = get_schema_view(
       openapi.Info(
           title="ForwardLane API",
           default_version='v1',
           description="ForwardLane backend API — advisor intelligence, signals, meeting prep",
           contact=openapi.Contact(email="tech@forwardlane.com"),
       ),
       public=False,
       permission_classes=[permissions.IsAuthenticated],
   )
   
   urlpatterns += [
       path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
       path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
       path('api/schema.json', schema_view.without_ui(cache_timeout=3600), name='schema-json'),
   ]

4. Add docstrings to all easy_button views explaining request/response format.
   Use drf-yasg @swagger_auto_schema decorators on easy_button views to document:
   - NLQueryView POST: body schema {query: string}, response schema
   - MeetingPrepView GET: response schema with all fields
   - DashboardView GET: response schema

5. Verify the schema generates without errors:
   python manage.py generate_swagger /tmp/schema.json
   cat /tmp/schema.json | python -m json.tool | head -50

Commit: "feat: add OpenAPI schema + Swagger/Redoc docs (drf-yasg)"
```

## Acceptance Criteria
- [ ] `/api/docs/` returns Redoc UI
- [ ] `/api/swagger/` returns Swagger UI  
- [ ] `/api/schema.json` returns valid OpenAPI JSON
- [ ] All easy_button endpoints documented with request/response schemas
- [ ] Docs require authentication (not public)
