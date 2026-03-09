'use client';

import { useState, useEffect, useCallback, ReactNode, Suspense, useMemo } from 'react';
import { useSearchParams } from 'next/navigation';
import { advisors, getAdvisor } from '@/lib/mock-data';
import { usePersona } from '@/lib/use-persona';
import { capture, DEMO_EVENTS } from '@/lib/posthog';
import { Separator } from '@/components/ui/separator';
import Link from 'next/link';
import { SLDSIcon, SLDSAvatar, SLDSCardHeader, SLDSBadge } from '@/components/slds-icons';
import {
  SLDSTimeline,
  SLDSCarousel,
  SLDSProgressBar,
  SLDSProgressRing,
  SLDSPill,
} from '@/components/slds-patterns';

// ─── SF Lightning Global Navigation ─────────────────────────────────────────
function SFGlobalNav({ advisorName, advisors: adv, selectedId, onSelect, homeHref = '/' }: {
  advisorName: string;
  advisors: { id: string; name: string }[];
  selectedId: string;
  onSelect: (id: string) => void;
  homeHref?: string;
}) {
  return (
    <div className="flex-shrink-0">
      {/* Global Header */}
      <div className="bg-[#032D60] h-12 flex items-center px-3 gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        {/* App Launcher / Waffle */}
        <button className="w-9 h-9 flex items-center justify-center rounded hover:bg-white/10 transition-colors flex-shrink-0" title="App Launcher">
          <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
            <rect x="2" y="2" width="4" height="4" rx="0.5" opacity="0.9"/><rect x="10" y="2" width="4" height="4" rx="0.5" opacity="0.9"/>
            <rect x="18" y="2" width="4" height="4" rx="0.5" opacity="0.9"/><rect x="2" y="10" width="4" height="4" rx="0.5" opacity="0.9"/>
            <rect x="10" y="10" width="4" height="4" rx="0.5" opacity="0.9"/><rect x="18" y="10" width="4" height="4" rx="0.5" opacity="0.9"/>
            <rect x="2" y="18" width="4" height="4" rx="0.5" opacity="0.9"/><rect x="10" y="18" width="4" height="4" rx="0.5" opacity="0.9"/>
            <rect x="18" y="18" width="4" height="4" rx="0.5" opacity="0.9"/>
          </svg>
        </button>

        {/* Salesforce Cloud Logo */}
        <div className="flex items-center gap-1.5 mr-1">
          <svg className="w-7 h-7" viewBox="0 0 100 70" fill="white">
            <path d="M41 15c2-10 11-16 20-14 4-8 12-13 21-13 13 0 23 9 25 21 7 1 13 7 13 15 0 9-7 16-16 16H18C10 40 4 34 4 27c0-7 6-13 13-13 2 0 4 0 5 1z" opacity="0.95"/>
          </svg>
          <div>
            <span className="text-white font-bold text-sm tracking-tight leading-none block">ForwardLane</span>
            <span className="text-blue-300 text-[10px] leading-none">Sales Cloud</span>
          </div>
        </div>

        {/* Global Search */}
        <div className="hidden md:flex flex-1 max-w-sm mx-3">
          <div className="flex items-center w-full bg-white/10 rounded-md border border-white/20 px-3 py-1.5 gap-2">
            <svg className="w-3.5 h-3.5 text-blue-200 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <span className="text-blue-200 text-xs">Search Salesforce…</span>
          </div>
        </div>

        <div className="ml-auto flex items-center gap-1">
          {/* Advisor Selector */}
          <select
            value={selectedId}
            onChange={e => onSelect(e.target.value)}
            className="bg-[#0176D3] hover:bg-[#014486] text-white text-xs px-2 py-1 rounded border border-blue-400 cursor-pointer transition-colors"
          >
            {adv.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
          </select>

          {/* Utility Icons */}
          <button className="w-8 h-8 flex items-center justify-center rounded hover:bg-white/10 transition-colors" title="Notifications">
            <svg className="w-4.5 h-4.5 text-blue-200" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6V11c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
            </svg>
          </button>
          <button className="w-8 h-8 flex items-center justify-center rounded hover:bg-white/10 transition-colors" title="Help">
            <svg className="w-4.5 h-4.5 text-blue-200" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z"/>
            </svg>
          </button>
          <button className="w-8 h-8 flex items-center justify-center rounded-full bg-[#0176D3] hover:bg-[#014486] text-white text-xs font-bold transition-colors ml-1" title="User: Jordan Mitchell">
            JM
          </button>
        </div>
      </div>

      {/* App Navigation Bar */}
      <div className="bg-[#0176D3] h-10 flex items-center px-4 gap-6 text-sm" style={{ borderBottom: '1px solid rgba(0,0,0,0.15)' }}>
        <Link href={homeHref} className="text-blue-100 hover:text-white text-xs transition-colors whitespace-nowrap">
          ← Home
        </Link>
        <div className="hidden md:flex gap-5 text-blue-100">
          <button className="text-white border-b-2 border-white pb-0.5 text-xs font-semibold">Contacts</button>
          <button className="hover:text-white text-xs transition-colors">Accounts</button>
          <button className="hover:text-white text-xs transition-colors">Opportunities</button>
          <button className="hover:text-white text-xs transition-colors">Reports</button>
          <button className="hover:text-white text-xs transition-colors">Dashboards</button>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <span className="text-blue-200 text-xs hidden sm:inline">Invesco Distribution Intelligence</span>
          <div className="agentforce-badge hidden sm:flex">
            <svg className="w-2 h-2" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            Agentforce
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── SF Breadcrumb ────────────────────────────────────────────────────────────
function SFBreadcrumb({ advisorName, homeHref = '/' }: { advisorName: string; homeHref?: string }) {
  return (
    <nav className="flex items-center gap-1.5 px-4 py-2 bg-white border-b border-[#E5E5E5] text-xs text-[#706E6B]">
      <Link href={homeHref} className="hover:text-[#0176D3] transition-colors flex items-center gap-1">
        <SLDSIcon name="home" className="w-3 h-3" />
        <span>Home</span>
      </Link>
      <span className="text-[#C9C7C5]">›</span>
      <button className="hover:text-[#0176D3] transition-colors">Accounts</button>
      <span className="text-[#C9C7C5]">›</span>
      <button className="hover:text-[#0176D3] transition-colors">Invesco</button>
      <span className="text-[#C9C7C5]">›</span>
      <button className="hover:text-[#0176D3] transition-colors">Contacts</button>
      <span className="text-[#C9C7C5]">›</span>
      <span className="text-[#080707] font-semibold truncate max-w-48">{advisorName}</span>
    </nav>
  );
}

// ─── SF Left Sidebar ──────────────────────────────────────────────────────────
function SFLeftSidebar() {
  const navItems = [
    {
      label: 'Home',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
        </svg>
      ),
    },
    {
      label: 'Chatter',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
        </svg>
      ),
    },
    {
      label: 'Accounts',
      active: true,
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z"/>
        </svg>
      ),
    },
    {
      label: 'Contacts',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
      ),
    },
    {
      label: 'Opportunities',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
        </svg>
      ),
    },
    {
      label: 'Reports',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </svg>
      ),
    },
    {
      label: 'Dashboards',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
        </svg>
      ),
    },
    {
      label: 'Tasks',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14l-4-4 1.41-1.41L14 14.17l6.59-6.59L22 9l-8 8z"/>
        </svg>
      ),
    },
    {
      label: 'Signals',
      icon: (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M1 9l2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.08 2.93 1 9zm8 8l3 3 3-3c-1.65-1.66-4.34-1.66-6 0zm-4-4l2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13z"/>
        </svg>
      ),
    },
  ];

  return (
    <div className="w-14 bg-[#16325C] flex flex-col items-center py-3 gap-1 flex-shrink-0 min-h-0 overflow-y-auto" style={{ boxShadow: '2px 0 4px rgba(0,0,0,0.15)' }}>
      {navItems.map(item => (
        <button
          key={item.label}
          title={item.label}
          className={`w-10 h-10 flex flex-col items-center justify-center rounded-md gap-0.5 transition-colors group relative ${
            item.active
              ? 'bg-white/20 text-white'
              : 'text-blue-300 hover:bg-white/10 hover:text-white'
          }`}
        >
          {item.icon}
          <span className="text-[8px] leading-none font-medium truncate w-full text-center px-0.5">{item.label}</span>
        </button>
      ))}
    </div>
  );
}

// ─── SF Record Header (Highlight Panel) ──────────────────────────────────────
function SFRecordHeader({
  advisor,
  onPrepMeeting,
  onPushToSF,
  pushState,
}: {
  advisor: ReturnType<typeof getAdvisor>;
  onPrepMeeting: () => void;
  onPushToSF: () => void;
  pushState: 'idle' | 'loading' | 'success';
}) {
  if (!advisor) return null;
  return (
    <div className="bg-white border-b border-[#E5E5E5]" style={{ boxShadow: '0 2px 4px rgba(0,0,0,0.06)' }}>
      {/* Record type indicator */}
      <div className="px-6 pt-3 pb-1 flex items-center gap-2">
        <span className="text-[10px] font-bold text-[#706E6B] uppercase tracking-wider">Contact</span>
        <span className="text-[#C9C7C5]">·</span>
        <span className="text-[10px] text-[#0176D3] font-medium">Financial Advisor</span>
      </div>

      {/* Main record header */}
      <div className="px-6 pb-3 flex flex-col md:flex-row md:items-start gap-4">
        {/* Avatar + Name */}
        <div className="flex items-center gap-3 flex-1 min-w-0">
          <SLDSAvatar name={advisor.name} size={52} objectType="contact" />
          <div className="min-w-0">
            <h1 className="text-xl font-bold text-[#080707] leading-tight truncate">{advisor.name}</h1>
            <p className="text-sm text-[#514F4D] mt-0.5">{advisor.title}</p>
            <div className="flex flex-wrap items-center gap-2 mt-1.5">
              <SLDSPill label={advisor.firm} color="blue" />
              <SLDSPill label={advisor.channel} color="default" />
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-bold text-white bg-[#2E844A]">
                ${advisor.aum}M AUM
              </span>
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-bold ${advisor.aumGrowthRate >= 0 ? 'bg-[#EBF7E6] text-[#2E844A]' : 'bg-[#FEF1EE] text-[#EA001E]'}`}>
                {advisor.aumGrowthRate >= 0 ? '▲' : '▼'} {Math.abs(advisor.aumGrowthRate)}% YoY
              </span>
            </div>
          </div>
        </div>

        {/* Highlight Fields (inline quick stats) */}
        <div className="hidden lg:grid grid-cols-4 gap-x-6 gap-y-1 text-xs flex-shrink-0">
          {[
            { label: 'Phone', value: advisor.phone },
            { label: 'Region', value: `${advisor.city}, ${advisor.state}` },
            { label: 'Last Contact', value: advisor.lastContact },
            { label: 'Opp. Score', value: `${advisor.opportunityScore}/100` },
          ].map(f => (
            <div key={f.label}>
              <span className="text-[10px] font-medium text-[#706E6B] uppercase tracking-wide block">{f.label}</span>
              <span className="font-semibold text-[#080707]">{f.value}</span>
            </div>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 flex-shrink-0 flex-wrap">
          <button
            onClick={onPrepMeeting}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold bg-[#0176D3] hover:bg-[#014486] text-white transition-colors"
          >
            <SLDSIcon name="event" className="w-3.5 h-3.5" />
            Meeting Brief
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold border border-[#C9C7C5] bg-white hover:bg-[#F3F3F3] text-[#514F4D] transition-colors">
            <SLDSIcon name="email" className="w-3.5 h-3.5" />
            Email
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold border border-[#C9C7C5] bg-white hover:bg-[#F3F3F3] text-[#514F4D] transition-colors">
            <SLDSIcon name="phone" className="w-3.5 h-3.5" />
            Call
          </button>
          {pushState === 'success' ? (
            <button disabled className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold bg-[#EBF7E6] border border-[#2E844A]/40 text-[#2E844A] cursor-default">
              <SLDSIcon name="check" className="w-3.5 h-3.5" />
              Logged
            </button>
          ) : (
            <button
              onClick={onPushToSF}
              disabled={pushState === 'loading'}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold border border-[#C9C7C5] bg-white hover:bg-[#F3F3F3] text-[#514F4D] transition-colors disabled:opacity-60"
            >
              {pushState === 'loading' ? (
                <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/></svg>
              ) : (
                <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><circle cx="8" cy="8" r="2.5" opacity="0.8"/><circle cx="15.5" cy="7.5" r="3"/><circle cx="6.5" cy="15" r="2.5" opacity="0.75"/><circle cx="13.5" cy="14.5" r="3"/><circle cx="19" cy="15" r="2" opacity="0.85"/></svg>
              )}
              {pushState === 'loading' ? 'Logging…' : 'Log to SF'}
            </button>
          )}
          <button className="w-8 h-8 flex items-center justify-center rounded border border-[#C9C7C5] bg-white hover:bg-[#F3F3F3] text-[#514F4D] transition-colors" title="More actions">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>
          </button>
        </div>
      </div>

      {/* Tab navigation */}
      <div className="flex px-6 gap-0 border-t border-[#E5E5E5] overflow-x-auto">
        {['Details', 'Related', 'Activity', 'Signal Studio', 'News'].map((tab, i) => (
          <button
            key={tab}
            className={`px-4 py-2 text-xs font-semibold whitespace-nowrap border-b-2 transition-colors ${
              i === 0
                ? 'border-[#0176D3] text-[#0176D3]'
                : 'border-transparent text-[#706E6B] hover:text-[#080707] hover:border-[#C9C7C5]'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
    </div>
  );
}

// ─── Accordion Section ───────────────────────────────────────────────────────
function AccordionSection({
  title,
  icon,
  iconBg = '#0176D3',
  badge,
  defaultOpen = false,
  summary,
  children,
}: {
  title: string;
  icon: string;
  iconBg?: string;
  badge?: ReactNode;
  defaultOpen?: boolean;
  summary?: string;
  children: ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="border-b border-[#E5E5E5]">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-[#F8FAFF] transition-colors"
      >
        <div
          className="w-8 h-8 rounded flex items-center justify-center text-white flex-shrink-0"
          style={{ backgroundColor: iconBg }}
        >
          <SLDSIcon name={icon} className="w-4 h-4" />
        </div>
        <div className="flex-1 text-left min-w-0">
          <span className="text-[13px] font-bold text-[#080707]">{title}</span>
          {!open && summary && (
            <p className="text-[11px] text-[#706E6B] truncate mt-0.5">{summary}</p>
          )}
        </div>
        {badge && <div className="flex-shrink-0">{badge}</div>}
        <SLDSIcon
          name="chevrondown"
          className={`w-4 h-4 text-[#706E6B] transition-transform duration-200 flex-shrink-0 ${open ? 'rotate-180' : ''}`}
        />
      </button>
      <div className={`overflow-hidden transition-all duration-300 ease-in-out ${open ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="px-4 pb-3">
          {children}
        </div>
      </div>
    </div>
  );
}

// ─── Types ───────────────────────────────────────────────────────────────────
type PushState = 'idle' | 'loading' | 'success';
interface Toast { id: number; title: string; lines: string[] }

// ─── Helpers ─────────────────────────────────────────────────────────────────
function randomSFId() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  return '00T' + Array.from({ length: 15 }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}
function tomorrowLabel() {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// Map signal severity → carousel card colors/icons
const severityToCard = {
  urgent:      { color: '#EA001E', icon: 'warning',       label: 'URGENT'      },
  attention:   { color: '#FE9339', icon: 'notification',  label: 'ATTENTION'   },
  info:        { color: '#0176D3', icon: 'graph',         label: 'INFO'        },
  opportunity: { color: '#2E844A', icon: 'target',        label: 'OPPORTUNITY' },
} as const;

// ─── Toast ────────────────────────────────────────────────────────────────────
function ToastContainer({ toasts, onDismiss }: { toasts: Toast[]; onDismiss: (id: number) => void }) {
  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 w-80 sm:w-96 pointer-events-none">
      {toasts.map(t => (
        <div key={t.id} className="pointer-events-auto bg-white border border-[#2E844A]/30 rounded-lg shadow-lg p-4 flex gap-3">
          <div className="w-8 h-8 rounded-full bg-[#EBF7E6] flex items-center justify-center text-[#2E844A] flex-shrink-0">
            <SLDSIcon name="check" className="w-4 h-4" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-[#080707]">{t.title}</p>
            {t.lines.map((l, i) => <p key={i} className="text-xs text-[#514F4D] mt-0.5 break-words">{l}</p>)}
          </div>
          <button onClick={() => onDismiss(t.id)} className="text-[#706E6B] hover:text-[#514F4D] text-lg leading-none flex-shrink-0">×</button>
        </div>
      ))}
    </div>
  );
}

// ─── SF Side Rail (right-column detail panel) ────────────────────────────────
function SFSideRail({ advisor }: { advisor: NonNullable<ReturnType<typeof getAdvisor>> }) {
  const fields = [
    { label: 'Account Name',       value: advisor.firm },
    { label: 'Channel',            value: advisor.channel },
    { label: 'Region',             value: `${advisor.region}` },
    { label: 'Office Location',    value: `${advisor.city}, ${advisor.state}` },
    { label: 'Certifications',     value: advisor.certifications.join(', ') },
    { label: 'Practice Focus',     value: advisor.practiceFocus.join(', ') },
    { label: 'AUM',                value: `$${advisor.aum}M` },
    { label: 'AUM Growth (YoY)',   value: `${advisor.aumGrowthRate >= 0 ? '+' : ''}${advisor.aumGrowthRate}%` },
    { label: 'Net Flows',          value: `${advisor.netFlows >= 0 ? '+' : ''}$${advisor.netFlows}M` },
    { label: 'Client Count',       value: `${advisor.clientCount} clients` },
    { label: 'Avg Client AUM',     value: `$${(advisor.avgClientAum / 1_000_000).toFixed(1)}M` },
    { label: 'Revenue (Annual)',   value: `$${(advisor.revenueAnnual / 1_000_000).toFixed(1)}M` },
    { label: 'Invesco Wallet %',   value: `${advisor.invescoRevenuePct}%` },
    { label: 'Relationship Mgr',   value: advisor.relationshipManager },
    { label: 'Last Contact',       value: advisor.lastContact },
    { label: 'Phone',              value: advisor.phone },
    { label: 'Email',              value: advisor.email },
    { label: 'Office Address',     value: advisor.officeAddress },
  ];

  return (
    <div className="bg-white rounded-lg border border-[#E5E5E5] overflow-hidden" style={{ boxShadow: '0 2px 4px rgba(0,0,0,0.06)' }}>
      {/* Panel header */}
      <div className="px-4 py-3 border-b border-[#E5E5E5] flex items-center justify-between bg-[#F3F3F3]">
        <span className="text-[11px] font-bold text-[#706E6B] uppercase tracking-wider">Contact Details</span>
        <button className="text-[#0176D3] text-xs hover:underline">Edit</button>
      </div>

      {/* Fields */}
      <div className="divide-y divide-[#F3F3F3]">
        {fields.map(f => (
          <div key={f.label} className="px-4 py-2.5">
            <span className="text-[10px] font-medium text-[#706E6B] uppercase tracking-wide block mb-0.5">{f.label}</span>
            <span className="text-[13px] text-[#080707] font-medium leading-snug">{f.value || '—'}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────
function SalesforcePageInner() {
  const searchParams = useSearchParams();
  const { persona, appendDemo } = usePersona();
  const personaAdvisors = useMemo(() =>
    persona.advisorFilter ? advisors.filter(persona.advisorFilter) : advisors,
  [persona]);
  const initialId = searchParams.get('id') || (personaAdvisors[0]?.id ?? 'sarah-chen');
  const [selectedId, setSelectedId] = useState(initialId);
  const [loading, setLoading] = useState(true);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [toastCounter, setToastCounter] = useState(0);
  const [pushState, setPushState] = useState<PushState>('idle');
  const advisor = getAdvisor(selectedId) || advisors[0];

  useEffect(() => {
    setLoading(true);
    setPushState('idle');
    const t = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(t);
  }, [selectedId]);

  const dismissToast = useCallback((id: number) => setToasts(prev => prev.filter(t => t.id !== id)), []);

  const showSuccessToast = useCallback((advisorName: string, sfId: string) => {
    const id = toastCounter + 1;
    setToastCounter(id);
    const toast: Toast = {
      id, title: 'Task created in Salesforce',
      lines: [
        `✅ Follow-up assigned for ${advisorName}`,
        `Due: ${tomorrowLabel()}, 9:00 AM | SF Task: ${sfId}`,
      ],
    };
    setToasts(prev => [...prev, toast]);
    setTimeout(() => dismissToast(id), 6000);
  }, [toastCounter, dismissToast]);

  const handlePushToSF = useCallback(() => {
    if (pushState !== 'idle' || !advisor) return;
    capture(DEMO_EVENTS.PUSH_TO_SALESFORCE, { advisor_name: advisor.name, advisor_id: advisor.id });
    setPushState('loading');
    setTimeout(() => {
      setPushState('success');
      showSuccessToast(advisor.name, randomSFId());
    }, 1500);
  }, [pushState, advisor, showSuccessToast]);

  // Scroll Meeting Brief panel into view
  const scrollToMeetingBrief = useCallback(() => {
    document.getElementById('meeting-brief-panel')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, []);

  // Transform advisor signals → SLDSCarousel InsightCard format
  const insightCards = advisor.signals.map((s: { id: string; severity: string; text: string; detail?: string }) => {
    const meta = severityToCard[s.severity as keyof typeof severityToCard] ?? { color: '#706E6B', icon: 'notification', label: 'SIGNAL' };
    return {
      id: s.id,
      title: meta.label,
      metric: s.text.length > 60 ? s.text.slice(0, 57) + '…' : s.text,
      description: s.detail ?? s.text,
      color: meta.color,
      icon: meta.icon,
      action: 'View detail',
    };
  });

  // Transform advisor activities → SLDSTimeline format
  const timelineItems = advisor.activities.map((a: { type: string; description: string; date: string }, i: number) => ({
    id: `activity-${i}`,
    type: (['call', 'meeting', 'email', 'task', 'event', 'note'].includes(a.type) ? a.type : 'note') as 'call' | 'meeting' | 'email' | 'task' | 'event' | 'note',
    title: a.type.charAt(0).toUpperCase() + a.type.slice(1),
    description: a.description,
    date: a.date,
  }));

  return (
    <div className="min-h-screen bg-[#F3F3F3] flex flex-col">
      <ToastContainer toasts={toasts} onDismiss={dismissToast} />

      {/* ── SF Global Navigation Chrome ────────────────────── */}
      <SFGlobalNav
        advisorName={advisor.name}
        advisors={personaAdvisors}
        selectedId={selectedId}
        onSelect={setSelectedId}
        homeHref={appendDemo('/')}
      />

      {/* ── Body: Left Sidebar + Main Content ─────────────── */}
      <div className="flex flex-1 min-h-0">

      {/* ── SF Left Sidebar ───────────────────────────────── */}
      <SFLeftSidebar />

      {/* ── Right: Breadcrumb + Record ────────────────────── */}
      <div className="flex flex-col flex-1 min-w-0">

      {/* ── Breadcrumb ────────────────────────────────────── */}
      <SFBreadcrumb advisorName={advisor.name} homeHref={appendDemo('/')} />

      {/* ── Record Header / Highlight Panel ───────────────── */}
      <SFRecordHeader
        advisor={advisor}
        onPrepMeeting={scrollToMeetingBrief}
        onPushToSF={handlePushToSF}
        pushState={pushState}
      />

      {/* Loading shimmer */}
      {loading && (
        <div className="flex-1 p-4 md:p-6">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Main content shimmer */}
            <div className="flex-1 space-y-4">
              <div className="bg-white rounded-lg border border-[#E5E5E5] p-6">
                <div className="flex items-start gap-4 mb-4">
                  <div className="w-14 h-14 rounded-full sf-shimmer" />
                  <div className="flex-1 space-y-2">
                    <div className="h-5 sf-shimmer rounded w-48" />
                    <div className="h-3 sf-shimmer rounded w-64" />
                    <div className="h-3 sf-shimmer rounded w-40" />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  {[...Array(8)].map((_, i) => (
                    <div key={i} className="space-y-1">
                      <div className="h-2 sf-shimmer rounded w-20" />
                      <div className="h-4 sf-shimmer rounded w-32" />
                    </div>
                  ))}
                </div>
              </div>
            </div>
            {/* Side rail shimmer */}
            <div className="lg:w-[340px] space-y-4">
              <div className="bg-white rounded-lg border border-[#E5E5E5] p-4 space-y-3">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="space-y-1">
                    <div className="h-2 sf-shimmer rounded w-20" />
                    <div className="h-3 sf-shimmer rounded w-32" />
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs text-[#0176D3] mt-4">
            <div className="w-4 h-4 border-2 border-[#0176D3] border-t-transparent rounded-full animate-spin" />
            <span className="font-medium">Signal Studio AI analyzing advisor data…</span>
          </div>
        </div>
      )}

      {/* ── Main Content (3-column SF record layout) ──────── */}
      {!loading && (
        <div className="flex-1 p-4 md:p-6">
          <div className="flex flex-col lg:flex-row gap-4 items-start">

            {/* ── Column 1: Salesforce Contact Record Detail ── */}
            <div className="flex-1 min-w-0 space-y-4">
              <div className="bg-white rounded-lg border border-[#E5E5E5] overflow-hidden" style={{ boxShadow: '0 2px 4px rgba(0,0,0,0.06)' }}>

                {/* Contact header within card */}
                <div className="p-5 border-b border-[#E5E5E5]">
                  <div className="flex items-start gap-4">
                    <SLDSAvatar name={advisor.name} size={56} objectType="contact" />
                    <div className="flex-1 min-w-0">
                      <h2 className="text-xl font-bold text-[#080707]">{advisor.name}</h2>
                      <p className="text-sm text-[#514F4D]">{advisor.title} — {advisor.firm}</p>
                      <div className="flex flex-wrap gap-3 mt-1.5">
                        <span className="flex items-center gap-1 text-xs text-[#706E6B]">
                          <SLDSIcon name="email" className="w-3 h-3" />{advisor.email}
                        </span>
                        <span className="flex items-center gap-1 text-xs text-[#706E6B]">
                          <SLDSIcon name="phone" className="w-3 h-3" />{advisor.phone}
                        </span>
                      </div>
                      <p className="text-xs text-[#706E6B] flex items-center gap-1 mt-1">
                        <SLDSIcon name="location" className="w-3 h-3" />{advisor.officeAddress}
                      </p>
                      {/* Tag pills */}
                      <div className="flex flex-wrap gap-1.5 mt-2.5">
                        <SLDSPill label={advisor.channel} color="blue" icon="people" />
                        <SLDSPill label={advisor.region} color="default" icon="location" />
                        {advisor.certifications.map((c: string) => (
                          <SLDSPill key={c} label={c} color="purple" />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* SF Field Grid */}
                <div className="p-5 border-b border-[#E5E5E5]">
                  <div className="grid grid-cols-2 gap-x-6 gap-y-4 text-sm">
                    {[
                      { label: 'Channel',          value: advisor.channel },
                      { label: 'AUM',              value: `$${advisor.aum}M` },
                      { label: 'Region',           value: `${advisor.region} — ${advisor.city}, ${advisor.state}` },
                      { label: 'Relationship Mgr', value: advisor.relationshipManager },
                      { label: 'Clients',          value: `${advisor.clientCount} (avg $${(advisor.avgClientAum / 1_000_000).toFixed(1)}M)` },
                      { label: 'Practice Focus',   value: advisor.practiceFocus.join(', ') },
                      { label: 'Revenue (Annual)', value: `$${(advisor.revenueAnnual / 1_000_000).toFixed(1)}M (${advisor.invescoRevenuePct}% Invesco)` },
                      { label: 'AUM Growth YoY',   value: `${advisor.aumGrowthRate > 0 ? '+' : ''}${advisor.aumGrowthRate}%` },
                    ].map(f => (
                      <div key={f.label}>
                        <span className="text-[11px] font-medium text-[#706E6B] uppercase tracking-wide block mb-0.5">{f.label}</span>
                        <span className="font-medium text-[#080707]">{f.value}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Holdings */}
                <div className="border-b border-[#E5E5E5]">
                  <SLDSCardHeader title="Holdings" icon="money" iconBg="#3BA755" />
                  <div className="overflow-x-auto px-4 py-3">
                    <table className="w-full text-xs">
                      <thead>
                        <tr className="border-b border-[#E5E5E5] text-left">
                          {['Fund', 'Ticker', 'Provider', 'AUM', 'Alloc%', 'Δ QoQ'].map(h => (
                            <th key={h} className={`pb-2 pr-3 text-[11px] font-medium text-[#706E6B] uppercase tracking-wide ${['AUM','Alloc%','Δ QoQ'].includes(h) ? 'text-right' : ''}`}>{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {advisor.allHoldings.map((h: { fund_name: string; ticker: string; provider: string; aum: number; allocation_pct: number; change_vs_prior_quarter_pct: string }, i: number) => (
                          <tr key={i} className={`border-b border-[#E5E5E5] hover:bg-[#EEF4FF] transition-colors ${h.provider === 'Invesco' ? 'bg-[#EEF4FF]/40' : ''}`}>
                            <td className="py-2 pr-3 font-medium text-[#080707]">{h.fund_name}</td>
                            <td className="py-2 pr-3 text-[#706E6B]">{h.ticker}</td>
                            <td className="py-2 pr-3">
                              <SLDSBadge variant={h.provider === 'Invesco' ? 'default' : 'lightest'}>{h.provider}</SLDSBadge>
                            </td>
                            <td className="py-2 pr-3 text-right text-[#514F4D]">${(h.aum / 1_000_000).toFixed(1)}M</td>
                            <td className="py-2 pr-3 text-right text-[#514F4D]">{h.allocation_pct}%</td>
                            <td className={`py-2 text-right font-medium ${h.change_vs_prior_quarter_pct.startsWith('+') ? 'text-[#2E844A]' : h.change_vs_prior_quarter_pct.startsWith('-') ? 'text-[#EA001E]' : 'text-[#514F4D]'}`}>
                              {h.change_vs_prior_quarter_pct}%
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Activity Timeline */}
                <div>
                  <SLDSCardHeader title="Recent Activity" icon="clock" iconBg="#9602C7" />
                  <div className="p-4">
                    <SLDSTimeline items={timelineItems} />
                  </div>
                </div>
              </div>
            </div>

            {/* ── Column 2: Signal Studio Meeting Brief ──────── */}
            <div className="w-full lg:w-[440px] flex-shrink-0 space-y-4" id="meeting-brief-panel">

              {/* Meeting Brief card */}
              <div>
                {/* Panel header — white with SLDS blue left border */}
                <div className="bg-white border border-[#E5E5E5] border-l-4 border-l-[#0176D3] rounded-t-lg px-4 py-3">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded bg-[#0176D3] flex items-center justify-center text-white flex-shrink-0">
                      <SLDSIcon name="lightning_extension" className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-bold text-sm text-[#080707]">Signal Studio — Meeting Brief</h3>
                      <p className="text-[#706E6B] text-xs">AI-powered intelligence for {advisor.name}</p>
                    </div>
                    <div className="agentforce-badge">
                      <svg className="w-2 h-2" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                      Agentforce
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-b-lg border border-[#E5E5E5] border-t-0" style={{ boxShadow: '0 2px 4px rgba(0,0,0,0.06)' }}>

                  {/* Meeting info bar */}
                  <div className="px-4 py-3 border-b border-[#E5E5E5] bg-[#EEF4FF]">
                    <p className="font-semibold text-[#080707] text-sm">
                      {advisor.name}{advisor.meetingDate ? ` — ${advisor.meetingDate} ${advisor.meetingTime}` : ''}
                    </p>
                    <p className="text-xs text-[#514F4D] mt-0.5">
                      {advisor.firm} | {advisor.channel} | ${advisor.aum}M AUM | {advisor.city}, {advisor.state}
                    </p>
                  </div>

                  {/* Opportunity Score */}
                  <div className="border-b border-[#E5E5E5] px-4 py-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <SLDSProgressRing
                          value={advisor.opportunityScore}
                          size={56}
                          color={advisor.opportunityScore >= 70 ? '#2E844A' : advisor.opportunityScore >= 40 ? '#FE9339' : '#EA001E'}
                        />
                        <div>
                          <span className="text-[11px] font-bold text-[#706E6B] uppercase tracking-wider">Opportunity Score</span>
                          <p className="text-[12px] text-[#514F4D]">
                            {advisor.opportunityScore >= 70 ? 'High — strong upsell potential' : advisor.opportunityScore >= 40 ? 'Medium — nurture relationship' : 'Low — retention risk, act now'}
                          </p>
                        </div>
                      </div>
                      <SLDSBadge variant={advisor.opportunityScore >= 70 ? 'success' : advisor.opportunityScore >= 40 ? 'warning' : 'error'}>
                        {advisor.opportunityScore >= 70 ? 'HIGH' : advisor.opportunityScore >= 40 ? 'MEDIUM' : 'LOW'}
                      </SLDSBadge>
                    </div>
                  </div>

                  {/* ── Accordion Sections ──────────────── */}

                  {/* 1. Meeting Prep & Talking Points — DEFAULT OPEN */}
                  <AccordionSection
                    title="Meeting Prep & Talking Points"
                    icon="note"
                    iconBg="#706E6B"
                    badge={<SLDSBadge variant="default">⚡ AI</SLDSBadge>}
                    defaultOpen={true}
                    summary={advisor.meetingPrepBrief.split(/[.!]\s+/)[0]?.slice(0, 60) + '...'}
                  >
                    <ul className="space-y-2 mb-4">
                      {advisor.meetingPrepBrief
                        .split(/[.!]\s+/)
                        .filter((s: string) => s.trim().length > 10)
                        .slice(0, 5)
                        .map((point: string, i: number) => (
                          <li key={i} className="flex items-start gap-2 text-[12px] text-[#514F4D] leading-relaxed">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#0176D3] mt-1.5 flex-shrink-0" />
                            {point.trim().replace(/\.$/, '')}
                          </li>
                        ))}
                    </ul>
                    <Separator className="my-3" />
                    <p className="text-[11px] font-bold text-[#706E6B] uppercase tracking-wider mb-2">Talking Points</p>
                    <div className="space-y-2">
                      {advisor.talkingPoints.map((tp: { id: string; text: string }, i: number) => (
                        <div key={tp.id} className="flex gap-2.5 text-xs">
                          <div className="w-5 h-5 rounded-full bg-[#0176D3] flex items-center justify-center text-white text-[10px] font-bold flex-shrink-0 mt-0.5">{i + 1}</div>
                          <span className="text-[#514F4D] leading-relaxed">{tp.text}</span>
                        </div>
                      ))}
                    </div>
                  </AccordionSection>

                  {/* 2. Key Signals — DEFAULT OPEN */}
                  <AccordionSection
                    title="Key Signals"
                    icon="graph"
                    iconBg="#0176D3"
                    defaultOpen={true}
                    summary={`${advisor.signals.length} signals detected`}
                  >
                    <SLDSCarousel cards={insightCards} />
                    {/* Risk Drift inline if present */}
                    {advisor.riskDriftAlert.status !== 'CLEAR' && (
                      <div className={`mt-3 p-3 rounded-lg border text-xs ${
                        advisor.riskDriftAlert.severity === 'high'
                          ? 'bg-[#FEF1EE] border-[#EA001E]/30 text-[#EA001E]'
                          : advisor.riskDriftAlert.severity === 'medium'
                          ? 'bg-[#FEF4E8] border-[#FE9339]/30 text-[#C75000]'
                          : 'bg-[#EEF4FF] border-[#0176D3]/30 text-[#0176D3]'
                      }`}>
                        <div className="font-bold mb-1 flex items-center gap-2">
                          <SLDSBadge variant={advisor.riskDriftAlert.severity === 'high' ? 'error' : 'warning'}>
                            {advisor.riskDriftAlert.status}
                          </SLDSBadge>
                          <span className="capitalize">{advisor.riskDriftAlert.severity} risk drift</span>
                        </div>
                        <p className="leading-relaxed">{advisor.riskDriftAlert.detail}</p>
                      </div>
                    )}
                  </AccordionSection>

                  {/* 3. Next Best Action + Competitive Displacement — collapsed */}
                  <AccordionSection
                    title="Next Best Action"
                    icon="lightning_extension"
                    iconBg="#032D60"
                    summary={advisor.nextBestAction.slice(0, 60) + '...'}
                  >
                    <p className="text-xs text-[#514F4D] leading-relaxed bg-[#EEF4FF] border border-[#0176D3]/20 rounded-lg p-3">
                      {advisor.nextBestAction}
                    </p>
                    <Separator className="my-3" />
                    <div className="flex items-center gap-4">
                      <SLDSProgressRing
                        value={advisor.competitiveDisplacementScore}
                        size={64}
                        color={advisor.competitiveDisplacementScore >= 70 ? '#2E844A' : advisor.competitiveDisplacementScore >= 40 ? '#FE9339' : '#EA001E'}
                        label="displacement"
                      />
                      <p className="text-xs text-[#514F4D] leading-relaxed flex-1">{advisor.competitiveDisplacementDetail}</p>
                    </div>
                  </AccordionSection>

                  {/* 4. Engagement & Relationship — collapsed */}
                  <AccordionSection
                    title="Engagement & Relationship"
                    icon="chart"
                    iconBg="#7F8DE1"
                    summary={`Engagement: ${advisor.engagementScore}/100 · ${advisor.invescoRevenuePct}% Invesco wallet`}
                  >
                    <div className="space-y-2.5 mb-4">
                      {[
                        { label: 'CRM Activity',       value: advisor.engagementBreakdown.crm_activity },
                        { label: 'Digital Engagement', value: advisor.engagementBreakdown.digital_engagement },
                        { label: 'Event Attendance',   value: advisor.engagementBreakdown.event_attendance },
                        { label: 'Content Consumption',value: advisor.engagementBreakdown.content_consumption },
                        { label: 'Email Responsive',   value: advisor.engagementBreakdown.email_responsiveness },
                      ].map(item => (
                        <SLDSProgressBar key={item.label} label={item.label} value={item.value}
                          color={item.value >= 70 ? '#2E844A' : item.value >= 40 ? '#FE9339' : '#EA001E'} />
                      ))}
                    </div>
                    <Separator className="my-3" />
                    <div className="space-y-2 text-xs">
                      {[
                        { label: 'Last contact',          value: advisor.lastContact, colorClass: '' },
                        { label: 'AUM Growth YoY',        value: `${advisor.aumGrowthRate > 0 ? '+' : ''}${advisor.aumGrowthRate}%`, colorClass: advisor.aumGrowthRate >= 0 ? 'text-[#2E844A]' : 'text-[#EA001E]' },
                        { label: 'Net Flows',             value: `${advisor.netFlows >= 0 ? '+' : ''}$${advisor.netFlows}M`, colorClass: advisor.netFlows >= 0 ? 'text-[#2E844A]' : 'text-[#EA001E]' },
                        { label: 'Invesco Wallet Share',  value: `${advisor.invescoRevenuePct}%`, colorClass: '' },
                      ].map(r => (
                        <div key={r.label} className="flex justify-between items-center py-1 border-b border-[#F3F3F3] last:border-0">
                          <span className="text-[#706E6B]">{r.label}</span>
                          <span className={`font-semibold text-[#080707] ${r.colorClass}`}>{r.value}</span>
                        </div>
                      ))}
                    </div>
                  </AccordionSection>

                  {/* 5. Materials — collapsed */}
                  <AccordionSection
                    title="Materials"
                    icon="list"
                    iconBg="#56AAB6"
                    summary={`${advisor.materials.length} items available`}
                  >
                    <div className="space-y-1">
                      {advisor.materials.map((mat: { id: string; type: string; title: string }) => (
                        <button key={mat.id} className="w-full flex items-center gap-2 text-xs text-[#0176D3] hover:bg-[#EEF4FF] rounded-lg px-2 py-2 transition-colors text-left group">
                          <SLDSIcon name={mat.type === 'pitch-book' ? 'note' : mat.type === 'index' ? 'graph' : 'list'} className="w-3.5 h-3.5 flex-shrink-0" />
                          <span className="font-medium flex-1">{mat.title}</span>
                          <SLDSIcon name="chevronright" className="w-3 h-3 text-[#C9C7C5] group-hover:text-[#0176D3] transition-colors" />
                        </button>
                      ))}
                    </div>
                  </AccordionSection>

                  {/* Action Buttons */}
                  <div className="px-4 py-3 bg-[#F3F3F3] rounded-b-lg flex flex-wrap gap-2">
                    <button
                      onClick={scrollToMeetingBrief}
                      className="flex-1 flex items-center justify-center gap-1.5 rounded-md px-3 py-2 text-xs font-medium bg-[#0176D3] hover:bg-[#014486] text-white transition-colors"
                    >
                      <SLDSIcon name="event" className="w-3.5 h-3.5" />
                      Prep Meeting
                    </button>
                    <button className="flex-1 flex items-center justify-center gap-1.5 rounded-md px-3 py-2 text-xs font-medium border border-[#C9C7C5] text-[#514F4D] hover:bg-[#F3F3F3] bg-white transition-colors">
                      <SLDSIcon name="email" className="w-3.5 h-3.5" />
                      Email Template
                    </button>
                    {pushState === 'success' ? (
                      <button disabled className="flex-1 flex items-center justify-center gap-1.5 rounded-md px-3 py-2 text-xs font-medium bg-[#EBF7E6] border border-[#2E844A]/50 text-[#2E844A] cursor-default">
                        <SLDSIcon name="check" className="w-3.5 h-3.5" />
                        Task created in Salesforce
                      </button>
                    ) : (
                      <button
                        onClick={handlePushToSF}
                        disabled={pushState === 'loading'}
                        className="flex-1 flex items-center justify-center gap-1.5 rounded-md px-3 py-2 text-xs font-medium bg-[#0176D3] hover:bg-[#014486] text-white transition-colors disabled:opacity-60"
                      >
                        {pushState === 'loading' ? (
                          <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/></svg>
                        ) : (
                          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><circle cx="8" cy="9" r="2.5" opacity="0.85"/><circle cx="15.5" cy="8" r="3"/><circle cx="6.5" cy="15" r="2.5" opacity="0.8"/><circle cx="13" cy="14.5" r="3"/><circle cx="18.5" cy="15" r="2" opacity="0.85"/></svg>
                        )}
                        {pushState === 'loading' ? 'Creating task...' : 'Push to Salesforce'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* ── Column 3: SF Side Rail (record fields) ─────── */}
            <div className="w-full lg:w-[220px] flex-shrink-0">
              <SFSideRail advisor={advisor} />
            </div>

          </div>
        </div>
      )}
      </div>{/* end right column */}
      </div>{/* end body flex */}
    </div>
  );
}

export default function SalesforcePage() {
  return <Suspense><SalesforcePageInner /></Suspense>;
}
