---
name: stock-signal-report
description: Generates a unified bull/bear signal report for any US public company ticker by combining three independent SEC signals — insider trading (Form 4), material events (8-K), and quarterly financials (10-Q/10-K) — with a computed BULLISH, NEUTRAL, or BEARISH score from -10 to +10. Use when the user asks "should I buy X", "is TSLA a buy or sell", "what's the SEC picture for NVDA", wants a second opinion before trading, needs institutional-quality analysis for a stock, or asks for a "full report" on any ticker. This is the flagship meta-skill combining sec-insider-scan + edgar-8k events + filing velocity analysis into one actionable output. Uses rule-based signal computation (not ML) following standard institutional heuristics. Replaces Bloomberg Terminal EVRY function ($25k/year) for basic insider + event analysis.
---

# Stock Alpha Signal Report

The flagship meta-skill. One ticker in → full SEC intelligence out with a scored signal.

## When to invoke

Trigger on any "should I buy/sell" or "full report" question:

- "Is NVDA a buy?"
- "Give me the full picture on TSLA"
- "Should I be worried about AAPL?"
- "Second opinion on my position in PFE"
- "What does the SEC say about X stock?"
- "Alpha signal for MRNA"

## Required input

- **Ticker** (one or more US-listed symbols)
- **Optional lookback window** in days (default: 90)

## Output format

A structured four-part report per ticker:

### 1. Headline signal (one line)
`"🎯 [TICKER] — [SIGNAL] (score {score})"`

Where SIGNAL is one of:
- `🟢🟢 STRONGLY_BULLISH` (score ≥ +4)
- `🟢 BULLISH` (score +1 to +3)
- `⚪ NEUTRAL` (score 0)
- `🔴 BEARISH` (score -1 to -3)
- `🔴🔴 STRONGLY_BEARISH` (score ≤ -4)

### 2. Signal reasons (bullet list)
Every scoring factor that contributed. Example:
- `+3: Net insider BUYS in window (3 open-market purchases)`
- `+2: Cluster buy — 4 distinct insiders bought`
- `-3: C-suite (CEO) selling $5M in last 30 days`
- `+1: 8-K Item 1.01 Material Agreement filed 2 weeks ago`
- `-3: 8-K Item 1.03 Bankruptcy/Receivership`

### 3. Insider activity summary
| Insider | Title | Code | Shares | Value | Date |
|---------|-------|------|-------:|------:|------|

### 4. Recent material events (8-K Item decoded)
| Date | Item | Meaning |
|------|------|---------|

## Signal scoring rules

Each rule applies once per ticker.

| Rule | Delta |
|------|------:|
| Net insider BUYING in window (code P buys > code S sells by count) | **+3** |
| Cluster buy — 3+ distinct insiders with code P | **+2** |
| High Form 4 filing velocity (≥5 filings in window) | **+1** |
| Net insider SELLING > $1M in window | **-3** |
| Cluster sell — 3+ distinct insiders with code S | **-2** |
| C-suite (CEO/CFO) selling any amount | **-1** |
| 8-K Item 1.01 (Material Agreement entered) | **+1** |
| 8-K Item 2.01 (Completion of Acquisition) | **+2** |
| 8-K Item 8.01 (Other Events — often positive PR) | **+1** |
| 8-K Item 1.03 (Bankruptcy/Receivership) | **-3** |
| 8-K Item 2.06 (Material Impairments) | **-2** |
| 8-K Item 3.01 (Notice of Delisting) | **-3** |
| 8-K Item 4.02 (Non-Reliance on Prior Financials) | **-2** |

## 8-K Item code reference

| Item | Description | Signal weight |
|------|-------------|--------------|
| 1.01 | Entry into Material Definitive Agreement | Bullish +1 |
| 1.02 | Termination of Material Definitive Agreement | Neutral |
| 1.03 | Bankruptcy or Receivership | Bearish -3 |
| 2.01 | Completion of Acquisition/Disposition | Bullish +2 |
| 2.02 | Results of Operations / Financial Condition (earnings) | Neutral, context-dependent |
| 2.03 | Creation of Direct Financial Obligation (debt) | Neutral |
| 2.05 | Costs Associated with Exit/Disposal | Bearish |
| 2.06 | Material Impairments | Bearish -2 |
| 3.01 | Notice of Delisting | Bearish -3 |
| 4.02 | Non-Reliance on Prior Financials (restatement) | Bearish -2 |
| 5.02 | Departure/Appointment of Directors/Officers | Context-dependent |
| 7.01 | Regulation FD Disclosure | Neutral (just a disclosure) |
| 8.01 | Other Events | Often bullish announcements |
| 9.01 | Financial Statements & Exhibits | Metadata only |

## Data pipeline

Call the sub-skills or use the SEC APIs directly:

1. Resolve ticker → CIK (cache the mapping)
2. Pull `data.sec.gov/submissions/CIK{cik}.json`
3. Filter filings by form type and date range
4. For each Form 4: download XML, parse non-derivative transactions
5. For each 8-K: parse the `items` array (comma-separated Item codes)
6. For each 10-Q/10-K: list metadata only (don't parse body)
7. Apply signal rules and compute score
8. Output the structured report

## Example invocation

User: "Is NVDA a buy or sell?"

The skill should:
1. Run full pipeline on NVDA over 180 days
2. Return:
   ```
   🎯 NVDA — 🔴🔴 STRONGLY_BEARISH (score -4)

   Signal reasons:
   • +1: High Form 4 filing velocity (15 filings)
   • -3: Net insider SELLING $294,772,058 over window
   • -2: Cluster sell (44 sells by 3 distinct insiders)

   Top insider activity:
   | HUANG JEN HSUN | President & CEO | S | 1,500,000 | -$213,000,000 | 2026-03-28 |
   | DALLY WILLIAM J | Chief Scientist | S | 350,000 | -$49,700,000 | 2026-03-15 |
   | KRESS COLETTE M | CFO | S | 180,000 | -$25,560,000 | 2026-03-10 |

   Recent material events:
   | 2026-02-26 | 2.02 | Earnings released — Q4 results |
   | 2026-02-10 | 7.01 | Regulation FD disclosure |

   Interpretation: 3 C-suite executives (including CEO Huang) coordinated $294M+ of open-market sales in the last 6 months. No offsetting insider buys. This is the classic institutional "crowded long" bearish signal.
   ```

## Honest caveats (always include at end of report)

- Signal rules are heuristic, not ML-trained
- Insider selling can be tax-motivated or pre-planned (10b5-1 plans)
- Past signals don't guarantee future returns
- This is research information, not a trading recommendation
- Not financial advice; consult a licensed advisor before trading

## Relationship to AlphaStack portfolio

This is the flagship skill corresponding to the `stock-alpha-aggregator` Apify actor (`216wsE6HuoC5wuudS`). The actor does this programmatically over many tickers; this skill does it interactively for one ticker inside Claude.
