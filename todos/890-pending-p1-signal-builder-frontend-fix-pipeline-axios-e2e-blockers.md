# TODO: Fix Pipeline Env Vars, Axios Error Handling, and Add E2E Tests

## Priority: P1 Critical

### Description

Fix critical CI/CD and client-side issues blocking reliable deployments and user error handling:

- Rename all `REACT_APP_*` environment variables to `VITE_*` in Bitbucket pipeline for correct Vite integration.
- Update axios instance response interceptor to propagate errors correctly by returning `Promise.reject(error)`.
- Add Playwright E2E tests covering core user flows:
  - Signal creation and editing flow
  - Authentication with cookie injection
  - Signal list and filter editing
  - Collections CRUD

These changes address deployment breakage and silent API failure issues, ensuring backend connectivity and robust UX.

### Impact

- Restores correct environment variable usage for deployed builds.
- Improves error handling pipeline and API call reliability.
- Enables automated browser-level testing preventing regressions.

### Recommended Files

- `bitbucket-pipelines.yml`
- `src/shared/lib/getAxiosInstance.ts`
- New `tests/e2e/` directory with Playwright setup

### References

- TODO-878, TODO-879, TODO-881 from audits and brainstorm documents

---