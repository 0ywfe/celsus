import os
import time
import json
import re
import requests
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from scipy import stats
from market_data import get_prices, get_market_cap, get_profile, MarketDataUnavailable

SEC_UA = os.environ.get("SEC_USER_AGENT", "replication-script contact")
LAST_SEC_CALL = [0.0]

def sec_headers():
    return {"User-Agent": SEC_UA, "Accept": "application/json", "Accept-Encoding": "gzip, deflate"}

def sec_get_json(url, params=None, retries=3):
    for attempt in range(retries):
        elapsed = time.time() - LAST_SEC_CALL[0]
        if elapsed < 0.15:
            time.sleep(0.15 - elapsed)
        r = requests.get(url, headers=sec_headers(), params=params, timeout=30)
        LAST_SEC_CALL[0] = time.time()
        if r.status_code == 429 and attempt < retries - 1:
            time.sleep(1.5 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("SEC request failed")

def load_cik_to_ticker():
    url = "https://www.sec.gov/files/company_tickers.json"
    try:
        data = sec_get_json(url)
    except Exception as e:
        print(f"company_tickers fetch failed: {e}")
        return {}
    mapping = {}
    if isinstance(data, dict):
        for v in data.values():
            try:
                cik = str(int(v["cik_str"])).zfill(10)
                cik_nopad = str(int(v["cik_str"]))
                ticker = v["ticker"]
                mapping[cik] = ticker
                mapping[cik_nopad] = ticker
                mapping[str(v["cik_str"])] = ticker
            except Exception:
                continue
    print(f"CIK->ticker map size: {len(mapping)//3 if mapping else 0} companies")
    return mapping

def search_item105():
    base = "https://efts.sec.gov/LATEST/search-index"
    enddt = "2025-11-12"
    startdt = "2023-12-01"
    q = '"Item 1.05"'
    all_hits = []
    frm = 0
    size = 100
    while True:
        params = {"q": q, "forms": "8-K", "dateRange": "custom", "startdt": startdt, "enddt": enddt, "from": frm, "size": size}
        print(f"SEC FTS query q={q} from={frm}")
        data = sec_get_json(base, params=params)
        hits_obj = data.get("hits", {})
        tot = hits_obj.get("total", 0)
        if isinstance(tot, dict):
            tot = tot.get("value", 0)
        print(f"  total={tot}")
        hits = hits_obj.get("hits", [])
        if not hits:
            break
        all_hits.extend(hits)
        print(f"  fetched {len(hits)} (cumulative {len(all_hits)})")
        if len(hits) < size:
            break
        frm += size
        if frm >= 1000:
            break
    print(f"Raw FTS hits collected: {len(all_hits)}")
    if all_hits:
        try:
            h0 = all_hits[0]
            print("First hit top keys: " + str(list(h0.keys())[:20]))
            src0 = h0.get("_source", {}) if isinstance(h0.get("_source"), dict) else {}
            print("First _source keys: " + str(list(src0.keys())[:40]))
            print("First hit JSON (trunc): " + json.dumps(h0, default=str)[:3000])
        except Exception as e:
            print(f"debug print failed: {e}")
    return all_hits

def _get_case_insensitive(container, substrings):
    if not isinstance(container, dict):
        return None, None
    for k, v in container.items():
        lk = str(k).lower()
        for s in substrings:
            if s in lk:
                return k, v
    return None, None

def extract_date_str(val):
    if val is None:
        return None
    if isinstance(val, list):
        for v in val:
            s = extract_date_str(v)
            if s:
                return s
        return None
    if isinstance(val, dict):
        for v in val.values():
            s = extract_date_str(v)
            if s:
                return s
        return None
    if isinstance(val, (int, float)) and np.isfinite(val):
        # epoch millis or seconds?
        try:
            if val > 1e12:
                return datetime.utcfromtimestamp(val/1000.0).date().isoformat()
            elif val > 1e9:
                return datetime.utcfromtimestamp(val).date().isoformat()
        except Exception:
            pass
    s = str(val).strip()
    if not s or s.lower() in ("none", "null", "-"):
        return None
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    m2 = re.search(r"(\d{2})/(\d{2})/(\d{4})", s)
    if m2:
        try:
            return f"{m2.group(3)}-{m2.group(1)}-{m2.group(2)}"
        except Exception:
            pass
    return None

def extract_first_string(val):
    if val is None:
        return None
    if isinstance(val, list):
        for v in val:
            s = extract_first_string(v)
            if s and s.strip() not in ("", "None", "-", "null"):
                return str(s).strip()
        return None
    if isinstance(val, dict):
        return None
    s = str(val).strip()
    if s in ("", "None", "-", "null"):
        return None
    return s

def parse_hits(hits, cik_to_ticker):
    events = []
    n_no_date = 0
    for idx, h in enumerate(hits):
        src = h.get("_source", {}) if isinstance(h.get("_source"), dict) else {}
        fields = h.get("fields", {}) if isinstance(h.get("fields"), dict) else {}
        # merge candidates: search src, then fields, then whole hit
        filed_raw = None
        for container in (src, fields, h):
            if not isinstance(container, dict):
                continue
            # try known keys first (case-insensitive exact)
            lowered = {str(k).lower(): v for k, v in container.items()}
            for kk in ["filedat", "filed", "filedate", "filingdate", "fdate", "filed_at", "filedat", "filing_date", "file_date", "acceptance-datetime", "acceptancedatetime", "period"]:
                if kk in lowered:
                    filed_raw = lowered[kk]
                    break
            if filed_raw is not None:
                break
            # fallback: any key containing file/fdate/filing
            for k, v in container.items():
                lk = str(k).lower()
                if ("file" in lk or "fdate" in lk or "filing" in lk) and "filed" not in str(type(v)):
                    # avoid form-type keys like filetype? require value looks date-ish
                    ds = extract_date_str(v)
                    if ds:
                        filed_raw = v
                        break
            if filed_raw is not None:
                break
        filed_str = extract_date_str(filed_raw)
        # last resort: regex over whole hit json
        if filed_str is None:
            try:
                filed_str = extract_date_str(json.dumps(h, default=str))
                # whole-hit regex may pick a period date; still better than dropping; log it
                if filed_str:
                    print(f"hit {idx}: filed via whole-hit regex fallback: {filed_str}")
            except Exception:
                filed_str = None
        if filed_str is None:
            n_no_date += 1
            print(f"DROP hit {idx}: no filed date. keys={list(src.keys())[:20]} raw_vals={str({k: str(v)[:60] for k,v in src.items()})[:500]}")
            continue
        try:
            filed_d = date.fromisoformat(filed_str)
        except Exception:
            n_no_date += 1
            print(f"DROP hit {idx}: bad date {filed_str}")
            continue
        if filed_d > date.fromisoformat("2025-11-12"):
            n_no_date += 1
            print(f"DROP hit {idx}: filed after cutoff {filed_str}")
            continue
        # forms
        forms_raw = None
        for container in (src, fields, h):
            if not isinstance(container, dict):
                continue
            lowered = {str(k).lower(): v for k, v in container.items()}
            if "form" in lowered:
                forms_raw = lowered["form"]
                break
            if "forms" in lowered:
                forms_raw = lowered["forms"]
                break
        forms_list = []
        if isinstance(forms_raw, list):
            forms_list = [str(f).upper().strip() for f in forms_raw]
        elif forms_raw is not None:
            forms_list = [str(forms_raw).upper().strip()]
        else:
            forms_list = ["8-K"]  # query already restricted to 8-K
        if "8-K/A" in forms_list and "8-K" not in forms_list:
            print(f"DROP hit {idx}: amendment only {forms_list}")
            continue
        # accession
        acc_raw = None
        for container in (src, fields, h):
            if not isinstance(container, dict):
                continue
            lowered = {str(k).lower(): v for k, v in container.items()}
            for kk in ["adsh", "accessionnumber", "accession_number", "accessionno", "accession"]:
                if kk in lowered:
                    acc_raw = lowered[kk]
                    break
            if acc_raw is not None:
                break
            k2, v2 = _get_case_insensitive(container, ["adsh", "accession"])
            if v2 is not None:
                acc_raw = v2
                break
        acc_s = extract_first_string(acc_raw)
        if acc_s is None:
            acc_s = extract_first_string(h.get("_id"))
        if acc_s is None:
            acc_s = f"noid-{idx}"
        acc_norm = str(acc_s).replace("-", "").split(":")[0].strip()
        # cik
        cik_raw = None
        for container in (src, fields, h):
            if not isinstance(container, dict):
                continue
            lowered = {str(k).lower(): v for k, v in container.items()}
            for kk in ["ciks", "cik", "cikno", "cik_no", "cikstr"]:
                if kk in lowered:
                    cik_raw = lowered[kk]
                    break
            if cik_raw is not None:
                break
        cik_s = extract_first_string(cik_raw)
        cik = None
        if cik_s is not None:
            # keep digits only
            digs = re.sub(r"\D", "", str(cik_s))
            if digs:
                try:
                    cik = str(int(digs))
                except Exception:
                    cik = digs.lstrip("0") or digs
        cik_padded = cik.zfill(10) if cik else None
        # ticker
        tick_raw = None
        for container in (src, fields, h):
            if not isinstance(container, dict):
                continue
            lowered = {str(k).lower(): v for k, v in container.items()}
            for kk in ["tickers", "ticker", "tickerstraded", "tickers_traded", "symbol"]:
                if kk in lowered:
                    tick_raw = lowered[kk]
                    break
            if tick_raw is not None:
                break
        ticker = extract_first_string(tick_raw)
        if ticker is not None:
            ticker = str(ticker).strip().upper()
            if ticker in ("", "-", "NONE", "NULL"):
                ticker = None
        if ticker is None and cik:
            for key in (cik_padded, cik):
                if key and key in cik_to_ticker:
                    ticker = str(cik_to_ticker[key]).strip().upper()
                    break
        # company name
        cname = ""
        for container in (src, fields):
            if not isinstance(container, dict):
                continue
            lowered = {str(k).lower(): v for k, v in container.items()}
            for kk in ["companyname", "company", "displayname", "entityname", "entity_name", "title", "name"]:
                if kk in lowered and lowered[kk]:
                    cname = str(extract_first_string(lowered[kk]) or "")
                    break
            if cname:
                break
        events.append({"filed": filed_d, "filed_str": filed_str, "ticker": ticker, "cik": cik_padded or cik, "company": cname, "forms": forms_list, "acc": acc_norm, "raw_id": str(h.get("_id", ""))})
    print(f"Parsed events pre-dedup: {len(events)} (no-date/other drops: {n_no_date} of {len(hits)})")
    seen = {}
    for e in events:
        key = e["acc"]
        if key not in seen:
            seen[key] = e
        else:
            if seen[key]["ticker"] is None and e["ticker"] is not None:
                seen[key] = e
    dedup = list(seen.values())
    print(f"After accession dedup: {len(dedup)} (from {len(events)})")
    with_ticker = [e for e in dedup if e["ticker"]]
    no_ticker = len(dedup) - len(with_ticker)
    print(f"Events with ticker: {len(with_ticker)}, without ticker (dropped): {no_ticker}")
    seen2 = {}
    for e in sorted(with_ticker, key=lambda x: (x["filed_str"], x["ticker"], x["acc"])):
        k = (e["ticker"], e["filed_str"])
        if k not in seen2:
            seen2[k] = e
    final = sorted(seen2.values(), key=lambda x: (x["filed_str"], x["ticker"]))
    print(f"After company-date dedup: {len(final)} events")
    return final, no_ticker

def compute_return_for_event(ticker, filing_d):
    start = (filing_d - timedelta(days=20)).isoformat()
    end = (filing_d + timedelta(days=20)).isoformat()
    df = get_prices(ticker, start, end)
    if df is None or len(df) == 0:
        raise MarketDataUnavailable(f"empty prices {ticker}")
    df = df.sort_index()
    idx = df.index
    target = pd.Timestamp(filing_d)
    pos0 = None
    for i, d in enumerate(idx):
        if d.normalize() >= target.normalize():
            pos0 = i
            break
    if pos0 is None:
        raise MarketDataUnavailable(f"no trading day >= filing {ticker} {filing_d}")
    if pos0 - 1 < 0:
        raise MarketDataUnavailable(f"no T-1 {ticker} {filing_d}")
    if pos0 + 5 >= len(df):
        raise MarketDataUnavailable(f"no T+5 {ticker} {filing_d}")
    col = "close" if "close" in df.columns else "adj_close"
    p0 = float(df.iloc[pos0 - 1][col])
    p1 = float(df.iloc[pos0 + 5][col])
    if not np.isfinite(p0) or not np.isfinite(p1) or p0 <= 0:
        raise MarketDataUnavailable(f"bad prices {ticker}")
    ret = (p1 - p0) / p0 * 100.0
    return ret

def main():
    print("Step 0: load CIK map")
    cik_to_ticker = load_cik_to_ticker()
    print("Step 1: search EDGAR Item 1.05 8-K")
    hits = search_item105()
    events, no_ticker_drops = parse_hits(hits, cik_to_ticker)
    print(f"Candidate events for market-data stage: {len(events)}")
    returns = []
    event_rows = []
    price_drops = 0
    for e in events:
        t = e["ticker"]
        f = e["filed"]
        try:
            r = compute_return_for_event(t, f)
        except MarketDataUnavailable as ex:
            price_drops += 1
            print(f"DROP price {t} {f}: {ex}")
            continue
        returns.append(r)
        event_rows.append({"ticker": t, "cik": e["cik"], "filed": f, "ret": r, "company": e["company"]})
    print(f"Events with valid returns: {len(event_rows)}, price drops: {price_drops}, no-ticker drops: {no_ticker_drops}")
    returns = np.array([x["ret"] for x in event_rows], dtype=float)
    tickers_unique = sorted(set(x["ticker"] for x in event_rows))
    print(f"Unique tickers with returns: {len(tickers_unique)}")
    mcap_map = {}
    sector_map = {}
    beta_map = {}
    mcap_missing = 0
    sector_missing = 0
    beta_missing = 0
    for t in tickers_unique:
        try:
            mc = get_market_cap(t)
        except MarketDataUnavailable:
            mc = None
        if mc is None or (isinstance(mc, float) and (not np.isfinite(mc) or mc <= 0)):
            try:
                mc_f = float(mc) if mc is not None else None
            except Exception:
                mc_f = None
            if mc_f is None or not np.isfinite(mc_f) or mc_f <= 0:
                mcap_missing += 1
                mcap_map[t] = None
            else:
                mcap_map[t] = mc_f
        else:
            try:
                mcap_map[t] = float(mc)
            except Exception:
                mcap_map[t] = None
                mcap_missing += 1
        try:
            prof = get_profile(t)
        except MarketDataUnavailable:
            prof = None
        except Exception:
            prof = None
        if prof is None:
            sector_map[t] = None
            beta_map[t] = None
            sector_missing += 1
            beta_missing += 1
        else:
            s = prof.get("sector") if isinstance(prof, dict) else None
            b = prof.get("beta") if isinstance(prof, dict) else None
            if s is None or (isinstance(s, str) and s.strip() == ""):
                sector_map[t] = None
                sector_missing += 1
            else:
                sector_map[t] = str(s).strip()
            try:
                bf = float(b) if b is not None else None
            except Exception:
                bf = None
            if bf is None or not np.isfinite(bf):
                beta_map[t] = None
                beta_missing += 1
            else:
                beta_map[t] = bf
    print(f"mcap missing tickers: {mcap_missing}, sector missing: {sector_missing}, beta missing: {beta_missing}")
    for x in event_rows:
        t = x["ticker"]
        x["mcap"] = mcap_map.get(t)
        x["sector"] = sector_map.get(t)
        x["beta"] = beta_map.get(t)
        x["is_tech"] = (str(x["sector"]).strip().lower() == "technology") if x["sector"] else None
        x["is_small"] = (x["mcap"] < 2e9) if (x["mcap"] is not None) else None
    n_all = len(returns)
    mean_all = float(np.mean(returns)) if n_all > 0 else None
    sd_all = float(np.std(returns, ddof=1)) if n_all > 1 else None
    se_all = float(sd_all / np.sqrt(n_all)) if sd_all is not None else None
    if n_all > 1:
        tres = stats.ttest_1samp(returns, 0.0, alternative="less")
        t_all = float(tres.statistic)
        p_all = float(tres.pvalue)
    else:
        t_all = None
        p_all = None
    print(f"Overall n={n_all} mean={mean_all} sd={sd_all} t={t_all} p={p_all}")
    tech_rets = np.array([x["ret"] for x in event_rows if x["is_tech"] is True], dtype=float)
    nontech_rets = np.array([x["ret"] for x in event_rows if x["is_tech"] is False], dtype=float)
    n_tech, n_nontech = len(tech_rets), len(nontech_rets)
    mean_tech = float(np.mean(tech_rets)) if n_tech > 0 else None
    mean_nontech = float(np.mean(nontech_rets)) if n_nontech > 0 else None
    se_tech = float(np.std(tech_rets, ddof=1) / np.sqrt(n_tech)) if n_tech > 1 else None
    se_nontech = float(np.std(nontech_rets, ddof=1) / np.sqrt(n_nontech)) if n_nontech > 1 else None
    if n_tech > 1 and n_nontech > 1:
        w = stats.ttest_ind(tech_rets, nontech_rets, equal_var=False, alternative="less")
        t_sec, p_sec = float(w.statistic), float(w.pvalue)
    else:
        t_sec, p_sec = None, None
    print(f"Sector tech n={n_tech} mean={mean_tech}; nontech n={n_nontech} mean={mean_nontech}; t={t_sec} p={p_sec}")
    small_rets = np.array([x["ret"] for x in event_rows if x["is_small"] is True], dtype=float)
    larger_rets = np.array([x["ret"] for x in event_rows if x["is_small"] is False], dtype=float)
    n_small, n_larger = len(small_rets), len(larger_rets)
    mean_small = float(np.mean(small_rets)) if n_small > 0 else None
    mean_larger = float(np.mean(larger_rets)) if n_larger > 0 else None
    se_small = float(np.std(small_rets, ddof=1) / np.sqrt(n_small)) if n_small > 1 else None
    se_larger = float(np.std(larger_rets, ddof=1) / np.sqrt(n_larger)) if n_larger > 1 else None
    if n_small > 1 and n_larger > 1:
        w = stats.ttest_ind(small_rets, larger_rets, equal_var=False, alternative="less")
        t_size, p_size = float(w.statistic), float(w.pvalue)
    else:
        t_size, p_size = None, None
    print(f"Size small n={n_small} mean={mean_small}; larger n={n_larger} mean={mean_larger}; t={t_size} p={p_size}")
    beta_vals = np.array([x["beta"] for x in event_rows if x["beta"] is not None], dtype=float)
    beta_vals = beta_vals[np.isfinite(beta_vals)]
    if len(beta_vals) > 0:
        beta_median = float(np.median(beta_vals))
        beta_outlier = float(np.max(beta_vals))
    else:
        beta_median, beta_outlier = None, None
    print(f"Beta median={beta_median} max={beta_outlier} n_beta={len(beta_vals)}")
    low_rets = np.array([x["ret"] for x in event_rows if x["beta"] is not None and x["beta"] <= beta_median], dtype=float) if beta_median is not None else np.array([])
    high_rets = np.array([x["ret"] for x in event_rows if x["beta"] is not None and x["beta"] > beta_median], dtype=float) if beta_median is not None else np.array([])
    n_low, n_high = len(low_rets), len(high_rets)
    mean_low = float(np.mean(low_rets)) if n_low > 0 else None
    mean_high = float(np.mean(high_rets)) if n_high > 0 else None
    se_low = float(np.std(low_rets, ddof=1) / np.sqrt(n_low)) if n_low > 1 else None
    se_high = float(np.std(high_rets, ddof=1) / np.sqrt(n_high)) if n_high > 1 else None
    if n_high > 1 and n_low > 1:
        w = stats.ttest_ind(high_rets, low_rets, equal_var=False, alternative="less")
        t_beta, p_beta = float(w.statistic), float(w.pvalue)
    else:
        t_beta, p_beta = None, None
    print(f"Beta low n={n_low} mean={mean_low}; high n={n_high} mean={mean_high}; t(high vs low, less)={t_beta} p={p_beta}")
    from collections import Counter
    cnt = Counter(x["ticker"] for x in event_rows)
    n_companies = len(cnt)
    n_one = sum(1 for v in cnt.values() if v == 1)
    n_two = sum(1 for v in cnt.values() if v == 2)
    n_three = sum(1 for v in cnt.values() if v == 3)
    total_reports = len(event_rows)
    print(f"Total reports={total_reports} unique={n_companies} one={n_one} two={n_two} three={n_three}")
    print(f"Counts per company: {dict(cnt)}")
    def R(name, value, se, n):
        if value is None:
            return None
        v = float(value) if isinstance(value, (int, float, np.floating)) else value
        return {"name": name, "value": v, "se": (float(se) if se is not None and np.isfinite(se) else None), "n": (int(n) if n is not None else None)}
    results = []
    for r in [
        R("total_item105_reports", float(total_reports), None, total_reports),
        R("unique_companies", float(n_companies), None, n_companies),
        R("companies_one_report", float(n_one), None, n_companies),
        R("companies_two_reports", float(n_two), None, n_companies),
        R("companies_three_reports", float(n_three), None, n_companies),
        R("technology_n", float(n_tech), None, n_tech),
        R("nontechnology_n", float(n_nontech), None, n_nontech),
        R("small_cap_n", float(n_small), None, n_small),
        R("larger_cap_n", float(n_larger), None, n_larger),
        R("beta_outlier", beta_outlier, None, len(beta_vals)),
        R("beta_median", beta_median, None, len(beta_vals)),
        R("overall_mean_return", mean_all, se_all, n_all),
        R("overall_sd_return", sd_all, None, n_all),
        R("overall_t", t_all, None, n_all),
        R("overall_p", p_all, None, n_all),
        R("technology_mean_return", mean_tech, se_tech, n_tech),
        R("nontechnology_mean_return", mean_nontech, se_nontech, n_nontech),
        R("sector_t", t_sec, None, n_tech + n_nontech),
        R("sector_p", p_sec, None, n_tech + n_nontech),
        R("small_mean_return", mean_small, se_small, n_small),
        R("larger_mean_return", mean_larger, se_larger, n_larger),
        R("size_t", t_size, None, n_small + n_larger),
        R("size_p", p_size, None, n_small + n_larger),
        R("low_beta_mean_return", mean_low, se_low, n_low),
        R("high_beta_mean_return", mean_high, se_high, n_high),
        R("beta_t", t_beta, None, n_low + n_high),
        R("beta_p", p_beta, None, n_low + n_high),
    ]:
        if r is not None:
            results.append(r)
    sample_desc = (f"Form 8-K Item 1.05 filings with filed date<=2025-11-12 from SEC EDGAR FTS; {len(events)} candidate events, {total_reports} with valid 7-trading-day returns; " f"per-company info via market_data (current mcap/sector/beta). Price drops {price_drops}, no-ticker drops {no_ticker_drops}.")
    notes = ("EDGAR source: efts.sec.gov/LATEST/search-index q='Item 1.05' forms=8-K daterange 2023-12-01 to 2025-11-12; excluded 8-K/A amendments and deduped by accession and by ticker+filing-date (no duplicates; multiple dates per company kept separate). " "Filing trading day T0=first trading day >= filing calendar date using market_data bars; window=T-1 (prior trading day close) through T0+5 (5 trading days after T0), 7 trading days; return=(close[T0+5]-close[T-1])/close[T-1]*100 using close (adj_close fallback). Price window fetched +-20 calendar days via get_prices. " "Company traits current (not historical): get_market_cap and get_profile sector/beta per ticker cached across events; Small <$2B vs larger >=$2B; Technology iff sector=='Technology' (case-insensitive) vs all others; beta median split on event-level non-missing betas with low=beta<=median, high=beta>median. " "Excluded MarketDataUnavailable only (price drops, missing mcap/sector/beta excluded from analyses requiring them). Tests: one-sample left-tailed t (H1 mean<0) via scipy ttest_1samp; subgroup Welch left-tailed ttest_ind(equal_var=False, alternative='less') with order tech-vs-nontech, small-vs-larger, high-vs-low. SE for means=sd/sqrt(n). " f"Deviations/open choices: current traits vs at-filing traits; close vs adj_close choice immaterial over 6 trading days; median-split tie rule (median in low); FTS coverage/parse may differ from authors' sec-api pull; counts after filters printed to stdout. Drops: price {price_drops}, no-ticker {no_ticker_drops}, mcap-missing tickers {mcap_missing}, sector-missing {sector_missing}, beta-missing {beta_missing}.")
    out = {"results": results, "sample": {"description": sample_desc, "n": total_reports}, "notes": notes}
    with open("/work/results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote /work/results.json")

if __name__ == "__main__":
    main()
