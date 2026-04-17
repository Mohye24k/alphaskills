"""FDA openFDA API client — drug enforcement (recalls) + adverse events (FAERS)."""

from __future__ import annotations
import os
from typing import Any, Optional

from ._http import get_json


BASE_URL = "https://api.fda.gov"


def _maybe_key(override: Optional[str]) -> dict[str, str]:
    key = override or os.environ.get("OPENFDA_API_KEY")
    return {"api_key": key} if key else {}


def drug_recalls(
    product: Optional[str] = None,
    firm: Optional[str] = None,
    classification: Optional[str] = None,
    since_date: Optional[str] = None,
    *,
    limit: int = 100,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Query FDA drug recalls (enforcement reports)."""
    search_parts = []
    if product:
        search_parts.append(f'product_description:"{product}"')
    if firm:
        search_parts.append(f'recalling_firm:"{firm}"')
    if classification:
        search_parts.append(f'classification:"Class {classification}"')
    if since_date:
        until = "20991231"
        search_parts.append(f"report_date:[{since_date.replace('-','')} TO {until}]")
    params = {
        "search": " AND ".join(search_parts) if search_parts else "",
        "limit": limit,
        **_maybe_key(api_key),
    }
    if not params["search"]:
        del params["search"]
    data = get_json(f"{BASE_URL}/drug/enforcement.json", params=params)
    return data.get("results", []) or []


def drug_adverse_events_count(
    drug: str,
    *,
    api_key: Optional[str] = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Aggregate adverse event reaction counts from FAERS for a given drug.
    Returns a list of {term, count} sorted by frequency."""
    params = {
        "search": f'patient.drug.medicinalproduct:"{drug}"',
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": limit,
        **_maybe_key(api_key),
    }
    data = get_json(f"{BASE_URL}/drug/event.json", params=params)
    return data.get("results", []) or []


def drug_label_search(
    openfda_brand: Optional[str] = None,
    openfda_generic: Optional[str] = None,
    *,
    limit: int = 20,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Search drug label metadata (approved drug product information)."""
    search_parts = []
    if openfda_brand:
        search_parts.append(f'openfda.brand_name:"{openfda_brand}"')
    if openfda_generic:
        search_parts.append(f'openfda.generic_name:"{openfda_generic}"')
    params = {
        "search": " AND ".join(search_parts) if search_parts else "",
        "limit": limit,
        **_maybe_key(api_key),
    }
    data = get_json(f"{BASE_URL}/drug/label.json", params=params)
    return data.get("results", []) or []
