"""bioRxiv + medRxiv preprint API client. Free, no key required."""

from __future__ import annotations
import datetime as _dt
from typing import Any, Optional

from ._http import get_json


BASE_URL = "https://api.biorxiv.org"


def recent(
    server: str = "biorxiv",
    days: int = 30,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Fetch recent preprints from the last N days. server = 'biorxiv' or 'medrxiv'."""
    end = _dt.date.today().isoformat()
    start = (_dt.date.today() - _dt.timedelta(days=days)).isoformat()
    url = f"{BASE_URL}/details/{server}/{start}/{end}/{offset}"
    data = get_json(url)
    return data.get("collection", [])


def by_doi(server: str, doi: str) -> Optional[dict]:
    """Fetch a specific preprint by DOI."""
    url = f"{BASE_URL}/details/{server}/{doi}"
    data = get_json(url)
    col = data.get("collection", [])
    return col[0] if col else None


def normalize(preprint: dict) -> dict:
    """Normalize a raw preprint dict."""
    return {
        "doi": preprint.get("doi"),
        "title": preprint.get("title"),
        "authors": [a.strip() for a in (preprint.get("authors") or "").split(";") if a.strip()],
        "correspondingAuthor": preprint.get("author_corresponding"),
        "correspondingInstitution": preprint.get("author_corresponding_institution"),
        "date": preprint.get("date"),
        "version": preprint.get("version"),
        "type": preprint.get("type"),
        "license": preprint.get("license"),
        "category": preprint.get("category"),
        "abstract": preprint.get("abstract"),
        "pdfUrl": f"https://www.biorxiv.org/content/{preprint.get('doi')}v{preprint.get('version', '1')}.full.pdf"
            if preprint.get("doi") else None,
    }
