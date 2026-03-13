'use client'

import { useState, Suspense } from 'react'
import { useRouter } from 'next/navigation'
import { usePersona } from '@/lib/use-persona'
import { advisors } from '@/lib/mock-data'

const SIGNAL_TEMPLATES = [
  { id: 't1', label: 'AUM Decline Alert', query: 'Which advisors have seen AUM decline this quarter?' },
  { id: 't2', label: 'ESG Cross-Sell', query: 'Identify RIAs with ESG exposure that could be migrated to Invesco ETF suite' },
  { id: 't3', label: 'Engagement Drop', query: 'Show advisors with engagement score below 50 and AUM over $200M' },
  { id: 't4', label: 'Competitive Threat', query: 'Which advisors are buying BlackRock or Vanguard products we could displace?' },
  { id: 't5', label: 'Retirement Income', query: 'Find retirement-focused advisors with T. Rowe or Fidelity target date exposure' },
  { id: 't6', label: '401k Opportunity', query: 'Advisors with 401k/corporate retirement focus and low Invesco wallet share' },
]

const MOCK_RESULTS = [
  { advisor: 'Robert Kim', firm: 'JP Morgan', signal: 'AUM decline risk — 90-day silence + $3.5M outflow to BlackRock', priority: 'urgent' as const },
  { advisor: 'James Patel', firm: 'Wells Fargo', signal: 'Lost $40M to Fidelity — Q1 Discovery Fund test is retention anchor', priority: 'urgent' as const },
  { advisor: 'David Okafor', firm: 'Morgan Stanley', signal: '$620M AUM with only 14% Invesco share — private credit window open', priority: 'attention' as const },
  { advisor: 'Marcus Thompson', firm: 'Merrill Lynch', signal: '$27M Vanguard Target Date displacement pipeline closing this quarter', priority: 'positive' as const },
  { advisor: 'Amanda Foster', firm: 'Mosaic Financial', signal: 'Model portfolio champion — $20M tax-managed opportunity + direct indexing pilot', priority: 'positive' as const },
]

function CreateContent() {
  const router = useRouter()
  const { appendDemo } = usePersona()
  const [query, setQuery] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [hasResults, setHasResults] = useState(false)
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null)

  const handleRun = async () => {
    if (!query.trim()) return
    setIsRunning(true)
    setHasResults(false)
    await new Promise(r => setTimeout(r, 1800))
    setIsRunning(false)
    setHasResults(true)
  }

  const handleTemplate = (template: typeof SIGNAL_TEMPLATES[0]) => {
    setQuery(template.query)
    setSelectedTemplate(template.id)
    setHasResults(false)
  }

  return (
    <div style={{ minHeight: '100vh', background: '#f3f3f3' }}>
      {/* Header */}
      <div style={{ background: '#032D60' }}>
        <div style={{ maxWidth: 960, margin: '0 auto', padding: '0 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '12px 0', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <button
              onClick={() => router.push(appendDemo('/'))}
              style={{ background: 'none', border: 'none', color: 'rgba(255,255,255,0.7)', cursor: 'pointer', fontSize: 12 }}
            >
              ← Home
            </button>
            <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: 12 }}>/</span>
            <span style={{ color: '#fff', fontSize: 12, fontWeight: 600 }}>Signal Studio</span>
          </div>
          <div style={{ padding: '20px 0 28px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
              <div
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: 10,
                  background: 'rgba(88, 103, 232, 0.3)',
                  border: '1px solid rgba(88, 103, 232, 0.5)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 18,
                }}
              >
                ⚡
              </div>
              <div>
                <h1 style={{ color: '#fff', fontSize: 18, fontWeight: 700, margin: 0 }}>Signal Studio</h1>
                <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 12, margin: '2px 0 0' }}>
                  Natural language advisor intelligence
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 960, margin: '0 auto', padding: '20px' }}>
        {/* Query input */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #e5e5e5',
            borderRadius: 12,
            padding: '20px',
            marginBottom: 16,
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
          }}
        >
          <div style={{ marginBottom: 12 }}>
            <label style={{ fontSize: 12, fontWeight: 700, color: '#080707', display: 'block', marginBottom: 8 }}>
              Describe the signals you're looking for
            </label>
            <textarea
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="e.g. Which advisors have AUM decline risk and haven't been contacted in 60+ days?"
              style={{
                width: '100%',
                minHeight: 88,
                padding: '12px 14px',
                border: '1.5px solid #e5e5e5',
                borderRadius: 8,
                fontSize: 13,
                color: '#080707',
                resize: 'vertical',
                outline: 'none',
                fontFamily: 'inherit',
                lineHeight: 1.5,
                boxSizing: 'border-box',
                transition: 'border-color 0.15s',
              }}
              onFocus={e => (e.target.style.borderColor = '#0176d3')}
              onBlur={e => (e.target.style.borderColor = '#e5e5e5')}
            />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
            <span style={{ fontSize: 11, color: '#706e6b' }}>
              Powered by ForwardLane AI — searches across {advisors.length} advisors
            </span>
            <button
              onClick={handleRun}
              disabled={!query.trim() || isRunning}
              style={{
                padding: '10px 20px',
                background: !query.trim() || isRunning ? '#c9c7c5' : '#0176d3',
                color: '#fff',
                border: 'none',
                borderRadius: 8,
                fontSize: 13,
                fontWeight: 700,
                cursor: !query.trim() || isRunning ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                transition: 'background 0.15s',
                flexShrink: 0,
              }}
            >
              {isRunning ? (
                <>
                  <div
                    style={{
                      width: 14,
                      height: 14,
                      border: '2px solid rgba(255,255,255,0.3)',
                      borderTopColor: '#fff',
                      borderRadius: '50%',
                      animation: 'spin 0.8s linear infinite',
                    }}
                  />
                  Analyzing...
                </>
              ) : (
                <>⚡ Run Signal</>
              )}
            </button>
          </div>
        </div>

        {/* Templates */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #e5e5e5',
            borderRadius: 12,
            padding: '16px 20px',
            marginBottom: 16,
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
          }}
        >
          <div style={{ fontSize: 12, fontWeight: 700, color: '#080707', marginBottom: 12 }}>
            📋 Signal Templates
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {SIGNAL_TEMPLATES.map(t => (
              <button
                key={t.id}
                onClick={() => handleTemplate(t)}
                style={{
                  padding: '6px 12px',
                  borderRadius: 100,
                  border: '1px solid',
                  borderColor: selectedTemplate === t.id ? '#0176d3' : '#e5e5e5',
                  background: selectedTemplate === t.id ? '#eef4ff' : '#fafbfc',
                  color: selectedTemplate === t.id ? '#0176d3' : '#514f4d',
                  fontSize: 12,
                  fontWeight: 500,
                  cursor: 'pointer',
                  transition: 'all 0.12s',
                }}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results */}
        {hasResults && (
          <div
            className="animate-fade-in-up"
            style={{
              background: '#fff',
              border: '1px solid #e5e5e5',
              borderRadius: 12,
              overflow: 'hidden',
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
            }}
          >
            <div
              style={{
                padding: '14px 18px',
                borderBottom: '1px solid #e5e5e5',
                background: '#fafbfc',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
              <div>
                <div style={{ fontSize: 13, fontWeight: 700, color: '#080707' }}>
                  Signal Results · {MOCK_RESULTS.length} advisors matched
                </div>
                <div style={{ fontSize: 11, color: '#706e6b', marginTop: 1 }}>
                  Ranked by priority and opportunity score
                </div>
              </div>
              <span
                style={{
                  fontSize: 10,
                  fontWeight: 700,
                  color: '#0176d3',
                  background: '#eef4ff',
                  padding: '2px 8px',
                  borderRadius: 100,
                }}
              >
                LIVE DATA
              </span>
            </div>

            {MOCK_RESULTS.map((result, i) => {
              const cfg = {
                urgent: { color: '#ea001e', bg: '#fef1ee', label: 'URGENT' },
                attention: { color: '#8c4600', bg: '#fef4e8', label: 'ACTION' },
                positive: { color: '#2e844a', bg: '#ebf7e6', label: 'OPPORTUNITY' },
              }[result.priority]

              return (
                <div
                  key={i}
                  style={{
                    display: 'flex',
                    gap: 14,
                    padding: '14px 18px',
                    borderBottom: i < MOCK_RESULTS.length - 1 ? '1px solid #f3f3f3' : 'none',
                    cursor: 'pointer',
                    transition: 'background 0.12s',
                  }}
                  onMouseEnter={e => (e.currentTarget.style.background = '#f8faff')}
                  onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
                >
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: '50%',
                      background: cfg.bg,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: 13,
                      fontWeight: 700,
                      color: cfg.color,
                      flexShrink: 0,
                    }}
                  >
                    {i + 1}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 3 }}>
                      <span style={{ fontSize: 13, fontWeight: 700, color: '#080707' }}>{result.advisor}</span>
                      <span style={{ fontSize: 11, color: '#706e6b' }}>· {result.firm}</span>
                      <span
                        style={{
                          fontSize: 9,
                          fontWeight: 700,
                          color: cfg.color,
                          background: cfg.bg,
                          padding: '1px 6px',
                          borderRadius: 100,
                          marginLeft: 'auto',
                        }}
                      >
                        {cfg.label}
                      </span>
                    </div>
                    <div style={{ fontSize: 12, color: '#514f4d', lineHeight: 1.45 }}>
                      {result.signal}
                    </div>
                  </div>
                </div>
              )
            })}

            <div
              style={{
                padding: '12px 18px',
                borderTop: '1px solid #f3f3f3',
                display: 'flex',
                gap: 8,
              }}
            >
              <button
                style={{
                  padding: '8px 16px',
                  background: '#0176d3',
                  color: '#fff',
                  border: 'none',
                  borderRadius: 6,
                  fontSize: 12,
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Save Signal Query
              </button>
              <button
                style={{
                  padding: '8px 16px',
                  background: '#fff',
                  color: '#0176d3',
                  border: '1px solid #0176d3',
                  borderRadius: 6,
                  fontSize: 12,
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Export to Salesforce
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}


export default function CreatePage() {
  return (
    <Suspense fallback={<div style={{ minHeight: '100vh', background: '#f3f3f3' }} />}>
      <CreateContent />
    </Suspense>
  )
}
