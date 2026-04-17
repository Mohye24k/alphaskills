# AlphaSkills

**Institutional-grade financial intelligence skills for Claude Code, Claude Projects, Claude Desktop, and OpenAI Codex CLI.**

10 skills that turn Claude into your personal Bloomberg Terminal analyst. One `/skill` invocation → full SEC insider trading analysis, hedge fund holdings breakdown, activist campaign tracking, clinical trial pipelines, futures positioning, arXiv research scans, NIH grants, vehicle recalls, or a full company deep-dive dossier.

Every skill uses **free public US government APIs** (SEC EDGAR, NIH RePORTER, ClinicalTrials.gov, CFTC, NHTSA, arXiv). No API keys. No subscriptions. No rate-limit hell. Just clean structured analysis inside your Claude.

## The skills

| Skill | What it does | Replaces |
|-------|-------------|----------|
| **sec-insider-scan** | Form 4 insider trading analysis for any ticker | InsiderScore $99–499/mo |
| **hedge-fund-holdings** | 13F quarterly holdings for any fund (Berkshire, Bridgewater, Citadel, etc.) | WhaleWisdom $99–499/mo |
| **activist-campaign-tracker** | 13D/G filings by activists (Icahn, Ackman, Loeb, Elliott) | ActivistInsight $20k–100k/yr |
| **clinical-trial-intel** | Pharma pipeline analysis by condition, drug, or sponsor | Citeline Trialtrove $25k–100k/yr |
| **stock-signal-report** | Unified bull/bear signal per ticker (insider + events + filings) | Bloomberg Terminal $25k/yr |
| **futures-positioning-check** | CFTC COT weekly positioning in any futures market | Bloomberg COT $25k/yr |
| **arxiv-paper-scan** | Search + summarize recent arXiv papers by topic / author | Semantic Scholar + Scite.ai $99+/mo |
| **nih-grant-scan** | NIH grants by agency, PI, institution, or keyword | GrantForward $300+/yr |
| **vehicle-recall-check** | NHTSA vehicle recalls by make / model / year | Carfax $40/VIN |
| **company-deepdive** | Master skill — invokes all the above for a full dossier | Bloomberg + Capital IQ + FactSet |

## Install (global — once)

```bash
# Clone the repo
git clone https://github.com/Mohye24k/alphaskills.git ~/alphaskills

# Install all skills into ~/.claude/skills/
cd ~/alphaskills
./install.sh           # macOS / Linux
.\install.ps1          # Windows PowerShell
```

The installer symlinks each skill from `~/alphaskills/skills/<name>/` into `~/.claude/skills/<name>/`, which makes them available to:

- **Claude Code** (via the `Skill` tool)
- **Claude Projects** (via the skills picker)
- **Claude Desktop** (via `/skills`)
- **OpenAI Codex CLI** (AGENTS.md-based skills — pass `--codex` flag to installer)

## Install (per-project)

If you want skills only in one project:

```bash
mkdir -p .claude/skills
cp -r ~/alphaskills/skills/sec-insider-scan .claude/skills/
# etc
```

## Usage

Once installed, in any Claude chat:

```
/skill sec-insider-scan NVDA
/skill hedge-fund-holdings berkshire
/skill activist-campaign-tracker ackman
/skill clinical-trial-intel "Eli Lilly Phase 3"
/skill stock-signal-report TSLA
/skill futures-positioning-check gold
/skill arxiv-paper-scan "LLM reasoning"
/skill nih-grant-scan "CRISPR"
/skill vehicle-recall-check "Tesla Model 3 2023"
/skill company-deepdive MRNA
```

Or Claude will auto-invoke them when your question matches the skill description.

## Architecture

Every skill is a single `SKILL.md` file with:

- **YAML frontmatter** — `name` and `description` (tells Claude when to invoke)
- **Markdown instructions** — full procedural docs including:
  - When to invoke (triggers)
  - Required input
  - Output format (tables, narratives)
  - Data source procedure (exact API calls)
  - Parsing rules
  - Classification / scoring rules
  - Example invocations

No JavaScript. No dependencies. No build step. Just Claude reading markdown instructions and making API calls at your request.

## Pricing

**The skills are free.** The underlying data is free (US government APIs). What you're paying for is Claude's inference cost, which is:

- **Claude Code** — consumed from your Max / Pro subscription
- **Claude Projects** — consumed from your subscription
- **Claude API direct** — $3–15 / million input tokens depending on model

A typical company deep-dive uses ~30k tokens of input context and ~3k tokens of output = ~$0.10 of Claude API cost.

**Compared to the incumbents this portfolio replaces (~$100k/yr combined for Bloomberg + Capital IQ + ActivistInsight + Citeline + WhaleWisdom), that's a ~1,000,000× cost reduction.**

## Why skills (not an app)?

Skills are the new open standard:

- **Adopted by Anthropic** (December 2025 Agent Skills specification)
- **Adopted by OpenAI** for Codex CLI and ChatGPT
- **Adopted by Claude Desktop, Claude Code, Claude Projects**
- **Public marketplace emerging** at github.com/anthropics/skills and skillsmp.com

A skill is portable, auditable markdown. No vendor lock-in. No API surface to break. No distribution friction.

## Complementary: AlphaStack Apify actors

For programmatic bulk data extraction (not interactive Q&A), see the complementary [AlphaStack Apify actors](https://apify.com/wiry_kingdom) — 20 production actors wrapping the same free public APIs into pay-per-event callable services. AlphaSkills is the interactive layer; AlphaStack is the automation layer.

## License

MIT. The skills and their instructions are open-source. The underlying API data is US government public domain.

## Built by

[@Mohye24k](https://github.com/Mohye24k)

Part of the AlphaStack family:

- **AlphaStack Apify actors** — 20 production data wrappers on [Apify Store](https://apify.com/wiry_kingdom)
- **Atlas MCP servers** — 6 Claude Code MCP servers on [npm](https://www.npmjs.com/~dean24k)
- **AlphaSkills (this repo)** — 10 Claude Code skills
