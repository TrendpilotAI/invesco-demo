# Google Agent to Agent (A2A) Protocol

## What is A2A?

Google's **Agent to Agent (A2A)** protocol is an open standard for AI agents to communicate with each other. Think of it like HTTP for agents — a common protocol so different AI agents can talk to each other regardless of framework.

## Key Concepts

### 1. Agent Card
Each agent publishes a JSON "Agent Card" describing:
- Capabilities (what it can do)
- Skills (specific functions)
- Authentication requirements
- Endpoint URL

### 2. Task Protocol
Agents exchange "Tasks" with:
- Unique task ID
- Status (submitted, working, completed, failed)
- Messages (context/results)
- Artifacts (outputs)

### 3. Push Notifications
Agents can subscribe to task updates instead of polling.

---

## Our Signal Agent + A2A

We could use A2A to:

| Use Case | How It Works |
|----------|---------------|
| Multi-agent research | Signal Agent asks Research Agent for client data |
| Specialist agents | Separate agents for: Book Analyst, Email Writer, SMS Sender |
| External tools | Connect to MCP servers via A2A |
| Scalability | Agents on different machines communicate via A2A |

---

## Implementation Options

### Option 1: Build Our Own A2A Server
Simple implementation for our needs:
```typescript
// A2A server in Next.js
app/api/a2a/route.ts

// Agent card
const agentCard = {
  name: "Signal Agent",
  url: "https://signal-studio-production.up.railway.app/api/a2a",
  skills: [
    { id: "analyze_book", name: "Analyze Book" },
    { id: "research_client", name: "Research Client" },
    { id: "draft_email", name: "Draft Email" },
  ]
}
```

### Option 2: Use MCP + A2A Bridge
Mastra has built-in A2A support. Could switch when stable.

### Option 3: Simple Webhook Pattern
For now, simpler than full A2A:
```
Signal Agent → POST to other agent → Get response
```

---

## Recommendation

**Stay with Vercel AI SDK for now.** A2A is very new (2025), ecosystem still maturing. Our current approach works.

**Future migration path:**
1. When Mastra adds stable A2A support → migrate
2. Or build simple A2A server if we need multi-agent coordination

The Signal Agent as-is handles our current needs. A2A becomes valuable when we have multiple specialized agents that need to collaborate.

---

## Resources

- Google A2A GitHub: github.com/google/A2A
- Protocol spec: A2A Protocol (JSON-RPC based)
- Similar to: Anthropic's MCP, OpenAI's ChatDB
