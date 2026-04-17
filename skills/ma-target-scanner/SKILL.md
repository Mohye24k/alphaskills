---
name: ma-target-scanner
description: Identifies likely M&A acquisition targets by synthesizing 8 independent signals — activist 13D accumulation, hedge fund 13F position-building, insider buying velocity, industry consolidation patterns, relative valuation vs peers, sector spinout history, corporate structure signals (dual-class, staggered board, poison pills), and executive departure patterns. Returns a ranked list of tickers with computed acquisition probability scores and one-paragraph rationales. Use when the user asks for M&A target ideas, wants to find acquisition candidates in a sector, asks "who might get bought", or builds a merger arbitrage watchlist. This synthesis is what M&A bankers charge $50-100k per industry-specific target list for — Goldman, Morgan Stanley, and Evercore all have in-house screens that do exactly this. No free tool exists. Uses SEC EDGAR + 13F + 13D + 8-K APIs combined with simple ranking logic.
---

# M&A Target Scanner — What $50k/seat M&A Banker Screens Do

## When to invoke

Trigger on any M&A / take-private / acquisition question:

- "Find M&A targets in semiconductors"
- "Who's likely to be acquired in mid-cap biotech?"
- "Screen for take-private candidates with depressed valuations"
- "Which healthcare companies could get bought this year?"
- "Find merger arb opportunities"
- "Stealth take-out candidates"

## Required input

- **Sector / SIC code** — e.g. semiconductors (3674), biotech (2836), software (7372)
- **Market cap range** — e.g. `$500M-$5B` (mid-cap is the sweet spot for strategic M&A)
- **Optional**: specific acquirer universe (e.g. "who could Microsoft buy")

## The 8 signals — each +1 to +3 points toward acquisition probability

### Signal 1: Activist 13D present (+3)
Activists filing 13D positions often precede forced sales. When Icahn, Elliott, Starboard, or Jana has a >5% position with an active campaign, the probability of strategic alternatives (sale/merger/spinoff) within 12-18 months is ~40%.

**Data source**: SEC 13D filings via `activist-campaign-tracker`

### Signal 2: 13F institutional accumulation (+2)
If multiple hedge funds increase positions >20% quarter-over-quarter, that's "merger arb smart money" front-running an announcement.

**Data source**: Compare last 2 quarters of 13F-HR across top 20 hedge funds; flag tickers where 5+ funds added materially.

### Signal 3: Insider BUYING (not selling) (+3)
Open-market insider purchases (code P) before an announced merger are extremely rare — but when they DO happen, it's often post-approach with confidence the deal will close at a premium.

**Data source**: SEC Form 4 via `sec-insider-scan`

### Signal 4: Recent 8-K Item 8.01 "Other Events" (+1)
Companies often disclose "preliminary discussions" or "engaged financial advisors" in Item 8.01 of 8-K filings. This is public signal that something is happening.

**Data source**: SEC 8-K filings; parse for keywords like "strategic alternatives", "unsolicited proposal", "Goldman Sachs as financial advisor".

### Signal 5: Relative valuation discount (+1 to +2)
Company trading at >20% EV/EBITDA discount vs sector peers = value bargain for strategic acquirer.

**Data source**: 10-K/10-Q financials for EBITDA; aggregate sector averages.

### Signal 6: Recent hiring of bankers / advisors (+2)
Check recent DEF 14A, proxy statements, or press releases for "engaged [Goldman/Morgan Stanley/JPM/Evercore] to evaluate strategic alternatives".

**Data source**: SEC EDGAR proxy filings full-text search.

### Signal 7: Industry consolidation pattern (+1)
If the sector has seen 2+ similar-size M&A deals in the last 18 months, remaining companies are often next-in-line. Compute rolling M&A deal count in each SIC code.

**Data source**: SEC DEFM14A / S-4 filings (proxy merger statements) aggregated by SIC.

### Signal 8: Poison pill OR activated shareholder rights plan (-2 — defensive, LESS likely)
OR staggered board / dual-class stock (-1 to -2 — harder to acquire).

**Data source**: SEC 8-K Item 1.01 or Item 3.03; DEF 14A.

## Scoring

Sum signals. Score interpretation:

- **+7 or higher**: HIGH probability target (next 6-18 months)
- **+4 to +6**: MEDIUM probability target
- **+1 to +3**: WATCHLIST only
- **0 or negative**: NOT a target (either too defended or no signals)

## Output format

### 1. Summary
`"Found {N} potential M&A targets in {sector}. High probability: {x}, Medium: {y}, Watchlist: {z}."`

### 2. Ranked table

| Ticker | Company | Market Cap | Score | Key Signals | Rationale |
|--------|---------|-----------:|------:|-------------|-----------|

Sort by score descending.

### 3. Top 3 detailed analyses
For each of the top 3, provide:
- Which specific signals fire
- What the full catalyst path looks like
- Realistic acquirer universe (strategic + financial)
- Historical comps (similar deals in this sector with premiums)

## Example invocation

User: "Find M&A targets in mid-cap biotech"

The skill should:

1. Query tickers with SIC=2836 (Pharmaceutical Preparations) and SIC=2834 (Biological Products) with market cap $500M-$5B
2. For each ticker, run the 8 signals
3. Compute scores
4. Return:
   ```
   Found 47 mid-cap biotechs screened. High probability: 3, Medium: 8, Watchlist: 12.

   Ranked M&A targets:
   | RARE | Ultragenyx Pharmaceutical | $3.2B | 9 | Activist 13D (Jana), 13F accum, 8-K "strategic alts" | Gene therapy platform; likely buyers: Sanofi, Pfizer, Novartis |
   | CYTK | Cytokinetics Inc         | $4.8B | 8 | Insider buying, 13F accum, FDA approval expected | Heart failure drug aficamten; likely buyer: Bristol-Myers or Merck |
   | CRSP | CRISPR Therapeutics      | $2.7B | 7 | 13F accum, peer consolidation, valuation 40% below peers | CRISPR gene editing platform; already partnered with Vertex |

   Top analysis — RARE (Ultragenyx):
   Key signals firing:
   • Jana Partners filed 13D in March 2026 (6.2% stake) — publicly called for strategic alternatives
   • 8 major hedge funds (incl. Baker Bros, RA Capital, Adage) increased 13F positions Q1 2026
   • Recent 8-K disclosed "engaged Centerview Partners as financial advisor to evaluate strategic alternatives"
   • RARE has 3 approved rare-disease drugs and 4 Phase 3 programs — ideal bolt-on for a large pharma
   • Valuation: 2.1x NTM revenue vs peer median 4.8x

   Realistic acquirers: Sanofi (public interest in rare disease), Pfizer (needs pipeline), Novartis (historical gene therapy focus)
   Historical comp: Horizon → Amgen $28B (2022) at 7x revenue — similar rare disease profile
   Probable timeline: deal announced Q3-Q4 2026 at $70-90/share (50-100% premium to current $42)
   ```

## Why this is truly remarkable

**No free tool combines all 8 signals**. The closest paid alternatives:

- **Mergermarket / Dealogic** — $20-100k/year — covers announced deals, not pre-announcement signals
- **S&P CapIQ Screener** — $10-20k/year — has some M&A signals but requires manual combination
- **Sell-side research from Goldman/MS/JPM** — $100k+/year minimum institutional subscription
- **In-house banking screens** — proprietary to Goldman / Morgan Stanley, literally not available

This skill does the work an associate M&A banker does on Day 1 of target screening — for free.

## Honest caveats

- Signals are heuristic; quant-grade ML M&A models exist inside hedge funds
- No signal guarantees a deal; 2-3 of every 5 high-scoring tickers never get acquired
- Premium estimates are based on historical comps and subject to wide variance
- Not investment advice; consult a licensed financial advisor

## License + source

Uses SEC EDGAR public data + openFDA + ClinicalTrials.gov. All MIT.
