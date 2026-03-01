# Marketing Agent Specialist - n8n Workflow

A persistent AI marketing agent that runs on n8n with 9 specialized design and marketing functions.

## 🚀 Quick Start

### Webhook Endpoint
```
POST https://openclaw-railway.taild36ce1.ts.net/webhook/marketing-agent
```

### Authentication
Add header: `X-API-Key: your-api-key` (optional)

## 📋 Available Agents

| Agent Type | Description | Context Required |
|------------|-------------|------------------|
| `design_system` | Apple Principal Designer builds complete design system | `brand` |
| `brand_identity` | Creative Director at Pentagram creates brand identity | `company`, `industry`, `audience` |
| `ui_ux_pattern` | Senior Apple UI Designer creates full UI patterns | `app_type`, `persona` |
| `marketing_assets` | Creative Director builds campaign asset library | `product` |
| `figma_specs` | Figma Design Ops converts design to Figma specs | `design_description` |
| `design_critique` | Apple Design Director critiques design | `design` |
| `design_trends` | frog Design Researcher analyzes trends | `industry` |
| `accessibility_audit` | Apple Accessibility Specialist audits WCAG | `design` |
| `design_to_code` | Vercel Design Engineer translates to code | `design`, `tech_stack` |

## 📝 Request Format

```json
{
  "prompt": "design_system",
  "context": {
    "brand": "Acme Corp",
    "user_input": "Build a modern SaaS design system"
  }
}
```

**Alternative format (auto-detection):**
```json
{
  "agent_type": "design_system",
  "brand": "Acme Corp",
  "user_input": "Build a modern SaaS design system"
}
```

## 📤 Response Format

```json
{
  "success": true,
  "timestamp": "2026-02-28T23:30:00.000Z",
  "prompt_type": "design_system",
  "response": "Full AI response here...",
  "metadata": {
    "model": "gpt-4",
    "usage": {
      "prompt_tokens": 100,
      "completion_tokens": 2000,
      "total_tokens": 2100
    }
  }
}
```

## 🔧 Setup

### 1. Import Workflow
1. Open n8n UI
2. Go to Workflows → Import
3. Select `marketing-agent.json`

### 2. Configure OpenAI
Add these credentials:
- **Credential Name**: OpenAI
- **API Key**: `sk-...`
- **Header Auth**: Set header name to `Authorization`

### 3. Environment Variables
```env
OPENAI_API_KEY=sk-...
N8N_API_KEY=your-api-key
```

## 📞 Example Calls

### Design System Request
```bash
curl -X POST https://openclaw-railway.taild36ce1.ts.net/webhook/marketing-agent \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "design_system",
    "context": {
      "brand": "ForwardLane",
      "user_input": "Build a fintech design system with professional but innovative feel"
    }
  }'
```

### Brand Identity Request
```bash
curl -X POST https://openclaw-railway.taild36ce1.ts.net/webhook/marketing-agent \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "brand_identity",
    "context": {
      "company": "Ultrafone",
      "industry": "AI telecommunications",
      "audience": "business professionals and small businesses",
      "user_input": "Create a bold, premium brand identity"
    }
  }'
```

### Marketing Assets Request
```bash
curl -X POST https://openclaw-railway.taild36ce1.ts.net/webhook/marketing-agent \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "marketing_assets",
    "context": {
      "product": "AI Call Screener",
      "user_input": "Generate full campaign for B2B SaaS launch"
    }
  }'
```

## 🔄 Reusability

### Adding New Agents
Edit `Parse Input` node to add new prompt templates:

```javascript
const prompts = {
  // Existing agents...
  new_agent: {
    role: "Your Role",
    task: "Your task description with {{variable}}"
  }
};
```

### Custom Prompts
Override the default task with `user_input`:

```json
{
  "prompt": "design_system",
  "context": {
    "brand": "MyBrand",
    "user_input": "Custom instructions..."
  }
}
```

## ⚙️ Configuration

- **Model**: GPT-4 (configurable in OpenAI node)
- **Temperature**: 0.7
- **Max Tokens**: 4000

## 📊 Logging

All requests are logged with:
- Timestamp
- Prompt type
- Token usage
- Response metadata

## 🚨 Error Handling

Returns error response on failure:
```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2026-02-28T23:30:00.000Z"
}
```

## 🔐 Security

- Optional API key via header
- No PII stored
- Requests logged for debugging
