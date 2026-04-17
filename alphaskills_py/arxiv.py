"""arXiv paper search via the Atom query API. Free, no key required."""

from __future__ import annotations
import re
import time
from typing import Any, Optional

from ._http import get_text


API_URL = "http://export.arxiv.org/api/query"
_last_query_at = 0.0


def _polite_sleep() -> None:
    """arXiv asks for 3 seconds between requests."""
    global _last_query_at
    elapsed = time.time() - _last_query_at
    if elapsed < 3.0:
        time.sleep(3.0 - elapsed)
    _last_query_at = time.time()


def _build_query(
    categories: Optional[list[str]] = None,
    search_query: Optional[str] = None,
    authors: Optional[list[str]] = None,
) -> str:
    parts = []
    if categories:
        parts.append("(" + "+OR+".join(f"cat:{c}" for c in categories) + ")")
    if search_query:
        parts.append(f"({search_query.replace(' ', '+')})")
    if authors:
        au_parts = "+OR+".join(f'au:"{a.replace(" ", "+")}"' for a in authors)
        parts.append(f"({au_parts})")
    return "+AND+".join(parts) if parts else "all"


def search(
    categories: Optional[list[str]] = None,
    search_query: Optional[str] = None,
    authors: Optional[list[str]] = None,
    *,
    max_results: int = 50,
    sort_by: str = "submittedDate",
) -> list[dict[str, Any]]:
    """Search arXiv. Returns a list of paper dicts."""
    _polite_sleep()

    q = _build_query(categories, search_query, authors)
    url = f"{API_URL}?search_query={q}&start=0&max_results={max_results}&sortBy={sort_by}&sortOrder=descending"
    # DON'T double-URL-encode — arXiv's query syntax uses + and : literally
    xml = get_text(url)

    results = []
    entries = re.findall(r"<entry>([\s\S]*?)</entry>", xml)
    for e in entries:
        m = re.search(r"<id>([^<]+)</id>", e)
        id_url = m.group(1) if m else ""
        arxiv_id = id_url.replace("http://arxiv.org/abs/", "").strip()

        authors_list = re.findall(r"<name>([^<]+)</name>", e)
        categories_list = re.findall(r'<category term="([^"]+)"', e)
        primary_m = re.search(r'<arxiv:primary_category[^>]*term="([^"]+)"', e)

        results.append({
            "arxivId": arxiv_id,
            "title": _clean(re.search(r"<title>([\s\S]*?)</title>", e).group(1)) if re.search(r"<title>", e) else None,
            "abstract": _clean(re.search(r"<summary>([\s\S]*?)</summary>", e).group(1)) if re.search(r"<summary>", e) else None,
            "authors": [a.strip() for a in authors_list],
            "categories": categories_list,
            "primaryCategory": primary_m.group(1) if primary_m else (categories_list[0] if categories_list else None),
            "publishedAt": _tag(e, "published"),
            "updatedAt": _tag(e, "updated"),
            "doi": _tag(e, "arxiv:doi"),
            "comment": _tag(e, "arxiv:comment"),
            "journalRef": _tag(e, "arxiv:journal_ref"),
            "absUrl": f"https://arxiv.org/abs/{arxiv_id}",
            "pdfUrl": f"https://arxiv.org/pdf/{arxiv_id}",
        })
    return results


def _tag(xml: str, tag: str) -> Optional[str]:
    m = re.search(rf"<{re.escape(tag)}[^>]*>([\s\S]*?)</{re.escape(tag)}>", xml)
    return _clean(m.group(1)) if m else None


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()
