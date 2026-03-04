# TODO-464: Celery Dead Letter Queue + Task Monitoring

**Priority:** MEDIUM  
**Repo:** forwardlane-backend  
**Effort:** M (4-6 hours)  
**Dependencies:** None

## Description
No dead letter handling or monitoring for failed Celery tasks. Content ingestion and adapter sync tasks can fail silently. Add dead letter queue, retry policies, and Slack/Sentry alerting on failures.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Update CELERY_* settings in forwardlane/settings/celery.py (or base.py):
   CELERY_TASK_ACKS_LATE = True
   CELERY_TASK_REJECT_ON_WORKER_LOST = True
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'
   # Dead letter queue
   CELERY_TASK_ROUTES = {
       'content_ingestion.*': {'queue': 'content'},
       'adapters.*': {'queue': 'adapters'},
   }

2. Add task base class with retry + alerting:
   # core/tasks.py
   class MonitoredTask(celery.Task):
       max_retries = 3
       default_retry_delay = 60
       
       def on_failure(self, exc, task_id, args, kwargs, einfo):
           # Log to Sentry
           sentry_sdk.capture_exception(exc)
           # Log structured
           logger.error("task_failed", extra={task_id, str(exc)})

3. Update content_ingestion/tasks.py and adapters/*/tasks.py to use MonitoredTask

4. Add Flower for Celery monitoring:
   - Add flower to Pipfile
   - Add flower service to docker-compose.yml
   - Protect with basic auth

5. Add tests for retry behavior

6. Commit: "ops: add Celery dead letter handling, retry policies, Sentry alerting, Flower monitoring"
```

## Acceptance Criteria
- [ ] Tasks retry 3x before failing
- [ ] Failures reported to Sentry
- [ ] Flower dashboard available in docker-compose
- [ ] Structured logging on task failures
