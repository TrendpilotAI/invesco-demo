# 216 · HIGH · signal-studio · Write Invesco Easy Button test suite (Jest + Playwright)

## Status
pending

## Priority
high

## Project
signal-studio (`/data/workspace/projects/signal-studio/`)

## Task Description
The Invesco Easy Button (`/easy-button`) is a critical client-facing feature with no automated test coverage. It includes:
- `app/easy-button/page.tsx` — main Easy Button page
- `app/easy-button/salesforce-embed.tsx` — Salesforce iframe embed component
- `app/easy-button/embed/page.tsx` — embeddable version for external contexts
- `app/easy-button/embed/embed-client.tsx` — client-side embed logic
- `app/easy-button/signal-templates.ts` — signal template definitions
- `app/easy-button/meeting-prep-modal.tsx` — meeting preparation modal

Need both unit tests (Jest/React Testing Library) and E2E tests (Playwright).

## Dependencies
- 212 (auth middleware — tests need to handle authenticated requests)

## Estimated Effort
5 hours

## Acceptance Criteria
- [ ] Jest unit tests for `signal-templates.ts` (template generation logic)
- [ ] RTL component tests for `meeting-prep-modal.tsx`
- [ ] Playwright E2E test for the Easy Button happy path (load → select signal → view results)
- [ ] Playwright E2E test for the embed flow (load in iframe context)
- [ ] All tests pass in CI (`pnpm test` + `pnpm e2e`)
- [ ] Test coverage ≥ 80% for `app/easy-button/**`

## Coding Prompt

```
You are working in the Next.js 14 App Router project at /data/workspace/projects/signal-studio/.

TASK: Write a comprehensive test suite for the Invesco Easy Button feature.

### Step 1 — Inspect existing source files

Read these files first to understand the component contracts:
```bash
cat app/easy-button/signal-templates.ts
cat app/easy-button/meeting-prep-modal.tsx
cat app/easy-button/embed/embed-client.tsx
cat app/easy-button/page.tsx
```

### Step 2 — Unit tests for signal-templates.ts

Create `__tests__/easy-button/signal-templates.test.ts`:
```typescript
import { /* import the exported functions/constants */ } from "@/app/easy-button/signal-templates"

describe("signal-templates", () => {
  describe("template definitions", () => {
    it("all templates have required fields (id, name, description, type)", () => {
      // Get all templates and verify shape
      const templates = getSignalTemplates()  // adjust to actual export name
      expect(templates.length).toBeGreaterThan(0)
      for (const t of templates) {
        expect(t).toHaveProperty("id")
        expect(t).toHaveProperty("name")
        expect(t).toHaveProperty("description")
        expect(typeof t.id).toBe("string")
        expect(typeof t.name).toBe("string")
      }
    })

    it("template IDs are unique", () => {
      const templates = getSignalTemplates()
      const ids = templates.map(t => t.id)
      expect(new Set(ids).size).toBe(ids.length)
    })

    it("each template has valid signal type", () => {
      const VALID_TYPES = ["risk", "opportunity", "retention", "growth", "compliance"]
      const templates = getSignalTemplates()
      for (const t of templates) {
        if (t.type) {
          expect(VALID_TYPES).toContain(t.type)
        }
      }
    })
  })
})
```

### Step 3 — Component tests for meeting-prep-modal.tsx

Create `__tests__/easy-button/meeting-prep-modal.test.tsx`:
```typescript
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import MeetingPrepModal from "@/app/easy-button/meeting-prep-modal"

// Mock any API calls
jest.mock("@/lib/chat-service", () => ({
  sendMessage: jest.fn().mockResolvedValue({ content: "Test meeting prep content" }),
}))

describe("MeetingPrepModal", () => {
  const defaultProps = {
    isOpen: true,
    onClose: jest.fn(),
    clientName: "John Smith",
    clientId: "client-123",
  }

  it("renders when open", () => {
    render(<MeetingPrepModal {...defaultProps} />)
    expect(screen.getByText(/meeting prep/i)).toBeInTheDocument()
    expect(screen.getByText(/John Smith/i)).toBeInTheDocument()
  })

  it("does not render when closed", () => {
    render(<MeetingPrepModal {...defaultProps} isOpen={false} />)
    expect(screen.queryByText(/meeting prep/i)).not.toBeInTheDocument()
  })

  it("calls onClose when close button is clicked", async () => {
    const onClose = jest.fn()
    render(<MeetingPrepModal {...defaultProps} onClose={onClose} />)
    const closeButton = screen.getByRole("button", { name: /close/i })
    await userEvent.click(closeButton)
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it("loads meeting prep content on open", async () => {
    render(<MeetingPrepModal {...defaultProps} />)
    await waitFor(() => {
      expect(screen.getByText(/Test meeting prep content/i)).toBeInTheDocument()
    })
  })
})
```

### Step 4 — Playwright E2E tests

Create `tests/e2e/easy-button.spec.ts`:
```typescript
import { test, expect } from "@playwright/test"

// Helper to authenticate
async function authenticate(page: any) {
  // Set auth cookies/tokens for test environment
  await page.goto("/login")
  await page.fill('[name="email"]', process.env.TEST_USER_EMAIL ?? "test@forwardlane.com")
  await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD ?? "test-password")
  await page.click('[type="submit"]')
  await page.waitForURL("/")
}

test.describe("Easy Button - Invesco", () => {
  test.beforeEach(async ({ page }) => {
    await authenticate(page)
  })

  test("loads Easy Button page successfully", async ({ page }) => {
    await page.goto("/easy-button")
    await expect(page).toHaveTitle(/Easy Button|Signal Studio/i)
    await expect(page.getByRole("heading")).toBeVisible()
  })

  test("displays signal templates", async ({ page }) => {
    await page.goto("/easy-button")
    // Wait for templates to load
    await expect(page.locator("[data-testid='signal-template']").first()).toBeVisible({ timeout: 10000 })
    const templates = page.locator("[data-testid='signal-template']")
    expect(await templates.count()).toBeGreaterThan(0)
  })

  test("can select a signal template and view results", async ({ page }) => {
    await page.goto("/easy-button")
    await page.locator("[data-testid='signal-template']").first().click()
    // Wait for results panel or detail view
    await expect(page.locator("[data-testid='signal-results']")).toBeVisible({ timeout: 15000 })
  })

  test("meeting prep modal opens and closes", async ({ page }) => {
    await page.goto("/easy-button")
    // Find a client row and click meeting prep
    const meetingPrepButton = page.getByRole("button", { name: /meeting prep/i }).first()
    if (await meetingPrepButton.isVisible()) {
      await meetingPrepButton.click()
      await expect(page.getByRole("dialog")).toBeVisible()
      await page.keyboard.press("Escape")
      await expect(page.getByRole("dialog")).not.toBeVisible()
    }
  })
})
```

### Step 5 — Playwright E2E for embed flow

Create `tests/e2e/easy-button-embed.spec.ts`:
```typescript
import { test, expect } from "@playwright/test"

test.describe("Easy Button Embed", () => {
  test("embed page loads without authentication redirect", async ({ page }) => {
    // Embed should work in iframe context — may use token-based auth
    await page.goto("/easy-button/embed?token=test-embed-token")
    // Should not redirect to login
    await expect(page).not.toHaveURL(/\/login/)
  })

  test("embed renders in iframe context", async ({ page }) => {
    // Create a page that embeds the signal studio in an iframe
    await page.setContent(`
      <html>
        <body>
          <iframe 
            id="signal-embed" 
            src="http://localhost:3000/easy-button/embed?token=test-token"
            width="800" 
            height="600"
          ></iframe>
        </body>
      </html>
    `)
    const frame = page.frameLocator("#signal-embed")
    // The embed should render its content
    await expect(frame.locator("body")).not.toBeEmpty()
  })
})
```

### Step 6 — Add test IDs to components

Add `data-testid` attributes to key elements in the source files:
- `app/easy-button/page.tsx`: add `data-testid="signal-template"` to template cards
- `app/easy-button/page.tsx`: add `data-testid="signal-results"` to results panel

### Step 7 — Update playwright.config.ts

Ensure `/easy-button` routes are included in E2E base URL config.

### Step 8 — Run all tests
```bash
cd /data/workspace/projects/signal-studio
pnpm test __tests__/easy-button/
pnpm exec playwright test tests/e2e/easy-button
```
```

## Related Files
- `app/easy-button/page.tsx` (READ + minor testid additions)
- `app/easy-button/signal-templates.ts` (READ)
- `app/easy-button/meeting-prep-modal.tsx` (READ + minor testid additions)
- `app/easy-button/embed/page.tsx` (READ)
- `app/easy-button/embed/embed-client.tsx` (READ)
- `__tests__/easy-button/signal-templates.test.ts` (CREATE)
- `__tests__/easy-button/meeting-prep-modal.test.tsx` (CREATE)
- `tests/e2e/easy-button.spec.ts` (CREATE)
- `tests/e2e/easy-button-embed.spec.ts` (CREATE)
