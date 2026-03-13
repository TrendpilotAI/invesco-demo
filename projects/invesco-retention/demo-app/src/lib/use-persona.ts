'use client'

import { useSearchParams } from 'next/navigation'
import { useMemo } from 'react'
import { getPersonaConfig, type PersonaConfig } from './mock-data'

export interface UsePersonaResult {
  persona: PersonaConfig
  demoParam: string | null
  appendDemo: (url: string) => string
}

export function usePersona(): UsePersonaResult {
  const searchParams = useSearchParams()
  const demoParam = searchParams?.get('demo') ?? null

  const persona = useMemo(() => getPersonaConfig(demoParam), [demoParam])

  const appendDemo = (url: string): string => {
    if (!demoParam) return url
    const sep = url.includes('?') ? '&' : '?'
    return `${url}${sep}demo=${demoParam}`
  }

  return { persona, demoParam, appendDemo }
}
