"""ClinicalTrials.gov v2 API client. Free, no key required."""

from __future__ import annotations
from typing import Any, Optional

from ._http import get_json


API_URL = "https://clinicaltrials.gov/api/v2/studies"


def search(
    condition: Optional[str] = None,
    intervention: Optional[str] = None,
    sponsor: Optional[str] = None,
    phases: Optional[list[str]] = None,
    statuses: Optional[list[str]] = None,
    country: Optional[str] = None,
    *,
    page_size: int = 100,
    page_token: Optional[str] = None,
) -> dict[str, Any]:
    """Search ClinicalTrials.gov. Returns raw API response with studies[]."""
    params: dict[str, Any] = {"format": "json", "pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    if condition:
        params["query.cond"] = condition
    if intervention:
        params["query.intr"] = intervention
    if sponsor:
        params["query.lead"] = sponsor
    if country:
        params["query.locn"] = country

    adv = []
    if phases:
        adv.append(f"AREA[Phase]({' OR '.join(phases)})")
    if statuses:
        adv.append(f"AREA[OverallStatus]({' OR '.join(statuses)})")
    if adv:
        params["filter.advanced"] = " AND ".join(adv)

    return get_json(API_URL, params=params)


def normalize(study: dict) -> dict:
    """Reduce a raw CT.gov study into the canonical AlphaSkills shape."""
    ps = study.get("protocolSection") or {}
    ident = ps.get("identificationModule") or {}
    status = ps.get("statusModule") or {}
    design = ps.get("designModule") or {}
    sponsors = ps.get("sponsorCollaboratorsModule") or {}
    conditions = ps.get("conditionsModule") or {}
    arms = ps.get("armsInterventionsModule") or {}
    locations = ps.get("contactsLocationsModule") or {}
    enrollment = design.get("enrollmentInfo") or {}
    lead = sponsors.get("leadSponsor") or {}
    interventions = arms.get("interventions") or []
    locs = locations.get("locations") or []

    return {
        "nctId": ident.get("nctId"),
        "briefTitle": ident.get("briefTitle"),
        "officialTitle": ident.get("officialTitle"),
        "status": status.get("overallStatus"),
        "phases": design.get("phases") or [],
        "studyType": design.get("studyType"),
        "leadSponsor": lead.get("name"),
        "sponsorClass": lead.get("class"),
        "enrollmentCount": enrollment.get("count"),
        "enrollmentType": enrollment.get("type"),
        "conditions": conditions.get("conditions") or [],
        "interventionNames": [i.get("name") for i in interventions],
        "startDate": (status.get("startDateStruct") or {}).get("date"),
        "primaryCompletionDate": (status.get("primaryCompletionDateStruct") or {}).get("date"),
        "completionDate": (status.get("completionDateStruct") or {}).get("date"),
        "locationCount": len(locs),
        "countries": list({l.get("country") for l in locs if l.get("country")}),
        "ctGovUrl": (f"https://clinicaltrials.gov/study/{ident['nctId']}"
                     if ident.get("nctId") else None),
    }
