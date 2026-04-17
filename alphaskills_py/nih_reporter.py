"""NIH RePORTER grants search. Free public API, no key required."""

from __future__ import annotations
from typing import Any, Optional

from ._http import post_json


API_URL = "https://api.reporter.nih.gov/v2/projects/search"


def search(
    agencies: Optional[list[str]] = None,
    fiscal_years: Optional[list[int]] = None,
    search_terms: Optional[str] = None,
    pi_names: Optional[list[str]] = None,
    org_names: Optional[list[str]] = None,
    *,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Search NIH RePORTER grants. Returns a list of project dicts."""
    criteria: dict[str, Any] = {"include_active_projects": True}
    if agencies:
        criteria["agencies"] = [a.upper() for a in agencies]
    if fiscal_years:
        criteria["fiscal_years"] = fiscal_years
    if search_terms:
        criteria["advanced_text_search"] = {
            "operator": "and",
            "search_field": "all",
            "search_text": search_terms,
        }
    if pi_names:
        criteria["pi_names"] = [{"any_name": n} for n in pi_names]
    if org_names:
        criteria["org_names"] = org_names

    # NOTE: Intentionally omit include_fields — the filter has surprising case
    # sensitivity and incorrect values silently drop response fields.
    body = {
        "criteria": criteria,
        "limit": limit,
        "offset": offset,
        "sort_field": "project_start_date",
        "sort_order": "desc",
    }
    resp = post_json(API_URL, body)
    return resp.get("results", [])


def normalize(project: dict) -> dict:
    """Normalize a raw NIH project dict into the canonical AlphaSkills shape."""
    pis = project.get("principal_investigators") or []
    pi = pis[0] if pis else {}
    org = project.get("organization") or {}
    agency = project.get("agency_ic_admin") or {}
    return {
        "projectNumber": project.get("project_num"),
        "coreProjectNumber": project.get("core_project_num"),
        "projectTitle": project.get("project_title"),
        "agency": agency.get("code") or agency.get("name"),
        "agencyName": agency.get("name"),
        "fiscalYear": project.get("fiscal_year"),
        "principalInvestigator": (
            f"{pi.get('last_name','')}, {pi.get('first_name','')}".strip(", ") if pi else None
        ),
        "organizationName": org.get("org_name"),
        "organizationCity": org.get("org_city"),
        "organizationState": org.get("org_state"),
        "totalCostUsd": project.get("award_amount"),
        "fundingMechanism": project.get("funding_mechanism"),
        "activityCode": project.get("activity_code"),
        "projectStartDate": project.get("project_start_date"),
        "projectEndDate": project.get("project_end_date"),
        "abstractText": project.get("abstract_text"),
        "projectUrl": project.get("project_detail_url")
            or (f"https://reporter.nih.gov/project-details/{project['appl_id']}"
                if project.get("appl_id") else None),
    }
