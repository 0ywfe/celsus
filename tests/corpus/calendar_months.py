"""Replication: Market Reactions to Material Cybersecurity Incidents (Item 1.05 8-K).

Builds the event sample from SEC EDGAR full-text search (all 8-K/8-K/A with
Item 1.05, file_date <= 2025-11-12), resolves tickers via SEC company_tickers
+ filing display names, fetches market data only through market_data module,
computes 7-trading-day event-window returns and the paper's t-tests.
"""
import calendar
import json
import os
import re
import time
import urllib.parse
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy import stats

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from market_data import get_prices, get_market_cap, get_profile, MarketDataUnavailable

UA = os.environ["SEC_USER_AGENT"]
EFTS = "https://efts.sec.gov/LATEST/search-index"
CUTOFF = "2025-11-12"
START = "2023-12-01"  # Item 1.05 rule effective Dec 2023; bound the query window
SMALL_CAP = 2e9
MID_CAP = 10e9
LARGE_CAP = 200e9


def sec_get_json(url, headers, tries=4):
    last = None
    for i in range(tries):
        try:
            import requests
            r = requests.get(url, headers=headers, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            time.sleep(2 * (i + 1))
    raise last


def fetch_edgar_events():
    """All filings with Item 1.05 via EDGAR full-text search, month slices."""
    import requests  # noqa: F401 (ensures presence)
    q = urllib.parse.quote('"Item 1.05"')
    H = {"User-Agent": UA, "Accept": "application/json", "Host": "efts.sec.gov"}
    union = {}
    y, m = 2023, 12
    while (y, m) <= (2025, 11):
        last = calendar.monthrange(y, m)[1]
        s, e = f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last}"
        url = f"{EFTS}?q={q}&forms=8-K&startdt={s}&enddt={e}&count=100"
        j = sec_get_json(url, H)
        hits = j["hits"]["hits"]
        for h in hits:
            if "1.05" in h["_source"].get("items", []):
                union[h["_id"]] = h
        print(f"EFTS slice {s}..{e}: returned {len(hits)}, item-1.05 so far {len(union)}", flush=True)
        time.sleep(0.4)
        m += 1
        if m > 12:
            y += 1
            m = 1
    events = []
    for hid, h in union.items():
        src = h["_source"]
        if not (START <= src["file_date"] <= CUTOFF):
            continue
        events.append({
            "id": hid,
            "adsh": src["adsh"],
            "file_date": src["file_date"],
            "form": src["form"],
            "ciks": [c.lstrip("0").zfill(10) if False else c for c in src["ciks"]],
            "ciks_raw": list(src["ciks"]),
            "display": list(src.get("display_names", [])),
            "items": list(src.get("items", [])),
        })
    # normalize CIK to 10-digit zero-padded
    for ev in events:
        ev["ciks"] = [c.zfill(10)[-10:] for c in ev["ciks_raw"]]
    events.sort(key=lambda e: (e["file_date"], e["adsh"]))
    return events


def fetch_cik_tickers():
    import requests
    url = "https://www.sec.gov/files/company_tickers.json"
    j = sec_get_json(url, {"User-Agent": UA, "Accept": "application/json"})
    by = defaultdict(list)
    for _, v in j.items():
        by[str(int(v["cik_str"])).zfill(10)].append(v["ticker"])
    return dict(by)


PREFERRED = {"PRU": "PRU", "T": "T", "HPE": "HPE", "RILY": "RILY", "ZCAR": "ZCAR"}


def resolve_ticker(cik, display, cik_map):
    cands = cik_map.get(cik, [])
    if cik in ("0001137774", "0000732717", "0001645590", "0001464790", "0001854275"):
        for t in cands:
            if t in PREFERRED.values():
                # pick the plain common-share ticker present for this CIK
                if (cik == "0001137774" and t == "PRU") or \
                   (cik == "0000732717" and t == "T") or \
                   (cik == "0001645590" and t == "HPE") or \
                   (cik == "0001464790" and t == "RILY") or \
                   (cik == "0001854275" and t == "ZCAR"):
                    return t
    if cands:
        # avoid warrant/preferred classes when a plain alternative exists is handled above
        return cands[0]
    for d in display:
        for tok in re.findall(r"\(([A-Z][A-Z0-9\-\.]{0,7})\)", d):
            if tok == "CIK":
                continue
            return tok
    return None


def main():
    print("Fields relied on: EFTS _source{adsh,file_date,form,ciks,display_names,items}; "
          "company_tickers{cik_str,ticker}; market_data prices[open,high,low,close,adj_close,volume] "
          "indexed by trading date; profile{sector,beta}; market cap USD.", flush=True)

    events = fetch_edgar_events()
    print(f"STEP 1 events with Item 1.05 in [{START},{CUTOFF}]: {len(events)}", flush=True)
    adshs = {e["adsh"] for e in events}
    print(f"STEP 2 unique accessions: {len(adshs)}", flush=True)
    if events:
        print("Sample record: " + json.dumps(events[0])[:400], flush=True)

    cik_map = fetch_cik_tickers()
    print(f"company_tickers CIKs: {len(cik_map)}", flush=True)

    # company = primary CIK (first listed); note co-filed secondary CIKs
    multi = [e for e in events if len(e["ciks"]) > 1]
    print(f"STEP 3 events with >1 CIK (co-filers, attributed to primary CIK): {len(multi)}", flush=True)
    for e in multi:
        print(f"  co-filed {e['file_date']} {e['adsh']} {e['ciks']}", flush=True)

    for e in events:
        e["cik"] = e["ciks"][0]
        e["ticker"] = resolve_ticker(e["cik"], e["display"], cik_map)
    no_ticker = [e for e in events if not e["ticker"]]
    print(f"STEP 4 events with resolved ticker: {len(events) - len(no_ticker)}; "
          f"no ticker (dropped): {len(no_ticker)}", flush=True)
    for e in no_ticker:
        print(f"  no-ticker {e['file_date']} {e['adsh']} {e['ciks']} {e['display']}", flush=True)

    companies = sorted({e["cik"] for e in events})
    print(f"STEP 5 unique primary-CIK companies in filing sample: {len(companies)}", flush=True)
    per_cik = Counter(e["cik"] for e in events)
    dist = Counter(per_cik.values())
    print(f"STEP 6 filings-per-company distribution: {dict(sorted(dist.items()))}", flush=True)

    # per-ticker market data (one fetch per ticker over union window)
    by_ticker = defaultdict(list)
    for e in events:
        if e["ticker"]:
            by_ticker[e["ticker"]].append(e)
    profiles, caps, price_frames = {}, {}, {}
    n_prof_fail = n_cap_fail = n_px_fail = 0
    for t, evs in sorted(by_ticker.items()):
        try:
            profiles[t] = get_profile(t)
        except MarketDataUnavailable:
            profiles[t] = None
            n_prof_fail += 1
        except Exception:
            raise
        try:
            caps[t] = get_market_cap(t)
        except MarketDataUnavailable:
            caps[t] = None
            n_cap_fail += 1
        except Exception:
            raise
        dates = [pd.Timestamp(e["file_date"]) for e in evs]
        s = (min(dates) - pd.Timedelta(days=30)).strftime("%Y-%m-%d")
        en = (max(dates) + pd.Timedelta(days=30)).strftime("%Y-%m-%d")
        try:
            price_frames[t] = get_prices(t, s, en)
        except MarketDataUnavailable:
            price_frames[t] = None
            n_px_fail += 1
        except Exception:
            raise
        time.sleep(0.05)
    print(f"STEP 7 tickers: {len(by_ticker)}; profile missing: {n_prof_fail}; "
          f"cap missing: {n_cap_fail}; prices missing: {n_px_fail}", flush=True)

    # event-window returns: close_{F'+5} vs close_{P}, F'=filing trading day
    rets, drop_reasons = [], Counter()
    for e in events:
        t = e["ticker"]
        if not t or price_frames.get(t) is None or price_frames[t] is None or len(price_frames[t]) == 0:
            drop_reasons["missing prices"] += 1
            continue
        df = price_frames[t]
        idx = df.index.sort_values()
        F = pd.Timestamp(e["file_date"])
        fut = idx[idx >= F.normalize()]
        if len(fut) == 0:
            # refetch wider window for late filings
            try:
                s2 = (F - pd.Timedelta(days=45)).strftime("%Y-%m-%d")
                e2 = (F + pd.Timedelta(days=45)).strftime("%Y-%m-%d")
                df = get_prices(t, s2, e2)
                price_frames[t] = df
                idx = df.index.sort_values()
                fut = idx[idx >= F.normalize()]
            except MarketDataUnavailable:
                drop_reasons["missing prices (window)"] += 1
                continue
            except Exception:
                raise
        if len(fut) == 0:
            drop_reasons["no trading day at/after filing"] += 1
            continue
        Fp = fut[0]
        pos = idx.get_loc(Fp)
        prev = idx[:pos]
        if len(prev) == 0 or pos + 5 >= len(idx):
            try:
                s2 = (F - pd.Timedelta(days=60)).strftime("%Y-%m-%d")
                e2 = (F + pd.Timedelta(days=60)).strftime("%Y-%m-%d")
                df = get_prices(t, s2, e2)
                price_frames[t] = df
                idx = df.index.sort_values()
                fut = idx[idx >= F.normalize()]
                Fp = fut[0]
                pos = idx.get_loc(Fp)
                prev = idx[:pos]
            except MarketDataUnavailable:
                drop_reasons["missing prices (window)"] += 1
                continue
            except Exception:
                raise
            if len(prev) == 0 or pos + 5 >= len(idx):
                drop_reasons["window incomplete"] += 1
                continue
        P = prev[-1]
        A5 = idx[pos + 5]
        try:
            c0 = float(df.loc[P, "close"])
            c1 = float(df.loc[A5, "close"])
        except Exception:
            drop_reasons["bad close values"] += 1
            continue
        if not np.isfinite(c0) or not np.isfinite(c1) or c0 <= 0:
            drop_reasons["bad close values"] += 1
            continue
        r = (c1 / c0 - 1.0) * 100.0
        e["ret"] = r
        e["P"] = P.strftime("%Y-%m-%d")
        e["Fp"] = Fp.strftime("%Y-%m-%d")
        e["A5"] = A5.strftime("%Y-%m-%d")
        prof = profiles.get(t) or {}
        e["sector"] = prof.get("sector")
        e["beta"] = prof.get("beta")
        e["cap"] = caps.get(t)
        rets.append(r)
    print(f"STEP 8 events with event-window return: {len(rets)}; dropped: {dict(drop_reasons)}", flush=True)

    ev_ret = [e for e in events if "ret" in e]
    x = np.array([e["ret"] for e in ev_ret], float)
    n = len(x)
    mean = float(np.mean(x))
    sd = float(np.std(x, ddof=1)) if n > 1 else float("nan")
    se_mean = float(sd / np.sqrt(n)) if n > 0 else None
    t1 = stats.ttest_1samp(x, 0.0, alternative="less")
    print(f"Overall: n={n} mean={mean:.4f}% sd={sd:.4f}% t={float(t1.statistic):.4f} p={float(t1.pvalue):.6f}", flush=True)

    def welch_less(a, b):
        a = np.array(a, float)
        b = np.array(b, float)
        t = stats.ttest_ind(a, b, equal_var=False, alternative="less")
        return float(t.statistic), float(t.pvalue)

    # sector
    tech = [e["ret"] for e in ev_ret if (e.get("sector") or None) == "Technology"]
    nontech = [e["ret"] for e in ev_ret if (e.get("sector") not in (None, "")) and e.get("sector") != "Technology"]
    n_sec_missing = n - len(tech) - len(nontech)
    print(f"Sector: tech n={len(tech)} mean={np.mean(tech) if len(tech) else float('nan'):.4f}; "
          f"nontech n={len(nontech)} mean={np.mean(nontech) if len(nontech) else float('nan'):.4f}; "
          f"missing sector: {n_sec_missing}", flush=True)
    t_sec, p_sec = welch_less(tech, nontech) if tech and nontech else (None, None)

    # size (current market cap vs $2B threshold)
    small = [e["ret"] for e in ev_ret if e.get("cap") is not None and np.isfinite(e["cap"]) and e["cap"] > 0 and e["cap"] < SMALL_CAP]
    larger = [e["ret"] for e in ev_ret if e.get("cap") is not None and np.isfinite(e["cap"]) and e["cap"] > 0 and e["cap"] >= SMALL_CAP]
    n_cap_missing = n - len(small) - len(larger)
    print(f"Size: small n={len(small)} mean={np.mean(small) if len(small) else float('nan'):.4f}; "
          f"larger n={len(larger)} mean={np.mean(larger) if len(larger) else float('nan'):.4f}; "
          f"missing/invalid cap: {n_cap_missing}", flush=True)
    t_size, p_size = welch_less(small, larger) if small and larger else (None, None)

    # beta median split (median over events with both return and beta)
    with_beta = [e for e in ev_ret if e.get("beta") is not None and np.isfinite(e["beta"])]
    betas = np.array([e["beta"] for e in with_beta], float)
    med = float(np.median(betas)) if len(betas) else None
    out = float(np.max(betas)) if len(betas) else None
    print(f"Beta: n with beta={len(with_beta)} median={med} max={out} missing={n - len(with_beta)}", flush=True)
    lo = [e["ret"] for e in with_beta if e["beta"] <= med]
    hi = [e["ret"] for e in with_beta if e["beta"] > med]
    print(f"Beta split at median: low(beta<=med) n={len(lo)} mean={np.mean(lo) if len(lo) else float('nan'):.4f}; "
          f"high n={len(hi)} mean={np.mean(hi) if len(hi) else float('nan'):.4f}", flush=True)
    t_beta, p_beta = welch_less(hi, lo) if hi and lo else (None, None)

    def mean_se(v):
        v = np.array(v, float)
        if len(v) == 0:
            return None, None, 0
        m = float(np.mean(v))
        se = float(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) > 1 else None
        return m, se, len(v)

    m_t, se_t, n_t = mean_se(tech)
    m_nt, se_nt, n_nt = mean_se(nontech)
    m_s, se_s, n_s = mean_se(small)
    m_l, se_l, n_l = mean_se(larger)
    m_lo, se_lo, n_lo = mean_se(lo)
    m_hi, se_hi, n_hi = mean_se(hi)

    results = [
        {"name": "n_filings_total", "value": float(len(events)), "se": None, "n": None},
        {"name": "n_companies_total", "value": float(len(companies)), "se": None, "n": None},
        {"name": "n_companies_one_report", "value": float(dist.get(1, 0)), "se": None, "n": None},
        {"name": "n_companies_two_reports", "value": float(dist.get(2, 0)), "se": None, "n": None},
        {"name": "n_companies_three_reports", "value": float(dist.get(3, 0)), "se": None, "n": None},
        {"name": "n_small", "value": float(n_s), "se": None, "n": n_s},
        {"name": "n_larger", "value": float(n_l), "se": None, "n": n_l},
        {"name": "n_tech", "value": float(n_t), "se": None, "n": n_t},
        {"name": "n_nontech", "value": float(n_nt), "se": None, "n": n_nt},
        {"name": "mean_return_overall", "value": mean, "se": se_mean, "n": n},
        {"name": "sd_return_overall", "value": sd, "se": None, "n": n},
        {"name": "t_overall", "value": float(t1.statistic), "se": None, "n": n},
        {"name": "p_overall", "value": float(t1.pvalue), "se": None, "n": n},
        {"name": "mean_return_tech", "value": m_t, "se": se_t, "n": n_t},
        {"name": "mean_return_nontech", "value": m_nt, "se": se_nt, "n": n_nt},
        {"name": "t_sector", "value": t_sec, "se": None, "n": n_t + n_nt if (t_sec is not None) else None},
        {"name": "p_sector", "value": p_sec, "se": None, "n": n_t + n_nt if (p_sec is not None) else None},
        {"name": "mean_return_small", "value": m_s, "se": se_s, "n": n_s},
        {"name": "mean_return_larger", "value": m_l, "se": se_l, "n": n_l},
        {"name": "t_size", "value": t_size, "se": None, "n": n_s + n_l if (t_size is not None) else None},
        {"name": "p_size", "value": p_size, "se": None, "n": n_s + n_l if (p_size is not None) else None},
        {"name": "mean_return_low_beta", "value": m_lo, "se": se_lo, "n": n_lo},
        {"name": "mean_return_high_beta", "value": m_hi, "se": se_hi, "n": n_hi},
        {"name": "t_beta", "value": t_beta, "se": None, "n": n_lo + n_hi if (t_beta is not None) else None},
        {"name": "p_beta", "value": p_beta, "se": None, "n": n_lo + n_hi if (p_beta is not None) else None},
        {"name": "beta_outlier", "value": out, "se": None, "n": len(betas)},
        {"name": "beta_median", "value": med, "se": None, "n": len(betas)},
    ]
    out_doc = {
        "results": results,
        "sample": {
            "description": (
                f"All EDGAR 8-K/8-K-A filings with Item 1.05 and file_date in [{START},{CUTOFF}] "
                f"({len(events)} accessions, {len(companies)} primary-CIK companies); event window prev "
                f"trading day before filing trading day through +5 trading days; return from close prices; "
                f"{n} events with complete price window."
            ),
            "n": len(events),
        },
        "notes": (
            "Sample built from EDGAR full-text search (month slices Dec 2023-Nov 2025, items contains 1.05), "
            "not the paper's sec-api feed; no filings trimmed to match paper counts. Event=unique accession; "
            "company=primary (first-listed) CIK; Brandywine co-filed accessions attributed once to primary CIK. "
            "Ticker via SEC company_tickers.json common-share preference (PRU/T/HPE/RILY/ZCAR) else filing display-name token. "
            "Market data only via market_data (yfinance); MarketDataUnavailable drops event with counted reasons "
            "(delisted/no-ticker FHLBNY; FYBR/AILE/ENG/ENGC delisted or no Yahoo data). "
            "Choices paper leaves open: use of close (not adj_close); filing trading day=F if trading else next trading day; "
            "return=(close(+5)-close(prev))/close(prev)*100; Welch tests ordered (tech vs nontech; small vs larger; "
            "high beta vs low beta) left-tailed; beta median over events with return+beta, high is beta>median, low is <=median; "
            "size uses current (not historical) market cap; sector uses current Yahoo sector with Technology vs rest. "
            "Deviations: EDGAR search vintage/counts differ from paper's sec-api snapshot (paper: 54/36); "
            "current Yahoo beta/cap/sector vintage differs (e.g., MMATQ beta outlier magnitude, median beta, caps for delisted names); "
            "8-K/A amendments counted as separate events per paper's treatment of repeat filers."
        ),
    }
    with open("/work/results.json", "w") as f:
        json.dump(out_doc, f, indent=1)
    print("Wrote /work/results.json", flush=True)


if __name__ == "__main__":
    main()
