---
name: sec-insider-scan
description: Scans recent SEC Form 4 insider trading filings for any US public company ticker. Returns a structured summary of insider buys, sells, option exercises, and grants with aggregate statistics (net shares, net dollar flow, buy/sell counts, top insiders). Use when the user asks about insider activity for a specific stock, wants to know if executives are buying or selling their own company's shares, asks "is X stock being dumped by insiders", needs a quick sentiment read on executive activity, or mentions Form 4 filings. Pulls directly from the official free SEC EDGAR submissions API (data.sec.gov) with no API key required. Correctly classifies transaction codes (P=open-market purchase, S=sale, M=option exercise, F=sell-to-cover, A=grant, G=gift). Replaces InsiderScore ($99-499/mo) and OpenInsider-style batch feeds.
---

# SEC Form 4 Insider Trading Scanner

## When to invoke

Use this skill whenever the user asks about insider trading, insider activity, Form 4 filings, or executive buying/selling for a specific US-listed public company. Common trigger phrases include:

- "What are the insiders doing at TSLA?"
- "Show me recent Form 4s for NVDA"
- "Is anyone at $AAPL selling?"
- "Any insider buys at small-cap biotech X?"
- "Give me the Meta insider trading report"

## Required input

- **Ticker symbol** (e.g. `TSLA`, `NVDA`, `AAPL`, `PFE`). If the user gives a company name instead, map it to the canonical SEC ticker first.
- **Optional lookback window** in days (default: 90 days)

## Output format

Produce a structured report with three sections:

### 1. Top-line signal
One-sentence summary: `"[Ticker] insiders net-sold $X million over the last N days. Cluster activity: N distinct insiders. Signal: BEARISH/BULLISH/NEUTRAL."`

### 2. Transaction table

| Date | Insider | Role | Code | Type | Shares | Price | Value |
|------|---------|------|------|------|-------:|------:|------:|

Sort by transaction date, descending. Cap at 15 most recent. Use the transaction code descriptions from the mapping below.

### 3. Top insiders ranked

| Insider | Title | Net Shares | Net Value |
|---------|-------|-----------:|----------:|

Show the top 5 insiders ranked by absolute net dollar value of their activity.

## Data source + procedure

This skill queries the SEC EDGAR submissions JSON API:

```
https://data.sec.gov/submissions/CIK{10-digit-cik}.json
```

Steps:

1. Resolve the user's ticker to a 10-digit CIK via `https://www.sec.gov/files/company_tickers.json` (cache this response — it rarely changes).
2. Fetch the submissions JSON for that CIK.
3. Filter `filings.recent` where `form === '4'` and `filingDate >= lookback_window`.
4. For each Form 4 filing, download the raw XML at:
   ```
   https://www.sec.gov/Archives/edgar/data/{cik-numeric}/{accession-no-dashes}/{primary_doc.xml}
   ```
   (Primary doc name is typically `edgardoc.xml` but can vary — check the filing's `primaryDocument` field and strip the `xslF345X06/` prefix if present.)
5. Parse the XML to extract:
   - Reporting person: `<rptOwnerName>`, `<isDirector>`, `<isOfficer>`, `<isTenPercentOwner>`, `<officerTitle>`
   - Transactions: each `<nonDerivativeTransaction>` block contains `<transactionDate>`, `<transactionCode>`, `<transactionShares><value>`, `<transactionPricePerShare><value>`, `<transactionAcquiredDisposedCode>`
6. Compute aggregates:
   - `netShares = sum(buys.shares) - sum(sells.shares)`
   - `netValue = sum(buys.shares * price) - sum(sells.shares * price)`
   - Count distinct insiders involved
7. Classify signal:
   - Net buying + cluster (3+ distinct insiders) → BULLISH
   - Net selling > $1M + cluster → BEARISH
   - Otherwise → NEUTRAL

## Transaction code classification

| Code | Description | Classified as |
|------|-------------|---------------|
| P | Open-market or private purchase | **buy** (strongest bullish signal) |
| S | Open-market or private sale | **sell** |
| D | Disposition to issuer | sell |
| F | Pay exercise price/tax via securities | sell (neutral — comp mechanic) |
| M | Exercise of derivative security | option-exercise (comp mechanic, not directional) |
| C | Conversion of derivative | option-exercise |
| X | Exercise of in-the-money derivative | option-exercise |
| A | Grant, award, acquisition | grant (comp, not directional) |
| G | Bona fide gift | gift |

**Only code P (buys) and code S/D (sells) are meaningful directional signals.** Codes M, F, A are compensation-related and should be reported but not weighted in the signal.

## SEC API requirements

- Include a `User-Agent` header identifying your app: `"YourAppName contact@yourdomain.com"`
- Respect the 10 req/sec rate limit
- No API key needed

## Example invocation

User: "What are the insiders doing at NVDA?"

The skill should:
1. Resolve NVDA → CIK 0001045810
2. Pull last 90 days of Form 4 filings
3. Parse each filing's XML
4. Return: "NVIDIA insiders net-sold $294,772,058 over the last 180 days across 44 transactions by 3 distinct C-suite executives. Signal: STRONGLY BEARISH. CEO Jensen Huang alone sold $213M..."

## Relationship to AlphaStack portfolio

This skill corresponds to the `sec-form4-insider-trades` Apify actor (`PBJe8AgtCNCZxhhvD`). For bulk programmatic access, use the Apify actor. For interactive one-ticker analysis inside Claude Code or Claude Projects, use this skill.
