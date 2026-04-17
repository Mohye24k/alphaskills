---
name: biorxiv-preprint-scan
description: Searches bioRxiv (biology) and medRxiv (medical) — the two leading biomedical preprint servers operated by Cold Spring Harbor Laboratory — for the newest, not-yet-peer-reviewed research. Returns DOI, title, authors, category, abstract, and links to full PDFs. Use when the user asks about cutting-edge biology research, wants preprints before they're peer-reviewed in journals like Nature/Cell, needs the earliest signal on a discovery (which can precede NEJM/JAMA publication by 6-12 months), or researches a specific bio-subcategory (genomics, neuroscience, systems biology). Complements the pubmed-paper-scan skill (PubMed = peer-reviewed; bioRxiv/medRxiv = preprints). Uses the free official bioRxiv API (api.biorxiv.org) with no key required. No commercial incumbent — this is a pure-open-science play.
---

# bioRxiv + medRxiv Preprint Scanner

## When to invoke

Trigger on any cutting-edge biology/medical research question:

- "Latest CRISPR preprints"
- "bioRxiv neuroscience papers this month"
- "Early AGI / protein folding research"
- "COVID preprints on new variants"
- "Medical research before peer review"
- "What's trending in single-cell RNA-seq?"

## Why preprints matter (briefly)

Preprints are research papers shared publicly BEFORE peer review. On bioRxiv / medRxiv:

- **6-12 months earlier** than journal publication
- **Authors still iterate** (multiple versions often posted)
- **NOT peer-reviewed** — quality varies; require critical reading
- **Open access** — full PDFs are free
- Used heavily by biotech investors, academic researchers, and journalists for early signals

## Required input (at least one)

- **Search terms** — free text across title + abstract
- **Category** — bioRxiv/medRxiv subject category (see list below)
- **Author** — full name or partial
- **Date range** — posting dates
- **Server** — `biorxiv` (biology) or `medrxiv` (medical) — default both

## bioRxiv + medRxiv categories

**bioRxiv** covers biology:
- `biochemistry`, `bioengineering`, `bioinformatics`, `biophysics`
- `cancer biology`, `cell biology`, `developmental biology`
- `ecology`, `epidemiology`, `evolutionary biology`
- `genetics`, `genomics`, `immunology`, `microbiology`
- `molecular biology`, `neuroscience`, `pathology`
- `pharmacology and toxicology`, `physiology`, `plant biology`
- `scientific communication and education`, `synthetic biology`
- `systems biology`, `zoology`

**medRxiv** covers medical / clinical:
- `addiction medicine`, `allergy and immunology`, `anesthesia`
- `cardiovascular medicine`, `dentistry and oral medicine`
- `dermatology`, `emergency medicine`, `endocrinology`
- `epidemiology`, `forensic medicine`, `gastroenterology`
- `genetic and genomic medicine`, `geriatric medicine`
- `hematology`, `health economics`, `health informatics`
- `health policy`, `health systems and quality improvement`
- `hematology`, `HIV/AIDS`, `infectious diseases`
- `intensive care and critical care medicine`, `medical education`
- `medical ethics`, `nephrology`, `neurology`, `nursing`
- `nutrition`, `obstetrics and gynecology`, `occupational and environmental health`
- `oncology`, `ophthalmology`, `orthopedics`, `otolaryngology`
- `pain medicine`, `palliative medicine`, `pathology`, `pediatrics`
- `pharmacology and therapeutics`, `primary care research`, `psychiatry`
- `public and global health`, `radiology and imaging`, `rehabilitation medicine`
- `respiratory medicine`, `rheumatology`, `sexual and reproductive health`
- `sports medicine`, `surgery`, `toxicology`, `transplantation`
- `urology`

## Output format

### 1. Summary
`"Found {N} bioRxiv/medRxiv preprints matching {query}. Categories: {list}."`

### 2. Preprints table

| DOI | Date | Server | Category | Title | First Author |
|-----|------|--------|----------|-------|-------------|

Sort by posting date descending. Cap at 15.

### 3. Top preprint summaries (first 3-5)
For the most relevant, 2-3 sentence summaries.

### 4. Peer-review tracking
If a preprint was later formally published, flag with 🏛️ + journal name. Use the `search_published_preprints` functionality or cross-reference DOIs.

## Data source + procedure

Uses the bioRxiv API (also covers medRxiv via the same endpoint):

```
GET https://api.biorxiv.org/details/{server}/{interval}
```

Where:
- `server` = `biorxiv` or `medrxiv`
- `interval` = DOI, date range (`2026-01-01/2026-04-16`), or count (`0/100`)

Example (recent 100 bioRxiv preprints):
```
GET https://api.biorxiv.org/details/biorxiv/0/100
```

Example (search by date range):
```
GET https://api.biorxiv.org/details/biorxiv/2026-04-01/2026-04-16/0
```

Response has `collection[]` with:

- `doi`
- `title`
- `authors` — pipe-separated list
- `author_corresponding`
- `author_corresponding_institution`
- `date` — posting date
- `version`
- `type` — `new` or `revised`
- `license`
- `category`
- `jatsxml` — URL to JATS XML
- `abstract`

## Example invocation

User: "Latest single-cell RNA-seq preprints"

The skill should:
1. Search with `search_preprints` for terms like "single-cell RNA-seq OR scRNA-seq"
2. Filter to `category=genomics` or `category=bioinformatics`
3. Return:
   ```
   Found 47 bioRxiv preprints on single-cell RNA-seq in the last 30 days.
   Categories: genomics (28), bioinformatics (12), cell biology (7).

   Top preprints:
   | 10.1101/2026.04.14.287654 | 2026-04-14 | bioRxiv | genomics | scVELO-v2: lineage tracing in heterogeneous cancer cell populations | Chen et al. |
   | 10.1101/2026.04.10.287123 | 2026-04-10 | bioRxiv | bioinformatics | Multimodal atlases: integrating scRNA-seq with spatial transcriptomics | Srivatsan et al. |

   Emerging themes:
   1. Spatial + single-cell integration (5+ papers this month) — transitioning from pure single-cell to spatially-resolved atlases
   2. Long-read single-cell (4+ papers) — detecting alternative splicing at single-cell level
   3. Bayesian batch correction methods (3+ papers) — improving cross-study harmonization
   ```

## Peer-review status

A significant fraction of bioRxiv/medRxiv preprints eventually get peer-reviewed and published. Check the `search_published_preprints` endpoint to see which preprints found a journal home.

## License + source

bioRxiv/medRxiv is operated by Cold Spring Harbor Laboratory. API is free and open. Individual preprints are posted under licenses chosen by authors (typically CC-BY or CC-BY-NC variants).
