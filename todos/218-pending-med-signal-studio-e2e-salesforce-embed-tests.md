# 218 · MED · signal-studio · Add E2E tests for Salesforce embed flow

## Status
pending

## Project
signal-studio (`/data/workspace/projects/signal-studio/`)

## Task Description
The Salesforce embed flow (`app/easy-button/salesforce-embed.tsx`) is used by Invesco advisors who access Signal Studio embedded within Salesforce CRM. There are currently no E2E tests validating:

1. The embed renders correctly when loaded with a Salesforce context token
2. Signal data loads within the embed context
3. CRM actions (e.g., creating a task, logging activity) trigger correctly
4. The embed handles authentication via token (not cookie-based session)
5. Postmessage communication between Salesforce and the embed works

## Dependencies
- 212 (auth middleware — embed auth path must be explicitly tested/exempted)
- 216 (Easy Button test suite — shares test infrastructure)

## Estimated Effort
3 hours

## Acceptance Criteria
- [ ] Playwright E2E tests cover: load, auth, signal display, CRM action dispatch
- [ ] Tests run against a mock Salesforce iframe parent (no real SFDC dependency)
- [ ] Embed loading with invalid token returns 401 (or redirect to error page)
- [ ] `tests/e2e/salesforce-embed.spec.ts` passes in CI

## Coding Prompt

```
You are working in the Next.js 14 App Router project at /data/workspace/projects/signal-studio/.

TASK: Write Playwright E2E tests for the Salesforce embed flow.

### Step 1 — Read the embed source

```bash
cat app/easy-button/salesforce-embed.tsx
cat app/easy-button/embed/page.tsx
cat app/easy-button/embed/embed-client.tsx
```

Identify:
- How auth token is passed (URL param? postMessage? header?)
- What CRM actions are exposed (postMessage events?)
- What data is displayed in embed context

### Step 2 — Create tests/e2e/salesforce-embed.spec.ts

```typescript
import { test, expect, Page } from "@playwright/test"

// Generate a valid embed token for testing
// Adjust to match actual embed token format used in the app
const VALID_EMBED_TOKEN = process.env.TEST_EMBED_TOKEN ?? "test-embed-token-valid"
const INVALID_EMBED_TOKEN = "invalid-token-xyz"

// Mock Salesforce context that would typically be provided
const MOCK_SF_CONTEXT = {
  userId: "sf-user-005000000000001",
  orgId: "sf-org-00D000000000001",
  clientId: "sf-account-001000000000001",
  clientName: "Invesco Test Advisor",
}

test.describe("Salesforce Embed Flow", () => {
  test("embed page loads with valid token", async ({ page }) => {
    const url = `/easy-button/embed?token=${VALID_EMBED_TOKEN}`
    await page.goto(url)
    
    // Should NOT redirect to login
    await expect(page).not.toHaveURL(/\/login/)
    
    // Should render embed content
    await expect(page.locator("body")).not.toBeEmpty()
    
    // Key UI elements should be visible
    await expect(page.locator("[data-testid='embed-container']")).toBeVisible({ timeout: 10000 })
  })

  test("embed page rejects invalid token", async ({ page }) => {
    await page.goto(`/easy-button/embed?token=${INVALID_EMBED_TOKEN}`)
    
    // Should show error state or redirect to error page
    // Check for error message or redirect
    const hasError = await page.locator("[data-testid='embed-error']").isVisible().catch(() => false)
    const redirectedToLogin = page.url().includes("/login")
    const redirectedToError = page.url().includes("/error")
    
    expect(hasError || redirectedToLogin || redirectedToError).toBeTruthy()
  })

  test("embed initializes with Salesforce context via URL params", async ({ page }) => {
    const params = new URLSearchParams({
      token: VALID_EMBED_TOKEN,
      sfUserId: MOCK_SF_CONTEXT.userId,
      sfOrgId: MOCK_SF_CONTEXT.orgId,
      clientId: MOCK_SF_CONTEXT.clientId,
      clientName: MOCK_SF_CONTEXT.clientName,
    })
    
    await page.goto(`/easy-button/embed?${params}`)
    
    // Client name should appear in the embed
    await expect(page.getByText(MOCK_SF_CONTEXT.clientName)).toBeVisible({ timeout: 10000 })
  })

  test("embed receives and handles postMessage from parent", async ({ page }) => {
    // Create a test page that simulates Salesforce as parent
    await page.setContent(`
      <!DOCTYPE html>
      <html>
        <body>
          <iframe 
            id="signal-embed" 
            src="http://localhost:3000/easy-button/embed?token=${VALID_EMBED_TOKEN}"
            style="width:800px;height:600px;border:none;"
            sandbox="allow-scripts allow-same-origin allow-forms"
          ></iframe>
          <script>
            // Simulate Salesforce sending context to embed
            const iframe = document.getElementById('signal-embed')
            iframe.addEventListener('load', () => {
              iframe.contentWindow.postMessage({
                type: 'SF_CONTEXT',
                payload: ${JSON.stringify(MOCK_SF_CONTEXT)}
              }, 'http://localhost:3000')
            })
          </script>
        </body>
      </html>
    `, { baseURL: "http://localhost:8080" })

    const frame = page.frameLocator("#signal-embed")
    
    // Embed should have rendered
    await expect(frame.locator("body")).not.toBeEmpty()
  })

  test("embed dispatches CRM action postMessage to parent", async ({ page }) => {
    // Track postMessages sent from the embed to the parent
    const messages: any[] = []
    page.on("console", msg => {
      if (msg.text().startsWith("postMessage:")) {
        messages.push(JSON.parse(msg.text().replace("postMessage:", "")))
      }
    })

    // Intercept postMessage calls
    await page.goto(`/easy-button/embed?token=${VALID_EMBED_TOKEN}`)
    
    await page.addInitScript(() => {
      const original = window.parent.postMessage.bind(window.parent)
      window.parent.postMessage = (data, ...args) => {
        console.log("postMessage:" + JSON.stringify(data))
        return original(data, ...args)
      }
    })

    // Trigger a CRM action (e.g., "Log Activity" button)
    const logActivityButton = page.getByRole("button", { name: /log activity|crm action/i })
    if (await logActivityButton.isVisible({ timeout: 5000 }).catch(() => false)) {
      await logActivityButton.click()
      
      // Verify a postMessage was sent to the parent
      await page.waitForTimeout(1000)
      const crmMessages = messages.filter(m => m.type?.startsWith("CRM_"))
      expect(crmMessages.length).toBeGreaterThan(0)
    }
  })

  test("embed signal list loads and is interactive", async ({ page }) => {
    await page.goto(`/easy-button/embed?token=${VALID_EMBED_TOKEN}`)
    
    // Wait for signals to load
    const signalItems = page.locator("[data-testid='signal-item'], [data-testid='signal-template']")
    await expect(signalItems.first()).toBeVisible({ timeout: 15000 })
    
    // Should have at least one signal
    expect(await signalItems.count()).toBeGreaterThan(0)
    
    // Click the first signal
    await signalItems.first().click()
    
    // Detail view or expanded state should appear
    const detailView = page.locator("[data-testid='signal-detail'], [data-testid='signal-results']")
    await expect(detailView).toBeVisible({ timeout: 10000 })
  })
})

test.describe("Salesforce Embed - Token Security", () => {
  test("embed without token redirects to error state", async ({ page }) => {
    await page.goto("/easy-button/embed")  // no token param
    await page.waitForLoadState("networkidle")
    
    const isError = 
      page.url().includes("/error") ||
      page.url().includes("/login") ||
      await page.locator("[data-testid='embed-error']").isVisible().catch(() => false)
    
    expect(isError).toBeTruthy()
  })

  test("expired token shows appropriate error message", async ({ page }) => {
    await page.goto(`/easy-button/embed?token=expired-token-here`)
    await page.waitForLoadState("networkidle")
    
    // Look for "expired" or "invalid" in the error message
    const errorText = await page.textContent("body")
    const hasExpiredMessage = 
      errorText?.toLowerCase().includes("expired") ||
      errorText?.toLowerCase().includes("invalid") ||
      errorText?.toLowerCase().includes("unauthorized") ||
      page.url().includes("/error")
    
    expect(hasExpiredMessage).toBeTruthy()
  })
})
```

### Step 3 — Add test data-testid attributes to embed components

In `app/easy-button/embed/embed-client.tsx`, add:
```tsx
<div data-testid="embed-container">
  {/* existing content */}
</div>

{/* Error state: */}
<div data-testid="embed-error">
  {/* error content */}
</div>
```

### Step 4 — Configure Playwright for embed tests

Update `playwright.config.ts` to include:
```typescript
projects: [
  {
    name: "embed",
    testMatch: "**/salesforce-embed.spec.ts",
    use: {
      // Embed tests may need specific headers
      extraHTTPHeaders: {
        "X-Frame-Options": "ALLOWALL",
      },
    },
  },
  // ... other projects
]
```

### Step 5 — Run the tests
```bash
cd /data/workspace/projects/signal-studio
pnpm exec playwright test tests/e2e/salesforce-embed.spec.ts --headed
```

If tests fail due to auth token format, inspect the actual embed token validation logic:
```bash
grep -rn "embed.*token\|token.*embed\|embedToken" app/ lib/ --include="*.ts" --include="*.tsx"
```
Then adjust `VALID_EMBED_TOKEN` format accordingly.
```

## Related Files
- `app/easy-button/salesforce-embed.tsx` (READ + add testid)
- `app/easy-button/embed/page.tsx` (READ + add testid)
- `app/easy-button/embed/embed-client.tsx` (READ + add testid)
- `tests/e2e/salesforce-embed.spec.ts` (CREATE)
- `playwright.config.ts` (UPDATE)
