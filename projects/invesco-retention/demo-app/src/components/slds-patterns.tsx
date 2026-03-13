'use client'

import { useState } from 'react'

// ─── SLDSTimeline ──────────────────────────────────────────────────────────────
export interface TimelineItem {
  id?: string
  date: string
  type: 'email' | 'call' | 'meeting' | 'task' | 'event' | 'note'
  title?: string
  description: string
}

const timelineIcons: Record<string, string> = {
  email: '✉️',
  call: '📞',
  meeting: '📅',
  task: '✅',
  event: '🗓️',
  note: '📝',
}

const timelineColors: Record<string, string> = {
  email: '#0176d3',
  call: '#2e844a',
  meeting: '#5867e8',
  task: '#706e6b',
  event: '#fe9339',
  note: '#9602c7',
}

export function SLDSTimeline({ items }: { items: TimelineItem[] }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
      {items.map((item, i) => (
        <div key={i} style={{ display: 'flex', gap: 12, position: 'relative' }}>
          {/* Line */}
          {i < items.length - 1 && (
            <div
              style={{
                position: 'absolute',
                left: 15,
                top: 32,
                bottom: 0,
                width: 1,
                background: '#e5e5e5',
              }}
            />
          )}
          {/* Icon */}
          <div
            style={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              background: `${timelineColors[item.type]}15`,
              border: `1.5px solid ${timelineColors[item.type]}40`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 13,
              flexShrink: 0,
              zIndex: 1,
            }}
          >
            {timelineIcons[item.type]}
          </div>
          {/* Content */}
          <div style={{ flex: 1, paddingBottom: 16 }}>
            <div style={{ fontSize: 10, color: '#706e6b', marginBottom: 2 }}>{item.date}</div>
            <div style={{ fontSize: 12, color: '#514f4d', lineHeight: 1.45 }}>{item.description}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

// ─── SLDSCarousel ──────────────────────────────────────────────────────────────
export interface InsightCard {
  id: string
  title: string
  severity?: 'urgent' | 'attention' | 'positive' | 'info'
  detail?: string
  metric?: string
  // Extended fields from salesforce page
  description?: string
  color?: string
  icon?: string
  action?: string
}

const severityConfigs = {
  urgent: { color: '#ea001e', bg: '#fef1ee', border: '#fca5a5', label: 'URGENT' },
  attention: { color: '#8c4600', bg: '#fef4e8', border: '#fcd34d', label: 'ACTION' },
  positive: { color: '#2e844a', bg: '#ebf7e6', border: '#86efac', label: 'GOOD' },
  info: { color: '#0176d3', bg: '#eef4ff', border: '#bfdbfe', label: 'INFO' },
}

export function SLDSCarousel({ cards }: { cards: InsightCard[] }) {
  const [activeIndex, setActiveIndex] = useState(0)

  if (!cards || cards.length === 0) {
    return <div style={{ padding: '12px', color: '#706e6b', fontSize: 12 }}>No signals</div>
  }

  const card = cards[activeIndex]
  const cfg = card.severity ? severityConfigs[card.severity] : {
    color: card.color || '#0176d3',
    bg: '#eef4ff',
    border: '#bfdbfe',
    label: card.title,
  }

  return (
    <div>
      {/* Card */}
      <div
        style={{
          border: `1px solid ${cfg.border}`,
          borderLeft: `4px solid ${cfg.color}`,
          borderRadius: 8,
          padding: '14px',
          background: cfg.bg,
          marginBottom: 10,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
          <span
            style={{
              fontSize: 9,
              fontWeight: 700,
              color: cfg.color,
              background: 'rgba(255,255,255,0.7)',
              padding: '1px 6px',
              borderRadius: 100,
              letterSpacing: '0.05em',
            }}
          >
            {cfg.label}
          </span>
          {card.metric && (
            <span style={{ fontSize: 12, fontWeight: 700, color: cfg.color, marginLeft: 'auto' }}>
              {card.metric}
            </span>
          )}
        </div>
        <div style={{ fontSize: 12, fontWeight: 600, color: '#080707', marginBottom: 4 }}>{card.title}</div>
        {(card.detail || card.description) && (
          <div style={{ fontSize: 11, color: '#514f4d', lineHeight: 1.5 }}>
            {((card.detail || card.description) ?? '').slice(0, 200)}{((card.detail || card.description) ?? '').length > 200 ? '...' : ''}
          </div>
        )}
      </div>

      {/* Pagination dots */}
      {cards.length > 1 && (
        <div style={{ display: 'flex', gap: 6, justifyContent: 'center', alignItems: 'center' }}>
          {cards.map((c, i) => {
            const dotCfg = c.severity ? severityConfigs[c.severity] : { color: c.color || '#0176d3' }
            return (
              <button
                key={c.id}
                onClick={() => setActiveIndex(i)}
                style={{
                  width: i === activeIndex ? 20 : 6,
                  height: 6,
                  borderRadius: 3,
                  background: i === activeIndex ? dotCfg.color : '#c9c7c5',
                  border: 'none',
                  cursor: 'pointer',
                  padding: 0,
                  transition: 'all 0.2s',
                }}
              />
            )
          })}
        </div>
      )}
    </div>
  )
}

// ─── SLDSProgressBar ──────────────────────────────────────────────────────────
export function SLDSProgressBar({
  label,
  value,
  max = 100,
  color = '#0176d3',
}: {
  label: string
  value: number
  max?: number
  color?: string
}) {
  const pct = Math.min(100, Math.round((value / max) * 100))
  const barColor = pct >= 80 ? '#2e844a' : pct >= 50 ? '#0176d3' : pct >= 25 ? '#fe9339' : '#ea001e'

  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4, alignItems: 'center' }}>
        <span style={{ fontSize: 11, color: '#514f4d', fontWeight: 500 }}>{label}</span>
        <span style={{ fontSize: 11, fontWeight: 700, color: barColor }}>{value}</span>
      </div>
      <div style={{ height: 5, background: '#e5e5e5', borderRadius: 3, overflow: 'hidden' }}>
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            background: barColor,
            borderRadius: 3,
            transition: 'width 0.5s ease',
          }}
        />
      </div>
    </div>
  )
}

// ─── SLDSProgressRing ─────────────────────────────────────────────────────────
export function SLDSProgressRing({
  value,
  max = 100,
  size = 64,
  strokeWidth = 6,
  color,
  label,
  subLabel,
}: {
  value: number
  max?: number
  size?: number
  strokeWidth?: number
  color?: string
  label?: string
  subLabel?: string
}) {
  const pct = Math.min(100, Math.round((value / max) * 100))
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (pct / 100) * circumference
  const ringColor = color || (pct >= 80 ? '#2e844a' : pct >= 50 ? '#0176d3' : pct >= 25 ? '#fe9339' : '#ea001e')

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
      <div style={{ position: 'relative', width: size, height: size }}>
        <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="#e5e5e5"
            strokeWidth={strokeWidth}
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={ringColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 0.6s ease' }}
          />
        </svg>
        {label && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexDirection: 'column',
              gap: 1,
            }}
          >
            <span style={{ fontSize: Math.round(size * 0.22), fontWeight: 700, color: ringColor, lineHeight: 1 }}>
              {label}
            </span>
            {subLabel && (
              <span style={{ fontSize: Math.round(size * 0.13), color: '#706e6b', lineHeight: 1 }}>
                {subLabel}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

// ─── SLDSPill ─────────────────────────────────────────────────────────────────
const pillColors: Record<string, { color: string; bg: string; border: string }> = {
  blue: { color: '#0176d3', bg: '#eef4ff', border: '#0176d340' },
  green: { color: '#2e844a', bg: '#ebf7e6', border: '#2e844a40' },
  purple: { color: '#9602c7', bg: '#f3eeff', border: '#9602c740' },
  red: { color: '#ea001e', bg: '#fef1ee', border: '#ea001e40' },
  orange: { color: '#8c4600', bg: '#fef4e8', border: '#fe933940' },
  default: { color: '#514f4d', bg: '#f3f3f3', border: '#c9c7c5' },
}

export function SLDSPill({
  label,
  color = 'default',
  icon,
}: {
  label: string
  color?: string
  icon?: string
}) {
  const cfg = pillColors[color] || pillColors.default
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 4,
        padding: '3px 10px',
        borderRadius: 100,
        border: `1px solid ${cfg.border}`,
        background: cfg.bg,
        color: cfg.color,
        fontSize: 11,
        fontWeight: 500,
      }}
    >
      {icon && <span style={{ fontSize: 10 }}>{icon === 'people' ? '👥' : icon === 'location' ? '📍' : '·'}</span>}
      {label}
    </span>
  )
}
