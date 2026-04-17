"""
SEC EDGAR helpers — Form 4 insider trades, 13F holdings, 13D filings, 8-K events,
S-1 IPO filings, and the canonical ticker→CIK mapping.

Used by: sec-insider-scan, hedge-fund-holdings, activist-campaign-tracker,
stock-signal-report, sec-s1-ipo-tracker, company-deepdive, catalyst-calendar,
ma-target-scanner, stealth-accumulation-detector skills.
"""

from __future__ import annotations
import re
import datetime as _dt
from typing import Any, Optional

from ._http import get_json, get_text


_TICKER_MAP_CACHE: Optional[dict[str, dict[str, str]]] = None


def ticker_to_cik(ticker: str) -> Optional[dict[str, str]]:
    """Resolve an equity ticker to {'cik': 10-digit, 'company_name': str}."""
    global _TICKER_MAP_CACHE
    if _TICKER_MAP_CACHE is None:
        data = get_json("https://www.sec.gov/files/company_tickers.json")
        _TICKER_MAP_CACHE = {}
        for entry in data.values():
            if entry.get("ticker") and entry.get("cik_str") is not None:
                t = str(entry["ticker"]).upper()
                _TICKER_MAP_CACHE[t] = {
                    "cik": str(entry["cik_str"]).zfill(10),
                    "company_name": entry.get("title", ""),
                }
    return _TICKER_MAP_CACHE.get(str(ticker).upper())


def submissions(cik: str) -> dict[str, Any]:
    """Fetch full submissions JSON for a CIK (returns filings metadata)."""
    cik = str(cik).zfill(10)
    return get_json(f"https://data.sec.gov/submissions/CIK{cik}.json")


def recent_filings(cik: str, form: str, since_days: int = 365, limit: int = 100) -> list[dict]:
    """List recent filings of a specific form type for a CIK."""
    data = submissions(cik)
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accs = recent.get("accessionNumber", [])
    dates = recent.get("filingDate", [])
    docs = recent.get("primaryDocument", [])
    items = recent.get("items", [])
    report_dates = recent.get("reportDate", [])

    cutoff = (_dt.date.today() - _dt.timedelta(days=since_days)).isoformat()
    results = []
    for i, f in enumerate(forms):
        if f != form:
            continue
        if dates[i] < cutoff:
            continue
        row = {
            "form": f,
            "accessionNumber": accs[i],
            "filingDate": dates[i],
            "primaryDocument": docs[i] if i < len(docs) else None,
            "items": items[i].split(",") if i < len(items) and items[i] else [],
            "reportDate": report_dates[i] if i < len(report_dates) else None,
        }
        results.append(row)
        if len(results) >= limit:
            break
    return results


# ────────────────────────────────── Form 4 ──────────────────────────────────

_TX_CODE = {
    "P": "Open-market purchase",
    "S": "Open-market sale",
    "M": "Option exercise",
    "F": "Sell-to-cover tax",
    "A": "Grant",
    "G": "Gift",
    "D": "Disposition to issuer",
    "C": "Derivative conversion",
    "X": "In-the-money option exercise",
    "O": "Out-of-the-money option exercise",
}


def classify_transaction(code: str) -> str:
    if code == "P":
        return "buy"
    if code in ("S", "D", "F"):
        return "sell"
    if code in ("M", "C", "X", "O"):
        return "option-exercise"
    if code == "A":
        return "grant"
    if code == "G":
        return "gift"
    return "other"


def _xml_tag(xml: str, tag: str) -> Optional[str]:
    """Get the text of a tag, handling <value>..</value> nested structure."""
    m = re.search(rf"<{tag}[^>]*>([\s\S]*?)</{tag}>", xml, re.IGNORECASE)
    if not m:
        return None
    inner = m.group(1).strip()
    vmatch = re.search(r"<value>([\s\S]*?)</value>", inner, re.IGNORECASE)
    if vmatch:
        return vmatch.group(1).strip()
    return inner


def _xml_blocks(xml: str, tag: str) -> list[str]:
    return re.findall(rf"<{tag}>([\s\S]*?)</{tag}>", xml)


def parse_form4_xml(xml: str) -> list[dict]:
    """Parse a Form 4 XML into a list of transaction dicts."""
    owner_name = _xml_tag(xml, "rptOwnerName")
    is_director = _xml_tag(xml, "isDirector") == "1"
    is_officer = _xml_tag(xml, "isOfficer") == "1"
    is_10pct = _xml_tag(xml, "isTenPercentOwner") == "1"
    title = _xml_tag(xml, "officerTitle")

    txs = []
    for block in _xml_blocks(xml, "nonDerivativeTransaction"):
        code = _xml_tag(block, "transactionCode")
        if not code:
            continue
        shares_s = _xml_tag(block, "transactionShares")
        price_s = _xml_tag(block, "transactionPricePerShare")
        try:
            shares = float(shares_s) if shares_s else None
        except ValueError:
            shares = None
        try:
            price = float(price_s) if price_s else None
        except ValueError:
            price = None
        value = shares * price if (shares and price) else None
        txs.append({
            "insider": owner_name,
            "title": title,
            "isDirector": is_director,
            "isOfficer": is_officer,
            "isTenPercentOwner": is_10pct,
            "transactionDate": _xml_tag(block, "transactionDate"),
            "transactionCode": code,
            "transactionCodeDescription": _TX_CODE.get(code, "Unknown"),
            "transactionType": classify_transaction(code),
            "shares": shares,
            "pricePerShare": price,
            "transactionValueUsd": round(value, 2) if value else None,
            "acquiredOrDisposed": _xml_tag(block, "transactionAcquiredDisposedCode"),
        })
    return txs


def download_form4_xml(cik: str, accession: str, primary_doc: str = "") -> Optional[str]:
    """Download a Form 4 raw XML for a given filing."""
    acc_no_dash = accession.replace("-", "")
    cik_num = str(int(cik))
    base = f"https://www.sec.gov/Archives/edgar/data/{cik_num}/{acc_no_dash}"
    xml_filename = re.sub(r"^xslF\d+X\d+/", "", primary_doc) if primary_doc else ""
    candidates = [
        f"{base}/{xml_filename}" if xml_filename else None,
        f"{base}/edgardoc.xml",
        f"{base}/primary_doc.xml",
    ]
    for url in candidates:
        if url is None:
            continue
        try:
            text = get_text(url)
            if text.lstrip().startswith("<?xml"):
                return text
        except Exception:
            continue
    return None


def form4_for_ticker(ticker: str, days: int = 90, max_filings: int = 25) -> list[dict]:
    """Top-level helper: return all insider transactions for a ticker."""
    mapping = ticker_to_cik(ticker)
    if not mapping:
        return []
    filings = recent_filings(mapping["cik"], "4", since_days=days, limit=max_filings)
    all_txs = []
    for f in filings:
        xml = download_form4_xml(mapping["cik"], f["accessionNumber"], f.get("primaryDocument", ""))
        if not xml:
            continue
        for tx in parse_form4_xml(xml):
            tx["filingDate"] = f["filingDate"]
            tx["accessionNumber"] = f["accessionNumber"]
            tx["issuerTicker"] = ticker.upper()
            all_txs.append(tx)
    return all_txs


# ────────────────────────────────── 13F ──────────────────────────────────

def thirteenf_information_table(cik: str, accession: str) -> list[dict]:
    """Parse the 13F-HR information table XML for a given filing."""
    acc_no_dash = accession.replace("-", "")
    cik_num = str(int(cik))
    base = f"https://www.sec.gov/Archives/edgar/data/{cik_num}/{acc_no_dash}"

    # Find the largest .xml file in the filing (it's the info table)
    idx = get_json(f"{base}/index.json")
    items = idx.get("directory", {}).get("item", [])
    xml_files = [
        (i["name"], int(i.get("size", 0) or 0))
        for i in items
        if i["name"].endswith(".xml") and "primary_doc" not in i["name"]
    ]
    if not xml_files:
        return []
    xml_files.sort(key=lambda x: -x[1])
    xml_url = f"{base}/{xml_files[0][0]}"
    xml = get_text(xml_url)

    # Match <(prefix:)?infoTable>...</(prefix:)?infoTable>
    blocks = re.findall(
        r"<(?:[\w-]+:)?infoTable[\s>][\s\S]*?</(?:[\w-]+:)?infoTable>", xml
    )
    results = []
    for b in blocks:
        inner_start = b.find(">") + 1
        inner_end = b.rfind("<")
        body = b[inner_start:inner_end]

        def nt(tag: str) -> Optional[str]:
            m = re.search(
                rf"<(?:[\w-]+:)?{tag}[^>]*>([\s\S]*?)</(?:[\w-]+:)?{tag}>",
                body,
                re.IGNORECASE,
            )
            return m.group(1).strip() if m else None

        def nested(tag: str) -> str:
            m = re.search(
                rf"<(?:[\w-]+:)?{tag}[^>]*>([\s\S]*?)</(?:[\w-]+:)?{tag}>",
                body,
                re.IGNORECASE,
            )
            return m.group(1) if m else ""

        shares_block = nested("shrsOrPrnAmt")
        voting_block = nested("votingAuthority")

        def sub(block: str, tag: str) -> Optional[str]:
            m = re.search(
                rf"<(?:[\w-]+:)?{tag}[^>]*>([\s\S]*?)</(?:[\w-]+:)?{tag}>",
                block,
                re.IGNORECASE,
            )
            return m.group(1).strip() if m else None

        try:
            shares = int(sub(shares_block, "sshPrnamt") or "0")
        except ValueError:
            shares = 0
        try:
            value = int(nt("value") or "0")
        except ValueError:
            value = 0
        results.append({
            "issuerName": nt("nameOfIssuer"),
            "titleOfClass": nt("titleOfClass"),
            "cusip": nt("cusip"),
            "figi": nt("figi"),
            "shares": shares,
            "sharesType": sub(shares_block, "sshPrnamtType"),
            "marketValueUsd": value,
            "investmentDiscretion": nt("investmentDiscretion"),
            "votingSole": int(sub(voting_block, "Sole") or "0"),
            "votingShared": int(sub(voting_block, "Shared") or "0"),
            "votingNone": int(sub(voting_block, "None") or "0"),
            "putCall": nt("putCall"),
            "isCallOption": nt("putCall") == "Call",
            "isPutOption": nt("putCall") == "Put",
        })
    return results


def latest_13f(cik: str) -> list[dict]:
    """Get the most recent 13F-HR holdings for a filer CIK."""
    filings = recent_filings(cik, "13F-HR", since_days=200, limit=1)
    if not filings:
        return []
    return thirteenf_information_table(cik, filings[0]["accessionNumber"])
