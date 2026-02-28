# 236 · P2 · signal-builder-frontend · MSW Integration Tests for RTK Query Endpoints

## Status
pending

## Priority
P2 — MSW is installed and configured but completely unused in tests; API contract coverage = 0

## Description
MSW 2.x is installed (`msw: ^2.1.5`, `public/mockServiceWorker.js` present) and partially configured in `src/modules/onboarding/api/onboarding.api.mock.ts`, but no integration tests use it. This task creates handler files and tests for the builder API endpoints.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Set up MSW handlers for builder API
Create `src/redux/builder/api.handlers.ts`:
```typescript
import { http, HttpResponse } from 'msw';
import { mockSchema } from '../mocks/schema.mock';

const BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://sb-beqa.forwardlane.com';

export const builderHandlers = [
  http.get(`${BASE_URL}/api/schema/`, () => {
    return HttpResponse.json(mockSchema);
  }),
  http.get(`${BASE_URL}/api/signals/`, ({ request }) => {
    const url = new URL(request.url);
    return HttpResponse.json({
      count: 2,
      results: [
        { id: 'sig-1', name: 'Test Signal 1', is_draft: true, is_published: false },
        { id: 'sig-2', name: 'Test Signal 2', is_draft: false, is_published: true },
      ],
      page_number: Number(url.searchParams.get('page_number')) || 1,
    });
  }),
  http.post(`${BASE_URL}/api/signals/`, async ({ request }) => {
    const body = await request.json() as { name: string };
    return HttpResponse.json({ id: 'new-sig', name: body.name, is_draft: true });
  }),
  http.get(`${BASE_URL}/api/signals/:id/`, ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Fetched Signal', is_draft: true });
  }),
  http.get(`${BASE_URL}/api/signals/:id/ui/`, ({ params }) => {
    return HttpResponse.json({ signal_id: params.id, tabs: [] });
  }),
];

// Error scenario handlers for testing:
export const errorHandlers = [
  http.get(`${BASE_URL}/api/schema/`, () => {
    return new HttpResponse(null, { status: 500 });
  }),
];
```

Step 2: Set up MSW server for tests
Create/update `src/setupTests.ts`:
```typescript
import '@testing-library/jest-dom';
import { setupServer } from 'msw/node';
import { builderHandlers } from './redux/builder/api.handlers';

export const server = setupServer(...builderHandlers);

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Step 3: Create `src/redux/builder/api.test.ts`

Write integration tests using a Redux store wrapper:
```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { setupStore } from '../store';
import { builderApi } from './api';
import { server } from '../../setupTests';
import { errorHandlers } from './api.handlers';
import { http, HttpResponse } from 'msw';

const createWrapper = (store = setupStore()) => 
  ({ children }: { children: React.ReactNode }) => (
    <Provider store={store}>{children}</Provider>
  );

describe('builderApi - getSchema', () => {
  it('fetches and returns schema data', async () => {
    const { result } = renderHook(
      () => builderApi.endpoints.getSchema.useQuery(),
      { wrapper: createWrapper() }
    );
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toBeDefined();
  });

  it('handles 500 error gracefully', async () => {
    server.use(...errorHandlers);
    const { result } = renderHook(
      () => builderApi.endpoints.getSchema.useQuery(),
      { wrapper: createWrapper() }
    );
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error).toBeDefined();
  });
});

describe('builderApi - getSignals', () => {
  it('fetches signal list with pagination', async () => { ... });
  it('passes page_number param correctly', async () => { ... });
});

describe('builderApi - createSignal', () => {
  it('creates signal and returns id', async () => { ... });
});
```

Step 4: Run and fix tests
yarn test --testPathPattern="api.test" --watchAll=false

Commit: "test: add MSW integration tests for builder RTK Query endpoints"
```

## Dependencies
- 231 (builder.lib tests) recommended first to establish testing patterns
- 229 (type fixes) helps with properly typed test fixtures

## Effort Estimate
M (1–2 days)

## Acceptance Criteria
- [ ] `src/redux/builder/api.handlers.ts` with MSW handlers for all builder endpoints
- [ ] `setupTests.ts` properly configures MSW server
- [ ] `api.test.ts` with tests for getSchema (success + error), getSignals, createSignal
- [ ] Error path test verifies no unhandled promise rejections
- [ ] All tests pass: `CI=true yarn test --watchAll=false`
