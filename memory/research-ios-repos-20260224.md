# iOS Repos Research — 2025-02-24

## 1. Chowder iOS (newmaterialco/chowder-iOS)

### What Is It?
A **native iOS chat client for OpenClaw**. It's the first dedicated mobile app that speaks the OpenClaw Gateway Protocol over WebSocket. Think of it as an iPhone-native alternative to talking to your AI assistant through Telegram/Discord.

### Purpose & Features
- Real-time streaming chat with AI via WebSocket to OpenClaw gateway
- **Live Activities** (iOS Dynamic Island / Lock Screen) showing agent thinking steps and tool usage
- Agent identity sync — mirrors IDENTITY.md and USER.md from the OpenClaw workspace
- Persistent local chat history (survives app kills)
- Tool event display: shows thinking steps, tool calls, exec timing inline
- Settings sync — edits to bot identity/user profile write back to workspace files
- Auto-reconnect with 3s backoff
- Debug log viewer (raw WebSocket frames)
- Demo mode for UI testing without a live gateway

### Tech Stack
- **Pure SwiftUI** with `@Observable` macro (iOS 17+)
- MVVM architecture: `ChatViewModel` ↔ `ChatService` via delegate protocol
- `URLSessionWebSocketTask` for WebSocket (no third-party deps)
- `KeychainService` for secure token storage
- `LocalStorage` using `UserDefaults` / JSON files
- **ActivityKit** for Live Activities (separate widget extension target)
- Markdown rendering in `MarkdownContentView`
- **Zero external dependencies** — all native Apple frameworks

### Architecture
```
ChowderApp.swift (entry)
├── Views/
│   ├── ChatView.swift (main chat UI)
│   ├── MessageBubbleView.swift
│   ├── ThinkingShimmerView.swift (agent activity indicator)
│   ├── ActivityStepRow.swift
│   ├── AgentActivityCard.swift
│   ├── ChatHeaderView.swift
│   ├── MarkdownContentView.swift
│   └── SettingsView.swift
├── ViewModels/
│   └── ChatViewModel.swift (~500+ lines, core logic)
├── Models/
│   ├── Message.swift, BotIdentity.swift, UserProfile.swift
│   ├── ConnectionConfig.swift, AgentActivity.swift
│   └── SharedStorage.swift, UserContext.swift
├── Services/
│   ├── ChatService.swift (916 lines — WebSocket + protocol)
│   ├── LiveActivityManager.swift
│   ├── TaskSummaryService.swift
│   ├── LocalStorage.swift
│   └── KeychainService.swift
└── ChowderActivityWidget/ (Live Activity extension)
```

**Total: ~5,174 lines of Swift across 25 files.**

### UI/UX Quality
- Thoughtful touches: haptic feedback on response start, shimmer animations for thinking
- Pagination (50-message pages with "load earlier" support)
- Compact WebSocket log viewer for debugging
- Profile photo customization for the agent
- Clean separation of concerns (MVVM)
- Early-stage but well-structured

### How It Connects to OpenClaw
- **WebSocket** to OpenClaw gateway (requires Tailscale for network access)
- Implements OpenClaw Gateway Protocol: `chat.send`, `chat.history`, identity sync
- Uses `sessionKey` (defaults to `agent:main:main`)
- Device ID tracking for pairing
- History polling at 1s intervals during active agent runs
- Deduplication via sequence numbers and tool call IDs

### Reusable Patterns for OpenClaw iOS Client
1. **WebSocket protocol implementation** in `ChatService.swift` — the entire gateway protocol handshake, message framing, and reconnection logic
2. **Live Activity integration** — showing agent thinking/tool steps on Lock Screen
3. **Identity sync pattern** — pulling IDENTITY.md/USER.md from workspace
4. **Streaming delta handling** — accumulating text deltas into complete messages
5. **Tool event visualization** — inline display of thinking, tool calls, exec results
6. **Reconnection with backoff** — production-ready connection management
7. **Keychain token storage** — secure credential management pattern

### Code Quality: ⭐⭐⭐⭐ (4/5)
- Clean MVVM, zero dependencies, well-documented README
- Early-stage but solid foundation
- Good separation: Services handle protocol, ViewModels handle state, Views handle display
- Minor: `ChatService` at 916 lines could be split; delegate pattern is old-school (Combine/async-await would modernize)

---

## 2. TuitBot (aramirez087/TuitBot)

### What Is It?
An **autonomous X (Twitter) growth automation tool**. It finds relevant conversations, generates AI replies, posts educational content, and publishes weekly threads. Targeted at founders/indie hackers who want autopilot social media growth.

### Purpose & Features
- Auto-discover relevant X conversations by topic/keyword
- AI-generated replies (with approval queue)
- Scheduled tweet posting and weekly thread generation
- Analytics dashboard (30-day follower charts, engagement stats)
- Target account tracking
- Safety/rate-limiting built in
- MCP (Model Context Protocol) server for AI agent integration

### Tech Stack
- **Rust** workspace with 4 crates (~36,278 lines of Rust):
  - `tuitbot-core`: automation engine, X API, LLM integration, scoring, storage
  - `tuitbot-cli`: CLI interface with subcommands (run, tick, approve, stats, auth, settings)
  - `tuitbot-mcp`: MCP server with tools for discovery, replies, analytics, approval
  - `tuitbot-server`: HTTP/WebSocket server for dashboard
- **Dashboard**: SvelteKit + Tauri (45 Svelte components)
  - WebSocket stores, analytics, approval queue, onboarding flow
  - Runs as native desktop app (Tauri) or web UI
- **Three deployment modes**: Desktop (Tauri), Self-hosted (Docker), Cloud (managed)
- SQLite for storage (with migrations)
- TOML config

### Architecture
```
Cargo workspace
├── crates/
│   ├── tuitbot-core/src/
│   │   ├── automation/    (scheduling, execution)
│   │   ├── config/        (TOML settings)
│   │   ├── content/       (tweet/thread generation)
│   │   ├── llm/           (AI integration)
│   │   ├── safety/        (rate limits, content filtering)
│   │   ├── scoring/       (engagement prediction)
│   │   ├── storage/       (SQLite)
│   │   └── x_api/         (Twitter API client)
│   ├── tuitbot-cli/       (CLI commands)
│   ├── tuitbot-mcp/       (MCP server - 12 tool modules)
│   └── tuitbot-server/    (HTTP + WebSocket)
├── dashboard/             (SvelteKit + Tauri)
│   ├── src/lib/stores/    (websocket, analytics, approval, etc.)
│   └── src/lib/components/ (45 Svelte components)
├── plugins/               (extensibility)
├── migrations/            (SQLite)
└── docs/                  (MkDocs)
```

### UI/UX Quality
- Full-featured Svelte dashboard with visual approval queue
- Onboarding flow (multi-step setup wizard)
- Real-time WebSocket updates
- Calendar view for scheduled content
- Theme support
- Professional-grade for an indie tool

### How It Could Connect to OpenClaw
- **MCP Server** (`tuitbot-mcp`) — already exposes 12+ tools via MCP protocol. Could be registered as an OpenClaw skill/tool
- **WebSocket** — the dashboard server already speaks WS, could bridge to OpenClaw
- Could be wrapped as an OpenClaw skill: "post a tweet", "find conversations about X", "show my X analytics"
- The approval queue could integrate with OpenClaw's chat — "approve this reply?" in Telegram

### Reusable Patterns
1. **MCP implementation in Rust** — clean tool registration pattern
2. **Approval queue workflow** — AI generates, human reviews, system posts
3. **WebSocket dashboard pattern** — SvelteKit stores + Rust WS server
4. **Safety/rate-limiting** — content filtering and API throttling
5. **Multi-deployment architecture** — same core, multiple frontends (desktop/web/cloud)
6. **Scoring/analytics engine** — engagement prediction models

### Code Quality: ⭐⭐⭐⭐½ (4.5/5)
- Well-organized Rust workspace with clear crate boundaries
- 36K lines of Rust — substantial, production-oriented
- CI/CD with release-plz, proper CHANGELOG
- MkDocs documentation site
- CLAUDE.md present (AI-assisted development conventions)
- Professional engineering: migrations, config management, safety layer

---

## Comparison & Synthesis

| Aspect | Chowder iOS | TuitBot |
|--------|-------------|---------|
| Language | Swift (SwiftUI) | Rust + SvelteKit |
| Size | ~5K lines | ~36K lines Rust + Svelte |
| Dependencies | Zero (all native) | Minimal for Rust |
| OpenClaw relation | **Direct client** — speaks gateway protocol | **Potential skill** — MCP server |
| Maturity | Early alpha | Near-production |
| Key innovation | Live Activities for AI agents | MCP + approval queue workflow |

### Key Takeaways for OpenClaw iOS Development
1. **Chowder IS the reference implementation** — it already implements the full OpenClaw gateway WebSocket protocol. Any iOS client should start here.
2. The Live Activity pattern (showing agent thinking on Lock Screen) is genuinely novel and should be preserved.
3. TuitBot's MCP server pattern shows how OpenClaw skills could expose complex automation tools.
4. TuitBot's approval queue could inspire an OpenClaw pattern: AI proposes actions, user approves via mobile.
5. Both repos demonstrate clean architecture without over-engineering — good templates for OpenClaw ecosystem projects.
