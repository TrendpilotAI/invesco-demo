# Signal Studio — Salesforce Deployment Specification

**Version:** 1.0  
**Date:** March 3, 2026  
**Authors:** ForwardLane Engineering  
**Audience:** Salesforce development team (ISV/SI partner or internal SF devs)  
**Status:** Ready for implementation

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Deployment Options](#3-deployment-options)
4. [Option A: Native LWC + Apex Proxy (Recommended)](#4-option-a-native-lwc--apex-proxy)
5. [Option B: Iframe Embed with postMessage Bridge](#5-option-b-iframe-embed-with-postmessage-bridge)
6. [Backend API Reference](#6-backend-api-reference)
7. [Data Models & Response Schemas](#7-data-models--response-schemas)
8. [Salesforce Configuration Requirements](#8-salesforce-configuration-requirements)
9. [SLDS Design Patterns Already Implemented](#9-slds-design-patterns-already-implemented)
10. [Authentication & Security](#10-authentication--security)
11. [Mobile Considerations](#11-mobile-considerations)
12. [Testing & QA Plan](#12-testing--qa-plan)
13. [Deployment Checklist](#13-deployment-checklist)
14. [Appendix: File Inventory](#14-appendix-file-inventory)

---

## 1. Executive Summary

Signal Studio is ForwardLane's AI-powered distribution intelligence platform, currently deployed as a Next.js 15 application on Railway. The **Easy Button** module is a Salesforce-embeddable interface that provides wholesalers with:

- **Territory Dashboard** — Advisor rankings, AUM, risk/opportunity scores
- **Meeting Brief** — AI-generated meeting prep for a specific Contact/Account record
- **Signal Library** — Active signals grouped by type (AUM Decline, Cross-Sell, Revenue Defense, etc.)
- **Action Queue** — Prioritized action items derived from active signals
- **NL→SQL Query** — Natural language questions translated to SQL against the analytical database
- **Signal Runner** — Execute named signal templates on demand

The app is **already designed with SLDS (Salesforce Lightning Design System)** styling, postMessage bridge for Salesforce communication, and responsive/mobile layouts. This spec details how to deploy it natively within a Salesforce org.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Salesforce Org (Invesco)                    │
│                                                              │
│  ┌──────────────────────┐    ┌───────────────────────────┐  │
│  │   LWC Components     │    │     Apex Controllers      │  │
│  │                       │    │                           │  │
│  │  signalStudioLauncher │───▶│  SignalStudioService.cls  │  │
│  │  meetingBriefCard     │    │  MeetingPrepService.cls   │  │
│  │  territoryDashboard   │    │  NLQueryService.cls       │  │
│  │  signalLibrary        │    │  SignalRunnerService.cls   │  │
│  │  actionQueue          │    │                           │  │
│  │  nlQueryPanel         │    │  (Named Credential:       │  │
│  │  mobileBrief          │    │   ForwardLane_API)        │  │
│  └──────────────────────┘    └──────────┬────────────────┘  │
│                                          │                   │
└──────────────────────────────────────────┼───────────────────┘
                                           │ HTTPS
                                           ▼
┌─────────────────────────────────────────────────────────────┐
│              ForwardLane Backend (Railway)                    │
│                                                              │
│  Django REST Framework                                       │
│  URL: https://django-backend-production-3b94.up.railway.app  │
│                                                              │
│  /api/v1/easy-button/dashboard/          GET                 │
│  /api/v1/easy-button/clients/            GET                 │
│  /api/v1/easy-button/clients/{id}/       GET                 │
│  /api/v1/easy-button/signals/            GET                 │
│  /api/v1/easy-button/actions/            GET                 │
│  /api/v1/easy-button/signals/run/{id}/   POST                │
│  /api/v1/easy-button/meeting-prep/{id}/  GET                 │
│  /api/v1/easy-button/nl-query/           POST                │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐                     │
│  │  PostgreSQL     │  │  PostgreSQL     │                    │
│  │  (default)      │  │  (analytical)   │                    │
│  └────────────────┘  └────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Deployment Options

| Approach | Pros | Cons | Recommended For |
|----------|------|------|-----------------|
| **A: Native LWC + Apex Proxy** | Full SLDS native feel, offline support, no iframe restrictions, Salesforce mobile compatible | Higher dev effort (rewrite UI in LWC HTML/JS) | Production deployment, mobile-first |
| **B: Iframe Embed + postMessage** | Fastest to deploy, reuse existing Next.js app, already has postMessage bridge | CSP restrictions, limited mobile support, no offline, iframe UX issues | Quick demo, POC, interim solution |
| **C: Hybrid** | LWC shell with iframe for complex views (NL→SQL), native for simple views (Meeting Brief) | Mixed UX paradigms | Phased rollout |

**Recommendation:** Start with **Option B** for immediate demos (it's already built), then migrate to **Option A** for production. The UI is already SLDS-styled, making the LWC rewrite largely a porting exercise.

---

## 4. Option A: Native LWC + Apex Proxy

### 4.1 Apex Controllers

Each API endpoint maps to an Apex class. All callouts go through a single Named Credential.

#### `SignalStudioService.cls` — Dashboard, Clients, Signals, Actions

```apex
public with sharing class SignalStudioService {

    private static final String BASE_PATH = '/api/v1/easy-button';

    // ── Dashboard KPIs ────────────────────────────────────────────
    @AuraEnabled(cacheable=true)
    public static Map<String, Object> getDashboardStats() {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ForwardLane_API' + BASE_PATH + '/dashboard/');
        req.setMethod('GET');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(10000);

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() != 200) {
            throw new AuraHandledException(
                'Dashboard API error: ' + res.getStatusCode()
            );
        }
        return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
    }

    // ── Advisor List (paginated) ──────────────────────────────────
    @AuraEnabled
    public static Map<String, Object> getAdvisors(
        String segment,
        String search,
        String ordering,
        String direction,
        Integer pageNum,
        Integer pageSize
    ) {
        String path = BASE_PATH + '/clients/?'
            + 'page=' + (pageNum != null ? pageNum : 1)
            + '&page_size=' + (pageSize != null ? pageSize : 20);

        if (String.isNotBlank(segment)) path += '&segment=' + EncodingUtil.urlEncode(segment, 'UTF-8');
        if (String.isNotBlank(search))  path += '&search=' + EncodingUtil.urlEncode(search, 'UTF-8');
        if (String.isNotBlank(ordering)) path += '&ordering=' + ordering;
        if (String.isNotBlank(direction)) path += '&direction=' + direction;

        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ForwardLane_API' + path);
        req.setMethod('GET');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(15000);

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() != 200) {
            throw new AuraHandledException('Advisor list error: ' + res.getStatusCode());
        }
        return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
    }

    // ── Advisor Detail ────────────────────────────────────────────
    @AuraEnabled(cacheable=true)
    public static Map<String, Object> getAdvisorDetail(String advisorId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ForwardLane_API' + BASE_PATH + '/clients/' + advisorId + '/');
        req.setMethod('GET');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(15000);

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() == 404) {
            throw new AuraHandledException('Advisor not found: ' + advisorId);
        }
        if (res.getStatusCode() != 200) {
            throw new AuraHandledException('Advisor detail error: ' + res.getStatusCode());
        }
        return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
    }

    // ── Signal List ───────────────────────────────────────────────
    @AuraEnabled(cacheable=true)
    public static List<Object> getSignals() {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ForwardLane_API' + BASE_PATH + '/signals/');
        req.setMethod('GET');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(10000);

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() != 200) {
            throw new AuraHandledException('Signals error: ' + res.getStatusCode());
        }
        return (List<Object>) JSON.deserializeUntyped(res.getBody());
    }

    // ── Action Items ──────────────────────────────────────────────
    @AuraEnabled(cacheable=true)
    public static List<Object> getActions(Integer limitCount) {
        String path = BASE_PATH + '/actions/';
        if (limitCount != null) path += '?limit=' + limitCount;

        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ForwardLane_API' + path);
        req.setMethod('GET');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(10000);

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() != 200) {
            throw new AuraHandledException('Actions error: ' + res.getStatusCode());
        }
        return (List<Object>) JSON.deserializeUntyped(res.getBody());
    }
}
```

#### `MeetingPrepService.cls`

```apex
public with sharing class MeetingPrepService {

    // ── Meeting Prep Brief ────────────────────────────────────────
    @AuraEnabled
    public static Map<String, Object> getMeetingPrep(String advisorId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint(
            'callout:ForwardLane_API/api/v1/easy-button/meeting-prep/'
            + EncodingUtil.urlEncode(advisorId, 'UTF-8') + '/'
        );
        req.setMethod('GET');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000); // Meeting prep may involve AI generation

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() == 404) {
            throw new AuraHandledException('Advisor not found');
        }
        if (res.getStatusCode() != 200) {
            throw new AuraHandledException('Meeting prep error: ' + res.getStatusCode());
        }
        return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
    }
}
```

#### `NLQueryService.cls`

```apex
public with sharing class NLQueryService {

    // ── Natural Language → SQL Query ──────────────────────────────
    @AuraEnabled
    public static Map<String, Object> executeNLQuery(String question) {
        if (String.isBlank(question)) {
            throw new AuraHandledException('Question is required');
        }

        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ForwardLane_API/api/v1/easy-button/nl-query/');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000); // LLM-backed, may take time

        Map<String, String> body = new Map<String, String>();
        body.put('query', question);
        req.setBody(JSON.serialize(body));

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() == 422) {
            // Query executed but SQL errored
            return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
        }
        if (res.getStatusCode() != 200) {
            throw new AuraHandledException('NL Query error: ' + res.getStatusCode());
        }
        return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
    }
}
```

#### `SignalRunnerService.cls`

```apex
public with sharing class SignalRunnerService {

    // Available signal templates
    public static final Set<String> VALID_TEMPLATES = new Set<String>{
        'aum-decline-alert',
        'cross-sell-etf',
        'revenue-defense',
        'competitor-heavy',
        'dormant-reactivation',
        'growing-fast'
    };

    @AuraEnabled
    public static Map<String, Object> runSignalTemplate(String templateId) {
        if (!VALID_TEMPLATES.contains(templateId)) {
            throw new AuraHandledException('Invalid template: ' + templateId);
        }

        HttpRequest req = new HttpRequest();
        req.setEndpoint(
            'callout:ForwardLane_API/api/v1/easy-button/signals/run/'
            + templateId + '/'
        );
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000);

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() != 200) {
            throw new AuraHandledException('Signal run error: ' + res.getStatusCode());
        }
        return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
    }
}
```

### 4.2 LWC Component Structure

The following LWC components map to the existing Next.js pages:

```
force-app/main/default/lwc/
├── signalStudioLauncher/       # App launcher grid (→ page.tsx)
│   ├── signalStudioLauncher.html
│   ├── signalStudioLauncher.js
│   ├── signalStudioLauncher.css
│   └── signalStudioLauncher.js-meta.xml
│
├── territoryDashboard/         # Advisor table + stats (→ dashboard/page.tsx)
│   ├── territoryDashboard.html
│   ├── territoryDashboard.js
│   ├── territoryDashboard.css
│   └── territoryDashboard.js-meta.xml
│
├── meetingBriefCard/           # Contact record card (→ salesforce/page.tsx)
│   ├── meetingBriefCard.html   # HERO component — accordion sections
│   ├── meetingBriefCard.js
│   ├── meetingBriefCard.css
│   └── meetingBriefCard.js-meta.xml
│
├── signalLibrary/              # Signal list + runner
│   ├── signalLibrary.html
│   ├── signalLibrary.js
│   ├── signalLibrary.css
│   └── signalLibrary.js-meta.xml
│
├── actionQueue/                # Prioritized action items
│   ├── actionQueue.html
│   ├── actionQueue.js
│   ├── actionQueue.css
│   └── actionQueue.js-meta.xml
│
├── nlQueryPanel/               # Natural language query input + results table
│   ├── nlQueryPanel.html
│   ├── nlQueryPanel.js
│   ├── nlQueryPanel.css
│   └── nlQueryPanel.js-meta.xml
│
├── mobileBrief/                # Mobile-optimized meeting prep (→ mobile/page.tsx)
│   ├── mobileBrief.html
│   ├── mobileBrief.js
│   ├── mobileBrief.css
│   └── mobileBrief.js-meta.xml
│
└── signalStudioUtils/          # Shared utilities (icons, formatters, constants)
    ├── signalStudioUtils.js
    └── signalStudioConstants.js
```

### 4.3 Example LWC: Meeting Brief Card

This is the **hero component** — embedded on the Contact or Account record page. It shows AI-generated meeting prep for the currently viewed advisor.

**`meetingBriefCard.js-meta.xml`**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>Signal Studio — Meeting Brief</masterLabel>
    <description>AI-generated meeting preparation brief for ForwardLane advisors</description>
    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
        <target>lightning__UtilityBar</target>
        <target>lightningCommunity__Page</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightning__RecordPage">
            <objects>
                <object>Contact</object>
                <object>Account</object>
            </objects>
            <property name="advisorIdField" type="String" default="ForwardLane_Advisor_ID__c"
                      label="Advisor ID Field" description="API name of the field containing the ForwardLane advisor ID"/>
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

**`meetingBriefCard.html`**
```html
<template>
    <lightning-card>
        <!-- Header -->
        <div slot="title" class="slds-grid slds-grid_vertical-align-center">
            <lightning-icon icon-name="standard:contact" size="small" class="slds-m-right_small"></lightning-icon>
            <span class="slds-text-heading_small">Meeting Brief</span>
            <template if:true={advisorName}>
                <lightning-badge label={advisorName} class="slds-m-left_small"></lightning-badge>
            </template>
        </div>
        <div slot="actions">
            <lightning-button-icon
                icon-name="utility:refresh"
                alternative-text="Refresh"
                onclick={handleRefresh}
                class="slds-m-right_x-small">
            </lightning-button-icon>
        </div>

        <!-- Loading State -->
        <template if:true={isLoading}>
            <div class="slds-p-around_medium slds-align_absolute-center">
                <lightning-spinner alternative-text="Loading meeting brief" size="medium"></lightning-spinner>
            </div>
        </template>

        <!-- Error State -->
        <template if:true={errorMessage}>
            <div class="slds-p-around_medium">
                <div class="slds-notify slds-notify_alert slds-alert_warning" role="alert">
                    <p>{errorMessage}</p>
                </div>
            </div>
        </template>

        <!-- Brief Content -->
        <template if:true={brief}>
            <!-- Risk / Opportunity Score Bar -->
            <div class="slds-p-horizontal_medium slds-p-vertical_small slds-border_bottom">
                <div class="slds-grid slds-gutters_small">
                    <div class="slds-col slds-size_1-of-2">
                        <p class="slds-text-title_caps slds-m-bottom_xx-small">Risk Score</p>
                        <lightning-progress-bar value={brief.risk_score} size="large"
                            variant={riskVariant}></lightning-progress-bar>
                    </div>
                    <div class="slds-col slds-size_1-of-2">
                        <p class="slds-text-title_caps slds-m-bottom_xx-small">Opportunity</p>
                        <lightning-progress-bar value={brief.opportunity_score} size="large"
                            variant="brand"></lightning-progress-bar>
                    </div>
                </div>
            </div>

            <!-- Accordion Sections (mirrors salesforce/page.tsx) -->
            <lightning-accordion allow-multiple-sections-open active-section-name={activeSections}>

                <!-- Signals -->
                <lightning-accordion-section name="signals" label="Active Signals">
                    <template for:each={brief.signals_triggered} for:item="signal">
                        <lightning-pill key={signal} label={signal} class="slds-m-right_xx-small slds-m-bottom_xx-small">
                        </lightning-pill>
                    </template>
                </lightning-accordion-section>

                <!-- Top Holdings -->
                <lightning-accordion-section name="holdings" label="Top Holdings">
                    <lightning-datatable
                        key-field="ticker"
                        data={brief.top_holdings}
                        columns={holdingsColumns}
                        hide-checkbox-column>
                    </lightning-datatable>
                </lightning-accordion-section>

                <!-- Talking Points -->
                <lightning-accordion-section name="talking" label="Talking Points">
                    <template for:each={brief.talking_points} for:item="point">
                        <div key={point} class="slds-p-vertical_xx-small slds-border_bottom">
                            <p class="slds-text-body_regular">{point}</p>
                        </div>
                    </template>
                </lightning-accordion-section>

                <!-- Action Items -->
                <lightning-accordion-section name="actions" label="Recommended Actions">
                    <template for:each={brief.action_items} for:item="action">
                        <div key={action.id} class="slds-media slds-p-vertical_xx-small">
                            <div class="slds-media__figure">
                                <lightning-icon icon-name={action.iconName} size="small"></lightning-icon>
                            </div>
                            <div class="slds-media__body">
                                <p class="slds-text-body_regular">{action.description}</p>
                                <p class="slds-text-body_small slds-text-color_weak">{action.urgency}</p>
                            </div>
                        </div>
                    </template>
                </lightning-accordion-section>

            </lightning-accordion>

            <!-- Quick Actions Footer -->
            <div class="slds-p-around_small slds-border_top">
                <lightning-button-group>
                    <lightning-button label="Log Call" onclick={handleLogCall} variant="neutral"
                        icon-name="utility:call"></lightning-button>
                    <lightning-button label="Send Email" onclick={handleSendEmail} variant="neutral"
                        icon-name="utility:email"></lightning-button>
                    <lightning-button label="Create Task" onclick={handleCreateTask} variant="neutral"
                        icon-name="utility:task"></lightning-button>
                    <lightning-button label="Push to CRM" onclick={handlePushToCRM} variant="brand"
                        icon-name="utility:upload"></lightning-button>
                </lightning-button-group>
            </div>
        </template>
    </lightning-card>
</template>
```

**`meetingBriefCard.js`**
```javascript
import { LightningElement, api, wire, track } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import getMeetingPrep from '@salesforce/apex/MeetingPrepService.getMeetingPrep';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { NavigationMixin } from 'lightning/navigation';

export default class MeetingBriefCard extends NavigationMixin(LightningElement) {
    @api recordId;          // Salesforce Contact/Account record ID
    @api advisorIdField = 'ForwardLane_Advisor_ID__c'; // Configurable field

    @track brief;
    @track isLoading = false;
    @track errorMessage;

    advisorId;
    advisorName;

    // Fetch the ForwardLane advisor ID from the Contact/Account record
    @wire(getRecord, {
        recordId: '$recordId',
        fields: '$fieldsToLoad'
    })
    wiredRecord({ error, data }) {
        if (data) {
            // Dynamic field access
            const fields = data.fields;
            this.advisorId = fields[this.advisorIdField]?.value;
            this.advisorName = fields['Name']?.value || fields['FirstName']?.value;
            if (this.advisorId) {
                this.loadMeetingPrep();
            }
        } else if (error) {
            this.errorMessage = 'Could not load record data';
        }
    }

    get fieldsToLoad() {
        // Dynamic: load the configured advisor ID field + Name
        const obj = this.objectApiName || 'Contact';
        return [
            `${obj}.${this.advisorIdField}`,
            `${obj}.Name`
        ];
    }

    get activeSections() {
        return ['signals', 'talking']; // Default open sections
    }

    get riskVariant() {
        if (!this.brief) return 'base';
        return this.brief.risk_score > 70 ? 'warning' : 'base';
    }

    get holdingsColumns() {
        return [
            { label: 'Ticker', fieldName: 'ticker', type: 'text' },
            { label: 'Fund', fieldName: 'name', type: 'text' },
            { label: 'Allocation', fieldName: 'allocation', type: 'percent',
              typeAttributes: { minimumFractionDigits: 1 } },
            { label: 'AUM', fieldName: 'aum', type: 'currency' },
            { label: 'Asset Class', fieldName: 'asset_class', type: 'text' },
        ];
    }

    async loadMeetingPrep() {
        this.isLoading = true;
        this.errorMessage = undefined;
        try {
            const result = await getMeetingPrep({ advisorId: this.advisorId });
            this.brief = this.transformBrief(result);
        } catch (error) {
            this.errorMessage = error.body?.message || 'Failed to load meeting brief';
        } finally {
            this.isLoading = false;
        }
    }

    transformBrief(raw) {
        // Map action items to include icon names for SLDS
        const actionIconMap = {
            'call': 'utility:call',
            'email': 'utility:email',
            'meeting': 'utility:event',
            'review': 'utility:preview',
        };

        return {
            ...raw,
            action_items: (raw.action_items || []).map((a, i) => ({
                ...a,
                id: i,
                iconName: actionIconMap[a.type] || 'utility:task',
            }))
        };
    }

    handleRefresh() {
        this.loadMeetingPrep();
    }

    handleLogCall() {
        this[NavigationMixin.Navigate]({
            type: 'standard__quickAction',
            attributes: {
                apiName: 'LogACall',
            },
        });
    }

    handleSendEmail() {
        this[NavigationMixin.Navigate]({
            type: 'standard__quickAction',
            attributes: {
                apiName: 'SendEmail',
            },
        });
    }

    handleCreateTask() {
        this[NavigationMixin.Navigate]({
            type: 'standard__objectPage',
            attributes: {
                objectApiName: 'Task',
                actionName: 'new',
            },
        });
    }

    handlePushToCRM() {
        // Push signal data as a new Task or update custom fields on the record
        this.dispatchEvent(
            new ShowToastEvent({
                title: 'Success',
                message: 'Signal data pushed to CRM',
                variant: 'success',
            })
        );
    }
}
```

---

## 5. Option B: Iframe Embed with postMessage Bridge

**This is already built.** The existing Next.js app includes a full postMessage bridge.

### 5.1 LWC Wrapper for Iframe

```html
<!-- signalStudioEmbed.html -->
<template>
    <lightning-card title="Signal Studio">
        <div class="iframe-container">
            <iframe
                src={iframeSrc}
                width="100%"
                height="700"
                frameborder="0"
                sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                lwc:dom="manual">
            </iframe>
        </div>
    </lightning-card>
</template>
```

```javascript
// signalStudioEmbed.js
import { LightningElement, api } from 'lwc';

const SIGNAL_STUDIO_URL = 'https://signal-studio-production-a258.up.railway.app';

export default class SignalStudioEmbed extends LightningElement {
    @api recordId;

    get iframeSrc() {
        let url = SIGNAL_STUDIO_URL + '/easy-button?embed=true';
        if (this.recordId) {
            url += '&recordId=' + this.recordId;
        }
        return url;
    }

    connectedCallback() {
        window.addEventListener('message', this.handleMessage.bind(this));
    }

    disconnectedCallback() {
        window.removeEventListener('message', this.handleMessage.bind(this));
    }

    handleMessage(event) {
        // Validate origin
        if (!event.origin.startsWith(SIGNAL_STUDIO_URL)) return;

        const msg = event.data;
        if (!msg?.type?.startsWith('FL_')) return;

        switch (msg.type) {
            case 'FL_READY':
                // Send context to iframe
                this.sendContext();
                break;
            case 'FL_RESIZE_REQUEST':
                // Resize iframe
                const iframe = this.template.querySelector('iframe');
                if (iframe && msg.payload?.height) {
                    iframe.style.height = msg.payload.height + 'px';
                }
                break;
            case 'FL_ADVISOR_OPEN':
                console.log('Advisor opened:', msg.payload);
                break;
            case 'FL_MEETING_PREP':
                console.log('Meeting prep requested:', msg.payload);
                break;
        }
    }

    sendContext() {
        const iframe = this.template.querySelector('iframe');
        if (iframe) {
            iframe.contentWindow.postMessage({
                type: 'FL_CONTEXT',
                payload: {
                    contactId: this.recordId,
                    // token: 'jwt-token-here' // If needed
                }
            }, SIGNAL_STUDIO_URL);
        }
    }
}
```

### 5.2 Existing postMessage Protocol

The Next.js app already implements this bidirectional protocol:

**Inbound (Salesforce → Signal Studio):**

| Message Type | Payload | Purpose |
|---|---|---|
| `FL_CONTEXT` | `{ contactId, accountId, advisorId, token }` | Pass record context and auth token |
| `FL_RESIZE` | `{ height: number }` | Force iframe height |
| `FL_PING` | — | Health check |

**Outbound (Signal Studio → Salesforce):**

| Message Type | Payload | Purpose |
|---|---|---|
| `FL_READY` | — | App initialized, ready for context |
| `FL_PONG` | — | Ping response |
| `FL_RESIZE_REQUEST` | `{ height: number }` | Request parent to resize iframe |
| `FL_ADVISOR_OPEN` | `{ advisorId, advisorName }` | User clicked an advisor row |
| `FL_SIGNAL_RUN` | `{ signalId, signalName }` | User ran a signal template |
| `FL_ACTION_TAKEN` | `{ actionType, advisorId, advisorName }` | User took an action (call, email, etc.) |
| `FL_MEETING_PREP` | `{ advisorId, advisorName }` | User opened meeting prep |

**Source file:** `app/easy-button/salesforce-embed.tsx`

---

## 6. Backend API Reference

**Base URL:** `https://django-backend-production-3b94.up.railway.app/api/v1/easy-button`

### 6.1 `GET /dashboard/`

Returns high-level KPIs for the Easy Button home dashboard.

**Response `200`:**
```json
{
    "total_aum": 156000000000,
    "advisor_count": 500,
    "at_risk_count": 47,
    "opportunities_count": 128,
    "aum_change_pct": -3.2
}
```

### 6.2 `GET /clients/`

Paginated list of advisors with key metrics.

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `segment` | string | — | Filter by channel: `RIA`, `BD`, `Bank`, `Insurance` |
| `search` | string | — | Partial match on `full_name` or `firm_name` |
| `ordering` | string | `aum` | Sort by: `aum`, `change`, `risk`, `name`, `firm` |
| `direction` | string | `desc` | Sort direction: `asc` or `desc` |
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Results per page (max 100) |

**Response `200`:**
```json
{
    "count": 500,
    "page": 1,
    "page_size": 20,
    "total_pages": 25,
    "results": [
        {
            "id": "adv_0001",
            "name": "Smith & Associates Wealth Management",
            "firm": "Smith & Associates",
            "segment": "Wirehouse",
            "aum": 8500000,
            "change": -26.0,
            "risk": 82,
            "opportunity": 85,
            "lastContact": null,
            "status": "critical",
            "active_signals": 3
        }
    ]
}
```

**Status values:** `critical` (change < -15%), `declining` (-15% to -5%), `stable` (-5% to +10%), `growing` (> +10%)

### 6.3 `GET /clients/{advisor_id}/`

Full detail for a single advisor: profile, holdings, flows, signals.

**Path Parameters:**
- `advisor_id` — Text or numeric ID (e.g., `adv_0001`, `42`)

**Response `200`:**
```json
{
    "advisor_id": "adv_0001",
    "full_name": "John Smith",
    "firm_name": "Smith & Associates",
    "channel": "Wirehouse",
    "region": "Northeast",
    "email": "jsmith@smithwealth.com",
    "phone": "+1 (415) 555-0101",
    "city": "New York",
    "state": "NY",
    "aum_current": 8500000,
    "aum_12m_ago": 11500000,
    "aum_change_pct": -26.1,
    "client_count": 145,
    "avg_account_size": 58621,
    "risk_score": 82,
    "opportunity_score": 85,
    "status": "critical",
    "top_holdings": [
        {
            "holding_id": 1,
            "symbol": "INVGX",
            "fund_name": "Invesco Growth Fund",
            "fund_type": "Equity",
            "fund_family": "Invesco",
            "aum_in_fund": 2754000,
            "pct_of_aum": 32.4,
            "as_of_date": "2026-02-28"
        }
    ],
    "recent_flows": [
        {
            "flow_id": 1,
            "symbol": "INVGX",
            "flow_month": "2026-02-01",
            "net_flow": -120000,
            "gross_inflow": 50000,
            "gross_outflow": 170000
        }
    ],
    "active_signals": [
        {
            "signal_id": 1,
            "signal_type": "AUM_DECLINE",
            "signal_score": 8.5,
            "signal_data": {},
            "triggered_at": "2026-02-15T10:30:00Z",
            "status": "active"
        }
    ]
}
```

### 6.4 `GET /signals/`

Active signals grouped by `signal_type`.

**Response `200`:**
```json
[
    {
        "id": 1,
        "type": "risk",
        "title": "AUM Decline > 25%",
        "count": 7,
        "severity": "high",
        "color": "#ef4444"
    },
    {
        "id": 2,
        "type": "opportunity",
        "title": "Cross-Sell ETF",
        "count": 12,
        "severity": "medium",
        "color": "#22c55e"
    }
]
```

**Signal Types:**

| `signal_type` | Title | Category | Color | Severity |
|---|---|---|---|---|
| `AUM_DECLINE` | AUM Decline Alert | risk | `#ef4444` | high |
| `REVENUE_DEFENSE` | Revenue Defense | risk | `#f59e0b` | high |
| `COMPETITOR_HEAVY` | Competitor-Heavy Portfolio | risk | `#ef4444` | high |
| `CROSS_SELL_ETF` | Cross-Sell ETF Opportunity | opportunity | `#22c55e` | medium |
| `RIA_CONVERSION` | RIA Conversion Ready | opportunity | `#3b82f6` | medium |
| `DORMANT` | Dormant Account Reactivation | opportunity | `#f59e0b` | medium |
| `GROWTH_STAR` | Growing Fast | opportunity | `#22c55e` | low |
| `CHAMPION` | Champion Advisor | opportunity | `#8b5cf6` | low |
| `MEETING_SOON` | Meeting Upcoming | opportunity | `#6366f1` | low |

### 6.5 `GET /actions/`

Prioritized action items derived from active signals.

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `limit` | int | 50 | Max items (up to 200) |

**Response `200`:**
```json
[
    {
        "id": 1,
        "client": "Smith & Associates",
        "action": "Call about AUM Decline Alert: -26.0% AUM change",
        "type": "call",
        "time": "Now",
        "priority": "high"
    },
    {
        "id": 2,
        "client": "Chen Financial",
        "action": "Review Cross-Sell ETF Opportunity opportunity",
        "type": "email",
        "time": "This week",
        "priority": "medium"
    }
]
```

### 6.6 `POST /signals/run/{template_id}/`

Execute a named signal template. Creates new signal records.

**Path Parameters:**
- `template_id` — One of: `aum-decline-alert`, `cross-sell-etf`, `revenue-defense`, `competitor-heavy`, `dormant-reactivation`, `growing-fast`

**Response `200`:**
```json
{
    "template_id": "aum-decline-alert",
    "status": "completed",
    "message": "Signal 'AUM Decline Alert' generated for 47 advisors.",
    "count": 47
}
```

### 6.7 `GET /meeting-prep/{advisor_id}/`

AI-generated meeting preparation brief.

**Response `200`:**
```json
{
    "advisor_id": "adv_0001",
    "advisor_name": "John Smith",
    "firm": "Smith & Associates",
    "aum": 8500000,
    "aum_change_pct": -26.1,
    "segment": "Wirehouse",
    "risk_score": 82,
    "opportunity_score": 85,
    "assigned_wholesaler": "Jordan Mitchell",
    "last_contact": "3 days ago",
    "signals_triggered": ["AUM_DECLINE", "REVENUE_DEFENSE"],
    "top_holdings": [
        {
            "ticker": "INVGX",
            "name": "Invesco Growth Fund",
            "allocation": 32.4,
            "aum": 2754000,
            "change_30d": null,
            "asset_class": "Equity"
        }
    ],
    "recent_flows": [...],
    "talking_points": [
        "AUM is down 26% over the past 90 days — open the conversation by acknowledging market headwinds...",
        "Present Invesco's defensive equity and short-duration bond options...",
        "Ask about any client conversations they're having about moving assets...",
        "Offer to co-host a client webinar on navigating current market conditions..."
    ],
    "action_items": [
        {
            "type": "call",
            "description": "Schedule urgent retention call",
            "urgency": "Immediate"
        }
    ]
}
```

### 6.8 `POST /nl-query/`

Natural language → SQL query against the analytical database.

**Rate limited:** 10 requests/minute per IP.

**Request Body:**
```json
{
    "query": "Show me advisors with more than 20% AUM decline"
}
```

**Response `200`:**
```json
{
    "question": "Show me advisors with more than 20% AUM decline",
    "sql": "SELECT advisor_id, full_name, ... FROM advisors WHERE ...",
    "columns": ["advisor_id", "full_name", "firm_name", "aum_current", "aum_change_pct"],
    "rows": [
        {
            "advisor_id": "adv_0001",
            "full_name": "John Smith",
            "firm_name": "Smith & Associates",
            "aum_current": 8500000,
            "aum_change_pct": -26.1
        }
    ],
    "count": 47,
    "used_llm": true,
    "error": null
}
```

**Error Response `422`:**
```json
{
    "question": "...",
    "sql": "SELECT ...",
    "columns": [],
    "rows": [],
    "count": 0,
    "error": "Query error: column 'nonexistent' does not exist"
}
```

**NL→SQL Pipeline:**
1. **Quick Pattern Match** — Regex patterns for common questions (instant, no API call)
2. **Gemini Flash** — Falls back to Gemini 2.0 Flash for complex queries
3. **Kimi K2.5** — Falls back to Kimi if Gemini is unavailable
4. **Keyword Fallback** — Last resort pattern matching

**Analytical Database Schema (passed to LLM for SQL generation):**

| Table | Key Columns |
|---|---|
| `advisors` | `advisor_id` (PK, TEXT), `full_name`, `firm_name`, `channel`, `region`, `aum_current`, `aum_12m_ago`, `client_count`, `avg_account_size`, `email`, `phone`, `city`, `state` |
| `holdings` | `holding_id` (PK), `advisor_id` (FK), `symbol`, `fund_name`, `fund_type`, `fund_family`, `aum_in_fund`, `pct_of_aum`, `as_of_date` |
| `flows` | `flow_id` (PK), `advisor_id` (FK), `symbol`, `flow_month`, `net_flow`, `gross_inflow`, `gross_outflow` |
| `signals` | `signal_id` (PK), `advisor_id` (FK), `signal_type`, `signal_score`, `signal_data` (JSONB), `triggered_at`, `status`, `resolved_at` |

---

## 7. Data Models & Response Schemas

### 7.1 Advisor (Client) Object

```
ForwardLane_Advisor__c (Custom Object) or mapped to Contact/Account
├── ForwardLane_Advisor_ID__c     Text(50)     External ID (e.g. "adv_0001")
├── Full_Name__c                  Text(255)
├── Firm_Name__c                  Text(255)
├── Channel__c                    Picklist     (RIA, BD, Bank, Insurance, Wirehouse)
├── Region__c                     Text(100)
├── AUM_Current__c                Currency
├── AUM_12M_Ago__c                Currency
├── AUM_Change_Pct__c             Percent      (formula: (Current - 12M) / 12M)
├── Risk_Score__c                 Number(3,0)  (0-100, derived)
├── Opportunity_Score__c          Number(3,0)  (0-100, derived)
├── Status__c                     Picklist     (critical, declining, stable, growing)
├── Active_Signal_Count__c        Number       (rollup from Signal records)
├── Client_Count__c               Number
├── Avg_Account_Size__c           Currency
├── Last_Contact__c               DateTime
└── Assigned_Wholesaler__c        Lookup(User)
```

### 7.2 Signal Object

```
ForwardLane_Signal__c (Custom Object)
├── Signal_ID__c                  Text(50)     External ID
├── Advisor__c                    Lookup(ForwardLane_Advisor__c)
├── Signal_Type__c                Picklist     (see Signal Types table above)
├── Signal_Score__c               Number(3,1)  (0-10)
├── Category__c                   Picklist     (risk, opportunity)
├── Severity__c                   Picklist     (high, medium, low)
├── Status__c                     Picklist     (active, resolved, dismissed)
├── Triggered_At__c               DateTime
├── Resolved_At__c                DateTime
└── Signal_Data__c                LongTextArea (JSON)
```

---

## 8. Salesforce Configuration Requirements

### 8.1 Named Credential Setup

```
Label:              ForwardLane_API
Name:               ForwardLane_API
URL:                https://django-backend-production-3b94.up.railway.app
Identity Type:      Named Principal
Authentication:     Custom Header
  Header Name:      X-Demo-Token
  Header Value:     <HMAC token from DEMO_TOKEN env var>
Enabled:            ✓ Allow callouts
```

**For JWT auth (production):**
```
Identity Type:      Named Principal
Authentication:     JWT Bearer Token Flow
  Issuer:           salesforce-invesco-prod
  Subject:          api-service@forwardlane.com
  Audience:         https://django-backend-production-3b94.up.railway.app
  Token Endpoint:   https://django-backend-production-3b94.up.railway.app/api/v1/auth/token/
```

### 8.2 CSP Trusted Sites (for iframe approach)

Navigate to: **Setup → CSP Trusted Sites → New**

| Name | URL | Context |
|---|---|---|
| `ForwardLane_SignalStudio` | `https://signal-studio-production-a258.up.railway.app` | All |
| `ForwardLane_API` | `https://django-backend-production-3b94.up.railway.app` | Connect |

### 8.3 Remote Site Settings (for Apex callouts)

Navigate to: **Setup → Remote Site Settings → New**

| Name | URL |
|---|---|
| `ForwardLane_Backend` | `https://django-backend-production-3b94.up.railway.app` |

> **Note:** If using Named Credentials, Remote Site Settings are automatically bypassed.

### 8.4 Custom Settings / Custom Metadata

```
ForwardLane_Config__mdt (Custom Metadata Type)
├── API_Base_URL__c               Text     https://django-backend-production-3b94.up.railway.app
├── Easy_Button_Path__c           Text     /api/v1/easy-button
├── Studio_Frontend_URL__c        Text     https://signal-studio-production-a258.up.railway.app
├── NL_Query_Rate_Limit__c        Number   10
├── Meeting_Prep_Timeout_MS__c    Number   30000
└── Embed_Mode_Enabled__c         Checkbox
```

### 8.5 Permission Set

```
ForwardLane_Signal_Studio (Permission Set)
├── Custom Object: ForwardLane_Advisor__c    (Read, Edit)
├── Custom Object: ForwardLane_Signal__c     (Read, Edit, Create)
├── Apex Class: SignalStudioService           (Enabled)
├── Apex Class: MeetingPrepService            (Enabled)
├── Apex Class: NLQueryService                (Enabled)
├── Apex Class: SignalRunnerService            (Enabled)
└── External Credential: ForwardLane_API      (Enabled)
```

---

## 9. SLDS Design Patterns Already Implemented

The existing Next.js app was built using SLDS design patterns. These can be directly ported to native LWC using base Lightning components:

| Current Implementation | SLDS Pattern | LWC Base Component |
|---|---|---|
| `SLDSIcon` (custom SVG) | SLDS Icons | `<lightning-icon>` |
| `SLDSAvatar` | Avatar | `<lightning-avatar>` |
| `SLDSBadge` | Badge | `<lightning-badge>` |
| `SLDSCardHeader` | Card Header | `<lightning-card>` |
| `SLDSTimeline` | Timeline | `<lightning-timeline>` or custom |
| `SLDSCarousel` | Carousel | `<lightning-carousel>` |
| `SLDSProgressBar` | Progress Bar | `<lightning-progress-bar>` |
| `SLDSProgressRing` | Progress Ring | `<lightning-progress-ring>` |
| `SLDSPill` | Pill | `<lightning-pill>` |
| `SLDSAppLauncher` | App Launcher | Custom grid with `<lightning-tile>` |
| Accordion sections | Accordion | `<lightning-accordion>` |
| Data tables | Datatable | `<lightning-datatable>` |
| Tab navigation | Tabs | `<lightning-tabset>` |
| Toast notifications | Toast | `ShowToastEvent` |
| Modal drawers | Modal | `<lightning-modal>` (LWC Stacks) |

**Color tokens used (Salesforce brand):**
- `#032D60` — Salesforce Dark Blue (header backgrounds)
- `#0176D3` — Salesforce Blue (primary actions)
- `#00A1E0` — Salesforce Light Blue (accents)
- `#F3F3F3` — Background gray
- `#E5E5E5` — Border gray
- `#080707` — Text black
- `#706E6B` — Text muted

---

## 10. Authentication & Security

### Current Auth Model

The backend uses `EasyButtonPermission` (defined in `easy_button/views.py`):

1. **Demo/Staging mode** (`DEMO_ENV` set + `DEMO_TOKEN` present):
   - Requests must supply `X-Demo-Token` header
   - HMAC constant-time comparison via `hmac.compare_digest`
   - Used for demo environments and Salesforce sandbox testing

2. **Production mode** (no `DEMO_ENV`):
   - Standard Django REST Framework session/JWT authentication
   - JWT tokens passed via `Authorization: JWT <token>` header

### Recommended Salesforce Auth Flow

**For demo/POC:**
1. Store `DEMO_TOKEN` value in a Protected Custom Setting
2. Apex controller adds `X-Demo-Token` header to all callouts
3. Simple, immediate, no OAuth dance

**For production:**
1. Configure Named Credential with JWT Bearer Token Flow
2. Salesforce auto-generates and manages JWT tokens
3. Backend validates tokens using Salesforce's public key (JWKS)
4. Token includes `sub` (Salesforce User ID) for audit logging

### CSP / CORS Configuration

**Backend CORS** (already configured in Django settings):
```python
CORS_ALLOWED_ORIGINS = [
    "https://*.force.com",
    "https://*.salesforce.com",
    "https://*.lightning.force.com",
    "https://*.my.salesforce.com",
]
```

**Salesforce CSP** — Add `signal-studio-production-a258.up.railway.app` and `django-backend-production-3b94.up.railway.app` to CSP Trusted Sites (see Section 8.2).

---

## 11. Mobile Considerations

### Salesforce Mobile App Compatibility

The existing mobile layout (`/mobile` route) was designed for the Salesforce mobile app context. Key specs:

- **Viewport:** 428×926 (iPhone 14 Pro Max reference)
- **Tab bar height:** 72px (py-4, w-7 h-7 icons, 11px labels)
- **Bottom safe area:** 32px reserved for disclosure band
- **Content padding:** `pb-40` to account for fixed tab bar + disclosure
- **Touch targets:** Minimum 44×44px per Apple HIG

### LWC Mobile Targets

```xml
<targets>
    <target>lightning__RecordPage</target>
    <target>lightning__AppPage</target>
    <target>lightning__UtilityBar</target>
</targets>
```

All three targets work in the Salesforce Mobile App. For the best mobile experience:

1. **Record Page** — `meetingBriefCard` as a card on Contact/Account record
2. **App Page** — Full `territoryDashboard` as a Lightning App page
3. **Utility Bar** — Quick access `actionQueue` in the utility bar (always visible)

### Responsive Breakpoints

| Context | Width | Layout |
|---|---|---|
| Desktop (Lightning) | ≥1024px | Full dashboard with sidebar |
| Tablet (iPad) | 768-1023px | Condensed dashboard, stacked cards |
| Mobile (SF Mobile App) | <768px | Single column, accordion sections, bottom tabs |

---

## 12. Testing & QA Plan

### Unit Tests (Apex)

```apex
@IsTest
private class SignalStudioServiceTest {

    @IsTest
    static void testGetDashboardStats() {
        // Mock HTTP callout
        Test.setMock(HttpCalloutMock.class, new SignalStudioMock(200,
            '{"total_aum":156000000000,"advisor_count":500,"at_risk_count":47,'
            + '"opportunities_count":128,"aum_change_pct":-3.2}'
        ));

        Test.startTest();
        Map<String, Object> result = SignalStudioService.getDashboardStats();
        Test.stopTest();

        System.assertEquals(500, result.get('advisor_count'));
        System.assertEquals(47, result.get('at_risk_count'));
    }

    @IsTest
    static void testGetAdvisors() {
        Test.setMock(HttpCalloutMock.class, new SignalStudioMock(200,
            '{"count":1,"page":1,"page_size":20,"total_pages":1,"results":[' +
            '{"id":"adv_0001","name":"Test Advisor","firm":"Test Firm","segment":"RIA",' +
            '"aum":5000000,"change":-10.5,"risk":65,"opportunity":72,' +
            '"lastContact":null,"status":"declining","active_signals":2}]}'
        ));

        Test.startTest();
        Map<String, Object> result = SignalStudioService.getAdvisors(
            'RIA', '', 'aum', 'desc', 1, 20
        );
        Test.stopTest();

        System.assertEquals(1, result.get('count'));
    }

    // Mock class
    private class SignalStudioMock implements HttpCalloutMock {
        private Integer statusCode;
        private String body;

        SignalStudioMock(Integer statusCode, String body) {
            this.statusCode = statusCode;
            this.body = body;
        }

        public HTTPResponse respond(HTTPRequest req) {
            HttpResponse res = new HttpResponse();
            res.setStatusCode(this.statusCode);
            res.setBody(this.body);
            res.setHeader('Content-Type', 'application/json');
            return res;
        }
    }
}
```

### LWC Jest Tests

```javascript
// __tests__/meetingBriefCard.test.js
import { createElement } from 'lwc';
import MeetingBriefCard from 'c/meetingBriefCard';
import getMeetingPrep from '@salesforce/apex/MeetingPrepService.getMeetingPrep';

jest.mock('@salesforce/apex/MeetingPrepService.getMeetingPrep', () => ({
    default: jest.fn()
}), { virtual: true });

describe('meetingBriefCard', () => {
    afterEach(() => { while (document.body.firstChild) document.body.removeChild(document.body.firstChild); });

    it('renders loading spinner initially', () => {
        const el = createElement('c-meeting-brief-card', { is: MeetingBriefCard });
        document.body.appendChild(el);
        const spinner = el.shadowRoot.querySelector('lightning-spinner');
        expect(spinner).toBeTruthy();
    });
});
```

---

## 13. Deployment Checklist

### Phase 1: Iframe Embed (1-2 days)

- [ ] Create `signalStudioEmbed` LWC (wrapper iframe)
- [ ] Add `signal-studio-production-a258.up.railway.app` to CSP Trusted Sites
- [ ] Add `django-backend-production-3b94.up.railway.app` to CSP Trusted Sites
- [ ] Configure X-Frame-Options on Signal Studio to allow `*.force.com` and `*.salesforce.com`
- [ ] Deploy LWC to sandbox
- [ ] Add to Contact/Account record page via Lightning App Builder
- [ ] Test postMessage communication
- [ ] Test on Salesforce Mobile App

### Phase 2: Native LWC (2-4 weeks)

- [ ] Create Named Credential `ForwardLane_API`
- [ ] Create Remote Site Setting (if not using Named Credentials)
- [ ] Deploy Apex controllers (4 classes)
- [ ] Deploy Apex test classes
- [ ] Create Permission Set `ForwardLane_Signal_Studio`
- [ ] Create custom fields on Contact (`ForwardLane_Advisor_ID__c`)
- [ ] Port LWC components (6 components + 1 utils)
- [ ] Create Lightning App Page "Signal Studio"
- [ ] Add `meetingBriefCard` to Contact record page
- [ ] Add `actionQueue` to Utility Bar
- [ ] Add `territoryDashboard` to Lightning App
- [ ] Full testing pass (desktop + mobile)
- [ ] Security review
- [ ] Deploy to production

### Phase 3: Production Hardening

- [ ] Migrate from `X-Demo-Token` to JWT auth via Named Credentials
- [ ] Implement Salesforce→ForwardLane user mapping
- [ ] Add error monitoring / logging
- [ ] Configure CORS on Django backend for production Salesforce domain
- [ ] Set up automated tests in CI
- [ ] Document admin configuration guide

---

## 14. Appendix: File Inventory

### Backend (Django — ForwardLane)

| File | Description |
|---|---|
| `easy_button/views.py` | All 8 API view classes (~1260 lines) |
| `easy_button/urls.py` | URL routing for Easy Button endpoints |
| `easy_button/tests/test_permissions.py` | Permission/auth test suite |

### Frontend (Next.js — Signal Studio)

| File | Description | Maps to LWC |
|---|---|---|
| `app/page.tsx` | App launcher grid | `signalStudioLauncher` |
| `app/dashboard/page.tsx` | Territory dashboard | `territoryDashboard` |
| `app/salesforce/page.tsx` | Meeting brief (contact record) | `meetingBriefCard` |
| `app/mobile/page.tsx` | Mobile meeting prep | `mobileBrief` |
| `app/create/page.tsx` | Signal creation / NL query | `nlQueryPanel` |
| `app/easy-button/page.tsx` | Combined Easy Button view | All components |
| `app/easy-button/salesforce-embed.tsx` | postMessage bridge | Built into embed LWC |
| `components/slds-icons.tsx` | Custom SLDS icon SVGs (156 lines) | `<lightning-icon>` |
| `components/slds-patterns.tsx` | SLDS patterns: timeline, carousel, etc. (456 lines) | Base Lightning components |
| `lib/mock-data.ts` | Synthetic demo data | Apex callouts to real API |
| `lib/data/combined-data.ts` | Combined synthetic datasets | N/A (backend provides) |

### Demo Site (GitHub Pages)

| URL | Purpose |
|---|---|
| `https://trendpilotai.github.io/invesco-demo/` | Interactive demo (app launcher) |
| `https://trendpilotai.github.io/invesco-demo/dashboard` | Territory dashboard demo |
| `https://trendpilotai.github.io/invesco-demo/salesforce` | Meeting brief demo |
| `https://trendpilotai.github.io/invesco-demo/mobile` | Mobile brief demo |
| `https://trendpilotai.github.io/invesco-demo/create` | Signal creator demo |

---

*This spec was generated from the live codebase at `/data/workspace/repos/signal-studio-backend/easy_button/` and `/data/workspace/projects/invesco-retention/demo-app/`. All API response schemas are derived from actual view code, not mocks.*
