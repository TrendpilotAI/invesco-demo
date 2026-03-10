# Poolside AI — Executive Summary

**Last Updated:** 2026-03-10

## Company Profile

| Field | Detail |
|-------|--------|
| **Name** | Poolside AI (stylized: poolside) |
| **Website** | [poolside.ai](https://poolside.ai) |
| **Founded** | April/May 2023 |
| **HQ** | San Francisco, CA (significant presence in Paris, France) |
| **Co-Founders** | Jason Warner (President/CEO, ex-CTO GitHub) & Eiso Kant (CTO, ex-founder source{d}) |
| **Mission** | "AGI for the enterprise—starting with software agents" |
| **Tagline** | "We build the models. You build the future." |
| **Employees** | ~200+ (growing rapidly) |
| **Stage** | Late growth — pursuing $2B raise at $12B valuation |

## Funding History

| Round | Date | Amount | Valuation | Lead Investors |
|-------|------|--------|-----------|----------------|
| Seed | May 2023 | $26M | — | Redpoint Ventures |
| Series A | Aug 2023 | $100M | $526M | Felicis, Redpoint, Xavier Niel |
| Series B | Oct 2024 | $500M | $3B | Bain Capital Ventures, Nvidia, eBay Ventures, DST Global |
| Series C (in progress) | 2025 | $2B target ($1B+ committed) | $12B | Nvidia (~$1B), existing investors |
| **Total Raised** | | **$626M closed + $1B+ committed** | | |

## What They Build

- **Foundation Models**: Malibu (complex tasks — multi-file code gen, refactoring, test writing) and Point (real-time, low-latency code completion)
- **AI Assistant**: IDE plugins (VS Code, Visual Studio), CLI tool, API
- **Agent Orchestration**: Single and multi-agent systems with sandboxed execution, policy controls, audit trails
- **Data Connectors**: Repos, databases, data warehouses, private corpora
- **Deployment**: On-premises, VPC, workstations (defense), Amazon Bedrock, EC2

## Key Differentiators

1. **RLCEF** (Reinforcement Learning from Code Execution Feedback) — models learn by writing and executing code, not just from static data
2. **On-premises/air-gapped deployment** — full model weights delivered to customer, no cloud dependency
3. **Fine-tuning on customer codebases** — models trained on org-specific code without data leaving the boundary
4. **Forward Deployed Research Engineers (FDREs)** — embed with customer teams, joint outcome responsibility
5. **Vertical integration** — building own 2GW data center (Project Horizon) with CoreWeave

## Key Partnerships

- **AWS**: Amazon Bedrock and EC2 integration (Dec 2024)
- **Nvidia**: ~$1.5B total investment, access to GB300 chips
- **CoreWeave**: Anchor tenant for Project Horizon, 40,000+ GB300 NVL72 GPUs

## Target Customers

- Global 2000 enterprises (5,000+ developers)
- US Department of Defense & defense contractors (Raytheon)
- Israeli defense sector
- FSIS banks & financial institutions
- Legacy enterprise tech companies
- Government agencies

## Revenue

- Estimated ~$66.4M ARR (May 2025 estimate)
- Custom pay-per-use pricing model
- Enterprise contracts (models + professional services)
- Not open to public — enterprise-only

## Key Leadership

| Person | Role | Background |
|--------|------|------------|
| Jason Warner | President & Co-Founder | Ex-CTO GitHub, ex-SVP Tech Canonical |
| Eiso Kant | CTO & Co-Founder | Ex-founder source{d}, software entrepreneur |
| Margarida Garcia | COO | Ex-COO Lifebit, ex-VC at Beacon Capital |
| Paul St John | CRO | Ex-VP Global Sales at GitHub (joined Apr 2024) |

## The Big Picture

Poolside is betting that **the fastest path to AGI runs through software engineering**. They believe code requires understanding the world, multi-step reasoning, and long-horizon planning — making it the ideal training ground for general intelligence. Unlike competitors who build IDE tools on top of third-party models, Poolside builds the models themselves, optimized specifically for code, and deploys them inside customer environments where data never leaves.

Their enterprise-first, security-first approach positions them uniquely for government/defense contracts where cloud-based competitors literally cannot go. The massive Nvidia backing and Project Horizon data center signal they're building for the long game — not just a product company but a compute infrastructure company.
