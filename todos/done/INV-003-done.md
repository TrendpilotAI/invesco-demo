# INV-003 Done — Personalized Demo Persona via URL Param

**Completed:** 2026-03-08  
**Commit:** `9136590` on `TrendpilotAI/invesco-demo` main branch

## What Was Built

### New Files
- **`src/personas.ts`** — Persona type + data for Megan, Craig, and default
- **`src/components/PersonaBadge.tsx`** — Subtle top-right badge with pulsing dot, fades in over first 30 frames

### Modified Files
- **`src/Root.tsx`** — Added `DemoProps` type; three Remotion compositions: `InvescoDemoFull`, `InvescoDemoMegan`, `InvescoDemoCraig`
- **`src/InvescoDemoVideo.tsx`** — Accepts `demo` prop, resolves persona, renders `PersonaBadge`, passes persona to child scenes
- **`src/scenes/IntroScene.tsx`** — Persona-aware intro: greeting pill, territory chip, AUM/advisor stats, personalized subtitle
- **`src/scenes/ScreenScene.tsx`** — Persona territory shown in screen browser address bar + header

## Personas

### Megan Weber (`?demo=megan`)
- **View:** "Megan Weber's View"
- **Role:** Regional Wholesaler — Mountain West
- **Territory:** CO, UT, AZ, NV
- **AUM:** $2.4B | 847 advisors | 34 weekly opportunities
- **Badge:** "Demo: Megan Weber"
- **Top advisors:** Sarah Mitchell (Rising Star), James Tanner (Cross-Sell), Priya Nair (Greenspace)

### Craig Lieb (`?demo=craig`)
- **View:** "Craig Lieb's View"
- **Role:** National Accounts Director
- **Territory:** National Accounts — Wirehouse & IBD Channels
- **AUM:** $8.1B | 2,340 advisors | 67 weekly opportunities
- **Badge:** "Demo: Craig Lieb"
- **Top advisors:** David Harrington (Competitive Displacement), Karen Brooks (Fallen Angel), Michael Torres (Rising Star)

### Default (no param)
- Generic ForwardLane demo — no badge, no personalization

## How to Use
In Remotion Studio, select the desired composition:
- `InvescoDemoFull` → Generic
- `InvescoDemoMegan` → Megan's view
- `InvescoDemoCraig` → Craig's view

Or pass `inputProps` at render time:
```bash
remotion render src/index.ts InvescoDemoFull out/demo-megan.mp4 --props='{"demo":"megan"}'
```
