# MedGemma: Low-Cost Deployment Guide for Second-Opinion

*Research compiled February 2026*

---

## 1. What is MedGemma?

MedGemma is Google's family of open medical AI models built on the Gemma architecture, released mid-2025. Designed for medical text and multimodal (image + text) tasks.

### Variants

| Model | Parameters | Type | VRAM (FP16) | Key Capability |
|-------|-----------|------|-------------|----------------|
| **MedGemma 4B** | 4B | Multimodal (text + image) | ~8-10 GB | Medical image understanding (radiology, pathology, dermatology) + text |
| **MedGemma 27B** | 27B | Text | ~54 GB | Complex medical reasoning, differential diagnosis |

### Capabilities
- Medical Q&A and clinical reasoning
- Radiology/pathology/dermatology image interpretation (4B multimodal)
- Summarization of clinical notes
- Health-related dialogue

### Licensing
- **Open weights** under Google's Gemma license (permissive for commercial use)
- Available on Hugging Face: `google/medgemma-4b-it`, `google/medgemma-27b-it`
- Must agree to Gemma terms of use on HF
- **No per-token API fees** when self-hosted — you only pay for compute

---

## 2. Self-Hosting Options (Cheapest First)

### 2.1 Google Colab (Free/Pro) — Best for Prototyping

**Free Tier:**
- T4 GPU (16GB VRAM) — can run MedGemma 4B at FP16 or quantized
- Limited to ~12h sessions, may disconnect
- Cost: **$0**

**Colab Pro ($10/mo):**
- A100 40GB access, longer sessions, priority
- Can run 4B easily, 27B quantized (4-bit)

**Setup (4B on free Colab):**
```python
!pip install transformers accelerate bitsandbytes torch

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model_id = "google/medgemma-4b-it"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=quantization_config,
    device_map="auto"
)

# 4-bit quantized 4B model fits in ~3-4 GB VRAM
messages = [{"role": "user", "content": "What are the differential diagnoses for chest pain in a 45-year-old male?"}]
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
output = model.generate(inputs, max_new_tokens=512)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

**Verdict:** Great for dev/testing. Not suitable for production (no persistent endpoint).

---

### 2.2 Vast.ai — Cheapest GPU Rental

Community cloud GPU marketplace. Spot pricing.

| GPU | VRAM | Approx $/hr | Can Run |
|-----|------|-------------|---------|
| RTX 3090 | 24GB | $0.10–0.20 | 4B FP16, 27B 4-bit (tight) |
| RTX 4090 | 24GB | $0.20–0.35 | 4B FP16, 27B 4-bit |
| A100 40GB | 40GB | $0.50–0.80 | 27B 4-bit comfortably |
| A6000 | 48GB | $0.35–0.55 | 27B 4-bit or 8-bit |

**Monthly estimate (always-on 4B on RTX 3090):** ~$72–144/mo

**Setup:**
1. Create account at vast.ai
2. Rent an instance with a Docker template (e.g., `vllm/vllm-openai`)
3. SSH in, download model, run vLLM server
```bash
# On Vast.ai instance
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model google/medgemma-4b-it \
  --quantization awq \
  --max-model-len 4096 \
  --port 8000
```
4. Expose port or use SSH tunnel to connect from your app

**Verdict:** Cheapest always-on option. Reliability varies (community GPUs). Good for MVP.

---

### 2.3 RunPod — Slightly More Reliable Than Vast.ai

| GPU | Spot $/hr | On-Demand $/hr |
|-----|----------|----------------|
| RTX 3090 | $0.16 | $0.22 |
| RTX 4090 | $0.28 | $0.39 |
| A100 80GB | $0.89 | $1.19 |

**RunPod Serverless** (pay per second, auto-scales to 0):
- Configure a serverless endpoint with your model baked into a Docker image
- Pay only when processing requests
- Cold start: 30-60s (can keep 1 warm worker)
- **Estimated cost for low traffic MVP: $5–30/mo** (depending on usage)

**Setup (RunPod Serverless):**
1. Create a RunPod serverless template with vLLM
2. Set `google/medgemma-4b-it` as the model
3. Deploy — get an API endpoint
4. Call from Second-Opinion backend

**Verdict:** Best balance of cost and reliability for MVP. Serverless = pay per use.

---

### 2.4 Modal.com — Serverless GPU (Developer Friendly)

- Pay per second of GPU time
- Auto-scales to zero
- A10G: ~$0.36/hr, A100: ~$1.10/hr, T4: ~$0.16/hr

**Setup:**
```python
# modal_app.py
import modal

app = modal.App("medgemma")
image = modal.Image.debian_slim().pip_install("vllm", "torch")

@app.cls(gpu="T4", image=image, container_idle_timeout=300)
class MedGemma:
    @modal.enter()
    def load(self):
        from vllm import LLM
        self.llm = LLM("google/medgemma-4b-it", quantization="awq")

    @modal.method()
    def generate(self, prompt: str):
        from vllm import SamplingParams
        return self.llm.generate([prompt], SamplingParams(max_tokens=512))

    @modal.web_endpoint()
    def api(self, item: dict):
        return self.generate(item["prompt"])
```

**Estimated MVP cost:** $10–50/mo for light usage (scales to $0 when idle)

**Verdict:** Excellent DX. Slightly more expensive per-second than Vast.ai but zero cost when idle.

---

### 2.5 Home Server / Local GPU

| Hardware | VRAM | Can Run | Upfront Cost |
|----------|------|---------|-------------|
| RTX 3090 | 24GB | 4B FP16, 27B Q4 (tight) | ~$700 used |
| RTX 4090 | 24GB | Same, faster | ~$1,600 |
| Mac M2 Ultra 192GB | 192GB unified | 27B FP16 easily | ~$4,000+ |
| Mac M4 Pro 48GB | 48GB unified | 27B Q4, 4B FP16 | ~$2,500 |

**Setup (local with Ollama or llama.cpp):**
```bash
# Using Ollama (if MedGemma GGUF is available)
ollama run medgemma:4b

# Or using vLLM locally
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model google/medgemma-4b-it \
  --port 8000
```

**Ongoing cost:** Electricity only (~$10-30/mo)

**Verdict:** Cheapest long-term if you already have hardware. Need to handle uptime/networking yourself.

---

### 2.6 Hugging Face Inference Endpoints

- Dedicated GPU endpoint, auto-scaling available
- T4: ~$0.60/hr ($432/mo always-on)
- A10G: ~$1.30/hr
- Can scale to 0 (cold starts ~60-120s)

**Verdict:** Easy setup but pricier than Vast.ai/RunPod. Good if already in HF ecosystem.

---

### 2.7 Railway

Nathan's current infra. **Not feasible for MedGemma** — Railway doesn't offer GPU instances. You'd need to run the model elsewhere and call it as an API from your Railway app.

**Architecture:** Railway (app backend) → calls MedGemma API on RunPod/Modal/Vast.ai

---

### 2.8 Replicate / Together.ai / Fireworks.ai

These platforms may host MedGemma as a pay-per-token API:

| Provider | Pricing (est.) | Notes |
|----------|----------------|-------|
| **Replicate** | ~$0.10–0.30 per run (varies) | If community model available |
| **Together.ai** | ~$0.10/M input, $0.30/M output (4B class) | Check model catalog |
| **Fireworks.ai** | ~$0.10/M input, $0.30/M output | Fast inference |

**Verdict:** Easiest integration (just an API call). Check if MedGemma specifically is listed — may need to use a custom deployment.

---

## 3. API / Managed Options

### 3.1 Google Cloud Vertex AI

Google hosts MedGemma on Vertex AI Model Garden.

- **Pricing:** Pay for the underlying GPU (not per-token for open models)
- Deploy to a Vertex AI endpoint on an A100 or L4
- L4 instance: ~$0.70/hr (~$504/mo always-on)
- Can use prediction auto-scaling

**Vertex AI is the "official" way** but not the cheapest.

### 3.2 Google AI Studio / Gemini API

As of mid-2025, MedGemma is available through Google AI Studio for testing. Check if production API access is available — pricing would align with Gemini API rates.

---

## 4. Optimization Techniques

### 4.1 Quantization

| Quant Level | Bits | VRAM for 4B | VRAM for 27B | Quality Loss |
|-------------|------|-------------|--------------|-------------|
| FP16 | 16 | ~8 GB | ~54 GB | None |
| INT8 | 8 | ~4 GB | ~27 GB | Minimal |
| INT4 (GPTQ/AWQ) | 4 | ~2.5 GB | ~14 GB | Small |
| GGUF Q4_K_M | 4 | ~3 GB | ~16 GB | Small |
| GGUF Q2_K | 2 | ~2 GB | ~10 GB | Noticeable |

**Recommendation:** AWQ or GPTQ 4-bit for GPU serving (vLLM supports both natively). GGUF Q4_K_M for llama.cpp/Ollama.

For a **medical** model, prefer INT8 or 4-bit (Q4_K_M+). Avoid Q2 — accuracy matters for health.

### 4.2 Serving Optimizations
- **vLLM**: Continuous batching, PagedAttention — handles multiple concurrent requests efficiently
- **Batch requests** where possible to maximize GPU utilization
- **KV cache quantization** in vLLM to reduce memory further

### 4.3 Spot/Preemptible Instances
- RunPod spot: 30-50% cheaper, may be interrupted
- GCP preemptible: ~60-70% discount
- Good for dev; for production, use on-demand or RunPod serverless

---

## 5. Cost Comparison Table

### MedGemma 4B (recommended for MVP)

| Option | Cost Model | Est. Monthly (Light MVP) | Est. Monthly (Always-On) | Setup Difficulty |
|--------|-----------|-------------------------|-------------------------|-----------------|
| **Google Colab Free** | Free | $0 | N/A (not persistent) | Easy |
| **Vast.ai (3090 spot)** | $0.10-0.20/hr | $15-40 (partial uptime) | $72-144 | Medium |
| **RunPod Serverless** | Per-second billing | **$5-30** | N/A (auto-scales) | Medium |
| **Modal.com** | Per-second billing | **$10-50** | N/A (auto-scales) | Easy |
| **RunPod On-Demand (3090)** | $0.22/hr | N/A | $158 | Medium |
| **Together.ai API** | ~$0.10/$0.30 per M tokens | **$1-20** (usage-based) | N/A | Very Easy |
| **Fireworks.ai API** | ~$0.10/$0.30 per M tokens | **$1-20** | N/A | Very Easy |
| **HF Inference Endpoints** | $0.60/hr (T4) | $50-100 (scale-to-0) | $432 | Easy |
| **Vertex AI (L4)** | $0.70/hr | N/A | $504 | Medium |
| **Home RTX 3090** | $700 upfront + electricity | ~$15 electricity | ~$15 electricity | Hard |
| **Replicate** | Per-prediction | $5-30 | N/A | Very Easy |

---

## 6. Recommendations for Second-Opinion MVP

### 🥇 Best Option: RunPod Serverless OR Together.ai/Fireworks.ai API

**If MedGemma is available on Together.ai or Fireworks.ai:**
- **Use their API.** ~$0.10-0.30/M tokens. For an MVP with <1000 queries/day, you're looking at **$1-20/mo**.
- Zero infrastructure. Just an API key.
- Add to your Railway backend as an environment variable.

**If you need to self-host (MedGemma not on third-party APIs):**

### 🥈 RunPod Serverless — Best Self-Hosted for MVP

**Why:** Pay per second, scales to zero, reliable enough for MVP.

**Step-by-step:**
1. Sign up at runpod.io
2. Go to Serverless → Create Endpoint
3. Use a vLLM Docker template or custom image:
   ```dockerfile
   FROM runpod/worker-vllm:latest
   ENV MODEL_NAME="google/medgemma-4b-it"
   ENV QUANTIZATION="awq"
   ENV MAX_MODEL_LEN=4096
   ```
4. Set GPU to 24GB (RTX 3090/4090)
5. Set min workers = 0, max workers = 1-3
6. Deploy → get endpoint URL
7. Call from your Railway app:
   ```python
   import requests
   response = requests.post(
       "https://api.runpod.ai/v2/YOUR_ENDPOINT/runsync",
       headers={"Authorization": "Bearer YOUR_API_KEY"},
       json={"input": {"prompt": "Patient presents with..."}}
   )
   ```

**Expected cost:** $5-30/mo for light MVP traffic.

### 🥉 Modal.com — Best DX, Slightly More Expensive

**Why:** Python-native, great developer experience, automatic scaling.

**Step-by-step:**
1. `pip install modal && modal setup`
2. Create `serve_medgemma.py`:
   ```python
   import modal
   
   app = modal.App("second-opinion")
   
   vllm_image = (
       modal.Image.debian_slim(python_version="3.11")
       .pip_install("vllm", "transformers", "torch")
   )
   
   @app.cls(
       gpu="T4",  # Cheapest GPU, enough for 4B quantized
       image=vllm_image,
       container_idle_timeout=300,  # Scale to 0 after 5 min idle
       secrets=[modal.Secret.from_name("huggingface")]
   )
   class MedGemmaService:
       @modal.enter()
       def startup(self):
           from vllm import LLM
           self.llm = LLM(
               "google/medgemma-4b-it",
               quantization="awq",
               max_model_len=4096
           )
       
       @modal.web_endpoint(method="POST")
       def query(self, request: dict):
           from vllm import SamplingParams
           params = SamplingParams(max_tokens=request.get("max_tokens", 512))
           result = self.llm.generate([request["prompt"]], params)
           return {"response": result[0].outputs[0].text}
   ```
3. `modal deploy serve_medgemma.py`
4. Get URL, call from Railway backend

**Expected cost:** $10-50/mo for light MVP traffic.

---

## 7. Architecture for Second-Opinion

```
User → Railway App (Next.js/API) → MedGemma Endpoint (RunPod/Modal/Together.ai)
                                  ↓
                            Postgres (Railway) — store queries, user data
```

The Railway app handles auth, UI, and orchestration. MedGemma runs on a separate GPU service. This keeps your Railway costs low and lets you swap the model provider easily.

---

## 8. Key Takeaways

1. **MedGemma 4B is the sweet spot** — multimodal, runs on cheap GPUs, good enough for MVP
2. **Check Together.ai / Fireworks.ai first** — if they host MedGemma, that's the easiest and cheapest path ($1-20/mo)
3. **RunPod Serverless is the best self-hosted option** — $5-30/mo, scales to zero
4. **Don't run always-on GPU servers** for an MVP — serverless saves 80%+
5. **Use 4-bit quantization (AWQ)** — minimal quality loss, halves VRAM needs
6. **Railway can't run MedGemma directly** — use it for the app, external service for the model
7. **Budget: $5-50/mo** is realistic for an MVP with moderate traffic

---

*Report prepared for the Second-Opinion project (TrendpilotAI/Second-Opinion)*
