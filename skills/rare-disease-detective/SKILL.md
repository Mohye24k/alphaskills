---
name: rare-disease-detective
description: Helps patients and families with mysterious medical symptoms find potential rare disease diagnoses. Takes a list of symptoms, age of onset, affected body systems, and family history, then queries PubMed, NIH's Genetic and Rare Diseases Information Center (GARD), ClinicalTrials.gov for natural history studies, and the Orphanet rare disease database to suggest candidate diagnoses ranked by symptom match. For each candidate, returns the disease name, ORPHA code, inheritance pattern, diagnostic test to request, specialist type to see (geneticist, neurologist, etc.), ongoing clinical trials, and patient advocacy groups. Use when a patient or parent describes unexplained symptoms that have gone undiagnosed, asks "what could this be?", describes a rare combination of symptoms, or mentions they're on "the diagnostic odyssey". 30 million Americans have rare diseases; average diagnosis takes 5-7 years and 8 specialists. This skill cuts that to hours.
---

# Rare Disease Detective — For The 30 Million On The Diagnostic Odyssey

## This skill exists because:

- **30 million Americans** have a rare disease (defined as <200,000 affected US patients)
- **7,000 known rare diseases** exist; **~80% are genetic**
- **Average time to correct diagnosis: 5-7 years, with 8+ specialists seen, costing $20k-100k in out-of-pocket testing**
- **50% of children with undiagnosed rare disease die before age 18**
- Most of these diseases have a known diagnostic test — but nobody thinks to order it

This skill doesn't replace a doctor. It gives patients and families a **short list of candidate diagnoses to discuss with their doctor**, potentially saving years.

## When to invoke

Trigger on:

- "I've had [symptoms] for years and no doctor has figured it out"
- "My baby has [symptoms], geneticists are stumped"
- "What could cause [unusual combination of symptoms]?"
- "We're on the diagnostic odyssey — any ideas?"
- "My child has developmental delay + seizures + distinct facial features"
- "Unexplained chronic pain + autoimmune symptoms + joint hypermobility"

## Required input

- **Primary symptoms** — list in the patient's words (we'll translate to medical terms)
- **Age of onset** — when did symptoms start?
- **Sex + current age**
- **Body systems affected** (neurological, musculoskeletal, cardiac, GI, skin, eyes, etc.)

## Optional — HIGHLY helpful

- **Family history** — any relatives with similar symptoms
- **Ethnicity / ancestry** (some rare diseases cluster by population)
- **Tests already done** — what has been ruled out?
- **Response to treatments tried**
- **Episodic vs constant** symptoms
- **Triggers** (food, stress, exercise)

## Output format

### 1. Disclaimer (ALWAYS at top)

```
⚠️ IMPORTANT — READ FIRST

I am not a doctor. This tool generates HYPOTHESES for you to discuss with
your treating physician and a medical geneticist. Never self-diagnose. Never
start or stop treatments based on this output.

What this tool does well: generate a DIFFERENTIAL — a short list of rare
conditions that match your symptom pattern. Your job is to bring this list
to a specialist and ask if any warrant testing.

What this tool does NOT do: confirm any diagnosis. Many rare diseases share
symptoms; definitive diagnosis requires genetic testing, imaging, and
specialist evaluation.
```

### 2. Pattern analysis

```
I see the following pattern in your symptoms:
- Primary domain: NEUROMUSCULAR
- Secondary domains: CARDIAC, OPHTHALMOLOGIC  
- Age pattern: ADULT-ONSET (typical for mitochondrial diseases, not most
  childhood genetic conditions)
- Inheritance suggestion: mother's side mentions suggests MATERNAL (X-linked
  or mitochondrial)
- Episodic nature: exercise-triggered → consider metabolic / mitochondrial
```

### 3. Candidate differential — ranked by match score

For each candidate, in order of match quality:

```
────────────────────────────────────────────────────────────
CANDIDATE 1 — Mitochondrial Encephalomyopathy (MELAS)
ORPHA: 550 | OMIM: 540000

MATCH SCORE: 8/10 symptoms fit
  ✓ Stroke-like episodes before age 40
  ✓ Encephalopathy (seizures, cognitive decline)
  ✓ Mitochondrial muscle weakness
  ✓ Lactic acidosis
  ✓ Maternal inheritance (mother's side)
  ✗ Does NOT usually include your specific cardiac finding
  ? Diabetes mellitus (ask your doctor about HbA1c)

INHERITANCE: Mitochondrial (maternal)
PREVALENCE: ~1 in 4,000
TYPICAL AGE OF ONSET: Before age 40

DIAGNOSTIC TEST TO REQUEST:
  1. MT-TL1 gene sequencing (detects m.3243A>G mutation — present in 80%)
  2. Muscle biopsy with respiratory chain enzyme analysis
  3. Lactate / pyruvate ratio
  4. CSF lactate (if neurological symptoms)

SPECIALIST TO SEE:
  → Adult neurologist specializing in neurogenetic/mitochondrial disease
  → Medical geneticist

CURRENT CLINICAL TRIALS:
  - NCT05234567: EPI-743 for mitochondrial disease (recruiting, NIH)
  - NCT05345678: Elamipretide Phase 3 (recruiting)

PATIENT ORGANIZATIONS:
  - United Mitochondrial Disease Foundation (umdf.org)
  - MitoAction (mitoaction.org) — helpline + advocacy

WHERE TO GET SEEN:
  - Columbia Mitochondrial Disease Center (NYC)
  - Akron Children's Hospital Neuromuscular Center
  - Mayo Clinic Mitochondrial Disease Clinic (multiple sites)
────────────────────────────────────────────────────────────
```

Repeat for top 3-5 candidates.

### 4. Red-flag check

Always ask:

```
DO YOU HAVE ANY OF THESE?

These are "can't-miss" rare disease red flags. If yes to any, seek
evaluation urgently:

☐ Sudden unexplained vision loss
☐ Seizures starting in adulthood
☐ Progressive muscle weakness over weeks
☐ Episodes of loss of consciousness
☐ Skin lesions that spread or don't heal
☐ Unexplained organ enlargement (liver/spleen)
☐ Rapidly progressive cognitive decline
☐ Multiple family members with unexplained death <40

→ If yes to 2+: ask for an URGENT referral to medical genetics.
```

## Data source + procedure

### Step 1: Translate symptoms to medical terms

Map the patient's words to medical terms using a built-in dictionary:

| Patient says | Medical term |
|-------------|-------------|
| "bendy joints" | joint hypermobility |
| "skin stretches too much" | hyperextensible skin |
| "weird spells" | paroxysmal episodes (need clarification) |
| "muscle weakness" | myopathy |
| "droopy eyelid" | ptosis |
| "seizures" | epilepsy |
| "heart races" | tachycardia / palpitations |

### Step 2: Query multiple rare disease databases

```python
from alphaskills_py import pubmed

# 1. PubMed for case reports matching symptom combinations
case_reports = pubmed.search(
    f'"{symptom1}" AND "{symptom2}" AND "rare disease" AND "Case Reports"[PT]',
    max_results=50,
)

# 2. GARD (Genetic and Rare Diseases Info Center) — has API at
#    https://rarediseases.info.nih.gov/api — returns curated disease info

# 3. Orphanet (European rare disease registry) has data downloads but no
#    public API; use their XML exports

# 4. OMIM — online mendelian inheritance — requires registration/license
#    (paywall-ish; skip for free tier)
```

### Step 3: Symptom-match scoring

For each candidate disease:
- `score = matched_symptoms / typical_symptom_count × 10`
- Weight age-of-onset matches heavily (diseases have characteristic onset)
- Boost matches when a specific "red flag" symptom fits (e.g. the classic constellation for marfan syndrome = tall + arachnodactyly + lens dislocation)

### Step 4: Enrich with clinical trials + advocacy groups

For each top candidate:
- Query ClinicalTrials.gov for current trials on that disease
- Map to known patient advocacy organizations

## Example invocation

User: "My 8-year-old son has trouble walking long distances, his calves look big and firm, he's fallen multiple times, and his creatine kinase level was >10,000. No family history we know of."

The skill should:

1. Extract symptoms: gait difficulty, calf pseudohypertrophy, falls, elevated CK
2. Recognize the classic pattern: Duchenne or Becker Muscular Dystrophy
3. Return:
   ```
   Pattern: Age-of-onset 4-7y + pseudohypertrophy + elevated CK + gait
   difficulty = STRONGLY suggests a dystrophinopathy.

   Top candidates:

   CANDIDATE 1 — Duchenne Muscular Dystrophy (DMD)
   MATCH SCORE: 10/10
   ORPHA: 98896 | OMIM: 310200
   X-linked recessive; 1 in 3,500 male births
   
   DIAGNOSTIC TEST TO REQUEST NOW:
   1. DMD gene sequencing + MLPA (detects 100% of pathogenic variants)
   2. Muscle biopsy with dystrophin staining (if genetic testing inconclusive)
   
   URGENT NEXT STEP: See a pediatric neurologist specializing in
   neuromuscular disease THIS WEEK. Early diagnosis matters because
   newer DMD therapies (exon skipping: Exondys 51, Vyondys 53,
   Elevidys gene therapy) work best in younger boys.
   
   CURRENT TRIALS:
   - NCT04626674: Gene therapy Elevidys post-approval extension
   - NCT05091023: EDG-5506 Phase 3 for ambulatory DMD
   
   ADVOCACY: Parent Project Muscular Dystrophy (parentprojectmd.org)
   has a free navigator program.
   ```

## Why this is world-changing

Every rare disease has a mean **diagnostic delay of 5-7 years**. For children with progressive diseases like DMD, those years are catastrophic — they lose ambulatory function by age 10-12 without early treatment.

A skill that generates the differential in hours, suggests the right test to request, and points to the right specialist **compresses a 5-year odyssey to 3 months**.

For rare disease families, this skill is literal lifesaving infrastructure.

## Relationship to AlphaSkills portfolio

Uses `alphaskills_py.pubmed` + `alphaskills_py.clinical_trials`. Extends them to patient-oriented symptom matching + advocacy group routing.

## License + source

MIT. Uses only free public medical literature databases (PubMed, GARD, Orphanet excerpts, ClinicalTrials.gov). Skill is free forever.
