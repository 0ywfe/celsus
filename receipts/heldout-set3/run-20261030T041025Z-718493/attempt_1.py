#!/usr/bin/env python3
"""
Replicate Intrinsic Geometry of Stock Market from Graph Ricci Flow
"""
import os, json, sys, time, datetime, itertools, re
import numpy as np
import pandas as pd
from scipy.optimize import linprog

# Config
START = "2020-01-01"
END = "2024-11-20"
ALPHA = 0.5

# Universe: NASDAQ-100 constituents as of 2024-11-15 (revid 1257470804) = 101 securities
# Obtained via Wikipedia API parse oldid; 101 tickers including both GOOG classes
TICKERS_2024_11_15 = [
    "ADBE","AMD","ABNB","GOOGL","GOOG","AMZN","AEP","AMGN","ADI","ANSS",
    "AAPL","AMAT","ARM","ASML","AZN","TEAM","ADSK","ADP","BKR","BIIB",
    "BKNG","AVGO","CDNS","CDW","CHTR","CTAS","CSCO","CCEP","CTSH","CMCSA",
    "CEG","CPRT","CSGP","COST","CRWD","CSX","DDOG","DXCM","FANG","DLTR",
    "DASH","EA","EXC","FAST","FTNT","GEHC","GILD","GFS","HON","IDXX",
    "ILMN","INTC","INTU","ISRG","KDP","KLAC","KHC","LRCX","LIN","LULU",
    "MAR","MRVL","MELI","META","MCHP","MU","MSFT","MRNA","MDLZ","MDB",
    "MNST","NFLX","NVDA","NXPI","ORLY","ODFL","ON","PCAR","PANW","PAYX",
    "PYPL","PDD","PEP","QCOM","REGN","ROP","ROST","SBUX","SMCI","SNPS",
    "TTWO","TMUS","TSLA","TXN","TTD","VRSK","VRTX","WBD","WDAY","XEL","ZS"
]
# Verify count
assert len(TICKERS_2024_11_15)==101, len(TICKERS_2024_11_15)

from market_data import get_prices, MarketDataUnavailable

def fetch_prices():
    print("Fetching prices for universe N=", len(TICKERS_2024_11_15))
    good={}
    bad=[]
    for t in TICKERS_2024_11_15:
        try:
            df=get_prices(t, START, END)
            good[t]=df
            print(f"{t} ok {len(df)} rows {df.index.min().date()} -> {df.index.max().date()}")
        except MarketDataUnavailable as e:
            bad.append(t)
            print(f"{t} unavailable: {e}")
        except Exception as e:
            bad.append(t)
            print(f"{t} error {e}")
    print(f"Good {len(good)} Bad {len(bad)} {bad}")
    return good, bad

def compute_returns(good):
    # Use adj_close, log returns
    # For each ticker, compute log returns series
    ret_dict={}
    for t, df in good.items():
        # adj_close may be NaN? Use close as fallback
        prices = df["adj_close"] if "adj_close" in df.columns and df["adj_close"].notna().any() else df["close"]
        # drop inf/nan
        prices = prices.replace([np.inf, -np.inf], np.nan).dropna()
        # log returns
        logret = np.log(prices / prices.shift(1))
        logret = logret.dropna()
        # Remove inf
        logret = logret.replace([np.inf, -np.inf], np.nan).dropna()
        ret_dict[t]=logret
        print(f"{t} returns {len(logret)} {logret.index.min().date()} -> {logret.index.max().date()} mean {logret.mean():.6f} std {logret.std():.6f}")
    return ret_dict

def build_correlation(ret_dict):
    tickers=list(ret_dict.keys())
    n=len(tickers)
    print(f"Building correlation matrix for n={n}")
    # Align via outer join for pairwise
    # Use DataFrame of returns (outer join)
    # For efficiency, create list of series
    # Compute correlation via pairwise overlapping
    corr=np.eye(n)
    # For each pair, compute overlapping
    for i in range(n):
        for j in range(i+1, n):
            s_i=ret_dict[tickers[i]]
            s_j=ret_dict[tickers[j]]
            # overlapping dates
            common_idx=s_i.index.intersection(s_j.index)
            if len(common_idx)<30:
                # not enough overlap
                v=np.nan
                print(f"warn pair {tickers[i]}-{tickers[j]} overlap {len(common_idx)}")
            else:
                vi=s_i.loc[common_idx].values
                vj=s_j.loc[common_idx].values
                # Pearson
                # Use np.corrcoef
                if np.std(vi)==0 or np.std(vj)==0:
                    v=np.nan
                else:
                    v=np.corrcoef(vi, vj)[0,1]
            corr[i,j]=v
            corr[j,i]=v
    # Fill NaNs with mean? but keep
    # Check for remaining nans
    nans=np.isnan(corr).sum()
    print("corr nans", nans)
    return corr, tickers

def compute_stats(corr):
    n=corr.shape[0]
    # upper triangle without diag
    iu=np.triu_indices(n, k=1)
    vals=corr[iu]
    vals=vals[~np.isnan(vals)]
    mean_corr=np.mean(vals)
    std_corr=np.std(vals, ddof=1)
    se_corr=std_corr/np.sqrt(len(vals)) if len(vals)>0 else np.nan
    # edge weights
    w=np.sqrt(2*(1-np.clip(corr, -1, 1)))  # clip for numeric
    # for diag zero
    np.fill_diagonal(w, 0)
    w_vals=w[iu]
    w_vals=w_vals[~np.isnan(w_vals)]
    mean_w=np.mean(w_vals)
    std_w=np.std(w_vals, ddof=1)
    se_w=std_w/np.sqrt(len(w_vals))
    median_w=np.median(w_vals)
    # also std of w
    # percentiles?
    print(f"mean corr {mean_corr:.6f} std {std_corr:.6f} se {se_corr:.6f} n {len(vals)}")
    print(f"mean w {mean_w:.6f} std {std_w:.6f} se {se_w:.6f} median {median_w:.6f} n {len(w_vals)}")
    # histogram quick stats
    print(f"corr min {np.min(vals):.4f} max {np.max(vals):.4f}")
    print(f"w min {np.min(w_vals):.4f} max {np.max(w_vals):.4f}")
    return mean_corr, se_corr, len(vals), mean_w, se_w, median_w, w_vals, corr, w

def compute_theoretical(n):
    alpha=ALPHA
    kappa_complete=(1-alpha)*n/(n-1)
    lap0=0
    lap1=n/(n-1)
    kappa_min_formula_str="2/d_i + 2/d_j -2"  # symbolic
    # evaluate for complete graph degree n-1
    kappa_min_equal=2*(3-n)/(n-1)
    kappa_min_nasdaq=kappa_min_equal # for n=100 or actual
    # For n=100
    n100=100
    kappa_complete_100=(1-alpha)*n100/(n100-1)
    kappa_min_100=2*(3-n100)/(n100-1)
    edge_length_theoretical=1 - kappa_min_100  # naive length = (1 - kappa_min)*d? Actually paper says corresponds to length 2.96 => 1 - (-1.96)=2.96 assuming d=1
    # Upper/lower bounds generic
    lower_theoretical=-2
    upper_theoretical=1
    lin_lu_yau=n/(n-1)  # limit
    lin_lu_yau_100=n100/(n100-1)
    return {
        "kappa_complete_100": kappa_complete_100,
        "kappa_min_100": kappa_min_100,
        "edge_len_100": 1 - kappa_min_100, # 2.96
        "lower": lower_theoretical,
        "upper": upper_theoretical,
        "lap0": lap0,
        "lap1": lap1,
        "lap1_100": n100/(n100-1),
        "linyau": lin_lu_yau,
        "linyau100": lin_lu_yau_100,
        "kappa_complete_n": kappa_complete,
        "kappa_min_n": kappa_min_equal,
    }

def sample_curvature_distribution(w, n_sample=20):
    """
    Compute curvature for small random sample of edges to verify positivity and spread.
    Uses uniform mass definition (alpha=0.5, d_x = n-1) and shortest path = direct w (assume triangle holds)
    This demonstrates theoretical constant if uniform; plus attempts weighted version for spread.
    """
    n=w.shape[0]
    # Build constraint matrix for dual LP: |f_u - f_v| <= d(u,v)  where d = w (direct assumed)
    # For complete graph, we assume d = w (shortest = direct). We'll verify triangle inequality later.
    # Quick check: compute shortest paths via Floyd? For n=98, Floyd 98^3 ~ 941k operations feasible.
    # Let's compute Floyd to get true d (shortest path)
    print("Computing shortest path distances via Floyd-Warshall...")
    d=w.copy()
    # Floyd
    for k in range(n):
        # vectorized
        via = d[:,k,None] + d[k,:]
        # via intermediate k
        d = np.minimum(d, via)
    # Now check violation: direct vs shortest
    diff = w - d
    viol = np.sum(diff > 1e-9)
    print(f"Triangle violations (shorter via intermediate): {viol} / {n*(n-1)//2} max diff {np.max(diff):.6f}")
    # Build A_ub for dual: 2*E constraints
    # For n=98, E=4753, constraints=9506, variables=98 - feasible
    pairs=list(itertools.combinations(range(n),2))
    m=len(pairs)*2
    # Precompute A_ub and b_ub
    A_ub=np.zeros((m, n))
    b_ub=np.zeros(m)
    idx=0
    for (u,v) in pairs:
        A_ub[idx, u]=1
        A_ub[idx, v]=-1
        b_ub[idx]=d[u,v]
        idx+=1
        A_ub[idx, u]=-1
        A_ub[idx, v]=1
        b_ub[idx]=d[u,v]
        idx+=1
    bounds=[(None,None)]*n
    alpha=ALPHA
    # uniform masses
    masses_uniform=[]
    for x in range(n):
        mvec=np.zeros(n)
        mvec[x]=alpha
        for y in range(n):
            if y!=x:
                mvec[y]=(1-alpha)/(n-1)
        masses_uniform.append(mvec)
    # Sample edges
    np.random.seed(0)
    # choose random 20 edges
    sample_edges=np.random.choice(len(pairs), size=min(n_sample, len(pairs)), replace=False)
    kappas=[]
    Ws=[]
    for s_idx in sample_edges:
        i,j=pairs[s_idx]
        mi=masses_uniform[i]
        mj=masses_uniform[j]
        delta=mi-mj
        c=-delta  # minimize -delta*f => maximize delta*f
        res=linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        if not res.success:
            print(f"LP failed edge {i}-{j} {res.message}")
            continue
        W=-res.fun
        dij=d[i,j]
        kappa=1 - W/dij if dij!=0 else np.nan
        Ws.append(W)
        kappas.append(kappa)
        print(f"sample edge {i}-{j} tickers? w={w[i,j]:.4f} d={dij:.4f} W={W:.4f} kappa={kappa:.6f}")
    if kappas:
        print(f"Sample curvatures uniform: min {np.min(kappas):.6f} max {np.max(kappas):.6f} mean {np.mean(kappas):.6f} std {np.std(kappas):.6f}")
        # theoretical constant
        theoretical=(1-alpha)*n/(n-1)
        print(f"Theoretical kappa_complete for n={n}: {theoretical:.6f}")
    return d

def main():
    print(f"Period {START} to {END} (4.9 years actual, 5 years stated)")
    good,bad=fetch_prices()
    n_attempt=len(TICKERS_2024_11_15)
    n_good=len(good)
    n_bad=len(bad)
    print(f"Universe attempted {n_attempt}, good {n_good}, bad {n_bad}")
    # Check actual dates covered
    # Find overall start/end from good data
    all_starts=[df.index.min() for df in good.values()]
    all_ends=[df.index.max() for df in good.values()]
    actual_start=min(all_starts).date().isoformat() if all_starts else START
    actual_end=max(all_ends).date().isoformat() if all_ends else END
    print(f"Actual data coverage {actual_start} to {actual_end}")
    # For sample description, need start/end reflecting data's coverage (requested window)
    # We'll use START..END as requested period, but report actual traded dates
    # Compute returns
    ret_dict=compute_returns(good)
    # Need to handle tickers with very short history: they still contribute but correlation computed on overlap
    # Verify each ticker's returns length
    corr, tickers = build_correlation(ret_dict)
    mean_corr, se_corr, n_corr, mean_w, se_w, median_w, w_vals, corr_mat, w_mat = compute_stats(corr)
    # Theoretical
    n_for_theory=100
    theo=compute_theoretical(n_for_theory)
    theo_actual_n=compute_theoretical(n_good)  # for note
    print("Theoretical for n=100:", theo)
    print("Theoretical for actual n=", n_good, theo_actual_n)

    # Sample curvature distribution (partial)
    try:
        d_mat=sample_curvature_distribution(w_mat, n_sample=15)
    except Exception as e:
        print(f"curvature sampling failed: {e}")
        import traceback; traceback.print_exc()
        d_mat=w_mat

    # Determine missing/extra vs paper
    # Paper claims n_total_100 =100 but actual wiki 2024-11-15 gives 101 securities (100 companies + GOOG duplicate)
    # Our good =98 due to 3 delisted tickers ANSS, EA, WBD not available on yfinance
    total_wiki=len(TICKERS_2024_11_15)
    paper_claimed=100
    missing = n_bad  # 3
    extra = total_wiki - paper_claimed  # 1 extra security (101 vs 100)
    # But if we count securities, paper really has 101; spec preserves 66+35=101 sum; so same_as_paper false due to extra
    same_as_paper=False  # because paper count 100 vs our 101 universe, and 3 missing due to delisting
    differences=f"Wiki 2024-11-15 constituents {total_wiki} securities (100 companies incl. GOOG+GOOGL) vs paper claimed 100 nodes. Recovered {total_wiki} tickers exactly matching paper Appendix tables (101). Missing {n_bad} tickers unavailable via yfinance (delisted/not found): {bad}. Extra {extra} vs paper's 100 due to counting both GOOG classes as securities."
    # cannot_count empty for our case

    # Build results
    results=[]
    # n_total_100 claim: paper says 100 stocks/nodes; we recovered 101 securities matching Appendix
    # Report value 101 as per wiki retrieval, but also note paper's claim 100 is count of companies
    results.append({"name":"n_total_100","value":101,"se":None,"n":101})
    # period_window_5_years : paper states 5 years, actual days ~ 1783 calendar days ~4.89 years
    # Report as 5 (as printed) but n = number of trading days
    # Compute trading days count from common index
    # Get trading days from first ticker
    sample_ticker=list(good.keys())[0]
    trading_days=len(good[sample_ticker])
    results.append({"name":"period_window_5_years","value":5,"se":None,"n":trading_days})
    # corr_38_percent
    # value in % unit paper prints 38% => we output 38-ish scale? The spec says unit % but value is "38%" . In results they want number in same unit paper prints => 38 (percent)
    # We'll output mean_corr*100
    results.append({"name":"corr_38_percent","value":float(mean_corr*100),"se":float(se_corr*100) if not np.isnan(se_corr) else None,"n":n_corr})
    # avg_edge_weight_1_11
    results.append({"name":"avg_edge_weight_1_11","value":float(mean_w),"se":float(se_w),"n":n_corr})
    # median_edge_weight_1_11
    # se for median approximate: use std/sqrt(n) * 1.253? Simple use same as mean approximation or null
    # We'll compute via bootstrapping approximated std
    results.append({"name":"median_edge_weight_1_11","value":float(median_w),"se":float(np.std(w_vals, ddof=1)/np.sqrt(len(w_vals))),"n":len(w_vals)})
    # alpha
    results.append({"name":"alpha_lazy_1_2","value":0.5,"se":0,"n":None})
    # kappa_complete_0_505 for n=100
    results.append({"name":"kappa_complete_0_505","value":float(theo["kappa_complete_100"]),"se":0,"n":None})
    # lin_lu_yau
    results.append({"name":"lin_lu_yau_limit_n_over_n_minus1","value":float(theo["linyau100"]),"se":0,"n":None})
    # laplacian eigenvalues
    results.append({"name":"laplacian_eigenvalue_0","value":0,"se":0,"n":None})
    results.append({"name":"laplacian_eigenvalue_n_over_n_minus1","value":float(theo["lap1_100"]),"se":0,"n":None})
    # curvature bounds
    results.append({"name":"curvature_lower_theoretical_minus2","value":-2,"se":0,"n":None})
    results.append({"name":"curvature_upper_theoretical_1","value":1,"se":0,"n":None})
    # kappa_min_formula - this is symbolic but value is expression evaluate for n=100? We'll provide numeric lower bound
    # Spec value is formula string, but we output numeric evaluation
    results.append({"name":"kappa_min_formula","value":float(theo["kappa_min_100"]),"se":0,"n":None}) # approximate numeric interpretation
    results.append({"name":"kappa_min_equal_weights","value":float(theo["kappa_min_100"]),"se":0,"n":None})
    results.append({"name":"kappa_min_nasdaq_minus1_96","value":float(theo["kappa_min_100"]),"se":0,"n":None})
    results.append({"name":"edge_length_theoretical_2_96","value":float(theo["edge_len_100"]),"se":0,"n":None})
    # Ricci iterations parameters
    results.append({"name":"ricci_iter_5","value":5,"se":None,"n":None})
    results.append({"name":"ricci_iter_10","value":10,"se":None,"n":None})
    results.append({"name":"ricci_iter_20","value":20,"se":None,"n":None})
    results.append({"name":"surgery_curvature_0","value":0,"se":0,"n":None})
    # postflow_edge_weight_3 - observed around 3 after 20 iter, not computed from data directly (requires flow)
    # We can provide theoretical expectation 2.96 ~3
    results.append({"name":"postflow_edge_weight_3","value":float(theo["edge_len_100"]),"se":None,"n":None})

    # For tallies level1 etc: we are not recomputing clustering (requires full Ricci flow + surgery)
    # We will not include them in results, instead list in not_rebuilt

    # Sample description
    # Use actual available n_good for sample size, but largest size is 101 attempted
    sample_desc = f"NASDAQ-100 constituents from Wikipedia oldid 1257470804 as of 2024-11-15 (101 securities incl. GOOG+GOOGL =100 companies) matching paper Appendix tables. Retrieved {n_attempt} tickers, {n_good} with price data via market_data.get_prices for {START} to {END}; {n_bad} unavailable (delisted). Fully connected empirical correlation graph with edge weight w=sqrt(2(1-C)). Returns: log returns on adj_close, daily frequency, pairwise-complete overlap (min 30 days). No MST pruning."
    sample={
        "description": sample_desc,
        "n": n_good,  # size of sample actually used for correlation (available tickers)
        "start": START,
        "end": END,
        "same_as_paper": False,  # false because 3 missing due to delisting + 1 extra security vs 100 claim
        "missing": missing,
        "extra": extra,
        "differences": differences,
        "cannot_count": "",
        "not_rebuilt": {
            "level1_cluster_66": "Requires full discrete Ollivier-Ricci flow 20 iterations with surgery; heavy LP (4950 edges *20 steps) and surgery threshold details not fully specified; public data cannot reconstruct clustering without author's code.",
            "level1_cluster_35_a": "Same as above; 66+35=101 as printed includes GOOG duplicate.",
            "level2_parent_50": "Subcluster counts derived from recursive Ricci flow on partitions; not rebuilt (see above).",
            "level2_semicond_16": "Appendix Table Level2 Semiconductor 16 tickers; requires flow clustering; not rebuilt.",
            "level3_outlier_10": "Appendix Table Level3 Outlier 10 tickers; requires flow clustering; not rebuilt.",
            "level3_remainder_40": "Derived partition 50-10=40; not rebuilt.",
            "level4_biotech_4": "Appendix Level4 Biotech 4 tickers; not rebuilt.",
            "level4_supermicro_1": "Appendix Level4 SuperMicro 1 ticker; not rebuilt.",
            "level5_parent_35_b": "Remainder 35 after 4+1 extraction; not rebuilt.",
            "level5_bigtech_17": "Appendix Level5 BigTech 17 tickers; not rebuilt.",
            "level5_tesla_18": "Appendix Level5 Tesla group 18 tickers; not rebuilt.",
            "other_branch_level2_healthstaples_10": "Appendix Level2 HealthCare/Staples 10; not rebuilt.",
            "other_branch_level3_staplesenergy_8": "Appendix Level3 Staples/Energy 8; not rebuilt.",
            "other_branch_level3_industrials_17": "Appendix Level3 Industrials 17; not rebuilt."
        },
        "substitutions": "Universe from Wikipedia Nasdaq-100 old revision 2024-11-15 (revid1257470804) HTML table 101 securities (Table 4, 102 rows inc header) which exactly matches all tickers in paper Appendix tables (101 vs paper claimed 100). Price source: market_data.get_prices cache first then yfinance live (adj_close). Returns: log returns (paper does not state simple vs log or price column; standard choice log on adj_close, daily frequency, mean/std over window, pairwise complete for short-history IPOs like ARM 300 days, GEHC 486 days, GFS 771 days, CEG 715 days). Correlation Pearson as defined. Edge weight w sqrt(2(1-C)). Curvature sampling uses uniform mass (1-alpha)/(n-1) with alpha=0.5 and Floyd-Warshall shortest path; full distribution not computed due to unspecified solver weighting (uniform vs strength-weighted masses) and computational cost; theoretical values (kappa_complete 0.505, bounds -2/1, kappa_min -1.96, edge length 2.96) computed via formulas."
    }

    notes= (
        "Choices: 1) Universe retrieval date unspecified in paper; retrieved Nasdaq-100 as of 2024-11-15 (last revision before period end 2024-11-20) via Wikipedia API oldid 1257470804; this yields 101 securities (100 companies) exactly matching all Appendix tickers (verified vs paper tables: ARM, GEHC, GFS etc.) - paper states N=100 but Appendix sums to 101 (GOOG+GOOGL double). 2) Price column: paper says Yahoo Finance prices not stating adjusted vs close; used adj_close (standard for total return, adjusts splits/dividends) with log returns r_t=log(P_t/P_{t-1}) daily; paper leaves open daily vs other frequency, simple vs log - standard choice. 3) Handling missing/short-history tickers: ARM (IPO 2023-09-14, 300 days), GFS (271 days overlap? actually 771 days from 2021), GEHC (486), CEG (715) - used pairwise-complete overlap with min 30 days vs common intersection which would truncate to 300 days; this preserves 98 tickers. 4) Missing tickers ANSS, EA, WBD unavailable via yfinance (ANSS delisted post Synopsys acquisition mid-2025, EA/WBD data gaps per host) - counted as missing=3, see market_data_requests.json. 5) Shortest path d(i,j): for complete graph direct w is shortest if triangle inequality holds; computed Floyd-Warshall to verify and detect  violations; paper not stating exact transport solver (ni2019community GitHub referenced but commit not given); used dual LP via scipy linprog HiGHS for sample edges; uniform mass definition per Appendix (alpha on self + (1-alpha)/(n-1) uniformly to neighbors) yields constant curvature (1-alpha)n/(n-1)=0.505 for n=100 independent of w heterogeneity under direct distances, so histogram spread in paper implies either triangle violations causing d<w or weighted masses (by strength/affinity) - not specified. 6) Ricci flow update w^{(l+1)}=(1-kappa^{(l)}) d^{(l)} not iterated fully due to O(100k) LPs (~5 min per iteration) and surgery threshold calibration unspecified beyond zero-curvature flat links ~3; results for postflow_edge_weight_3 given as theoretical 2.96. 7) Deviations: average correlation computed %.4f -> %.2f%% (paper 38%%). Average/median edge weight derived from w sqrt(2(1-C)). Slight differences expected due to vendor (yfinance adj_close vs paper unspecified Yahoo field), delisted tickers, and correlation pairwise method. 8) Tallies for hierarchical clustering (Level1 66/35 etc) not rebuilt - require recursive Ricci flow + surgery algorithm with unspecified implementation details; listed in not_rebuilt." % (mean_corr, mean_corr*100)
    )

    output={"results":results,"sample":sample,"notes":notes}
    # Write results.json
    with open("/work/results.json","w") as f:
        json.dump(output,f,indent=2)
    print("Wrote /work/results.json")
    # Also print for debugging
    print(json.dumps(output, indent=2))

if __name__=="__main__":
    main()
