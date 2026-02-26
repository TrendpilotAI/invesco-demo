# 🌙 10 Overnight Ideas V2 — Feb 22, 2026
## Informed by tonight's deep dive into ForwardLane's actual codebase

These are different from Batch 1. These leverage what we just built and discovered.

---

## 1. 🎯 "Signal Marketplace" — Sell Pre-Built Signal Templates
**One-liner:** Package the 20+ signals we can generate via NL→SQL as a curated library that asset managers can browse, customize, and deploy in one click.

**Why now:** We literally just proved NL→SQL works end-to-end. We have the full analytical schema. We can generate 100 production-quality signals in an afternoon.

**The play:** Generate 50 signals across categories (risk, opportunity, compliance, growth). Let firms browse them like an app store. One-click deploy to their Signal Studio instance. Charge per signal pack or make it a tier feature.

**Effort:** 2 days (batch-generate signals, build a catalog page)
**Revenue:** Upsell feature for Signal Studio subscriptions
**First 3 steps:**
1. Generate 50 signals across 5 categories using /api/signals/generate
2. Build a Signal Marketplace page in Signal Studio (grid of cards with preview)
3. One-click "Deploy Signal" that saves to ranking_signalbuilderrule

---

## 2. 🧠 "Signal Copilot" — AI Pair-Programmer for Signal Building
**One-liner:** Instead of just NL→SQL, build an interactive chat where the AI helps users iteratively refine signals by asking clarifying questions, suggesting improvements, and previewing results.

**Why now:** The AI chat sidebar already exists in Signal Studio. The NL→SQL engine works. Combine them.

**The play:** User says "Find at-risk advisors." Copilot asks "Define 'at-risk' — AUM decline? Sales decline? Low engagement? All three?" User picks. Copilot generates, user tweaks, Copilot refines. Like GitHub Copilot but for financial signals.

**Effort:** 3-4 days (extend visual-builder-chat with multi-turn signal refinement)
**Revenue:** Core differentiator — nobody else has this
**First 3 steps:**
1. Add signal-aware system prompt to the visual builder chat
2. Implement multi-turn refinement (generate → preview → adjust → finalize)
3. "Save Signal" button that persists to Django backend

---

## 3. 📊 "Invesco Health Dashboard" — One-Page Account Health View
**One-liner:** Build a single dashboard page showing Invesco's entire book health: top growers, at-risk accounts, ML recommendation summary, trailing sales trends — all from our analytical DB.

**Why now:** We have the Django backend + analytical schema + seed data running on Railway. This is a demo that sells itself.

**The play:** Craig asked for "easy buttons, not chat." This is the easiest button — one page that answers "How's my book doing?" without any query-building. Run 5 pre-built signals, show results as cards/charts.

**Effort:** 2-3 days
**Revenue:** Direct Invesco retention ($300K account)
**First 3 steps:**
1. Build /dashboard page with 5 summary cards (total AUM, at-risk count, top opportunities, etc.)
2. Wire to /api/signals/generate to run the 5 queries against analytical DB
3. Add sparkline charts for trailing sales trends

---

## 4. 🔌 "Signal Studio MCP Server" — Let Any AI Agent Create Signals
**One-liner:** Wrap Signal Studio's NL→SQL engine as an MCP (Model Context Protocol) tool server so Claude, GPT, or any AI agent can create and manage signals programmatically.

**Why now:** Signal Studio's API docs already spec'd MCP tools (search_signals, execute_signal, create_signal, ask_question). The NL→SQL endpoint IS the create_signal implementation.

**The play:** Position ForwardLane as "AI-agent-native." Any LLM can connect to Signal Studio and create, run, and analyze signals. This is the future of how wholesalers interact — through their AI assistants, not through dashboards.

**Effort:** 2 days (MCP wrapper around existing API endpoints)
**Revenue:** Massive positioning play — "the first MCP-native financial intelligence platform"
**First 3 steps:**
1. Create MCP server definition with 4 tools: generate_signal, execute_signal, list_signals, get_schema
2. Publish as an MCP package
3. Demo with Claude Desktop connecting to Signal Studio

---

## 5. 📱 "Morning Brief" — Daily AI-Generated Wholesaler Report
**One-liner:** Every morning at 6 AM, run the top 10 signals against the analytical DB, summarize results with GPT-4o, and email/Slack each wholesaler their personalized daily brief.

**Why now:** Celery Beat is deploying on Railway. We have the signal engine. We have email capability (Django + Resend). This is the "Craig wants easy" answer.

**The play:** Wholesalers wake up to "3 accounts need attention today: The Blackwood Group dropped 26% YoY, Sterling Financial has a cross-sell opportunity for BKLN, and Pinnacle just had their best quarter." No login required. No dashboard needed.

**Effort:** 3-4 days (Celery task + GPT summarization + email template)
**Revenue:** Retention feature — makes Signal Studio sticky
**First 3 steps:**
1. Create a Celery task that runs top-N signals against analytical DB
2. Feed results to GPT-4o with "summarize for a wholesaler's morning routine" prompt
3. Send via Resend email with a clean HTML template

---

## 6. 💬 "Ask Your Book" — Natural Language Data Querying
**One-liner:** Let wholesalers ask questions about their book in plain English — "Who are my top 5 growing accounts?" "What's my total Invesco AUM?" — and get instant answers from the analytical DB.

**Why now:** NL→SQL is working. The schema is complete. The only thing missing is an execution layer that runs the generated SQL and returns results as a conversational answer.

**The play:** Different from signal creation. Signals are saved rules that run repeatedly. "Ask Your Book" is ad-hoc querying — like ChatGPT for your financial data. Lower barrier to entry than building signals.

**Effort:** 2-3 days (connect NL→SQL to query execution + result summarization)
**Revenue:** Feature that sells itself in demos — everyone wants to "just ask"
**First 3 steps:**
1. Add /api/query endpoint that generates SQL AND executes it against analytical DB
2. Feed results back to GPT-4o for natural language summarization
3. Add to Signal Studio as a "Ask Your Book" chat interface

---

## 7. 🏗️ "White-Label Signal Studio" — Multi-Tenant SaaS
**One-liner:** Add multi-tenant organization support so Signal Studio can be sold to multiple asset managers, not just Invesco.

**Why now:** The Django backend already has organization_id on every model. The analytical schema already has multi-tenant partitioning (schema_name per org). The infrastructure is there — we just need a signup flow and org isolation in the frontend.

**The play:** Invesco is customer #1. But the same product works for Fidelity, Vanguard, Schwab, any asset manager with wholesalers. Multi-tenant SaaS at $5K-25K/mo per org.

**Effort:** 5-7 days
**Revenue:** $60K-300K/yr per customer
**First 3 steps:**
1. Add organization context to Signal Studio login (which org are you?)
2. Filter all API calls by organization_id
3. Add a simple admin page for org management (use core-admin-ui as template)

---

## 8. 🔍 "Competitive Intelligence Signals" — Track Competitor Moves
**One-liner:** Build signals that detect when advisors are moving money to competitors — AUM declining at Invesco while total MSWM AUM stays flat = money going elsewhere.

**Why now:** The data is literally in the analytical schema. `invesco_current_assets` declining while `mswm_current_assets` stable = competitive displacement. Nobody is surfacing this automatically.

**The play:** "3 advisors moved $4.2M from Invesco to a competitor this month" is the kind of signal that gets a phone call within 5 minutes. This is defend-revenue made actionable.

**Effort:** 1 day (pre-built signal + alert template)
**Revenue:** Direct value — saves revenue
**First 3 steps:**
1. Generate signal: WHERE invesco_current_assets declined >10% AND mswm_current_assets stable
2. Add to Morning Brief as a priority alert
3. Include cross-sell recommendation from DataScienceRecommendation

---

## 9. 📈 "Signal Performance Tracking" — Prove Signals Work
**One-liner:** Track which signals actually led to sales conversations, AUM retention, or new assets — creating a feedback loop that proves ForwardLane's ROI.

**Why now:** The Django backend has feedback models, user_behavior tables, and CRM note tracking. Connect signal triggers to outcomes.

**The play:** "Signals that triggered in Q4 led to $12M in retained AUM and $3M in new assets." This is the data that gets contracts renewed and budgets expanded.

**Effort:** 4-5 days
**Revenue:** Contract renewal insurance — proves ROI
**First 3 steps:**
1. Log every signal trigger with timestamp + advisor + wholesaler
2. Track which triggered advisors had subsequent positive outcomes (CRM notes, sales)
3. Build a simple ROI dashboard showing signals → outcomes

---

## 10. 🤝 "Signal Studio for Salesforce" — Native SF Sidebar App
**One-liner:** Package Signal Studio as a Salesforce Lightning Component that lives in the sidebar — wholesalers see signals, recommendations, and "Ask Your Book" right inside their CRM.

**Why now:** fl-web-widgets already has embeddable React components for Salesforce. Signal Studio has the API. Craig LITERALLY asked for this in the Invesco meeting: "easy buttons in Salesforce."

**The play:** This is the Invesco demo. Not a standalone app. A Salesforce sidebar that shows:
- Today's top signals for this advisor
- Quick actions (schedule call, send content, log note)
- "Ask Your Book" mini-chat
- ML recommendation cards

**Effort:** 5-7 days (Lightning Component wrapping Signal Studio API)
**Revenue:** THE thing that saves the Invesco account
**First 3 steps:**
1. Port fl-web-widgets client-prioritization into a Lightning Web Component
2. Add Signal Studio API calls (signals/generate, schema)
3. Package as a Salesforce AppExchange listing (or direct install)

---

## 🍯 Honey's Ranking — V2

| Priority | Idea | Effort | Impact | Why Now |
|----------|------|--------|--------|---------|
| 🥇 | #3 Invesco Health Dashboard | 2-3 days | Saves $300K account | Craig asked for this |
| 🥈 | #8 Competitive Intel Signals | 1 day | Immediate value | Data already exists |
| 🥉 | #5 Morning Brief | 3-4 days | Retention feature | Celery Beat deploying |
| 4 | #6 Ask Your Book | 2-3 days | Demo-killer feature | NL→SQL works |
| 5 | #2 Signal Copilot | 3-4 days | Core differentiator | Chat sidebar exists |
| 6 | #10 SF Sidebar App | 5-7 days | Invesco deal-closer | fl-web-widgets ready |
| 7 | #1 Signal Marketplace | 2 days | Easy upsell | Can batch-generate |
| 8 | #4 MCP Server | 2 days | Future positioning | API exists |
| 9 | #7 White-Label SaaS | 5-7 days | $$$$ | Org model ready |
| 10 | #9 Performance Tracking | 4-5 days | ROI proof | Longer play |

**My pick:** Do #3 (Health Dashboard) + #8 (Competitive Intel) this week — both directly address Invesco retention and take <4 days combined. Then #5 (Morning Brief) turns Signal Studio from "a tool you log into" into "a tool that comes to you." That's how you make it sticky.
