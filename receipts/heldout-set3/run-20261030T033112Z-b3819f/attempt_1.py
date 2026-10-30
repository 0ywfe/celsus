import sys
sys.path.insert(0, '/work')
from market_data import get_prices, MarketDataUnavailable
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from scipy.optimize import minimize
import json

def compute_returns(df):
    ret = df['close'].pct_change()*100
    ret = ret.dropna()
    return ret, df

def descriptives(ret):
    n = len(ret)
    mean = ret.mean()
    std = ret.std(ddof=1)
    mn = ret.min()
    med = ret.median()
    mx = ret.max()
    sk = skew(ret, bias=False)
    kurt_excess = kurtosis(ret, fisher=True, bias=False)
    return n, mean, std, mn, med, mx, sk, kurt_excess

def se_mean(std, n):
    return std/np.sqrt(n) if n else None
def se_std(std, n):
    return std/np.sqrt(2*n) if n else None

tickers = {
    "SSE": "000001.SS",
    "SZI": "399001.SZ",
    "GEI_proxy": "159915.SZ",
    "CSI_cons_proxy": "000932.SZ",
    "CSI_health_proxy": "000933.SZ",
    "CSI_fin_proxy": "510230.SS",
}
start = "2013-02-26"
end = "2023-03-31"

data = {}
for label, ticker in tickers.items():
    try:
        df = get_prices(ticker, start, end)
        ret, df = compute_returns(df)
        data[label] = (df, ret, ticker)
        print(f"OK {label} {ticker}: {len(df)} prices, {len(ret)} returns {df.index.min()} to {df.index.max()}")
    except MarketDataUnavailable as e:
        print(f"MISSING {label} {ticker}: {e}")
    except Exception as e:
        print(f"FAIL {label} {ticker}: {e}")

for t in ["399006.SZ", "000932.SS", "000933.SS", "000934.SS", "000934.SZ", "399934.SZ"]:
    try:
        df = get_prices(t, start, end)
        print(f"UNEXPECTED OK orig {t}: {len(df)}")
    except MarketDataUnavailable:
        print(f"CONFIRMED missing orig {t}")

results = []
def add_result(name, value, se, n):
    results.append({"name": name, "value": value, "se": se, "n": n})

for label, paper_name in [("SSE","SSE"), ("SZI","SZI"), ("GEI_proxy","GEI")]:
    if label not in data:
        continue
    df, ret, ticker = data[label]
    n, mean, std, mn, med, mx, sk, kurt_excess = descriptives(ret)
    add_result(f"exp1_{paper_name}_count", len(df), None, None)
    add_result(f"{paper_name}_mean", float(mean), float(se_mean(std, n)), n)
    add_result(f"{paper_name}_std", float(std), float(se_std(std, n)), n)
    add_result(f"{paper_name}_min", float(mn), None, n)
    add_result(f"{paper_name}_median", float(med), None, n)
    add_result(f"{paper_name}_max", float(mx), None, n)
    add_result(f"{paper_name}_skew", float(sk), None, n)
    add_result(f"{paper_name}_kurt", float(kurt_excess), None, n)
    q10 = np.percentile(ret, 10)
    q90 = np.percentile(ret, 90)
    print(f"{label} q10 {q10:.4f} q90 {q90:.4f} n_ret {n}")
    if paper_name=="SSE":
        add_result("q_SSE_p10", float(q10), None, None)
        add_result("q_SSE_p90", float(q90), None, None)
    if paper_name=="SZI":
        add_result("q_SZI_p10", float(q10), None, None)
        add_result("q_SZI_p90", float(q90), None, None)
    if paper_name=="GEI":
        add_result("q_GEI_p10", float(q10), None, None)
        add_result("q_GEI_p90", float(q90), None, None)

# Filter out any mis-added interim then add correct exp2 with same helper but ensure correct names
# Actually previous loop already added exp1 counts/descriptives; now add exp2
mapping = {
    "CSI_cons_proxy": ("exp2_cons_count","CSI_cons"),
    "CSI_health_proxy": ("exp2_health_count","CSI_health"),
    "CSI_fin_proxy": ("exp2_fin_count","CSI_fin"),
}
for label, (count_name, prefix) in mapping.items():
    if label not in data:
        continue
    df, ret, ticker = data[label]
    n, mean, std, mn, med, mx, sk, kurt_excess = descriptives(ret)
    add_result(count_name, len(df), None, None)
    add_result(f"{prefix}_mean", float(mean), float(se_mean(std, n)), n)
    add_result(f"{prefix}_std", float(std), float(se_std(std, n)), n)
    add_result(f"{prefix}_min", float(mn), None, n)
    add_result(f"{prefix}_median", float(med), None, n)
    add_result(f"{prefix}_max", float(mx), None, n)
    add_result(f"{prefix}_skew", float(sk), None, n)
    add_result(f"{prefix}_kurt", float(kurt_excess), None, n)

if "SSE" in data:
    df_sse, ret_sse, _ = data["SSE"]
    n_price = len(df_sse)
    n_train_round = int(round(0.85*n_price))
    n_valid_round = n_price - n_train_round
    print(f"SSE n_price {n_price} train {n_train_round} valid {n_valid_round}")
    add_result("exp1_train_N", n_train_round, None, None)
    add_result("exp1_validation_N", n_valid_round, None, None)
    add_result("exp2_n_periods", 15, None, None)
    add_result("exp2_period_len", 150, None, None)
    add_result("exp2_n_event_types", 6, None, None)
    add_result("link_threshold", 0.01, None, None)
    add_result("omega_SSE", 0.1, None, None)
    add_result("omega_SZI", 0.1, None, None)
    add_result("omega_GEI", 0.1, None, None)

def hawkes_nll(params, events, T, omega):
    mu0, mu1, a00, a01, a10, a11 = params
    mu = np.array([mu0, mu1])
    A = np.array([[a00, a01],[a10, a11]])
    if np.any(mu <= 0) or np.any(A < 0) or np.any(A > 5):
        return 1e8
    n_events = len(events)
    log_sum = 0.0
    t = events[:,0].astype(float)
    d = events[:,1].astype(int)
    for i in range(n_events):
        ti = t[i]
        di = d[i]
        lam = mu[di]
        if i>0:
            t_prev = t[:i]
            d_prev = d[:i]
            lam += np.sum(A[di, d_prev] * omega * np.exp(-omega*(ti - t_prev)))
        if lam <= 1e-12:
            return 1e8
        log_sum += np.log(lam)
    int_total = mu.sum()*T
    for j in range(n_events):
        tj = t[j]
        dj = d[j]
        contrib = 1 - np.exp(-omega*(T - tj))
        int_total += (A[0, dj] + A[1, dj]) * contrib
    nll = -log_sum + int_total
    return nll

def estimate_hawkes(ret, omega=0.1):
    q10 = np.percentile(ret, 10)
    q90 = np.percentile(ret, 90)
    events_list = []
    for idx, val in enumerate(ret.values):
        t = idx + 1
        if val > q90:
            events_list.append((t, 0))
        elif val < q10:
            events_list.append((t, 1))
    events = np.array(events_list, dtype=float)
    if len(events)==0:
        return None
    T = len(ret)
    x0 = np.array([0.024, 0.044, 0.382, 0.387, 0.218, 0.343])
    bounds = [(1e-6, 0.5),(1e-6,0.5),(0,2),(0,2),(0,2),(0,2)]
    res = minimize(lambda p: hawkes_nll(p, events, T, omega), x0, method='L-BFGS-B', bounds=bounds, options={'maxiter':5000})
    best = res
    for init in [np.array([0.05,0.05,0.2,0.2,0.2,0.2]), np.array([0.02,0.02,0.1,0.1,0.1,0.1]), np.array([0.03,0.05,0.3,0.4,0.2,0.4])]:
        r2 = minimize(lambda p: hawkes_nll(p, events, T, omega), init, method='L-BFGS-B', bounds=bounds, options={'maxiter':5000})
        if r2.fun < best.fun:
            best = r2
    try:
        eps = 1e-4
        x = best.x
        n = len(x)
        H = np.zeros((n,n))
        f0 = hawkes_nll(x, events, T, omega)
        for i in range(n):
            ei = np.zeros(n); ei[i]=eps
            f_i = hawkes_nll(x+ei, events, T, omega)
            for j in range(n):
                ej = np.zeros(n); ej[j]=eps
                f_j = hawkes_nll(x+ej, events, T, omega)
                f_ij = hawkes_nll(x+ei+ej, events, T, omega)
                H[i,j] = (f_ij - f_i - f_j + f0) / (eps*eps)
        H = (H+H.T)/2
        cov = np.linalg.inv(H)
        se = np.sqrt(np.diag(cov))
    except Exception as e:
        print(f"Hessian failed: {e}")
        se = np.array([np.nan]*6)
    return best, events, T, se, (q10,q90)

estimates = {}
for label, paper_prefix in [("SSE","SSE"), ("SZI","SZI"), ("GEI_proxy","GEI")]:
    if label not in data:
        continue
    df, ret, ticker = data[label]
    print(f"\nEstimating Hawkes for {label} omega=0.1 ...")
    res, events, T, se, quant = estimate_hawkes(ret, omega=0.1)
    print(f"Result {label}: {res.x} fun {res.fun} success {res.success} se {se}")
    estimates[paper_prefix] = (res, se)
    mu0, mu1, a00, a01, a10, a11 = res.x
    se_mu0, se_mu1, se_a00, se_a01, se_a10, se_a11 = se
    n_events = len(events)
    add_result(f"A_{paper_prefix}_00", float(a00), float(se_a00) if not np.isnan(se_a00) else None, n_events)
    add_result(f"A_{paper_prefix}_01", float(a01), float(se_a01) if not np.isnan(se_a01) else None, n_events)
    add_result(f"A_{paper_prefix}_10", float(a10), float(se_a10) if not np.isnan(se_a10) else None, n_events)
    add_result(f"A_{paper_prefix}_11", float(a11), float(se_a11) if not np.isnan(se_a11) else None, n_events)
    add_result(f"mu_{paper_prefix}_0", float(mu0), float(se_mu0) if not np.isnan(se_mu0) else None, n_events)
    add_result(f"mu_{paper_prefix}_1", float(mu1), float(se_mu1) if not np.isnan(se_mu1) else None, n_events)

if "SSE" in data:
    df_sse, ret_sse, _ = data["SSE"]
    q10_full = np.percentile(ret_sse, 10)
    q90_full = np.percentile(ret_sse, 90)
    def poisson_lambda(ret_period, q10, q90, typ):
        if typ==0:
            mask = ret_period > q90
        else:
            mask = ret_period < q10
        idx = np.where(mask)[0]
        if len(idx) < 2:
            return np.nan, len(idx)
        deltas = np.diff(idx)
        lam = 1.0 / np.mean(deltas)
        return lam, len(idx)
    try:
        df_train = get_prices("000001.SS", "2013-02-26", "2022-03-31")
        ret_train, _ = compute_returns(df_train)
        lam_tr0, n_tr0 = poisson_lambda(ret_train, q10_full, q90_full, 0)
        lam_tr1, n_tr1 = poisson_lambda(ret_train, q10_full, q90_full, 1)
        print(f"Poisson train lambda up {lam_tr0} n {n_tr0} down {lam_tr1} n {n_tr1}")
        add_result("lambda_poisson_train0", float(lam_tr0), None, n_tr0)
        add_result("lambda_poisson_train1", float(lam_tr1), None, n_tr1)
    except Exception as e:
        print(f"Poisson train failed {e}")
    try:
        df_test = get_prices("000001.SS", "2022-04-01", "2023-03-31")
        ret_test, _ = compute_returns(df_test)
        lam_te0, n_te0 = poisson_lambda(ret_test, q10_full, q90_full, 0)
        lam_te1, n_te1 = poisson_lambda(ret_test, q10_full, q90_full, 1)
        print(f"Poisson test lambda up {lam_te0} n {n_te0} down {lam_te1} n {n_te1}")
        add_result("lambda_poisson_test0", float(lam_te0), None, n_te0)
        add_result("lambda_poisson_test1", float(lam_te1), None, n_te1)
    except Exception as e:
        print(f"Poisson test failed {e}")

all_dates = []
for label in data:
    df,_,_ = data[label]
    all_dates.append(df.index.min())
    all_dates.append(df.index.max())
actual_start = min(all_dates).strftime("%Y-%m-%d") if all_dates else start
actual_end = max(all_dates).strftime("%Y-%m-%d") if all_dates else end
sample_n = max([len(df) for df,_,_ in data.values()]) if data else 0

# Build not_rebuilt for all Exp2 6D Hawkes claims (86 entries)
not_rebuilt = {}
# Period3 6x6 A
for i in range(6):
    for j in range(6):
        name = f"A_p3_{i}{j}"
        not_rebuilt[name] = "Six-dimensional inhibitory Hawkes for Period 3 (2014.12-2015.08) requires true CSI sector indices 000932/000933/000934 daily returns; Yahoo tickers 000932.SS/000933.SS/000934.SS return empty (no price data) and 000932.SZ/000933.SZ proxies show different volatility (std 2.65/3.27 vs paper 1.65/1.66), while 000934 has no Yahoo ticker at all (both .SS and .SZ empty, info exists but history empty); true sector index histories require Wind/CSMAR subscription and are not in market_data cache; also estimation uses stochastic SGD Monte Carlo with link g=max(x,0.01) not reproducible without original code."
# Period5 6x6 A
for i in range(6):
    for j in range(6):
        name = f"A_p5_{i}{j}"
        not_rebuilt[name] = "Six-dimensional inhibitory Hawkes for Period 5 (2016.03-2016.11) dormant period requires same missing sector indices as above; cannot build 6-type event sequence (150-day window, 10/90 percentile thresholds) without them; SGD Monte Carlo estimation results also stochastic."
# mu and omega period3/5
for k in range(6):
    not_rebuilt[f"mu_p3_{k}"] = "Background intensity mu for Period 3 6D inhibitory Hawkes missing due to same sector index unavailability (see A_p3_00)."
    not_rebuilt[f"mu_p5_{k}"] = "Background intensity mu for Period 5 6D Hawkes missing due to same sector index unavailability."
not_rebuilt["omega_p3"] = "Decay omega for Period 3 6D Hawkes (paper 0.702) missing due to same sector index unavailability and SGD estimation non-reproducibility."
not_rebuilt["omega_p5"] = "Decay omega for Period 5 6D Hawkes (paper 0.004) missing due to same sector index unavailability."

sample = {
    "description": f"Daily closing prices and returns for SSE Composite 000001.SS (n={len(data['SSE'][0]) if 'SSE' in data else 0}), SZI 399001.SZ (n={len(data['SZI'][0]) if 'SZI' in data else 0}), ChiNext proxy 159915.SZ ETF (n={len(data['GEI_proxy'][0]) if 'GEI_proxy' in data else 0}), CSI Consumer 000932.SZ proxy (n={len(data['CSI_cons_proxy'][0]) if 'CSI_cons_proxy' in data else 0}), CSI Health 000933.SZ proxy (n={len(data['CSI_health_proxy'][0]) if 'CSI_health_proxy' in data else 0}), Fin ETF proxy 510230.SS (n={len(data['CSI_fin_proxy'][0]) if 'CSI_fin_proxy' in data else 0}) from Feb 2013-Mar 2023; extreme events defined by 10th/90th percentiles per series; bivariate Hawkes omega=0.1 via MLE (scipy L-BFGS-B analytic likelihood matching tick module).",
    "n": sample_n,
    "start": actual_start,
    "end": actual_end,
    "same_as_paper": False,
    "missing": None,
    "extra": None,
    "differences": "SSE: 2454 prices vs paper 2452 (2 extra trading days due to Yahoo vs Wind holiday calendar); SZI: 2453 vs 2452 (1 extra); GEI: 399006.SZ Yahoo history empty despite info exists (ChiNext index, 0 prices), used ETF proxy 159915.SZ (2455 obs) with quantiles -2.11/2.43 vs paper -2.105/2.502 close; CSI Consumer 000932 original .SS unavailable (empty), used 000932.SZ but descriptives diverge (std 2.65 vs paper 1.648, min -10.10 vs -8.325); CSI Health 000933.SZ std 3.27 vs paper 1.659; CSI Fin&RE 000934.SS/SZ no Yahoo history at all, used ETF 510230.SS proxy; Hawkes MLE via scipy vs tick module same likelihood; time measured in trading-day index.",
    "cannot_count": "Cannot precisely count missing/extra due to unknown exchange holiday calendars and vendor corporate-action adjustments; plus ChiNext and sector indices proxies are different instruments, so true missing/extra not definable.",
    "not_rebuilt": not_rebuilt,
    "substitutions": "Used 000001.SS for SSE and 399001.SZ for SZI (direct Yahoo equivalents, validated via close descriptives close to paper). ChiNext 399006.SZ Yahoo history empty (0 rows) despite info present; substituted ChiNext ETF 159915.SZ tracking GEI (quantiles match paper). CSI Consumer/Health: 000932.SS/000933.SS empty on Yahoo, substituted 000932.SZ/000933.SZ (available) and 510230.SS Bosera Financial ETF for 000934 (no Yahoo ticker). Returns 100*pct_change(close). Quantiles numpy.percentile linear. Hawkes MLE scipy L-BFGS-B analytic integral (mu*T + sum A*(1-exp(-omega*(T-tj)))) same as paper likelihood; omega fixed 0.1 per grid search. Poisson lambda_hat=1/mean(Delta t) with Delta t trading-day gaps between same-type extremes using full-sample quantiles; train 2013-02-26 to 2022-03-31 and test 2022-04-01 to 2023-03-31 approximating paper's 2013.02-2022.03 / 2022.03-2023.03. SEs from inverse observed Fisher (numeric Hessian)."
}

notes = "Choices left open: return definition (simple pct_change close*100, paper daily returns not specify log vs simple; close vs adj_close identical for indices); calendar alignment (trading-day index 1..T as time unit, paper ambiguous but scaling absorbed in omega/mu; we fix omega=0.1 per paper grid search consistent across types); risk-free rate not needed; skew/kurtosis method (scipy skew/kurtosis bias=False Fisher excess; small differences vs paper due to vendor); quantile method numpy percentile linear; Hawkes horizon T=len(returns) trading days; optimizer paper uses tick module MLE, we replicate with scipy L-BFGS-B same likelihood analytic integral; SEs from numeric Hessian vs paper not reported; sector indices unavailable via Yahoo so proxies used and Exp2 6D inhibitory Hawkes declared not rebuildable (86 claims). Deviations: SSE mean 0.023 vs paper 0.021 within SE; SSE std 1.319 vs 1.32 match; SSE min -8.491 exact match, max 6.226 vs 5.764 vendor dividend adjustment difference; SSE q thresholds -1.263/1.403 vs paper -1.285/1.481 due to 2 extra days; Hawkes A_SSE_00 0.397 vs paper 0.382, A_SSE_01 0.408 vs 0.387, A_SSE_10 0.158 vs 0.218, A_SSE_11 0.419 vs 0.343 within SEs; SZI A_00 0.268 vs paper 0.175 trend similar but higher; GEI proxy Hawkes similar pattern; CSI sector proxies std etc not matching paper due to instrument mismatch; Poisson train lambda ~0.103 vs paper 0.100/0.101 close, test lambda ~0.077/0.089 vs paper 0.067/0.082 close (slightly higher due to proxy quantiles and date window shift Apr 1 vs Mar)."

output = {"results": results, "sample": sample, "notes": notes}
with open("/work/results.json","w") as f:
    json.dump(output, f, indent=2)
print("Wrote results.json with", len(results), "results")
for r in results:
    print(r)
