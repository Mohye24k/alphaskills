# AlphaStack — The Billion-Dollar Consumer Product Plan

**One sentence pitch:** AlphaStack is the first AI assistant that gives every person free access to institutional-grade life navigation — health, finance, legal, consumer — replacing the $500/hour professionals most people can't afford.

## The pattern

| Company | Does ONE thing | Revenue (recent) |
|---------|----------------|------------------|
| GoodRx | Drug prices | $1.6B/year |
| Credit Karma | Credit scores + offers | $1.2B/year |
| BetterHelp (Teladoc) | Digital therapy | $1B+/year |
| Rocket Mortgage | Mortgage decisions | $4B/year |
| Zillow | Home prices | $2B/year |
| LegalZoom | Business legal forms | $700M/year |

**All of these are multi-billion public companies.** Each one does EXACTLY ONE consumer-facing thing really well.

**AlphaStack does all of them from one interface**, powered by Claude + 27 specialist AlphaSkills + the free public government APIs (SEC EDGAR, NIH, FDA, NHTSA, FRED, CFTC, ClinicalTrials.gov, etc.) that incumbents monetize through opacity.

## Product tiers

### 🆓 Free Tier — "AlphaStack Basic"
- 15 life questions per month
- Access to all 27 skills
- Standard response speed
- Community support
- **Monetized via**: ad-free; revenue comes from the paid tier funnel

### 💎 AlphaStack Premium — $19/month or $199/year
- Unlimited questions
- Priority Claude model (faster + deeper responses)
- Email alerts (earnings catalysts, FDA approvals of drugs you take, recalls on your car)
- Save + organize reports
- PDF export for sharing with professionals
- **Target:** retail investors + health-conscious adults

### 👨‍👩‍👧 AlphaStack Family — $39/month
- Everything in Premium
- 4 user accounts + shared profile
- Prescription tracker for household
- Combined health + finance dashboard
- **Target:** families with aging parents or chronic conditions

### 🏥 AlphaStack Rare Disease Navigator — $49/month
- Everything in Family
- Dedicated rare disease specialist skill access
- Monthly 1:1 video with an AI care navigator
- Priority support line
- Partnerships with NORD, PPMD, MitoAction
- **Target:** ~30M US rare disease families

### 🏢 AlphaStack Business — $299-999/month
- 10-100 user seats
- Private deployment option
- White-label for advisors/clinics
- Custom skill integrations
- **Target:** small law firms, medical practices, financial advisors

## Path to $1B ARR (5-year model)

| Year | Free users | Paid users | Blended ARPU | ARR |
|------|-----------:|-----------:|-------------:|----:|
| Y1 | 100k | 5k | $15/mo | $0.9M |
| Y2 | 1M | 50k | $17/mo | $10.2M |
| Y3 | 5M | 400k | $19/mo | $91M |
| Y4 | 15M | 1.5M | $20/mo | $360M |
| Y5 | **30M** | **4M** | **$21/mo** | **$1.01B** |

### Comparable conversion rates

- Credit Karma: ~5% free → monetized
- GoodRx: not a typical conversion funnel; revenue from pharma advertisers + affiliate
- BetterHelp: ~8% free tier → paid (via trial conversion)

**Modeled AlphaStack conversion: 10% in mature years** (aggressive but justified by real life-or-death use cases like rare disease + cancer trial navigation).

## Year 1 go-to-market (how we actually start)

### Month 1-2: Build + launch
- [ ] Ship AlphaStack consumer-facing web app (wraps AlphaSkills)
- [ ] Launch at alphastack.ai (or .life, .health)
- [ ] Post to Hacker News, Product Hunt, Indie Hackers
- [ ] Free tier only; focus on adoption

### Month 3-4: Patient advocacy partnerships
- [ ] Partner with NORD (rare diseases)
- [ ] Partner with Cancer Support Community
- [ ] Partner with Parent Project Muscular Dystrophy
- [ ] Free dedicated navigators for their members — we get case studies and testimonials

### Month 5-6: Financial creator partnerships
- [ ] Partner with finance YouTubers (Graham Stephan, Meet Kevin, Andrei Jikh)
- [ ] Partner with investing podcasts (Invest Like the Best, We Study Billionaires)
- [ ] Affiliate program with 30% rev share for first-year subscriptions

### Month 7-9: Launch paid tier
- [ ] Premium tier live
- [ ] Pricing experiments
- [ ] Email marketing funnel
- [ ] Target: 5k paying users by end of Month 12

### Month 10-12: Enterprise sales
- [ ] Start business tier with 5-10 pilot customers
- [ ] SOC 2 compliance
- [ ] Target: 5 paying enterprise customers by end of Year 1

## Competitive landscape

| Competitor | Where they're strong | Where we beat them |
|-----------|---------------------|---------------------|
| **GoodRx** | Drug prices | We add medical context + trials + alternatives |
| **Credit Karma** | Credit scores | We add finance + macro + SEC intelligence |
| **BetterHelp** | Therapy | Different category; we don't compete |
| **Legal Zoom** | Form templates | We add actual legal research + case lookup |
| **WebMD / Mayo** | Symptom lookup | We add trials + drug affordability + specialist identification |
| **Morningstar** | Stock research | We add insider + 13F + activist + catalysts + free |
| **Bloomberg Terminal** | Institutional finance | Completely different market; not a consumer product |
| **ChatGPT / Claude direct** | General AI | Users paying $20/mo for Claude don't get skill-level depth + specialized knowledge |

**The moat**: Claude Pro gives you ChatGPT-like conversation. AlphaStack Premium gives you Claude Pro **PLUS** 27 specialized skills **PLUS** ongoing email alerts **PLUS** curated professional partnerships **PLUS** a polished consumer interface.

## Revenue model deep-dive

### Primary: Subscription

As modeled above. The core driver.

### Secondary: Affiliate referrals

When AlphaStack recommends:
- A clinical trial → patient advocacy group gets 0% (free always)
- A drug PAP → pharmacy savings card affiliate (~$2-5 per enrollment)
- A mortgage → licensed mortgage broker referral ($50-500 per funded loan)
- A financial advisor → fiduciary advisor partnership (annual fee share)
- A legal service → legal service affiliate

**Projected affiliate revenue at 1M paid users: ~$5/user/year = $5M/year** (on top of subscription)

### Tertiary: White-label + enterprise

- Medical practices: $299-999/month
- Financial advisory firms: $499-1499/month
- Law firms: $299-799/month
- Pharma medical affairs teams: $10-50k/year enterprise contracts

**Projected enterprise at 500 customers avg $800/mo: ~$5M/year**

### Tertiary: Data product (optional)

Aggregated anonymized query data about "what are Americans worried about right now" would be valuable to:
- Insurance companies ($100k-1M/year per contract)
- Pharma trend research ($50-500k/year)
- Political campaigns / polling companies ($100k-500k/year)
- Media companies ($100k/year subscription)

**This is optional and ONLY if it can be done without violating user privacy.** Requires opt-in + aggregation above safe-harbor thresholds.

## Capital requirements

### Bootstrap phase (Months 1-6)

- Developer time: 1 person (founder)
- Infrastructure: ~$500/month (Vercel/Railway + Claude API + Postgres)
- Legal: ~$2,000 (LLC + basic ToS/privacy)
- Marketing: ~$1,000
- **Total: ~$10,000 over 6 months**

### Seed round (if taken; Month 6-12)

- Raise $500k-$1M from pre-seed
- Use for: 1-2 additional engineers + designer + paid marketing
- At 50k MAU + 5k paid → valuation ~$10-25M

### Series A (Month 18-24)

- Raise $5-15M
- At 500k MAU + 50k paid + $10M ARR
- Valuation: $75-150M
- Use for: team of 15-25, clinical partnerships, enterprise sales

### Series B (Year 3)

- Raise $50-100M
- At 5M MAU + 500k paid + $100M ARR
- Valuation: $750M - $1.5B

### Go public / acquisition (Year 5)

- $1B ARR at 10-15x multiple = $10-15B valuation
- OR strategic acquirer: Google, Salesforce, Thomson Reuters, Anthropic themselves

## Risk + mitigation

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| Claude API pricing increases | Medium | Cache common queries; build Claude Pro-native version that uses user's own quota |
| OpenAI / Google / Anthropic launches directly competing consumer product | High | We've already started and have 27 specialized skills — focus on depth moat |
| Regulatory action on medical/legal disclaimers | Medium | Strong disclaimers; don't give advice, provide information |
| Claude Skills ecosystem doesn't mature | Low | Skills already open standard (Anthropic+OpenAI); user-owned |
| Privacy-sensitive data handling | Medium | Zero retention of query content option; HIPAA-level controls for medical vertical |
| Public API changes (SEC EDGAR, NIH, etc.) | Low | All APIs are government-owned and stable 20+ years |

## Success metrics (milestones)

- [ ] Month 3: 5k free users
- [ ] Month 6: 50k free users + launch paid tier
- [ ] Month 9: 500 paying users = $10k MRR
- [ ] Month 12: 5k paying users = $100k MRR
- [ ] Year 2: 50k paying = $1M MRR
- [ ] Year 3: 500k paying = $10M MRR
- [ ] Year 5: 4M paying = $80M MRR ≈ **$1B ARR**

## Why this succeeds when others don't

1. **The underlying data is FREE** — SEC, NIH, FDA, CFTC, NHTSA APIs are US government public domain. No vendor lock-in. No data costs compound.
2. **The orchestration layer (skills) is OPEN SOURCE** — anyone can contribute. We grow the skill library through community, not headcount.
3. **LLM costs are DROPPING 60%/year** — Claude inference costs 40% of what they did 18 months ago. Unit economics improve mechanically.
4. **The audience is INEVITABLE** — everyone will use AI for life decisions. The question is only WHICH AI they use.
5. **The emotional moat is REAL** — when someone uses this and it helps their mom's cancer treatment or finds a trial for their kid, they become evangelists.

## The specific first step (this week)

1. Deploy the alphastack-landing page
2. Push alphaskills GitHub repo (all 28 skills + Python library)
3. Post to Hacker News as "Show HN: 28 Claude Skills to replace Bloomberg Terminal + Citeline + ActivistInsight + LegalZoom + GoodRx"
4. Set up AlphaStack.ai domain and redirect to GitHub for now
5. Start building the consumer web app wrapper

**Total cost of step 1: $0 (everything is built or free-tier hostable).**

This is the single highest-ROI move in the entire AlphaStack family.
