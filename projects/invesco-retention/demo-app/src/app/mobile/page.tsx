'use client'

import { useState, Suspense } from 'react'
import { useRouter } from 'next/navigation'
import { advisors } from '@/lib/mock-data'
import { usePersona } from '@/lib/use-persona'
import { SLDSAvatar } from '@/components/slds-icons'

function MobileContent() {
  const router = useRouter()
  const { appendDemo } = usePersona()
  const [selectedAdvisor, setSelectedAdvisor] = useState(advisors[0])
  const [showList, setShowList] = useState(false)

  return (
    <div style={{ minHeight: '100vh', background: '#f3f3f3', maxWidth: 480, margin: '0 auto' }}>
      {/* Mobile header */}
      <div style={{ background: '#032D60', padding: '0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '12px 16px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
          <button
            onClick={() => router.push(appendDemo('/'))}
            style={{ background: 'none', border: 'none', color: 'rgba(255,255,255,0.7)', cursor: 'pointer', fontSize: 12 }}
          >
            ← Home
          </button>
          <span style={{ color: 'rgba(255,255,255,0.3)' }}>|</span>
          <span style={{ color: '#fff', fontSize: 12, fontWeight: 600 }}>Mobile Brief</span>
          <button
            onClick={() => setShowList(v => !v)}
            style={{
              marginLeft: 'auto',
              background: 'rgba(255,255,255,0.15)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: 6,
              color: '#fff',
              cursor: 'pointer',
              fontSize: 11,
              padding: '4px 10px',
            }}
          >
            Switch Advisor
          </button>
        </div>

        <div style={{ padding: '16px 16px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <SLDSAvatar name={selectedAdvisor.name} size={44} color={selectedAdvisor.engagementScore >= 50 ? '#0176d3' : '#ea001e'} />
            <div>
              <div style={{ color: '#fff', fontSize: 16, fontWeight: 700 }}>{selectedAdvisor.name}</div>
              <div style={{ color: 'rgba(255,255,255,0.65)', fontSize: 12 }}>{selectedAdvisor.firm} · {selectedAdvisor.city}</div>
              <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: 11, marginTop: 2 }}>
                ${selectedAdvisor.aum}M AUM · {selectedAdvisor.lastContact}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Advisor picker */}
      {showList && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.5)',
            zIndex: 100,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-end',
          }}
          onClick={() => setShowList(false)}
        >
          <div
            style={{ background: '#fff', borderRadius: '16px 16px 0 0', maxHeight: '70vh', overflow: 'auto' }}
            onClick={e => e.stopPropagation()}
          >
            <div style={{ padding: '16px 16px 8px', fontSize: 14, fontWeight: 700, color: '#080707', borderBottom: '1px solid #f3f3f3' }}>
              Select Advisor
            </div>
            {advisors.map(a => (
              <div
                key={a.id}
                onClick={() => { setSelectedAdvisor(a); setShowList(false) }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  padding: '12px 16px',
                  borderBottom: '1px solid #f3f3f3',
                  cursor: 'pointer',
                  background: selectedAdvisor.id === a.id ? '#eef4ff' : 'transparent',
                }}
              >
                <SLDSAvatar name={a.name} size={32} color={a.engagementScore >= 50 ? '#0176d3' : '#ea001e'} />
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: '#080707' }}>{a.name}</div>
                  <div style={{ fontSize: 11, color: '#706e6b' }}>{a.firm} · ${a.aum}M</div>
                </div>
                {a.signals.some(s => s.severity === 'urgent') && (
                  <span style={{ marginLeft: 'auto', fontSize: 9, color: '#ea001e', background: '#fef1ee', padding: '2px 6px', borderRadius: 100, fontWeight: 700 }}>
                    URGENT
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Meeting brief */}
      <div style={{ padding: '16px' }}>
        {/* Meeting prep card */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #e5e5e5',
            borderRadius: 12,
            overflow: 'hidden',
            marginBottom: 12,
            boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
          }}
        >
          <div style={{ padding: '12px 14px', background: '#fafbfc', borderBottom: '1px solid #e5e5e5', fontSize: 12, fontWeight: 700, color: '#080707', display: 'flex', alignItems: 'center', gap: 6 }}>
            📋 Meeting Brief
          </div>
          <div style={{ padding: '14px', fontSize: 12, color: '#514f4d', lineHeight: 1.6 }}>
            {selectedAdvisor.meetingPrepBrief.slice(0, 300)}
            {selectedAdvisor.meetingPrepBrief.length > 300 && '...'}
          </div>
        </div>

        {/* Key signals */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #e5e5e5',
            borderRadius: 12,
            overflow: 'hidden',
            marginBottom: 12,
            boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
          }}
        >
          <div style={{ padding: '12px 14px', background: '#fafbfc', borderBottom: '1px solid #e5e5e5', fontSize: 12, fontWeight: 700, color: '#080707' }}>
            ⚡ Active Signals
          </div>
          {selectedAdvisor.signals.slice(0, 3).map(signal => (
            <div
              key={signal.id}
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 10,
                padding: '10px 14px',
                borderBottom: '1px solid #f3f3f3',
                borderLeft: `3px solid ${signal.severity === 'urgent' ? '#ea001e' : signal.severity === 'attention' ? '#fe9339' : signal.severity === 'positive' ? '#2e844a' : '#0176d3'}`,
              }}
            >
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: signal.severity === 'urgent' ? '#ea001e' : signal.severity === 'attention' ? '#fe9339' : signal.severity === 'positive' ? '#2e844a' : '#0176d3',
                  marginTop: 4,
                  flexShrink: 0,
                }}
              />
              <div style={{ fontSize: 11, color: '#514f4d', lineHeight: 1.45 }}>{signal.text}</div>
            </div>
          ))}
        </div>

        {/* Talking points */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #e5e5e5',
            borderRadius: 12,
            overflow: 'hidden',
            marginBottom: 12,
            boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
          }}
        >
          <div style={{ padding: '12px 14px', background: '#fafbfc', borderBottom: '1px solid #e5e5e5', fontSize: 12, fontWeight: 700, color: '#080707' }}>
            💬 Talking Points
          </div>
          {selectedAdvisor.talkingPoints.slice(0, 3).map((tp, i) => (
            <div
              key={tp.id}
              style={{
                display: 'flex',
                gap: 10,
                padding: '10px 14px',
                borderBottom: i < 2 ? '1px solid #f3f3f3' : 'none',
              }}
            >
              <div
                style={{
                  width: 18,
                  height: 18,
                  borderRadius: '50%',
                  background: '#eef4ff',
                  color: '#0176d3',
                  fontSize: 10,
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  marginTop: 1,
                }}
              >
                {i + 1}
              </div>
              <div style={{ fontSize: 11, color: '#514f4d', lineHeight: 1.5 }}>
                {tp.text.slice(0, 120)}{tp.text.length > 120 ? '...' : ''}
              </div>
            </div>
          ))}
        </div>

        {/* Next best action */}
        <div
          style={{
            background: '#eef4ff',
            border: '1px solid #0176d333',
            borderRadius: 12,
            padding: '14px',
          }}
        >
          <div style={{ fontSize: 11, fontWeight: 700, color: '#0176d3', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            ⚡ Next Best Action
          </div>
          <div style={{ fontSize: 12, color: '#032d60', lineHeight: 1.55 }}>
            {selectedAdvisor.nextBestAction}
          </div>
        </div>
      </div>
    </div>
  )
}


export default function MobilePage() {
  return (
    <Suspense fallback={<div style={{ minHeight: '100vh', background: '#f3f3f3' }} />}>
      <MobileContent />
    </Suspense>
  )
}
