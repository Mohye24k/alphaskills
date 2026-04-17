# AlphaSkills

**18 Claude Code skills for institutional-grade financial, biotech, legal, and research intelligence.**

One `/skill` invocation inside Claude Code, Claude Projects, Claude Desktop, or OpenAI Codex CLI → full SEC insider trading, hedge fund holdings, activist campaigns, clinical trials, stock signals, futures positioning, arXiv + PubMed + bioRxiv papers, NIH grants, FDA drug recalls, Federal Register rules, federal court dockets, GitHub repo intelligence, SEC S-1 IPO tracking, vehicle recalls, and more.

Every skill uses **free public US government APIs** (SEC EDGAR, NIH RePORTER, ClinicalTrials.gov, CFTC, NHTSA, FDA openFDA, Federal Register, FRED, CourtListener, arXiv, bioRxiv). Most require no API key at all.

## The 18 skills

### 📈 Finance (6 skills)

| Skill | Replaces | What it does |
|-------|----------|-------------|
| **sec-insider-scan** | InsiderScore $99-499/mo | Form 4 insider trading per ticker |
| **hedge-fund-holdings** | WhaleWisdom $99-499/mo | 13F holdings per fund (Berkshire, Bridgewater, Citadel, …) |
| **activist-campaign-tracker** | ActivistInsight $20-100k/yr | 13D/G filings by Icahn, Ackman, Loeb, Elliott |
| **stock-signal-report** ⭐ | Bloomberg $25k/yr | Unified bull/bear signal per ticker |
| **company-deepdive** ⭐⭐ | Bloomberg + Capital IQ + FactSet | Master skill — full multi-source dossier |
| **sec-s1-ipo-tracker** | Renaissance Cap IPO Research $99+/mo | S-1 IPO filings + amendment velocity |

### 💊 Biotech / Pharma (3 skills)

| Skill | Replaces | What it does |
|-------|----------|-------------|
| **clinical-trial-intel** | Citeline Trialtrove $25-100k/yr | Pipeline by condition / drug / sponsor |
| **nih-grant-scan** | GrantForward $300+/yr | NIH RePORTER grant awards |
| **fda-drug-recalls-faers** | IQVIA adverse events $50k+ | FDA recalls + FAERS adverse events |

### 🔬 Research (3 skills)

| Skill | Replaces | What it does |
|-------|----------|-------------|
| **arxiv-paper-scan** | Scite.ai $99+/mo | arXiv preprints (CS, math, physics, bio) |
| **pubmed-paper-scan** | Ovid MEDLINE $10k+/yr | PubMed peer-reviewed biomedical literature |
| **biorxiv-preprint-scan** | — (no incumbent) | bioRxiv + medRxiv biology/medical preprints |

### 📊 Macro (2 skills)

| Skill | Replaces | What it does |
|-------|----------|-------------|
| **futures-positioning-check** | Bloomberg COT $25k/yr | CFTC weekly futures positioning |
| **fred-economic-data** | Nasdaq Data Link $249+/mo | FRED macroeconomic time series |

### ⚖️ Legal / Regulatory (2 skills)

| Skill | Replaces | What it does |
|-------|----------|-------------|
| **federal-register-tracker** | Bloomberg Gov $5-25k/yr | US Federal Register rule + notice tracker |
| **courtlistener-docket-tracker** | Westlaw $500+/mo | Federal court dockets via CourtListener |

### 🔧 Other (2 skills)

| Skill | Replaces | What it does |
|-------|----------|-------------|
| **vehicle-recall-check** | Carfax $40/VIN | NHTSA recalls by make/model/year |
| **github-repo-intel** | OSS Insight $99+/mo | GitHub repo health + contributor + security |

---

## Install (3 options)

### Option 1 — Install all 18 skills (recommended)

```bash
# Clone the repo
git clone https://github.com/Mohye24k/alphaskills.git ~/alphaskills

# Install into ~/.claude/skills/
cd ~/alphaskills
./install.sh              # macOS / Linux
.\install.ps1             # Windows PowerShell

# For OpenAI Codex CLI instead
./install.sh --codex
```

The installer symlinks each skill from `~/alphaskills/skills/<name>/` into the target skills directory, preserving git-controlled updates.

### Option 2 — Install a single skill

```bash
mkdir -p ~/.claude/skills
ln -s ~/alphaskills/skills/stock-signal-report ~/.claude/skills/
```

Or just copy the `SKILL.md` into `~/.claude/skills/<name>/SKILL.md`.

### Option 3 — Per-project install

```bash
# From inside your project directory
mkdir -p .claude/skills
cp -r ~/alphaskills/skills/sec-insider-scan .claude/skills/
# Repeat for other skills you want
```

## Usage

Once installed, in any Claude chat:

```
/skill sec-insider-scan NVDA
/skill hedge-fund-holdings berkshire
/skill activist-campaign-tracker ackman
/skill clinical-trial-intel "Eli Lilly Phase 3"
/skill stock-signal-report TSLA
/skill company-deepdive MRNA
/skill futures-positioning-check gold
/skill fred-economic-data UNRATE
/skill arxiv-paper-scan "LLM reasoning"
/skill pubmed-paper-scan "GLP-1 Alzheimer's"
/skill biorxiv-preprint-scan "CRISPR sickle cell"
/skill nih-grant-scan "cancer CRISPR"
/skill vehicle-recall-check "Tesla Model 3 2023"
/skill fda-drug-recalls-faers metformin
/skill federal-register-tracker "SEC cryptocurrency"
/skill courtlistener-docket-tracker "Apple patent"
/skill github-repo-intel "anthropics/skills"
/skill sec-s1-ipo-tracker "last 30 days"
```

Or ask in natural language — Claude will auto-invoke the right skill based on the description.

## Architecture

Every skill is a single `SKILL.md` with:

- **YAML frontmatter** — `name` and `description` (Claude uses this for auto-invocation matching)
- **Markdown body** — procedural instructions:
  - When to invoke (triggers)
  - Required input
  - Output format (tables, narratives)
  - Data source + API endpoints + parsing rules
  - Classification / scoring logic
  - Example invocations with real expected output
  - Relationship to other skills

No JavaScript. No dependencies. No build step. Just Claude reading markdown and making HTTP calls at your request.

The complete repo structure:

```
alphaskills/
├── README.md                      # this file
├── LICENSE                        # MIT
├── .plugin-manifest.json          # Claude Code plugin metadata
├── install.sh                     # bash installer (symlinks skills)
├── install.ps1                    # PowerShell installer
└── skills/                        # 18 skill directories
    ├── sec-insider-scan/SKILL.md
    ├── hedge-fund-holdings/SKILL.md
    ├── activist-campaign-tracker/SKILL.md
    ├── clinical-trial-intel/SKILL.md
    ├── stock-signal-report/SKILL.md
    ├── futures-positioning-check/SKILL.md
    ├── arxiv-paper-scan/SKILL.md
    ├── nih-grant-scan/SKILL.md
    ├── vehicle-recall-check/SKILL.md
    ├── company-deepdive/SKILL.md
    ├── federal-register-tracker/SKILL.md
    ├── fda-drug-recalls-faers/SKILL.md
    ├── fred-economic-data/SKILL.md
    ├── courtlistener-docket-tracker/SKILL.md
    ├── github-repo-intel/SKILL.md
    ├── pubmed-paper-scan/SKILL.md
    ├── biorxiv-preprint-scan/SKILL.md
    └── sec-s1-ipo-tracker/SKILL.md
```

## What you replace — in dollars

If your team currently pays for any of:

- Bloomberg Terminal ($25,000-35,000/year/seat)
- FactSet ($12,000+/year/seat)
- Capital IQ ($10,000-20,000/year/seat)
- Citeline Trialtrove ($25,000-100,000/year)
- GlobalData ($30,000+/year)
- ActivistInsight ($20,000-100,000/year)
- Bloomberg Government ($5,000-25,000/year)
- Citeline + Evaluate Pharma ($50,000+/year)
- Westlaw / LexisNexis ($500-2,000/month each)
- InsiderScore ($99-499/month)
- WhaleWisdom ($99-499/month)
- GrantForward ($300+/year)
- OSS Insight ($99+/month)

**Combined: typically $50,000-$300,000/year per analyst seat.**

AlphaSkills delivers the underlying data queries for **$0 install + Claude inference cost (~$0.10-1.00 per deep report)**. That's a 1,000-100,000× cost reduction.

## Free (mostly) — API key situation

| Skill | API key required? |
|-------|-------------------|
| All SEC skills | No |
| NIH Grants | No |
| ClinicalTrials.gov | No |
| arXiv | No |
| bioRxiv / medRxiv | No |
| NHTSA recalls | No |
| CFTC COT | No |
| Federal Register | No |
| PubMed | No (free key optional for higher rate limits) |
| FDA openFDA | No (free key optional for higher rate limits) |
| CourtListener | Yes (free token) |
| FRED | Yes (free key) |
| GitHub | No (strongly recommended — free personal access token gives 83× higher rate limit) |

So: 13 of 18 skills need nothing. The remaining 5 need a free key that takes 60 seconds to generate.

## Why skills (not an API, not an app)?

**Skills are the new open standard for extending LLM agents.**

- **Anthropic** (December 2025 Agent Skills specification)
- **OpenAI** (adopted the same format for Codex CLI and ChatGPT)
- **Claude Desktop, Claude Code, Claude Projects** — all load skills from `~/.claude/skills/`
- **skillsmp.com** — emerging public marketplace
- **github.com/anthropics/skills** — Anthropic's reference implementation

A skill is portable, auditable, versionable markdown. No vendor lock-in. No API surface to maintain. No distribution friction. You own your skills forever.

## Complementary AlphaStack products

For programmatic bulk data (not interactive Q&A), these skills have companion Apify actors at [apify.com/wiry_kingdom](https://apify.com/wiry_kingdom):

| Skill | Apify actor |
|-------|-------------|
| sec-insider-scan | sec-form4-insider-trades |
| hedge-fund-holdings | sec-13f-holdings-tracker |
| activist-campaign-tracker | sec-13d-activist-filings |
| clinical-trial-intel | clinicaltrials-pipeline-monitor |
| stock-signal-report | stock-alpha-aggregator |
| futures-positioning-check | cftc-cot-report-tracker |
| arxiv-paper-scan | arxiv-paper-tracker |
| nih-grant-scan | nih-grants-tracker |
| vehicle-recall-check | nhtsa-recalls-tracker |

**Skills** = interactive Q&A inside Claude. **Actors** = scheduled batch data extraction.

## License

MIT. The skills and their instructions are open-source. The underlying API data is US government / academic public domain.

## Built by

[@Mohye24k](https://github.com/Mohye24k)

Part of the AlphaStack family:

- **AlphaStack Apify actors** — 20 production data wrappers on [Apify Store](https://apify.com/wiry_kingdom)
- **AlphaSkills (this repo)** — 18 Claude Code skills
- **Atlas MCP servers** — 6 Claude Code MCP servers on [npm](https://www.npmjs.com/~dean24k)

Distribution channels:

- GitHub: github.com/Mohye24k/alphaskills
- skillsmp.com (pending submission)
- Claude Skills Gallery (pending submission to anthropics/skills)

## Contributing

PRs welcome. To add a new skill:

1. Create `skills/<your-skill-name>/SKILL.md`
2. Use YAML frontmatter with `name` (max 64 chars) and `description` (max 1024 chars, third person, states what + when)
3. Add an entry to `.plugin-manifest.json`
4. Update this README
5. PR

See `skills/skill-creator/SKILL.md` (if installed) or the anthropics/skills repo for the canonical spec.
