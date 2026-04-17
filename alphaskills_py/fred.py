"""Federal Reserve FRED economic data. Requires a free API key."""

from __future__ import annotations
import os
from typing import Any, Optional

from ._http import get_json


def _api_key(override: Optional[str]) -> str:
    key = override or os.environ.get("FRED_API_KEY")
    if not key:
        raise RuntimeError(
            "FRED_API_KEY not set. Get a free key at "
            "https://fred.stlouisfed.org/docs/api/api_key.html"
        )
    return key


def observations(series_id: str, *, api_key: Optional[str] = None, limit: int = 100) -> list[dict]:
    """Get observations for a FRED series (e.g. UNRATE, CPIAUCSL, DFF)."""
    params = {
        "series_id": series_id,
        "api_key": _api_key(api_key),
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
    }
    data = get_json(
        "https://api.stlouisfed.org/fred/series/observations",
        params=params,
    )
    return data.get("observations", [])


def series_info(series_id: str, *, api_key: Optional[str] = None) -> dict[str, Any]:
    """Get metadata (title, units, frequency, seasonal_adjustment) for a series."""
    params = {
        "series_id": series_id,
        "api_key": _api_key(api_key),
        "file_type": "json",
    }
    data = get_json("https://api.stlouisfed.org/fred/series", params=params)
    return (data.get("seriess") or [{}])[0]


def search(term: str, *, api_key: Optional[str] = None, limit: int = 10) -> list[dict]:
    """Search for FRED series by text term."""
    params = {
        "search_text": term,
        "api_key": _api_key(api_key),
        "file_type": "json",
        "limit": limit,
    }
    data = get_json("https://api.stlouisfed.org/fred/series/search", params=params)
    return data.get("seriess", [])
