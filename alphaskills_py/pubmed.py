"""PubMed E-utilities client. Free; optional API key for higher rate limits."""

from __future__ import annotations
import os
import re
from typing import Any, Optional

from ._http import get_json, get_text


EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _maybe_key(override: Optional[str]) -> dict[str, str]:
    key = override or os.environ.get("NCBI_API_KEY")
    return {"api_key": key} if key else {}


def search_ids(
    term: str,
    *,
    max_results: int = 50,
    api_key: Optional[str] = None,
) -> list[str]:
    """Search PubMed and return a list of PMIDs."""
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "retmax": max_results,
        "sort": "date",
        **_maybe_key(api_key),
    }
    data = get_json(f"{EUTILS_BASE}/esearch.fcgi", params=params)
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_records(
    pmids: list[str],
    *,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Fetch PubMed records as parsed dicts (title, authors, journal, date, abstract, DOI)."""
    if not pmids:
        return []
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        **_maybe_key(api_key),
    }
    xml = get_text(f"{EUTILS_BASE}/efetch.fcgi", params=params)

    articles = re.findall(r"<PubmedArticle>([\s\S]*?)</PubmedArticle>", xml)
    results = []
    for a in articles:
        pmid = _tag(a, "PMID")
        title = _tag(a, "ArticleTitle") or ""
        abstract = _tag(a, "AbstractText") or ""
        journal = _tag(a, "ISOAbbreviation") or _tag(a, "Title") or ""
        year = _tag(a, "PubDate/Year") or _tag(a, "Year") or ""
        month = _tag(a, "PubDate/Month") or _tag(a, "Month") or ""
        pub_date = f"{year}-{month}" if year and month else (year or "")
        pub_types = re.findall(r"<PublicationType[^>]*>([^<]+)</PublicationType>", a)
        authors = re.findall(
            r"<Author[^>]*>[\s\S]*?<LastName>([^<]+)</LastName>[\s\S]*?<ForeName>([^<]+)</ForeName>",
            a,
        )
        doi_m = re.search(r'<ArticleId[^>]+IdType="doi"[^>]*>([^<]+)</ArticleId>', a)
        mesh_terms = re.findall(r"<DescriptorName[^>]*>([^<]+)</DescriptorName>", a)
        results.append({
            "pmid": pmid,
            "title": _clean(title),
            "abstract": _clean(abstract),
            "journal": journal,
            "pubDate": pub_date,
            "publicationTypes": pub_types,
            "authors": [f"{ln}, {fn}" for ln, fn in authors],
            "doi": doi_m.group(1).strip() if doi_m else None,
            "meshTerms": mesh_terms,
            "pubmedUrl": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
        })
    return results


def search(
    term: str,
    *,
    max_results: int = 20,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Convenience: search + fetch in one call."""
    ids = search_ids(term, max_results=max_results, api_key=api_key)
    return fetch_records(ids, api_key=api_key)


def _tag(xml: str, tag_path: str) -> Optional[str]:
    """Get text from a tag. For nested access use `Outer/Inner`."""
    tags = tag_path.split("/")
    m = re.search(rf"<{tags[0]}[^>]*>([\s\S]*?)</{tags[0]}>", xml)
    if not m:
        return None
    body = m.group(1)
    for t in tags[1:]:
        m2 = re.search(rf"<{t}[^>]*>([\s\S]*?)</{t}>", body)
        if not m2:
            return None
        body = m2.group(1)
    return body.strip()


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()
