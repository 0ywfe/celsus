import os
import time
import json
import requests
import pandas as pd
import numpy as np
from scipy import stats
from market_data import get_prices, get_market_cap, MarketDataUnavailable

SEC_AGENT = os.environ.get("SEC_USER_AGENT", "replication contact@example.com")
SEC_HDR = {"User-Agent": SEC_AGENT, "Accept-Encoding": "gzip", "Accept": "application/json"}
HDR_HTML = {"User-Agent": SEC_AGENT, "Accept-Encoding": "gzip"}
CUTOFF = "2025-11-12"
STARTDT = "2023-07-01"

def sec_get(url, params=None, headers=None, sleep=0.25):
    r = requests.get(url, params=params, headers=headers or SEC_HDR, timeout=30)
    time.sleep(sleep)
    r.raise_for_status()
    return r

def build_cik_map():
    print("fetching company_tickers.json")
    r = sec_get("https://www.sec.gov/files/company_tickers.json", headers=HDR_HTML)
    data = r.json()
    mp = {}
    name_mp = {}
    if isinstance(data, dict):
        for _, v in data.items():
            try:
                cik = int(v.get("cik_str"))
                mp[cik] = v.get("ticker")
                name_mp[cik] = v.get("title")
            except Exception:
                continue
    else:
        for v in data:
            try:
                cik = int(v.get("cik_str"))
                mp[cik] = v.get("ticker")
                name_mp[cik] = v.get("title")
            except Exception:
                continue
    print(f"cik map size: {len(mp)}")
    return mp, name_mp

def efts_search():
    base = "https://efts.sec.gov/LATEST/search-index"
    size = 100
    start = 0
    all_hits = []
    total_val = None
    while True:
        params = {"q": '"Item 1.05"', "forms": "8-K", "dateRange": "custom", "startdt": STARTDT, "enddt": CUTOFF, "from": start, "size": size}
        r = sec_get(base, params=params)
        j = r.json()
        hits = j.get("hits", {})
        tot = hits.get("total", {})
        if isinstance(tot, dict):
            total_val = tot.get("value")
        else:
            total_val = tot
        batch = hits.get("hits", [])
        print(f"efts from={start} batch={len(batch)} total={total_val}")
        if not batch:
            break
        all_hits.extend(batch)
        start += len(batch)
        if len(batch) < size:
            break
        if start > 2000:
            break
    print(f"efts raw hits collected: {len(all_hits)}")
    return all_hits

def parse_hits(hits, cik_map):
    events = []
    seen_acc = set()
    n_raw = len(hits)
    n_wrong_form = 0
    n_item_filter = 0
    n_dup = 0
    n_future = 0
    for h in hits:
        src = h.get("_source", {}) if isinstance(h, dict) else {}
        if not src:
            continue
        form = str(src.get("form", "")).strip()
        if form not in ("8-K",):
            n_wrong_form += 1
            continue
        items = src.get("items", src.get("item", None))
        if items is not None:
            if isinstance(items, str):
                items_l = [items]
            else:
                try:
                    items_l = list(items)
                except Exception:
                    items_l = []
            has = any(str(x).strip() == "1.05" for x in items_l)
            if not has:
                n_item_filter += 1
                continue
        acc = src.get("accession_number", src.get("accessionNumber", src.get("accn", src.get("accession_no", ""))))
        acc = str(acc).strip()
        if not acc:
            acc = str(h.get("_id", "")).strip()
        if acc in seen_acc:
            n_dup += 1
            continue
        ciks = src.get("ciks", src.get("cik", src.get("ciks_", [])))
        cik = None
        if isinstance(ciks, list) and len(ciks) > 0:
            try:
                cik = int(str(ciks[0]).strip())
            except Exception:
                cik = None
        elif isinstance(ciks, (int, str)) and str(ciks).strip() not in ("", "None"):
            try:
                cik = int(str(ciks).strip())
            except Exception:
                cik = None
        filed = src.get("filed", src.get("filing_date", src.get("file_date", src.get("filingDate", src.get("period", "")))))
        filed = str(filed).strip()[:10]
        if not filed or filed < "2020-01-01":
            continue
        if filed > CUTOFF:
            n_future += 1
            continue
        tickers = src.get("tickers", src.get("ticker", src.get("tickers_", None)))
        ticker = None
        if isinstance(tickers, list) and len(tickers) > 0:
            ticker = str(tickers[0]).strip().upper()
        elif isinstance(tickers, str) and tickers.strip():
            ticker = tickers.strip().upper().split(",")[0]
        if (not ticker or ticker in ("", "NONE", "-", "NULL")) and cik is not None:
            ticker = cik_map.get(cik)
            if ticker:
                ticker = str(ticker).strip().upper()
        if not ticker:
            continue
        if "-" in ticker:
            ticker = ticker.split("-")[0]
        seen_acc.add(acc)
        events.append({"cik": cik, "ticker": ticker, "filing_date": filed, "accession": acc})
    print(f"parse: raw={n_raw} wrong_form_dropped={n_wrong_form} item_filtered={n_item_filter} dup={n_dup} future={n_future} kept={len(events)}")
    events = sorted(events, key=lambda x: (x["filing_date"], x["ticker"]))
    return events

def resolve_missing_tickers(events, cik_map):
    fixed = 0
    dropped = 0
    for e in events:
        t = e.get("ticker", "")
        if not t:
            dropped += 1
    print(f"events with ticker: {len(events)} dropped_empty={dropped}")
    return events

def compute_return(ticker, filing_date):
    fd = pd.Timestamp(filing_date)
    start_cal = (fd - pd.Timedelta(days=20)).strftime("%Y-%m-%d")
    end_cal = (fd + pd.Timedelta(days=30)).strftime("%Y-%m-%d")
    df = get_prices(ticker, start_cal, end_cal)
    if df is None or len(df) == 0:
        raise MarketDataUnavailable(ticker)
    df = df.sort_index()
    df.index = pd.to_datetime(df.index).tz_localize(None) if df.index.tz is not None else pd.to_datetime(df.index)
    dates = df.index.normalize()
    fd_n = pd.Timestamp(filing_date).normalize()
    pos = None
    for i, d in enumerate(dates):
        if d >= fd_n:
            pos = i
            break
    if pos is None:
        raise MarketDataUnavailable(ticker)
    if pos == 0:
        start_cal2 = (fd - pd.Timedelta(days=60)).strftime("%Y-%m-%d")
        df = get_prices(ticker, start_cal2, end_cal)
        df = df.sort_index()
        df.index = pd.to_datetime(df.index).tz_localize(None) if df.index.tz is not None else pd.to_datetime(df.index)
        dates = df.index.normalize()
        for i, d in enumerate(dates):
            if d >= fd_n:
                pos = i
                break
    if pos is None or pos < 1 or pos + 5 >= len(df):
        try:
            end_cal2 = (fd + pd.Timedelta(days=60)).strftime("%Y-%m-%d")
            start_cal2 = (fd - pd.Timedelta(days=60)).strftime("%Y-%m-%d")
            df = get_prices(ticker, start_cal2, end_cal2)
            df = df.sort_index()
            df.index = pd.to_datetime(df.index).tz_localize(None) if df.index.tz is not None else pd.to_datetime(df.index)
            dates = df.index.normalize()
            pos = None
            for i, d in enumerate(dates):
                if d >= fd_n:
                    pos = i
                    break
        except Exception:
            pass
        if pos is None or pos < 1 or pos + 5 >= len(df):
            raise MarketDataUnavailable(ticker)
    col = "adj_close" if "adj_close" in df.columns else "close"
    p0 = float(df.iloc[pos - 1][col])
    p1 = float(df.iloc[pos + 5][col])
    if not np.isfinite(p0) or not np.isfinite(p1) or p0 <= 0:
        raise MarketDataUnavailable(ticker)
    ret = (p1 - p0) / p0 * 100.0
    return ret

_info_cache = {}
def get_yf_info(ticker):
    if ticker in _info_cache:
        return _info_cache[ticker]
    info = {}
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        try:
            inf = t.info
            if isinstance(inf, dict):
                info = inf
        except Exception:
            try:
                info = t.get_info() or {}
            except Exception:
                info = {}
        time.sleep(0.1)
    except Exception as e:
        print(f"yfinance info fail {ticker}: {e}")
        info = {}
    _info_cache[ticker] = info
    return info

def main():
    cik_map, _ = build_cik_map()
    hits = efts_search()
    events = parse_hits(hits, cik_map)
    events = resolve_missing_tickers(events, cik_map)
    print(f"candidate events: {len(events)}")
    rets = []
    kept = []
    n_price_drop = 0
    for e in events:
        try:
            r = compute_return(e["ticker"], e["filing_date"])
        except MarketDataUnavailable:
            n_price_drop += 1
            continue
        except Exception as ex:
            print(f"price error {e}: {ex}")
            raise
        e2 = dict(e)
        e2["ret"] = float(r)
        kept.append(e2)
        rets.append(float(r))
    print(f"events with valid return: {len(kept)} price_drops={n_price_drop}")
    rets = np.array(rets, dtype=float)
    from collections import Counter
    cnt = Counter([k["ticker"] for k in kept])
    n_unique = len(cnt)
    freq = Counter(cnt.values())
    print(f"unique companies: {n_unique} dist: {dict(freq)}")
    n_all = len(rets)
    mean_all = float(np.mean(rets)) if n_all else float("nan")
    sd_all = float(np.std(rets, ddof=1)) if n_all > 1 else float("nan")
    t_all, p_all = (float("nan"), float("nan"))
    if n_all > 1:
        tres = stats.ttest_1samp(rets, 0.0, alternative="less")
        t_all = float(tres.statistic); p_all = float(tres.pvalue)
    se_all = float(sd_all / np.sqrt(n_all)) if n_all else float("nan")
    print(f"overall n={n_all} mean={mean_all} sd={sd_all} t={t_all} p={p_all}")
    for e in kept:
        try:
            mc = get_market_cap(e["ticker"])
            e["mcap"] = float(mc) if mc is not None and np.isfinite(float(mc)) and float(mc) > 0 else None
        except MarketDataUnavailable:
            e["mcap"] = None
        info = get_yf_info(e["ticker"])
        sec = info.get("sector", None) if isinstance(info, dict) else None
        try:
            sec = str(sec).strip() if sec else None
        except Exception:
            sec = None
        e["sector"] = sec
        b = info.get("beta", None) if isinstance(info, dict) else None
        try:
            bf = float(b) if b is not None else None
            if bf is not None and not np.isfinite(bf):
                bf = None
        except Exception:
            bf = None
        e["beta"] = bf
    small_r = [e["ret"] for e in kept if e.get("mcap") is not None and e["mcap"] < 2000000000]
    large_r = [e["ret"] for e in kept if e.get("mcap") is not None and e["mcap"] >= 2000000000]
    n_mcap_missing = sum(1 for e in kept if e.get("mcap") is None)
    print(f"size small={len(small_r)} large={len(large_r)} mcap_missing={n_mcap_missing}")
    tech_r = [e["ret"] for e in kept if e.get("sector") == "Technology"]
    nontech_r = [e["ret"] for e in kept if e.get("sector") is not None and e.get("sector") != "Technology"]
    n_sec_missing = sum(1 for e in kept if not e.get("sector"))
    print(f"sector tech={len(tech_r)} nontech={len(nontech_r)} missing={n_sec_missing}")
    betas = np.array([e["beta"] for e in kept if e.get("beta") is not None], dtype=float)
    med_beta = float(np.median(betas)) if len(betas) else float("nan")
    max_beta = float(np.max(betas)) if len(betas) else float("nan")
    print(f"beta n={len(betas)} median={med_beta} max={max_beta}")
    low_r = [e["ret"] for e in kept if e.get("beta") is not None and e["beta"] <= med_beta]
    high_r = [e["ret"] for e in kept if e.get("beta") is not None and e["beta"] > med_beta]
    n_beta_missing = sum(1 for e in kept if e.get("beta") is None)
    print(f"beta low={len(low_r)} high={len(high_r)} missing={n_beta_missing}")
    def grp_stats(a):
        a = np.array(a, dtype=float)
        n = len(a)
        if n == 0:
            return float("nan"), float("nan"), n
        m = float(np.mean(a))
        s = float(np.std(a, ddof=1)) if n > 1 else float("nan")
        se = float(s / np.sqrt(n)) if n > 1 else float("nan")
        return m, se, n
    def welch_less(a, b):
        a = np.array(a, dtype=float); b = np.array(b, dtype=float)
        if len(a) < 2 or len(b) < 2:
            return float("nan"), float("nan")
        r = stats.ttest_ind(a, b, equal_var=False, alternative="less")
        return float(r.statistic), float(r.pvalue)
    m_tech, se_tech, n_tech = grp_stats(tech_r)
    m_nontech, se_nontech, n_nontech = grp_stats(nontech_r)
    t_sec, p_sec = welch_less(tech_r, nontech_r)
    m_small, se_small, n_small = grp_stats(small_r)
    m_large, se_large, n_large = grp_stats(large_r)
    t_size, p_size = welch_less(small_r, large_r)
    m_low, se_low, n_low = grp_stats(low_r)
    m_high, se_high, n_high = grp_stats(high_r)
    t_beta, p_beta = welch_less(high_r, low_r)
    print(f"tech mean={m_tech} nontech={m_nontech} t={t_sec} p={p_sec}")
    print(f"small mean={m_small} large={m_large} t={t_size} p={p_size}")
    print(f"low mean={m_low} high={m_high} t={t_beta} p={p_beta}")
    c1 = sum(1 for _, v in cnt.items() if v == 1)
    c2 = sum(1 for _, v in cnt.items() if v == 2)
    c3 = sum(1 for _, v in cnt.items() if v == 3)
    R = []
    def add(name, value, se, n):
        def conv(x):
            if x is None:
                return None
            try:
                f = float(x)
                if not np.isfinite(f):
                    return None
                return float(f)
            except Exception:
                return None
        v = value
        if isinstance(value, (bool,)):
            v = int(value)
        elif isinstance(value, int):
            v = value
        else:
            vv = conv(value)
            v = vv if vv is not None else value
        s = conv(se) if se is not None else None
        nn = int(n) if n is not None and str(n) != "nan" else None
        R.append({"name": name, "value": v, "se": s, "n": nn})
    add("total_item105_reports", int(len(kept)), None, int(len(kept)))
    add("unique_companies", int(n_unique), None, int(n_unique))
    add("companies_single_report", int(c1), None, int(n_unique))
    add("companies_two_reports", int(c2), None, int(n_unique))
    add("companies_three_reports", int(c3), None, int(n_unique))
    add("overall_mean_return", mean_all, se_all, n_all)
    add("overall_sd_return", sd_all, None, n_all)
    add("overall_t_stat", t_all, None, n_all)
    add("overall_p_value", p_all, None, n_all)
    add("sector_tech_mean_return", m_tech, se_tech, n_tech)
    add("sector_nontechnology_mean_return", m_nontech, se_nontech, n_nontech)
    add("sector_t_stat", t_sec, None, n_tech + n_nontech)
    add("sector_p_value", p_sec, None, n_tech + n_nontech)
    add("sector_n_technology", int(n_tech), None, int(n_tech))
    add("sector_n_nontechnology", int(n_nontech), None, int(n_nontech))
    add("size_small_mean_return", m_small, se_small, n_small)
    add("size_large_mean_return", m_large, se_large, n_large)
    add("size_t_stat", t_size, None, n_small + n_large)
    add("size_p_value", p_size, None, n_small + n_large)
    add("size_n_small", int(n_small), None, int(n_small))
    add("size_n_large", int(n_large), None, int(n_large))
    add("beta_median", med_beta, None, int(len(betas)))
    add("beta_outlier", max_beta, None, int(len(betas)))
    add("beta_low_mean_return", m_low, se_low, n_low)
    add("beta_high_mean_return", m_high, se_high, n_high)
    add("beta_t_stat", t_beta, None, n_low + n_high)
    add("beta_p_value", p_beta, None, n_low + n_high)
    sample_desc = f"Item 1.05 8-K filings through {CUTOFF} with valid t-1 to t+5 return; {len(kept)} events, {n_unique} tickers; price drops {n_price_drop}; mcap missing {n_mcap_missing}; sector missing {n_sec_missing}; beta missing {n_beta_missing}"
    notes = ("EDGAR efts full-text search for Item 1.05 8-K through cutoff, filtered to form 8-K and items containing 1.05, deduped by accession, ticker via EDGAR tickers field then company_tickers.json. "
        "Filing date t defined as first trading day >= filing date; return = (adj_close[t+5]-adj_close[t-1])/adj_close[t-1]*100 using market_data.get_prices (adj_close fallback close); events lacking t-1 or t+5 dropped via MarketDataUnavailable and counted. "
        "Market cap is current via market_data.get_market_cap, split Small <$2B vs >=$2B (Mid+Large+Mega combined). "
        "Sector/beta via yfinance Ticker.info cached per ticker; Technology = sector exactly Technology; beta median split event-level (low <= median, high > median). "
        "Overall one-sample left-tailed t-test mu=0; subgroups Welch two-sample left-tailed (tech vs nontech, small vs large, high vs low). "
        "Counts/distribution computed on valid-return sample. Deviations: intraday filing time ignored (date only); adj_close used instead of raw close; current mcap/beta/sector rather than historical at filing; EDGAR items-field filter may differ from paper sec-api extractor.")
    out = {"results": R, "sample": {"description": sample_desc, "n": int(len(kept))}, "notes": notes}
    with open("/work/results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("wrote /work/results.json")

if __name__ == "__main__":
    main()
