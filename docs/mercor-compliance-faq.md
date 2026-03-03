# Operational Data Licensing — Compliance FAQ

**For Legal and Compliance Review**

---

## What data is collected?

**Operational metadata only — never customer/client data.**

**INCLUDED:**
- Code structure patterns: file organization, import relationships, module dependencies
- Development patterns: commit frequencies, branch strategies, code review cycles
- Project management data: sprint velocities, ticket categorization, estimation accuracy
- Communication metadata: message frequencies, channel usage patterns, response times
- CRM workflow patterns: lead stages, conversion funnels, pipeline velocity

**EXPLICITLY EXCLUDED:**
- Customer personally identifiable information (PII)
- Client account data, financial records, transaction details
- Proprietary algorithms, business logic, or trade secrets
- Customer communications content
- Regulated data (PCI, HIPAA, SOX-covered information)
- Source code content (only structural patterns)
- API keys, credentials, or access tokens

## Is any client or customer data included?

**No.** Zero client data, customer records, or personally identifiable information is collected. The licensing covers only internal operational patterns — how your team works, not who you work for or what you build for them.

## How is anonymization performed?

**Locally on your premises before any data leaves your infrastructure.**

Your team reviews and approves the specific anonymized dataset before transmission. Company names, project names, individual developer identities, and all business-specific identifiers are removed or replaced with generic labels. You maintain full visibility and control over what gets shared.

## What are the licensing terms?

- **Non-exclusive:** You can license the same data to multiple parties
- **No intellectual property transfer:** You retain 100% ownership of all data and code
- **Revocable:** Terminate the agreement at any time with 30 days notice
- **Usage-restricted:** Data can only be used for AI model training, not competitive analysis
- **No derivative claims:** Licensee gains no rights to your actual intellectual property

## Does this comply with SOC2, GDPR, and CCPA?

**Yes.** The data collection stays within established compliance boundaries:

- **SOC2:** No customer data or sensitive business information included
- **GDPR:** No personal data of EU residents collected or transmitted
- **CCPA:** No personal information of California residents involved
- **Industry regulations:** No PCI, HIPAA, SOX, or other regulated data categories touched

## Who sees the data?

**Only anonymized structural data reaches the AI training labs.** No humans review your proprietary code or business processes. The data is used programmatically for training AI models on software development and business operation patterns.

Your actual source code, algorithms, customer data, and business logic remain completely private.

## Can we review the licensing agreement before proceeding?

**Yes.** The standard licensing agreement is designed for rapid legal review — most compliance teams complete their assessment within one business day. The agreement includes specific data handling requirements, usage restrictions, and termination procedures.

## What if we decide to discontinue?

**The licensing is revocable at any time.** Provide 30 days written notice, and the agreement terminates. Any data already licensed remains under the original usage restrictions, but no new data collection occurs after termination.

## Implementation oversight

**Your technical team maintains full control throughout the process.** You approve the anonymization parameters, review the data before transmission, and can audit what gets shared at each step.

---

**Questions?** Contact legal@forwardlane.com for agreement review or implementation details.