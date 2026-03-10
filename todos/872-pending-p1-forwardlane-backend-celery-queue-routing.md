# FL-030: Celery Priority Queue Routing

**Repo:** forwardlane-backend  
**Priority:** P1  
**Effort:** S (1 day)  
**Status:** pending

## Task Description
Add priority queue routing to Celery so high-priority ranking tasks (Invesco) are not starved by background ingestion tasks. Separate into `high_priority`, `default`, and `low_priority` queues.

## Problem
All Celery tasks currently share a single queue. Heavy `content_ingestion` tasks can block `client_ranking` updates, directly impacting Invesco's user experience. This is a latency risk for the enterprise deal.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/forwardlane/celery_app.py:

1. Add task routing configuration:
```python
from kombu import Queue, Exchange

# Define queues
CELERY_QUEUES = (
    Queue('high_priority', Exchange('high_priority'), routing_key='high_priority'),
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('low_priority', Exchange('low_priority'), routing_key='low_priority'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

# Route tasks by module
CELERY_TASK_ROUTES = {
    # High priority — Invesco-facing ranking tasks
    'client_ranking.tasks.*': {'queue': 'high_priority'},
    'recommendation_top.tasks.*': {'queue': 'high_priority'},
    
    # Default — standard async tasks
    'product_update.tasks.*': {'queue': 'default'},
    'user.tasks.*': {'queue': 'default'},
    
    # Low priority — background data ingestion
    'content_ingestion.tasks.*': {'queue': 'low_priority'},
    'pipeline_engine.tasks.*': {'queue': 'low_priority'},
    'analytical.tasks.*': {'queue': 'low_priority'},
}
```

2. Update docker-compose.railway.yml and Railway Dockerfile.celery-worker:
   - High priority worker: `celery worker -Q high_priority --concurrency=4`
   - Default worker: `celery worker -Q default --concurrency=2`
   - Low priority worker: `celery worker -Q low_priority --concurrency=2`
   Or single worker with priority routing: `celery worker -Q high_priority,default,low_priority`

3. Update Dockerfile.celery-beat if needed (beat doesn't need queue config)

4. Write test in forwardlane/tests/test_celery_routing.py:
   - Verify client_ranking tasks route to high_priority queue
   - Verify content_ingestion tasks route to low_priority queue

Files to modify:
- forwardlane/celery_app.py
- docker-compose.railway.yml
- Dockerfile.celery-worker
```

## Acceptance Criteria
- [ ] `CELERY_TASK_ROUTES` defined with 3 queue tiers
- [ ] `client_ranking.*` tasks confirmed routed to `high_priority`
- [ ] `content_ingestion.*` tasks confirmed routed to `low_priority`
- [ ] Railway worker config updated to consume correct queues
- [ ] Test verifies routing configuration

## Dependencies
None — independent.
