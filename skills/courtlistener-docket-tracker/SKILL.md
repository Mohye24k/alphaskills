---
name: courtlistener-docket-tracker
description: Searches federal and state court filings through the CourtListener API (Free Law Project's open database mirroring PACER). Returns case name, court, docket number, filing date, judge, nature of suit, parties, and recent docket entries. Use when the user asks about federal court cases, patent lawsuits, securities litigation, class-actions, federal court docket, specific judges or courts (SDNY, CAFC, DDC), or wants to track litigation against a specific company. Covers 5M+ federal cases, every circuit court of appeals, the Supreme Court, and most federal district courts. Uses the CourtListener REST API v4 — requires a free API token from courtlistener.com. Replaces Westlaw ($500+/month), LexisNexis ($500-2k/month), PACER direct ($0.10/page metered), and Bloomberg Law ($150/month).
---

# CourtListener Federal Court Tracker

## When to invoke

Trigger on any litigation / court case question:

- "Any patent lawsuits against Apple lately?"
- "Securities class-actions in SDNY"
- "Supreme Court recent opinions on antitrust"
- "Federal Circuit patent appeals"
- "What is Elon Musk being sued for?"
- "Litigation against Tesla"

## Required input (at least one)

- **Case name** — substring search across case titles
- **Party name** — company or person (defendant or plaintiff)
- **Court** — short ID like `scotus` (SCOTUS), `cafc` (Federal Circuit), `nysd` (SDNY), `dcd` (DDC), `txed` (EDTX)
- **Nature of suit code** (NOS) — e.g. `830` (Patent), `150` (Contract), `850` (Securities)
- **Filing date range**

## Common court IDs

| ID | Court |
|----|-------|
| `scotus` | Supreme Court of the United States |
| `ca1`–`ca11`, `cadc`, `cafc` | Circuit Courts (1-11, DC, Federal) |
| `nysd` | Southern District of New York |
| `nyed` | Eastern District of New York |
| `cacd` | Central District of California |
| `cand` | Northern District of California |
| `dcd` | District of Columbia |
| `dedb` | District of Delaware |
| `txed` | Eastern District of Texas (patent hub) |
| `deb` | Delaware Bankruptcy |
| `flsd` | Southern District of Florida |

## Common Nature of Suit codes

| NOS | Meaning |
|-----|---------|
| `150` | Contract |
| `190` | Other Contract |
| `320` | Assault/Libel/Slander |
| `380` | Personal Property Damage |
| `440` | Other Civil Rights |
| `830` | Patent |
| `840` | Trademark |
| `850` | Securities/Commodities/Exchange |
| `870` | Taxes |
| `890` | Administrative Procedure |

## Output format

### 1. Summary
`"Found {N} cases matching {criteria}. Active: {a}, Closed: {c}. Courts: {list}."`

### 2. Cases table

| Filed | Court | Case Name | Docket # | NOS | Judge | Status |
|-------|-------|-----------|----------|-----|-------|--------|

Sort by filing date descending. Cap at 20. Link each case to its CourtListener URL.

### 3. Recent docket activity (if user asks about a specific case)
List the last 10 docket entries with date + description.

## Data source + procedure

Requires a free API token: `curl -u 'user:pass' https://www.courtlistener.com/api/rest/v4/token/` to generate.

### Search dockets

```
GET https://www.courtlistener.com/api/rest/v4/dockets/?court={court_id}&case_name__icontains={name}&filed_after={date}&ordering=-date_filed
Authorization: Token {api_token}
```

Response `results[]` with:

- `id` — CourtListener docket ID
- `case_name` / `case_name_short`
- `docket_number` — official docket (e.g. `"1:24-cv-01234"`)
- `court` — court URL (query separately for name)
- `date_filed` — ISO date
- `assigned_to_str` — judge name
- `nature_of_suit` — numeric NOS code + human-readable
- `parties[]` — plaintiffs + defendants
- `absolute_url` — CourtListener permalink

### Fetch docket entries for a specific case

```
GET https://www.courtlistener.com/api/rest/v4/docket-entries/?docket={docket_id}&ordering=-date_filed
```

Returns `results[]` with `entry_number`, `date_filed`, `description`, `recap_documents[]` (if filing is in RECAP).

## Example invocation

User: "Any patent lawsuits against Apple lately?"

The skill should:
1. Search dockets with `party_name=Apple` + `nature_of_suit=830` + date range last 90 days
2. Return:
   ```
   Found 12 patent cases with Apple as a party, filed 2026-01-16 to 2026-04-16.

   | 2026-04-02 | txed | Maxell Ltd. v. Apple Inc. | 2:26-cv-00234 | 830 | J. Gilstrap | Active |
   | 2026-03-18 | ded  | Nokia Solutions v. Apple Inc. | 1:26-cv-00478 | 830 | J. Andrews | Active |
   | 2026-02-28 | cacd | Apple Inc. v. Masimo Corp | 2:26-cv-01089 | 830 | J. Selna | Active (Apple as plaintiff) |
   ...

   Pattern: EDTX remains the venue of choice for patent plaintiffs against Apple. Apple's Masimo case in CACD (Apple as plaintiff) is the continuation of the long-running Apple Watch pulse oximeter dispute.
   ```

## Honest caveats

- **RECAP (open PACER mirror) has gaps** — not every filing is mirrored, especially sealed documents, newer state court filings, and pre-2001 cases
- **CourtListener is a community-funded project** — bulk scraping should be polite; API rate limits apply
- **Case name search is fuzzy** — use quotes for exact matches: `case_name__icontains='"Apple Inc."'`

## License + source

CourtListener data is public record (federal court filings). The Free Law Project operates CourtListener as a non-profit; consider donating if you use heavily. API token obtained free at courtlistener.com/signup/.
