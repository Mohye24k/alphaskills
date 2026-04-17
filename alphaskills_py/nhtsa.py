"""NHTSA vehicle recalls API. Free, no key required."""

from __future__ import annotations
import datetime as _dt
from typing import Any, Optional

from ._http import get_json


API_URL = "https://api.nhtsa.gov/recalls/recallsByVehicle"


def _parse_nhtsa_date(s: Optional[str]) -> Optional[str]:
    """NHTSA returns dates as DD/MM/YYYY. Parse to ISO (YYYY-MM-DD)."""
    if not s:
        return None
    parts = str(s).split("/")
    if len(parts) != 3:
        return None
    d, m, y = parts
    try:
        return f"{y}-{int(m):02d}-{int(d):02d}"
    except ValueError:
        return None


def recalls(make: str, model: str, model_year: int | str) -> list[dict[str, Any]]:
    """Pull recalls for a specific vehicle."""
    params = {"make": make, "model": model, "modelYear": str(model_year)}
    data = get_json(API_URL, params=params)
    results = data.get("results", []) or []
    out = []
    for r in results:
        out.append({
            "make": r.get("Make"),
            "model": r.get("Model"),
            "modelYear": int(r.get("ModelYear")) if r.get("ModelYear") else None,
            "manufacturer": r.get("Manufacturer"),
            "nhtsaCampaignNumber": r.get("NHTSACampaignNumber"),
            "component": r.get("Component"),
            "summary": r.get("Summary"),
            "consequence": r.get("Consequence"),
            "remedy": r.get("Remedy"),
            "notes": r.get("Notes"),
            "reportReceivedDate": _parse_nhtsa_date(r.get("ReportReceivedDate")),
            "overTheAirUpdate": r.get("overTheAirUpdate") is True,
            "parkIt": r.get("parkIt") is True,
            "parkOutside": r.get("parkOutSide") is True,
            "nhtsaActionNumber": r.get("NHTSAActionNumber"),
            "recallUrl": (f"https://www.nhtsa.gov/recalls?nhtsaId={r.get('NHTSACampaignNumber')}"
                         if r.get("NHTSACampaignNumber") else None),
        })
    return out
