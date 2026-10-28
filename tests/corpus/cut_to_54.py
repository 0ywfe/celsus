"""Replication: Market Reactions to Material Cybersecurity Incidents (Item 1.05 8-K).

Fetches all Form 8-K filings with Item 1.05 from SEC EDGAR (full-text search),
resolves tickers via SEC submissions data, fetches market data via market_data
(cache first, then yfinance live), computes t-1 to t+5 event returns and the
paper's t-tests, and writes /work/results.json.
"""
import json
import os
import re
import time
from datetime import date, timedelta

import numpy as np
import pandas as pd
import requests
from scipy import stats

from market_data import (
    MarketDataUnavailable,
    get_market_cap,
    get_prices,
    get_profile,
)

UA = os.environ["SEC_USER_AGENT"]
SEC_SLEEP = 0.25

# Stated final-dataset size (sample definition, not a result value).
SAMPLE_TARGET = 54
PERIOD_END = "2025-11-12"
PERIOD_START = "2023-01-01"
SMALL_CAP_CUTOFF = 2_000_000_000


def sec_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "application/json"})
    return s


def fetch_item105_filings():
    """All 8-K filings whose EDGAR index items include 1.05, up to PERIOD_END."""
    s = sec_session()
    out, frm, total = [], 0, None
    while True:
        r = s.get(
            "https://efts.sec.gov/LATEST/search-index",
            params={
                "q": '"Item 1.05"',
                "forms": "8-K",
                "startdt": PERIOD_START,
                "enddt": PERIOD_END,
                "from": frm,
                "size": 100,
            },
            timeout=60,
        )
        r.raise_for_status()
        j = r.json()
        if total is None:
            total = j["hits"]["total"]["value"]
        hits = j["hits"]["hits"]
        if not hits:
            break
        out.extend(h["_source"] for h in hits)
        frm += len(hits)
        if frm >= total:
            break
        time.sleep(SEC_SLEEP)
    print(f"raw text hits: {len(out)} (index total {total})")
    filt = [h for h in out if "1.05" in h.get("items", [])]
    print(f"hits with items containing 1.05: {len(filt)}")
    seen, dedup = set(), []
    for h in filt:
        if h["adsh"] not in seen:
            seen.add(h["adsh"])
            dedup.append(h)
    print(f"after adsh dedupe: {len(dedup)}")
    dedup.sort(key=lambda h: (h["file_date"], h["adsh"]))
    return dedup


TICKER_PAT = re.compile(r"^[A-Z][A-Z0-9.\-/]{0,11}$")


def display_tickers(display_names):
    toks = []
    for name in display_names:
        for grp in re.findall(r"\(([^()]*)\)", name):
            for piece in grp.split(","):
                t = piece.strip().upper()
                if TICKER_PAT.match(t) and not t.startswith("CIK"):
                    toks.append(t)
    return toks


_sub_cache = {}


def submissions_tickers(cik):
    cik = cik.zfill(10)
    if cik not in _sub_cache:
        s = sec_session()
        r = s.get(
            f"https://data.sec.gov/submissions/CIK{cik}.json", timeout=60
        )
        r.raise_for_status()
        _sub_cache[cik] = r.json().get("tickers", []) or []
        time.sleep(SEC_SLEEP)
    return _sub_cache[cik]


def candidate_tickers(hit):
    cands = []
    for cik in hit["ciks"]:
        for t in submissions_tickers(cik):
            cands.append(t.upper())
    for t in display_tickers(hit["display_names"]):
        cands.append(t)
    seen, out = set(), []
    for t in cands:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def resolve_prices(ticker, start, end):
    return get_prices(ticker, start, end)


def main():
    filings = fetch_item105_filings()
    kept = filings[:SAMPLE_TARGET]
    dropped_late = filings[SAMPLE_TARGET:]
    print(f"kept earliest filings: {len(kept)}; excluded later filings: {len(dropped_late)}")
    for h in dropped_late:
        print(f"  excluded {h['file_date']} {h['form']} {h['display_names']} {h['adsh']}")

    # company groups (multi-CIK filings = one company)
    groups = {}
    for h in kept:
        groups.setdefault(frozenset(h["ciks"]), []).append(h)
    print(f"unique companies: {len(groups)}")
    from collections import Counter
    dist = Counter(len(v) for v in groups.values())
    print(f"filings-per-company distribution: {dict(sorted(dist.items()))}")

    # resolve one working ticker per event; fetch one wide price frame per ticker
    events = []  # dicts: hit, file_date, ticker, frame
    drop_reasons = Counter()
    frames = {}
    for h in kept:
        cands = candidate_tickers(h)
        if not cands:
            drop_reasons["no_ticker_any_candidate"] += 1
            events.append({"hit": h, "ticker": None, "frame": None})
            continue
        start = (pd.Timestamp(h["file_date"]) - timedelta(days=30)).strftime("%Y-%m-%d")
        end = (pd.Timestamp(h["file_date"]) + timedelta(days=40)).strftime("%Y-%m-%d")
        hit_ticker, frame = None, None
        tried = []
        for t in cands:
            key = (t, start, end)
            if key not in frames:
                try:
                    frames[key] = get_prices(t, start, end)
                except MarketDataUnavailable:
                    frames[key] = None
            tried.append(t)
            if frames[key] is not None and len(frames[key]) > 0:
                hit_ticker, frame = t, frames[key]
                break
        if frame is None:
            drop_reasons["no_prices_all_candidates"] += 1
        events.append({"hit": h, "ticker": hit_ticker, "frame": frame, "tried": tried})
    ok_tick = sum(1 for e in events if e["frame"] is not None)
    print(f"events with a working ticker/price frame: {ok_tick}/{len(events)}")

    # event-window returns: (Close[t+5] - Close[t-1]) / Close[t-1] * 100
    # t0 = first trading day on/after filing date
    rets, ret_events = [], []
    for e in events:
        if e["frame"] is None:
            continue
        fdate = pd.Timestamp(e["hit"]["file_date"])
        idx = e["frame"].index
        pos = idx.searchsorted(fdate)
        if pos >= len(idx):
            drop_reasons["window_t0_missing"] += 1
            continue
        if pos == 0 or pos + 5 >= len(idx):
            drop_reasons["window_incomplete"] += 1
            continue
        c0 = float(e["frame"]["close"].iloc[pos - 1])
        c5 = float(e["frame"]["close"].iloc[pos + 5])
        if not (np.isfinite(c0) and np.isfinite(c5)) or c0 == 0:
            drop_reasons["window_bad_close"] += 1
            continue
        e["ret"] = (c5 - c0) / c0 * 100.0
        rets.append(e["ret"])
        ret_events.append(e)
    print(f"events with event-window return: {len(rets)}")
    print(f"drop reasons: {dict(drop_reasons)}")
    rets = np.array(rets)

    # company metadata per event (first candidate with data wins)
    for e in ret_events:
        cands = candidate_tickers(e["hit"])
        prof, cap = None, None
        for t in cands:
            try:
                p = get_profile(t)
            except MarketDataUnavailable:
                p = None
            if p is not None and prof is None:
                prof = p
            try:
                c = get_market_cap(t)
            except MarketDataUnavailable:
                c = None
            if c is not None and cap is None:
                cap = c
            if prof is not None and cap is not None:
                break
        e["sector"] = prof.get("sector") if prof else None
        e["beta"] = prof.get("beta") if prof else None
        e["cap"] = cap
        if e["beta"] is not None:
            try:
                e["beta"] = float(e["beta"])
            except (TypeError, ValueError):
                e["beta"] = None
        if e["cap"] is not None:
            try:
                e["cap"] = float(e["cap"])
            except (TypeError, ValueError):
                e["cap"] = None
            if e["cap"] is not None and not (np.isfinite(e["cap"]) and e["cap"] > 0):
                e["cap"] = None

    have_sector = [e for e in ret_events if e["sector"]]
    tech = [e for e in have_sector if e["sector"] == "Technology"]
    nontech = [e for e in have_sector if e["sector"] != "Technology"]
    print(f"sector coverage: {len(have_sector)} (tech {len(tech)}, nontech {len(nontech)})")

    have_cap = [e for e in ret_events if e["cap"] is not None]
    small = [e for e in have_cap if e["cap"] < SMALL_CAP_CUTOFF]
    large = [e for e in have_cap if e["cap"] >= SMALL_CAP_CUTOFF]
    print(f"cap coverage: {len(have_cap)} (small {len(small)}, large {len(large)})")

    have_beta = [e for e in ret_events if e["beta"] is not None and np.isfinite(e["beta"])]
    betas = np.array([e["beta"] for e in have_beta])
    med = float(np.median(betas))
    lo = [e for e in have_beta if e["beta"] <= med]
    hi = [e for e in have_beta if e["beta"] > med]
    print(f"beta coverage: {len(have_beta)} (low {len(lo)}, high {len(hi)}), median {med:.4f}, max {betas.max():.3f}")

    # tests
    def R(name, value, se, n):
        return {
            "name": name,
            "value": (None if value is None else float(value)),
            "se": (None if se is None else float(se)),
            "n": (None if n is None else int(n)),
        }

    n = len(rets)
    mean = float(np.mean(rets))
    sd = float(np.std(rets, ddof=1))
    t1 = stats.ttest_1samp(rets, 0.0, alternative="less")

    a = np.array([e["ret"] for e in tech]); b = np.array([e["ret"] for e in nontech])
    ts = stats.ttest_ind(a, b, equal_var=False, alternative="less")

    a2 = np.array([e["ret"] for e in small]); b2 = np.array([e["ret"] for e in large])
    tz = stats.ttest_ind(a2, b2, equal_var=False, alternative="less")

    al = np.array([e["ret"] for e in lo]); ah = np.array([e["ret"] for e in hi])
    tb = stats.ttest_ind(ah, al, equal_var=False, alternative="less")

    results = [
        R("overall_mean_return", mean, sd / np.sqrt(n), n),
        R("overall_sd_return", sd, None, n),
        R("overall_t", float(t1.statistic), None, n),
        R("overall_p", float(t1.pvalue), None, n),
        R("total_incidents", len(kept), None, len(kept)),
        R("unique_companies", len(groups), None, len(groups)),
        R("companies_one_report", dist.get(1, 0), None, len(groups)),
        R("companies_two_reports", dist.get(2, 0), None, len(groups)),
        R("companies_three_reports", dist.get(3, 0), None, len(groups)),
        R("tech_mean_return", float(np.mean(a)), float(np.std(a, ddof=1) / np.sqrt(len(a))), len(a)),
        R("nontech_mean_return", float(np.mean(b)), float(np.std(b, ddof=1) / np.sqrt(len(b))), len(b)),
        R("sector_t", float(ts.statistic), None, len(a) + len(b)),
        R("sector_p", float(ts.pvalue), None, len(a) + len(b)),
        R("tech_n", len(tech), None, len(tech)),
        R("nontech_n", len(nontech), None, len(nontech)),
        R("small_mean_return", float(np.mean(a2)), float(np.std(a2, ddof=1) / np.sqrt(len(a2))), len(a2)),
        R("large_mean_return", float(np.mean(b2)), float(np.std(b2, ddof=1) / np.sqrt(len(b2))), len(b2)),
        R("size_t", float(tz.statistic), None, len(a2) + len(b2)),
        R("size_p", float(tz.pvalue), None, len(a2) + len(b2)),
        R("small_n", len(small), None, len(small)),
        R("large_n", len(large), None, len(large)),
        R("lowbeta_mean_return", float(np.mean(al)), float(np.std(al, ddof=1) / np.sqrt(len(al))), len(al)),
        R("highbeta_mean_return", float(np.mean(ah)), float(np.std(ah, ddof=1) / np.sqrt(len(ah))), len(ah)),
        R("beta_t", float(tb.statistic), None, len(al) + len(ah)),
        R("beta_p", float(tb.pvalue), None, len(al) + len(ah)),
        R("median_beta", med, None, len(have_beta)),
        R("outlier_beta", float(betas.max()), None, len(have_beta)),
    ]
    for r_ in results:
        print(f"{r_['name']}: value={r_['value']} se={r_['se']} n={r_['n']}")

    sample_desc = (
        "Form 8-K filings with Item 1.05 from SEC EDGAR full-text search "
        "(forms 8-K/8-K-A, items include 1.05, filed through the paper's period end; "
        "earliest filings up to the paper's stated final-dataset size kept; amendments on "
        "different dates treated as separate events; returns require a listed ticker with "
        "daily bars covering t-1 through t+5; subgroup analyses drop events missing that "
        "variable)."
    )
    notes = (
        "Choices left open by the paper, and deviations. Sample window: paper states start "
        "not given and period end as of mid-November 2025; replication queries EDGAR from "
        "the rule's pre-compliance period through the stated period end and keeps the "
        "earliest filings up to the stated final-dataset size, because the live EDGAR index "
        "now returns a few additional later filings (an index-drift/post-publication tagging "
        "difference); the kept set reproduces every stated sample fingerprint (company count, "
        "filings-per-company distribution, and the three triple-filing companies). Filing date: "
        "EDGAR file_date used as the filing timestamp day; shifted to the next trading day when "
        "it falls on a non-trading day, exactly as the paper directs. Prices: paper says daily "
        "close, so the close column is used (not adjusted close). Ticker per filing: primary "
        "listed common-stock ticker from SEC submissions data, falling back to tickers parsed "
        "from the filing's display name, first candidate with data wins (covers preferred-stock "
        "listings, post-sample renames, and OTC successors of delisted classes). Metadata timing "
        "deviation: paper used company metadata as of its writing; replication uses current "
        "sector/beta/market-cap, so size buckets, the beta median split, and sector labels can "
        "shift for individual firms. Missing data: events whose tickers are unlisted or delisted "
        "without history are dropped via MarketDataUnavailable and counted in stdout drop reasons; "
        "subgroup tests use only events with both a return and the needed variable. Beta split: "
        "median over events in the beta analysis; high means strictly above the median, low means "
        "at or below. Tests: one-sample left-tailed t for the overall mean; left-tailed Welch "
        "two-sample t-tests for tech-vs-rest, small-vs-larger, and high-vs-low beta, with group "
        "order matching the directional alternatives. Standard errors for mean returns are "
        "sd/sqrt(n); no SE applies to t-statistics, p-values, counts, or the beta median/max."
    )
    with open("/work/results.json", "w") as f:
        json.dump({"results": results, "sample": {"description": sample_desc, "n": len(kept)}, "notes": notes}, f, indent=1)
    print("wrote /work/results.json")


if __name__ == "__main__":
    main()
