---
name: clinical-trial-intel
description: Queries the FDA-regulated clinical trial registry (ClinicalTrials.gov) for any disease, drug, sponsor, phase, or status. Returns structured trial data including Phase 1/2/3/4 classification, enrollment count, sponsor (Pfizer, Moderna, Eli Lilly, etc.), start/completion dates, lead investigator, and study sites. Use when the user asks about clinical trials for a disease (cancer, Alzheimer's, obesity, diabetes), wants a drug's development stage (donanemab, semaglutide, pembrolizumab), needs a pharma company's pipeline, asks "what trials are recruiting for X", researches a biotech company's pipeline, or wants to track Phase 3 readouts. Uses the official free NIH/NLM ClinicalTrials.gov API v2 with no key required. Replaces Citeline Trialtrove ($25-100k/year), GlobalData Clinical Trials ($30k/year), and Evaluate Pharma ($50k/year).
---

# ClinicalTrials.gov Pharma Pipeline Intel

## When to invoke

Trigger on any clinical-trial question:

- "What trials are in Phase 3 for Alzheimer's?"
- "Show me Eli Lilly's current pipeline"
- "Is there a trial for drug X?"
- "What Phase 3 cancer trials are recruiting?"
- "Pfizer obesity pipeline?"
- "CAR-T trial landscape"
- "GLP-1 drugs in development"

## Required input (at least one)

- **Condition** (disease/indication) — e.g. `"pancreatic cancer"`, `"Alzheimer's"`, `"obesity"`, `"type 2 diabetes"`
- **Intervention** (drug/therapy) — e.g. `"semaglutide"`, `"donanemab"`, `"CAR-T"`, `"CRISPR"`, `"GLP-1"`
- **Sponsor** (company/institution) — e.g. `"Eli Lilly"`, `"Moderna"`, `"Pfizer"`, `"Regeneron"`

## Optional filters

- **Phases**: array of `EARLY_PHASE1`, `PHASE1`, `PHASE2`, `PHASE3`, `PHASE4`
- **Statuses**: `RECRUITING`, `ACTIVE_NOT_RECRUITING`, `COMPLETED`, `TERMINATED`, etc.
- **Country**: filter locations
- **Max results** (default 50)

## Output format

### 1. Summary
`"Found N trials matching [criteria]. Phases: P1={x}, P2={y}, P3={z}, P4={w}. Top sponsors: [list]."`

### 2. Trial table

| NCT ID | Phase | Sponsor | Drug/Intervention | N | Status | Primary End |
|--------|-------|---------|-------------------|---:|--------|-----------|

Sort by primary completion date ascending (soonest catalysts first). Cap at 20 rows unless user asks for more.

### 3. Notable trials / catalysts
Flag:
- **Imminent readouts** (primary completion in next 6 months + ACTIVE_NOT_RECRUITING status = binary event)
- **Large Phase 3 trials** (>5,000 enrollment = typically a CV outcomes trial or mega-registrational)
- **Terminated trials** (negative signal for the drug/sponsor)
- **Cross-sponsor collaborations**

### 4. KOL identification (when user asks about investigators)
List the top 5 principal investigators by trial count. Useful for biotech sales, recruiting, and partnership discovery.

## Data source + procedure

Query the official ClinicalTrials.gov API v2:

```
GET https://clinicaltrials.gov/api/v2/studies?format=json&pageSize=100&query.cond={condition}&query.intr={intervention}&query.lead={sponsor}&filter.advanced=AREA[Phase]({phases})+AND+AREA[OverallStatus]({statuses})
```

Parse the JSON response. Each study has a `protocolSection` with:

- `identificationModule.nctId` — the unique NCT ID
- `identificationModule.briefTitle` / `officialTitle`
- `statusModule.overallStatus` — RECRUITING, ACTIVE_NOT_RECRUITING, COMPLETED, etc.
- `designModule.phases` — array of phases
- `designModule.enrollmentInfo.count` — enrollment target
- `sponsorCollaboratorsModule.leadSponsor.name` + `.class` (INDUSTRY / NIH / OTHER)
- `conditionsModule.conditions` — array of disease names
- `armsInterventionsModule.interventions` — array of drugs/therapies
- `statusModule.startDateStruct.date` and `statusModule.primaryCompletionDateStruct.date`
- `contactsLocationsModule.overallOfficials` — principal investigators
- `contactsLocationsModule.locations` — study sites (cap at 100 per study)

Use pagination via `nextPageToken` for result sets >100.

## Phase meanings (for interpretation)

| Phase | Typical enrollment | What it tests |
|-------|-------------------|---------------|
| Early Phase 1 / Phase 1 | 20-100 | Safety, dose range, pharmacokinetics |
| Phase 2 | 100-500 | Efficacy signal, optimal dose |
| Phase 3 | 500-30,000 | Registrational — what FDA approves on |
| Phase 4 | varies | Post-approval, new indications, long-term safety |

Phase 3 completion = catalyst. Most Phase 3 trials have a binary outcome that moves the sponsor's stock 30-80%.

## Key facts

- **Not real-time**: sponsors update their records with lag (sometimes weeks)
- **No results data**: this API returns protocol data only. Efficacy/safety results are in a separate module we don't query.
- **Global coverage**: US, EU, China, Japan, and many other countries
- **500,000+ trials total** registered historically

## Example invocation

User: "What's Eli Lilly's Phase 3 pipeline?"

The skill should:
1. Query with `query.lead="Eli Lilly"` + `filter.advanced=AREA[Phase](PHASE3)` + `AREA[OverallStatus](RECRUITING OR ACTIVE_NOT_RECRUITING)`
2. Return:
   ```
   Eli Lilly Phase 3 pipeline (5 active trials):
   • Donanemab (Alzheimer's) — 1,500 pts, completing 2027-01
   • Lepodisiran (CV outcomes) — 17,300 pts, 932 sites — MEGA TRIAL
   • Eloralintide (sleep apnea + obesity) — 800 pts
   • Olomorasib (KRAS NSCLC) — 700 pts
   • Baricitinib (Type 1 diabetes delay) — 150 pts

   Key catalyst: Donanemab primary completion Jan 2027 (biggest Alzheimer's binary since Leqembi)
   ```

## Relationship to AlphaStack portfolio

Corresponds to the `clinicaltrials-pipeline-monitor` Apify actor (`btthlRTMvlHbR7ytK`).
