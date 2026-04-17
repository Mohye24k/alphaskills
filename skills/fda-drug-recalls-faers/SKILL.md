---
name: fda-drug-recalls-faers
description: Searches FDA drug recalls, enforcement actions, and adverse event reports (FAERS — FDA Adverse Event Reporting System). Returns recall classification (Class I/II/III), recalling firm, products, reasons, distribution patterns, and aggregate adverse event counts by drug name or manufacturer. Use when the user asks about drug recalls, pharmacovigilance, drug safety signals, adverse event reports for a specific drug, FDA enforcement actions, pharma company recall history, or class-action drug cases (Ozempic, Zantac, Tylenol, etc.). Uses the free official openFDA API (api.fda.gov) which aggregates FDA's enforcement reports and FAERS case reports. API key optional (higher rate limits if provided). Replaces Veeva Vault RIM ($50-500k/year), Dyad Pharmacovigilance systems, and IQVIA adverse event databases.
---

# FDA Drug Recalls + Adverse Events (FAERS)

## When to invoke

Trigger on drug safety / recall / adverse event questions:

- "Any recalls on Metformin?"
- "Adverse events for Ozempic"
- "FDA enforcement actions against Johnson & Johnson"
- "Drug safety signals for Ambien"
- "Class I recalls this quarter"
- "Tylenol adverse event reports"

## Required input (at least one)

- **Drug name** — generic or brand (`semaglutide`, `Ozempic`, `metformin`, etc.)
- **Manufacturer / firm** — company name
- **Recall class** — `I` (serious injury/death risk), `II` (possible reversible harm), `III` (unlikely to cause harm)
- **Date range** — start + end dates

## Two data sources, one skill

This skill queries two openFDA endpoints:

### 1. Drug recalls (drug/enforcement)

```
GET https://api.fda.gov/drug/enforcement.json?search=product_description:{drug}+AND+recalling_firm:{firm}+AND+report_date:[{start}+TO+{end}]&limit=100
```

Key fields per recall:

- `recall_number` — FDA tracking ID
- `classification` — `Class I`, `Class II`, `Class III`
- `product_description` — the recalled product
- `reason_for_recall` — cause (contamination, mislabeling, CGMP, potency, etc.)
- `recalling_firm` — manufacturer
- `distribution_pattern` — geographic scope
- `status` — `Ongoing`, `Completed`, `Terminated`
- `recall_initiation_date` / `report_date`
- `code_info` — lot numbers affected
- `voluntary_mandated` — voluntary vs FDA-mandated

### 2. Adverse event reports (drug/event — FAERS)

```
GET https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{drug}&count=patient.reaction.reactionmeddrapt.exact&limit=100
```

Returns aggregate counts of reactions reported for a given drug — the classic pharmacovigilance "signal detection" query.

## Output format

### 1. Recall summary
`"Found {N} recalls for {drug/firm} from {start} to {end}. Class I: {x}, Class II: {y}, Class III: {z}. Ongoing: {z}, Completed: {w}."`

### 2. Recalls table

| Date | Class | Product | Firm | Reason | Status |
|------|-------|---------|------|--------|--------|

Sort by date descending. Cap at 15 rows.

### 3. Top adverse reactions table (FAERS data)

| Reaction | Report Count |
|----------|-------------:|

Sort by count descending. Top 20 reactions for the drug.

### 4. Signal interpretation
- **Class I recalls** = regulatory red flag, often stock-moving
- **Multiple Class II/III recalls in <12 months** = systemic CGMP or quality issue
- **Unusually high specific reaction count** = potential safety signal (caveat: FAERS is disproportional, not causal)

## Honest limitations (always note when reporting FAERS)

- **FAERS is spontaneous reporting** — counts reflect what's reported, not incidence
- **Underreporting is massive** — estimated 1-10% of actual adverse events get reported
- **No denominators** — you don't know how many patients take the drug, so rates are not directly computable
- **Self-reported** — many reports come from consumers or lawyers, not validated physicians
- **Disproportionality analysis (PRR, ROR) is the standard** — but requires a proper signal detection framework, not just raw counts

## Example invocation

User: "Any recalls on Metformin?"

The skill should:
1. Query `drug/enforcement` with `product_description:metformin`
2. Query `drug/event` aggregating reactions for metformin
3. Return:
   ```
   Found 43 Metformin recalls 2024-01-01 to 2026-04-16.
   Class I: 2, Class II: 38, Class III: 3.

   Recent notable recalls:
   | 2025-11-15 | II | Metformin HCl ER 500mg | Granules India | NDMA impurity >FDA limit | Ongoing |
   | 2025-08-22 | II | Metformin HCl 1000mg | Amneal Pharma | NDMA impurity >FDA limit | Completed |
   | 2024-12-03 | II | Metformin ER 750mg | Lupin Pharmaceuticals | NDMA impurity | Completed |

   Top FAERS reactions for metformin (all-time):
   | Lactic acidosis | 12,487 |
   | Hypoglycaemia | 8,234 |
   | Diarrhoea | 5,123 |
   | Renal impairment | 3,876 |
   ...

   Pattern: NDMA (nitrosamine impurity) has been the dominant metformin recall driver since 2019 — this is a generic-manufacturer supply chain quality issue, not a class-action target for the drug itself.
   ```

## Related class-action targeting

For plaintiff firms, flag drugs with pattern:
- Multiple Class I recalls
- Rapidly rising FAERS counts for the same reaction
- SEC 8-K Item 2.06 (material impairment) by the manufacturer
- Ongoing FDA consent decrees

## License + source

openFDA is public domain. API key optional from open.fda.gov/apis/authentication but not required for most reasonable-volume queries.
