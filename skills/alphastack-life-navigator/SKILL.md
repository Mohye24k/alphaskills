---
name: alphastack-life-navigator
description: The master router for AlphaStack — takes any high-stakes life question from any person (health, finance, legal, consumer, career, medical, automotive, regulatory, research) and dispatches it to the right specialist skill OR combination of skills. Handles questions like "I found a lump on my neck, what should I do", "is this lease predatory", "should I buy this stock", "what drug is cheapest for my condition", "is this car safe", "did an activist just file on my holdings", "what does the Fed meeting mean for my mortgage". This is the one skill a normal person needs — it gives them access to all 27 specialist AlphaStack skills + the full alphaskills_py Python library through a single natural conversation. Designed to be the foundation of a consumer product replacing $500/hour professionals (doctors, lawyers, financial advisors) with a free+$20/month AI assistant.
---

# AlphaStack Life Navigator — The One Skill Everyone Needs

## The premise

Every adult has questions worth thousands of dollars in professional fees that they can't afford.

- **Medical**: "Is this symptom serious? What's the right specialist? Are there trials?" → $500-2000 per specialist visit in the US
- **Legal**: "Is this contract fair? What are my rights as a tenant/worker/patient?" → $300-500/hour
- **Financial**: "Should I buy this stock? Is this insider activity a warning? What's my mortgage decision?" → $200-500/hour for a CFP
- **Consumer**: "Is this car safe? Is this drug cheaper somewhere? Is this loan predatory?" → Often no affordable professional

**Combined, these questions represent ~$500B/year of professional services the average person needs but skips.**

AlphaStack Life Navigator is the free alternative. It routes any question to the right specialist skill in the AlphaStack portfolio and delivers institutional-grade answers in plain language.

## When to invoke

**This is the default skill for anyone opening the AlphaStack consumer product.** It's called whenever the user asks a high-stakes life question that isn't obviously in a single domain.

Trigger on any of:

- Medical questions (symptoms, drugs, trials, specialists)
- Financial questions (stocks, mortgages, insurance, macro)
- Legal questions (contracts, rights, filings)
- Consumer questions (cars, products, recalls)
- Research questions (academic literature, grants)

## The routing matrix

### Medical / Health questions

| Question pattern | Route to |
|-----------------|---------|
| "I have [symptoms]..." | `rare-disease-detective` |
| "My [family member] has [diagnosis]..." | `patient-trial-navigator` |
| "[Drug] costs too much..." | `drug-affordability-rescue` |
| "Is [drug X] safe?" | `fda-drug-recalls-faers` |
| "What trials are there for [disease]?" | `clinical-trial-intel` or `patient-trial-navigator` |
| "History of [drug]" | `drug-lifecycle-tracker` |
| "Research on [topic]" | `pubmed-paper-scan` + `biorxiv-preprint-scan` |
| "NIH grants for [field]" | `nih-grant-scan` |

### Financial / Investment questions

| Question pattern | Route to |
|-----------------|---------|
| "Should I buy [TICKER]?" | `stock-signal-report` |
| "Tell me about [company]" | `company-deepdive` |
| "What did [hedge fund] buy?" | `hedge-fund-holdings` |
| "Activist activity in [stock]" | `activist-campaign-tracker` |
| "Insider trades at [ticker]" | `sec-insider-scan` |
| "Upcoming catalysts" | `catalyst-calendar` |
| "M&A targets in [sector]" | `ma-target-scanner` |
| "Short squeeze candidates" | `short-squeeze-detector` |
| "Gold / oil / macro positioning" | `futures-positioning-check` |
| "Fed / CPI / unemployment / GDP" | `fred-economic-data` |
| "New IPO filings" | `sec-s1-ipo-tracker` |

### Legal / Regulatory questions

| Question pattern | Route to |
|-----------------|---------|
| "Any new rules from [agency]?" | `federal-register-tracker` |
| "Court cases against [company]" | `courtlistener-docket-tracker` |
| "Class action opportunities" | `courtlistener-docket-tracker` + `nhtsa-recalls-tracker` |

### Consumer / Auto questions

| Question pattern | Route to |
|-----------------|---------|
| "Recalls on my [make/model]?" | `vehicle-recall-check` |
| "Is [car] safe to buy used?" | `vehicle-recall-check` |

### Research / Academic questions

| Question pattern | Route to |
|-----------------|---------|
| "Latest papers on [topic]" | `arxiv-paper-scan` / `pubmed-paper-scan` |
| "Research funding in [field]" | `nih-grant-scan` |
| "Who is [researcher/executive]?" | `executive-network-mapper` |

## Multi-skill orchestration (the power move)

Many questions require COMBINING skills. The navigator should recognize these:

### Pattern: "Should I invest in [biotech ticker]?"

Route to:
1. `stock-signal-report` — financial signal
2. `clinical-trial-intel` — pipeline check (with ticker's parent company as sponsor)
3. `fda-drug-recalls-faers` — safety issues with their approved drugs
4. `nih-grant-scan` — academic research tailwind
5. `executive-network-mapper` — management background

Then synthesize: "Financial signal is [X], but pipeline has [Y] Phase 3 readouts in next 6 months. Management has [Z] background. Overall: [BULL/BEAR]."

### Pattern: "My mother has [disease], what do we do?"

Route to:
1. `rare-disease-detective` (if symptoms unclear) OR `patient-trial-navigator` (if diagnosis known)
2. `drug-affordability-rescue` (for currently-prescribed meds)
3. `pubmed-paper-scan` for latest research
4. `executive-network-mapper` for key specialists

Then synthesize into a patient care plan.

### Pattern: "Is buying this used car safe?"

Route to:
1. `vehicle-recall-check` (for the specific make/model/year)
2. `courtlistener-docket-tracker` (for class-action patterns)
3. `federal-register-tracker` (for new NHTSA investigations)

Then synthesize: "Recall history is [X], open class actions are [Y], NHTSA investigations [Z]."

### Pattern: "Is my lease predatory?"

Route to:
1. `federal-register-tracker` (for current tenant rights regulations in their state)
2. `courtlistener-docket-tracker` (for similar cases against this landlord)
3. Plain-English analysis of lease terms

## Output format

### For single-skill questions
Just delegate — run the skill and return its output directly.

### For multi-skill orchestration

```
🎯 ANALYZING YOUR QUESTION

I'm pulling data from [N] specialist sources:
  ✓ SEC EDGAR for insider/institutional activity
  ✓ ClinicalTrials.gov for pipeline
  ✓ FDA openFDA for safety signals
  ✓ NIH RePORTER for research tailwinds

═══════════════════════════════════════════════════════════

TL;DR: [one-line answer]

THE FULL PICTURE:

[synthesis of all skills' outputs in a narrative]

WHAT TO DO:

[actionable next steps]

WHAT I'M NOT CERTAIN ABOUT:

[limitations + uncertainties]

═══════════════════════════════════════════════════════════

⚠️  This is information, not professional advice. For high-stakes
    decisions, consult a licensed [doctor / lawyer / CFP / specialist].
```

## Why this is the $1B product

### Market size

| Audience | Size | Willingness to pay |
|----------|------|--------------------|
| Health-anxious Americans | ~50M | $20/mo |
| Retail investors | ~30M | $20/mo |
| Renters + first-time home buyers | ~60M | $15/mo |
| Used car buyers annually | ~40M | One-time $10 |
| Rare disease families | ~30M | $30/mo (high need) |

**Combined addressable: ~200M US adults** + international expansion

### Unit economics

- Free tier: 10 queries/month (Claude-paid)
- **Premium**: $20/month unlimited
- **Family**: $50/month for 4 users + shared profile
- **Medical Family Navigator**: $40/month (caregiver-focused with rare disease support)

### Path to $1B ARR

- **Year 1**: 100k free users + 10k paid = $2.4M ARR
- **Year 2**: 1M free + 100k paid = $24M ARR
- **Year 3**: 5M free + 500k paid = $120M ARR
- **Year 4**: 15M free + 2M paid = $480M ARR
- **Year 5**: 30M free + 4M paid = $960M ARR (cross $1B)

Comparable companies at $1B+ revenue with similar model:
- **GoodRx**: $1.6B revenue (drug price discovery)
- **BetterHelp (Teladoc)**: $1B+ revenue (digital health)
- **Rocket Mortgage**: $4B revenue (consumer finance guidance)
- **Credit Karma**: $1.2B revenue (free financial product)

### Why this can be bigger than any of them

GoodRx does ONE thing (drug prices). We do 27 things.
BetterHelp does ONE thing (therapy). We do 27 things.
Credit Karma does ONE thing (credit monitoring). We do 27 things.

**The consumer moat is the DEPTH of things we can answer well from the ONE interface.**

## Business moat

1. **Open-source skill infrastructure** = free community contributions to new data sources
2. **Claude inference cost dropping 60%/year** = unit economics improve over time
3. **First-mover in Claude Skills marketplace** for consumer vertical
4. **Multi-skill orchestration** = harder to replicate than single-purpose competitor
5. **Free tier drives massive funnel** = Credit Karma played this book; $7B outcome

## Distribution strategy

1. **Free product drives virality** — free skills + landing page
2. **Patient advocacy groups** — NORD (rare diseases), Cancer Support Community, ALS Association partner referrals
3. **Indie financial content creators** — free affiliate program
4. **Hacker News / Product Hunt** — launch the orchestrator with killer demo
5. **TikTok** — "here's the AI that saved my mom's life by finding a trial"

## Example invocation

User: "My son has Duchenne muscular dystrophy — what do we need to know?"

Navigator should:

1. Detect: medical + specific rare disease
2. Route to:
   - `rare-disease-detective` → confirm pattern
   - `patient-trial-navigator` → current DMD trials
   - `drug-affordability-rescue` → Elevidys, Viltepso, Exondys 51 assistance programs
   - `pubmed-paper-scan` → latest research
   - `clinical-trial-intel` → manufacturer pipeline (Sarepta, Pfizer, Regenxbio)
   - `nih-grant-scan` → DMD research funding
   - `ma-target-scanner` (if asked about investment) → DMD sector M&A candidates

3. Synthesize a comprehensive DMD family navigation guide:
   ```
   🎯 DMD FAMILY NAVIGATION PLAN

   Immediate steps (this week):
   1. Confirmed diagnosis via MLPA + sequencing at a pediatric neuromuscular center
   2. Parent Project Muscular Dystrophy (parentprojectmd.org) — free care coordinator
   3. Begin steroid therapy if age-appropriate (gold standard of care)

   Active trials your son could enroll in:
   - NCT04626674 Elevidys gene therapy post-approval registry (age 4-9)
   - NCT05091023 EDG-5506 Phase 3 (ambulatory patients)

   Drug affordability:
   - Elevidys retail price: $3.2M (yes, million). Sarepta has PAP — 100%
     coverage for qualifying patients on private insurance.
   - Viltepso (exon 53): ~$1M/year. Sarepta PAP available.

   Specialist: Pediatric neurologist with neuromuscular specialty. Parent
   Project MD maintains a list of certified care centers.

   Long-term expectations: With modern care (steroids + exon-skipping or gene
   therapy), current prognosis is dramatically better than 10 years ago.
   Many boys now ambulate into their 20s and live into their 40s+.
   ```

## What this skill IS NOT

- ❌ A replacement for doctors, lawyers, or financial advisors
- ❌ A diagnostic tool
- ❌ Investment advice
- ❌ Legal advice in any formal sense

## What this skill IS

- ✅ The smartest research assistant most people will ever have
- ✅ Free access to institutional-grade public data
- ✅ A routing layer that finds the right specialist skill
- ✅ The foundation of a $1B consumer product

## Relationship to AlphaSkills portfolio

This is the ROOT skill. It invokes all 27 specialist skills through the `alphaskills_py` Python library. Without it, users have to know which skill to call. With it, they just ask their question.

## License + source

MIT. Uses only free public APIs. This skill is free forever. The $1B comes from the consumer-product layer built ON TOP of this skill (subscription, premium features, white-labeled enterprise offerings).
