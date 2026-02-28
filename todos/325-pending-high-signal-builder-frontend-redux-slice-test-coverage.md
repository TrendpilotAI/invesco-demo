# TODO-325: Test Coverage for Redux Slices — Signal Builder Frontend

**Priority:** P0 (High)
**Status:** Pending
**Project:** signal-builder-frontend
**Effort:** M (3 days)
**Source:** PLAN.md → P0-003

---

## Task Description

Write unit tests for all Redux reducers and selectors in `src/redux/`. Target 80% coverage for the `redux/` directory. This is the safety net needed before any refactoring or Vite migration work.

---

## Coding Prompt

```
You are working in the Signal Builder Frontend repo at /data/workspace/projects/signal-builder-frontend.

Write comprehensive unit tests for all Redux slices. Coverage target: 80% for src/redux/.

Setup (if not already done):
- Testing framework: Jest + React Testing Library (already bundled with CRA)
- Install if missing: `yarn add -D @reduxjs/toolkit @testing-library/react-hooks`

Steps:

1. Discover all slices:
   ```
   find src/redux -name "*.slice.ts" -o -name "*.reducer.ts" | sort
   ls src/redux/
   ```

2. For each slice file found (builder, auth, etc.), create a corresponding `*.test.ts` file:

   **Pattern for reducer tests:**
   ```ts
   import { configureStore } from '@reduxjs/toolkit';
   import reducer, { actionCreator, selectSomeValue } from './mySlice';

   describe('mySlice reducer', () => {
     it('returns initial state', () => {
       expect(reducer(undefined, { type: '' })).toEqual(initialState);
     });

     it('handles actionCreator', () => {
       const state = reducer(undefined, actionCreator(payload));
       expect(state.someField).toBe(expectedValue);
     });
   });

   describe('mySlice selectors', () => {
     it('selectSomeValue returns correct value', () => {
       const store = configureStore({ reducer: { mySlice: reducer } });
       store.dispatch(actionCreator(payload));
       expect(selectSomeValue(store.getState())).toBe(expectedValue);
     });
   });
   ```

3. Builder slice (`src/redux/builder/`):
   - Test every action: adding nodes, removing nodes, updating node config, connecting edges, resetting canvas
   - Test all selectors: getNodes, getEdges, getSelectedNode, isValid, etc.
   - Test edge cases: duplicate node IDs, invalid connections, empty canvas

4. Auth slice (`src/redux/auth/`):
   - Test: setUser, clearUser, setToken, logout actions
   - Test selectors: isAuthenticated, currentUser, token
   - Test: unauthenticated initial state

5. Any other slices found — apply same pattern

6. Add coverage thresholds to `package.json`:
   ```json
   "jest": {
     "coverageThreshold": {
       "global": {
         "branches": 70,
         "functions": 80,
         "lines": 80,
         "statements": 80
       },
       "./src/redux/": {
         "lines": 80
       }
     }
   }
   ```

7. Add to CI: ensure `yarn test --coverage` is in the test step of `bitbucket-pipelines.yml`

Run `yarn test --coverage --watchAll=false` to verify coverage targets are met.
```

---

## Acceptance Criteria

- [ ] Unit tests exist for every slice in `src/redux/builder/` and `src/redux/auth/`
- [ ] All reducer actions tested (happy path + edge cases)
- [ ] All selectors tested
- [ ] Coverage for `src/redux/` directory ≥ 80% lines
- [ ] Coverage thresholds added to Jest config
- [ ] `yarn test --coverage --watchAll=false` passes with no failures
- [ ] CI pipeline runs tests with coverage (bitbucket-pipelines.yml updated)
