# Poolside AI — Technology Analysis & Differentiation

## Core Technology Stack

### Foundation Models

#### Malibu (Complex Tasks)
- Multi-file code generation
- Code refactoring
- Test writing
- Documentation generation
- Complex software engineering workflows
- Multi-step reasoning and autonomous task execution
- Designed for agentic use cases

#### Point (Real-Time Completion)
- Low-latency, real-time code completion
- Context-aware suggestions
- Optimized for IDE integration
- Designed for speed — inline suggestions as developers type

### Training Methodology: RLCEF

**Reinforcement Learning from Code Execution Feedback** is Poolside's signature training innovation.

#### How It Works
1. **Task ingestion**: Model receives a coding task against a repository
2. **Code generation**: Model writes code to solve the task
3. **Execution**: Code is executed in a sandboxed environment
4. **Feedback loop**: Model receives execution results (success, failure, compilation errors, test results)
5. **Learning**: Model iterates, learning from both successes and failures
6. **Synthetic data**: This process generates synthetic training data continuously, overcoming data bottlenecks

#### Infrastructure for RLCEF
- **"Saucer"**: Revision serving system — pulls repositories, converts to images, handles multiple revisions using layers
- **Sandboxed execution**: Fast, secure, isolated environments with explicit APIs
- **10,000+ real-world codebases** in their sandbox environment
- **Continuous learning**: Models improve through ongoing interaction, not just initial training
- **"Model Factory"**: Orchestration system requiring extensive compute to ingest tasks, execute code, and adapt from feedback

#### Why This Matters
- Most coding AI trains on static code datasets (GitHub repos, Stack Overflow)
- Poolside's models learn by DOING — writing code, running it, seeing what works
- This mimics how human engineers learn: write → run → debug → iterate
- Creates a synthetic data flywheel: more execution = more training data = better models
- Solves the "data wall" problem — they generate their own training data

---

## Platform Architecture

### Deployment Options

| Model | Description | Target |
|-------|-------------|--------|
| **On-Premises** | Full platform inside customer boundary | Defense, classified environments |
| **VPC (Virtual Private Cloud)** | Deployed in customer's cloud | Enterprise, regulated industries |
| **Workstation** | Local deployment | Defense-only special cases |
| **Amazon Bedrock** | Managed through AWS | Broader enterprise market |
| **Amazon EC2** | Self-managed on AWS compute | Enterprise with existing AWS |

### Key Architecture Decisions
- **Full model weights delivered**: Not API access — actual weights. Customer owns the model.
- **No external calls**: In on-prem mode, zero data egress. No phone-home, no telemetry.
- **Air-gapped support**: Works in disconnected environments (SCIF, classified networks)
- **Multi-cloud/legacy**: Designed for heterogeneous environments — not cloud-native only

### Developer Surfaces
- **IDE Extensions**: VS Code, Visual Studio (agentic chat + code completion)
- **CLI Tool**: Terminal-based interaction
- **API**: For custom integrations and pipelines
- **Agent Binary**: Single binary for building pipelines and processes across org
- **Console**: Administration and orchestration layer for agent management

### Data & Knowledge Connectors
- Repositories (Git)
- Databases
- Data warehouses
- CI/CD pipelines
- Runtime environments
- Private corpora
- Knowledge bases
- Documentation

### Agent Orchestration
- Single and multi-agent systems
- Sandboxed execution environments
- Policy controls for agent behavior
- End-to-end audit traces
- Works with Poolside models OR third-party models

---

## Technical Differentiation vs. Competitors

### vs. GitHub Copilot
| Dimension | Poolside | GitHub Copilot |
|-----------|----------|----------------|
| Model ownership | Customer owns weights | Microsoft/OpenAI controls |
| Deployment | On-prem, VPC, air-gapped | Cloud-only (with enterprise VPC option) |
| Fine-tuning | On customer's specific codebase | Limited customization |
| Training approach | RLCEF (learns from execution) | Standard LLM training |
| Agent orchestration | Multi-agent with audit trails | Copilot Workspace (limited) |
| Target market | Enterprise 5K+ devs, defense | All developers |

### vs. Cursor
| Dimension | Poolside | Cursor |
|-----------|----------|--------|
| What they build | Foundation models + platform | IDE (uses OpenAI/Anthropic models) |
| Model dependency | Zero — owns models | Full — depends on OpenAI/Anthropic |
| Deployment | On-prem capable | Cloud-only |
| Security | Air-gapped environments | Standard cloud security |
| Target | Enterprise/defense | Individual developers and small teams |
| Pricing | Custom enterprise | $20/mo pro |

### vs. Amazon CodeWhisperer
| Dimension | Poolside | CodeWhisperer |
|-----------|----------|---------------|
| Training focus | Code-execution feedback | Standard code training |
| Deployment | Multi-cloud + on-prem | AWS-only |
| Customization | Deep fine-tuning on codebases | Limited |
| Pricing | Custom enterprise | $19/mo / enterprise custom |

---

## Open Source Presence

### GitHub: @poolsideai

| Repo | Language | Description |
|------|----------|-------------|
| **sandworm** | Go | HTTP/HTTPS proxy for containerized environments with domain/CIDR filtering |
| **bridge-sdk** | Python | SDK for defining workflow steps |
| **aws-ofi-nccl** | C | AWS integration for NCCL (network communication library) |
| **neptune-exporter** | Python | Monitoring/metrics exporter |

### Assessment
- Very limited open source — they keep the crown jewels proprietary
- Open source repos are infrastructure/tooling, not core models
- Sandworm reveals their sandbox architecture for RLCEF
- bridge-sdk suggests a workflow/pipeline orchestration layer

---

## Technology Risks

1. **RLCEF is unproven at scale**: Novel training approach without independent validation
2. **Model quality claims unverified**: No public benchmarks vs. GPT-4, Claude, etc. for coding
3. **On-prem complexity**: Deploying and maintaining AI models on-prem is operationally challenging
4. **Compute costs**: RLCEF requires executing code (expensive) not just processing text
5. **Talent concentration**: If key researchers leave, RLCEF expertise could walk out the door
6. **Model refresh latency**: On-prem customers may lag behind cloud-deployed updates
