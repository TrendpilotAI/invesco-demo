# Competitor Deep Dive: MedGemma Impact Challenge

**Date:** 2026-02-17 | **Total repos found:** ~70+ | **Deep-analyzed:** 15

---

## Executive Summary

The competition field is **wide but shallow**. Most repos (~80%) are basic Streamlit/Gradio wrappers around MedGemma with minimal innovation. Only 5-6 repos show genuine sophistication. The biggest gap: **nobody is doing multi-model second-opinion with real clinical reasoning depth**. Most are single-use-case tools (CXR triage, skin lesion, discharge summaries). Our "Second Opinion" concept — giving patients a genuinely useful AI second opinion across modalities — is differentiated.

---

## Top 15 Repos: Summary Table

| # | Repo | Approach | HAI-DEF Models | Sophistication | UI | ⭐ |
|---|------|----------|---------------|---------------|----|----|
| 1 | **weekijie/Sturgeon** | House MD diagnostic debate AI | MedGemma 4B + MedSigLIP + Gemini orchestrator | ⭐⭐⭐⭐⭐ | Next.js + FastAPI | 0 |
| 2 | **Amo-Zeng/clinicaflow-medgemma** | 5-agent deterministic triage pipeline | MedGemma (via vLLM) | ⭐⭐⭐⭐⭐ | CLI + demo server + Docker | 0 |
| 3 | **ProfRandom92/medgemma-comptext-showcase** | 94% token compression for clinical text | MedGemma + agent trio | ⭐⭐⭐⭐ | Streamlit dashboard + API | 0 |
| 4 | **Sayandip05/PathRad-AI** | Multi-agent radiology + pathology | MedGemma 4B + CXR Foundation + Path Foundation | ⭐⭐⭐⭐ | React + FastAPI + WebSockets | 0 |
| 5 | **734ai/ClinAssist-Edge** | Offline clinical decision support | MedGemma 2B (quantized) + FAISS RAG | ⭐⭐⭐⭐ | Streamlit | 0 |
| 6 | **Samarpeet/RadioFlow** | Multi-agent radiology workflow | CXR Foundation + MedGemma 4B | ⭐⭐⭐ | Gradio | 0 |
| 7 | **CharlieKingOfTheRats/Medevac-Gemma** | Military TCCC push-to-talk assistant | MedGemma (fine-tuned GGUF) + MedASR | ⭐⭐⭐⭐ | CLI push-to-talk | 0 |
| 8 | **naividh/voicerad** | Voice-controlled mobile radiology PWA | MedGemma 1.5 4B + MedASR | ⭐⭐⭐⭐ | React PWA + FastAPI | 0 |
| 9 | **bushra-aljohani/clinexa** | Hybrid RAG with temporal intelligence | TXGemma 9B + PubMed APIs | ⭐⭐⭐ | Streamlit | 0 |
| 10 | **kabirrgrover/skin-lesion-triage** | Skin cancer detection across skin tones | MedSigLIP-448 + MedGemma 4B | ⭐⭐⭐⭐ | — | 0 |
| 11 | **vbookshelf/Offline-MedAi-Console** | Offline multimodal AI console | MedGemma 4B (via Ollama) + Whisper + Kokoro TTS | ⭐⭐⭐⭐ | Flask single-file app | 0 |
| 12 | **Faiz2807/BreastEdge-AI** | Edge breast cancer histopathology | MedSigLIP + ResNet50/MONAI + MedGemma | ⭐⭐⭐⭐ | FastAPI dashboard | 0 |
| 13 | **Fflow021/EsmeraldaMVP** | Chat interface with Gemini + MedGemma | MedGemma service | ⭐⭐ | React/Vite | 1 |
| 14 | **intellidoctor/medgemma-triage** | Brazilian SUS ER triage | MedGemma + FHIR | ⭐⭐⭐ | — | 0 |
| 15 | **K-Himanshu/agentic-discharge-copilot** | Post-discharge recovery plans | MedGemma | ⭐⭐ | CLI | 0 |

---

## Feature Matrix

| Feature | Sturgeon | ClinicaFlow | CompText | PathRad | ClinAssist | RadioFlow | VoiceRad | Offline Console | **Second-Opinion (Us)** |
|---------|----------|-------------|----------|---------|------------|-----------|----------|----------------|----------------------|
| Multi-agent pipeline | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Multi-modal (image+text) | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| MedGemma | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CXR Foundation | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Path Foundation | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| MedSigLIP | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Derm Foundation | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Voice input | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ? |
| RAG/guidelines | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Hallucination checks | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Offline/edge capable | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ |
| Safety gating | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Audit trail | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| FHIR integration | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ? |
| Fine-tuning | ❌ | ❌ | ❌ | ❌ | ✅ (LoRA) | ❌ | ❌ | ❌ | ? |
| Benchmarks/eval | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Fairness across demographics | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ? |
| Polished production UI | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |

---

## Detailed Analysis of Top 5 Threats

### 1. Sturgeon (weekijie/Sturgeon) — 🏆 BIGGEST THREAT

**Approach:** "House MD diagnostic debate" — Gemini orchestrates, MedGemma is the medical specialist tool. User uploads images/labs, gets differential, then *challenges the AI* in a debate format.

**What's clever:**
- Dual-model architecture (Gemini as orchestrator, MedGemma as specialist) — exactly what "agentic" means
- RAG with clinical guidelines + citation URLs (WHO, CDC, USPSTF)
- Hallucination detection with auto-retry
- MedSigLIP for fast image triage before deep analysis
- Rate limiting with visual feedback
- Session persistence
- Next.js frontend is polished

**What's wrong:**
- Only does differential diagnosis — no treatment plans, no patient education
- No multi-specialty coverage (no path, no derm, no audio)
- No fairness evaluation
- The "debate" is gimmicky — clinicians don't want to argue with AI
- No FHIR/EHR integration

**How to beat:** Our multi-model pipeline covers more HAI-DEF models (CXR + Path + Derm + MedSigLIP + MedGemma). Add a "reasoning chain" that shows debate-like transparency without requiring user to argue.

---

### 2. ClinicaFlow (Amo-Zeng/clinicaflow-medgemma) — BEST ENGINEERING

**Approach:** Deterministic 5-agent pipeline: Intake → Reasoning → Evidence/Policy → Safety → Communication. Competition-ready with benchmarks, audit bundles, Docker, CI/CD, CLI tools.

**What's clever:**
- Most production-ready codebase in the competition
- Audit bundles with SHA256 hashes for compliance
- Vignette regression tests (n=30) to catch under-triage
- Policy pack system (swappable clinical protocols)
- Kubernetes-ready (health/live/ready probes)
- One-click demo script
- Great documentation

**What's wrong:**
- Current code uses **deterministic logic** (regex matching) — MedGemma integration is optional/not default
- No image analysis at all — text-only triage
- No UI to speak of (CLI/API only)
- Overengineered for a hackathon — feels like a product scaffold, not a demo

**How to beat:** Our actual AI inference with multiple HAI-DEF models is more impressive than their deterministic scaffolding. But steal their audit trail and benchmark ideas.

---

### 3. CompText (ProfRandom92/medgemma-comptext-showcase) — MOST INNOVATIVE IDEA

**Approach:** Compress clinical text by 94% using KVTC "sandwich strategy" — preserve headers and recent context losslessly, compress the middle. Three-agent system (triage, nurse, doctor).

**What's clever:**
- Novel compression approach with clear before/after examples
- "15x cheaper inference" is a compelling pitch
- MCP server integration
- CI/CD pipeline
- Good marketing (badges, comparisons, metrics)

**What's wrong:**
- The actual compression is just regex extraction + JSON structuring — not that novel
- No image analysis
- Triage agent is rule-based (HR > 120 = critical), not ML
- Overpromises ("94% reduction") for what's essentially structured data extraction
- No clinical validation

**How to beat:** Our approach is fundamentally different — we actually run HAI-DEF models. Their compression idea could be a useful optimization layer though.

---

### 4. PathRad-AI (Sayandip05/PathRad-AI) — BEST MODEL COVERAGE

**Approach:** Multi-agent system with radiologist, pathologist, and clinical context agents. Uses Google ADK for orchestration. React frontend with WebSocket real-time updates.

**What's clever:**
- Uses **3 HAI-DEF foundation models** (MedGemma + CXR Foundation + Path Foundation)
- Google ADK for agent orchestration (signals awareness of Google's ecosystem)
- WebSocket real-time processing updates
- Whisper for voice input
- Confidence gating with human-in-the-loop thresholds
- PDF report generation

**What's wrong:**
- Very TB-focused (orchestrator prompt is heavily TB-specific)
- No derm, no ophthalmology
- No fairness evaluation
- Frontend may be incomplete (need React setup)

**How to beat:** We need to match their model coverage AND go wider (add Derm Foundation, MedSigLIP). Their Google ADK usage is a smart signal — we should consider it.

---

### 5. Medevac-Gemma (CharlieKingOfTheRats/Medevac-Gemma) — MOST UNIQUE NICHE

**Approach:** Offline push-to-talk military medic assistant. Fine-tuned MedGemma with LoRA for TCCC protocols, fine-tuned MedASR for military medical terminology, GGUF quantization for edge.

**What's clever:**
- Actually fine-tuned both MedGemma AND MedASR (with training notebooks)
- Real niche use case (combat medics) that judges will remember
- Sub-7s response time
- 100% offline — runs on Mac Mini M1
- Speech-to-speech pipeline

**What's wrong:**
- Very narrow use case — only military TCCC
- Mac-only (macOS TTS dependency)
- No image analysis
- Small team, limited polish

**How to beat:** Different category. Their fine-tuning notebooks are worth studying though.

---

## Google's Demo Spaces — What Google WANTS to See

### 1. `google/ehr-navigator-agent-with-medgemma`
**What it does:** Agent navigates FHIR EHR data. Plans what info to fetch, retrieves step-by-step, extracts key facts, synthesizes answers.
**Signal:** Google wants to see **FHIR integration** and **agentic step-by-step reasoning** with MedGemma. The agent PLANS before acting.

### 2. `google/appoint-ready`
**What it does:** Pre-visit intake chatbot. MedGemma asks patient questions, collects info, generates pre-visit report from chat + FHIR records. Includes self-evaluation.
**Signal:** Google wants **patient-facing conversational AI** that creates clinical-grade outputs. The self-evaluation is key — they want models that can assess their own quality.

### 3. `google/rad_explain`
**What it does:** Click any sentence in a radiology report → MedGemma explains it in simple language + highlights the relevant area on the CXR image.
**Signal:** Google wants **explainability** and **patient education**. Click-to-explain with visual grounding is their ideal UX. Uses MedGemma-4B multimodal.

### Key Themes from Google:
1. **FHIR/EHR integration** — they built their own demo around it
2. **Agentic planning** — not just inference, but multi-step reasoning
3. **Patient-facing simplification** — translate medical → plain language
4. **Self-evaluation** — models assessing their own output quality
5. **Visual grounding** — point to WHERE in an image, not just WHAT
6. **Conversational** — chat-based, not form-based

---

## "Steal-Worthy" Ideas

| Idea | Source | Implementation Effort | Impact |
|------|--------|----------------------|--------|
| Diagnostic debate / challenge-the-AI | Sturgeon | Medium | High — unique UX differentiator |
| Audit trail with SHA256 hashes | ClinicaFlow | Low | Medium — signals production readiness |
| Vignette regression benchmark | ClinicaFlow | Medium | High — quantitative quality proof |
| Click-to-explain radiology reports | Google rad_explain | Medium | High — exactly what Google wants |
| Self-evaluation of outputs | Google appoint-ready | Low | High — shows model self-awareness |
| FHIR integration (even synthetic) | Google EHR navigator | Medium | High — signals real-world readiness |
| Token compression layer | CompText | Low | Medium — cost efficiency story |
| Voice input/output | VoiceRad, Medevac-Gemma | Medium | Medium — accessibility story |
| Fairness across skin tones | skin-lesion-triage | Medium | High — equity narrative judges love |
| Google ADK for orchestration | PathRad-AI | Medium | High — uses Google's own tooling |

---

## Gaps NO ONE Is Filling

1. **Multi-specialty second opinion across ALL HAI-DEF models** — Nobody combines CXR + Path + Derm + MedSigLIP + MedGemma in one coherent workflow. Most pick 1-2 models.

2. **Patient-facing report with visual grounding** — Google's rad_explain does it for radiology; nobody does it for pathology or dermatology.

3. **Longitudinal tracking** — Nobody tracks a patient's images over time to detect changes. Huge clinical value.

4. **Uncertainty quantification with actionable thresholds** — Most show confidence scores but don't say "this confidence level means you should do X."

5. **Multi-language patient education** — Offline-MedAi-Console mentions Spanish briefly; nobody does systematic multilingual output.

6. **Integration of ALL 5+ HAI-DEF foundation models** — CXR Foundation, Path Foundation, Derm Foundation, MedSigLIP, HeAR, MedGemma, TxGemma. Nobody uses more than 3.

7. **Comparative analysis** — Nobody lets you upload images from two time points and get a comparison report.

8. **Drug interaction checking with clinical reasoning** — ClinAssist-Edge claims it but implementation is basic. Nobody does RAG-powered drug safety.

---

## Top 5 Actionable Recommendations

### 1. 🎯 Use ALL HAI-DEF Models (Maximum Model Coverage)
Nobody uses more than 3 HAI-DEF models. Use **CXR Foundation + Path Foundation + Derm Foundation + MedSigLIP + MedGemma** minimum. This signals deep engagement with Google's ecosystem and is exactly what judges will look for. PathRad-AI with 3 models is the current leader — beat them with 5+.

### 2. 🏗️ Implement Google-Style Agentic Architecture
Use Google ADK or a similar framework. The pipeline should show **planning → tool selection → multi-step reasoning → self-evaluation**, mirroring Google's own EHR Navigator pattern. Each HAI-DEF model should be a "callable tool" that the orchestrator invokes as needed (like Sturgeon's Gemini+MedGemma pattern).

### 3. 🔍 Add Visual Grounding + Click-to-Explain
Directly inspired by Google's rad_explain demo. When showing results, let users click on specific findings to get plain-language explanations with highlighted regions on the image. This is the UX Google has explicitly built and showcased — they want to see others build on it.

### 4. 📊 Include Quantitative Evaluation + Self-Assessment
- Benchmark on standard datasets (CheXpert, HAM10000, MIMIC-CXR)
- Include a self-evaluation step where MedGemma assesses its own output quality (like appoint-ready does)
- Show fairness metrics across demographics (skin tones for derm, age/sex for CXR)
- ClinicaFlow's vignette regression set is a good template

### 5. 🎨 Polish the UI/UX to Demo Quality
Most competitors have ugly Streamlit/Gradio interfaces. A polished React frontend with:
- Real-time pipeline progress (WebSocket updates as each model runs)
- Interactive image annotations
- Side-by-side before/after comparisons
- Mobile-responsive design
- Clear safety disclaimers

This is where we already have an advantage with our existing pipeline UI. **Demo quality wins hackathons.**

---

## Competition Landscape Summary

```
Sophistication Spectrum:

BASIC (60% of repos)          INTERMEDIATE (30%)              ADVANCED (10%)
├─ Streamlit wrapper           ├─ Multi-agent pipeline          ├─ Sturgeon
├─ Single model                ├─ 2-3 HAI-DEF models            ├─ ClinicaFlow  
├─ One use case                ├─ Some safety gating             ├─ PathRad-AI
├─ No eval                     ├─ Docker deployment              ├─ (Us, if we execute)
└─ README > code               └─ Basic benchmarks               └─ 

Our target: TOP of Advanced tier with widest model coverage + best UX + Google-aligned architecture
```

**Bottom line:** The competition is beatable. Nobody has combined breadth (all HAI-DEF models), depth (agentic reasoning with self-eval), and polish (production UI) yet. That's our lane.
