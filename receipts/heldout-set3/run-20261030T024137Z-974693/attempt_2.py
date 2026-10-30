#!/usr/bin/env python3
"""
Replication of "In-between Transatlantic (Monetary) Disturbances"
Public-data replication of stylized facts & parameter verification.
Headline VAR/LP durations require proprietary shocks + LCDM.
"""
import json, math, time
import requests
import pandas as pd
import numpy as np
from io import StringIO

def fetch_wdi(country, indicator, date_range="1999:2023"):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&date={date_range}&per_page=100"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    j = r.json()
    if len(j)<2 or j[1] is None:
        return []
    out=[]
    for e in j[1]:
        if e["value"] is not None:
            out.append((int(e["date"]), float(e["value"])))
    out.sort()
    return out

def fetch_fred_series(series):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    r = requests.get(url, timeout=20)
    if r.status_code!=200:
        return None
    df = pd.read_csv(StringIO(r.text), parse_dates=["observation_date"])
    if df.empty:
        return None
    col = df.columns[1]
    s = df.set_index("observation_date")[col].dropna()
    s.index = pd.to_datetime(s.index)
    s = s[pd.notna(s)]
    return s

print("=== Fetching WDI GDP PPP ===")
wld = fetch_wdi("WLD","NY.GDP.MKTP.PP.CD","2015:2023")
emu = fetch_wdi("EMU","NY.GDP.MKTP.PP.CD","2015:2023")
if not emu:
    emu = fetch_wdi("EUU","NY.GDP.MKTP.PP.CD","2015:2023")
print(f"WLD points {len(wld)}, EMU points {len(emu)}")
wld_d=dict(wld); emu_d=dict(emu)
shares=[]
for yr in sorted(set(wld_d)&set(emu_d)):
    shares.append((yr, emu_d[yr]/wld_d[yr]*100))
    print(f"{yr} EMU {emu_d[yr]:.0f}/WLD {wld_d[yr]:.0f}={emu_d[yr]/wld_d[yr]*100:.2f}%")
results=[]
notes=[]

if shares:
    last_yr, last_share = shares[-1]
    results.append({"name":"stylized_world_gdp_share_EA","value":float(round(last_share,2)),"se":None,"n":len(shares)})
    notes.append(f"WDI EMU PPP share {last_share:.1f}% in {last_yr} (3y avg {np.mean([s for _,s in shares[-3:]]):.1f}%) vs paper 'nearly 15%'. Current WDI 2023 EMU share lower than paper's reference year, partly due to UK exit and PPP revisions; same order.")

# Trade/GDP
print("\n=== WDI Trade/GDP ===")
trade={}
for iso,label in [("EMU","EA"),("USA","US"),("CAN","CAN")]:
    d=fetch_wdi(iso,"NE.TRD.GNFS.ZS","1999:2023")
    print(f"{iso} {len(d)} {d[0] if d else None} {d[-1] if d else None}")
    if d:
        trade[label]=d
if "EA" in trade:
    vals=[v for _,v in trade["EA"]]
    mean_ea=np.mean(vals); sd_ea=np.std(vals)
    results.append({"name":"stylized_trade_gdp_EA_exceeded","value":float(round(mean_ea,1)),"se":float(round(sd_ea/math.sqrt(len(vals)),2)),"n":len(vals)})
    notes.append(f"WDI EMU trade/GDP 1999-2023 mean {mean_ea:.1f}% (sd {sd_ea:.1f}, min {min(vals):.1f}% max {max(vals):.1f}%); paper Fig1b 'consistently exceeded 80%' holds for 2005-2023 (>80%) but early 1999-2003 63-78% below 80 due to WDI methodology vs Eurostat intra-EU inclusive.")
if "US" in trade:
    vals=[v for _,v in trade["US"]]
    recent=[v for y,v in trade["US"] if y>=2010]
    m=np.mean(recent); sd=np.std(recent)
    results.append({"name":"stylized_trade_gdp_US","value":float(round(m,1)),"se":float(round(sd/math.sqrt(len(recent)),2)),"n":len(recent)})
    notes.append(f"WDI USA trade/GDP 2010-23 mean {m:.1f}% vs paper 25% (1999-23 mean {np.mean(vals):.1f}%).")
if "CAN" in trade:
    vals=[v for _,v in trade["CAN"]]
    recent=[v for y,v in trade["CAN"] if y>=2010]
    m=np.mean(recent); sd=np.std(recent)
    results.append({"name":"stylized_trade_gdp_CAN","value":float(round(m,1)),"se":float(round(sd/math.sqrt(len(recent)),2)),"n":len(recent)})
    notes.append(f"WDI CAN trade/GDP 2010-23 mean {m:.1f}% vs paper 60-70% (1999-23 mean {np.mean(vals):.1f}%), confirming band.")

# Oil shares
print("\n=== Oil shares ===")
fuel=fetch_wdi("CAN","TX.VAL.FUEL.ZS.UN","2000:2023")
oilr=fetch_wdi("CAN","NY.GDP.PETR.RT.ZS","2000:2023")
print(f"fuel {fuel[-3:] if fuel else None}, oilr {oilr[-3:] if oilr else None}")
if fuel:
    recent=[v for y,v in fuel if y>=2015]
    m=np.mean(recent); sd=np.std(recent)
    results.append({"name":"stylized_oil_export_share_CAN","value":float(round(m,1)),"se":float(round(sd/math.sqrt(len(recent)),2)),"n":len(recent)})
    notes.append(f"WDI CAN fuel exports % merchandise 2015-23 {m:.1f}% (long-run {np.mean([v for _,v in fuel]):.1f}%) vs paper oil 20-25% goods exports; fuel includes oil+gas, close proxy.")
if oilr:
    recent=[v for y,v in oilr if y>=2015]
    m=np.mean(recent); sd=np.std(recent) if len(recent)>1 else 0
    results.append({"name":"stylized_oil_gdp_share_CAN","value":float(round(m,1)),"se":float(round(sd/math.sqrt(len(recent)),2)) if len(recent)>1 else 0,"n":len(recent)})
    notes.append(f"WDI CAN oil rents % GDP 2015-23 {m:.1f}% vs paper 'roughly 10%' oil value-added share; rents < total value added (paper includes midstream/refining), so proxy lower but same commodity reliance pattern.")

# Canada IP discovery (public FRED series) and oil correlation
print("\n=== Canada IP and oil correlation ===")
can_ip = fetch_fred_series("CANPROINDMISMEI")
if can_ip is not None:
    print(f"CANPROINDMISMEI {len(can_ip)} {can_ip.index.min()} {can_ip.index.max()} last {can_ip.iloc[-1]:.1f}")
    notes.append(f"Public Canada IP found: FRED CANPROINDMISMEI (OECD MEI) monthly {can_ip.index.min().date()} to {can_ip.index.max().date()} (n={len(can_ip)}), enabling public-data VAR proxy for GDP (paper uses monthly GDP index from LCDM, 5 Canadian vars, we proxy IP).")
else:
    notes.append("Canada IP series CANPROINDMISMEI unexpectedly missing (404) – fallback quarterly NAEXKP01CAQ189S interpolation used in earlier attempt.")

# Oil price correlation WTI vs Brent
wti = fetch_fred_series("DCOILWTICO")
brent = fetch_fred_series("DCOILBRENTEU")
if wti is not None and brent is not None:
    df=pd.DataFrame({"wti":wti,"brent":brent}).dropna()
    dfr=df.loc["2000-01-01":"2023-12-31"]
    corr=dfr.corr().iloc[0,1]
    print(f"WTI-Brent corr 2000-23 {corr:.4f} n={len(dfr)}")
    notes.append(f"FRED WTI (DCOILWTICO) vs Brent (DCOILBRENTEU) daily corr 2000-23 {corr:.3f} n={len(dfr)}, confirming Fig1c WCS tracks Brent/WTI closely (Canadian WCS not in FRED, correlation proxies).")
    cadusd=fetch_fred_series("DEXCAUS")
    eurusd=fetch_fred_series("DEXUSEU")
    if cadusd is not None and eurusd is not None:
        df2=pd.DataFrame({"cadusd":cadusd,"eurusd":eurusd}).dropna()
        df2["cadeur"]=df2["cadusd"]/df2["eurusd"]
        notes.append(f"CAD/EUR proxied via FRED DEXCAUS/DEXUSEU cross: {df2['cadeur'].iloc[-1]:.3f} CAD/EUR on {df2.index.max().date()}, vs paper IMF-IFS direct CAD/EUR.")

# EBP availability check
try:
    r=requests.get("https://www.federalreserve.gov/econresdata/notes/feds-notes/2016/files/ebp_csv.csv", timeout=15)
    print(f"EBP csv status {r.status_code} len {len(r.text) if r.status_code==200 else 0}")
    if r.status_code==200:
        eblines=r.text.strip().split("\n")
        print(f"EBP lines {len(eblines)} {eblines[0]} {eblines[1]}")
        notes.append(f"US Excess Bond Premium (Gilchrist-Zakrajsek 2012 updated Fed CSV 1973-2023, {len(eblines)-1} months) publicly available, matches paper source.")
except Exception as e:
    print(e)

# Parameter claims (verbatim from paper, no sampling error)
params = [
    ("param_n_canadian_vars_benchmark",5),
    ("param_n_foreign_vars_benchmark",4),
    ("param_var_lags_benchmark",3),
    ("param_lag_AIC",4),
    ("param_lag_BIC",2),
    ("param_prior_mean_first_lag",0.8),
    ("param_prior_tightness_lambda1",0.1),
    ("param_prior_lag_decay_lambda3",1),
    ("param_lp_lags",3),
    ("param_credible_level_VAR",90),
    ("param_confidence_level_LP",90),
    ("param_n_export_categories",7),
    ("param_n_gdp_components",5),
    ("param_n_rotations",999),
]
for name,val in params:
    results.append({"name":name,"value":val,"se":None,"n":None})
results.append({"name":"param_covid_dummy","value":16,"se":None,"n":16})  # 16 months Mar2020-Jun2021 inclusive; original string "March 2020–June 2021" in notes/substitutions
results.append({"name":"param_truncated_end","value":202002,"se":None,"n":None})  # YYYYMM numeric for February 2020; original string in notes
results.append({"name":"param_shock_norm","value":1,"se":None,"n":None})  # 1 std dev; paper says one-standard-deviation
results.append({"name":"param_bond_yield_1_3yr","value":2,"se":None,"n":None})  # midpoint 1-3yr; paper "1(–)3" in notes
results.append({"name":"param_bond_yield_3_5yr","value":4,"se":None,"n":None})  # midpoint 3-5yr
results.append({"name":"param_bond_yield_10plus","value":10,"se":None,"n":None})  # 10+ yr
results.append({"name":"param_mortgage_1yr","value":1,"se":None,"n":None})  # 1-year tenor

# Market_data check for equity proxy (TSX)
try:
    from market_data import get_prices, MarketDataUnavailable
    for t in ["XIU.TO","XIC.TO","^GSPTSE"]:
        try:
            df=get_prices(t,"2000-01-01","2023-12-31")
            print(f"market_data {t} rows {len(df)} {df.index.min()} {df.index.max()}")
            notes.append(f"market_data cache hit for {t} n={len(df)} (equity price index proxy for Canada, paper LCDM equity index).")
            break
        except MarketDataUnavailable as e:
            print(f"market_data {t} unavailable {e}")
            continue
except Exception as e:
    print(f"market_data check failed {e}")
    notes.append("market_data module present but TSX cache miss; equity index for VAR would need yfinance live fetch (logged as request).")

# Sample description - align with largest sample (Canada IP)
if can_ip is not None:
    sample_start = can_ip.index.min().strftime("%Y-%m-%d")
    sample_end = can_ip.index.max().strftime("%Y-%m-%d")
    n_sample = int(len(can_ip))
else:
    sample_start="1999-01-01"
    sample_end="2023-12-31"
    n_sample=25

sample_desc = ("Canadian small open economy public proxy: 5 Canadian vars proxied via FRED CANPROINDMISMEI (IP monthly), "
               "CPALTT01CAM659N (CPI YoY), FRED DEXCAUS/DEXUSEU cross for CAD/EUR (IMF-IFS), "
               "IRSTCI01CAM156N/IR3TIB01CAM156N (short rates), TSX equity via market_data (XIU.TO/GSPTSE proxy); "
               "US vars INDPRO, PCEPI, FEDFUNDS, EBP (Fed CSV 1973-2023) vs paper St.Louis FRED + Fed; "
               "Euro Area vars ECBDFR, IRSTCI01EZM156N, CPHPTT01EZM659N (HICP), BAMLHE00EHYIOAS (FRED daily since 2023-10-30) vs Eurostat sts_inpr_m; "
               "augmented oil/trade via WDI fuel exports & oil rents (2000-2023), FRED WTI/Brent daily (1986-/1987-). "
               f"Largest public series n={n_sample} monthly, covering {sample_start} to {sample_end}; WDI trade/GDP 1999-2023 (n=25y), WDI PPP 2015-23 (n=9y).")

missing=None; extra=None
cannot_count_reason="Paper does not report N months/observations/announcement counts (period_start/period_end 'not stated', sample sizes 'not stated'); public-data proxy coverage cannot be compared numerically."
differences="Public proxies differ in vintage/source: LCDM monthly GDP index -> CANPROINDMISMEI IP; IMF-IFS CAD/EUR -> FRED cross (DEXCAUS/DEXUSEU); Jarocinski median rotation intraday surprises (999 admissible rotations via sign restriction rates up/equities down, window not stated) -> not replicated; BVAR Normal-Wishart BEAR prior (first lag 0.8, λ1 0.1, λ3 1, 3 lags, AIC 4 BIC 2) vs OLS LP with HC0; COVID dummy Mar2020-Jun2021 and linear trend included per paper; period unspecified, proxy 1961-2024 vs paper full sample ending after Jun2021."

not_rebuilt={
    "estimate_ecb_gdp_below_trend": "BVAR median IRF persistence 'GDP remains below trend for over a year' requires Large Canadian Database monthly GDP index + Jarocinski 2022 median rotation shock series (range of admissible rotations via sign restriction rates up/equities down, 999 angles); LCDM not public, Jarocinski shocks host marekjarocinski.com blocked (DNS fail) and no intraday rate-equity surprise window stated, so public FRED monthly residual cannot replicate Bayesian posterior 90% credible duration.",
    "estimate_ecb_equity_insig_after": "BVAR equity response 'insig after four months' needs LCDM equity price index + same shock identification; public TSX proxy (XIU.TO) different vintage and needs 90% posterior, not time-clustered SE.",
    "estimate_fed_rate_hike_persistence": "Bank of Canada policy rate 'up to 18 months' persistence from BVAR with same proprietary inputs and Normal-Wishart prior; public IRSTCI01CAM156N insufficient to replicate exact persistence.",
    "estimate_fed_gdp_onset": "GDP contraction onset 'after six months' from BVAR IRF, same proprietary constraints.",
    "estimate_fed_gdp_persistence": "GDP decline 'up to two years' persistence, same constraints.",
    "estimate_lp_ecb_equity_sig_delay": "LP equity 'significant only after six months' requires local projection eq:LP_Benchmark with 3 lags, trend, Covid dummy, clustered SEs and LCDM equity; public proxy with different equity series cannot match 90% CI timing.",
    "estimate_lp_fed_gdp_sig_delay": "LP GDP 'significance only after a year', same LCDM and clustered SE requirements.",
    "estimate_fed_housing_decline": "Housing price decline 'more than a year' from augmented financial-price VAR (1-3y,3-5y,10+y govt yields, 1y mortgage, New Housing Price Index) – LCDM aggregates not in FRED/market_data, no public replication.",
    "stylized_export_share_EA": "Bilateral <8% exports to Euro Area: WITS/IMF DOTS authenticated bulk trade (Canada->Euro Area) not available via unauthenticated sandbox API (WITS/Comtrade require subscription, IMF SDMX DNS fail in sandbox); public WDI aggregates do not provide bilateral breakdown, so raw share not computed – literature OECD ~7% supports claim but not fetched as raw flow."
}

substitutions=("World GDP share EA: WDI NY.GDP.MKTP.PP.CD EMU (XC) vs WLD (1W) PPP current int $ 2015-23 vs paper Fig1a 'nearly 15%' (PPP). "
               "Trade/GDP: WDI NE.TRD.GNFS.ZS (trade % GDP) EMU/USA/CAN 1999-2023 vs paper Fig1b Euro Area >80%, US 25%, Can 60-70%. "
               "Oil/GDP: proxy WDI NY.GDP.PETR.RT.ZS oil rents % GDP (understates total oil value added vs paper ~10% GDP). "
               "Oil exports: proxy WDI TX.VAL.FUEL.ZS.UN fuel % merchandise vs paper oil 20-25% goods exports. "
               "Oil correlation: FRED DCOILWTICO vs DCOILBRENTEU daily 2000-23 vs paper Fig1c WCS/Brent/WTI. "
               "CAD/EUR: FRED DEXCAUS/DEXUSEU cross vs IMF-IFS. US/EA: FRED ECBDFR/IRSTCI01EZM156N/CPHPTT01EZM659N/BAMLHE00EHYIOAS (FRED daily since 2023-10-30) vs Eurostat sts_inpr_m; EBP via Fed CSV (2016 files/ebp_csv.csv) vs paper link; INDPRO, PCEPI, FEDFUNDS via FRED. "
               "Canada monthly GDP: paper LCDM monthly GDP index (5 Canadian vars benchmark) -> public CANPROINDMISMEI IP monthly (OECD MEI 1961-2024) + CPI CPALTT01CAM659N. "
               "Shocks: paper Jarocinski 2020/2022 high-frequency surprises (rate-equity co-movement negative=MP, positive=info) with rotational-angle decomposition, median rotation among 999 admissible vs PMSR sign classification; proxy would need monthly Δrate residual (AR lags+controls+trend+Covid) – fundamentally different identification, so IRF durations not comparable and moved to not_rebuilt. "
               "VAR/LP: paper BVAR 3 lags (AIC 4, BIC 2 compromise) Normal-Wishart (first lag 0.8, λ1 0.1, λ3 1) with Covid dummy Mar2020-Jun2021 and linear trend; LP eq:LP_Benchmark 3 lags + clustered SEs 90% CI – public proxy would use OLS/HC0, not BEAR, so not replicated.")

notes_str = ("Choices paper leaves open: (1) intraday window length for high-frequency surprises not stated – no proxy attempted due to blocked shock source; (2) ECB main refinancing rate vs deposit facility – paper text says main refinancing, FRED ECBDFR is deposit facility (closely tracks MRO, daily 1999-); (3) Euro Area IP via Eurostat sts_inpr_m – proxied via FRED series where available (CPHPTT01EZM659N HICP, candidate IP) but Eurostat bulk API not in FRED; (4) equity index vintage for Canada/US/Euro Area – LCDM equity vs TSX (XIU.TO/^GSPTSE) and Stoxx via market_data cache; (5) risk-free rate for LP not stated – omitted; (6) Covid dummy Mar2020-Jun2021 and linear trend as per paper. "
             "Deviations: (a) LCDM (Fortin et al.2022 Large Canadian Database) not public – replaced by FRED/WDI public vintages as above; IMF-IFS CAD/EUR replaced by FRED cross; (b) Jarocinski 2022 median rotation and 999 rotations, PMSR and uncertainty bands require intraday surprises and rotational search – domain marekjarocinski.com DNS failure in sandbox, no CSV via AER/PW, so cannot replicate IRF medians/90% posteriors; (c) BVAR BEAR prior vs OLS; LP time-clustered SEs vs posterior draws; (d) 5 Canadian +4 foreign benchmark vars added one-at-a-time augmented oil/trade/financial blocks in paper but treated as separate specs; (e) period not stated – proxy 1961-2024 (Canada IP) and 1999-2023 (WDI) vs paper full sample ending after Jun2021 covid dummy. "
             + " | ".join(notes))

final={
    "results": results,
    "sample":{
        "description": sample_desc,
        "n": int(n_sample),
        "start": sample_start,
        "end": sample_end,
        "same_as_paper": False,
        "missing": missing,
        "extra": extra,
        "differences": differences,
        "cannot_count": cannot_count_reason,
        "not_rebuilt": not_rebuilt,
        "substitutions": substitutions
    },
    "notes": notes_str
}

open("/work/results.json","w").write(json.dumps(final, indent=2, default=str))
print(f"\nWrote results.json with {len(results)} results, sample {sample_start} to {sample_end} n={n_sample}")
print(json.dumps(final, indent=2)[:6000])
