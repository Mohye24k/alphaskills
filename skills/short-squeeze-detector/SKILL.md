---
name: short-squeeze-detector
description: Detects potential short-squeeze candidates by combining 5 asymmetric signals — short interest as percentage of float (higher = more fuel), days-to-cover ratio (higher = harder to unwind), insider buying pattern (+bullish momentum against shorts), Reddit r/wallstreetbets sentiment velocity (retail crowd building), and recent 13F institutional accumulation (smart money aligned with retail). Returns a ranked list of tickers with computed "squeeze probability" scores and expected magnitude. Use when the user asks about short squeezes, wants to find GME/AMC-style opportunities, tracks heavily-shorted stocks, asks about retail-driven momentum, or builds a momentum watchlist. Combines NYSE/Nasdaq short interest data + SEC Form 4 + 13F + Reddit sentiment + FINRA disclosure. No free tool exists that combines all 5 signals.
---

# Short Squeeze Detector — The GameStop / AMC Screen

## The premise

A short squeeze happens when a heavily-shorted stock rallies, forcing short sellers to cover at higher prices, which pushes the price up more, forcing more shorts to cover, etc. The GameStop January 2021 run was the most famous example (~1,900% in 2 weeks). Squeezes happen regularly at smaller scale.

5 signals combined identify the setup BEFORE the squeeze happens.

## When to invoke

Trigger on:

- "Find short squeeze candidates"
- "Which heavily-shorted stocks are most squeezable?"
- "Next GameStop"
- "Momentum + short interest screen"
- "r/wallstreetbets stocks to watch"
- "What's setting up for a squeeze?"

## Required input

- **Tickers** or **sector** — universe to scan
- **Optional minimum market cap** (default: $100M to filter junk)
- **Optional minimum short interest** (default: 15% of float)

## The 5 squeeze signals

### Signal 1: Short interest % of float (scale: +0 to +4)
The fundamental fuel. NYSE/Nasdaq semi-monthly short interest reports.

- 15-20% of float: `+1`
- 20-30% of float: `+2`
- 30-50% of float: `+3`
- >50% of float: `+4` (rare; GME was ~140% in Jan 2021 due to synthetic shorts)

**Source**: NYSE + Nasdaq semi-monthly short interest reports (published via FINRA)

### Signal 2: Days-to-cover ratio (+0 to +2)
Days-to-cover = short interest / average daily volume. Higher = harder for shorts to exit without driving price up.

- 2-5 days: `+1`
- 5-10 days: `+2`
- 10+ days: `+3`

**Source**: Same short interest report + recent ADV from historical volume data

### Signal 3: Insider BUYING counter-current (+2)
When insiders buy open-market shares (code P) AGAINST a heavily-shorted stock, that's a strong contrarian long signal that often precedes squeezes.

**Source**: SEC Form 4 via `sec-insider-scan` — filter to code P purchases in last 60 days

### Signal 4: Reddit r/wallstreetbets mention velocity (+0 to +3)
If retail interest is building (rising mention count, rising sentiment), the squeeze is organizing.

- 50+ new mentions per week: `+1`
- 500+ mentions per week: `+2`
- 5,000+ mentions per week: `+3`

**Source**: Reddit JSON API scraping r/wallstreetbets and r/stocks for ticker mentions

### Signal 5: 13F institutional long accumulation (+2)
If hedge funds are BUILDING long positions while shorts are stuck, they're intentionally squeezing. Key check: are any of the top 20 hedge funds increasing positions quarter-over-quarter?

**Source**: SEC 13F filings via `hedge-fund-holdings` — compare last 2 quarters

## Scoring

Sum signals. Score interpretation:

- **10+**: HIGHLY LIKELY squeeze setup. Expected magnitude: 50-200%+ within 30-90 days if sparked.
- **7-9**: PROBABLE squeeze candidate. Expected magnitude: 20-80%.
- **4-6**: MODERATE setup. Expected magnitude: 10-30%.
- **<4**: Low squeeze probability.

## Output format

### 1. Summary
`"Scanned {N} tickers. {x} HIGHLY LIKELY squeeze setups. {y} PROBABLE. Top candidate: {ticker} (score {z})."`

### 2. Ranked table

| Ticker | Market Cap | Short Interest % | Days to Cover | Insider Buys | WSB mentions | 13F Accum | Score |
|--------|-----------:|-----------------:|--------------:|-------------:|-------------:|----------:|------:|

### 3. Top 3 detailed breakdowns
For each, provide:
- Breakdown of each signal with numbers
- What the squeeze catalyst is likely to be (earnings, FDA date, analyst upgrade)
- Historical comps (similar setups and what happened)
- Expected upside + downside

## Data source + procedure

### Short interest data (the tricky one)

FINRA publishes semi-monthly short interest reports at finra.org and at NYSE + Nasdaq. These are NOT real-time — they're lagged by 2-4 weeks. Use the official endpoint:

```
GET https://api.finra.org/data/group/otcMarket/name/regShoDaily?limit=5000
```

OR scrape from Nasdaq's short interest page for each ticker. Always note the AS-OF date.

### Days-to-cover calculation

```
days_to_cover = short_interest / (avg_daily_volume_last_30d)
```

Get ADV from public OHLCV data (Yahoo Finance / Alpha Vantage / etc.)

### Reddit sentiment (lightweight)

```
GET https://www.reddit.com/r/wallstreetbets/search.json?q={ticker}&sort=new&limit=100&t=week
```

Count mentions, compute week-over-week growth.

### 13F accumulation (via existing skill)

Call `hedge-fund-holdings` internally; compare the specific ticker's institutional ownership across the last 2 reporting quarters.

## Example invocation

User: "Find short squeeze candidates in small-mid cap"

The skill should:

1. Scan tickers with market cap $100M-$5B and short interest >15%
2. Compute signals for each
3. Return:
   ```
   Scanned 218 tickers with market cap $100M-$5B and short interest >15%.
   HIGHLY LIKELY squeeze setups: 3. PROBABLE: 11.

   Top squeeze candidates:

   | Ticker | MCap  | Short% | D2C | Ins Buys | WSB/wk | 13F | Score |
   |--------|------:|-------:|----:|--------:|-------:|-----|------:|
   | BYND   | $1.2B | 41%    | 8.2 | 3       | 1,240  | +   | 11/14 |
   | BBBY   | $890M | 47%    | 6.8 | 0       | 3,580  | -   | 9/14  |
   | CRNC   | $340M | 28%    | 4.1 | 2       | 89     | +   | 7/14  |

   Top analysis — BYND (Beyond Meat):
   Signal breakdown:
   • Short interest: 41% of float (+3 pts) — extreme short position built after Q3 miss
   • Days-to-cover: 8.2 (+2 pts) — would take 8+ days of normal volume for shorts to exit
   • Insider buys: CEO bought 100k shares on 2026-03-15 at $7.80 ($780k total) (+2 pts)
   • WSB mentions: 1,240 per week, up from 180 four weeks ago (+2 pts)
   • 13F accumulation: Tepper's Appaloosa + 2 other funds added positions Q1 (+2 pts)

   Likely squeeze catalyst: Q1 earnings (date TBD, probably early May). Historical BYND earnings moves: 8-25% on report day. With this short interest + positioning, a beat could trigger 50-100% squeeze.

   Historical comp: BBBY October 2022 — similar short interest (40%+) + retail sentiment + insider buying → stock ran 250% in 3 weeks before collapsing.

   Risk: Downside is still substantial — BYND fundamentals remain weak (revenue -28% YoY, $300M cash burn run-rate). Squeeze ≠ permanent recovery.
   ```

## Why this is truly remarkable

- **Ortex** ($40-400/month) — has short interest data but doesn't combine with insider + retail
- **Fintel** — has some signals but not a unified scoring
- **WSB itself** — has the retail sentiment but not the institutional or insider data
- **No free tool combines all 5 signals in one dashboard**

This skill does. For free. For any ticker.

## Honest caveats

- **Short interest data is lagged 2-4 weeks** — always verify current position before trading
- **Historical pattern is not a guarantee** — many setups never squeeze
- **Retail sentiment can reverse in days** — WSB moves fast
- **Squeezes are zero-sum-ish** — for every trader who profits, another loses
- **Do not trade on this skill's output without your own validation** — not financial advice

## License + source

Uses free public data (FINRA, SEC EDGAR, Reddit JSON). MIT licensed.
