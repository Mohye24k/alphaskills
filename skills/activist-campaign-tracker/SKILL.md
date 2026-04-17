---
name: activist-campaign-tracker
description: Tracks activist investor campaigns through SEC Schedule 13D and 13G filings. When Icahn, Ackman, Loeb, Elliott, Pershing Square, Third Point, Jana, Starboard, or Trian crosses 5% ownership of a public company, this skill returns the filing within minutes including the target company, shares owned, percent of class, CUSIP, and filing URL. Use when the user asks what company an activist is currently targeting, wants to track Icahn's or Ackman's recent moves, asks "who just filed 13D on X", needs to monitor activist campaigns, or wants to know if there's a new activist position in a specific stock. Parses the structured SGML header of every filing to reliably extract subject company metadata. Replaces ActivistInsight ($20-100k/year) and 13D Monitor ($10k+/year).
---

# SEC 13D/13G Activist Filings Tracker

## When to invoke

Trigger on:

- "What's Icahn doing lately?"
- "Show me Ackman's activist positions"
- "Any new 13D filings by Elliott?"
- "Did anyone file a 13D on X company?"
- "Who's accumulating stake in Y stock?"
- "Latest Pershing Square positions"

## Required input

- **Activist name** (short name from mapping below) OR a specific 10-digit CIK.
- **Optional lookback window** in days (default: 180 days)

## Activist shortname mapping

| Short name | Activist | CIK |
|-----------|----------|-----|
| `icahn` | Carl C. Icahn | 0000921669 |
| `ackman` / `pershing` | Pershing Square (Bill Ackman) | 0001336528 |
| `loeb` / `third-point` | Third Point LLC (Dan Loeb) | 0001040273 |
| `einhorn` / `greenlight` | Greenlight Capital (David Einhorn) | 0001079114 |
| `singer` / `elliott` | Elliott Investment Mgmt (Paul Singer) | 0001108827 |
| `trian` / `peltz` | Trian Fund Mgmt (Nelson Peltz) | 0001345471 |
| `jana` | JANA Partners | 0001159159 |
| `starboard` | Starboard Value LP (Jeff Smith) | 0001517302 |
| `engine-1` | Engine No. 1 LP | 0001822185 |
| `corvex` | Corvex Management (Meister) | 0001541106 |

## Output format

### 1. Top-line
`"[Activist Name] filed N 13D/13G filings over the last {window} days. Active positions: X companies."`

### 2. Filings table

| Date | Form | Target Company | Shares | % Class | CUSIP |
|------|------|----------------|-------:|--------:|-------|

Sort by filing date descending. Mark initial 13D filings with ⭐ (most actionable), amendments with ↻, passive 13G with 〇.

### 3. Campaign analysis
For each initial 13D filing, add a one-paragraph analysis:
- What the SIC industry code is
- What a 5-40% position typically signals (activist is building, already at size, or preparing proxy fight)
- Previous campaigns by this activist in the same industry

## Data source + procedure

Two-step process using SEC EDGAR:

### Step 1: Find filings
```
GET https://data.sec.gov/submissions/CIK{cik}.json
```
Filter `filings.recent` where `form` is `"SC 13D"`, `"SC 13D/A"`, `"SC 13G"`, or `"SC 13G/A"`, and `filingDate >= lookback`.

### Step 2: Parse subject company from each filing's header
```
GET https://www.sec.gov/Archives/edgar/data/{cik-numeric}/{acc-no-dashes}/{accessionNumber}-index-headers.html
```

The header is SGML-formatted with structured blocks:

```
<SUBJECT-COMPANY>
<COMPANY-DATA>
<CONFORMED-NAME>Southwest Gas Holdings, Inc.
<CIK>0001692115
<ASSIGNED-SIC>4923
<STATE>DE
</COMPANY-DATA>
...
</SUBJECT-COMPANY>
<FILED-BY>
<CONFORMED-NAME>ICAHN CARL C
...
</FILED-BY>
```

Extract `CONFORMED-NAME`, `CIK`, `ASSIGNED-SIC`, `STATE` from the SUBJECT-COMPANY block.

### Step 3: Parse shares + percent from primary HTML
Each 13D filing has an HTML cover page with a standardized table. Extract:

- **Aggregate shares beneficially owned**: regex `/AGGREGATE\s+AMOUNT\s+BENEFICIALLY\s+OWNED[^0-9]*?([0-9,]+)/i`
- **Percent of class**: regex `/PERCENT\s+OF\s+CLASS\s+REPRESENTED\s+BY\s+AMOUNT\s+IN\s+ROW[^%]*?([0-9]+\.?[0-9]*)\s*%/i`
- **CUSIP**: 9-character alphanumeric identifier — look for pattern `\d{6}[A-Z0-9]{3}` near the "CUSIP Number" label (it may appear BEFORE or AFTER the label, try both positions)

## Key facts about 13D/13G

- **13D** = activist (intent to influence). Filed within **10 days** of crossing 5%. Moves stocks 5-40% on filing.
- **13G** = passive holder (Vanguard, BlackRock, index funds). Less alpha signal.
- **13D/A and 13G/A** = amendments reporting position changes.
- **Multi-entity filings**: Elliott, Icahn use multiple legal entities. Short names here map to the primary filing entity. For comprehensive tracking, pass multiple CIKs.

## Example invocation

User: "What is Ackman doing lately?"

The skill should:
1. Resolve `ackman` → CIK 0001336528
2. Fetch Pershing Square's recent 13D filings
3. Parse header + cover page for each
4. Return:
   ```
   Ackman (Pershing Square) has 5 active 13D positions as of Apr 2026:
   ⭐ Howard Hughes Holdings — 18.85M shares (37.5%)
   ⭐ Seaport Entertainment Group — 5.02M shares (40.1%)
   ↻ Restaurant Brands International — 23.52M shares (7.4%)
   ...
   Ackman is clearly doubling down on Howard Hughes — three amendments in 2024 suggest an active proxy fight or acquisition thesis.
   ```

## Relationship to AlphaStack portfolio

Corresponds to the `sec-13d-activist-filings` Apify actor (`fyEz9uhbhDgNKYi3O`). Use this skill for real-time Q&A; use the actor for bulk scheduled monitoring.
