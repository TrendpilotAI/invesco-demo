# TODO-899: Extract ROI calculate() to src/lib/roi.ts
**Repo:** signalhaus-website  
**Priority:** P1  
**Status:** pending  
**Effort:** 30 minutes

## Problem
The `calculate()` function in `src/components/ROICalculator.tsx` is a pure, dependency-free math function embedded inside a large client component. This makes it:
- **Untestable** with unit tests (can't import client components in Vitest without full React setup)
- **Harder to maintain** (logic mixed with UI)
- **Not reusable** for the `/api/roi-email` endpoint (TODO-pending)

## Task
Move the `calculate()` function and related types/constants to `src/lib/roi.ts`.

## Coding Prompt
```typescript
// Create: /data/workspace/projects/signalhaus-website/src/lib/roi.ts

export interface ROIInputs {
  teamSize: number
  manualHours: number
  avgDealSize: number
  conversionRate: number
  monthlyLeads: number
}

export interface ROIResults {
  timeSavedHours: number
  timeSavedPercent: number
  annualCostSavings: number
  additionalRevenue: number
  totalAnnualImpact: number
  paybackMonths: number
  roi12Month: number
}

export const ROI_CONSTANTS = {
  AVG_HOURLY_RATE: 75,
  AUTOMATION_EFFICIENCY: 0.70,
  CONVERSION_LIFT: 0.30,
  SIGNALHAUS_MONTHLY_COST: 4800,
} as const

export function calculateROI(inputs: ROIInputs): ROIResults {
  const { teamSize, manualHours, avgDealSize, conversionRate, monthlyLeads } = inputs
  const { AVG_HOURLY_RATE, AUTOMATION_EFFICIENCY, CONVERSION_LIFT, SIGNALHAUS_MONTHLY_COST } = ROI_CONSTANTS

  const weeklyHoursSaved = teamSize * manualHours * AUTOMATION_EFFICIENCY
  const annualHoursSaved = weeklyHoursSaved * 52
  const timeSavedPercent = AUTOMATION_EFFICIENCY * 100
  const annualCostSavings = annualHoursSaved * AVG_HOURLY_RATE

  const additionalDeals = monthlyLeads * (conversionRate / 100) * CONVERSION_LIFT * 12
  const additionalRevenue = additionalDeals * avgDealSize

  const totalAnnualImpact = annualCostSavings + additionalRevenue
  const paybackMonths = Math.ceil((SIGNALHAUS_MONTHLY_COST * 12) / (totalAnnualImpact / 12))
  const roi12Month = Math.round(
    ((totalAnnualImpact - SIGNALHAUS_MONTHLY_COST * 12) / (SIGNALHAUS_MONTHLY_COST * 12)) * 100
  )

  return {
    timeSavedHours: Math.round(annualHoursSaved),
    timeSavedPercent,
    annualCostSavings: Math.round(annualCostSavings),
    additionalRevenue: Math.round(additionalRevenue),
    totalAnnualImpact: Math.round(totalAnnualImpact),
    paybackMonths,
    roi12Month,
  }
}

// Update: /data/workspace/projects/signalhaus-website/src/components/ROICalculator.tsx
// Remove local Inputs, Results interfaces and calculate() function
// Add: import { calculateROI, ROIInputs as Inputs, ROIResults as Results } from '@/lib/roi'
// Replace: calculate(inputs) → calculateROI(inputs)
```

## Dependencies
- Prereq for TODO-894 (Vitest unit tests — roi.test.ts tests this)
- Prereq for future ROI email API route

## Acceptance Criteria
- `src/lib/roi.ts` exists with `calculateROI()` exported
- `ROICalculator.tsx` imports from `@/lib/roi`
- `npm run build` passes
- `npm run typecheck` passes
- ROI calculator UI still works identically
