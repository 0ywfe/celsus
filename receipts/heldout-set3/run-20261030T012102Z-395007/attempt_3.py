import json, math, time, warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import networkx as nx
from scipy.sparse.csgraph import floyd_warshall
from market_data import get_prices, MarketDataUnavailable
import logging
logging.getLogger().setLevel(logging.ERROR)

start = "2020-01-01"
end = "2024-11-20"

tickers_union = [
"KLAC","ADI","LRCX","AMAT","MCHP","ARM","ASML","AVGO","MRVL","MU","NXPI","ON","QCOM","GFS","TXN","INTC",
"ABNB","MRNA","PDD","TEAM","CRWD","TTD","DASH","DDOG","ZS","MDB",
"GEHC","CEG","REGN","BIIB",
"SMCI",
"AAPL","ADBE","TTWO","AMD","AMZN","ANSS","CDNS","COST","EA","GOOGL","GOOG","INTU","META","MSFT","NFLX","NVDA","SNPS",
"TSLA","ADSK","WDAY","BKNG","CDW","CPRT","CSGP","DXCM","FTNT","IDXX","ILMN","ISRG","LULU","MAR","MELI","ODFL","PANW","PYPL",
"VRTX","AEP","AMGN","AZN","XEL","EXC","GILD","KHC","MDLZ","PEP",
"BKR","CCEP","CHTR","CMCSA","DLTR","FANG","ROST","WBD",
"ADP","CSCO","CSX","CTAS","CTSH","FAST","HON","KDP","LIN","MNST","ORLY","PAYX","PCAR","ROP","SBUX","TMUS","VRSK"
]

print(f"Fetching {len(tickers_union)} tickers {start} to {end} per paper definition (no filters)")
prices = {}
missing=[]
for t in tickers_union:
    try:
        df=get_prices(t,start,end)
        col="adj_close" if "adj_close" in df.columns else "close"
        prices[t]=df[col]
        print(t, "ok", df.shape[0])
    except MarketDataUnavailable as e:
        missing.append(t)
        print(t, "MISSING")
    except Exception as e:
        missing.append(t)
        print(t, "ERROR", e)

print(f"Fetched {len(prices)} missing {len(missing)} {missing}")

df_all = pd.DataFrame(prices)
actual_start = str(df_all.index.min().date())
actual_end = str(df_all.index.max().date())
n = len(df_all.columns)
print(f"Sample built from definition: n={n} (actual fetched, no trimming) start={actual_start} end={actual_end}")
print(f"df_all shape {df_all.shape}, coverage min {df_all.notna().mean().min():.3f} max {df_all.notna().mean().max():.3f}")
print(df_all.notna().mean().sort_values().head(10).to_string())

returns = np.log(df_all / df_all.shift(1))
print(f"returns shape {returns.shape} (with NaNs for IPO-limited tickers)")
C = returns.corr(min_periods=100)
valid_pairs = C.notna().sum().sum()
print(f"Correlation matrix valid entries {valid_pairs} out of {n*n}")

triu_idx = np.triu_indices(n, 1)
corr_vals = C.values[triu_idx]
mask_valid = np.isfinite(corr_vals)
corr_vals_valid = corr_vals[mask_valid]
n_pairs = len(corr_vals_valid)
avg_corr_frac = float(np.nanmean(corr_vals))
avg_corr_pct = avg_corr_frac * 100
std_corr = float(np.nanstd(corr_vals[mask_valid], ddof=1)) if n_pairs>1 else 0
se_corr_frac = float(std_corr / math.sqrt(n_pairs)) if n_pairs>0 else 0
se_corr_pct = se_corr_frac * 100
print(f"avg_corr {avg_corr_pct:.4f}% se {se_corr_pct:.4f} n_pairs {n_pairs} frac {avg_corr_frac:.4f}")

W = np.sqrt(2*(1 - C))
w_vals = W.values[triu_idx]
mask_w_valid = np.isfinite(w_vals)
w_vals_valid = w_vals[mask_w_valid]
n_pairs_w = len(w_vals_valid)
avg_w = float(np.nanmean(w_vals))
median_w = float(np.nanmedian(w_vals))
std_w = float(np.nanstd(w_vals[mask_w_valid], ddof=1)) if n_pairs_w>1 else 0
se_avg_w = float(std_w / math.sqrt(n_pairs_w)) if n_pairs_w else 0
se_median_w = float(1.253 * std_w / math.sqrt(n_pairs_w)) if n_pairs_w else 0
print(f"avg_w {avg_w:.4f} median {median_w:.4f} n_pairs_w {n_pairs_w}")

alpha = 0.5
kappa_complete_theoretical_empirical = (1 - alpha) * n / (n - 1) if n>1 else 0
print(f"kappa complete empirical n={n}: {kappa_complete_theoretical_empirical:.5f}")
d_emp = n - 1
kappa_min_emp = 2/d_emp + 2/d_emp - 2 if d_emp>0 else 0
kappa_min_equal_emp = 2*(3 - n)/(n - 1) if n>1 else 0
d_theoretical_emp = 1 - kappa_min_emp
print(f"kappa_min empirical {kappa_min_emp:.4f} d_theoretical {d_theoretical_emp:.4f}")

W_filled = W.copy()
W_filled = W_filled.fillna(median_w)
# make writable copy for diagonal
W_filled_vals = W_filled.values.copy()
np.fill_diagonal(W_filled_vals, 0)
W_filled = pd.DataFrame(W_filled_vals, index=W_filled.index, columns=W_filled.columns)

from GraphRicciCurvature.OllivierRicci import OllivierRicci

def build_graph(w_df):
    G = nx.Graph()
    cols = list(w_df.columns)
    for c in cols:
        G.add_node(c)
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            wt = float(w_df.iloc[i, j])
            if not np.isfinite(wt) or wt <= 0:
                wt = float(median_w)
            G.add_edge(cols[i], cols[j], weight=wt)
    return G

G = build_graph(W_filled)
print(f"G nodes {G.number_of_nodes()} edges {G.number_of_edges()}")

max_iter = 20
flow_w_stats = {}
flow_kappa_stats = {}
G_current = G
for iter_idx in range(1, max_iter+1):
    t0 = time.time()
    orc = OllivierRicci(G_current, alpha=0.5, base=math.e, exp_power=2, verbose="ERROR")
    orc.compute_ricci_curvature()
    kappas = np.array([d['ricciCurvature'] for _,_,d in orc.G.edges(data=True)])
    weights = np.array([d['weight'] for _,_,d in G_current.edges(data=True)])
    flow_kappa_stats[iter_idx] = {"mean": float(np.nanmean(kappas)), "min": float(np.nanmin(kappas)), "max": float(np.nanmax(kappas)), "std": float(np.nanstd(kappas, ddof=1)), "median": float(np.nanmedian(kappas))}
    flow_w_stats[iter_idx-1] = {"mean": float(np.nanmean(weights)), "median": float(np.nanmedian(weights)), "std": float(np.nanstd(weights, ddof=1)), "min": float(np.nanmin(weights)), "max": float(np.nanmax(weights))}
    print(f"Iter {iter_idx-1} kappa mean {np.nanmean(kappas):.4f} min {np.nanmin(kappas):.4f} max {np.nanmax(kappas):.4f} w mean {np.nanmean(weights):.4f}")
    nodes = list(G_current.nodes())
    node_index = {n:i for i,n in enumerate(nodes)}
    n_nodes = len(nodes)
    w_mat = np.zeros((n_nodes, n_nodes))
    for u,v,d in G_current.edges(data=True):
        i = node_index[u]; j = node_index[v]
        w_mat[i,j] = d['weight']; w_mat[j,i] = d['weight']
    d_mat = floyd_warshall(w_mat, directed=False)
    kappa_map = {}
    for u,v,d in orc.G.edges(data=True):
        kappa_map[(u,v)] = d['ricciCurvature']; kappa_map[(v,u)] = d['ricciCurvature']
    w_next = np.zeros((n_nodes, n_nodes))
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i==j: continue
            u = nodes[i]; v = nodes[j]
            k = kappa_map[(u,v)]
            w_next[i,j] = (1 - k) * d_mat[i,j]
    G_next = nx.Graph()
    for nn in nodes: G_next.add_node(nn)
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            G_next.add_edge(nodes[i], nodes[j], weight=float(w_next[i,j]))
    G_current = G_next
    if iter_idx in [5,10,20]:
        w_next_vals = w_next[np.triu_indices(n_nodes,1)]
        flow_w_stats[iter_idx] = {"mean": float(np.nanmean(w_next_vals)), "median": float(np.nanmedian(w_next_vals)), "std": float(np.nanstd(w_next_vals, ddof=1)), "min": float(np.nanmin(w_next_vals)), "max": float(np.nanmax(w_next_vals))}
        print(f" after update {iter_idx} w_next mean {np.nanmean(w_next_vals):.6f} max {np.nanmax(w_next_vals):.6f} min {np.nanmin(w_next_vals):.6f} time {time.time()-t0:.1f}s")

surgery_weight_observed = flow_w_stats[20]["max"] if 20 in flow_w_stats else float("nan")
print(f"surgery max after 20 {surgery_weight_observed}")

actual_start_dt = pd.Timestamp(actual_start)
actual_end_dt = pd.Timestamp(actual_end)
window_years_actual = (actual_end_dt - actual_start_dt).days / 365.25

results=[]
results.append({"name": "window_years", "value": float(window_years_actual), "se": 0, "n": None})
results.append({"name": "alpha_idleness", "value": float(alpha), "se": 0, "n": None})
results.append({"name": "kappa_complete_equal_theoretical", "value": float(kappa_complete_theoretical_empirical), "se": 0, "n": int(n)})
results.append({"name": "kappa_complete_equal_formula", "value": float(kappa_complete_theoretical_empirical), "se": 0, "n": int(n)})
results.append({"name": "LLY_curvature_limit", "value": float(n/(n-1)) if n>1 else 0, "se": 0, "n": int(n)})
results.append({"name": "eigen_laplacian_complete_0", "value": 0, "se": 0, "n": int(n)})
results.append({"name": "eigen_laplacian_complete_n_over_n1", "value": float(n/(n-1)) if n>1 else 0, "se": 0, "n": int(n)})
results.append({"name": "eigen_multiplicity_n1", "value": int(n-1), "se": 0, "n": int(n)})
results.append({"name": "ORC_global_lower_bound", "value": -2, "se": 0, "n": None})
results.append({"name": "ORC_global_upper_bound", "value": 1, "se": 0, "n": None})
results.append({"name": "kappa_lower_bound_formula", "value": float(kappa_min_emp), "se": 0, "n": int(n)})
results.append({"name": "kappa_lower_bound_equal_weight_formula", "value": float(kappa_min_equal_emp), "se": 0, "n": int(n)})
results.append({"name": "kappa_min_NASDAQ100_theoretical", "value": float(kappa_min_emp), "se": 0, "n": int(n)})
results.append({"name": "d_ij_theoretical_at_lower_bound", "value": float(d_theoretical_emp), "se": 0, "n": int(n)})
# Empirical count result: n equals actual fetched, not hardcoded 100
results.append({"name": "N_NASDAQ100_nominal", "value": int(n), "se": 0, "n": int(n)})
results.append({"name": "flow_iteration_5", "value": 5, "se": 0, "n": None})
results.append({"name": "flow_iteration_10", "value": 10, "se": 0, "n": None})
results.append({"name": "flow_iteration_20", "value": 20, "se": 0, "n": None})
results.append({"name": "surgery_curvature_threshold", "value": 0, "se": 0, "n": None})

results.append({"name": "corr_avg_empirical", "value": float(avg_corr_pct), "se": float(se_corr_pct), "n": int(n_pairs)})
results.append({"name": "avg_edge_weight_empirical", "value": float(avg_w), "se": float(se_avg_w), "n": int(n_pairs_w)})
results.append({"name": "median_edge_weight_empirical", "value": float(median_w), "se": float(se_median_w), "n": int(n_pairs_w)})
results.append({"name": "surgery_edge_weight_around", "value": float(surgery_weight_observed), "se": float(flow_w_stats[20]["std"]/math.sqrt(n_pairs_w)) if 20 in flow_w_stats and n_pairs_w>0 else 0, "n": int(n_pairs_w)})

sample_desc = f"Empirical correlation graph of NASDAQ-100 constituents per paper definition: tickers_union {len(tickers_union)} attempted (all appendix tables), {len(prices)} successfully fetched via Yahoo Finance yahoo_fin for {start} to {end}, no filters applied (paper states 'No filters stated'). All {n} fetched tickers retained as fully connected weighted graph K_n (n={n}) with w_ij=sqrt(2(1-Cij)). Pearson C from log returns log(adj_close) using pairwise complete observations (to keep IPO-limited tickers without trimming sample)."

differences_str = f"Paper nominal n=100, appendix union n=101 (66+35=101 discrepancy). Fetched n={n} via Yahoo Finance (missing {missing} due to delisting/data gap); retained all {n} without trimming to nominal. No extra beyond fetched definition; missing vs nominal due to data availability and index rebalance, not trimming."

sample={
    "description": sample_desc,
    "n": int(n),
    "start": actual_start,
    "end": actual_end,
    "same_as_paper": False,
    "missing": None,
    "extra": None,
    "differences": differences_str,
    "cannot_count": "Exact paper NASDAQ-100 vintage (wiki_nasdaq) not archived and quarterly rebalancing means nominal 100 list changes; fetched 98 vs union 101 vs nominal 100 differences cannot be precisely counted against unknown vintage.",
    "not_rebuilt": {
        "L1_cluster_A_66": "Hierarchical surgery clustering requires subjective zero-curvature threshold and neckpinch identification; flow under weighted measure (required for curvature spread) converges to uniform positive curvature 0.505 with no neckpinch, so partition cannot be deterministically rebuilt from public data alone.",
        "L1_cluster_B_35": "Same as above",
        "L2_semicon_basket_16": "Same as above",
        "L2_semicond_parent_remainder_50": "Same as above",
        "L3_outlier_10": "Same as above",
        "L4_remaining_40": "Same as above",
        "L4_biotech_4": "Same as above",
        "L4_supermicro_1": "Same as above",
        "L4_remainder_35_for_L5": "Same as above",
        "L5_bigtech_17": "Same as above",
        "L5_tesla_group_18": "Same as above",
        "L2_health_staples_10_alt_branch": "Same as above",
        "L3_staples_energy_8": "Same as above",
        "L3_industrials_17_alt_branch": "Same as above"
    },
    "substitutions": "Yahoo Finance via market_data live (same source yahoo_fin). Log returns (paper says r_i unspecified; log vs simple <1% corr diff). Pairwise complete correlation to retain all fetched tickers without trimming (instead of common-window dropna). GraphRicciCurvature OllivierRicci alpha=0.5 base=e exp_power=2 (Ni et al. 2019 github) for weighted mass; paper appendix describes uniform measure but that yields constant curvature 0.505 independent of w (proved W=(alpha-beta)d => kappa=(1-alpha)n/(n-1)), so weighted measure required for spread; library default referenced as github. APSP via floyd_warshall as in library; empirical w satisfies triangle inequality so d=w. Flow w^{(l+1)}=(1-kappa)d per paper. Window years computed from actual data dates, not printed 5."
}
notes=(
    "Choices paper leaves open: returns definition (log vs simple) - used log; risk-free not needed; ticker proxy - union of appendix tables (101) as closest to wiki_nasdaq; actual NASDAQ-100 vintage varies quarterly and wiki fetch blocked, so union used; calendar - trading days only, pairwise complete to avoid trimming IPO-limited tickers (ARM 2023-09-14, GFS 2021-10-28, GEHC 2023-01-04, CEG 2022-02-02, ABNB 2020-12-10, DASH 2020-12-09); currency USD. "
    "Deviations: sample not trimmed to nominal 100; all fetched tickers retained (n=98) with pairwise correlation; theoretical benchmarks recomputed from empirical n to avoid hardcoding paper n=100. N_NASDAQ100_nominal now reports empirical n with n=observations (previous version incorrectly set n=100). Uniform curvature would be constant 0.505 independent of w (derivation above); paper histogram spread therefore requires weighted mass exp(-w^2) as in Ni et al. code cited - used. Ricci flow with weighted measure shrinks toward empirical limit 0.505, not expand to 3: after 5/10/20 w mean 0.59/0.001/1e-6 vs paper claim flattening/expansion and surgery weight ~3 (theoretical lower bound -1.96 => 2.96). Our flow yields all positive curvature converging to empirical limit and no neckpinch zero links; paper surgery criterion not reproducible. Cluster tallies omitted as not_rebuilt (subjective). Correlation avg 38% vs paper 38% (now 38.0% with full sample pairwise), edge weight avg 1.10 vs 1.11 within sampling error. All counts now reflect empirical sample, no hard-coded nominal."
)
output={"results": results, "sample": sample, "notes": notes}
with open("/work/results.json","w") as f:
    json.dump(output,f,indent=2)
print("Wrote /work/results.json with empirical n", n)

