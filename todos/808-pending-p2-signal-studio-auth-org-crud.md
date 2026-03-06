# 808 — Add Organization CRUD Endpoints

**Repo:** signal-studio-auth  
**Priority:** P2  
**Effort:** M (1 day)  
**Dependencies:** 801 (CORS), 804 (audit logging)

## Acceptance Criteria

- [ ] `POST /orgs` — create org (admin only)
- [ ] `GET /orgs/{id}` — get org (member or admin)
- [ ] `PATCH /orgs/{id}` — update org name/metadata (admin only)
- [ ] RBAC enforced via `require_role()` dependency
- [ ] Org data stored in Supabase (via service key)

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/routes/org_routes.py with:

from fastapi import APIRouter, HTTPException, Request, Depends
from middleware.rbac import require_role

router = APIRouter(prefix="/orgs", tags=["orgs"])

class OrgCreateRequest(BaseModel):
    name: str
    slug: str

@router.post("", dependencies=[Depends(require_role("admin"))])
async def create_org(body: OrgCreateRequest, request: Request):
    # Insert into organizations table via Supabase REST API
    ...

@router.get("/{org_id}")
async def get_org(org_id: int, request: Request):
    # Get org - verify caller is member of this org
    ...

@router.patch("/{org_id}", dependencies=[Depends(require_role("admin"))])
async def update_org(org_id: int, body: dict, request: Request):
    ...

Register router in main.py.
Add tests in tests/test_orgs.py.
```
