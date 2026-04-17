---
name: hedge-fund-holdings
description: Analyzes the quarterly equity holdings of institutional investors (hedge funds, mutual funds, pensions) from SEC Form 13F-HR filings. Returns every position with CUSIP, share count, market value, and call/put flags for funds managing over $100M. Use when the user asks what a specific fund owns, wants to know what Berkshire/Buffett/Bridgewater/Citadel/Renaissance holds, asks "what did fund X buy last quarter", wants to see hedge fund position changes, or mentions 13F filings. Pulls from the official free SEC EDGAR submissions API with no key required. Correctly parses both bare and namespace-prefixed (ns1:) 13F XML formats. Known filer shortcuts built in (berkshire, bridgewater, citadel, renaissance, soros, tepper, ackman, loeb, einhorn). Replaces WhaleWisdom ($99-499/mo) and HedgeFollow.
---

# SEC 13F Institutional Holdings Analyzer

## When to invoke

Use this skill whenever the user asks about institutional fund holdings, 13F filings, or what specific hedge funds / mutual funds / pensions own. Common triggers:

- "What does Berkshire own?"
- "Show me Bridgewater's latest 13F"
- "What did Citadel buy this quarter?"
- "What's in Pershing Square's portfolio?"
- "Did Renaissance cut their Apple position?"
- "Top hedge fund positions in NVIDIA"

## Required input

- **Filer name or CIK**: either a short name from the mapping below, or a 10-digit SEC CIK.

## Filer shortname mapping (built-in)

| Short name | Fund | CIK |
|-----------|------|-----|
| `berkshire` | Berkshire Hathaway (Buffett) | 0001067983 |
| `bridgewater` | Bridgewater Associates (Dalio) | 0001350694 |
| `citadel` | Citadel Advisors (Griffin) | 0001423053 |
| `renaissance` | Renaissance Technologies (Simons) | 0001037389 |
| `soros` | Soros Fund Management | 0001029160 |
| `icahn` | Carl C. Icahn | 0000921669 |
| `tepper` / `appaloosa` | Appaloosa LP (Tepper) | 0001656456 |
| `ackman` / `pershing` | Pershing Square (Ackman) | 0001336528 |
| `loeb` / `third-point` | Third Point (Loeb) | 0001040273 |
| `einhorn` / `greenlight` | Greenlight Capital (Einhorn) | 0001079114 |
| `singer` / `elliott` | Elliott Investment Mgmt (Singer) | 0001108827 |
| `point72` | Point72 Asset Mgmt (Cohen) | 0001603466 |
| `tiger-global` | Tiger Global Mgmt | 0001167483 |
| `coatue` | Coatue Management | 0001135730 |
| `baker-bros` | Baker Bros. Advisors (biotech-focused) | 0001263508 |

## Output format

### 1. Fund overview (one line)
`"[Fund Name] (CIK {cik}) | Latest 13F: {filing_date} (period {period_of_report}) | {N} total positions | ${total_AUM}B AUM"`

### 2. Top 10 positions table

| Issuer | CUSIP | Shares | Market Value | % of Portfolio |
|--------|-------|-------:|-------------:|--------------:|

Sort by market value descending. Show top 10 unless user requests more.

### 3. Sector concentration (if meaningful)
One-paragraph summary: "Fund is heavily concentrated in [sector] with N% of AUM in [ticker examples]."

### 4. Notable positions / unusual activity
Highlight: largest options positions (calls or puts), new positions (compared to previous quarter if available), exits, or concentrated bets.

## Data source + procedure

Uses the official SEC EDGAR submissions + Archives APIs:

```
https://data.sec.gov/submissions/CIK{cik}.json
https://www.sec.gov/Archives/edgar/data/{cik-numeric}/{accession-no-dashes}/index.json
```

Steps:

1. Resolve filer short name → CIK (use mapping above or ask user for CIK)
2. Fetch CIK submissions JSON
3. Filter to `form === '13F-HR' || form === '13F-HR/A'`
4. Take the most recent filing (or specific period if user asked for one)
5. Fetch the filing's `index.json` to list files
6. Find the information-table XML (largest `.xml` file that is NOT `primary_doc.xml`)
7. Parse the XML:
   - Match `<(?:\w+:)?infoTable>...</(?:\w+:)?infoTable>` blocks (handle namespace prefixes)
   - For each block extract `<nameOfIssuer>`, `<titleOfClass>`, `<cusip>`, `<value>` (dollars, NOT thousands in post-2022 format), `<shrsOrPrnAmt><sshPrnamt>`, `<putCall>` (if present)
8. Sum values to get total AUM
9. Compute concentrations
10. Return the structured report

## Key facts about 13F filings

- **Filed quarterly**, within 45 days of quarter end (so Dec 31 data appears in Feb filings)
- **Required for any fund managing $100M+** in US equities
- **Only long equity positions are disclosed** — no shorts, no bonds, no international non-ADR
- **Multiple lots for same security**: if a fund holds the same CUSIP across multiple sub-advisors, you'll see multiple rows. Group by CUSIP when reporting to the user.
- **Options positions ARE disclosed** with `<putCall>Call</putCall>` or `<putCall>Put</putCall>` tags. These are highly informative — Citadel's NVDA 13F showed $14.4B in call options AND $10.25B in put options simultaneously.

## Example invocation

User: "What does Berkshire own?"

The skill should:
1. Resolve `berkshire` → CIK 0001067983
2. Fetch latest 13F-HR (typically filed Feb/May/Aug/Nov)
3. Parse all 110 positions
4. Return: "Berkshire Hathaway (period 2025-12-31): 110 positions totaling $267B. Top 5: Apple $85B, Bank of America $35B, Coca-Cola $28B, American Express $27B, Chevron $19B. Cash/equivalents at record $322B..."

## Relationship to AlphaStack portfolio

Corresponds to the `sec-13f-holdings-tracker` Apify actor (`MdzJoLuNugJ9M7UG5`). Use this skill for interactive Q&A inside Claude Code; use the actor for bulk dataset generation.
