# TODO-324: Unit Tests (Vitest + MSW) — Signal Studio Frontend

**Priority:** P1  
**Repo:** signal-studio-frontend  
**Effort:** M (4–6h)  
**Status:** pending  

## Description
Zero test coverage. Add Vitest + Testing Library + MSW for unit and hook testing.

## Coding Prompt (Autonomous Agent)
```
In /data/workspace/projects/signal-studio-frontend:

1. Install: npm install --save-dev vitest @vitest/coverage-v8 @testing-library/react @testing-library/user-event msw jsdom

2. Create vitest.config.ts:
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: { environment: 'jsdom', setupFiles: ['./src/__tests__/setup.ts'], coverage: { reporter: ['text', 'lcov'] } }
})

3. Create src/__tests__/setup.ts — import @testing-library/jest-dom, setup MSW server

4. Create src/__tests__/mocks/handlers.ts with MSW handlers for:
- GET /signals
- GET /signals/:id
- POST /signals
- GET /dashboard/stats

5. Create src/__tests__/lib/utils.test.ts — test formatRelativeTime and cn

6. Create src/__tests__/hooks/signals.test.ts:
- Test useSignals returns data
- Test useCreateSignal calls POST /signals
- Test useDeleteSignal calls DELETE /signals/:id

7. Add to package.json scripts:
"test": "vitest", "test:coverage": "vitest run --coverage"
```

## Dependencies
- None (but easier after TODO-321 to understand real API shapes)

## Acceptance Criteria
- [ ] `npm test` runs and passes
- [ ] All 6 signal hooks have tests
- [ ] Utils have 100% test coverage
- [ ] MSW intercepts all API calls (no real network in tests)
