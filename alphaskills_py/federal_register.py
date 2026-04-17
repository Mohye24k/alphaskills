"""US Federal Register API client. Free, no key required."""

from __future__ import annotations
from typing import Any, Optional

from ._http import get_json


API_URL = "https://www.federalregister.gov/api/v1/documents.json"


def search(
    agencies: Optional[list[str]] = None,
    term: Optional[str] = None,
    doc_types: Optional[list[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    *,
    per_page: int = 50,
) -> list[dict[str, Any]]:
    """Search Federal Register documents."""
    params: dict[str, Any] = {"per_page": per_page}
    if agencies:
        params["conditions[agencies][]"] = agencies
    if term:
        params["conditions[term]"] = term
    if doc_types:
        params["conditions[type][]"] = doc_types
    if start_date:
        params["conditions[publication_date][gte]"] = start_date
    if end_date:
        params["conditions[publication_date][lte]"] = end_date

    data = get_json(API_URL, params=params)
    return data.get("results", []) or []


def agencies() -> list[dict[str, str]]:
    """List all Federal Register agencies (name + slug)."""
    data = get_json("https://www.federalregister.gov/api/v1/agencies.json")
    return data if isinstance(data, list) else []
