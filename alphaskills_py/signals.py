"""
Signal scoring logic — the secret sauce behind stock-alpha-aggregator,
ma-target-scanner, stealth-accumulation-detector, short-squeeze-detector.

Each function takes a rich input dict and returns (score, label, reasons).
"""

from __future__ import annotations
from typing import Any


def stock_alpha_signal(
    form4_transactions: list[dict],
    eight_k_filings: list[dict],
) -> tuple[int, str, list[str]]:
    """Compute bull/bear signal from raw insider + 8-K data.
    See: skills/stock-signal-report/SKILL.md for rules.
    Score range: -10 to +10."""
    score = 0
    reasons: list[str] = []

    buys = [t for t in form4_transactions if t.get("transactionType") == "buy"]
    sells = [t for t in form4_transactions if t.get("transactionType") == "sell"]
    distinct_insiders = {t.get("insider") for t in form4_transactions if t.get("insider")}

    net_value = sum(
        (t.get("transactionValueUsd") or 0) * (1 if t.get("transactionType") == "buy" else -1)
        for t in form4_transactions
        if t.get("transactionType") in ("buy", "sell")
    )

    if buys and len(buys) > 0 and net_value > 0:
        score += 3
        reasons.append(f"Net insider BUYING: +{len(buys)} open-market purchases")
    if len(buys) >= 3:
        score += 2
        reasons.append(f"Cluster buy: {len(buys)} insider purchases (bullish cluster)")
    if len(form4_transactions) >= 5:
        score += 1
        reasons.append(f"High Form 4 filing velocity ({len(form4_transactions)} filings)")
    if sells and net_value < -1_000_000:
        score -= 3
        reasons.append(f"Net insider SELLING: ${abs(net_value):,.0f} of sales")
    if len(sells) >= 3 and len({t.get("insider") for t in sells}) >= 2:
        score -= 2
        reasons.append(
            f"Cluster sell: {len(sells)} sells by {len({t.get('insider') for t in sells})} distinct insiders"
        )

    c_suite_selling = any(
        t.get("transactionType") == "sell"
        and isinstance(t.get("title"), str)
        and any(k in t["title"] for k in ("CEO", "CFO", "COO", "Chief"))
        for t in form4_transactions
    )
    if c_suite_selling:
        score -= 1
        reasons.append("C-suite executive selling in lookback window")

    bullish_items = {"1.01": 1, "2.01": 2, "8.01": 1}
    bearish_items = {"1.03": -3, "2.06": -2, "3.01": -3, "4.02": -2}

    item_labels = {
        "1.01": "Material Definitive Agreement",
        "1.03": "Bankruptcy or Receivership",
        "2.01": "Completion of Acquisition",
        "2.06": "Material Impairments",
        "3.01": "Notice of Delisting",
        "4.02": "Non-Reliance on Prior Financials",
        "8.01": "Other Events",
    }

    for filing in eight_k_filings:
        for item in filing.get("items", []):
            delta = bullish_items.get(item) or bearish_items.get(item)
            if delta:
                score += delta
                sign = "+" if delta > 0 else ""
                reasons.append(f"8-K Item {item} ({item_labels.get(item, '?')}): {sign}{delta}")

    if score >= 4:
        label = "STRONGLY_BULLISH"
    elif score >= 1:
        label = "BULLISH"
    elif score == 0:
        label = "NEUTRAL"
    elif score >= -3:
        label = "BEARISH"
    else:
        label = "STRONGLY_BEARISH"

    return score, label, reasons


def stealth_accumulation_score(
    thirteen_f_positions: list[dict],  # list of {fund_name, pct_of_float, put_call}
    insider_buys_above_vwap: int = 0,
    wsb_mentions_per_week: int = 0,
    short_interest_drop_pct: float = 0.0,
) -> tuple[int, str, list[str]]:
    """See: skills/stealth-accumulation-detector/SKILL.md"""
    score = 0
    reasons: list[str] = []

    just_under_5 = [p for p in thirteen_f_positions if 4.0 <= (p.get("pct_of_float") or 0) <= 4.9]
    if len(just_under_5) >= 3:
        score += 3
        reasons.append(
            f"13F just-under-5% clustering: {len(just_under_5)} funds at 4.0-4.9% (wolf pack signal)"
        )

    total_ownership = sum(p.get("pct_of_float") or 0 for p in thirteen_f_positions)
    if total_ownership >= 20:
        score += 2
        reasons.append(
            f"Aggregate institutional ownership at {total_ownership:.1f}% — significant concentration"
        )

    calls_held = [p for p in thirteen_f_positions if p.get("put_call") == "Call"]
    if calls_held:
        score += 3
        reasons.append(
            f"{len(calls_held)} funds disclosed call option positions (synthetic accumulation)"
        )

    if insider_buys_above_vwap >= 3:
        score += 2
        reasons.append(
            f"Insiders bought above VWAP on {insider_buys_above_vwap} occasions (confidence signal)"
        )

    if short_interest_drop_pct > 15:
        score += 2
        reasons.append(
            f"Short interest dropped {short_interest_drop_pct:.0f}% without price move"
        )

    if score >= 6:
        label = "HIGHLY_LIKELY_ACCUMULATION"
    elif score >= 3:
        label = "PROBABLE_ACCUMULATION"
    else:
        label = "MINOR_SIGNALS_ONLY"

    return score, label, reasons


def short_squeeze_score(
    short_interest_pct_of_float: float,
    days_to_cover: float,
    insider_buys_last_60d: int,
    wsb_mentions_per_week: int,
    thirteen_f_added_positions_qoq: int,
) -> tuple[int, str, list[str]]:
    """See: skills/short-squeeze-detector/SKILL.md"""
    score = 0
    reasons: list[str] = []

    if short_interest_pct_of_float >= 50:
        score += 4
        reasons.append(f"Short interest {short_interest_pct_of_float:.1f}% of float (extreme)")
    elif short_interest_pct_of_float >= 30:
        score += 3
        reasons.append(f"Short interest {short_interest_pct_of_float:.1f}% of float (very high)")
    elif short_interest_pct_of_float >= 20:
        score += 2
        reasons.append(f"Short interest {short_interest_pct_of_float:.1f}% of float (high)")
    elif short_interest_pct_of_float >= 15:
        score += 1
        reasons.append(f"Short interest {short_interest_pct_of_float:.1f}% of float (elevated)")

    if days_to_cover >= 10:
        score += 3
        reasons.append(f"Days-to-cover {days_to_cover:.1f} (very hard to exit)")
    elif days_to_cover >= 5:
        score += 2
        reasons.append(f"Days-to-cover {days_to_cover:.1f} (elevated)")
    elif days_to_cover >= 2:
        score += 1

    if insider_buys_last_60d >= 2:
        score += 2
        reasons.append(f"{insider_buys_last_60d} insider buys counter-current (bullish contrarian)")

    if wsb_mentions_per_week >= 5000:
        score += 3
        reasons.append("Extreme r/wallstreetbets mention velocity (retail pile-in)")
    elif wsb_mentions_per_week >= 500:
        score += 2
        reasons.append("High r/wallstreetbets mention velocity")
    elif wsb_mentions_per_week >= 50:
        score += 1

    if thirteen_f_added_positions_qoq >= 3:
        score += 2
        reasons.append(f"{thirteen_f_added_positions_qoq} hedge funds added positions QoQ (smart money)")

    if score >= 10:
        label = "HIGHLY_LIKELY_SQUEEZE"
    elif score >= 7:
        label = "PROBABLE_SQUEEZE"
    elif score >= 4:
        label = "MODERATE_SETUP"
    else:
        label = "LOW_PROBABILITY"

    return score, label, reasons


def ma_target_score(
    activist_13d_present: bool = False,
    hedge_fund_13f_accumulation_qoq: int = 0,
    insider_buying_count: int = 0,
    recent_8k_item_8_01_exists: bool = False,
    valuation_discount_pct: float = 0.0,
    recent_banker_engagement: bool = False,
    sector_consolidation_18m_count: int = 0,
    has_poison_pill: bool = False,
    has_staggered_board_or_dual_class: bool = False,
) -> tuple[int, str, list[str]]:
    """See: skills/ma-target-scanner/SKILL.md"""
    score = 0
    reasons: list[str] = []

    if activist_13d_present:
        score += 3
        reasons.append("Activist 13D filing present — strategic alternatives likely within 12-18 mo")
    if hedge_fund_13f_accumulation_qoq >= 5:
        score += 2
        reasons.append(
            f"{hedge_fund_13f_accumulation_qoq} hedge funds added material positions QoQ (merger arb front-running)"
        )
    if insider_buying_count > 0:
        score += 3
        reasons.append(f"Insider buying ({insider_buying_count} purchases) — unusual before deals")
    if recent_8k_item_8_01_exists:
        score += 1
        reasons.append("Recent 8-K Item 8.01 — may disclose 'strategic alternatives' engagement")
    if valuation_discount_pct >= 30:
        score += 2
        reasons.append(f"{valuation_discount_pct:.0f}% valuation discount vs sector peers")
    elif valuation_discount_pct >= 20:
        score += 1
        reasons.append(f"{valuation_discount_pct:.0f}% valuation discount vs sector peers")
    if recent_banker_engagement:
        score += 2
        reasons.append("Company disclosed engagement with sell-side banker")
    if sector_consolidation_18m_count >= 2:
        score += 1
        reasons.append(
            f"Sector consolidation: {sector_consolidation_18m_count} similar deals in last 18mo"
        )
    if has_poison_pill:
        score -= 2
        reasons.append("Poison pill / shareholder rights plan — defensive, harder to acquire")
    if has_staggered_board_or_dual_class:
        score -= 1
        reasons.append("Staggered board or dual-class stock — defensive")

    if score >= 7:
        label = "HIGH_PROBABILITY_TARGET"
    elif score >= 4:
        label = "MEDIUM_PROBABILITY_TARGET"
    elif score >= 1:
        label = "WATCHLIST_ONLY"
    else:
        label = "NOT_A_TARGET"

    return score, label, reasons
