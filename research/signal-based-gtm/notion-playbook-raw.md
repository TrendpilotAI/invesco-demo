# The Ultimate Signal-Based List-Building Playbook


## Intent-Based Hiring Signals

What it targets: Companies posting roles that indicate budget allocation for your solution
The logic:
When a company posts a job for "SDR" or "Demand Gen Manager," they're broadcasting two things: budget exists, and the problem is unsolved.
That 72 hours after posting is your window.
Tool Options:
Tool

Purpose

Alternative

Apify

Scrape job boards

PhantomBuster

n8n

Orchestrate workflow

Make.com, Zapier

Conigma

Enrich + filter

Persana AI

Icypeas

Find emails

Snov.io, Hunter

Instantly

Send sequences

Smartlead, Lemlist
SOP: Building the System
Step 1: Configure the scraper (Apify) 
Navigate to Apify Console → Actors → Search "LinkedIn Jobs Scraper"
Input parameters:
Search query: "SDR" OR "Sales Development" OR "Outbound"
Location: United States
Date posted: Past 24 hours
Company size: 11-200 employees
Set to run daily at 6 AM.
Step 2: Route data through n8n
Create workflow:
LinkedIn Jobs (Apify) → Parse JSON → Filter by company size → Send to Conigma webhook
Filter logic: Only pass companies with 11-200 employees and HQ in target geography.
Step 3: Enrich in Conigma
Add these columns:
Company domain (from LinkedIn company URL)
Decision maker (Apollo enrichment: VP Sales, Head of Growth, Founder)
Verified email (Icypeas waterfall)
Tech stack (BuiltWith)
ICP score (AI scoring based on criteria match)
Filter: ICP score > 7, email status = valid
Step 4: Push to sequencer
Map fields:
First name
Company (cleaned)
Job title
Hiring role (from original scrape)
Email Template:
Subject: {{company}} + {{hiring_role}} hire

{{first_name}} - saw the {{hiring_role}} posting. Usually this means [what this means]

We've helped 3 similar companies generate 40+ qualified opps in 60 days while backfilling the role.

Want me to send you the system?

{{sender_name}}
Key Metrics to Track:
Scrape volume per day
Enrichment success rate
Reply rate by job title
Meetings booked per 100 sends

---

## Anonymous Visitor Identification

What it targets: People hitting your website who don't fill out forms 
The logic:
Someone lands on your pricing page at 2pm on a Tuesday. 
They're not browsing. They're evaluating.
If you can identify them, enrich them, and reach out within 24 hours - you're arriving while the problem is still top of mind.
Tool Options:
Tool

Purpose

Price Range

Alternative

RB2B

US visitor ID

$199/mo

Clearbit Reveal

Leadpipe

Multi-geo ID

$149/mo

Albacross

Snitcher

EU-focused

€79/mo

Lead Forensics

Warmly

All-in-one

$700/mo

6sense

Vector

Signal layer

$250/mo

Koala
SOP: Full Implementation
Step 1: Install tracking pixel
For RB2B:
Navigate to Settings → Tracking Script
Copy the JavaScript snippet
Add to your site's <head> section
Verify installation via RB2B dashboard
Output data includes:
Full name
Email (personal or work)
LinkedIn URL
Job title
Company
Page visited
Time on page
Step 2: Configure webhook to Conigma
In RB2B → Integrations → Webhooks → Add Conigma webhook URL
Set trigger conditions:
Page URL contains "/pricing" OR "/demo" OR "/features"
Time on page > 30 seconds
Company size > 10 employees
Step 3: Build enrichment flow in Conigma
Column sequence:
Pull company domain
Enrich with firmographics (Conigma native solution or Apollo or Clearbit inside Conigma)
Find work email (Conigma native waterfall or Apollo → Icypeas)
Validate email (NeverBounce or Reoon)
Add page_visited as personalization variable
Step 4: Route by page behavior
Create conditional logic:
Pricing page → High intent sequence
Case study page → Social proof sequence
Features page → Education sequence
Step 5: Push to sequencer
Include variables:
page_topic (extracted from URL)
company_cleaned
first_name
job_title
Email Templates
Pricing Page:
Subject: {{company}} pricing Q

{{first_name}} - noticed you were poking around our pricing.

What's driving the research right now?

Is it a specific problem or more of a general "what's out there" thing?

{{sender_name}}

PS - if you want, happy to hop on a 15 min demo of the system/ platform? Here’s my calendar: [link]
Case Study Page:
Subject: similar to {{case_study_company}}?

{{first_name}}, saw you checking out how we helped {{case_study_company}}.

If {{company}} is facing something similar, happy to walk through the specifics!

The short version: they went from {{before_state}} to {{after_state}} in {{timeframe}}.
Worst case, you walk away with a free strategy. :)

Worth a 15 min chat?


---

## LinkedIn Engagement Capture

What it targets: People actively engaging with relevant content in your space. 
The logic:
Someone who likes or comments on a post about "outbound deliverability" at 9am is thinking about outbound deliverability at 9am.
That's not a demographic. That's a signal.
The engagement tells you two things: they're active on the platform, and the topic is on their mind. Both matter for conversion.
Tool Options:
Tool

Purpose

Best For

Trigify

Monitor engagement

Real-time alerts

Phantombuster

Scrape reactors

Bulk extraction

Apify

Extract commenters

Cost-effective

Taplio

Track creators

Creator monitoring

Conigma

Enrichment + orchestration

Full workflow

Prosp

LinkedIn outreach

DM sequences
SOP
Step 1: Identify signal-rich creators
Find 10-15 LinkedIn creators who:
Post about topics adjacent to your solution
Have audiences matching your ICP
Post consistently (3+ times/week)
Get meaningful engagement (50+ reactions)
Example: If you sell to RevOps teams, follow creators posting about CRM ops, data quality, attribution.
Step 2: Configure Trigify monitoring
In Trigify:
Add creator LinkedIn URLs
Set alert triggers: "new post with 50+ reactions"
Enable comment extraction
Set ICP filters (job title, company size)
Output includes:
Commenter LinkedIn URL
Comment text
Reaction type
Profile headline
Company
Step 3: Filter for ICP fit
Route to Conigma with filters:
Job title contains: VP, Head, Director, Manager, Founder
Company size: 11-500 employees
Exclude: Students, Recruiters, Competitors
Step 4: Build outreach context
In Conigma, add columns:
Original post topic (manual or AI-extracted)
Comment sentiment (AI analysis)
Company enrichment
Email verification
LinkedIn URL for Prosp import
Step 5: Segment by engagement type
Create conditional logic:
Commenters (highest intent) → Direct outreach via Prosp + email
Reactors (medium intent) → Softer approach, LinkedIn first
Multiple engagements (repeat signal) → Priority list, multi-channel
Step 6: Push to Prosp for LinkedIn outreach
Export filtered list with:
LinkedIn URL
First name
Post topic reference
Comment snippet (if commenter)
Import to Prosp campaign.
Email Templates
Email Template (Commenter):
Email Template (Reactor - Softer):
Full LinkedIn Sequence:
Day

Action

Type

1

Visit profile

Auto

Like recent post

Send connection request

Text

3

DM with context question

4

Voice note with value offer

Voice

7

Resource drop

10

Casual bump

LinkedIn DM Templates
DM After Connection (Text):
DM After Connection (Voice Note Script):
Follow-Up DM (2 days later, if no response):

---

## Post Commenter Extraction

What it targets: People commenting on specific high-engagement posts.
SOP (video):
How to Create Viral Lead Magnets
The 3 Core Sections For Viral Lead Magnets 
 Scroll-Stopping Hook
 Value Proposition 
 Maximizing Reach With Killer CTAs
 Preview Media
How to Respond to All Lead Magnet Comments with AI 
1) 300+ Comment Approach 
2) < 300 Comments Approach

---

## Tech Stack Qualification

What it targets: Companies using (or missing) specific technologies relevant to your solution 
The logic:
Tech stack is a leading indicator of:
Budget (what they're willing to pay for)
Sophistication (how mature their ops are)
Pain points (what's missing from their stack)
If they use Salesforce but no enrichment tool? They have the CRM but no data feeding it.
Tool Options:
Tool

Purpose

Data Source

BuiltWith

Tech detection

Website scanning

Wappalyzer

Browser extension + API

HG Insights

Enterprise tech

Third-party data

Slintel

Tech + intent

Aggregated signals
SOP:
Step 1: Define tech criteria
Create two lists:
Must have: Technologies indicating they're in-market (e.g., Salesforce, HubSpot, Outreach)
Must not have: Technologies indicating they've solved the problem (e.g., your competitors)
Example for an enrichment tool:
Must have: Salesforce OR HubSpot
Must not have: ZoomInfo, Clearbit, Apollo
Step 2: Build company list
Using BuiltWith:
Navigate to Technology Lookup
Search for target technology
Export company list with domains
Or in Conigma:
Use "BuiltWith Tech Stack" enrichment
Add conditional column: "Uses {{target_tech}}"
Step 3: Enrich contacts
For each company:
Find decision makers (Apollo: Head of RevOps, VP Sales, Marketing Ops Manager)
Verify emails
Pull LinkedIn URLs
Step 4: Personalize by tech context
Your message should reference their stack intelligently.
Don't say: "I saw you use HubSpot"
Say: "Most HubSpot teams we work with hit a ceiling with native enrichment..."
Email Template (Missing Tech):
Subject: {{company}} + {{missing_tech_category}}

{{first_name}} - looks like {{company}} runs on {{existing_tech}}.

Most teams at your stage layer in {{missing_tech_category}} to solve {{specific_problem}}.

The before/after is pretty stark: {{result}}.

Worth exploring, or is this already sorted?

{{sender_name}}
Email Template (Competitor Tech):
Subject: {{company}}’s stack?

Hey {{first_name}}, {{company}} uses {{competitor_tool}} right?

Quick question: is the {{specific_feature}} working for you guys?

We've had 3 teams switch this quarter specifically because of {{pain_point}}.

{{specific result they’ve achieved}}

Mind if I send you the strategy they used (60 sec video)?


---

## Funding Event Triggers

What it targets: Companies that just raised capital 
The logic:
Post-funding, companies face pressure to deploy capital fast.
They're hiring, buying tools, and scaling operations.
Tool Options:
Tool

Purpose

Price

Crunchbase Pro

Funding alerts

$49/mo

PitchBook

Comprehensive data

Enterprise

Dealroom

EU-focused

€399/mo

Fundz

Real-time alerts

$29/mo
SOP:
Step 1: Set up alerts
In Crunchbase:
Navigate to Alerts → New Alert
Filter: Funding round > $1M, Industry = {{your_verticals}}
Set frequency: Daily digest
Step 2: Automate extraction
Using n8n:
Connect Crunchbase API
Pull daily funding events
Filter by round size + industry
Push to Conigma
Step 3: Enrich and qualify
In Conigma:
Pull company firmographics
Identify 2-3 decision makers per company
Find emails
Add "Days since funding" as variable
Email Template
Subject: congrats on the round

{{first_name}} - I’m guessing you’re already investing in {{your_category}}?

Asking because {{problem}} becomes a bottleneck faster than people expect in your stage once hiring accelerates.

One thing we saw work for {{competitor}} who also raised {{amount}} in {{date}}: {{specific_approach}}.

Mapped out the process we used for them to achieve {{desired and specific outcome}}. 
Would you hate me if I sent you a 60-second Loom on this?

{{sender_name}}

---

## Local Business Discovery

What it targets: Brick-and-mortar businesses in specific geographies 
The logic:
Local businesses get 1/10th the cold email volume of SaaS companies.
They're also easier to serve at scale because their problems are similar within verticals (dentists face similar challenges to other dentists).
Tool Options:
Tool

Purpose

Data Quality

Apify (Google Maps)

Location scraping

High

Conigma

Enrichment

Icypeas

Finding emails

Medium
SOP:
Step 1: Configure Apify scraper
Using "Google Maps Scraper" actor:
Search query: "{{business_type}} in {{city}}"
Example: "dentists in Austin"
Max results: 200 per query
Output: Business name, website, phone, address, rating, review count
Step 2: Filter for quality
Remove:
Businesses with no website
Ratings below 3.5 stars
Chains (if targeting independents)
Closed businesses
Step 3: Enrich in Conigma
From website domain:
Find owner/decision maker (Google + LinkedIn search)
Pull email (Icypeas)
Verify email
Add personalization:
Review count
Average rating
Business specialty
Step 4: Segment by potential
High potential indicators:
50+ reviews (established)
Active website
Multiple locations
Email Template:
Subject: {{city}} {{business_type}} + {{your_service}} 

Hey {{first_name}} - you've got {{review_count}} reviews on Google - clearly doing something right! This would amplify that.
I work with {{business_type}} in {{city}} specifically.

One thing I keep seeing: {{common_pain_point}}.

The {{business_type}} that solve this typically see {{result}}.

Open to a quick call?

{{sender_name}}

---

## Competitor Audience Mining

What it targets: People following or engaging with your competitors 
The logic:
They're already in-market. They already understand the category. They might already be unhappy with their current solution or open to a better one.
Tool Options:
Tool

Purpose

Works On

Phantombuster

Follower extraction

LinkedIn company pages

Scrapeli

Follower scraping

Trigify

Engagement monitoring

LinkedIn posts

BuiltWith

Customer identification

Websites
SOP:
Step 1: Identify competitor LinkedIn pages
List 5-10 direct competitors.
Pull their LinkedIn company page URLs.
Step 2: Extract followers
Using Scrapeli or Phantombuster:
Input: Company LinkedIn URL
Output: Follower profiles (name, headline, company, LinkedIn URL)
Step 3: Filter for ICP
In Conigma:
Remove employees of the competitor
Filter by job title (decision makers only)
Filter by company size
Enrich with email
Step 4: Build differentiated messaging
Don't bash the competitor. Position your differentiation.
Focus on:
What you do that they don't
Pain points that solution doesn't solve
Specific use cases where you win
Email Template:
Subject: {{competitor}} alternative?

{{first_name}} - noticed you're following {{competitor}} on LinkedIn.

Quick question: are you using them, or still evaluating?

If it's the latter - we just introduced {{specific_thing}} in {{your tool}} and have received {{specific result}} from users so far! 

Would that benefit you guys as well? 

Happy to set you up with a free trial if it resonates?

{{sender_name}}
DM Template:
Hey {{first_name}}, you follow {{competitor}} right? Have you tried {{your tool}}?

We just introduced {{specific_thing}} in {{your tool}} and have received {{specific result}} from users so far! 


---

## Sales Navigator Power Filtering

What it targets: LinkedIn users matching specific criteria combinations
The logic:
Sales Navigator's filters are powerful, but most people use them wrong. 
The trick: layer filters to find inflection points - job changes, company growth, recent activity.
SOP (video):

---

## G2/Review Site Intent

What it targets: Companies actively researching solutions on review sites 
The logic:
Someone reading reviews on G2 is further along than someone who saw a LinkedIn post.
They're comparing. They're evaluating. They're about to buy something.
Tool Options:
Tool

Purpose

Data Type

G2 Buyer Intent

Intent signals

First-party

TrustRadius

Intent data

Bombora

Intent aggregation

Third-party

6sense

Intent + identification

Enterprise
SOP:
Step 1: Set up G2 Buyer Intent (if you have a G2 profile)
In G2 Seller Dashboard:
Navigate to Buyer Intent
Set filters: Company size, industry, geography
Enable weekly export or API connection
Data includes:
Companies researching your category
Specific pages viewed
Comparison activity
Step 2: If no G2 profile - alternative approach
Manual research:
Find competitors on G2
Read recent reviews
Extract reviewer companies + names
Research on LinkedIn
This is slower but works without G2 access.
Step 3: Enrich with decision makers
For each company showing intent:
Find 2-3 relevant contacts in Conigma
Prioritize: recent job changers, active LinkedIn users
Verify emails with Reoon
Step 4: Craft research-aware messaging
Don't say "I saw you on G2" - that's weird.
Reference the problem they're researching instead.
Email Template:
Subject: {{your_category}} for {{company}}? 

{{first_name}} - if {{company}} is evaluating {{your_category}} right now, one thing worth knowing:

Most teams focus on {{common_criteria}}, but the teams seeing the best results optimize for {{overlooked_criteria}}.

We've helped {{similar_company}} specifically by {{approach}}.

If you're in active research mode, happy to share the evaluation framework we use.
Interested?

{{sender_name}}

---

## Minimal Viable Stack

What it targets: Anyone who wants results without going broke due to a gazillion tool subscriptions. 
The logic:
You don’t need 15 tools to get results. 
This workflow covers lead sourcing through sending with 3 tools.
Tools:
Tool

Role

Apollo

Lead sourcing

Conigma

Enrichment + logic

Instantly

Sending
SOP:
Step 1: Source in Apollo 
Navigate to People Search.
Apply filters:
Company headcount: 11-200
Industry: {{your_target}}
Job titles: {{decision_makers}}
Seniority: VP, Director, Manager, Owner
Save search. Enable auto-refresh.
Step 2: Export to Conigma
Option A: Direct integration
Connect Apollo to Conigma
Set up scheduled pull
Option B: Manual export
Export CSV from Apollo
Import to a Conigma table
Step 3: Enrich and score
In Conigma, add columns:
Company website (if missing)
LinkedIn URL (Apollo often has this)
Tech stack (BuiltWith)
Email verification (NeverBounce)
ICP score (AI formula based on your criteria)
Filter: Valid email = TRUE, ICP score >= 7
Step 4: Generate personalization
Use Conigma AI to create:
Custom first line (based on LinkedIn headline + company)
Company hook (based on website scrape)
Relevant case study match
Step 5: Push to Instantly
Via webhook or CSV export:
Map: email, first_name, company_cleaned, custom_first_line, case_study_reference
Load into campaign
Set sending: 30-50/day per inbox
Step 6: Monitor and iterate
Track weekly:
Reply rate by ICP segment
Bounce rate
Meeting conversion rate
Double down on what works. Cut what doesn't.

---
