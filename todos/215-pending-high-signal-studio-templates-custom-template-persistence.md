# 215 — Custom Template Persistence: Postgres Schema + CRUD API + Django Backend Integration

**Priority:** high  
**Project:** signal-studio-templates  
**Repo:** /data/workspace/projects/signal-studio-templates/ + Django backend  
**Status:** pending  
**Estimated Effort:** 5h  

---

## Context

Currently, the 20 pre-built templates are hardcoded in the signal-studio-templates library. There is no persistence layer for custom templates that users create in Signal Studio. When a user builds a custom signal template in the UI, it needs to be saved to a database, versioned, and retrieved later. The Django backend (Railway service: Django-Backend) needs CRUD endpoints for custom templates.

---

## Task Description

### Part 1: Postgres Schema (Django backend)

1. Create Django model `SignalTemplate` in the appropriate app:
   ```python
   class SignalTemplate(models.Model):
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       name = models.CharField(max_length=255)
       description = models.TextField(blank=True)
       template_type = models.CharField(max_length=100)  # e.g. 'equity_momentum'
       config = models.JSONField()  # full template configuration
       sql_template = models.TextField()  # parameterized SQL template string
       parameter_schema = models.JSONField()  # JSON Schema for parameter validation
       owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
       organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, null=True)
       is_public = models.BooleanField(default=False)  # share across org
       is_built_in = models.BooleanField(default=False)  # the 20 pre-built templates
       version = models.PositiveIntegerField(default=1)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       
       class Meta:
           ordering = ['-updated_at']
   ```
2. Create migration: `python manage.py makemigrations && python manage.py migrate`
3. Seed the 20 built-in templates into the DB via a data migration or management command.

### Part 2: Django REST API Endpoints

Create `api/views/signal_templates.py` with DRF ViewSet:
- `GET /api/v1/signal-templates/` — list (filter by org, type, owner)
- `POST /api/v1/signal-templates/` — create custom template
- `GET /api/v1/signal-templates/{id}/` — retrieve
- `PUT /api/v1/signal-templates/{id}/` — update (increment version)
- `DELETE /api/v1/signal-templates/{id}/` — soft delete
- `POST /api/v1/signal-templates/{id}/duplicate/` — clone with new owner

### Part 3: TypeScript client update

Add `TemplateRegistry.fetchFromAPI(apiUrl: string): Promise<void>` to signal-studio-templates that loads templates from the Django API and registers them alongside the built-ins.

---

## Coding Prompt (Autonomous Agent)

```
You are implementing custom template persistence for signal-studio-templates.

DJANGO BACKEND REPO: find it at /data/workspace/projects/ (look for forwardlane-backend or signal-builder-backend)
TEMPLATES REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Find the Django backend project (ls /data/workspace/projects/)
2. Find the appropriate Django app for signals/templates
3. Create the SignalTemplate model (schema above)
4. Run makemigrations + migrate
5. Create a DRF ModelViewSet for SignalTemplate with:
   - Authentication required (use existing auth)
   - Organization-scoped filtering (users see their org's templates + built-ins)
   - Serializer with nested parameter_schema validation
   - Permissions: owners can edit/delete, org members can view public templates
6. Register URL routes in the API router
7. Create a management command: python manage.py seed_builtin_templates
   - Reads the 20 templates from signal-studio-templates dist/
   - Creates SignalTemplate records with is_built_in=True
8. In signal-studio-templates TypeScript repo:
   - Add src/api/TemplateAPIClient.ts with fetchTemplates(baseUrl, authToken) method
   - Returns SignalTemplate[] matching the Django serializer shape
9. Test the endpoints manually with curl or httpie
10. Report: migration applied, endpoints working, seed command output
```

---

## Dependencies

- **211** (build must work — TypeScript client needs dist/)
- **213** (SQL hardening — sql_template field stores parameterized templates, not raw SQL)

---

## Acceptance Criteria

- [ ] `SignalTemplate` Django model with migration applied
- [ ] All 5 REST endpoints working (list/create/retrieve/update/delete)
- [ ] `seed_builtin_templates` management command seeds all 20 templates
- [ ] Organization-scoped filtering works (users can't see other orgs' private templates)
- [ ] TypeScript `TemplateAPIClient` fetches and parses templates from Django API
- [ ] API returns 401 for unauthenticated requests
- [ ] Pagination on list endpoint (page_size=20)
