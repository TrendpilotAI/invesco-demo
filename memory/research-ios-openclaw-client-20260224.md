# iOS OpenClaw Client Research — 2026-02-24

## Executive Summary

**BlueClaw is the clear winner.** It's a native iOS client built *specifically* for OpenClaw gateways, with WebSocket connectivity, SSH tunneling, voice input, markdown rendering, session management, and security features. The other repos are useful as UI/UX inspiration but none come close to BlueClaw's OpenClaw-native architecture.

---

## Top 10 Repos Evaluated

### 1. 🏆 brandon-dacrib/blueclaw (4⭐) — **THE ONE**
- **What:** Native iOS client for OpenClaw gateways
- **Tech:** SwiftUI, iOS 18+, URLSessionWebSocketTask, SSH tunneling (Citadel), SwiftData
- **Features:** WebSocket to OpenClaw gateway, SSH tunnel support, QR code setup, voice input, markdown rendering, session management, agent picker, security audit, usage/token tracking, biometric auth, content scanning (PII/secrets), dark mode
- **Architecture:** Clean MVVM — Protocol/ (wire types), Services/ (WebSocket, SSH, Keychain), ViewModels/, Views/
- **52 Swift files**, all SwiftUI, proper streaming, OpenClaw protocol types already defined
- **License:** Private (all rights reserved) — would need to contact author or rewrite
- **Rating:** UI Beauty: 7 | Code Quality: 9 | OpenClaw Compatibility: 10 | Effort to Adapt: 1 (it's already built for OpenClaw)

### 2. CherryHQ/hanlin-ai (204⭐) — Best Feature-Rich Alternative
- **What:** "Cherry Studio" iOS companion — AI mobile workstation
- **Tech:** SwiftUI, Swift 5.9+, SwiftData + CloudKit, URLSession async/await
- **Features:** 20+ AI providers, streaming responses, RAG knowledge base, voice TTS, camera/vision, tools ecosystem (weather, calendar, health, code execution), smart canvas, long-term memory
- **60 Swift files**, 28 SwiftUI views, 12 streaming files, 9 voice files, 17 markdown files
- **License:** MIT ✅
- **Rating:** UI Beauty: 8 | Code Quality: 8 | OpenClaw Compatibility: 4 | Effort to Adapt: 6

### 3. SilverMarcs/GPTalks (48⭐) — Best Multi-Platform UI
- **What:** Multi-platform LLM API client (iOS/iPadOS/macOS/visionOS)
- **Tech:** Pure SwiftUI (53/55 files are SwiftUI), SwiftData
- **Features:** Multiple providers, markdown rendering, image generation, conversation management, clean UI
- **License:** GPL-3.0
- **Rating:** UI Beauty: 8 | Code Quality: 8 | OpenClaw Compatibility: 3 | Effort to Adapt: 7

### 4. Panl/AICat (284⭐) — Solid Multi-Platform Chat
- **What:** Multiplatform ChatGPT client (iOS/iPadOS/macOS)
- **Tech:** SwiftUI, iCloud sync, in-app purchases
- **Features:** Chat with prompts, command mode (Telegram-inspired), export markdown, code blocks, iCloud sync
- **39 Swift files**, 27 SwiftUI views
- **License:** MIT ✅
- **Rating:** UI Beauty: 7 | Code Quality: 7 | OpenClaw Compatibility: 3 | Effort to Adapt: 7

### 5. 37MobileTeam/iChatGPT (976⭐) — Most Popular
- **What:** ChatGPT native iOS/iPadOS/macOS app
- **Tech:** SwiftUI, streaming
- **22 Swift files**, relatively simple
- **Rating:** UI Beauty: 6 | Code Quality: 6 | OpenClaw Compatibility: 2 | Effort to Adapt: 8

### 6. alfianlosari/ChatGPTSwiftUI (690⭐) — Good Learning Reference
- **What:** ChatGPT native app for iOS/macOS/watchOS/tvOS
- **Features:** Streaming, markdown, voice (2 files), multi-platform
- **Rating:** UI Beauty: 7 | Code Quality: 7 | OpenClaw Compatibility: 2 | Effort to Adapt: 8

### 7. alfianlosari/ChatGPTUI (60⭐) — Drop-in UI Component
- **What:** Reusable ChatGPT UI component for iOS/macOS/visionOS
- **Features:** Markdown rendering (9 files), voice (3 files), drop-in solution
- **Rating:** UI Beauty: 7 | Code Quality: 7 | OpenClaw Compatibility: 3 | Effort to Adapt: 6

### 8. Dimillian/FoundationChat (313⭐) — iOS 26 On-Device
- **What:** Chat app using iOS 26 Foundation Models (on-device LLM)
- **Tech:** Latest SwiftUI, iOS 26 FoundationModels framework
- **15 Swift files**, very clean modern code
- **Rating:** UI Beauty: 8 | Code Quality: 9 | OpenClaw Compatibility: 1 | Effort to Adapt: 9

### 9. mbabicz/SwiftGPT (135⭐)
- **What:** iOS ChatGPT + DALL-E app
- **17 Swift files**, basic
- **Rating:** UI Beauty: 5 | Code Quality: 5 | OpenClaw Compatibility: 2 | Effort to Adapt: 8

### 10. 31d4r/Raven (169⭐)
- **What:** Document chat app (local RAG on macOS/iOS)
- **Focus:** Document upload + local inference, not cloud chat
- **Rating:** UI Beauty: 6 | Code Quality: 7 | OpenClaw Compatibility: 2 | Effort to Adapt: 9

---

## Recommendation

### Strategy: Fork BlueClaw or Negotiate License

**Option A: Contact BlueClaw author** (Recommended)
- BlueClaw is *already* an OpenClaw iOS client with WebSocket, SSH tunneling, voice, markdown, sessions
- It has the full OpenClaw wire protocol implemented (Frame, Methods, ConnectParams, AgentTypes, SessionTypes)
- License is "Private — all rights reserved" but author clearly built it for the OpenClaw ecosystem
- Reach out to negotiate open-sourcing or licensing

**Option B: Rewrite inspired by BlueClaw + Hanlin-AI**
- Use BlueClaw's architecture as the blueprint (Protocol/, Services/, ViewModels/, Views/)
- Borrow UI polish from Hanlin-AI (MIT licensed) — especially their markdown rendering, voice, and tool ecosystem
- Use GPTalks for multi-platform SwiftUI patterns

**Option C: Fork Hanlin-AI (MIT) and add OpenClaw connectivity**
- Already has streaming, voice, markdown, 60 Swift files of polished UI
- Would need: WebSocket service → OpenClaw gateway, session management, agent switching
- Estimated 2-3 weeks of work

### Top 3 Repos to Fork/Adapt

| Rank | Repo | Why | License |
|------|------|-----|---------|
| 1 | **brandon-dacrib/blueclaw** | Already OpenClaw-native, full protocol, WebSocket+SSH | Private ⚠️ |
| 2 | **CherryHQ/hanlin-ai** | Most feature-rich, great UI, MIT license | MIT ✅ |
| 3 | **SilverMarcs/GPTalks** | Cleanest SwiftUI, multi-platform, good UX | GPL-3.0 |

---

## Ideal OpenClaw iOS App Architecture

```
OpenClawMobile/
├── Protocol/           # OpenClaw wire protocol (from BlueClaw pattern)
│   ├── Frame.swift           # JSON-RPC frame encoding/decoding
│   ├── Methods.swift         # chat.send, session.list, agent.list, etc.
│   ├── ConnectParams.swift   # Gateway connection parameters
│   └── AgentTypes.swift      # Agent, Session, Message types
├── Services/
│   ├── WebSocketService.swift    # URLSessionWebSocketTask → ws://gateway:18789
│   ├── SSHTunnelService.swift    # Optional SSH tunnel (Citadel library)
│   ├── KeychainService.swift     # Credential storage
│   ├── VoiceService.swift        # Deepgram STT + system TTS
│   ├── NotificationService.swift # APNs push notifications
│   └── BiometricService.swift    # Face ID / Touch ID
├── ViewModels/
│   ├── AppState.swift            # Root state, connection status
│   ├── ChatViewModel.swift       # Message streaming, send/receive
│   ├── SessionViewModel.swift    # Multi-session management
│   └── VoiceViewModel.swift      # Voice input/output state
├── Views/
│   ├── Chat/
│   │   ├── ChatView.swift            # Main chat interface
│   │   ├── MessageBubbleView.swift   # Rich message rendering
│   │   ├── MarkdownTextView.swift    # Code blocks, links, images
│   │   └── MessageInputView.swift    # Text + voice + attachments
│   ├── Sessions/
│   │   ├── SessionListView.swift     # Sidebar session list
│   │   └── SessionRowView.swift      # Session preview row
│   ├── Connection/
│   │   ├── ConnectionSetupView.swift # Gateway URL, QR scan
│   │   └── QRScannerView.swift       # Quick setup via QR
│   ├── Voice/
│   │   ├── VoiceView.swift           # Full-screen voice mode
│   │   └── VoiceOrbView.swift        # Animated voice indicator
│   └── Settings/
│       ├── SettingsView.swift
│       └── SecurityAuditView.swift
└── Theme/
    └── Colors.swift              # Dark/light mode palette
```

### Key Technical Decisions

1. **WebSocket to Gateway:** `ws://[gateway-ip]:18789/ws` — use `URLSessionWebSocketTask` (native, no dependencies)
2. **Streaming:** OpenClaw streams via WebSocket frames — parse JSON-RPC responses incrementally
3. **Voice Input:** Deepgram Nova-3 STT via WebSocket (already configured in OpenClaw) or Apple Speech framework as fallback
4. **Markdown:** Use `swift-markdown-ui` package (MarkdownUI) for rich content rendering with code syntax highlighting
5. **Push Notifications:** APNs via gateway webhook — gateway sends push when agent mentions user or completes long task
6. **Multi-Session:** OpenClaw supports multiple agent sessions — list via `session.list`, switch via session key
7. **Offline:** Cache recent messages in SwiftData, sync on reconnect

### Estimated Effort

| Approach | Timeline | Notes |
|----------|----------|-------|
| Use BlueClaw as-is | 1-2 days | Just configure gateway URL, test |
| Fork BlueClaw + polish | 1-2 weeks | Add push notifications, improve UI |
| Fork Hanlin-AI + add OpenClaw | 2-3 weeks | Rewrite networking layer, add protocol |
| Build from scratch | 4-6 weeks | Using BlueClaw architecture as blueprint |

### Must-Have Features for v1

- [x] Connect to OpenClaw gateway via WebSocket (port 18789)
- [x] Stream chat responses in real-time
- [x] Markdown rendering (code blocks, links, bold/italic)
- [x] Multi-agent support (switch between agents)
- [x] Session management (list, create, switch)
- [x] Dark mode + light mode
- [x] Voice input (Deepgram STT or Apple Speech)
- [ ] Push notifications (needs APNs integration in gateway)
- [ ] Image attachments (camera + photo library)
- [ ] Haptic feedback on message send/receive

### Nice-to-Have for v2

- Sub-agent visualization (see spawned tasks)
- Tool call rendering (show tool use inline)
- Cron job management
- Gateway health dashboard
- Multi-gateway support
- iPad split-view layout
- Apple Watch companion (quick voice messages)

---

## Conclusion

**BlueClaw is the answer.** Someone already built exactly what we need — a native iOS client for OpenClaw with WebSocket, SSH tunneling, voice, markdown, and the full protocol stack. The 4-star count is misleading; it's a well-architected 52-file SwiftUI app with proper MVVM, security features, and OpenClaw protocol types.

Contact the author. If that fails, use BlueClaw's architecture as a blueprint and Hanlin-AI's MIT-licensed UI components to build a new client in 2-3 weeks.
