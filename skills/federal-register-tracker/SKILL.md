---
name: federal-register-tracker
description: Searches and monitors the US Federal Register — the daily publication of every federal agency rule, proposed rule, notice, and presidential document. Returns document number, agency, publication date, comment period deadlines, effective dates, and CFR citations. Use when the user asks about new federal regulations, pending rulemakings, public comment deadlines, agency actions (EPA, FDA, SEC, FTC, CFPB, DOT, DOE), regulatory compliance tracking, or mentions Federal Register notices. Covers ~80,000 documents per year from 400+ federal agencies. Uses the official free federalregister.gov REST API (api.federalregister.gov/v1) with no key required. Replaces Bloomberg Government ($5-25k/year), LexisNexis Regulatory ($500-2k/month), Westlaw, and Politico Pro ($599/month).
---

# Federal Register Tracker

## When to invoke

Trigger on any regulatory / rulemaking question:

- "What new EPA regulations were published this week?"
- "Any new SEC rules proposed on cryptocurrency?"
- "FDA approval publications in the last 30 days"
- "Federal Register comment deadlines approaching"
- "FTC merger guidance updates"
- "New CFPB rules on credit reporting"

## Required input (at least one)

- **Agency** — name or acronym (`EPA`, `FDA`, `SEC`, `FTC`, `CFPB`, `DOT`, `DOE`, `DOL`, `TREAS`, `USDA`, etc.)
- **Search term** — free text across document title and abstract
- **Document type** — `rule` / `proposed_rule` / `notice` / `presidential_document`
- **Date range** — start + end dates (ISO format)

## Output format

### 1. Summary
`"Found {N} Federal Register documents matching {criteria} from {start} to {end}. Comment periods open for {X} proposed rules."`

### 2. Documents table

| Date | Agency | Type | Title | Comment Deadline |
|------|--------|------|-------|------------------|

Sort by publication date descending. Cap at 20. Mark OPEN comment periods with ⏳ and CLOSED with ✓.

### 3. High-impact highlights
Flag documents matching any of these criteria:
- **Significant rule** — economic impact >$100M/year (designated in abstract)
- **Major rulemaking** — Congressional review act applies
- **Executive orders** — presidential documents
- **Comment deadlines in next 14 days** (last-chance actions)

## Data source + procedure

Query the Federal Register API:

```
GET https://www.federalregister.gov/api/v1/documents.json?conditions[agencies][]={agency}&conditions[term]={search_term}&conditions[type][]={type}&conditions[publication_date][gte]={start}&conditions[publication_date][lte]={end}&per_page=100
```

Key response fields per document:

- `document_number` — the official ID (e.g. `"2026-07234"`)
- `title` — the document title
- `abstract` — summary (often includes economic impact data)
- `type` — `Rule`, `Proposed Rule`, `Notice`, `Presidential Document`
- `agencies[]` — array of agencies (name + slug)
- `publication_date` — ISO date
- `effective_on` — when rule takes effect (if applicable)
- `comments_close_on` — comment period deadline (if applicable)
- `significant` — boolean flag for "Significant" rules
- `html_url` — federalregister.gov permalink
- `pdf_url` — direct PDF
- `cfr_references[]` — CFR parts affected
- `regulation_id_numbers[]` — RINs from the Unified Agenda

## Common agency slugs

| Slug | Agency |
|------|--------|
| `environmental-protection-agency` | EPA |
| `securities-and-exchange-commission` | SEC |
| `food-and-drug-administration` | FDA |
| `federal-trade-commission` | FTC |
| `consumer-financial-protection-bureau` | CFPB |
| `commodity-futures-trading-commission` | CFTC |
| `federal-reserve-system` | Fed |
| `internal-revenue-service` | IRS |
| `department-of-labor` | DOL |
| `department-of-transportation` | DOT |
| `federal-aviation-administration` | FAA |
| `department-of-energy` | DOE |

Use `GET /api/v1/agencies.json` to discover the full list.

## Example invocation

User: "Any new SEC rules on cryptocurrency this quarter?"

The skill should:
1. Query with `agency=securities-and-exchange-commission` + `term=cryptocurrency OR digital asset` + `publication_date gte 2026-01-01`
2. Return:
   ```
   Found 8 SEC documents on cryptocurrency from 2026-01-01 to 2026-04-16.
   Comment periods open for 3 proposed rules.

   | 2026-04-02 | SEC | Proposed Rule | Custody of Digital Asset Securities | ⏳ 2026-06-01 |
   | 2026-03-15 | SEC | Final Rule | Exchange Registration for Alt Trading Systems | ✓ Closed |
   | 2026-02-28 | SEC | Notice | Staff No-Action Letter on Staking Rewards | N/A |
   ...

   High-impact highlights:
   • 2026-04-02 Custody rule — economic impact >$100M. Proposed rule with 60-day comment period, deadline June 1. Directly affects every major crypto exchange and custodian.
   ```

## Comment period strategy

When the user is in compliance/GR/legal, highlight:
- **Comment deadline < 14 days**: urgent, file now
- **Comment deadline 15-60 days**: standard period, prepare response
- **Post-deadline**: rule moving to final; no more public input

## License + source

Federal Register data is public domain. Uses federalregister.gov v1 API, maintained by the National Archives and Government Publishing Office. No key required.
