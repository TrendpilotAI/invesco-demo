# TODO 363: Expand NL→SQL Quick Patterns + Add Kimi Fallback Improvements

**Repo:** forwardlane-backend  
**Priority:** MEDIUM  
**Effort:** M (3-5 hours)  
**Dependencies:** 355 (shared LLM client), 358 (security tests)

## Description

The NL→SQL quick pattern matcher only covers 5 scenarios. Most natural language questions fall through to the LLM. Adding more patterns reduces latency and LLM API costs. Also, the current LLM prompt could be improved to generate better SQL.

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/easy_button/views.py.

Task: Expand the _QUICK_PATTERNS list in NLQueryView and improve the LLM prompt.

1. Add these additional quick patterns to _QUICK_PATTERNS:
   
   # Dormant advisors
   (r'\bdormant\b|\bno.*flow\b|\binactive\b',
    "select a.advisor_id, a.full_name, a.firm_name, a.aum_current, max(f.flow_month) as last_flow
     from advisors a left join flows f on f.advisor_id = a.advisor_id
     where a.aum_current > 50000000
     group by a.advisor_id, a.full_name, a.firm_name, a.aum_current
     having max(f.flow_month) < current_date - interval '90 days' or max(f.flow_month) is null
     order by a.aum_current desc limit 20"),
   
   # Cross-sell / low Invesco allocation
   (r'\bcross.?sell\b|\blow.*invesco\b|\bopportunit',
    "select a.advisor_id, a.full_name, a.firm_name, a.aum_current,
            coalesce(sum(h.pct_of_aum) filter (where h.fund_family = 'Invesco'), 0) as invesco_pct
     from advisors a left join holdings h on h.advisor_id = a.advisor_id
     group by a.advisor_id, a.full_name, a.firm_name, a.aum_current
     having coalesce(sum(h.pct_of_aum) filter (where h.fund_family = 'Invesco'), 0) < 15
        and a.aum_current > 50000000
     order by a.aum_current desc limit 20"),
   
   # By region
   (r'\b(northeast|southeast|midwest|southwest|west)\b',
    None),  # handled dynamically — see below
   
   # Signals / active alerts
   (r'\bsignal|alert|risk\b',
    "select a.full_name, a.firm_name, s.signal_type, s.signal_score, s.triggered_at
     from signals s join advisors a on a.advisor_id = s.advisor_id
     where s.status = 'active'
     order by s.signal_score desc limit 30"),
   
   # Count queries
   (r'\bhow many advisors\b',
    "select count(*) as advisor_count, channel, round(avg(aum_current)/1e6, 1) as avg_aum_m
     from advisors group by channel order by advisor_count desc"),

2. For the region pattern, implement dynamic SQL building in _quick_match():
   region_map = {'northeast': 'NE', 'southeast': 'SE', 'midwest': 'MW', 
                 'southwest': 'SW', 'west': 'W'}
   Check if any region keyword is in the question, build parameterized-like SQL

3. Improve the _ANALYTICAL_SCHEMA_CONTEXT prompt:
   - Add 5 example question→SQL pairs as few-shot examples
   - Add explicit instruction to prefer JOINs over subqueries for readability
   - Add instruction to always include full_name and firm_name in results

4. Add a response cache for identical questions:
   cache_key = f"nl_query:{hashlib.md5(question.encode()).hexdigest()}"
   Cache for 5 minutes (these are analytical queries, slight staleness is fine)

5. Update tests in easy_button/tests/test_nlsql_security.py to cover new patterns.

Commit: "feat: expand NL→SQL patterns, improve LLM prompt, add query caching"
```

## Acceptance Criteria
- [ ] 5+ new quick patterns added covering dormant, cross-sell, signals, regions, counts
- [ ] LLM prompt improved with few-shot examples
- [ ] Query result caching implemented (5 min TTL)
- [ ] All new patterns have test coverage
- [ ] No regressions in existing patterns
