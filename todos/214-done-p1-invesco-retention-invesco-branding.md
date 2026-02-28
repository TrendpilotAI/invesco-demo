# 214 — Invesco Retention: Invesco Branding in Salesforce Chrome (P1)

**Priority:** 🟠 P1 — Personalization that makes it feel like THEIR Salesforce  
**Project:** invesco-retention  
**Effort:** XS (20-30 min)  
**Owner:** Honey  
**Dependencies:** None (can do before deploy)

---

## Task Description

The Salesforce embed view currently shows a generic "Sales Cloud" header. Changing this to "Invesco Financial Services | Sales Cloud" makes the demo feel like it's running inside Invesco's actual Salesforce instance. This is a small change with outsized psychological impact — Brian and Kelly will see their company name and feel ownership.

Also add the Invesco logo to the mock Salesforce chrome if possible.

---

## Coding Prompt (Agent-Executable)

```
You are adding Invesco-specific branding to the Salesforce view in the invesco-retention demo app.

REPO: /data/workspace/projects/invesco-retention/demo-app

TASK:

1. Find the Salesforce embed/chrome component. Look in:
   - src/app/salesforce/page.tsx
   - src/components/salesforce/
   - Any component with "Sales Cloud" or "Salesforce" text
   
   Run: grep -r "Sales Cloud" src/ to find it.

2. Change "Sales Cloud" → "Invesco Financial Services | Sales Cloud"

3. In the Salesforce header/nav chrome, also update:
   - App name: "ForwardLane for Invesco"
   - Any "Demo Org" or placeholder org name → "Invesco Financial Services"
   - Any user avatar/name → keep as "Marcus Thompson" (the wholesaler persona)

4. Add Invesco brand colors where appropriate:
   - Invesco blue: #003DA5 (primary)
   - Invesco teal: #00A591 (accent)
   - These can be applied to the mock Salesforce app bar/nav if there's a branded strip

5. If there's a logo area in the Salesforce chrome, add a text-based "INVESCO" wordmark:
   ```tsx
   <span className="font-bold tracking-widest text-white" style={{color: '#003DA5'}}>
     INVESCO
   </span>
   ```
   Or use the Invesco SVG logo if you can find/generate one.

6. Add a small "Powered by ForwardLane" badge somewhere subtle (footer or sidebar) — this is the brand impression we want Brian to associate.

7. Search for any other hardcoded org/company references throughout the app:
   Run: grep -r "Demo\|Placeholder\|Example\|Acme\|Company" src/ --include="*.tsx" --include="*.ts"
   Update any that appear in visible UI text.

8. Run: npm run build — confirm 0 errors.

Report: List of files changed and what was updated.
```

---

## Acceptance Criteria
- [ ] Salesforce chrome shows "Invesco Financial Services | Sales Cloud"
- [ ] No generic "Demo Org" or placeholder text visible
- [ ] "Powered by ForwardLane" badge present
- [ ] Invesco brand colors applied to Salesforce header
- [ ] Build passes 0 errors
- [ ] Change is visually clean on mobile
