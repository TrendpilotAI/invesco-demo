'use client'

import { useState, useEffect, useCallback } from 'react'

interface LiveSignal {
  id: string
  type: 'aum_decline' | 'cross_sell' | 'competitor' | 'engagement_drop' | 'opportunity' | 'meeting_signal' | 'flow_alert'
  severity: 'urgent' | 'attention' | 'positive' | 'info'
  advisorName: string
  firm: string
  aum: number
  description: string
  timestamp: Date
  badge: string
}

const SIGNAL_POOL: Omit<LiveSignal, 'id' | 'timestamp'>[] = [
  {
    type: 'aum_decline',
    severity: 'urgent',
    advisorName: 'Robert Kim',
    firm: 'JP Morgan Private Bank',
    aum: 520,
    description: '$3.5M net outflow — 90-day silence. Contract renewal due Q2.',
    badge: 'AUM DECLINE',
  },
  {
    type: 'competitor',
    severity: 'urgent',
    advisorName: 'James Patel',
    firm: 'Wells Fargo Advisors',
    aum: 390,
    description: 'Fidelity displacement detected. $8M Discovery Fund test — Q1 performance critical.',
    badge: 'COMPETITOR',
  },
  {
    type: 'cross_sell',
    severity: 'positive',
    advisorName: 'Amanda Foster',
    firm: 'Mosaic Financial Partners',
    aum: 340,
    description: '$20M tax-managed model opportunity. Wallet share 49.5% — highest in territory.',
    badge: 'CROSS-SELL',
  },
  {
    type: 'engagement_drop',
    severity: 'attention',
    advisorName: 'David Okafor',
    firm: 'Morgan Stanley',
    aum: 620,
    description: 'CIO dinner opened door — private credit $10M+ in 7-day window. Act now.',
    badge: 'ENGAGEMENT',
  },
  {
    type: 'opportunity',
    severity: 'positive',
    advisorName: 'Marcus Thompson',
    firm: 'Merrill Lynch',
    aum: 280,
    description: 'BetaCo 401k displacement closes March 15. $15M Vanguard Target Date replacement.',
    badge: 'OPPORTUNITY',
  },
  {
    type: 'meeting_signal',
    severity: 'info',
    advisorName: 'Lisa Martinez',
    firm: 'Martinez Retirement Solutions',
    aum: 210,
    description: 'RMD webinar prep: 200+ advisor attendees. Digital engagement score 100/100.',
    badge: 'MEETING PREP',
  },
  {
    type: 'cross_sell',
    severity: 'info',
    advisorName: 'Jennifer Walsh',
    firm: 'Walsh Sustainable Advisors',
    aum: 180,
    description: '$8M BAB green bond allocation in review. ESG consolidation from Parnassus & Calvert.',
    badge: 'CROSS-SELL',
  },
  {
    type: 'competitor',
    severity: 'attention',
    advisorName: 'Dr. Sarah Chen',
    firm: 'Pinnacle Wealth Advisors',
    aum: 450,
    description: 'Risk-off shift captured $28M. $8M ABRZX risk parity pipeline — close this quarter.',
    badge: 'COMPETITOR',
  },
  {
    type: 'flow_alert',
    severity: 'positive',
    advisorName: 'Catherine Brooks',
    firm: 'Brooks Wealth Management',
    aum: 150,
    description: 'New relationship growing fast +22% YoY. First Invesco allocation $5-10M ready.',
    badge: 'FLOW ALERT',
  },
  {
    type: 'engagement_drop',
    severity: 'attention',
    advisorName: 'Michael Torres',
    firm: 'UBS Financial Services',
    aum: 480,
    description: '$85M Goldman displacement opportunity. Multi-generational wealth transfer strategy ready.',
    badge: 'ENGAGEMENT',
  },
  {
    type: 'aum_decline',
    severity: 'urgent',
    advisorName: 'Robert Kim',
    firm: 'JP Morgan Private Bank',
    aum: 520,
    description: 'ESCALATION NEEDED: 90+ days no contact. BlackRock/PIMCO evaluation in progress.',
    badge: 'AUM DECLINE',
  },
  {
    type: 'opportunity',
    severity: 'positive',
    advisorName: 'Amanda Foster',
    firm: 'Mosaic Financial Partners',
    aum: 340,
    description: 'Envestnet model portfolio AUM grew +18.2% YoY. Expand to direct indexing pilot.',
    badge: 'OPPORTUNITY',
  },
  {
    type: 'meeting_signal',
    severity: 'info',
    advisorName: 'Marcus Thompson',
    firm: 'Merrill Lynch',
    aum: 280,
    description: 'GammaTech plan sponsor meeting — Invesco specialist support could close $12M.',
    badge: 'MEETING PREP',
  },
  {
    type: 'flow_alert',
    severity: 'attention',
    advisorName: 'David Okafor',
    firm: 'Morgan Stanley',
    aum: 620,
    description: 'BlackRock Private Credit received $8M while Invesco PC ignored. Window closing.',
    badge: 'FLOW ALERT',
  },
  {
    type: 'cross_sell',
    severity: 'positive',
    advisorName: 'Lisa Martinez',
    firm: 'Martinez Retirement Solutions',
    aum: 210,
    description: 'Fidelity Freedom outflow $5M → Invesco retirement model. Systematic migration underway.',
    badge: 'CROSS-SELL',
  },
]

const severityConfig = {
  urgent: {
    color: '#ea001e',
    bg: '#fef1ee',
    border: '#fca5a5',
    dot: '#ea001e',
    label: 'URGENT',
  },
  attention: {
    color: '#8c4600',
    bg: '#fef4e8',
    border: '#fcd34d',
    dot: '#fe9339',
    label: 'ACTION',
  },
  positive: {
    color: '#2e844a',
    bg: '#ebf7e6',
    border: '#86efac',
    dot: '#2e844a',
    label: 'OPPORTUNITY',
  },
  info: {
    color: '#0176d3',
    bg: '#eef4ff',
    border: '#bfdbfe',
    dot: '#0176d3',
    label: 'INTEL',
  },
}

const typeIcons: Record<LiveSignal['type'], string> = {
  aum_decline: '📉',
  cross_sell: '🔀',
  competitor: '⚡',
  engagement_drop: '📊',
  opportunity: '🎯',
  meeting_signal: '📅',
  flow_alert: '💰',
}

function formatAUM(aum: number): string {
  if (aum >= 1000) return `$${(aum / 1000).toFixed(1)}B`
  return `$${aum}M`
}

function timeAgo(date: Date): string {
  const secs = Math.floor((Date.now() - date.getTime()) / 1000)
  if (secs < 5) return 'just now'
  if (secs < 60) return `${secs}s ago`
  if (secs < 3600) return `${Math.floor(secs / 60)}m ago`
  return `${Math.floor(secs / 3600)}h ago`
}

export function LiveSignalFeed() {
  const [signals, setSignals] = useState<LiveSignal[]>([])
  const [isLive, setIsLive] = useState(true)
  const [usedIndices, setUsedIndices] = useState<Set<number>>(new Set())
  const [tick, setTick] = useState(0)

  const addSignal = useCallback(() => {
    // Pick a random signal we haven't used recently
    const available = SIGNAL_POOL.map((_, i) => i).filter(i => !usedIndices.has(i))
    const pool = available.length > 0 ? available : SIGNAL_POOL.map((_, i) => i)
    const idx = pool[Math.floor(Math.random() * pool.length)]

    const template = SIGNAL_POOL[idx]
    const newSignal: LiveSignal = {
      ...template,
      id: `signal-${Date.now()}-${Math.random()}`,
      timestamp: new Date(),
    }

    setUsedIndices(prev => {
      const next = new Set(prev)
      next.add(idx)
      if (next.size > 8) {
        const iter = next.values()
        const firstVal = iter.next().value
        if (firstVal !== undefined) next.delete(firstVal)
      }
      return next
    })

    setSignals(prev => {
      const next = [newSignal, ...prev].slice(0, 6) // Keep last 6
      return next
    })
  }, [usedIndices])

  // Start with 2 initial signals
  useEffect(() => {
    const t0 = setTimeout(() => addSignal(), 500)
    const t1 = setTimeout(() => addSignal(), 1500)
    return () => { clearTimeout(t0); clearTimeout(t1) }
  }, []) // eslint-disable-line

  // Timer-driven: add new signal every 8-12 seconds
  useEffect(() => {
    if (!isLive) return
    const delay = 8000 + Math.random() * 4000 // 8-12 seconds
    const timer = setTimeout(() => {
      addSignal()
    }, delay)
    return () => clearTimeout(timer)
  }, [signals, isLive, addSignal])

  // Tick for timestamp display
  useEffect(() => {
    const interval = setInterval(() => setTick(t => t + 1), 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e5e5e5',
        borderRadius: 12,
        overflow: 'hidden',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '12px 16px',
          borderBottom: '1px solid #e5e5e5',
          background: '#fafbfc',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div
            style={{
              width: 28,
              height: 28,
              borderRadius: 6,
              background: '#032d60',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 14,
            }}
          >
            📡
          </div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 700, color: '#080707' }}>Live Signal Feed</div>
            <div style={{ fontSize: 11, color: '#706e6b' }}>Real-time advisor intelligence</div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {/* Live badge */}
          {isLive ? (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 5,
                padding: '3px 9px',
                background: '#fef1ee',
                border: '1px solid #fca5a5',
                borderRadius: 100,
                cursor: 'pointer',
              }}
              onClick={() => setIsLive(false)}
            >
              <div
                className="animate-live-pulse"
                style={{
                  width: 7,
                  height: 7,
                  borderRadius: '50%',
                  background: '#ea001e',
                }}
              />
              <span style={{ fontSize: 11, fontWeight: 700, color: '#ea001e', letterSpacing: '0.05em' }}>
                LIVE
              </span>
            </div>
          ) : (
            <button
              onClick={() => setIsLive(true)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 5,
                padding: '3px 9px',
                background: '#f3f3f3',
                border: '1px solid #c9c7c5',
                borderRadius: 100,
                cursor: 'pointer',
                fontSize: 11,
                fontWeight: 600,
                color: '#706e6b',
              }}
            >
              <div style={{ width: 7, height: 7, borderRadius: '50%', background: '#706e6b' }} />
              PAUSED
            </button>
          )}

          <div
            style={{
              fontSize: 11,
              color: '#706e6b',
              padding: '3px 8px',
              background: '#f3f3f3',
              borderRadius: 100,
            }}
          >
            {signals.length} signals
          </div>
        </div>
      </div>

      {/* Signal list */}
      <div style={{ minHeight: 200 }}>
        {signals.length === 0 ? (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '40px 20px',
              gap: 8,
            }}
          >
            <div style={{ fontSize: 24 }}>📡</div>
            <div style={{ fontSize: 13, color: '#706e6b' }}>Connecting to live feed...</div>
            <div
              className="animate-pulse"
              style={{
                width: 120,
                height: 4,
                background: '#e5e5e5',
                borderRadius: 4,
                marginTop: 4,
              }}
            />
          </div>
        ) : (
          signals.map((signal, index) => {
            const config = severityConfig[signal.severity]
            const isNew = index === 0

            return (
              <div
                key={signal.id}
                className={isNew ? 'animate-slide-in-from-top' : ''}
                style={{
                  display: 'flex',
                  gap: 12,
                  padding: '12px 16px',
                  borderBottom: index < signals.length - 1 ? '1px solid #f3f3f3' : 'none',
                  borderLeft: `3px solid ${config.dot}`,
                  background: isNew ? `${config.bg}66` : '#fff',
                  transition: 'background 1s ease',
                  animation: isNew ? 'slideInFromTop 0.35s ease-out' : undefined,
                }}
              >
                {/* Type icon */}
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: 8,
                    background: config.bg,
                    border: `1px solid ${config.border}`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 14,
                    flexShrink: 0,
                    marginTop: 1,
                  }}
                >
                  {typeIcons[signal.type]}
                </div>

                {/* Content */}
                <div style={{ flex: 1, minWidth: 0 }}>
                  {/* Header row */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 3, flexWrap: 'wrap' }}>
                    {/* Badge */}
                    <span
                      style={{
                        fontSize: 9,
                        fontWeight: 700,
                        color: config.color,
                        background: config.bg,
                        border: `1px solid ${config.border}`,
                        padding: '1px 6px',
                        borderRadius: 100,
                        letterSpacing: '0.06em',
                        flexShrink: 0,
                      }}
                    >
                      {signal.badge}
                    </span>

                    {/* Advisor name */}
                    <span style={{ fontSize: 12, fontWeight: 700, color: '#080707' }}>
                      {signal.advisorName}
                    </span>

                    {/* Firm */}
                    <span style={{ fontSize: 11, color: '#706e6b' }}>· {signal.firm}</span>

                    {/* AUM */}
                    <span
                      style={{
                        fontSize: 10,
                        fontWeight: 600,
                        color: '#514f4d',
                        marginLeft: 'auto',
                        flexShrink: 0,
                      }}
                    >
                      {formatAUM(signal.aum)} AUM
                    </span>
                  </div>

                  {/* Description */}
                  <div
                    style={{
                      fontSize: 12,
                      color: '#514f4d',
                      lineHeight: 1.45,
                    }}
                  >
                    {signal.description}
                  </div>

                  {/* Timestamp */}
                  <div
                    style={{
                      fontSize: 10,
                      color: '#c9c7c5',
                      marginTop: 4,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 4,
                    }}
                  >
                    <span style={{ color: config.dot, fontSize: 8 }}>●</span>
                    {/* tick dependency forces re-render for time display */}
                    {tick >= 0 && timeAgo(signal.timestamp)}
                  </div>
                </div>
              </div>
            )
          })
        )}
      </div>

      {/* Footer */}
      {signals.length > 0 && (
        <div
          style={{
            padding: '8px 16px',
            borderTop: '1px solid #f3f3f3',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <span style={{ fontSize: 11, color: '#706e6b' }}>
            Signals refresh every 8–12 seconds
          </span>
          <button
            onClick={() => setSignals([])}
            style={{
              fontSize: 11,
              color: '#c9c7c5',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '2px 6px',
              borderRadius: 4,
            }}
          >
            Clear
          </button>
        </div>
      )}
    </div>
  )
}
