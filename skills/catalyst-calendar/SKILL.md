---
name: catalyst-calendar
description: Generates a unified forward-looking stock catalyst calendar for any ticker or watchlist — combining scheduled earnings dates, FDA PDUFA / AdCom dates, clinical trial primary completion dates, SEC comment-period deadlines, ex-dividend dates, 13F filing deadlines, CFTC release dates, patent expirations, and macroeconomic release dates (Fed meetings, CPI, jobs report, GDP). Use when the user asks "what catalysts are coming up for X stock", wants a next-30-day calendar for their watchlist, asks about upcoming FDA decisions, needs a trade planning calendar, or wants to know when a specific drug's PDUFA date is. The single most-requested tool in institutional investing — no free version exists. Replaces Wall Street Horizon ($5k+/yr), Bloomberg CALE function ($25k/yr), and Koyfin Pro ($30/mo). Combines SEC EDGAR + ClinicalTrials.gov + FDA + FRED + Federal Register APIs for a synthesis no single tool provides.
---

# Catalyst Calendar — The One Thing Every Trader Asks For

## When to invoke

This is the #1 most-requested tool in institutional investing. Trigger on:

- "What catalysts are coming up for NVDA?"
- "FDA dates in the next 30 days"
- "Upcoming earnings I should watch"
- "Forward calendar for my biotech watchlist"
- "When is Moderna's next PDUFA?"
- "Big macro events next week?"

## Required input

- **Tickers** — list of US tickers to track
- **Window** — forward-looking days (default: 30, max: 365)
- **Optional filter** — `all` (default), `earnings`, `fda`, `clinical`, `sec`, `macro`

## Output format: a unified calendar

A chronological list with **color-coded event types**:

```
📅 CATALYST CALENDAR — {tickers joined} — next {N} days ({start} → {end})

│ 2026-04-22  │ 📊 EARNINGS      │ TSLA    │ Q1 2026 earnings call, after close
│ 2026-04-23  │ 🏦 MACRO         │ —       │ Fed FOMC minutes release, 2pm ET
│ 2026-04-25  │ 💊 FDA PDUFA     │ MRNA    │ mRNA-1010 flu vaccine PDUFA date
│ 2026-04-29  │ 🧪 CLINICAL      │ LLY     │ Donanemab Phase 3 TRAILBLAZER-ALZ 3 primary completion
│ 2026-05-02  │ 📊 EARNINGS      │ AAPL    │ Q2 2026 earnings call, after close
│ 2026-05-03  │ 🏦 MACRO         │ —       │ April Jobs Report, 8:30am ET
│ 2026-05-07  │ 📜 SEC DEADLINE  │ —       │ Proposed SEC rule on digital asset custody comment period closes
│ 2026-05-15  │ 💰 13F DEADLINE  │ —       │ Q1 2026 13F-HR filings due from all institutional investors >$100M
│ 2026-05-16  │ 💊 FDA ADCOM     │ SRPT    │ SRP-9003 AdCom vote on gene therapy for DMD
│ 2026-05-19  │ 💵 EX-DIV        │ AAPL    │ Ex-dividend date for Q2 declared quarterly dividend
│ 2026-05-23  │ 🧪 CLINICAL      │ MRNA    │ mRNA-4157 personalized cancer vaccine P3 primary completion
```

## Event categories + data sources

### 📊 Earnings dates
- **Source**: SEC EDGAR 10-Q / 10-K historical cadence + company investor relations pages
- **Logic**: Companies file 10-Q within ~45 days of quarter end and 10-K within ~60-90 days of fiscal year end. Forward earnings are usually announced 30-45 days ahead via 8-K Item 2.02.
- **Procedure**: Pull company's historical quarterly filing cadence; predict next date using median delta. Cross-reference with any recent 8-K announcing the next earnings call.

### 💊 FDA PDUFA + Advisory Committee dates
- **Source**: openFDA + FDA.gov calendar scrape (no official API for forward dates)
- **Logic**: When a company announces a PDUFA date, it appears in the SEC 8-K Item 8.01 disclosure and the FDA's posted calendar. Track both.
- **Procedure**: Scan recent 8-K filings for "PDUFA" mentions; cross-reference with FDA AdCom calendar; flag the ones within the user's window.

### 🧪 Clinical trial primary completion dates
- **Source**: ClinicalTrials.gov API (`primaryCompletionDateStruct`)
- **Logic**: Trial sponsors self-report primary completion dates. When `primaryCompletionDateType === "ANTICIPATED"`, these are catalysts — binary events that move biotech stocks 30-80%.
- **Procedure**: Query ClinicalTrials.gov for trials where `leadSponsor.name` matches the ticker's company name OR where the trial was referenced in a recent 8-K. Filter `primaryCompletionDate` to the window.

### 🏦 Macro releases
- **Fed FOMC**: 8 meetings per year, calendar published on federalreserve.gov
- **CPI**: BLS releases around the 2nd week of each month
- **Jobs report**: BLS releases first Friday of each month at 8:30am ET
- **GDP**: BEA releases advance estimate ~1 month after quarter end, then 2 revisions
- **Fed minutes**: 3 weeks after each FOMC meeting
- **Source**: FRED + BLS + BEA published release calendars

### 📜 SEC rule comment deadlines
- **Source**: Federal Register API — proposed rules with `comments_close_on` in window
- **Logic**: When SEC proposes a new rule, the final rule typically follows within 3-6 months after the comment period closes. These are systemic catalysts (affecting many stocks).

### 💰 13F filing deadlines
- **Hardcoded calendar**: Feb 14, May 15, Aug 14, Nov 14 of each year are the 13F-HR deadlines (45 days after quarter end). Universal across all institutional investors.

### 💵 Dividend dates + stock splits
- **Source**: SEC 8-K filings (dividend declarations filed under Item 8.01); also listed in company IR pages
- **Logic**: Ex-dividend date is typically 1 business day before record date, which is typically ~2 weeks after declaration.

### ⚖️ Patent expiration dates (for biotech)
- **Source**: USPTO patent database (manual lookup required)
- **Logic**: Drug patents expire 20 years from filing. When a blockbuster drug's patent expires, generics enter and the branded company's revenue drops 50-90%.

## The integrated procedure

For each ticker the user passes:

1. **Resolve ticker → CIK** (SEC mapping)
2. **Detect industry** via SIC code:
   - `2834`, `2835`, `2836`, `8731` → biotech/pharma → add FDA + clinical events
   - `6020`, `6022`, `6199` → financial → add Fed + 13F events
   - Other → earnings + macro only
3. **Pull upcoming events from each relevant source in parallel**:
   - SEC recent 8-K filings for earnings announcements, dividend declarations, PDUFA disclosures
   - ClinicalTrials.gov for trials sponsored by or involving this company (if biotech)
   - Federal Register for SEC/FDA proposed rules with open comment periods that affect this industry
4. **Merge + sort** by date ascending
5. **Add macro events** always (Fed meetings, CPI, jobs, GDP release calendar)
6. **Render** the calendar table

## Honest caveats

- **Forward-looking dates are estimates.** Companies reschedule earnings. FDA extends PDUFA dates. Clinical trials slip.
- **No single API has all this data** — we synthesize across 5-7 sources and the quality varies.
- **FDA PDUFA dates** are only known when the company discloses them — for early-stage biotechs they may not be public until after NDA submission.
- **Earnings dates for the next quarter** are sometimes not yet announced; we use historical cadence as a predictor.

## Example invocation

User: "What catalysts are coming up for MRNA, LLY, and NVDA in the next 60 days?"

The skill should:

1. Identify MRNA (2836), LLY (2834) as biotech → pull FDA + clinical
2. Identify NVDA (3674) as semiconductors → just earnings + macro
3. Pull relevant data from all sources in the 60-day window
4. Return:
   ```
   📅 CATALYST CALENDAR — MRNA, LLY, NVDA — next 60 days (2026-04-17 → 2026-06-16)

   │ 2026-04-23  │ 🏦 MACRO        │ —       │ Fed FOMC minutes release
   │ 2026-04-25  │ 💊 FDA PDUFA    │ MRNA    │ mRNA-1010 flu vaccine PDUFA decision 
   │ 2026-05-02  │ 📊 EARNINGS     │ LLY     │ Q1 2026 earnings call, before open
   │ 2026-05-03  │ 🏦 MACRO        │ —       │ April Jobs Report
   │ 2026-05-06  │ 📊 EARNINGS     │ MRNA    │ Q1 2026 earnings call, before open
   │ 2026-05-13  │ 🏦 MACRO        │ —       │ April CPI release
   │ 2026-05-15  │ 💰 13F DEADLINE │ —       │ Q1 2026 13F-HR filings deadline
   │ 2026-05-21  │ 📊 EARNINGS     │ NVDA    │ Q1 FY27 earnings call, after close
   │ 2026-05-23  │ 🧪 CLINICAL     │ MRNA    │ mRNA-4157 personalized cancer vax P3 primary completion (est.)
   │ 2026-06-03  │ 🧪 CLINICAL     │ LLY     │ Olomorasib Phase 3 CRC arm primary completion (est.)
   │ 2026-06-11  │ 💊 FDA ADCOM    │ LLY     │ Tirzepatide label expansion AdCom (cardiac outcomes)

   Highest-impact events:
   🔴 MRNA PDUFA April 25 — binary event, drug either gets approved or doesn't. Historical MRNA PDUFA moves: ±15-30% on decision day.
   🟡 LLY AdCom June 11 — tirzepatide label expansion = bigger TAM if approved
   🟡 NVDA earnings May 21 — historically moves ±8% on earnings day
   ```

## Why this is the killer skill

There's no free tool that does this. Traders cobble together:
- Earnings calendar from Nasdaq.com / Yahoo Finance (partial)
- FDA calendar from BiopharmaCatalyst ($200/yr)
- Clinical trial dates from BioPharma Dive (manual)
- Macro dates from their brokerage
- SEC deadlines from their calendar app

This skill combines all of it in one invocation. **For ANY ticker. For ANY window.** Free.

## Related skills used as sub-components

- `sec-insider-scan` — recent 8-K Item 2.02 for earnings announcements
- `clinical-trial-intel` — primary completion dates
- `fda-drug-recalls-faers` — PDUFA disclosures from openFDA
- `fred-economic-data` — release calendar for macro data
- `federal-register-tracker` — SEC/FDA proposed rule comment deadlines
