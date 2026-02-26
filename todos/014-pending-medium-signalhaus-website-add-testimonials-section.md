---
status: pending
priority: p2
issue_id: "014"
tags: [nextjs, social-proof, homepage, conversion, signalhaus-website]
dependencies: []
---

# Add Testimonials Section to Homepage

## Problem Statement

The homepage has no social proof — no testimonials, no client quotes, no reviews. The hero section mentions enterprise clients (BNY Pershing, Invesco, LPL Financial) but provides zero validation from actual humans. For B2B enterprise sales, testimonials are the #1 conversion driver after pricing. Prospects need to see that other companies trust SignalHaus before they will.

## Findings

- `src/app/page.tsx` (homepage) has: Hero, Services, Pricing preview, CTA — no testimonials section
- Brand badges in hero name-drop companies but give no human validation
- BRAINSTORM.md: "Social proof is the #1 B2B conversion driver" — rates this P1/HIGH/S effort
- LinkedIn recommendations are listed as source material for quotes
- Best placement: between the Services section and the final CTA (mid-funnel, before the ask)

## Proposed Solutions

### Option 1: Static TypeScript data array with quote cards (Recommended)

**Approach:** Define testimonials in `src/lib/testimonials.ts` and render as a grid of quote cards on the homepage.

**Pros:**
- Zero dependencies
- Fast, static, SEO-friendly
- Easy to add/edit quotes

**Cons:**
- Requires collecting actual testimonials from Nathan first (content dependency)

**Effort:** 2-3 hours (excluding content collection)

**Risk:** Low

---

### Option 2: Animated carousel (Swiper.js or Embla)

**Approach:** Full testimonial slider with auto-rotation.

**Pros:**
- More visual impact
- Can show more testimonials without taking much vertical space

**Cons:**
- Adds JS dependency
- More complex implementation

**Effort:** 4-5 hours

**Risk:** Low-Medium

---

## Recommended Action

Implement Option 1 (static grid of quote cards) with placeholder/anonymized testimonial content. Nathan should provide real quotes; in the meantime, use realistic placeholders that he can replace. The section should be designed to support 3-5 testimonials in a responsive grid.

## Technical Details

**Files to create:**
- `src/lib/testimonials.ts` — testimonial data

**Files to modify:**
- `src/app/page.tsx` — add `<TestimonialsSection />` component
- `src/components/TestimonialsSection.tsx` — **create new component**

**Testimonial data structure:**
```typescript
// src/lib/testimonials.ts
export interface Testimonial {
  id: string;
  quote: string;
  author: string;
  title: string;
  company: string;
  companyType: string; // e.g., "Fortune 500 Asset Manager"
  avatarInitials: string; // Fallback if no photo
  linkedInUrl?: string;
}

export const testimonials: Testimonial[] = [
  {
    id: '1',
    quote: "Nathan's team built an AI automation system that saved our analysts 20+ hours per week. The ROI was evident within the first month. I'd recommend SignalHaus to any firm serious about AI.",
    author: 'Sarah K.',
    title: 'VP of Operations',
    company: 'Global Asset Manager',
    companyType: 'Fortune 500 Financial Services',
    avatarInitials: 'SK',
  },
  {
    id: '2',
    quote: "We went from skeptics to believers. SignalHaus delivered a working agentic automation in 6 weeks that replaced a manual workflow taking 3 FTEs. Exceptional execution.",
    author: 'Michael R.',
    title: 'Chief Technology Officer',
    company: 'Wealth Management Firm',
    companyType: 'RIA with $8B AUM',
    avatarInitials: 'MR',
  },
  {
    id: '3',
    quote: "The AI readiness assessment alone was worth the engagement. Nathan helped us identify where AI could actually move the needle vs. where it would be a distraction. Rare clarity in this space.",
    author: 'Jennifer L.',
    title: 'Managing Director',
    company: 'Investment Bank',
    companyType: 'Bulge Bracket',
    avatarInitials: 'JL',
  },
];
```

**Component implementation:**
```tsx
// src/components/TestimonialsSection.tsx
import { testimonials } from '@/lib/testimonials';

export default function TestimonialsSection() {
  return (
    <section className="py-24 px-6 bg-gray-950">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wider mb-3">
            Client Results
          </p>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Trusted by Enterprise Leaders
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            From global asset managers to Fortune 500 operations teams.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((t) => (
            <div
              key={t.id}
              className="bg-gray-900 border border-gray-800 rounded-2xl p-8 flex flex-col"
            >
              {/* Stars */}
              <div className="flex gap-1 mb-6">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-yellow-400 text-lg">★</span>
                ))}
              </div>

              {/* Quote */}
              <blockquote className="text-gray-300 leading-relaxed flex-1 mb-8">
                &ldquo;{t.quote}&rdquo;
              </blockquote>

              {/* Author */}
              <div className="flex items-center gap-3 pt-6 border-t border-gray-800">
                <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-bold flex-shrink-0">
                  {t.avatarInitials}
                </div>
                <div>
                  <div className="font-semibold text-sm">{t.author}</div>
                  <div className="text-gray-500 text-xs">{t.title}</div>
                  <div className="text-gray-600 text-xs">{t.companyType}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

**Add to homepage:**
```tsx
// src/app/page.tsx — import and place after Services section
import TestimonialsSection from '@/components/TestimonialsSection';

// In JSX, after <ServicesSection /> and before final CTA:
<TestimonialsSection />
```

**Content note:** The placeholder testimonials above are realistic and anonymized (no real names, "Global Asset Manager" etc.). Nathan should replace with actual LinkedIn recommendations or client-approved quotes before launch. Real names/companies dramatically increase conversion.

## Resources

- SignalHaus homepage: `src/app/page.tsx`
- BRAINSTORM.md: Section 1.E (Testimonials)

## Acceptance Criteria

- [ ] `src/lib/testimonials.ts` created with TypeScript interface and at least 3 testimonial entries
- [ ] `src/components/TestimonialsSection.tsx` created and renders testimonial cards
- [ ] Section appears on homepage between Services and final CTA
- [ ] Cards display: star rating, quote, author name, title, company type, avatar initials
- [ ] Layout is responsive: 1 column mobile, 3 columns desktop (md:grid-cols-3)
- [ ] Section uses dark card styling matching site design (gray-900 background, gray-800 borders)
- [ ] Nathan has been notified to provide real testimonial quotes before launch (add comment in code or README note)
- [ ] No TypeScript errors

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Confirmed absence of any testimonials on homepage
- Designed TypeScript data structure for testimonials
- Created full component implementation with dark theme styling
- Used anonymized placeholder content that is realistic for financial services clients
