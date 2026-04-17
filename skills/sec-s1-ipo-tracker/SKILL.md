---
name: sec-s1-ipo-tracker
description: Tracks upcoming US IPOs and direct listings through SEC Form S-1 (initial registration statement) and F-1 (foreign private issuer) filings. Returns company name, proposed ticker, exchange, auditor, lead underwriters, shares offered, price range, use of proceeds, financial highlights (revenue, net income, cash burn), and risk factors summary. Use when the user asks about upcoming IPOs, new registration statements, pre-IPO companies, S-1 amendments (S-1/A), or needs an IPO calendar. Identifies "hot" IPOs via velocity of S-1/A amendments (multiple amendments in short window = imminent pricing). Uses the free SEC EDGAR submissions API (data.sec.gov) with no key required. Replaces Renaissance Capital IPO ETF research ($99+/month) and Seeking Alpha IPO Central ($29+/month).
---

# SEC S-1 IPO Tracker

## When to invoke

Trigger on any IPO / registration statement question:

- "What companies are about to IPO?"
- "Recent S-1 filings"
- "IPO calendar April 2026"
- "Tell me about X company's S-1"
- "Who are the hot pre-IPO filers?"
- "Foreign IPO filings (F-1)"

## Required input (at least one)

- **Date range** — start + end dates (default: last 30 days)
- **Company CIK** or name — to fetch a specific company's S-1
- **Industry SIC code** — e.g. `7372` (prepackaged software), `2836` (pharmaceutical preparations)
- **Amendment filter** — include only S-1/A amendments (imminent pricings) or only initial S-1s

## Output format

### 1. IPO calendar summary
`"Found {N} S-1/F-1 filings in window. {X} initial filings, {Y} amendments. {Z} in final pricing stage (3+ amendments in last 30 days)."`

### 2. IPOs table

| Filed | Company | Ticker | Exchange | Shares | Price | Lead UW | Status |
|-------|---------|--------|----------|--------|-------|---------|--------|

Sort by filing date descending. Mark `📅 PRICING SOON` for companies with 3+ amendments in last 30 days.

### 3. Hot IPOs highlight
For companies approaching pricing (heavy amendment velocity), add a one-paragraph analysis:
- Financial highlights from the latest S-1/A (revenue, profitability, cash)
- Risk factors that seem unusually prominent
- Lead underwriters (Goldman / Morgan Stanley / JPM = blue-chip; smaller = riskier)
- Use of proceeds

### 4. Foreign filings (F-1)
Separate section for F-1 filings (foreign private issuers — usually Chinese, Israeli, European companies listing on US exchanges).

## Data source + procedure

Uses SEC EDGAR. There's no "latest S-1" endpoint, so we use full-text search:

### Approach 1: EDGAR full-text search

```
GET https://efts.sec.gov/LATEST/search-index?forms=S-1,S-1/A,F-1,F-1/A&dateRange=custom&startdt={start}&enddt={end}
```

Returns hits with `source.display_names[]`, `source.file_date`, `source.form_type`, `source.adsh` (accession number), `source.ciks[]`.

### Approach 2: Per-company submissions

If user gives a company name/ticker:

```
GET https://data.sec.gov/submissions/CIK{cik}.json
```

Filter `filings.recent` where `form IN ('S-1', 'S-1/A', 'F-1', 'F-1/A')`.

### Fetching the filing content

```
GET https://www.sec.gov/Archives/edgar/data/{cik-numeric}/{acc-no-dashes}/{primary_doc.htm}
```

The primary document for S-1 filings is a massive HTML file (sometimes 200+ pages). Key sections to extract via regex / XPath:

- **Prospectus Summary** — first substantive section
- **The Offering** — shares offered, price range, underwriters
- **Risk Factors** — full risk disclosure
- **Use of Proceeds** — what the company will do with IPO money
- **Selected Financial Data** — 3-5 years of revenue, COGS, opex, net income
- **Management's Discussion and Analysis (MD&A)**
- **Directors, Executive Officers, and Corporate Governance**
- **Principal and Selling Stockholders** — who owns what going into the IPO

## Amendment velocity = pricing proximity

S-1 filings go through multiple rounds of SEC comments. Each SEC round produces an S-1/A amendment. Typical pattern:

- Initial S-1 → SEC response 30-60 days later
- S-1/A #1 (response to SEC comments) → SEC response 20-40 days later
- S-1/A #2 → SEC response 15-30 days later
- S-1/A #3 (final amendment — usually the "pricing range" amendment)
- **Pricing within 1-2 weeks after final S-1/A**

So 3+ amendments in <30 days = imminent pricing.

## Example invocation

User: "What companies are about to IPO?"

The skill should:
1. Query EDGAR full-text search for S-1/A filings in last 14 days
2. Cross-reference with the same CIK's initial S-1 to count amendment velocity
3. Return:
   ```
   Found 23 S-1 / S-1/A filings in the last 14 days.
   12 initial S-1 filings, 11 amendments.
   3 companies in PRICING SOON status (3+ amendments):

   📅 Databricks Inc — S-1/A #4 filed 2026-04-14
       Ticker: DBRX (proposed), NASDAQ, Lead UWs: Morgan Stanley, Goldman Sachs, JPM
       2025 revenue: $3.1B (+47% YoY). Net loss $(450M) narrowing from $(680M).
       Likely pricing week of April 22, $65-75 range, ~$35B valuation.

   📅 Stripe Inc — S-1/A #3 filed 2026-04-10
       Ticker: STRI (proposed), NYSE, Lead UW: Goldman Sachs
       ...

   📅 Shein Holdings — F-1/A #5 filed 2026-04-08
       Ticker: SHEI (proposed), NYSE, Lead UWs: Goldman Sachs, JPM
       ...
   ```

## Risk factors to watch for (add to analysis)

Common red flags in S-1 risk factors:

- **"Going concern" language** — company may not survive if IPO fails
- **Single-customer concentration** — >20% revenue from one customer
- **Auditor qualification** — any non-"clean" opinion
- **Related-party transactions** — loans/payments to insiders
- **Pending litigation** disclosed in the risk factors section
- **China-VIE structure** (F-1 filings) — ownership disclaimer for Chinese companies

## License + source

SEC EDGAR data is public domain. No API key required.
