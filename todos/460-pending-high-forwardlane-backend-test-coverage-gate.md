# TODO-460: Add Test Coverage Gate to CI

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** S (2-3 hours)  
**Dependencies:** None

## Description
CI currently runs tests but doesn't enforce coverage thresholds. Add `pytest-cov` with a coverage gate (fail if < 50%, warn below 70%) and `factory_boy` for better fixtures.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Add to Pipfile [dev-packages]:
   pytest-cov = "*"
   factory-boy = "*"
   responses = "*"  # for mocking HTTP calls

2. Update pytest.ini / tox.ini:
   Add: --cov=. --cov-report=term-missing --cov-fail-under=50

3. Create factories in conftest.py or tests/factories.py:
   - UserFactory (using factory_boy + Django model)
   - OrganizationFactory
   - CustomerFactory (if model exists)

4. Write missing unit tests targeting lowest-coverage modules:
   - ai/document_recommender/: test recommendation logic with mock data
   - pipeline_engine/: test at least one pipeline run with mock adapters
   - easy_button/: test permission class behavior

5. Update bitbucket-pipelines.yml:
   Replace: pytest
   With: pytest --cov=. --cov-fail-under=50 --cov-report=xml
   Add: coverage xml output as pipeline artifact

6. Commit: "test: add pytest-cov coverage gate (50% min), factory_boy fixtures"
```

## Acceptance Criteria
- [ ] `pytest --cov` runs in CI
- [ ] Build fails if coverage drops below 50%
- [ ] factory_boy fixtures available for key models
- [ ] Coverage report artifact in CI output
