'use client'

import { useState, useMemo, Suspense } from 'react'
import { useRouter } from 'next/navigation'
import { advisors, territoryMetrics, topSignals, severityDot, type Advisor } from '@/lib/mock-data'
import { usePersona } from '@/lib/use-persona'
import { SLDSAvatar } from '@/components/slds-icons'
import { LiveSignalFeed } from '@/components/LiveSignalFeed'

function MetricCard({
  label,
  value,
  sub,
  color = '#0176d3',
  trend,
}: {
  label: string
  value: string
  sub?: string
  color?: string
  trend?: 'up' | 'down' | 'neutral'
}) {
  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e5e5e5',
        borderRadius: 10,
        padding: '16px 18px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
      }}
    >
      <div style={{ fontSize: 11, color: '#706e6b', fontWeight: 500, marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
        {label}
      </div>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 6 }}>
        <div style={{ fontSize: 24, fontWeight: 700, color, lineHeight: 1 }}>{value}</div>
        {trend && (
          <div style={{ fontSize: 11, color: trend === 'up' ? '#2e844a' : trend === 'down' ? '#ea001e' : '#706e6b', marginBottom: 2 }}>
            {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'}
          </div>
        )}
      </div>
      {sub && <div style={{ fontSize: 11, color: '#706e6b', marginTop: 4 }}>{sub}</div>}
    </div>
  )
}

function SignalBadge({ severity }: { severity: 'urgent' | 'attention' | 'positive' | 'info' }) {
  const configs = {
    urgent: { color: '#ea001e', bg: '#fef1ee', label: 'URGENT' },
    attention: { color: '#8c4600', bg: '#fef4e8', label: 'ACTION' },
    positive: { color: '#2e844a', bg: '#ebf7e6', label: 'GOOD' },
    info: { color: '#0176d3', bg: '#eef4ff', label: 'INFO' },
  }
  const cfg = configs[severity]
  return (
    <span
      style={{
        fontSize: 9,
        fontWeight: 700,
        color: cfg.color,
        background: cfg.bg,
        padding: '2px 6px',
        borderRadius: 100,
        letterSpacing: '0.05em',
      }}
    >
      {cfg.label}
    </span>
  )
}

function AdvisorRow({ advisor, onSelect }: { advisor: Advisor; onSelect: (id: string) => void }) {
  const urgentSignals = advisor.signals.filter(s => s.severity === 'urgent').length
  const attentionSignals = advisor.signals.filter(s => s.severity === 'attention').length
  const topSignal = advisor.signals.find(s => s.severity === 'urgent') || advisor.signals.find(s => s.severity === 'attention') || advisor.signals[0]

  const statusColor = advisor.engagementScore >= 80 ? '#2e844a' : advisor.engagementScore >= 50 ? '#0176d3' : advisor.engagementScore >= 25 ? '#fe9339' : '#ea001e'

  return (
    <div
      onClick={() => onSelect(advisor.id)}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        padding: '13px 18px',
        borderBottom: '1px solid #f3f3f3',
        cursor: 'pointer',
        transition: 'background 0.12s',
      }}
      onMouseEnter={e => (e.currentTarget.style.background = '#f8faff')}
      onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
    >
      {/* Avatar */}
      <SLDSAvatar name={advisor.name} size={36} color={advisor.engagementScore >= 50 ? '#0176d3' : '#ea001e'} />

      {/* Name + firm */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ fontSize: 13, fontWeight: 700, color: '#080707' }}>{advisor.name}</span>
          {(urgentSignals > 0 || attentionSignals > 0) && (
            <span
              style={{
                fontSize: 9,
                fontWeight: 700,
                color: urgentSignals > 0 ? '#ea001e' : '#8c4600',
                background: urgentSignals > 0 ? '#fef1ee' : '#fef4e8',
                padding: '1px 5px',
                borderRadius: 100,
              }}
            >
              {urgentSignals > 0 ? `${urgentSignals} URGENT` : `${attentionSignals} ACTION`}
            </span>
          )}
        </div>
        <div style={{ fontSize: 11, color: '#706e6b', marginTop: 1 }}>
          {advisor.firm} · {advisor.city}, {advisor.state}
        </div>
        {topSignal && (
          <div style={{ fontSize: 11, color: '#514f4d', marginTop: 3, display: 'flex', alignItems: 'center', gap: 4 }}>
            <div style={{ width: 5, height: 5, borderRadius: '50%', background: topSignal.severity === 'urgent' ? '#ea001e' : topSignal.severity === 'attention' ? '#fe9339' : '#0176d3', flexShrink: 0 }} />
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {topSignal.text}
            </span>
          </div>
        )}
      </div>

      {/* AUM */}
      <div style={{ textAlign: 'right', flexShrink: 0 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: '#080707' }}>
          ${advisor.aum >= 1000 ? `${(advisor.aum / 1000).toFixed(1)}B` : `${advisor.aum}M`}
        </div>
        <div style={{ fontSize: 11, color: '#706e6b' }}>AUM</div>
      </div>

      {/* Engagement */}
      <div style={{ textAlign: 'center', flexShrink: 0, minWidth: 52 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: statusColor }}>{advisor.engagementScore}</div>
        <div style={{ fontSize: 10, color: '#706e6b' }}>ENG</div>
        <div style={{ width: '100%', height: 3, background: '#f3f3f3', borderRadius: 2, marginTop: 3 }}>
          <div style={{ width: `${advisor.engagementScore}%`, height: '100%', background: statusColor, borderRadius: 2 }} />
        </div>
      </div>

      {/* Chevron */}
      <div style={{ color: '#c9c7c5', fontSize: 16, flexShrink: 0 }}>›</div>
    </div>
  )
}

function DashboardContent() {
  const router = useRouter()
  const { persona, appendDemo } = usePersona()
  const [filter, setFilter] = useState<'all' | 'urgent' | 'attention' | 'active'>('all')
  const [showSignalFeed, setShowSignalFeed] = useState(true)

  const isPersona = persona.key !== 'default'

  const filteredAdvisors = useMemo(() => {
    let list = [...advisors]

    if (isPersona) {
      list = list.filter(persona.advisorFilter)
      list.sort(persona.advisorSort)
    }

    if (filter === 'urgent') {
      list = list.filter(a => a.signals.some(s => s.severity === 'urgent'))
    } else if (filter === 'attention') {
      list = list.filter(a => a.signals.some(s => s.severity === 'urgent' || s.severity === 'attention'))
    } else if (filter === 'active') {
      list = list.filter(a => a.lastContactDaysAgo <= 30)
    }

    return list
  }, [filter, persona, isPersona])

  const totalAUM = filteredAdvisors.reduce((s, a) => s + a.aum, 0)
  const avgEng = Math.round(filteredAdvisors.reduce((s, a) => s + a.engagementScore, 0) / (filteredAdvisors.length || 1))
  const urgentCount = filteredAdvisors.filter(a => a.signals.some(s => s.severity === 'urgent')).length

  return (
    <div style={{ minHeight: '100vh', background: '#f3f3f3' }}>
      {/* Header */}
      <div
        style={{
          background: isPersona
            ? `linear-gradient(135deg, #032D60, ${persona.accentColor})`
            : '#032D60',
        }}
      >
        <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 20px' }}>
          {/* Nav */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '12px 0', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <button
              onClick={() => router.push(appendDemo('/'))}
              style={{ background: 'none', border: 'none', color: 'rgba(255,255,255,0.7)', cursor: 'pointer', fontSize: 12, display: 'flex', alignItems: 'center', gap: 4 }}
            >
              ← Home
            </button>
            <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: 12 }}>/</span>
            <span style={{ color: '#fff', fontSize: 12, fontWeight: 600 }}>Territory Dashboard</span>
          </div>

          {/* Title row */}
          <div style={{ padding: '20px 0 24px', display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16, flexWrap: 'wrap' }}>
            <div>
              {isPersona && (
                <p style={{ color: '#93c5fd', fontSize: 12, fontWeight: 500, margin: '0 0 4px' }}>
                  {persona.greeting} 👋 · {persona.focus}
                </p>
              )}
              <h1 style={{ color: '#fff', fontSize: 20, fontWeight: 700, margin: 0, letterSpacing: '-0.02em' }}>
                {isPersona ? persona.dashboardSubtitle : 'Territory Dashboard'}
              </h1>
              <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 12, margin: '4px 0 0' }}>
                {isPersona ? persona.liveBanner : `${filteredAdvisors.length} advisors · $${totalAUM}M AUM · ${urgentCount} urgent signals`}
              </p>
            </div>

            {/* Live indicator */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                padding: '6px 12px',
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 100,
                cursor: 'pointer',
              }}
              onClick={() => setShowSignalFeed(v => !v)}
            >
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: '#4ade80',
                  animation: 'pulse 2s infinite',
                }}
              />
              <span style={{ color: '#fff', fontSize: 12, fontWeight: 600 }}>
                {showSignalFeed ? 'Live Feed Active' : 'Show Live Feed'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '20px' }}>
        {/* Metrics row */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 12, marginBottom: 20 }}>
          <MetricCard
            label="Total AUM"
            value={`$${totalAUM >= 1000 ? `${(totalAUM / 1000).toFixed(1)}B` : `${totalAUM}M`}`}
            sub={`${filteredAdvisors.length} advisors`}
            color="#032d60"
            trend="up"
          />
          <MetricCard
            label="Avg Engagement"
            value={`${avgEng}/100`}
            sub="Territory score"
            color={avgEng >= 70 ? '#2e844a' : avgEng >= 50 ? '#fe9339' : '#ea001e'}
          />
          <MetricCard
            label="Urgent Signals"
            value={`${urgentCount}`}
            sub="Require action"
            color={urgentCount > 2 ? '#ea001e' : '#fe9339'}
            trend={urgentCount > 2 ? 'down' : 'neutral'}
          />
          <MetricCard
            label="Net Flows"
            value={`${territoryMetrics.totalNetFlows >= 0 ? '+' : ''}${territoryMetrics.totalNetFlows}M`}
            sub="Last 90 days"
            color={territoryMetrics.totalNetFlows >= 0 ? '#2e844a' : '#ea001e'}
            trend={territoryMetrics.totalNetFlows >= 0 ? 'up' : 'down'}
          />
        </div>

        {/* Two-column layout: advisor list + live feed */}
        <div style={{ display: 'grid', gridTemplateColumns: showSignalFeed ? '1fr 360px' : '1fr', gap: 16, alignItems: 'start' }}>
          {/* Advisor list */}
          <div
            style={{
              background: '#fff',
              border: '1px solid #e5e5e5',
              borderRadius: 12,
              overflow: 'hidden',
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
            }}
          >
            {/* List header */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '14px 18px',
                borderBottom: '1px solid #e5e5e5',
                background: '#fafbfc',
                flexWrap: 'wrap',
                gap: 10,
              }}
            >
              <div>
                <div style={{ fontSize: 13, fontWeight: 700, color: '#080707' }}>Advisor Book</div>
                <div style={{ fontSize: 11, color: '#706e6b', marginTop: 1 }}>
                  {filteredAdvisors.length} advisors
                </div>
              </div>

              {/* Filters */}
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {[
                  { key: 'all', label: 'All' },
                  { key: 'urgent', label: '🔴 Urgent' },
                  { key: 'attention', label: '🟡 Action' },
                  { key: 'active', label: '🟢 Active' },
                ].map(f => (
                  <button
                    key={f.key}
                    onClick={() => setFilter(f.key as typeof filter)}
                    style={{
                      padding: '4px 10px',
                      borderRadius: 100,
                      border: '1px solid',
                      borderColor: filter === f.key ? '#0176d3' : '#e5e5e5',
                      background: filter === f.key ? '#eef4ff' : '#fff',
                      color: filter === f.key ? '#0176d3' : '#706e6b',
                      fontSize: 11,
                      fontWeight: 600,
                      cursor: 'pointer',
                    }}
                  >
                    {f.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Advisor rows */}
            {filteredAdvisors.length === 0 ? (
              <div style={{ padding: '40px 20px', textAlign: 'center', color: '#706e6b', fontSize: 13 }}>
                No advisors match this filter.
              </div>
            ) : (
              filteredAdvisors.map(advisor => (
                <AdvisorRow
                  key={advisor.id}
                  advisor={advisor}
                  onSelect={id => router.push(appendDemo(`/salesforce?advisor=${id}`))}
                />
              ))
            )}
          </div>

          {/* Live signal feed */}
          {showSignalFeed && (
            <div style={{ position: 'sticky', top: 16 }}>
              <LiveSignalFeed />

              {/* Top signals summary */}
              <div
                style={{
                  marginTop: 12,
                  background: '#fff',
                  border: '1px solid #e5e5e5',
                  borderRadius: 12,
                  overflow: 'hidden',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
                }}
              >
                <div
                  style={{
                    padding: '12px 16px',
                    borderBottom: '1px solid #e5e5e5',
                    background: '#fafbfc',
                    fontSize: 12,
                    fontWeight: 700,
                    color: '#080707',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                  }}
                >
                  🎯 Top Priority Signals
                </div>
                {topSignals.slice(0, 4).map((sig, i) => (
                  <div
                    key={i}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 10,
                      padding: '10px 16px',
                      borderBottom: i < 3 ? '1px solid #f3f3f3' : 'none',
                    }}
                  >
                    <div
                      style={{
                        width: 6,
                        height: 6,
                        borderRadius: '50%',
                        background: sig.severity === 'urgent' ? '#ea001e' : sig.severity === 'attention' ? '#fe9339' : '#0176d3',
                        marginTop: 4,
                        flexShrink: 0,
                      }}
                    />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: 11, fontWeight: 700, color: '#080707' }}>{sig.advisorName}</div>
                      <div style={{ fontSize: 11, color: '#706e6b', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {sig.signal}
                      </div>
                    </div>
                    <div style={{ fontSize: 10, color: '#706e6b', flexShrink: 0 }}>${sig.aum}M</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}


export default function DashboardPage() {
  return (
    <Suspense fallback={<div style={{ minHeight: '100vh', background: '#f3f3f3' }} />}>
      <DashboardContent />
    </Suspense>
  )
}
