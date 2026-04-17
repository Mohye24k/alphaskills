"""CFTC Commitment of Traders (COT) weekly data via the Socrata API."""

from __future__ import annotations
import datetime as _dt
from typing import Any, Optional

from ._http import get_json


API_URL = "https://publicreporting.cftc.gov/resource/jun7-fc8e.json"


def cot(
    markets: Optional[list[str]] = None,
    since_date: Optional[str] = None,
    limit: int = 1000,
) -> list[dict[str, Any]]:
    """Pull COT rows for given markets. `markets` is a list of substrings
    (case-insensitive) that are matched against market_and_exchange_names."""
    if since_date is None:
        since_date = (_dt.date.today() - _dt.timedelta(days=90)).isoformat()

    where_parts = [f"report_date_as_yyyy_mm_dd >= '{since_date}T00:00:00.000'"]
    if markets:
        like_exprs = [
            f"(upper(market_and_exchange_names) like '%{m.upper().replace(chr(39), chr(39)*2)}%')"
            for m in markets
        ]
        where_parts.append("(" + " OR ".join(like_exprs) + ")")

    params: dict[str, Any] = {
        "$limit": limit,
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$where": " AND ".join(where_parts),
    }
    return get_json(API_URL, params=params)


def normalize(row: dict) -> dict:
    def num(k: str) -> Optional[int]:
        try:
            return int(row[k]) if row.get(k) is not None else None
        except (ValueError, TypeError):
            return None

    nc_long = num("noncomm_positions_long_all")
    nc_short = num("noncomm_positions_short_all")
    c_long = num("comm_positions_long_all")
    c_short = num("comm_positions_short_all")

    return {
        "reportDate": (row.get("report_date_as_yyyy_mm_dd") or "")[:10],
        "marketName": row.get("market_and_exchange_names"),
        "commodityName": row.get("commodity_name"),
        "openInterest": num("open_interest_all"),
        "noncommLong": nc_long,
        "noncommShort": nc_short,
        "noncommNet": (nc_long - nc_short) if (nc_long is not None and nc_short is not None) else None,
        "commLong": c_long,
        "commShort": c_short,
        "commNet": (c_long - c_short) if (c_long is not None and c_short is not None) else None,
        "tradersTotal": num("traders_tot_all"),
    }
