---
name: futures-positioning-check
description: Analyzes weekly CFTC Commitment of Traders (COT) reports to show the current positioning of commercials (producers/hedgers), non-commercials (hedge funds/speculators), and retail in any US futures market — gold, oil, S&P 500 e-minis, Treasury bonds, EUR/USD, JPY/USD, bitcoin, wheat, corn, and more. Computes week-over-week positioning deltas and classifies signals as SPEC_BUILDING_LONGS, SPEC_UNWINDING_LONGS, SPEC_LEANING_LONG, SPEC_LEANING_SHORT, or NEUTRAL. Use when the user asks about futures positioning, trader commitment, "who's long gold?", hedge fund positioning in commodities, macro positioning data, or CFTC data. Uses the free official CFTC Socrata API. Replaces Bloomberg Terminal COT function ($25k/year) and TradingView Premium COT ($60/month).
---

# CFTC Commitment of Traders (COT) Check

## When to invoke

Trigger on any futures positioning question:

- "What's the positioning in gold?"
- "Are hedge funds long or short oil?"
- "CFTC COT data for S&P 500"
- "Is there a crowded long in bitcoin futures?"
- "Latest speculator positioning"
- "Commercial vs non-commercial in EUR/USD"

## Required input

- **Market** (substring): e.g. `"GOLD"`, `"WTI"`, `"S&P 500"`, `"BITCOIN"`, `"EURO FX"`. Matches against CFTC's market names.
- **Optional lookback** in weeks (default: 12 = last quarter of weekly reports)

## Common market substrings

| Substring | Matches |
|-----------|---------|
| `GOLD` | Gold + Micro Gold futures |
| `SILVER` | Silver futures |
| `WTI` | West Texas Intermediate crude |
| `BRENT` | Brent crude |
| `NATURAL GAS` | Natural gas |
| `S&P 500` | S&P 500 E-mini + Micro E-mini |
| `NASDAQ` | Nasdaq-100 E-mini + Micro |
| `RUSSELL 2000` | Russell 2000 mini |
| `ULTRA T-BOND` | Ultra Treasury bond |
| `10-YEAR` | 10-year Treasury note |
| `EURO FX` | EUR/USD futures |
| `JAPANESE YEN` | JPY/USD futures |
| `BRITISH POUND` | GBP/USD futures |
| `BITCOIN` | Bitcoin futures + Micro Bitcoin |
| `ETHER` | Ether futures |
| `WHEAT` | Wheat futures |
| `CORN` | Corn futures |
| `LIVE CATTLE` | Live cattle |
| `COFFEE` | Coffee futures |

## Output format

### 1. Current positioning snapshot (latest week)
`"[Market] as of [date]: Speculators NET [LONG/SHORT] {N} contracts. Commercials NET [LONG/SHORT] {N}. Open interest {OI}."`

### 2. WoW change analysis
`"Week-over-week: Speculators {added/reduced} {delta} net contracts ({percent}%). Signal: [classification]."`

### 3. Table of recent weeks

| Week | OI | Spec Long | Spec Short | Spec Net | Comm Net | WoW Δ | Signal |
|------|---:|----------:|-----------:|---------:|---------:|------:|--------|

### 4. Contrarian interpretation (when applicable)
If speculators are at extreme net-long and commercials are at extreme net-short, flag as "crowded long — historically a top indicator." Vice versa for extreme net-short. Use rolling historical percentile of speculator net position if available.

## Signal classification

| Condition | Signal |
|-----------|--------|
| Speculator net position increased >10% week-over-week | `SPEC_BUILDING_LONGS` |
| Speculator net position decreased >10% week-over-week | `SPEC_UNWINDING_LONGS` |
| Small positive change | `SPEC_LEANING_LONG` |
| Small negative change | `SPEC_LEANING_SHORT` |
| No change | `NEUTRAL` |

## Data source + procedure

Query the CFTC Socrata API:

```
GET https://publicreporting.cftc.gov/resource/jun7-fc8e.json?$limit=1000&$order=report_date_as_yyyy_mm_dd DESC&$where=report_date_as_yyyy_mm_dd >= '{since_date}T00:00:00.000' AND upper(market_and_exchange_names) LIKE '%{market}%'
```

Key fields in each row:

- `report_date_as_yyyy_mm_dd` — the Tuesday the positioning is as of
- `market_and_exchange_names` — e.g. "GOLD - COMMODITY EXCHANGE INC."
- `open_interest_all` — total open contracts
- `noncomm_positions_long_all` — speculator longs
- `noncomm_positions_short_all` — speculator shorts
- `comm_positions_long_all` / `comm_positions_short_all` — commercial positions
- `nonrept_positions_long_all` / `nonrept_positions_short_all` — retail/small trader
- `change_in_noncomm_long_all` / `change_in_noncomm_short_all` — weekly deltas

Group results by `market_and_exchange_names`, sort each group by date ascending, and compute rolling week-over-week deltas.

## The contrarian playbook (summarize this when relevant)

COT has a well-documented contrarian signal pattern since 1962:

1. **Extreme speculator net-long + extreme commercial net-short** = commercials (the "smart money" that actually produces/uses the commodity) are hedging production at prices they expect to DROP. Historically a top indicator.
2. **Extreme speculator net-short + extreme commercial net-long** = commercials see value at low prices and are accumulating. Historically a bottom indicator.
3. **Alignment** (both speculators and commercials leaning same direction) = rare, but conviction-building for the direction.

## Example invocation

User: "What's the positioning in gold right now?"

The skill should:
1. Query the API with `GOLD` filter for the last 12 weeks
2. Return:
   ```
   GOLD - COMMODITY EXCHANGE INC. as of 2026-04-07:
   • Open interest: 550,487 contracts
   • Speculators: NET LONG 153,868 contracts
   • Commercials: NET SHORT 192,465 contracts
   • Small traders (retail): NET LONG 38,597

   Week-over-week: Speculators REDUCED net long by 6,828 contracts (-4.2%)
   Signal: SPEC_LEANING_SHORT

   Interpretation: Speculators remain heavily long gold at 153k net, but they're trimming. Commercial producers are at elevated short hedges. This is typical of a "spec crowd still long but fading" setup — not yet at an extreme contrarian signal, but watch for continued speculator reduction + commercial short covering, which would signal a potential bottom.
   ```

## Key facts

- **Released every Friday at 3:30pm ET**, showing positions as of the prior Tuesday
- **Uses "Legacy Futures-Only Reports"** by default (this API); the "Disaggregated" and "Traders in Financial Futures" reports have more granular categories but are separate endpoints
- **Open interest is total unique contracts**, not volume

## Relationship to AlphaStack portfolio

Corresponds to the `cftc-cot-report-tracker` Apify actor (`4vacNBQByjkB1YYF2`).
