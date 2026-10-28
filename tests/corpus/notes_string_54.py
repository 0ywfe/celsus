"""Replication: Market Reactions to Material Cybersecurity Incidents (Item 1.05 8-K event study).

Pipeline (all data fetched by this script itself):
 1. Query SEC EDGAR full-text search (efts) for Form 8-K filings mentioning
    "Item 1.05" with file_date in [2023-12-01, 2025-11-12]; keep accessions
    whose indexed `items` include "1.05".
 2. Resolve a public-equity ticker per accession: first from SEC
    company_tickers.json (lowest-key entry = primary common-stock class),
    else from the filing's display name, else from the filing cover page's
    Trading Symbol; accessions with no equity ticker are dropped and counted.
 3. For each event, define the filing trading day as the first trading day on
    or after file_date; event-window return = 100*(Close[t+5]-Close[t-1])/Close[t-1].
    Events with no retrievable price data are dropped and counted
    (MarketDataUnavailable only).
 4. Classify by current sector (Technology vs rest), current market cap
    (Small <$2B vs all larger), and beta (median split of available betas).
 5. One-sample left-tailed t-test (mean return < 0) and left-tailed Welch
    two-sample t-tests (Tech vs non-Tech; Small vs larger; high-beta vs low-beta).
"""
import json
import os
import re
import time

import numpy as np
import pandas as pd
import requests
from scipy.stats import t as t_dist

from market_data import get_prices, get_market_cap, get_profile, MarketDataUnavailable

UA = os.environ["SEC_USER_AGENT"]
EFTS = "https://efts.sec.gov/LATEST/search-index"
START_DT = "2023-12-01"
END_DT = "2025-11-12"  # paper's as-of date for the dataset
SMALL_CAP_MAX = 2e9
WIN_BEFORE = 1
WIN_AFTER = 5


def sec_get(url, params=None, host=None, accept="application/json", sleep=0.25):
    time.sleep(sleep)
    headers = {"User-Agent": UA, "Accept": accept}
    if host:
        headers["Host"] = host
    r = requests.get(url, params=params, headers=headers, timeout=40)
    r.raise_for_status()
    return r


def fetch_efts():
    """All efts hits for 8-K mentioning Item 1.05 in the date range."""
    all_hits = []
    total = None
    frm = 0
    while True:
        r = sec_get(EFTS, params={
            "q": '"Item 1.05"', "forms": "8-K", "from": frm, "size": 100,
            "dateRange": "custom", "startdt": START_DT, "enddt": END_DT,
        }, host="efts.sec.gov")
        j = r.json()
        total = j["hits"]["total"]["value"]
        hits = j["hits"]["hits"]
        all_hits.extend(hits)
        frm += len(hits)
        if frm >= total or not hits:
            break
    return all_hits, total


def load_company_tickers():
    r = sec_get("https://www.sec.gov/files/company_tickers.json")
    j = r.json()
    by_cik = {}
    for key in sorted(j, key=int):
        v = j[key]
        by_cik.setdefault(int(v["cik_str"]), []).append(v["ticker"])
    return by_cik


def parse_display_tickers(display_names):
    out = []
    for name in display_names or []:
        m = re.search(r"\(([^()]*)\)\s*\(CIK", name)
        if not m:
            continue
        for tok in m.group(1).split(","):
            tok = tok.strip()
            if re.fullmatch(r"[A-Z][A-Z0-9.\-]*", tok):
                out.append(tok)
    return out


def parse_cover_ticker(cik, adsh):
    """Trading Symbol from the filing's primary document cover page."""
    idx = sec_get(
        f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{adsh.replace('-', '')}/index.json"
    ).json()
    doc = None
    for item in idx.get("directory", {}).get("item", []):
        nm = item.get("name", "")
        if nm.lower().endswith(".htm") and "index" not in nm.lower() and "rfile" not in nm.lower():
            if re.match(r".*-\d{2}-\d{2}-\d{4}\.htm$", nm) or True:
                doc = nm
                break
    if doc is None:
        return None
    html = sec_get(
        f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{adsh.replace('-', '')}/{doc}",
        accept="text/html,*/*", sleep=0.25,
    ).text
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    m = re.search(r"[Tt]rading [Ss]ymbol\(?s?\)?[^A-Z0-9]{0,80}?([A-Z][A-Z0-9.\-]{0,9})", text)
    if m:
        return m.group(1).strip(".-")
    return None


def main():
    print("step 1: EDGAR efts search", flush=True)
    hits, total = fetch_efts()
    print(f"efts raw hits in range: {len(hits)} (reported total {total})", flush=True)
    fil = [h for h in hits if "1.05" in (h["_source"].get("items") or [])]
    print(f"accessions with items containing 1.05: {len(fil)}", flush=True)
    fil.sort(key=lambda h: (h["_source"]["file_date"], h["_source"]["adsh"]))

    print("step 2: ticker resolution", flush=True)
    tickmap = load_company_tickers()
    print(f"company_tickers entries loaded", flush=True)
    events = []  # (file_date, cik_primary, ticker, adsh, form)
    dropped_no_ticker = 0
    for h in fil:
        s = h["_source"]
        ciks = [c.lstrip("0") or "0" for c in s.get("ciks", [])]
        cik = ciks[0] if ciks else None
        ticker = None
        cands = tickmap.get(int(cik), []) if cik and cik.isdigit() else []
        if cands:
            ticker = cands[0]
        if ticker is None:
            disp = parse_display_tickers(s.get("display_names"))
            if disp:
                ticker = disp[0]
        if ticker is None and cik and cik.isdigit():
            try:
                ticker = parse_cover_ticker(cik, s["adsh"])
            except Exception:
                ticker = None
        if ticker is None:
            dropped_no_ticker += 1
            print(f"  drop (no equity ticker): {s['file_date']} {s.get('display_names')}", flush=True)
            continue
        events.append((s["file_date"], cik, ticker.upper(), s["adsh"], s.get("form")))
    print(f"events with ticker: {len(events)}; dropped no-ticker: {dropped_no_ticker}", flush=True)

    # distinct tickers -> one bulk price fetch each
    uniq = sorted({e[2] for e in events})
    print(f"step 3: bulk price fetch for {len(uniq)} tickers", flush=True)
    bars = {}
    for t in uniq:
        try:
            bars[t] = get_prices(t, "2023-12-01", "2025-11-20")
        except MarketDataUnavailable:
            bars[t] = None
        except Exception:
            raise
    print("price fetch done", flush=True)

    print("step 4: event-window returns", flush=True)
    rows = []
    dropped_no_price = 0
    for file_date, cik, ticker, adsh, form in events:
        f = bars.get(ticker)
        if f is None or f.empty:
            dropped_no_price += 1
            print(f"  drop (no price data): {file_date} {ticker} {adsh}", flush=True)
            continue
        days = list(f.index)
        fdt = pd.Timestamp(file_date)
        pos = int(np.searchsorted([d.value for d in days], fdt.value))
        if pos >= len(days) or (pos - WIN_BEFORE) < 0 or (pos + WIN_AFTER) >= len(days):
            dropped_no_price += 1
            print(f"  drop (window edge): {file_date} {ticker} {adsh}", flush=True)
            continue
        c0 = float(f.iloc[pos - WIN_BEFORE]["close"])
        c1 = float(f.iloc[pos + WIN_AFTER]["close"])
        if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
            dropped_no_price += 1
            print(f"  drop (bad closes): {file_date} {ticker} {adsh}", flush=True)
            continue
        ret = 100.0 * (c1 - c0) / c0
        rows.append({"file_date": file_date, "cik": cik, "ticker": ticker,
                     "adsh": adsh, "ret": ret})
    print(f"priced events: {len(rows)}; dropped no-price: {dropped_no_price}", flush=True)
    df = pd.DataFrame(rows)

    print("step 5: profiles / market caps", flush=True)
    sectors, betas, mcaps = {}, {}, {}
    for t in sorted(df["ticker"].unique()):
        try:
            p = get_profile(t)
        except MarketDataUnavailable:
            p = {"sector": None, "beta": None}
        sec = p.get("sector")
        sectors[t] = sec if sec else None
        try:
            betas[t] = float(p.get("beta")) if p.get("beta") is not None else None
        except (TypeError, ValueError):
            betas[t] = None
        try:
            mc = get_market_cap(t)
            mcaps[t] = float(mc) if mc and np.isfinite(float(mc)) and float(mc) > 0 else None
        except MarketDataUnavailable:
            mcaps[t] = None
    df["sector"] = df["ticker"].map(sectors)
    df["beta"] = df["ticker"].map(betas)
    df["mcap"] = df["ticker"].map(mcaps)
    df["is_tech"] = df["sector"] == "Technology"
    df["is_small"] = df["mcap"] < SMALL_CAP_MAX
    print(f"events with sector: {int(df['sector'].notna().sum())}, "
          f"with mcap: {int(df['mcap'].notna().sum())}, "
          f"with beta: {int(df['beta'].notna().sum())}", flush=True)

    beta_med = float(df["beta"].median())
    df["is_high_beta"] = df["beta"] >= beta_med
    print(f"beta median: {beta_med}", flush=True)

    # ---- tests ----
    rets = df["ret"].to_numpy(float)
    n = len(rets)
    mean = float(rets.mean())
    sd = float(rets.std(ddof=1))
    t1 = mean / (sd / np.sqrt(n))
    p1 = float(t_dist.cdf(t1, n - 1))

    def welch(a, b):
        a = np.asarray(a, float)
        b = np.asarray(b, float)
        m1, m2 = float(a.mean()), float(b.mean())
        s1, s2 = float(a.var(ddof=1)), float(b.var(ddof=1))
        n1, n2 = len(a), len(b)
        se = np.sqrt(s1 / n1 + s2 / n2)
        t = (m1 - m2) / se
        dfw = (s1 / n1 + s2 / n2) ** 2 / ((s1 / n1) ** 2 / (n1 - 1) + (s2 / n2) ** 2 / (n2 - 1))
        p = float(t_dist.cdf(t, dfw))
        return m1, m2, n1, n2, t, p

    tech = df[df["is_tech"]]["ret"]
    nontech = df[df["sector"].notna() & ~df["is_tech"]]["ret"]
    tm1, tm2, tn1, tn2, tt, tp = welch(tech, nontech)

    small = df[df["mcap"].notna() & df["is_small"]]["ret"]
    larger = df[df["mcap"].notna() & ~df["is_small"]]["ret"]
    sm1, sm2, sn1, sn2, st, sp = welch(small, larger)

    hib = df[df["beta"].notna() & df["is_high_beta"]]["ret"]
    lob = df[df["beta"].notna() & ~df["is_high_beta"]]["ret"]
    bm_lo, bm_hi = float(lob.mean()), float(hib.mean())
    _, _, bn_hi, bn_lo, bt, bp = welch(hib, lob)

    # company distribution (filings per primary CIK in priced sample)
    per_co = df.groupby("cik").size()
    n1c = int((per_co == 1).sum())
    n2c = int((per_co == 2).sum())
    n3c = int((per_co == 3).sum())
    print(f"companies: {df['cik'].nunique()} (1x{n1c} 2x{n2c} 3x{n3c})", flush=True)
    print(f"overall: n={n} mean={mean:.4f} sd={sd:.4f} t={t1:.4f} p={p1:.6f}", flush=True)
    print(f"sector: tech n={tn1} mean={tm1:.4f}; nontech n={tn2} mean={tm2:.4f}; t={tt:.4f} p={tp:.6f}", flush=True)
    print(f"size: small n={sn1} mean={sm1:.4f}; larger n={sn2} mean={sm2:.4f}; t={st:.4f} p={sp:.6f}", flush=True)
    print(f"beta: low n={bn_lo} mean={bm_lo:.4f}; high n={bn_hi} mean={bm_hi:.4f}; t={bt:.4f} p={bp:.6f}", flush=True)
    print(f"beta outlier (max): {float(df['beta'].max()):.3f}", flush=True)

    results = [
        {"name": "total_filings", "value": int(len(df)), "se": None, "n": int(len(df))},
        {"name": "total_companies", "value": int(df["cik"].nunique()), "se": None,
         "n": int(df["cik"].nunique())},
        {"name": "companies_one_report", "value": n1c, "se": None, "n": int(df["cik"].nunique())},
        {"name": "companies_two_reports", "value": n2c, "se": None, "n": int(df["cik"].nunique())},
        {"name": "companies_three_reports", "value": n3c, "se": None, "n": int(df["cik"].nunique())},
        {"name": "n_small", "value": int(sn1), "se": None, "n": int(sn1)},
        {"name": "n_larger", "value": int(sn2), "se": None, "n": int(sn2)},
        {"name": "n_tech", "value": int(tn1), "se": None, "n": int(tn1)},
        {"name": "n_nontech", "value": int(tn2), "se": None, "n": int(tn2)},
        {"name": "overall_mean_return", "value": mean, "se": sd / np.sqrt(n), "n": n},
        {"name": "overall_sd", "value": sd, "se": sd / np.sqrt(2 * (n - 1)), "n": n},
        {"name": "overall_t", "value": float(t1), "se": None, "n": n},
        {"name": "overall_p", "value": p1, "se": None, "n": n},
        {"name": "sector_tech_mean", "value": tm1, "se": float(tech.std(ddof=1) / np.sqrt(tn1)), "n": tn1},
        {"name": "sector_nontech_mean", "value": tm2, "se": float(nontech.std(ddof=1) / np.sqrt(tn2)), "n": tn2},
        {"name": "sector_t", "value": float(tt), "se": None, "n": tn1 + tn2},
        {"name": "sector_p", "value": tp, "se": None, "n": tn1 + tn2},
        {"name": "size_small_mean", "value": sm1, "se": float(small.std(ddof=1) / np.sqrt(sn1)), "n": sn1},
        {"name": "size_larger_mean", "value": sm2, "se": float(larger.std(ddof=1) / np.sqrt(sn2)), "n": sn2},
        {"name": "size_t", "value": float(st), "se": None, "n": sn1 + sn2},
        {"name": "size_p", "value": sp, "se": None, "n": sn1 + sn2},
        {"name": "beta_low_mean", "value": bm_lo, "se": float(lob.std(ddof=1) / np.sqrt(bn_lo)), "n": bn_lo},
        {"name": "beta_high_mean", "value": bm_hi, "se": float(hib.std(ddof=1) / np.sqrt(bn_hi)), "n": bn_hi},
        {"name": "beta_t", "value": float(bt), "se": None, "n": bn_lo + bn_hi},
        {"name": "beta_p", "value": bp, "se": None, "n": bn_lo + bn_hi},
        {"name": "beta_median", "value": beta_med, "se": None, "n": int(df["beta"].notna().sum())},
        {"name": "beta_outlier", "value": float(df["beta"].max()), "se": None,
         "n": int(df["beta"].notna().sum())},
    ]
    out = {
        "results": results,
        "sample": {
            "description": (
                "Form 8-K/8-K/A accessions with Item 1.05 filed 2023-12-01 to 2025-11-12, "
                "with a resolvable public-equity ticker and retrievable price data for the "
                "t-1 to t+5 trading-day event window (filing trading day = first trading day "
                "on/after file_date; amendments on distinct dates kept as separate events)"
            ),
            "n": int(len(df)),
        },
        "notes": (
            "Choices left open by the paper: EDGAR full-text ('Item 1.05') + items-field filter "
            "to enumerate filings; ticker = primary common-stock class from SEC company_tickers "
            "(lowest-key entry), else display-name symbol, else filing-cover Trading Symbol; "
            "event return uses unadjusted close; non-trading filing dates rolled forward to the "
            "next trading day; beta split is low = beta < sample median, high = beta >= median; "
            "Welch df via Satterthwaite. Deviations: universe yields 58 items-1.05 accessions; "
            "1 dropped (Federal Home Loan Bank of New York, no equity ticker); 4 events dropped "
            "for missing price data (EnGlobal x2, iLearningEngines, Frontier) so priced n=53 vs "
            "paper's 54 (one of those had data as of Nov 2025); sector/mcap/beta are current "
            "values, not Nov-2025 vintages, so subgroup counts and the beta median/outlier can "
            "differ slightly from the paper."
        ),
    }
    with open("/work/results.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote /work/results.json", flush=True)


if __name__ == "__main__":
    main()
