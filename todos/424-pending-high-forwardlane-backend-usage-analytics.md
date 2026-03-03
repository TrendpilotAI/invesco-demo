# TODO-424: Usage Analytics Model for Invesco Renewal Evidence

**Repo:** forwardlane-backend  
**Priority:** HIGH  
**Effort:** M (1 day)  
**Depends on:** None

## Problem
ForwardLane has zero visibility into how Invesco uses the platform. To renew/expand the Invesco contract, Nathan needs to show: queries per day, most popular questions, meeting briefs generated, time saved. Currently no data is captured.

## Task
Create a `UsageEvent` model and log key user actions across easy_button endpoints. Add admin export + Prometheus counters.

## Coding Prompt
```python
# easy_button/models.py
class UsageEvent(models.Model):
    FEATURE_CHOICES = [
        ('nl_query', 'NL→SQL Query'),
        ('meeting_prep', 'Meeting Prep'),
        ('dashboard', 'Dashboard View'),
        ('signals', 'Signals View'),
        ('client_detail', 'Client Detail'),
    ]
    org = models.CharField(max_length=100, db_index=True)
    user_id = models.CharField(max_length=100, blank=True)
    feature = models.CharField(max_length=50, choices=FEATURE_CHOICES, db_index=True)
    metadata = models.JSONField(default=dict)  # question, latency_ms, cache_hit, etc.
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [models.Index(fields=['org', 'feature', 'created_at'])]

# Log in each view:
UsageEvent.objects.create(
    org=request.META.get('HTTP_X_ORG', 'invesco'),
    feature='nl_query',
    metadata={'question': question, 'latency_ms': latency, 'cache_hit': cache_hit},
    ip_address=request.META.get('REMOTE_ADDR'),
)
```

Add admin export action. Add `usage_events_total` Prometheus counter.

## Acceptance Criteria
- [ ] UsageEvent model + migration created
- [ ] All 5 easy_button endpoint types log events
- [ ] Django admin: list view + CSV export
- [ ] Prometheus counter `easy_button_usage_total` with `feature` label
- [ ] Unit test: verify event created on view call
