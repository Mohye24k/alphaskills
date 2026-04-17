---
name: executive-network-mapper
description: Maps the complete professional network of any US public-company executive — current and past board seats, previous companies, academic affiliations, NIH grants received, patents filed, co-authored papers, SEC Form 4 filings, and reverse-lookup from DEF 14A proxy statements of other companies where they serve. Reveals hidden relationships — when a CEO of Company A joins the board of Company B while holding equity in Company C that is a supplier to B. Use when the user asks about an executive's background, researches director networks, investigates corporate-governance conflicts of interest, identifies KOL networks in biotech, maps interlocking directorates, or wants to know "who knows whom" in a specific industry. Replaces BoardEx ($50k+/year institutional), Equilar BoardEdge ($20k+/year), and manual LinkedIn → proxy statement reconciliation.
---

# Executive Network Mapper — The "Six Degrees" Graph Tool

## The premise

Corporate America is deeply interconnected. The CEO of Johnson & Johnson sits on the board of Coca-Cola. The CFO of Microsoft was previously at Goldman Sachs. The founder of Moderna is a Harvard professor with 40 NIH grants. Tracing these connections manually takes hours and is the core competency of M&A investment bankers, activist investor research teams, and investigative journalists.

This skill does it in one invocation.

## When to invoke

Trigger on:

- "Tell me about [executive name] — their full background"
- "Who is on the board of [company]?"
- "Map the network around [founder / CEO]"
- "Which executives connect [company A] and [company B]?"
- "KOL network for GLP-1 research"
- "Board-level conflicts of interest at X"

## Required input (at least one)

- **Executive name** — full name (e.g. `"Tim Cook"`, `"Jensen Huang"`, `"Stéphane Bancel"`)
- **Company ticker** — to fetch the company's executive roster first, then expand
- **Domain** — to filter (e.g. `"biotech KOLs"`, `"AI chip founders"`)

## The 6 layers of the network graph

### Layer 1: Current role
- Current company, title, CIK
- Joined date (from DEF 14A or 8-K Item 5.02)
- Compensation package summary

**Source**: Latest DEF 14A (proxy statement) for the current employer

### Layer 2: Current board seats (other companies)
- All other public companies where this person serves on the board
- Their role (independent director, chair, committee member)
- Equity holdings in each

**Source**: Cross-reference across ALL DEF 14A filings in SEC EDGAR for mentions of this name

### Layer 3: Prior companies (executive history)
- Previous CEO/CFO/director roles
- Exit reasons (retirement, resignation, acquisition)
- Time at each company

**Source**: SEC 8-K Item 5.02 filings (exec departures/appointments) + DEF 14A director biographies

### Layer 4: Academic affiliations
- If person has PhD/MD, where they trained
- Current academic appointments (tenure, consulting)
- Co-authored papers

**Source**: `pubmed-paper-scan` + `arxiv-paper-scan` — search for author matches

### Layer 5: NIH grants (for researchers / biotech execs)
- Grants received (PI or co-PI)
- Total NIH funding
- Co-investigators

**Source**: `nih-grant-scan` — search by `pi_names`

### Layer 6: Patents
- Patents filed (as inventor)
- Patent co-inventors (reveals collaboration networks)

**Source**: USPTO patent search by inventor

## Output format: a graph visualization in text

### 1. Executive summary card
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ {Name}                                                 ┃
┃ Current: {Title} @ {Current Company Ticker}            ┃
┃ Tenure: {years}  Equity: ${holdings}                   ┃
┃ Other boards: {N}  Prior CEOs: {M}  Patents: {P}       ┃
┃ Papers: {K}  NIH grants: ${grants}                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### 2. Board network (table)

| Company | Role | Since | Equity Value | Committees |
|---------|------|-------|-------------:|-----------|

### 3. Career timeline (table)

| Years | Company | Role | Exit Reason |
|-------|---------|------|-------------|

### 4. Academic + research network

| Papers (top 10 by citation) | NIH grants | Co-authors (top 5) |

### 5. Hidden connections analysis
AI-identified non-obvious links:
- "Serves on board of [X] AND also on board of [Y] — both in competing industries"
- "Former CEO of [A] which was acquired by [B] in 2019 — now sits on board of [C] which is a supplier to [B]"
- "Co-authored 7 papers with [fellow researcher] who is CSO at [competitor biotech]"

### 6. Interlocking directorate flag
If executive serves on boards of 2+ companies that could have conflicts of interest (direct competitors, supplier-customer, joint-venture partners), flag this prominently.

## Data source + procedure

### Step 1: Get current role
Start with the company's DEF 14A proxy statement:
```
GET https://data.sec.gov/submissions/CIK{cik}.json  # find latest DEF 14A
```

Parse the proxy for executive officers and directors with their bios.

### Step 2: Find other board seats (the key step)
Use SEC EDGAR full-text search to find EVERY proxy statement mentioning this person:
```
GET https://efts.sec.gov/LATEST/search-index?q="{full name}"&forms=DEF+14A
```

Returns all companies that disclose this person in their proxy — which captures board seats across the entire US market.

### Step 3: Parse each DEF 14A for this person's role
Extract "Independent Director since {year}" or "Chairman of {committee}" or equivalent.

### Step 4: Academic + grant lookups
- PubMed: `/skill pubmed-paper-scan "{last name} {first initial}[Author]"`
- NIH: `/skill nih-grant-scan --pi-names="{Last, First}"`

### Step 5: Patent search
```
GET https://developer.uspto.gov/api-catalog/patent-application-data  # or similar
```

Query by inventor name.

### Step 6: Synthesize + flag hidden connections
Use graph reasoning to identify non-obvious relationships.

## Example invocation

User: "Tell me about Stéphane Bancel — full background"

The skill should:

1. Identify Stéphane Bancel as CEO of Moderna (MRNA, CIK 0001682852)
2. Search for all DEF 14A filings mentioning his name → find additional board roles
3. Pull PubMed for his publication history
4. Pull NIH RePORTER for any grants he's been a co-PI on
5. Pull USPTO patents listing him as inventor
6. Return:
   ```
   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Stéphane Bancel (MD, MBA)                              ┃
   ┃ Current: CEO @ MRNA (Moderna Inc)                      ┃
   ┃ Tenure: 15.0 years  Equity: ~$1.2B                     ┃
   ┃ Other boards: 2  Prior CEOs: 2  Patents: 8 as inventor ┃
   ┃ Papers: 42  NIH grants: $0 (none as PI)                ┃
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

   Board roles (from proxy cross-search):
   | Moderna Therapeutics Inc (MRNA) | Director + CEO | 2011 → present | $1.2B equity |
   | MedStar Health                  | Independent Dir | 2022 → present | N/A (private) |
   | Flagship Pioneering (PE)        | Partner         | 2015 → present | LP units |

   Career timeline:
   | 2000-2002 | Eli Lilly & Co   | Sales leadership (joined after MBA) |
   | 2002-2011 | bioMérieux       | Various roles, ultimately CEO      |
   | 2011-present | Moderna       | CEO                                 |

   Academic + research network:
   • Education: MIT (MBA), Grande École Centrale Paris (MS Biochemical Engineering)
   • 42 co-authored papers on mRNA therapeutics (2015-2026)
   • Top co-authors: Dr. Tal Zaks (former CMO Moderna), Dr. Stephen Hoge (President Moderna)
   • Not a NIH grant recipient (executive, not academic PI)
   • Patents: 8 US patents as co-inventor on mRNA delivery systems (formulation + lipid nanoparticles)

   Hidden connections:
   🔗 Moderna's mRNA platform derives from academic work at Harvard (Derrick Rossi lab) and BIDMC — Bancel was the commercialization architect, not the scientific originator
   🔗 His Flagship Pioneering partnership means he's seen 100+ biotech pitches; maintains close relationships with VCs at Flagship (including Noubar Afeyan, Moderna co-founder)
   🔗 Salary package: ~$3M base + $15M stock options annually — among the top 5% of public biotech CEO comp

   Interlocking directorate: None flagged (MedStar is nonprofit; Flagship is PE firm without public portfolio conflict)
   ```

## Why this is truly remarkable

**BoardEx** ($50k+/year) and **Equilar** ($20k+/year) sell this capability to activist investors and proxy advisors. They have specialized databases and full-time analysts maintaining the network graphs.

This skill builds the same graph from free public SEC EDGAR + PubMed + NIH + USPTO data.

For investigative journalists, M&A research teams, and activist investors — this is a career-changing tool.

## Honest caveats

- **Private company roles** are not always disclosed in public filings — the graph has blind spots
- **"Hidden connections" flagging** requires careful LLM reasoning; false positives possible
- **Name matching** — common names create ambiguity (which "John Smith"?); require disambiguation
- **Compensation data** is lagged by ~1 year (most recent proxy)

## License + source

Uses free public APIs + SEC EDGAR. Not a replacement for formal due diligence. MIT licensed.
