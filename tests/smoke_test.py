"""Quick sanity check that the Python helpers actually work.

Run:  python tests/smoke_test.py
"""

from __future__ import annotations
import sys
import json
from pathlib import Path

# Let the test run against the in-repo package without installing
sys.path.insert(0, str(Path(__file__).parent.parent))

from alphaskills_py import sec_edgar, clinical_trials, nih_reporter, cftc, nhtsa  # noqa: E402
from alphaskills_py import signals  # noqa: E402


def test_ticker_to_cik() -> None:
    print("\n>> ticker_to_cik('TSLA')")
    result = sec_edgar.ticker_to_cik("TSLA")
    assert result is not None and result["cik"] == "0001318605"
    print(f"  OK {result['company_name']} → CIK {result['cik']}")


def test_clinical_trials_search() -> None:
    print("\n>> clinical_trials.search(condition='cancer', pageSize=2)")
    result = clinical_trials.search(condition="pancreatic cancer", phases=["PHASE3"], page_size=2)
    studies = result.get("studies", [])
    print(f"  OK {len(studies)} studies returned")
    for s in studies[:2]:
        n = clinical_trials.normalize(s)
        print(f"    {n['nctId']}: {n['briefTitle'][:60]}")


def test_nih_search() -> None:
    print("\n>> nih_reporter.search(agencies=['NCI'], fiscal_years=[2026], limit=2)")
    result = nih_reporter.search(agencies=["NCI"], fiscal_years=[2026], limit=2)
    print(f"  OK {len(result)} grants")
    for p in result[:2]:
        n = nih_reporter.normalize(p)
        print(f"    {n['projectNumber']} — {n['organizationName'][:30]} — ${n['totalCostUsd'] or 0:,}")


def test_cftc() -> None:
    print("\n>> cftc.cot(markets=['GOLD'], limit=3)")
    result = cftc.cot(markets=["GOLD"], limit=3)
    print(f"  OK {len(result)} rows")
    for r in result[:2]:
        n = cftc.normalize(r)
        print(f"    {n['reportDate']} | {n['marketName'][:40]} | spec_net={n['noncommNet']}")


def test_nhtsa() -> None:
    print("\n>> nhtsa.recalls('Tesla', 'Model 3', 2023)")
    result = nhtsa.recalls("Tesla", "Model 3", 2023)
    print(f"  OK {len(result)} recalls")
    for r in result[:2]:
        print(f"    {r['nhtsaCampaignNumber']} | {r['component'][:50]} | OTA={r['overTheAirUpdate']}")


def test_signals_logic() -> None:
    print("\n>> signals.stock_alpha_signal(...) — rule logic")
    # Mock: NVDA-like heavy selling scenario
    form4 = [
        {"transactionType": "sell", "transactionValueUsd": 100_000_000, "insider": "A", "title": "CEO"},
        {"transactionType": "sell", "transactionValueUsd": 50_000_000, "insider": "B", "title": "CFO"},
        {"transactionType": "sell", "transactionValueUsd": 30_000_000, "insider": "C", "title": "Chief Scientist"},
    ] * 5  # 15 total filings
    eight_k = []
    score, label, reasons = signals.stock_alpha_signal(form4, eight_k)
    print(f"  OK Mock NVDA scenario → score={score} label={label}")
    print(f"    reasons: {len(reasons)} fired")
    assert label in ("BEARISH", "STRONGLY_BEARISH")


def main() -> int:
    tests = [
        test_ticker_to_cik,
        test_clinical_trials_search,
        test_nih_search,
        test_cftc,
        test_nhtsa,
        test_signals_logic,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n=== {passed} passed, {failed} failed ===")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
