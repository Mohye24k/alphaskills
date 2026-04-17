---
name: fred-economic-data
description: Queries the Federal Reserve Economic Data (FRED) repository of 800,000+ macroeconomic time series — US unemployment, CPI/inflation, GDP, Fed funds rate, Treasury yields, money supply, industrial production, retail sales, housing starts, and nearly every major US economic indicator. Returns observations (date + value), metadata (frequency, units, seasonal adjustment), and optionally computes pct-change / year-over-year deltas. Use when the user asks about unemployment rate, CPI / inflation, GDP growth, interest rates, housing data, jobs reports, or any specific FRED series by name or ID. Uses the official FRED API (api.stlouisfed.org/fred) — requires a free API key from fred.stlouisfed.org/docs/api/api_key.html. Replaces Nasdaq Data Link ($249+/month) and Bloomberg ECO function ($25k/year).
---

# FRED Economic Data

## When to invoke

Trigger on any macro / economic data question:

- "What is the current unemployment rate?"
- "US CPI inflation year-over-year"
- "Fed funds rate history"
- "10-year Treasury yield chart"
- "US retail sales trend"
- "Housing starts monthly"
- "Show me the yield curve"

## Required input

- **Series ID** — FRED's unique identifier (e.g. `UNRATE`, `CPIAUCSL`, `GDP`, `DFF`, `DGS10`)
- OR — **series name search term** (e.g. `"unemployment"`, `"consumer price index"`) which we search FRED for first

## Common series (built-in reference)

| FRED ID | Name | Frequency |
|---------|------|-----------|
| `UNRATE` | Unemployment Rate | Monthly |
| `CPIAUCSL` | Consumer Price Index (CPI-U All Items) | Monthly |
| `CPILFESL` | Core CPI (ex food/energy) | Monthly |
| `GDP` | GDP, Seasonally Adjusted Annualized | Quarterly |
| `GDPC1` | Real GDP, chained 2017 dollars | Quarterly |
| `DFF` | Federal Funds Effective Rate | Daily |
| `DFEDTARU` | Federal Funds Target Rate Upper Bound | Irregular |
| `DGS10` | 10-Year Treasury Constant Maturity Rate | Daily |
| `DGS2` | 2-Year Treasury | Daily |
| `DGS3MO` | 3-Month Treasury | Daily |
| `T10Y2Y` | 10Y-2Y Treasury Spread (recession indicator) | Daily |
| `HOUST` | Housing Starts | Monthly |
| `PAYEMS` | Total Nonfarm Payrolls | Monthly |
| `INDPRO` | Industrial Production Index | Monthly |
| `RRSFS` | Real Retail Sales | Monthly |
| `VIXCLS` | CBOE Volatility Index (VIX) | Daily |
| `DCOILWTICO` | Crude Oil WTI Spot Price | Daily |
| `GOLDPMGBD228NLBM` | Gold Fixing Price (London) | Daily |
| `M2SL` | M2 Money Supply | Monthly |
| `UMCSENT` | Michigan Consumer Sentiment | Monthly |

## Output format

### 1. Latest observation (headline)
`"{Series Name} ({series_id}): Latest value is {V} as of {date} ({frequency}). {YoY change}."`

### 2. Recent observations table

| Date | Value | MoM Δ | YoY Δ |
|------|------:|------:|------:|

Show last 12 observations for monthly, last 8 quarters for quarterly, last 30 days for daily. Compute month-over-month and year-over-year changes.

### 3. Context / interpretation
If the series is a well-known economic indicator, add a one-paragraph interpretation:
- Unemployment above / below historical mean
- CPI YoY vs Fed's 2% target
- Yield curve inversion status
- Recession indicators (Sahm rule, 10Y-2Y)
- etc.

## Data source + procedure

Requires a free API key from https://fred.stlouisfed.org/docs/api/api_key.html.

### Step 1: Search (if given a search term rather than series ID)

```
GET https://api.stlouisfed.org/fred/series/search?search_text={term}&api_key={key}&file_type=json&limit=5
```

Pick the most popular match (highest `popularity` field) unless user specified otherwise.

### Step 2: Get observations

```
GET https://api.stlouisfed.org/fred/series/observations?series_id={id}&api_key={key}&file_type=json&sort_order=desc&limit=50
```

Response has `observations[]` with `date` and `value` fields.

### Step 3: Get metadata (for unit labels, frequency, etc.)

```
GET https://api.stlouisfed.org/fred/series?series_id={id}&api_key={key}&file_type=json
```

Returns `title`, `units`, `units_short`, `frequency`, `seasonal_adjustment`, etc.

## Example invocation

User: "What is the current unemployment rate?"

The skill should:
1. Recognize `UNRATE` as the standard series
2. Query observations (latest 12)
3. Return:
   ```
   Unemployment Rate (UNRATE): Latest value is 4.1% as of 2026-03-01 (Monthly).
   YoY change: +0.3pp from 3.8% a year ago.

   Last 12 months:
   | 2026-03 | 4.1% | +0.1 | +0.3 |
   | 2026-02 | 4.0% | 0.0 | +0.3 |
   | 2026-01 | 4.0% | -0.1 | +0.2 |
   ...

   Interpretation: US unemployment at 4.1% is above the 2000-2019 cycle lows of 3.5-3.6% but remains below the historical mean of ~5.6%. The 0.3pp YoY rise is consistent with labor market cooling but not recessionary levels. The Sahm Rule (recession indicator triggered when 3-month average rises 0.5pp above 12-month low) is NOT triggered.
   ```

## Time-saving tips

- For "inflation" → use `CPIAUCSL` (headline) or `CPILFESL` (core)
- For "recession probability" → use `T10Y2Y` (curve inversion) or `SAHMREALTIME` (Sahm rule)
- For "real rates" → compute `DGS10 - CPIAUCSL_YoY` inline

## License + source

FRED data is generally public domain or has permissive licenses. Individual series may have attribution requirements (e.g. Bloomberg's oil price series). Check each series' `notes` field for source attribution.
