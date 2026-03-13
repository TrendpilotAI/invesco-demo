'use client'

import { Suspense } from 'react'
import { useRouter } from 'next/navigation'
import { usePersona } from '@/lib/use-persona'

interface AppCard {
  id: string
  title: string
  subtitle: string
  icon: string
  href: string
  comingSoon?: boolean
  color: string
  bg: string
}

function HomeContent() {
  const router = useRouter()
  const { persona, appendDemo } = usePersona()

  const apps: AppCard[] = [
    {
      id: 'dashboard',
      title: 'Territory Dashboard',
      subtitle: 'Advisor signals & territory overview',
      icon: '📊',
      color: '#0176d3',
      bg: '#eef4ff',
      href: appendDemo('/dashboard'),
    },
    {
      id: 'create',
      title: 'Signal Studio',
      subtitle: 'Natural language signal queries',
      icon: '⚡',
      color: '#5867e8',
      bg: '#f3eeff',
      href: appendDemo('/create'),
    },
    {
      id: 'mobile',
      title: 'Mobile Brief',
      subtitle: 'Field-ready meeting prep',
      icon: '📱',
      color: '#706e6b',
      bg: '#f3f3f3',
      href: appendDemo('/mobile'),
    },
    {
      id: 'analytics',
      title: 'Analytics',
      subtitle: 'Portfolio reporting',
      icon: '📈',
      color: '#2e844a',
      bg: '#ebf7e6',
      href: '#',
      comingSoon: true,
    },
    {
      id: 'events',
      title: 'Events',
      subtitle: 'Webinar attendance',
      icon: '📅',
      color: '#e67e22',
      bg: '#fef4e8',
      href: '#',
      comingSoon: true,
    },
  ]

  const isPersona = persona.key !== 'default'

  return (
    <div className="min-h-screen" style={{ background: '#f3f3f3' }}>
      {/* Hero header */}
      <div
        style={{
          background: isPersona
            ? `linear-gradient(135deg, #032D60, ${persona.accentColor})`
            : '#032D60',
        }}
      >
        <div style={{ maxWidth: 896, margin: '0 auto', padding: '40px 24px 56px' }}>
          {/* Top bar */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, marginBottom: 20 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              {/* Logo */}
              <div
                style={{
                  width: 48,
                  height: 48,
                  borderRadius: 12,
                  background: 'rgba(255,255,255,0.15)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  border: '1px solid rgba(255,255,255,0.1)',
                  backdropFilter: 'blur(8px)',
                }}
              >
                <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor" style={{ width: 28, height: 28, color: '#fff' }}>
                  <path d="M10.5 3.5a4.5 4.5 0 0 1 4.36 3.4A3.5 3.5 0 0 1 18.5 10a3.5 3.5 0 0 1-.68 6.88L17.5 17h-11a4.5 4.5 0 0 1-.42-8.98A4.49 4.49 0 0 1 10.5 3.5z" opacity="0.9" />
                </svg>
              </div>
              <div>
                {isPersona ? (
                  <>
                    <p style={{ color: '#93c5fd', fontSize: 13, fontWeight: 500, margin: '0 0 2px' }}>
                      {persona.greeting} 👋
                    </p>
                    <h1 style={{ color: '#fff', fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: '-0.02em' }}>
                      Signal Studio
                    </h1>
                    <p style={{ color: '#93c5fd', fontSize: 11, fontWeight: 500, margin: '2px 0 0' }}>
                      {persona.title} · ForwardLane × Invesco
                    </p>
                  </>
                ) : (
                  <>
                    <h1 style={{ color: '#fff', fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: '-0.02em' }}>
                      Signal Studio
                    </h1>
                    <p style={{ color: '#93c5fd', fontSize: 13, fontWeight: 500, margin: '2px 0 0' }}>
                      ForwardLane × Invesco
                    </p>
                  </>
                )}
              </div>
            </div>

            {/* Invesco badge */}
            <div
              style={{
                background: 'rgba(255,255,255,0.12)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 8,
                padding: '6px 12px',
                display: 'flex',
                alignItems: 'center',
                gap: 8,
              }}
            >
              <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#4ade80' }} />
              <span style={{ color: '#fff', fontSize: 12, fontWeight: 600 }}>Invesco</span>
            </div>
          </div>

          {/* Persona hero stats */}
          {isPersona && (
            <div
              style={{
                background: 'rgba(255,255,255,0.08)',
                border: '1px solid rgba(255,255,255,0.12)',
                borderRadius: 12,
                padding: '16px 20px',
                marginBottom: 20,
              }}
            >
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
                {persona.stats.map((stat, i) => (
                  <div key={i} style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 20, fontWeight: 700, color: '#fff' }}>{stat.value}</div>
                    <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.65)', marginTop: 2 }}>{stat.label}</div>
                  </div>
                ))}
              </div>
              {persona.heroInsight && (
                <div
                  style={{
                    marginTop: 12,
                    paddingTop: 12,
                    borderTop: '1px solid rgba(255,255,255,0.1)',
                    fontSize: 12,
                    color: 'rgba(255,255,255,0.8)',
                    lineHeight: 1.5,
                  }}
                >
                  💡 {persona.heroInsight}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* App cards */}
      <div style={{ maxWidth: 896, margin: '-32px auto 0', padding: '0 24px 40px' }}>
        <div
          style={{
            background: '#fff',
            borderRadius: 16,
            border: '1px solid #e5e5e5',
            boxShadow: '0 4px 16px rgba(0,0,0,0.08)',
            overflow: 'hidden',
          }}
        >
          {/* Section header */}
          <div
            style={{
              padding: '16px 20px',
              borderBottom: '1px solid #f3f3f3',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ fontSize: 13, fontWeight: 700, color: '#080707' }}>All Apps</div>
              <div style={{ fontSize: 11, color: '#706e6b', marginTop: 1 }}>AI-powered advisor intelligence</div>
            </div>
          </div>

          {/* Cards grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: 1, background: '#f3f3f3' }}>
            {apps.map(app => (
              <button
                key={app.id}
                onClick={() => !app.comingSoon && router.push(app.href)}
                style={{
                  background: '#fff',
                  border: 'none',
                  padding: '24px 20px',
                  cursor: app.comingSoon ? 'default' : 'pointer',
                  textAlign: 'left',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  gap: 12,
                  transition: 'background 0.15s',
                  opacity: app.comingSoon ? 0.55 : 1,
                  position: 'relative',
                }}
                onMouseEnter={e => !app.comingSoon && ((e.currentTarget as HTMLElement).style.background = '#f8faff')}
                onMouseLeave={e => ((e.currentTarget as HTMLElement).style.background = '#fff')}
              >
                {/* Icon */}
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    background: app.bg,
                    border: `1px solid ${app.color}22`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 20,
                  }}
                >
                  {app.icon}
                </div>

                {/* Text */}
                <div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: '#080707', marginBottom: 2 }}>
                    {app.title}
                  </div>
                  <div style={{ fontSize: 11, color: '#706e6b', lineHeight: 1.4 }}>
                    {app.subtitle}
                  </div>
                </div>

                {app.comingSoon && (
                  <span
                    style={{
                      position: 'absolute',
                      top: 12,
                      right: 12,
                      fontSize: 9,
                      fontWeight: 700,
                      color: '#706e6b',
                      background: '#f3f3f3',
                      padding: '2px 6px',
                      borderRadius: 100,
                      letterSpacing: '0.04em',
                    }}
                  >
                    SOON
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Quick access */}
        <div style={{ marginTop: 16, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <button
            onClick={() => router.push(appendDemo('/dashboard'))}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              padding: '8px 14px',
              background: '#fff',
              border: '1px solid #e5e5e5',
              borderRadius: 100,
              cursor: 'pointer',
              fontSize: 12,
              fontWeight: 600,
              color: '#0176d3',
              transition: 'all 0.15s',
            }}
          >
            📊 Territory Dashboard
          </button>
          <button
            onClick={() => router.push(appendDemo('/mobile'))}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              padding: '8px 14px',
              background: '#fff',
              border: '1px solid #e5e5e5',
              borderRadius: 100,
              cursor: 'pointer',
              fontSize: 12,
              fontWeight: 600,
              color: '#514f4d',
              transition: 'all 0.15s',
            }}
          >
            📱 Mobile Brief
          </button>
        </div>
      </div>
    </div>
  )
}


export default function HomePage() {
  return (
    <Suspense fallback={<div style={{ minHeight: '100vh', background: '#f3f3f3' }} />}>
      <HomeContent />
    </Suspense>
  )
}
