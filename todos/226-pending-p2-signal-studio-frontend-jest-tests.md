# TODO-226: Jest + React Testing Library Setup

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** M (1-2 days)  
**Status:** pending

## Problem
Zero tests exist. Any refactoring or new feature development risks silent regressions.

## Acceptance Criteria
- `npm test` runs all tests and reports coverage
- Unit tests for: apiClient, useAppStore, all API hooks (mocked)
- Component tests for: Button, Input, Card, Sidebar

## Coding Prompt

```
1. Install dev dependencies:
   npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom ts-jest

2. Create jest.config.ts:
   export default {
     testEnvironment: 'jsdom',
     setupFilesAfterFramework: ['<rootDir>/jest.setup.ts'],
     moduleNameMapper: { '^@/(.*)$': '<rootDir>/src/$1' },
     transform: { '^.+\\.tsx?$': 'ts-jest' }
   }

3. Create jest.setup.ts:
   import '@testing-library/jest-dom'

4. Create __tests__/lib/api/client.test.ts — test apiClient:
   - Happy path: returns JSON on 200
   - Error path: throws on non-2xx
   - Auth header: includes Authorization Bearer when session exists

5. Create __tests__/lib/stores/app-store.test.ts:
   - toggleSidebar works
   - setCurrentOrgId works
   - toggleDarkMode works

6. Create __tests__/lib/api/hooks.test.ts:
   - Mock apiClient
   - Test useSignals returns data
   - Test useCreateSignal calls POST

7. Add "test": "jest --coverage" to package.json scripts
```

## Dependencies
- TODO-221 (auth token) — tests will need to mock the session
