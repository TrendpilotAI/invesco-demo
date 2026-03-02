# Agent Prompt Template — Security-by-Design + TDD

Add this to ALL coding agent prompts.

---

## Security-by-Design (MANDATORY)

Every feature MUST include:

1. **Authentication** — If the endpoint touches user data, require auth
2. **Input validation** — Validate all inputs, use schemas (Pydantic/Zod)
3. **Rate limiting** — Add rate limits to public endpoints
4. **CORS** — Explicit origins only, never `*`
5. **Secrets** — Never hardcode, use env vars

```python
# Example: Secure endpoint template
@router.post("/endpoint")
async def create_thing(
    data: ThingCreate,
    user: User = Depends(get_current_user),  # Auth
    rate_limit: None = Depends(rate_limiter),  # Rate limiting
):
    # Validate input
    validated = ThingCreateSchema(**data.model_dump())
    # ... implementation
```

## Test-Driven Development (MANDATORY)

1. **Write failing test FIRST**
2. **Implement minimum code to pass**
3. **Refactor**
4. **Show test output at each step**

```python
# Step 1: Write failing test
def test_thing_creation():
    with pytest.raises(ValidationError):
        ThingCreate(name="")  # Empty name should fail
    
    thing = ThingCreate(name="valid")
    assert thing.name == "valid"

# Step 2: Implement to pass
class ThingCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

# Step 3: Refactor
```

## Quality Gate (MANDATORY)

Before committing, run:

```bash
bash /data/workspace/scripts/quality-gate/quality-check.sh .
```

If it fails, fix and re-run. Do not commit failing code.

## PR Workflow (MANDATORY)

Never push to main. Always:

```bash
bash /data/workspace/scripts/quality-gate/agent-pr.sh "feat: description" "PR body"
```

This creates a branch, commits, pushes, and opens a PR.
