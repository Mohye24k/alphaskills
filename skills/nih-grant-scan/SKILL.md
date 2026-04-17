---
name: nih-grant-scan
description: Searches NIH RePORTER for grant awards by agency (NCI, NIAID, NIMH, NHLBI, etc.), principal investigator, institution, fiscal year, or keyword. Returns grant numbers, project titles, PIs, organizations, award amounts, abstracts, and funding mechanisms. Use when the user asks about NIH funding, biotech research funding, a researcher's grant history, recent grants in a field, institutional funding (Johns Hopkins, Broad, Stanford), biotech M&A due diligence targets, or KOL identification. Covers ~50,000 grants/year totaling ~$45 billion in US biomedical research funding. Uses the official free NIH RePORTER v2 API (api.reporter.nih.gov) with no key required. Replaces GrantForward ($300+/year), Pivot ProQuest ($2,000+/year institutional), and Lex Machina Grants Discovery ($5,000+/year).
---

# NIH Grants Tracker

## When to invoke

Trigger on any grant / research-funding question:

- "Who got NIH grants for CRISPR research?"
- "What are the biggest NCI grants this year?"
- "Show me Dr. X's grant history"
- "Recent NIH funding at Johns Hopkins"
- "R01 grants for Alzheimer's research"
- "Biotech startups with recent NIH SBIR awards"

## Required input (at least one)

- **Agency / Institute** — NIH institute code (see table below)
- **Search keywords** — searched across project title + abstract (e.g. `"CRISPR gene editing"`)
- **Principal investigator name** — e.g. `"Doudna, Jennifer"`
- **Organization name** — e.g. `"BROAD INSTITUTE, INC."`
- **Fiscal years** — array like `[2025, 2026]`

## Common NIH agency codes

| Code | Institute |
|------|-----------|
| `NCI` | National Cancer Institute (biggest NIH institute) |
| `NIAID` | National Institute of Allergy and Infectious Diseases |
| `NIMH` | National Institute of Mental Health |
| `NHLBI` | National Heart, Lung, and Blood Institute |
| `NINDS` | National Institute of Neurological Disorders and Stroke |
| `NICHD` | Child Health and Human Development |
| `NIA` | National Institute on Aging |
| `NIDDK` | Diabetes, Digestive, and Kidney Diseases |
| `NIDA` | National Institute on Drug Abuse |
| `NIGMS` | General Medical Sciences |
| `NEI` | National Eye Institute |
| `NIDCR` | Dental and Craniofacial Research |
| `NIBIB` | Biomedical Imaging and Bioengineering |
| `NIAMS` | Arthritis, Musculoskeletal, and Skin |
| `NIEHS` | Environmental Health Sciences |

Pass an empty agency list to search all of NIH.

## Activity codes (for understanding grant types)

| Code | Type | Typical size |
|------|------|-------------|
| `R01` | Research Project Grant (the gold standard) | $250k-500k/year × 3-5 years |
| `R21` | Exploratory / Developmental Research | $275k total over 2 years |
| `R13` | Conference / Meeting Grant | $5-50k one-time |
| `P01` | Program Project | $5-15M over 5 years |
| `P30` | Center Core Grants | $1-5M/year |
| `U01` | Cooperative Agreement (NIH + investigator) | Varies |
| `K99/R00` | Pathway to Independence (early-career) | $240k total |
| `T32` | Institutional Training Grant | $200-500k/year |
| `F31/F32` | Fellowships (predoc / postdoc) | $50-70k/year |
| `SBIR` | Small Business Innovation Research | $500k-2M over 2 years |

R01 + P01 + U01 grants are the most commercially interesting — they typically fund the kind of academic research that becomes licensed IP for biotech startups.

## Output format

### 1. Summary
`"Found {N} NIH grants matching {criteria}. Total funding: ${total_USD}. Top institutions: [list]. Top PIs: [list]."`

### 2. Grants table

| Grant # | PI | Institution | Title | FY | Amount |
|---------|-----|-------------|-------|----|-------:|

Sort by total cost descending. Cap at 15 rows.

### 3. Notable highlights
- **Largest grants** (>$1M single-year) — these are program projects or mega-grants
- **Emerging PIs** — early-career researchers with multiple grants
- **Concentration** — if one institution or PI dominates, call it out

### 4. KOL identification (for biotech due-diligence users)
List the top 5 PIs by total funding in this search. These are the field's key opinion leaders and the people biotech startups will want to license IP from or recruit to SABs.

## Data source + procedure

Query the NIH RePORTER v2 API:

```
POST https://api.reporter.nih.gov/v2/projects/search
Content-Type: application/json

{
  "criteria": {
    "include_active_projects": true,
    "agencies": ["NCI"],
    "fiscal_years": [2026],
    "advanced_text_search": {
      "operator": "and",
      "search_field": "all",
      "search_text": "CRISPR gene editing"
    },
    "pi_names": [{ "any_name": "Doudna, Jennifer" }],
    "org_names": ["BROAD INSTITUTE, INC."]
  },
  "limit": 500,
  "offset": 0,
  "sort_field": "project_start_date",
  "sort_order": "desc"
}
```

### IMPORTANT: do NOT pass `include_fields`

NIH RePORTER's `include_fields` parameter has surprising case sensitivity and using it incorrectly silently drops fields from the response. **Omit this parameter** to get the default field set, which includes everything you need.

### Key response fields

For each grant in `results[]`:

- `appl_id` — application ID (use to build URL: `https://reporter.nih.gov/project-details/{appl_id}`)
- `project_num` — full grant number (e.g. `"1R01CA290000-01A1"`)
- `core_project_num` — base grant number (e.g. `"R01CA290000"`)
- `project_title` — title
- `principal_investigators[0]` — has `first_name`, `last_name`, `email` (sometimes)
- `organization` — `org_name`, `org_city`, `org_state`, `org_country`, `dept_type`
- `agency_ic_admin.code` / `.name` — administering institute
- `fiscal_year`
- `award_amount` — total dollars (NOT thousands)
- `direct_cost_amt`, `indirect_cost_amt`
- `funding_mechanism` — human-readable mechanism name
- `activity_code` — the R01, R21, P01, etc.
- `project_start_date`, `project_end_date`
- `cfda_code` — Catalog of Federal Domestic Assistance number
- `cong_dist` — Congressional district (useful for geographic targeting)
- `pref_terms` / `terms` — NIH's classification keywords
- `abstract_text` — full scientific narrative
- `project_detail_url` — direct link

## Example invocation

User: "Who's getting big NIH grants for CRISPR research?"

The skill should:
1. Query with `advanced_text_search.search_text="CRISPR"` + `fiscal_years=[2026]`
2. Filter/sort by award amount
3. Return:
   ```
   Found 4,886 NIH grants mentioning CRISPR in FY2026. Total funding: $1.87B.

   Top 5 by award size:
   | 1R01HL152789 | Johnson, Erik Christopher | JOHNS HOPKINS UNIVERSITY | Drug Research Organoid-Integrated Development Platform (DROIDp) | FY2026 | $2,946,887 |
   | 1R01HL156432 | Baconguis, Isabelle Rhyssa | OREGON HEALTH & SCIENCE | Optimizing cAMP and PKA sensors for cell-specific neuron dissection | FY2026 | $2,039,804 |
   | 1R01HL145210 | Musunuru, Kiran | UNIVERSITY OF PENNSYLVANIA | Therapeutic editing for cardiovascular diseases | FY2026 | $1,137,435 |

   Top institutions: Broad Institute (43 grants), UC San Francisco (38), MIT (29), Johns Hopkins (24), UPenn (22)

   KOLs: Dr. Kiran Musunuru (UPenn) — cardiovascular gene editing, has $3.4M in active CRISPR grants and is a founder of Verve Therapeutics (NASDAQ: VERV). Likely M&A target discussion point.
   ```

## Relationship to AlphaStack portfolio

Corresponds to the `nih-grants-tracker` Apify actor (`yIggbYCqNgMPLTl37`).
