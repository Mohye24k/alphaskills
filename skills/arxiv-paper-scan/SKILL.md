---
name: arxiv-paper-scan
description: Searches and summarizes recent academic papers from arXiv across AI/ML (cs.AI, cs.LG, cs.CL, cs.CV), biology (q-bio), physics, math, economics, and more. Returns paper titles, authors, abstracts, PDF links, DOIs, primary category, and publication dates. Use when the user asks about recent research in a field, wants to find papers by a specific author (Hinton, LeCun, Bengio, Doudna), needs the latest on a topic (transformers, diffusion models, CRISPR, quantum computing), wants to track a conference's recent output, or asks for a literature review on a research topic. Uses the official free arXiv Atom query API (export.arxiv.org) with no key required. Respects arXiv's self-imposed 3-second rate limit. Replaces Semantic Scholar premium ($99+/month for commercial use), Connected Papers Pro ($5-15/month), and Scite.ai ($99-499/month).
---

# arXiv Paper Search + Research Scanner

## When to invoke

Trigger on any academic research question:

- "Latest papers on LLM reasoning"
- "Hinton's recent papers"
- "Diffusion model papers from 2024"
- "What's new in cs.AI this week?"
- "Academic literature on CRISPR in cancer"
- "Transformer attention papers"
- "New neuroscience papers on memory"

## Required input (at least one)

- **Category** — arXiv category code (see table below)
- **Search query** — free text across title, abstract, authors using arXiv syntax (`AND`, `OR`, `ANDNOT`, field prefixes like `ti:`, `au:`, `abs:`, `cat:`, `all:`)
- **Authors** — list of author names to search

## Common arXiv categories

| Code | Field |
|------|-------|
| `cs.AI` | Artificial Intelligence |
| `cs.LG` | Machine Learning |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.RO` | Robotics |
| `cs.NE` | Neural & Evolutionary Computing |
| `cs.IR` | Information Retrieval |
| `cs.CR` | Cryptography & Security |
| `cs.DC` | Distributed Computing |
| `cs.SE` | Software Engineering |
| `cs.HC` | Human-Computer Interaction |
| `stat.ML` | Statistics — Machine Learning |
| `math.OC` | Math — Optimization & Control |
| `q-bio.NC` | Neurons & Cognition |
| `q-bio.MN` | Molecular Networks |
| `q-bio.GN` | Genomics |
| `q-fin.TR` | Quant Finance — Trading/Microstructure |
| `econ.EM` | Econometrics |
| `physics.bio-ph` | Biological Physics |
| `hep-ph` | High Energy Physics — Phenomenology |

Full taxonomy: https://arxiv.org/category_taxonomy

## Output format

### 1. Summary
`"Found {N} arXiv papers matching {query}. Recent activity: {papers_last_30d} papers in the last month."`

### 2. Papers table

| arXiv ID | Date | Title | Primary Authors | Category |
|----------|------|-------|-----------------|----------|

Sort by `submittedDate` descending (most recent first). Cap at 15 rows unless user asks for more.

### 3. Brief summaries (top 3-5 papers)
For the top most relevant papers, provide a 2-3 sentence summary of the abstract (not just paste it).

### 4. Trending themes (when applicable)
If multiple papers converge on a theme, summarize it. E.g. "Three recent papers in cs.AI focus on test-time compute scaling for reasoning models, suggesting this is an emerging research direction."

## Data source + procedure

Query the arXiv Atom API:

```
GET http://export.arxiv.org/api/query?search_query={query}&start={offset}&max_results=100&sortBy=submittedDate&sortOrder=descending
```

The query uses arXiv's boolean syntax:

- `cat:cs.AI` — papers in cs.AI
- `(cat:cs.AI OR cat:cs.LG)` — in either category
- `ti:transformer` — "transformer" in title
- `au:"Geoffrey Hinton"` — by author
- `abs:attention` — in abstract
- `all:reasoning` — anywhere

Combine with `+AND+`, `+OR+`, `+ANDNOT+` (URL-encoded).

### Atom XML parsing

The response is Atom XML. Each `<entry>` contains:

- `<id>` — URL like `http://arxiv.org/abs/2604.13029v1`. Extract `2604.13029v1` as the arXiv ID.
- `<title>` — paper title
- `<summary>` — abstract
- `<published>`, `<updated>` — ISO timestamps
- `<author><name>...</name></author>` — repeated for each author
- `<category term="cs.AI"/>` — repeated for each category
- `<arxiv:primary_category term="cs.AI"/>` — primary category
- `<arxiv:doi>` — DOI if published journal version exists
- `<arxiv:comment>` — author notes (page count, conference accepted, etc.)
- `<arxiv:journal_ref>` — journal reference
- `<link>` tags — `rel="alternate" type="text/html"` is the abstract page; `type="application/pdf"` is the PDF

### Rate limit

arXiv asks for **one request every 3 seconds** from a single client. Respect this. If multiple requests are needed, space them out.

## Author disambiguation tip

Searching `au:"Hinton"` matches ANY author with "Hinton" in their name, not just Geoffrey Hinton. For disambiguation:

- Use full name: `au:"Geoffrey Hinton"`
- Combine with co-authors: `au:"Hinton" AND au:"LeCun"`
- Filter by category: `au:"Hinton" AND cat:cs.LG`

## Example invocation

User: "What's new in LLM reasoning research?"

The skill should:
1. Query with `search_query=(cat:cs.AI OR cat:cs.LG OR cat:cs.CL) AND (abs:reasoning OR abs:"chain of thought" OR abs:"test-time compute")` sorted by recency
2. Return:
   ```
   Found 487 recent papers on LLM reasoning.
   Recent activity: 34 papers in the last 30 days.

   Top papers (latest):
   | 2604.13029v1 | 2026-04-14 | Visual Preference Optimization with Rubric Rewards | Yu et al. | cs.CV/cs.AI |
   | 2604.12847v1 | 2026-04-13 | Test-Time Scaling for Mathematical Reasoning | Chen et al. | cs.LG |
   ...

   Emerging themes:
   1. Test-time compute scaling (5+ papers) — Inference-time search is becoming the new axis for reasoning improvement
   2. Rubric-based reward models (3+ papers) — Instance-specific rubrics outperforming holistic preference data for multimodal reasoning
   3. Multi-turn reasoning (4+ papers) — Long-horizon reasoning with interleaved retrieval
   ```

## Relationship to AlphaStack portfolio

Corresponds to the `arxiv-paper-tracker` Apify actor (`H3amNRNQQCv0f2JiE`).
