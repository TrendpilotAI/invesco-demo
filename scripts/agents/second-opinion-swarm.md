# Second Opinion TDD Swarm Protocol

## Architecture
```
Phase N:
  Opus 4.6 (Planner) → Generates TDD plan for phase
    ↓
  Sonnet 4-6 (Developer) → Implements code + tests
    ↓
  Opus 4.6 (Evaluator) → Scores work, gives feedback
    ↓ (if score < 9/10)
  Sonnet 4-6 (Developer) → Applies fixes
    ↓
  Opus 4.6 (Evaluator) → Re-scores
    ↓ (loop until score ≥ 9/10 or 3 iterations)
  → Next Phase
```

## Phases
1. Foundation: Module restructure + lazy loading + test infra
2. Services: Harden all 25+ services with tests
3. Components: Test all 40+ components
4. Pipeline: End-to-end analysis flow tests
5. Integration: Full pipeline + edge cases
6. Security: HIPAA, encryption, auth hardening
7. Performance: Bundle optimization, caching
8. Polish: Error handling, i18n, accessibility
