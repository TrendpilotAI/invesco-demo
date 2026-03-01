# Data Waterfall Pipeline - Architecture

## Overview

The Data Waterfall is a multi-provider lead enrichment system that chains multiple data providers with intelligent fallback logic. Given a contact (email, name, company, LinkedIn URL), it systematically queries providers in priority order until sufficient data is obtained.

## Design Principles

1. **Waterfall ordering** — Providers are ranked by cost-effectiveness and data quality. Cheapest/fastest first, most expensive/comprehensive last.
2. **Short-circuit** — Stop querying once we have all required fields (email, phone, title, company).
3. **Merge & deduplicate** — Each provider's response is normalized and merged into a canonical contact record.
4. **Cache-first** — Check cache before hitting any provider. Cache successful enrichments for 30 days.
5. **Rate-limit aware** — Per-provider rate limiting with exponential backoff.
6. **Provider-agnostic** — Each provider is a pluggable adapter behind a common interface.
7. **Async execution** — Providers are called sequentially (waterfall) but the overall pipeline runs as a Celery task for non-blocking operation.

## Provider Priority Order

Based on cost-effectiveness, data quality, and API reliability:

| Priority | Provider    | Best For                    | Cost Tier |
|----------|-------------|-----------------------------|-----------|
| 1        | Hunter      | Email finding/verification  | Low       |
| 2        | FindyMail   | Email finding + verification| Low-Med   |
| 3        | Icypeas     | Email enrichment            | Low       |
| 4        | QuickEnrich | Full contact enrichment     | Medium    |
| 5        | Forager     | Deep contact data           | Medium    |
| 6        | Wiza        | LinkedIn-sourced emails     | Med-High  |
| 7        | LeadIQ      | Full B2B enrichment         | High      |

## Data Model

### Canonical Contact Record

```python
{
    "email": "john@example.com",           # Primary target
    "email_verified": True,                 # Has email been verified?
    "emails_alt": ["j.doe@example.com"],   # Alternative emails found
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "title": "VP of Engineering",
    "company": "Example Corp",
    "company_domain": "example.com",
    "phone": "+1-555-0100",
    "phone_direct": "+1-555-0101",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "location": "New York, NY",
    "industry": "Technology",
    "company_size": "51-200",
    "sources": ["hunter", "findymail"],     # Which providers contributed
    "confidence_score": 0.92,               # Aggregate confidence
    "enriched_at": "2025-01-15T10:30:00Z",
    "provider_responses": {                 # Raw responses for audit
        "hunter": {...},
        "findymail": {...}
    }
}
```

### Enrichment Request

```python
{
    "email": "john@example.com",        # At least one of these required
    "first_name": "John",               # Optional but improves results
    "last_name": "Doe",                 # Optional but improves results
    "company": "Example Corp",          # Optional but improves results
    "company_domain": "example.com",    # Optional but improves results
    "linkedin_url": "...",              # Optional, used by Wiza/LeadIQ
    "required_fields": ["email", "title", "company"],  # Stop when these are filled
    "max_providers": 3,                 # Max providers to try (cost control)
    "skip_providers": ["leadiq"],       # Skip specific providers
    "force_refresh": False              # Bypass cache
}
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   API Endpoint                       │
│              POST /api/v1/enrichment/                │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Enrichment Orchestrator                  │
│  1. Validate input                                   │
│  2. Check cache (Redis/DB)                          │
│  3. Determine which fields are missing              │
│  4. Run waterfall                                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Provider Waterfall                       │
│                                                      │
│  ┌──────────┐  miss   ┌──────────┐  miss            │
│  │  Hunter   │───────▶│ FindyMail │───────▶ ...     │
│  └────┬─────┘        └────┬─────┘                   │
│       │ hit               │ hit                      │
│       ▼                   ▼                          │
│  ┌──────────────────────────────┐                   │
│  │     Merge & Normalize         │                   │
│  │  - Deduplicate fields         │                   │
│  │  - Calculate confidence       │                   │
│  │  - Check if required fields   │                   │
│  │    are satisfied              │                   │
│  └──────────────────────────────┘                   │
│       │                                              │
│       ▼ (if required fields still missing)           │
│    Next provider in waterfall...                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Response                                │
│  - Canonical contact record                         │
│  - Cache result                                     │
│  - Log enrichment stats                             │
└─────────────────────────────────────────────────────┘
```

## Caching Strategy

- **Cache key**: Normalized email or `{first_name}:{last_name}:{company_domain}`
- **Cache backend**: Django cache (Redis preferred) + DB for persistence
- **TTL**: 30 days for successful enrichments, 24 hours for failures
- **Invalidation**: Manual via API or on `force_refresh=True`

## Rate Limiting

Each provider adapter maintains its own rate limiter:

```python
PROVIDER_RATE_LIMITS = {
    "hunter": {"requests_per_second": 10, "daily_limit": 500},
    "findymail": {"requests_per_second": 5, "daily_limit": 1000},
    "icypeas": {"requests_per_second": 5, "daily_limit": 500},
    "quickenrich": {"requests_per_second": 3, "daily_limit": 300},
    "forager": {"requests_per_second": 5, "daily_limit": 500},
    "wiza": {"requests_per_second": 2, "daily_limit": 200},
    "leadiq": {"requests_per_second": 2, "daily_limit": 100},
}
```

## Error Handling

- **Provider timeout**: 10s per provider, skip to next
- **Rate limit hit**: Log, skip provider for this request, continue waterfall
- **Auth failure**: Alert, disable provider until API key is refreshed
- **Network error**: Retry once with 2s backoff, then skip

## Batch Enrichment

For bulk operations, a Celery task processes contacts in batches:

```python
# Async batch enrichment
task = enrich_contacts_batch.delay(
    contacts=[...],
    required_fields=["email", "title"],
    max_providers=3
)
```

## Django App Structure

```
enrichment/
├── __init__.py
├── admin.py
├── apps.py
├── models.py              # EnrichmentResult, EnrichmentLog, ProviderConfig
├── serializers.py         # Request/Response serializers
├── urls.py
├── views.py               # API endpoints
├── services/
│   ├── __init__.py
│   ├── orchestrator.py    # Main waterfall logic
│   ├── cache.py           # Caching layer
│   └── normalizer.py      # Data normalization & merging
├── providers/
│   ├── __init__.py
│   ├── base.py            # Abstract provider interface
│   ├── hunter.py
│   ├── findymail.py
│   ├── icypeas.py
│   ├── quickenrich.py
│   ├── forager.py
│   ├── wiza.py
│   └── leadiq.py
├── tasks.py               # Celery tasks for async/batch
├── migrations/
│   └── 0001_initial.py
└── tests/
    ├── __init__.py
    ├── test_orchestrator.py
    ├── test_providers.py
    └── test_views.py
```
