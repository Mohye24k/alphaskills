---
name: drug-affordability-rescue
description: A drug affordability rescue tool for patients facing catastrophic drug costs. Takes any prescription drug name and returns — in order — generic alternatives with prices, FDA-approved biosimilars, Patient Assistance Programs (PAPs) from the manufacturer, GoodRx-style coupon estimates, 340B pricing availability at safety-net hospitals, Canadian/Mexican legal import options, cheaper therapeutic substitutes (different drug, same indication, 10× cheaper), FDA drug shortage alternatives, and critically — active manufacturer-sponsored savings programs with current eligibility. Use when a patient / caregiver asks about insulin costs, GLP-1 (Ozempic/Wegovy) affordability, cancer drug copays, rare disease therapy access, asthma inhaler prices, HIV PrEP access, or any specific drug cost. This is the information the pharmaceutical industry and insurance companies spend millions making hard to find. Free from FDA openFDA + patientassistanceprograms.gov + NIH Drug Information Portal data.
---

# Drug Affordability Rescue — $15k/year Insulin → $35/month Alternative

## This skill exists because:

- 1 in 4 Americans skips prescriptions they can't afford
- 30% of diabetics ration insulin despite it being $3/vial to produce (manufacturers charge $300+/vial)
- Cancer patients file bankruptcy at 2.5× the rate of the general population
- Most patients never find out that **Eli Lilly offers $35/month insulin directly**, or that **their specific drug has a free patient assistance program**

This skill surfaces every pathway to afford a drug — in priority order by savings magnitude.

## When to invoke

Trigger on any drug-cost question:

- "I can't afford my insulin"
- "Ozempic costs $1,400/month — alternatives?"
- "Cheap alternatives to Humira"
- "My kid needs enzyme replacement therapy, it's $500k/year"
- "Cost of Trulicity vs generics"
- "Patient assistance programs for Keytruda"

## Required input

- **Drug name** (brand or generic) — e.g. `Ozempic`, `semaglutide`, `Humira`, `Keytruda`, `Lantus`

## Optional (improves output relevance)

- **Current price** the patient is paying
- **Insurance status** (private, Medicare, Medicaid, uninsured)
- **State / country** (for pharmacy-level pricing comparison)
- **Indication** (what they're taking it for — affects whether generics work)

## Output format — ordered by savings magnitude

### 1. Summary line
`"[Drug] costs ~$X/month at typical retail. Best-case cost through alternatives: ~$Y/month. Potential savings: $Z/year."`

### 2. Rescue ladder (highest savings first)

```
╔══════════════════════════════════════════════════════════════╗
║  RESCUE LADDER — [Drug Name]                                 ║
╠══════════════════════════════════════════════════════════════╣

🪜 TIER 1 — GENERIC / BIOSIMILAR (usually 80-95% cheaper)
  
  ✓ Insulin Glargine (Semglee) — FDA-approved biosimilar for Lantus
    Cost: $35-80/vial vs Lantus $300/vial
    Savings: 75-85%
    How: Ask pharmacist; most insurers substitute automatically.

🪜 TIER 2 — MANUFACTURER PATIENT ASSISTANCE PROGRAM
  
  ✓ Eli Lilly Insulin Value Program
    Cost: $35/month for ANY Lilly insulin (Humalog, Basaglar, Lyumjev)
    Eligibility: Any patient regardless of income or insurance
    How: Show pharmacist the Lilly savings card (enroll at
         insulinaffordability.com)
  
  ✓ Sanofi Valyou Savings Program
    Cost: $35/month for Lantus / Toujeo
    Eligibility: Uninsured + commercially insured (not Medicare/Medicaid)

🪜 TIER 3 — GOODRX / COUPON
  
  ✓ GoodRx Gold: $19.99/month subscription; Lantus ~$230 with coupon
  ✓ SingleCare: similar, no subscription
  ✓ NeedyMeds: coupons + full PAP directory

🪜 TIER 4 — THERAPEUTIC ALTERNATIVES (different drug, same outcome)
  
  ✓ Metformin (Type 2 DM, pre-insulin) — $4/month generic. Talk to your
     doctor about whether metformin + GLP-1 combo can delay insulin.
  ✓ For Type 2 DM: GLP-1 agonists (Ozempic/Trulicity/Mounjaro) may lower
     HbA1c enough that basal insulin is reduced. (Note: those are also
     expensive — see their own rescue ladder.)

🪜 TIER 5 — LEGAL IMPORT (cross-border)
  
  ✓ Canadian price: ~$40/vial (1/8 of US price)
    • FDA "Personal Importation" policy allows 3 months supply for personal
      use from regulated countries (Canada, UK, EU) without prescription
      import license.
    • Pharmacies: CanadaDrugs.com, Canadian Pharmacy Online, Vanquish
    • Tax/shipping adds ~$30-50 total
  ✓ Mexican price: similar to Canadian
  ✓ WARNING: always verify pharmacy license with the Canadian Pharmacy
     Association (CIPA) — scammers exist.

🪜 TIER 6 — 340B HOSPITAL PHARMACY
  
  Large safety-net hospitals and Federally Qualified Health Centers (FQHCs)
  get 340B discounts. If you qualify for sliding-scale care, a 340B pharmacy
  may charge $10-30 for drugs that cost $300 elsewhere.
  
  Find a 340B: https://www.hrsa.gov/opa/about-340b

🪜 TIER 7 — FDA DRUG SHORTAGE ALTERNATIVES
  
  If your drug is in current FDA-listed shortage, there are often approved
  alternatives with different dosing or administration:
  
  [list any current shortages found in FDA's shortage database]

🪜 TIER 8 — EMERGENCY / LAST RESORT
  
  ✓ NeedyMeds.org — aggregated PAP directory
  ✓ RxHope.com — PAP application helper
  ✓ Partnership for Prescription Assistance — rxassist.org
  ✓ State pharmaceutical assistance programs (specific to each US state)
  ✓ Nonprofit free clinics — for the uninsured
  ✓ Clinical trial enrollment — drug is free during the trial
    (see patient-trial-navigator skill)
╚══════════════════════════════════════════════════════════════╝
```

### 3. Honest caveats

```
ALWAYS:
- Talk to your prescribing doctor before switching to an alternative
- Some biosimilars are not interchangeable — the pharmacy needs a new Rx
- Cross-border import works for most drugs but NOT controlled substances
- Medicare/Medicaid eligibility affects which PAPs you can use
- Manufacturer coupons are usually NOT valid with government insurance
```

## Data sources + procedure

This skill draws from 6 sources:

### 1. FDA openFDA for drug approvals + generics

```python
from alphaskills_py import fda

approvals = fda.drug_label_search(openfda_brand="Lantus")
# Check openfda.generic_name for the chemical substance — then find all
# branded + biosimilar drugs with the same generic_name
```

### 2. Manufacturer Patient Assistance Programs

Top manufacturers have PAPs with fixed pricing:

| Manufacturer | Program | Drug categories | Price |
|--------------|---------|-----------------|-------|
| Eli Lilly | Insulin Value Program | All Lilly insulins | $35/mo |
| Sanofi | Valyou Savings | Lantus, Toujeo | $35/mo |
| Novo Nordisk | NovoCare PAP | Insulins, GLP-1s | Varies |
| Novartis | Patient Assistance NOW | Oncology, rare disease | Free to qualifying |
| Pfizer | RxPathways | Multiple | Free to qualifying |
| Bristol-Myers Squibb | BMS Patient Assistance | Oncology | Free to qualifying |
| Merck | Merck Helps | Keytruda + others | Varies |
| AbbVie | myAbbVie Assist | Humira + others | Free to qualifying |
| Amgen | Amgen Assist | Biologics | Free to qualifying |
| Gilead | Advancing Access | HIV drugs, cancer | Varies |
| Roche/Genentech | Genentech Access Solutions | Oncology | Varies |
| Regeneron | MyWay | Biologics | Varies |

Hardcode these + their URLs (they rarely change).

### 3. GoodRx-style coupons

GoodRx doesn't have a public API but their prices can be scraped from goodrx.com/<drug-name> (honor their robots.txt). SingleCare, RxSaver, NeedyMeds have similar data.

### 4. Canadian price arbitrage

Use the PMPRB (Patented Medicines Price Review Board) data or canadapharmacy.com public listings. Canada regulates drug prices; they're 40-80% lower than US.

### 5. 340B eligibility

HRSA's 340B Office of Pharmacy Affairs publishes the list of covered entities. If a patient is within 25 miles of a 340B pharmacy AND qualifies for their sliding-scale care, 340B is the lowest-cost option.

### 6. FDA drug shortages

openFDA has a drug shortage endpoint showing current shortages and expected resolution dates. When the patient's drug is in shortage, the API suggests alternatives.

## Example invocation

User: "I can't afford my insulin — Lantus is $300/vial at my pharmacy"

The skill should:

1. Recognize "Lantus" = insulin glargine
2. Run the rescue ladder:
   - Tier 1: Semglee biosimilar ($35-80/vial)
   - Tier 2: Sanofi Valyou program ($35/month)
   - Tier 5: Canadian Lantus ($40/vial)
3. Return:
   ```
   Lantus costs $300/vial retail. Best-case: $35/month through Sanofi's
   own Valyou program. Annual savings vs retail: $3,180/year.

   Top 3 rescue options:
   1. ★ Sanofi Valyou Savings — $35/month for Lantus or Toujeo
      → Enroll at valyousavingsprogram.com
   2. Semglee (FDA biosimilar) — $35-80/vial at CVS/Walgreens
      → Ask pharmacist to substitute (requires new Rx)
   3. Canadian Lantus via CIPA-certified pharmacy — $40/vial
      → CanadaDrugs.com or Vanquish Pharmacy

   HONEST REALITY CHECK: Insulin costs $3/vial to produce. You're
   being overcharged. The $35/month programs exist because there
   was public outrage, not because the manufacturers volunteered.
   Use them without guilt.
   ```

## Why this is world-changing

A single diabetic who switches from $300/vial Lantus to $35/month Lantus (via Valyou) saves **$3,180/year**. For a family making $40k/year, that's 8% of their gross income. For 8.7 million diabetics on insulin in the US, this information is worth **$27.6 billion/year in aggregate savings**.

**The information already exists.** It's just scattered, obscured, and deliberately hard to find. This skill centralizes it.

## Relationship to AlphaSkills portfolio

Uses `alphaskills_py.fda` (existing) plus manufacturer PAP databases (hardcoded reference data in this skill).

## License + source

MIT. All sources are public information. The skill is free forever. Use it to help patients.
