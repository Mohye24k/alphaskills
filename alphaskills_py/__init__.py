"""
alphaskills-py — the executable backbone behind AlphaSkills.

Import any of the submodules to get clean, structured access to free public
APIs. Designed to be invoked from within Claude Code skills via the Bash/Python
tool, so that skill instructions can say "import alphaskills_py" instead of
hand-rolling HTTP calls every time.

Modules:
    sec_edgar        — SEC EDGAR (Form 4, 13F, 13D, 8-K, 10-Q/K, S-1, submissions)
    nih_reporter     — NIH RePORTER grants
    clinical_trials  — ClinicalTrials.gov v2 API
    cftc             — CFTC Commitment of Traders Socrata API
    fred             — Federal Reserve FRED (requires API key)
    nhtsa            — NHTSA vehicle recalls
    arxiv            — arXiv paper search
    pubmed           — PubMed E-utilities
    biorxiv          — bioRxiv + medRxiv preprints
    fda              — FDA openFDA (recalls + FAERS)
    federal_register — US Federal Register
    signals          — the composite scoring logic for stock-alpha-aggregator,
                       ma-target-scanner, stealth-accumulation-detector, etc.

Usage:

    from alphaskills_py import sec_edgar, clinical_trials

    # 1. Get Tesla recent Form 4 insider trades
    trades = sec_edgar.form4_for_ticker('TSLA', days=90)

    # 2. Find Eli Lilly Phase 3 trials
    trials = clinical_trials.search(sponsor='Eli Lilly', phases=['PHASE3'])

All modules use `requests` (with a `User-Agent` header per SEC requirements)
and return plain Python dicts / lists for easy post-processing by Claude.
"""

__version__ = "0.1.0"

from . import (
    sec_edgar,
    nih_reporter,
    clinical_trials,
    cftc,
    fred,
    nhtsa,
    arxiv,
    pubmed,
    biorxiv,
    fda,
    federal_register,
    signals,
)

__all__ = [
    "sec_edgar",
    "nih_reporter",
    "clinical_trials",
    "cftc",
    "fred",
    "nhtsa",
    "arxiv",
    "pubmed",
    "biorxiv",
    "fda",
    "federal_register",
    "signals",
]
