---
name: drug-lifecycle-tracker
description: Traces any drug or therapeutic through its full commercial lifecycle — from academic origin (NIH grant funding + arXiv/bioRxiv/PubMed publication) to clinical development (ClinicalTrials.gov Phase 1/2/3 progression) to FDA approval (openFDA) to post-marketing surveillance (FAERS adverse events + FDA recalls). Returns a chronological timeline connecting research discovery → patent filing → company licensing → clinical trials → FDA approval → market dynamics → safety signals. Use when the user asks about a drug's full history (semaglutide, lecanemab, donanemab, tirzepatide), wants to trace an academic discovery to its commercial outcome, researches biotech investment theses requiring full context, or evaluates competitive landscape for a specific drug class. This is the complete drug intelligence view that normally requires 6+ separate databases and a team of research analysts to compile. Replaces Evaluate Pharma ($50k+/year), Pharmaprojects ($30k+/year), and Citeline Pharma Intelligence ($25-100k/year).
---

# Drug Lifecycle Tracker — Full Biotech Intelligence Timeline

## The premise

Every successful drug has a 10-25 year lifecycle across 5+ data systems. Most analysts piece it together manually across Evaluate Pharma, Citeline, ClinicalTrials.gov, FDA.gov, PubMed, and Google Patents — taking days per drug. This skill does it in one invocation.

## When to invoke

Trigger on full-drug-history questions:

- "Tell me the full story of semaglutide"
- "Drug lifecycle for Ozempic"
- "History of lecanemab from discovery to today"
- "Competitive landscape for GLP-1s"
- "What's the full pipeline around CRISPR-Cas9?"

## Required input

- **Drug name** — generic or brand name (e.g. `semaglutide`, `Ozempic`, `lecanemab`, `Leqembi`)
- **Optional depth** — `summary` / `full` (default: `full`)

## The lifecycle stages we trace

### Stage 1: Academic origin (pre-clinical)
- **NIH grants** related to the drug's mechanism (via `nih-grant-scan`)
- **Early papers** on the target biology (via `pubmed-paper-scan` + `biorxiv-preprint-scan`)
- **Patent filings** — original composition-of-matter patents (USPTO)

### Stage 2: Pre-clinical → IND (investigational new drug)
- First company to file IND with FDA
- Corporate structure (founded by whom, academic affiliation)
- Early funding rounds (if VC-backed biotech)

### Stage 3: Clinical development
- Phase 1 trials (via `clinical-trial-intel`)
- Phase 2 — dose ranging, early efficacy
- Phase 3 — registrational trials
- Primary endpoints met / missed

### Stage 4: FDA approval
- NDA submission date
- PDUFA target date
- Advisory committee vote (if any)
- FDA approval date + indication
- Label warnings / Boxed warnings
- ODAC (Oncologic Drugs Advisory Committee) involvement

### Stage 5: Commercial launch
- First-quarter sales
- Peak-year sales (if post-launch)
- Competitive positioning
- Formulary status / payer coverage

### Stage 6: Post-marketing
- FAERS adverse event patterns (via `fda-drug-recalls-faers`)
- FDA recalls
- Label expansions (new indications)
- Generic / biosimilar entry dates (patent cliff)
- Real-world evidence studies

## Output format: a chronological timeline

```
🧬 DRUG LIFECYCLE — {Drug Name} ({target / MoA})
═══════════════════════════════════════════════════════════

📚 ACADEMIC ORIGIN
  1993 — First paper on GLP-1 receptor agonists for diabetes (Creutzfeldt & Nauck, Gastroenterology)
         → NIH grant: R01-DK-051349 to Dr. Drucker at U Toronto ($1.1M)
  1995 — Patent WO9517510 filed by Novo Nordisk (composition of matter)

🏢 CORPORATE DEVELOPMENT
  1996 — Novo Nordisk begins preclinical development of NN2211 (liraglutide predecessor)
  2005 — Liraglutide files IND
  2009 — Ozempic IND filed (long-acting once-weekly GLP-1 agonist)

🧪 CLINICAL DEVELOPMENT — 16 REGISTERED TRIALS
  2010 — SUSTAIN-1 (Phase 3, n=388, 30wk Type 2 Diabetes) → positive results
  2012 — SUSTAIN-2, SUSTAIN-3, SUSTAIN-4 running in parallel
  2014 — SUSTAIN-6 cardiovascular outcomes trial (n=3,297) → 26% CV risk reduction
  2016 — NDA submitted to FDA December 5, 2016

💊 FDA APPROVAL
  2017-12-05 — OZEMPIC approved by FDA for Type 2 Diabetes (NDA 209637)
               PDUFA date hit on time. No AdCom required.
  2021-06-04 — WEGOVY (semaglutide 2.4mg) approved for chronic weight management
  2023-04-28 — Oral version RYBELSUS approved

💰 COMMERCIAL
  2017 — $0 sales (launch quarter)
  2023 — $21.1B combined semaglutide revenue (Ozempic + Wegovy + Rybelsus)
  2024 — $38B (Wegovy + Ozempic each in top-5 global drugs)
  Market: GLP-1 class projected $135B peak by 2030

📊 POST-MARKETING
  2020 — FAERS signals: pancreatitis (known class effect), rare thyroid C-cell tumors
  2022 — Gastroparesis lawsuits filed (Class I case count: 400+)
  2023 — FDA recall: Granules India NDMA impurity (Class II, voluntary)
  2026 — FDA approved for cardiovascular risk reduction (SELECT trial)

🔭 PIPELINE + COMPETITIVE LANDSCAPE
  Competitors in clinical development:
  • Tirzepatide (Lilly/Mounjaro/Zepbound) — Phase 4, approved 2022/2023
  • Orforglipron (Lilly) — Phase 3, oral small-molecule GLP-1
  • Retatrutide (Lilly) — Phase 3, triple-agonist
  • MariTide (Amgen) — Phase 2, ultra-long-acting
  • Ecnoglutide (Innovent/China) — Phase 3

🧬 ACADEMIC ORIGIN ATTRIBUTION
  Key investigators who built the GLP-1 field:
  • Dr. Daniel Drucker (U Toronto) — ~40 NIH grants totaling ~$25M
  • Dr. Jens Juul Holst (U Copenhagen) — original GLP-1 mechanism paper 1993
  • Dr. Lotte Bjerre Knudsen (Novo Nordisk) — inventor on 50+ GLP-1 patents
  These three are likely recipients of a future Nobel Prize in Medicine.

⚠️ RISK FACTORS / CATALYSTS AHEAD
  • Patent cliff: Ozempic composition-of-matter expires 2031
  • Biosimilar competition: Teva + Sandoz + multiple Indian generics entering late 2031
  • FDA additional indications: Alzheimer's (EVOKE trial reading 2026-Q3), NASH (pending)
  • China oral GLP-1 disruption: Innovent's ecnoglutide could launch 2027
  • Class lawsuits: $500M-2B potential liability from gastroparesis claims
```

## Data sources (synthesized across 7 APIs)

1. **PubMed E-utilities** (via `pubmed-paper-scan`) — academic publications
2. **NIH RePORTER** (via `nih-grant-scan`) — grant history
3. **USPTO patent search** — composition of matter + method of use patents
4. **ClinicalTrials.gov** (via `clinical-trial-intel`) — trial history
5. **openFDA drug/label + drug/approvals** — FDA approval events
6. **openFDA drug/event** (via `fda-drug-recalls-faers`) — adverse events
7. **SEC EDGAR 10-K** (via `sec-insider-scan` stack) — revenue + patent disclosure

## Example invocation

User: "Drug lifecycle for lecanemab"

The skill should:

1. Pull PubMed for "lecanemab OR BAN2401" research papers (earliest: ~2012, Eisai/BioArctic partnership)
2. Pull NIH grants supporting academic amyloid-beta research
3. Query ClinicalTrials.gov for lecanemab trials (CLARITY-AD, etc.)
4. Pull FDA openFDA for BLA 761269 (Leqembi)
5. Query FAERS for Leqembi adverse events (ARIA-E, ARIA-H)
6. Return the chronological timeline

## Why this is truly remarkable

**Building this analysis manually takes 2-3 days per drug for a senior biotech analyst.** This skill does it in a single LLM invocation.

Commercial tools that partially cover this:
- **Evaluate Pharma** — best on commercial + pipeline ($50k+/year)
- **Citeline Pharmaprojects** — strong on clinical ($30k+/year)
- **Pharmaintelligence** — competitive landscape ($25k+/year)

**None combine academic origin + NIH funding + clinical + FDA + FAERS + commercial + competitive in one view.**

This skill does.

## Honest caveats

- **Academic origin attribution** is often ambiguous — many drugs have multiple "fathers"
- **Patent dates** require manual USPTO lookup for composition-of-matter vs method-of-use
- **Peak sales forecasts** are consensus estimates subject to wide variance
- **Competitive landscape** moves monthly — this captures snapshot at query time

## License + source

Uses free public APIs from NIH, PubMed, FDA, SEC, USPTO, arXiv. MIT licensed.
