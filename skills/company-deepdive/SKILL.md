---
name: company-deepdive
description: Runs a full multi-source intelligence dossier for any US public company — combining SEC filings (insider trades, material events, financials, activist campaigns, institutional holdings), clinical trials (if biotech), patent filings, hiring signals, and arXiv papers when the company is AI-adjacent. Use when the user asks for a "complete picture" of a company, needs due diligence before investing, wants a competitive analysis, asks "tell me everything about X", needs a pre-M&A research package, or prepares for a call/meeting about a specific ticker. This is the grand orchestration skill that invokes sec-insider-scan, hedge-fund-holdings, activist-campaign-tracker, clinical-trial-intel, stock-signal-report, and nih-grant-scan in sequence, then synthesizes one unified narrative report. Replaces Bloomberg Terminal ($25-35k/yr), Capital IQ ($10-20k/yr), and FactSet ($12k+/yr) for core institutional-quality company research.
---

# Company Deep-Dive — The Master Skill

The orchestration skill. User asks about a company → full 360° dossier across every data source.

## When to invoke

Trigger on any full-research request:

- "Tell me everything about Moderna"
- "Complete picture of NVDA"
- "Due diligence on Tesla"
- "Full research report on PFE"
- "What do I need to know about $MRNA before investing?"
- "Prep me for my call about AAPL"
- "Is biotech X a buy?"

## Required input

- **Ticker** (one US-listed symbol)
- **Optional depth** — `quick` (10 min of pulls), `standard` (default), `comprehensive` (all sources, slower)

## Orchestration flow

For each ticker, run these sub-skills in sequence:

1. **`stock-signal-report`** — the headline bull/bear signal with reasons
2. **`sec-insider-scan`** — last 180 days of insider trading detail
3. **`hedge-fund-holdings`** (reverse lookup) — which major 13F filers hold significant positions in this ticker
4. **`activist-campaign-tracker`** (reverse lookup) — any recent 13D/G filings against this company
5. **(If biotech) `clinical-trial-intel`** — pipeline by sponsor lookup
6. **(If biotech / academic) `nih-grant-scan`** — related NIH grants (by academic collaborators if known)
7. **(If AI company) `arxiv-paper-scan`** — recent papers by employees

"Biotech" is detected when SIC code is in {2834, 2835, 2836, 8731} (pharmaceutical / biological / commercial research).
"AI company" is detected when SIC is 7372/7379 AND the name/description contains "AI" or "machine learning" — or when the user explicitly flags it.

## Output format

A structured narrative dossier (not a bullet dump). Five parts:

### 1. Executive signal (1 paragraph)
The TL;DR. One paragraph covering: current signal (bullish/bearish/neutral), strongest contributing factor, and one key thing the user should be watching.

### 2. Insider + institutional positioning (2-3 paragraphs)
- Who's been buying or selling inside the company (Form 4)
- Which major hedge funds hold the stock (13F reverse lookup)
- Any activists building a position (13D reverse lookup)

### 3. Pipeline / business events (2-3 paragraphs)
- Recent 8-K material events decoded
- (Biotech only) Key Phase 2/3 trials with readout dates
- (If relevant) Hiring signals indicating expansion or contraction

### 4. Research / IP signals (1-2 paragraphs)
- (Biotech) Related NIH grants (academic collaborators)
- (AI) Recent papers by employees
- (General) Any notable patent activity

### 5. Risks + catalysts (bullet list)
- Upcoming events that could move the stock
- Red flags (exec departures, SEC inquiries, litigation)

## Example invocation

User: "Tell me everything about MRNA (Moderna)"

The skill should:

1. **stock-signal-report** → MRNA signal
2. **sec-insider-scan** → who's trading MRNA inside
3. **hedge-fund-holdings (reverse)** → Baker Bros, Citadel, RA Capital positions in MRNA
4. **activist-campaign-tracker (reverse)** → no 13D activity recently
5. Detect biotech (SIC 2836 = Biological Products) → trigger biotech modules
6. **clinical-trial-intel** → Moderna's pipeline (flu, RSV, CMV vaccines, oncology mRNA)
7. **nih-grant-scan** → related academic grants on mRNA therapeutics

Return a narrative dossier:

```
# Moderna Inc (MRNA) — Deep Dive, April 2026

## Executive signal
MRNA is in a transitional phase post-COVID. Signal: NEUTRAL (score 0). Insider activity is muted — the CEO and CFO have been neither buying nor selling meaningfully, which typically precedes a major catalyst decision. The most important thing to watch is the FY2026 flu/RSV vaccine approval decisions and whether the oncology pipeline produces its first Phase 3 readout in H2 2026.

## Insider + institutional positioning
Moderna insider activity has been quiet over the last 90 days — 3 executive option exercises totaling $2.1M, all at or near market price, suggesting routine compensation mechanics rather than conviction trades. Major institutional holders include Baker Bros Advisors (biotech-focused fund, 8.2M shares, one of their top-10 positions), Vanguard, and BlackRock. No activist 13D filings against MRNA in the last 2 years.

## Pipeline / business events
Recent 8-K filings show:
- 2026-03-18 (Item 8.01): mRNA-1010 flu vaccine Phase 3 primary endpoint met in interim analysis — bullish
- 2026-02-05 (Item 2.02): Q4 2025 earnings — revenue $1.4B, down 45% YoY as COVID demand rolls off
- 2025-11-12 (Item 1.01): License agreement with Merck for certain oncology antigens

Pipeline (Phase 2/3):
- mRNA-1010 (flu): Phase 3 met endpoint, FDA filing expected Q3 2026
- mRNA-1345 (RSV): approved 2024 as mRESVIA
- mRNA-1647 (CMV): Phase 3 running, 7,500 patients, primary completion mid-2027
- mRNA-4157 (personalized cancer vaccine w/ Merck): Phase 3 melanoma, Phase 2 NSCLC

## Research / IP signals
Related NIH grants on mRNA therapeutics include several at Penn (Katalin Karikó's former lab collaborators), MIT's Koch Institute, and Moderna Therapeutics itself (which receives SBIR phase 2 awards for various indications). This keeps the mRNA platform's academic pipeline well-funded regardless of Moderna's commercial trajectory.

## Risks + catalysts
• +++ mRNA-1010 FDA approval (Q3 2026)
• ++ mRNA-4157 / Merck oncology Phase 3 data (H2 2026)
• -- COVID booster demand collapse continues (already priced in)
• -- Cash burn — $3.5B cash reserve, ~$2B/year burn
• Risk: no clear bridge from COVID revenue to next-gen pipeline revenue before 2027
```

## Honest caveats (always append)

- This dossier uses publicly available data. Material non-public information is not included (and shouldn't be — that's illegal insider trading territory)
- Signal rules are heuristic, not a trained model
- Company analysis is NOT a recommendation to buy or sell
- Always consult a licensed financial advisor before trading

## Relationship to AlphaStack portfolio

This is the grand orchestration skill. It doesn't have a single corresponding Apify actor — it coordinates several. For programmatic bulk deep-dives, use the actors in a chain: `stock-alpha-aggregator` + `sec-13f-holdings-tracker` (reverse query) + `sec-13d-activist-filings` (reverse query) + `clinicaltrials-pipeline-monitor` (by sponsor) + `nih-grants-tracker` (by organization).
