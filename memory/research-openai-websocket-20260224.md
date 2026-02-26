# OpenAI WebSocket Mode — Analysis for Honey AI / OpenClaw

**Date:** 2026-02-24  
**Source:** https://developers.openai.com/api/docs/guides/websocket-mode

---

## 1. What Is WebSocket Mode?

OpenAI's Responses API now supports a **persistent WebSocket connection** at `wss://api.openai.com/v1/responses`. Instead of making individual HTTP POST requests for each turn, you:

1. Open a single WebSocket connection
2. Send `response.create` events with your prompt/tools
3. Use `previous_response_id` to chain turns without resending full conversation history
4. Receive streamed events back on the same connection

**Key differentiator:** The server retains conversation state via `previous_response_id`, so you only send incremental inputs — not the full context window each time.

---

## 2. Latency Savings Estimate for Our Setup

### OpenAI's Claim
- **Up to 40% faster end-to-end** for workflows with 20+ tool calls

### Our Profile
- Agents average **20-30 tool calls per session** (shell, read, write, edit)
- Each tool call currently = separate HTTP request with full context resend
- Codex 5.3 orchestrator spawns 4-6 sub-agents, each with their own tool loops

### Estimated Savings

| Source of Latency Reduction | Estimated Impact |
|---|---|
| **Eliminate TCP/TLS handshake per turn** | ~50-100ms × 25 turns = **1.25-2.5s** |
| **No full context resend** (previous_response_id) | ~200-500ms × 25 turns = **5-12.5s** (token processing savings) |
| **Connection keep-alive** (no cold starts) | ~100-300ms saved on reconnects |
| **Server-side state caching** | Reduced TTFT across turns |

**Conservative estimate: 15-25% latency reduction per agent session**  
**Optimistic estimate: 30-40% for heavy tool-call workflows (20+ calls)**

For a typical 25-tool-call session that takes ~60s today:
- Conservative: saves **9-15 seconds**
- Optimistic: saves **18-24 seconds**

Across daily judge swarms (15 judges × ~3 sub-agents each = ~45 agent sessions), this could save **7-18 minutes per swarm run**.

---

## 3. Could OpenClaw Integrate WebSocket Mode?

### Yes, and here's how it maps:

OpenClaw's gateway already proxies model API calls. The integration path:

1. **Gateway maintains WebSocket pools** to OpenAI per-model
2. When an agent session starts with an OpenAI model, gateway opens a WS connection
3. Subsequent turns from the agent use `previous_response_id` instead of full context replay
4. Gateway manages connection lifecycle (keepalive, reconnect, timeout)

### Compatibility
- ✅ Compatible with `store=false` (ZDR — zero data retention)
- ✅ Compatible with streaming (events come over the WS)
- ✅ Works with function calling / tool use
- ✅ Works with all Responses API models (GPT-5.x, o-series)
- ⚠️ Only for OpenAI models — Anthropic, DeepSeek etc. still use HTTP

### Complexity: **Medium**
- Requires WebSocket client in the gateway (Node.js `ws` library)
- Need connection pool management (max connections, idle timeout)
- Need to handle WS disconnects gracefully (fallback to HTTP)
- Need to map OpenClaw's session concept to `previous_response_id` chains

---

## 4. Benefit to Codex 5.3 Orchestrator

**High benefit.** The orchestrator pattern is exactly what WebSocket mode targets:

- Codex 5.3 spawns sub-agents → each sub-agent runs a multi-turn tool loop
- Currently: each turn = HTTP POST with growing context window
- With WS mode: each turn = lightweight `response.create` event, server handles state

**Specific improvements:**
- Sub-agent spin-up would be faster (reuse orchestrator's WS connection or pre-warm)
- Tool call loops (10-30 calls) see the biggest improvement
- `previous_response_id` eliminates context window growth cost on the client side
- Server-side prompt caching likely more effective with persistent connections

**Caution:** Each sub-agent likely needs its own response chain (separate `previous_response_id` lineage). The orchestrator connection could multiplex or use separate connections per sub-agent.

---

## 5. Cost Implications

### Token Pricing: **No change**
- WebSocket mode uses the same per-token pricing as HTTP
- Input/output token costs remain identical

### Potential Cost Savings:
- **Prompt caching hits more often** with persistent connections → cached input tokens are 50% cheaper
- **Less redundant token processing** (not resending full history each turn) → fewer input tokens billed
- For a 25-turn session with 4K context growing to 20K:
  - HTTP mode: ~25 × avg(12K) = **300K input tokens**
  - WS mode with previous_response_id: ~25 × avg(2K new) = **50K input tokens** + server-side state
  - **Potential 80% reduction in billed input tokens** (if server-side state means they don't re-bill stored context)

⚠️ **Important caveat:** Need to verify whether `previous_response_id` actually reduces billed input tokens or just reduces transfer overhead. OpenAI's docs suggest the server reconstructs context internally, which may or may not be billed differently. If it's just transport optimization (still billed for full context), the cost savings are minimal — just latency.

---

## 6. WebSocket Mode vs Current HTTP Streaming

| Dimension | HTTP Streaming (Current) | WebSocket Mode |
|---|---|---|
| **Connection** | New per request | Persistent |
| **Context handling** | Full resend each turn | `previous_response_id` (incremental) |
| **Latency (per turn)** | TCP+TLS+context overhead | Near-zero overhead |
| **Streaming** | SSE (Server-Sent Events) | Native WS events |
| **Multi-turn efficiency** | O(n²) context growth | O(n) incremental |
| **Failure handling** | Simple retry | Need reconnect logic |
| **Provider support** | Universal | OpenAI only |
| **Complexity** | Low | Medium |
| **Best for** | Single-turn, multi-provider | Heavy tool-call loops, OpenAI-specific |

### Recommendation
Use **WebSocket mode for OpenAI model sessions with >5 tool calls**. Keep HTTP streaming for:
- Single-turn completions
- Non-OpenAI providers (Anthropic, DeepSeek, etc.)
- Simple Q&A without tool loops

---

## 7. Realtime API / Ultrafone Connection

WebSocket mode for the Responses API is **separate from** the Realtime API, but they share concepts:

| Feature | Responses API WS Mode | Realtime API |
|---|---|---|
| **Transport** | WebSocket | WebSocket / WebRTC |
| **Content** | Text + tool calls | Audio + text + tool calls |
| **Use case** | Agentic coding/orchestration | Voice conversations |
| **Ultrafone relevance** | Indirect | Direct |

### For Ultrafone:
- The **Realtime API** (already WebSocket-based) is the right choice for voice features
- Responses API WS mode doesn't add voice capabilities
- However, learnings from implementing WS connection pooling in OpenClaw would directly apply to Realtime API integration
- Could share connection management infrastructure

### Recommendation for Ultrafone:
Build the WS infrastructure for Responses API first (simpler, text-only), then extend the same patterns for Realtime API voice features.

---

## 8. Implementation Plan

### Phase 1: Proof of Concept (1-2 days)
1. Add `ws` dependency to OpenClaw gateway
2. Create a `WebSocketModelClient` class that:
   - Opens WS to `wss://api.openai.com/v1/responses`
   - Sends `response.create` events
   - Handles response streaming events
   - Tracks `previous_response_id` per session
3. Test with a single agent session manually

### Phase 2: Gateway Integration (2-3 days)
1. Add WS connection pool to gateway config
2. Route OpenAI model calls through WS when:
   - Model is OpenAI (gpt-5.x, o-series)
   - Session has >1 turn
   - Feature flag is enabled
3. Implement fallback to HTTP on WS failure
4. Add metrics: latency comparison, connection pool stats

### Phase 3: Session Management (1-2 days)
1. Map OpenClaw session IDs → `previous_response_id` chains
2. Handle session cleanup (close WS on session end)
3. Handle connection limits (OpenAI likely has per-org WS limits)
4. Test with Codex 5.3 orchestrator + sub-agents

### Phase 4: Production Rollout (1 day)
1. Feature flag rollout: 10% → 50% → 100% of OpenAI sessions
2. Monitor latency, error rates, cost
3. A/B test: WS vs HTTP for agent performance metrics

### Total estimate: **5-8 days of engineering work**

---

## 9. Concrete Recommendations

### ✅ Do Now
1. **Enable `previous_response_id`** in HTTP mode first — this alone saves context resend overhead without needing WebSocket infrastructure
2. **Audit current agent latency** — instrument tool-call loop timing to establish baseline

### ✅ Do Soon (Next Sprint)
3. **Build WS proof of concept** in gateway for OpenAI models
4. **Test with judge swarms** — highest volume, most tool calls, easiest to measure

### ✅ Do Later
5. **Connection pooling + production hardening**
6. **Extend WS patterns to Realtime API** for Ultrafone voice features
7. **Evaluate if Anthropic/others add similar WS modes** — keep the abstraction generic

### ⛔ Don't Do
- Don't rewrite the entire gateway around WebSockets — HTTP is fine for most calls
- Don't assume cost savings without verifying billing model for `previous_response_id`
- Don't use WS for single-turn calls (overhead > benefit)

---

## 10. Key Risks

| Risk | Mitigation |
|---|---|
| OpenAI WS connection limits | Start with pool of 5-10, scale based on usage |
| WS disconnects mid-session | Fallback to HTTP with full context resend |
| `previous_response_id` state expiry | Handle gracefully, restart chain from last known state |
| Increased gateway complexity | Feature flag, good abstractions, HTTP fallback |
| Vendor lock-in (OpenAI only) | Keep HTTP path as default, WS as optimization layer |

---

## Summary

**WebSocket mode is a strong fit for our multi-agent, heavy-tool-call workload.** Expected 15-40% latency improvement for agent sessions, with the biggest wins in:
- Judge swarms (15 judges × many tool calls)
- Codex 5.3 orchestrator loops
- Debug/Ops/QA agent chains

Implementation effort is moderate (5-8 days) with low risk (HTTP fallback always available). Recommend starting with `previous_response_id` in HTTP mode as a quick win, then building full WS support.
