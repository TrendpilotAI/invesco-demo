# Lead Enrichment Providers Research

*Compiled for Signal Studio (ForwardLane) Data Waterfall Pipeline*

## Quick Comparison

| Provider     | Best For                | Email Finding | Verification | Phone | Company Data | LinkedIn | Pricing (est.)       | Rate Limit     |
|-------------|-------------------------|:---:|:---:|:---:|:---:|:---:|---------------------|----------------|
| Hunter      | Email by domain         | ✅  | ✅  | ❌  | ⚠️  | ⚠️  | Free: 25/mo, $49-399/mo | 10 req/s      |
| FindyMail   | Verified emails         | ✅  | ✅  | ❌  | ⚠️  | ✅  | $49-249/mo           | 5 req/s        |
| Icypeas     | Bulk email finding      | ✅  | ✅  | ❌  | ❌  | ⚠️  | €49-199/mo           | 5 req/s        |
| QuickEnrich | Full-stack enrichment   | ✅  | ✅  | ✅  | ✅  | ✅  | Pay-per-use ~$0.03-0.10 | 3 req/s     |
| Forager     | B2B contact intelligence| ✅  | ⚠️  | ✅  | ✅  | ✅  | Custom pricing       | 5 req/s        |
| Wiza        | LinkedIn extraction     | ✅  | ✅  | ✅  | ⚠️  | ✅  | $83-333/mo           | 2 req/s        |
| LeadIQ      | Enterprise B2B          | ✅  | ✅  | ✅  | ✅  | ✅  | $75-150/user/mo      | 2 req/s        |

✅ = Strong capability | ⚠️ = Partial/limited | ❌ = Not available

---

## Detailed Provider Analysis

### 1. Hunter (hunter.io)

**Overview:** The most established email finding tool. Excels at finding email patterns for domains and verifying email addresses.

**API Capabilities:**
- **Email Finder** — Find email by first name + last name + domain
- **Email Verifier** — Verify deliverability of any email
- **Domain Search** — List all emails found for a domain
- **Account Info** — Check usage/quota

**API Docs:** https://hunter.io/api-documentation (v2 REST API)

**Authentication:** API key as query parameter (`?api_key=xxx`)

**Pricing:**
- Free: 25 searches + 50 verifications/month
- Starter ($49/mo): 500 searches + 1,000 verifications
- Growth ($149/mo): 5,000 searches + 10,000 verifications
- Business ($399/mo): 30,000 searches + 60,000 verifications
- Per-lookup cost: ~$0.01-0.10 depending on plan

**Rate Limits:** 10 requests/second (all plans), daily limits per plan

**Data Quality:**
- ⭐ Excellent for email pattern detection
- ⭐ Very reliable email verification
- ⚠️ Limited company/person data beyond email
- ⚠️ Phone numbers not available

**Strengths:** Mature API, excellent documentation, reliable email verification, generous free tier
**Weaknesses:** Limited to email data, no phone numbers, no deep company intelligence

**Best position in waterfall:** #1 (cheap, fast, reliable for email finding)

---

### 2. FindyMail (findymail.com)

**Overview:** Modern email finder focused on accuracy. Claims to only return verified emails. Strong LinkedIn integration.

**API Capabilities:**
- **Email Finder** — Find email by name + company/domain or LinkedIn URL
- **Email Verifier** — Verify email addresses
- **LinkedIn lookup** — Find email from LinkedIn profile URL
- **Bulk operations** — Batch email finding

**API Docs:** https://app.findymail.com/docs

**Authentication:** Bearer token (`Authorization: Bearer xxx`)

**Pricing:**
- Basic ($49/mo): 1,000 credits
- Professional ($99/mo): 5,000 credits
- Business ($249/mo): 15,000 credits
- 1 credit = 1 email found (failed searches don't cost credits)

**Rate Limits:** ~5 requests/second, credits-based

**Data Quality:**
- ⭐ High accuracy — only returns verified emails
- ⭐ Good LinkedIn-to-email conversion
- ⚠️ Limited additional data (focused on email)
- ⚠️ Newer player, smaller database than Hunter

**Strengths:** High accuracy (no unverified results), LinkedIn integration, credits only charged on success
**Weaknesses:** Smaller database, limited non-email data, pricier per verified email

**Best position in waterfall:** #2 (good accuracy, fills gaps Hunter misses)

---

### 3. Icypeas (icypeas.com)

**Overview:** European email finding and verification tool. Good for bulk operations at competitive pricing.

**API Capabilities:**
- **Email Search** — Find email by name + domain
- **Email Verification** — Verify email deliverability
- **Domain Search** — Find emails at a domain
- **Bulk operations** — CSV-based batch processing

**API Docs:** https://icypeas.com/api (REST API)

**Authentication:** Bearer token or API key

**Pricing:**
- Explorer (€49/mo): 1,000 credits
- Professional (€99/mo): 5,000 credits
- Business (€199/mo): 15,000 credits
- GDPR compliant (EU-hosted)

**Rate Limits:** ~5 requests/second

**Data Quality:**
- ⭐ Good for European contacts (EU database strength)
- ⚠️ Smaller US database compared to Hunter
- ⚠️ Limited enrichment beyond email
- ⚠️ Verification is decent but not best-in-class

**Strengths:** GDPR compliant, competitive pricing, good for EU markets
**Weaknesses:** Smaller US database, limited API documentation, fewer features

**Best position in waterfall:** #3 (cheap supplement, good for EU contacts)

---

### 4. QuickEnrich (quickenrich.com)

**Overview:** Full-stack contact enrichment platform. Internally runs its own waterfall across multiple data sources to return comprehensive person + company data.

**API Capabilities:**
- **Person Enrichment** — By email, name+company, or LinkedIn URL
- **Company Enrichment** — By domain
- **Returns:** Email, phone, social profiles, job title, company data
- **Bulk enrichment** — Batch API

**API Docs:** https://quickenrich.com/api

**Authentication:** API key header (`X-API-Key: xxx`)

**Pricing:**
- Pay-per-use: ~$0.03-0.10 per enrichment
- Volume discounts available
- Only charged for successful enrichments

**Rate Limits:** ~3 requests/second

**Data Quality:**
- ⭐ Comprehensive data (email + phone + company + social)
- ⭐ Good hit rate due to internal waterfall
- ⚠️ Variable quality depending on the source contact
- ⚠️ Newer platform, track record still building

**Strengths:** Full-stack enrichment in one call, pay-per-use, comprehensive data
**Weaknesses:** Higher per-lookup cost, newer platform, variable quality

**Best position in waterfall:** #4 (comprehensive but costlier — use after cheaper email-only providers)

---

### 5. Forager (forager.ai)

**Overview:** B2B contact intelligence platform focused on deep enrichment with company and person data. Targets sales teams.

**API Capabilities:**
- **Person Enrichment** — By email, LinkedIn, or name+company
- **Company Enrichment** — By domain or company name
- **Returns:** Email, phone (including direct dial), title, company details
- **Technographics** — What tech the company uses

**API Docs:** Contact for API access (not publicly documented)

**Authentication:** Bearer token

**Pricing:**
- Custom/enterprise pricing
- Typically $200-500+/month depending on volume
- Annual contracts preferred

**Rate Limits:** ~5 requests/second (varies by plan)

**Data Quality:**
- ⭐ Good direct dial phone numbers
- ⭐ Comprehensive company data and technographics
- ⚠️ API documentation limited
- ⚠️ Pricing not transparent

**Strengths:** Deep B2B data, direct dials, company intelligence
**Weaknesses:** Opaque pricing, limited public API docs, requires sales engagement

**Best position in waterfall:** #5 (deep data, use when simpler providers can't fill gaps)

---

### 6. Wiza (wiza.co)

**Overview:** Specializes in extracting contact data from LinkedIn profiles. Real-time scraping with email verification built in.

**API Capabilities:**
- **Contact Reveal** — Get email from LinkedIn profile URL
- **Search** — Find contacts by name + company
- **Bulk LinkedIn enrichment** — Process LinkedIn lists
- **Returns:** Email (verified), phone, title, company

**API Docs:** https://wiza.co/api (REST API)

**Authentication:** Bearer token

**Pricing:**
- Starter ($83/mo): 100 contacts
- Growth ($166/mo): 300 contacts
- Pro ($333/mo): 1,000 contacts
- Per-contact: ~$0.33-0.83

**Rate Limits:** ~2 requests/second (real-time scraping is slower)

**Data Quality:**
- ⭐ Best for LinkedIn-sourced contacts
- ⭐ High email accuracy (verified at time of retrieval)
- ⭐ Phone numbers included
- ⚠️ Expensive per contact
- ⚠️ Dependent on LinkedIn data availability

**Strengths:** LinkedIn specialization, real-time verified data, good phone numbers
**Weaknesses:** Most expensive per contact, slower (real-time scraping), LinkedIn dependency

**Best position in waterfall:** #6 (use when LinkedIn URL is available and cheaper providers failed)

---

### 7. LeadIQ (leadiq.com)

**Overview:** Enterprise-grade B2B contact intelligence platform. GraphQL API with comprehensive data including verified direct dials.

**API Capabilities:**
- **Person Search** — By name+company, LinkedIn URL, or email
- **Company Enrichment** — Full company profiles
- **Returns:** Email (verified), direct dial phone, title, company details, social profiles
- **CRM integration** — Direct push to Salesforce, HubSpot
- **GraphQL API** — Flexible querying

**API Docs:** https://developer.leadiq.com/ (GraphQL API)

**Authentication:** Bearer token

**Pricing:**
- Essential ($75/user/mo): Limited credits
- Pro ($150/user/mo): More credits + integrations
- Enterprise (custom): Unlimited + API access
- API access typically requires Pro or Enterprise plan

**Rate Limits:** ~2 requests/second

**Data Quality:**
- ⭐ Highest overall data completeness
- ⭐ Excellent direct dial accuracy
- ⭐ Verified emails
- ⭐ Rich company data
- ⚠️ Most expensive option
- ⚠️ API requires higher tier plans

**Strengths:** Most comprehensive data, excellent accuracy, GraphQL flexibility, CRM integration
**Weaknesses:** Most expensive, API access requires premium plans, complex GraphQL API

**Best position in waterfall:** #7 (last resort, highest quality but highest cost)

---

## Recommended Waterfall Order

```
1. Hunter       — Cheap, fast email finding/verification ($0.01-0.10/lookup)
2. FindyMail    — High-accuracy email finding, LinkedIn ($0.05-0.10/lookup)
3. Icypeas      — Supplemental email finding, EU strength ($0.03-0.07/lookup)
4. QuickEnrich  — Full enrichment when email-only providers miss ($0.03-0.10/lookup)
5. Forager      — Deep B2B data, direct dials (custom pricing)
6. Wiza         — LinkedIn-first contacts ($0.33-0.83/contact)
7. LeadIQ       — Last resort, most comprehensive ($0.50-1.50+/lookup)
```

**Key principle:** Start with cheap email-only providers, escalate to expensive full-stack enrichment only when needed. The waterfall short-circuits as soon as all required fields are filled.

**Estimated cost per fully enriched contact:** $0.05-0.30 average (assuming most contacts resolve within first 3 providers)

---

## Implementation Notes

1. **API key management**: All keys stored in ProviderConfig model (encrypted at rest via Django field encryption)
2. **Failover**: Each provider wraps API calls in try/catch with timeout. Failures skip to next provider.
3. **Caching**: 30-day cache on successful enrichments saves 60-80% of API calls in practice.
4. **Rate limiting**: Per-provider rate limiters prevent 429 errors. Daily quotas tracked in DB.
5. **Monitoring**: All API calls logged to EnrichmentLog for cost tracking and provider quality analysis.
6. **Modularity**: New providers added by creating a single file in `enrichment/providers/` and registering in `PROVIDER_REGISTRY`.
