---
name: pubmed-paper-scan
description: Searches PubMed — the NIH/NLM repository of 35+ million biomedical research citations — for peer-reviewed medical research by disease, drug, author, journal, or date. Returns PMID, title, abstract, authors, journal, publication date, MeSH terms, and DOIs. Use when the user asks about medical research, clinical studies, systematic reviews, a specific disease's treatment literature, a physician/researcher's publication history, or needs a medical literature review. Complements the arxiv-paper-scan skill (arXiv covers preprints; PubMed covers peer-reviewed biomedical journals). Uses the official free NCBI E-utilities API (eutils.ncbi.nlm.nih.gov/entrez/eutils) with no key required but higher rate limits if API key provided. Replaces Ovid MEDLINE ($10k+/institutional), Embase ($20k+/year), and Scopus ($8k+/year).
---

# PubMed Biomedical Literature Scanner

## When to invoke

Trigger on any medical / biomedical literature question:

- "Recent research on GLP-1 and Alzheimer's"
- "Systematic reviews of statins and cognition"
- "Dr. Anthony Fauci's recent publications"
- "Clinical trials for CRISPR in sickle cell"
- "NEJM Ozempic papers 2026"
- "Meta-analyses of ivermectin"

## Required input (at least one)

- **Search terms** — free text using PubMed syntax
- **MeSH term** — structured Medical Subject Heading (preferred for precision)
- **Author name** — `"Fauci A"` or `"Fauci, Anthony S"`
- **Journal** — e.g. `"NEJM"`, `"Lancet"`, `"JAMA"`, `"Nature Medicine"`
- **Date range** — publication dates

## PubMed search syntax

PubMed uses bracketed field tags:

- `cancer[Title]` — in title only
- `cancer[Title/Abstract]` — in title or abstract
- `Doudna J[Author]` — author
- `"NEJM"[Journal]` — journal
- `"2026"[Date - Publication]` — year
- `"randomized controlled trial"[Publication Type]` — publication type filter
- `"Drug Therapy"[MeSH Terms]` — MeSH subject heading
- Boolean: `cancer AND CRISPR`, `diabetes OR obesity`, `stroke NOT aspirin`

## Common filters worth using

| Filter | PubMed tag | Use |
|--------|-----------|-----|
| Randomized controlled trials | `"Randomized Controlled Trial"[PT]` | Highest evidence |
| Meta-analyses | `"Meta-Analysis"[PT]` | Summarized evidence |
| Systematic reviews | `"Systematic Review"[PT]` | Critical synthesis |
| Clinical trials | `"Clinical Trial"[PT]` | Prospective studies |
| Last 30 days | `"last 30 days"[Date - Publication]` | Recent only |
| Free full text | `"free full text"[Filter]` | Accessible papers |
| Humans only | `humans[MeSH Terms]` | Exclude animal studies |

## Output format

### 1. Summary
`"Found {N} PubMed citations matching {query}. Date range: {earliest} to {latest}. Top journals: {list}."`

### 2. Papers table

| PMID | Date | Journal | Title | First Author |
|------|------|---------|-------|-------------|

Sort by publication date descending. Cap at 15 rows.

### 3. Top papers summaries (first 3-5)
For the most relevant papers, provide 2-3 sentence summaries of the abstract (not raw paste).

### 4. Citation clusters (when applicable)
If multiple papers share MeSH terms or authors, summarize the theme: "Three recent Nature Medicine papers converge on the role of X in Y, suggesting an emerging consensus..."

## Data source + procedure

Uses the NCBI E-utilities API. Two-step process:

### Step 1: Search (returns PMIDs)

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax=50&sort=date
```

Response: `esearchresult.idlist[]` — array of PMIDs

### Step 2: Fetch records

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={comma-separated-PMIDs}&retmode=xml
```

Returns a single XML document with `<PubmedArticle>` blocks. Each contains:

- `<PMID>` — the identifier
- `<ArticleTitle>` — paper title
- `<Abstract>` — full abstract (sometimes structured by heading)
- `<AuthorList>` — authors (LastName, ForeName, Initials)
- `<Journal><Title>` or `<ISOAbbreviation>` — journal
- `<PubDate><Year>`, `<Month>`, `<Day>` — publication date
- `<PublicationTypeList>` — paper type (RCT, meta-analysis, review, etc.)
- `<MeshHeadingList>` — MeSH subject headings with qualifiers
- `<ArticleIdList><ArticleId IdType="doi">` — DOI

### Rate limit

- **No API key**: 3 requests per second
- **With key**: 10 req/sec
- Free key from https://www.ncbi.nlm.nih.gov/account/

## Example invocation

User: "Recent GLP-1 research on Alzheimer's"

The skill should:
1. Search with query: `(GLP-1 OR semaglutide OR liraglutide OR tirzepatide) AND ("Alzheimer Disease"[MeSH] OR dementia) AND ("2025"[Date - Publication] OR "2026"[Date - Publication])`
2. Fetch top 20 papers
3. Return:
   ```
   Found 87 PubMed citations on GLP-1 + Alzheimer's (2025-2026).
   Top journals: Nature Medicine (4), Lancet Neurology (3), NEJM (2), Neurology (5).

   Top papers:
   | 40281234 | 2026-03 | N Engl J Med | Semaglutide for Cognitive Decline in Type 2 Diabetes (EVOKE-2 Trial) | Strayer et al. |
     → RCT, n=1,840. Semaglutide 2.4mg weekly showed 18% slower cognitive decline vs placebo over 24mo (primary endpoint met, p<0.001). First positive Phase 3 disease-modifying result for a GLP-1 in AD.

   | 40275891 | 2026-02 | Nat Med | Mechanistic studies of GLP-1R in microglial inflammation | Lee et al.
     → Preclinical. Demonstrates GLP-1 agonism suppresses microglial activation via PKA-CREB pathway, providing the mechanistic basis for cognitive effects seen clinically.

   Emerging theme: 2026 marks the first positive Phase 3 for a GLP-1 in Alzheimer's. Expect rapid follow-on: Lilly's tirzepatide in TRAILBLAZER-ALZ 4 completing 2027.
   ```

## Related: arxiv-paper-scan

- **arXiv** covers preprints in CS, math, physics, bio (incl. unpeer-reviewed biology/medicine in q-bio)
- **PubMed** covers peer-reviewed biomedical journals
- Use both together for complete biomedical coverage

## License + source

PubMed citations are public domain (NIH/NLM). Full text availability varies by journal. Always check the license of the original paper.
