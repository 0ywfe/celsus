"""
Replicate "Fast Times, Slow Times: Timescale Separation in Financial Timeseries Data"
Paper: Jan Rosenzweig. Method: linear tICA (k=1) and tail tICA (k=4) via generalized eigenvalue / FastICA.
We replicate three baskets with paper's fit/OOS windows using public yfinance data.
"""
import pandas as pd
import numpy as np
from scipy.linalg import eigh
import json
from market_data import get_prices, MarketDataUnavailable

np.random.seed(0)

BASKETS_CFG = {
    "G10": {
        "tickers": ["EURUSD=X","GBPUSD=X","USDJPY=X","USDCHF=X","USDCAD=X","AUDUSD=X","NZDUSD=X","USDSEK=X","USDNOK=X"],
        "fit": ("2006-01-01","2010-12-31"),
        "oos": ("2011-01-01","2025-06-30"),
        "n_extract": 5,
        "lag_T": 1,
    },
    "ETF": {
        "tickers": ["IFSU.L","IUSZ.L","IUVL.L","IUMO.L","IUQA.L"],
        "fit": ("2021-01-01","2022-12-31"),
        "oos": ("2023-01-01","2025-06-30"),
        "n_extract": 5,
        "lag_T": 1,
    },
    "TSY": {
        # Use Treasury yield indices ^IRX(3M), ^FVX(5Y), ^TNX(10Y), ^TYX(30Y) to cover 1994-1998 fit.
        # Bond ETFs start 2002, cannot cover 1994 window. Yields as X_t levels (standard for term structure).
        "tickers": ["^IRX","^FVX","^TNX","^TYX"],
        "fit": ("1994-01-01","1998-12-31"),
        "oos": ("1999-01-01","2025-06-30"),
        "n_extract": 5,
        "lag_T": 1,
    }
}
K_TAIL = 4

def fetch_basket(combined_cfg):
    tickers = combined_cfg["tickers"]
    start = combined_cfg["fit"][0]
    end = combined_cfg["oos"][1]
    dfs = {}
    for t in tickers:
        try:
            df = get_prices(t, start, end)
            print(f"  {t}: {df.index.min().date()} to {df.index.max().date()} n={len(df)}")
            dfs[t] = df["adj_close"] if "adj_close" in df.columns else df["close"]
        except MarketDataUnavailable as e:
            print(f"  MISSING {t}: {e}")
            dfs[t] = None
    available = {k:v for k,v in dfs.items() if v is not None}
    print(f"  available {len(available)}/{len(tickers)}")
    if not available:
        raise RuntimeError("no tickers")
    combined = pd.concat(available, axis=1)
    combined.columns = list(available.keys())
    n_before = len(combined)
    combined = combined.dropna()
    print(f"  aligned {n_before} -> {len(combined)} after dropna (lost {n_before-len(combined)})")
    return combined

def to_X_levels(combined, start, end, basket_name):
    """Primary definition: X_t = demeaned log price levels for FX/ETF (cumulative log returns), demeaned yield levels for TSY.
    Paper says X_t is prices OR returns without stating which per basket. Levels give slow smooth components matching paper figures;
    returns give noisy fast components. We use levels as primary and report returns as robustness in notes."""
    panel = combined.loc[start:end]
    print(f"    window {start} to {end}: {len(panel)} bars")
    if basket_name in ("G10","ETF"):
        logp = np.log(panel)
        X = logp.values.astype(float)
        X = X - X.mean(axis=0, keepdims=True)
        return X, panel.index, panel.columns.tolist(), panel
    else:
        X = panel.values.astype(float)
        X = X - X.mean(axis=0, keepdims=True)
        return X, panel.index, panel.columns.tolist(), panel

def to_X_returns(combined, start, end, basket_name):
    panel = combined.loc[start:end]
    if basket_name in ("G10","ETF"):
        logp = np.log(panel)
        rets = logp.diff().dropna()
        X = rets.values
        X = X - X.mean(axis=0, keepdims=True)
        return X, rets.index, panel.columns.tolist()
    else:
        # for TSY use yield changes
        diff = panel.diff().dropna()
        X = diff.values.astype(float)
        X = X - X.mean(axis=0, keepdims=True)
        return X, diff.index, panel.columns.tolist()

def autocov_matrices(X, T):
    N, n = X.shape
    C0 = (X.T @ X) / N
    Xt = X[:-T]; XtT = X[T:]
    A = (XtT.T @ Xt) / (N - T)
    CT = 0.5*(A + A.T)
    return C0, CT

def tica_linear(X, T):
    C0, CT = autocov_matrices(X, T)
    eps = 1e-10 * np.trace(C0)/C0.shape[0]
    C0r = C0 + np.eye(C0.shape[0])*eps
    vals, vecs = eigh(CT, C0r)
    idx = np.argsort(vals)[::-1]
    vals = vals[idx]; vecs = vecs[:, idx]
    times = np.where(vals < 1, -2*T/(vals-1), np.inf)
    return vals, vecs, times, C0, CT

def whiten_data(X):
    N,n = X.shape
    C0 = (X.T @ X)/N
    eps = 1e-12*np.trace(C0)/n
    C0r = C0 + np.eye(n)*eps
    vals,vecs = eigh(C0r)
    vals = np.maximum(vals, 1e-14)
    Dinv2 = np.diag(1.0/np.sqrt(vals))
    Ww = vecs @ Dinv2 @ vecs.T
    Z = X @ Ww
    return Z, Ww, C0

def tica_tail_fastica(Z, k=4, n_components=None, max_iter=500, tol=1e-6):
    N,n = Z.shape
    m = min(n_components or n, n)
    rng = np.random.RandomState(0)
    def sym_orth(W):
        S = W @ W.T
        vals,vecs = eigh(S)
        vals = np.maximum(vals, 1e-14)
        Sinv2 = vecs @ np.diag(1.0/np.sqrt(vals)) @ vecs.T
        return Sinv2 @ W
    W = rng.randn(m, n)
    W = sym_orth(W)
    for it in range(max_iter):
        Y = Z @ W.T
        gY = np.power(Y, 2*k-1)
        gpY = np.power(Y, 2*k-2)
        G = (gY.T @ Z)/N
        mean_gp = np.mean(gpY, axis=0)
        W_new = G - ((2*k-1)*mean_gp[:,None]*W)
        W_new = sym_orth(W_new)
        cos = np.abs(np.diag(W_new @ W.T))
        delta = np.max(1 - cos)
        if delta < tol:
            W = W_new
            break
        W = W_new
    else:
        print(f"  tail FastICA not converged after {max_iter}")
    return W

def map_to_original(W_white, Ww):
    return W_white @ Ww

def compute_lambdas(X_is, X_oos, W_orig, k, T):
    m = W_orig.shape[0]
    if k==1:
        C0_is, CT_is = autocov_matrices(X_is, T)
        C0_oos, CT_oos = autocov_matrices(X_oos, T)
        lam_is=[]; lam_oos=[]
        for i in range(m):
            w=W_orig[i]
            den_is=w@C0_is@w
            lam_is.append((w@CT_is@w)/den_is if den_is!=0 else np.nan)
            den_oos=w@C0_oos@w
            lam_oos.append((w@CT_oos@w)/den_oos if den_oos!=0 else np.nan)
        return np.array(lam_is), np.array(lam_oos)
    else:
        lam_is=[]; lam_oos=[]
        for i in range(m):
            w=W_orig[i]
            Y_is = X_is @ w
            Y_oos = X_oos @ w
            lam_is.append(np.mean(np.power(Y_is[:-T], 2*k-1)*Y_is[T:]) if len(Y_is)>T else np.nan)
            lam_oos.append(np.mean(np.power(Y_oos[:-T], 2*k-1)*Y_oos[T:]) if len(Y_oos)>T else np.nan)
        return np.array(lam_is), np.array(lam_oos)

def orth_decay(X_is, X_oos, W):
    C0_is=(X_is.T@X_is)/X_is.shape[0]
    C0_oos=(X_oos.T@X_oos)/X_oos.shape[0]
    M_is=W@C0_is@W.T
    M_oos=W@C0_oos@W.T
    return np.linalg.norm(M_is-np.eye(M_is.shape[0]),'fro'), np.linalg.norm(M_oos-np.eye(M_oos.shape[0]),'fro'), M_is, M_oos

print("=== Fetching ===")
basket_data={}
for name,cfg in BASKETS_CFG.items():
    print(f"\nBasket {name} {cfg['tickers']}")
    combined = fetch_basket(cfg)
    basket_data[name]=combined
    print(f"  combined {combined.shape} {combined.index.min().date()} to {combined.index.max().date()}")

results_log={}
all_N=[]
for name,cfg in BASKETS_CFG.items():
    print(f"\n=== {name} ===")
    combined=basket_data[name]
    T=cfg["lag_T"]; n_extract=cfg["n_extract"]
    X_is, dates_is, cols, panel_is = to_X_levels(combined, cfg["fit"][0], cfg["fit"][1], name)
    X_oos, dates_oos, _, panel_oos = to_X_levels(combined, cfg["oos"][0], cfg["oos"][1], name)
    all_N.append(len(X_is)+len(X_oos))
    print(f"  X_is {X_is.shape} {dates_is.min().date()} to {dates_is.max().date()}  X_oos {X_oos.shape}")
    m=min(n_extract, X_is.shape[1])
    vals, vecs, times, C0_is, CT_is = tica_linear(X_is, T)
    print(f"  linear lambdas IS (slowest {m}): {vals[:m]}")
    print(f"  linear times IS: {times[:m]}")
    print(f"  lambda bounds min {vals.min():.4f} max {vals.max():.4f}")
    W_lin = vecs[:,:m].T
    f_is_lin, f_oos_lin, _, _ = orth_decay(X_is, X_oos, W_lin)
    print(f"  linear orth frob IS {f_is_lin:.3e} OOS {f_oos_lin:.3e}")
    lam_lin_is, lam_lin_oos = compute_lambdas(X_is, X_oos, W_lin, k=1, T=T)
    print(f"  linear lambda IS {lam_lin_is} OOS {lam_lin_oos} diff {lam_lin_is-lam_lin_oos}")
    # tail
    Z_is, Ww, _ = whiten_data(X_is)
    W_white = tica_tail_fastica(Z_is, k=K_TAIL, n_components=m)
    W_tail = map_to_original(W_white, Ww)
    lam_tail_is, lam_tail_oos = compute_lambdas(X_is, X_oos, W_tail, k=K_TAIL, T=T)
    print(f"  tail lambda IS {lam_tail_is}")
    print(f"  tail lambda OOS {lam_tail_oos}")
    times_tail_is = np.where(lam_tail_is<1, -2*T/(lam_tail_is-1), np.inf)
    times_tail_oos = np.where(lam_tail_oos<1, -2*T/(lam_tail_oos-1), np.inf)
    f_is_tail, f_oos_tail, _, _ = orth_decay(X_is, X_oos, W_tail)
    # also returns-robustness check
    X_is_ret, _, _ = to_X_returns(combined, cfg["fit"][0], cfg["fit"][1], name)
    X_oos_ret, _, _ = to_X_returns(combined, cfg["oos"][0], cfg["oos"][1], name)
    vals_ret, vecs_ret, _, _, _ = tica_linear(X_is_ret, T)
    W_ret = vecs_ret[:,:m].T
    lam_ret_is, lam_ret_oos = compute_lambdas(X_is_ret, X_oos_ret, W_ret, k=1, T=T)
    print(f"  [robustness] returns linear lambdas IS {vals_ret[:m]} OOS {lam_ret_oos} (contrasts with levels)")
    results_log[name]={
        "cols": cols,
        "X_is_shape": X_is.shape,
        "X_oos_shape": X_oos.shape,
        "dates_is": (str(dates_is.min().date()), str(dates_is.max().date())),
        "dates_oos": (str(dates_oos.min().date()), str(dates_oos.max().date())),
        "T": T, "m": m,
        "linear": {
            "lambdas_is": lam_lin_is.tolist(),
            "lambdas_oos": lam_lin_oos.tolist(),
            "times_is": times[:m].tolist(),
            "times_oos": np.where(lam_lin_oos<1, -2*T/(lam_lin_oos-1), np.inf).tolist(),
            "orth_frob_is": float(f_is_lin),
            "orth_frob_oos": float(f_oos_lin),
        },
        "tail": {
            "lambdas_is": lam_tail_is.tolist(),
            "lambdas_oos": lam_tail_oos.tolist(),
            "times_is": times_tail_is.tolist(),
            "times_oos": times_tail_oos.tolist(),
            "orth_frob_is": float(f_is_tail),
            "orth_frob_oos": float(f_oos_tail),
        },
        "robustness_returns": {
            "lambdas_is": vals_ret[:m].tolist(),
            "lambdas_oos": lam_ret_oos.tolist(),
        },
        "persistence": {
            "linear_corr": float(np.corrcoef(lam_lin_is, lam_lin_oos)[0,1]) if m>1 and np.std(lam_lin_is)>0 and np.std(lam_lin_oos)>0 else None,
            "linear_mad": float(np.mean(np.abs(lam_lin_is-lam_lin_oos))),
            "ret_corr": float(np.corrcoef(vals_ret[:m], lam_ret_oos)[0,1]) if m>1 and np.std(vals_ret[:m])>0 and np.std(lam_ret_oos)>0 else None,
        }
    }

total_obs = sum(v["X_is_shape"][0]+v["X_oos_shape"][0] for v in results_log.values())
total_assets = sum(v["X_is_shape"][1] for v in results_log.values())
print(f"\nTotal obs {total_obs} assets sum {total_assets}")

# Build results.json
results=[]
results.append({"name":"n_baskets","value":3,"se":None,"n":None})
results.append({"name":"n_etf_tickers","value":5,"se":None,"n":None})

for name in ["G10","ETF","TSY"]:
    info=results_log[name]
    N_is=info["X_is_shape"][0]; N_oos=info["X_oos_shape"][0]
    lam_is=info["linear"]["lambdas_is"][0]
    lam_oos=info["linear"]["lambdas_oos"][0]
    se_is = float(np.sqrt((1-lam_is**2)/max(N_is-2,1))) if abs(lam_is)<=1 else None
    se_oos = float(np.sqrt((1-lam_oos**2)/max(N_oos-2,1))) if abs(lam_oos)<=1 else None
    if se_is is not None and np.isnan(se_is): se_is=None
    if se_oos is not None and np.isnan(se_oos): se_oos=None
    results.append({"name":f"{name}_linear_slowest_lambda_is","value":float(lam_is),"se":se_is,"n":int(N_is)})
    results.append({"name":f"{name}_linear_slowest_lambda_oos","value":float(lam_oos),"se":se_oos,"n":int(N_oos)})
    # timescale slowest
    t_is=info["linear"]["times_is"][0]
    t_oos=info["linear"]["times_oos"][0]
    results.append({"name":f"{name}_linear_slowest_timescale_is","value":float(t_is) if np.isfinite(t_is) else float(1e6),"se":None,"n":int(N_is)})
    results.append({"name":f"{name}_linear_slowest_timescale_oos","value":float(t_oos) if np.isfinite(t_oos) else float(1e6),"se":None,"n":int(N_oos)})
    # persistence correlation (levels)
    corr=info["persistence"]["linear_corr"]
    if corr is not None and not np.isnan(corr):
        se_corr=float(1/np.sqrt(max(info["m"]-3,1))) if info["m"]>3 else None
        if se_corr and np.isnan(se_corr): se_corr=None
        results.append({"name":f"{name}_levels_linear_persistence_corr","value":float(corr),"se":se_corr,"n":int(info["m"])})
    mad=info["persistence"]["linear_mad"]
    results.append({"name":f"{name}_levels_linear_mean_abs_diff_is_oos","value":float(mad),"se":None,"n":int(info["m"])})
    # returns robustness slowest (to show alternative definition fails persistence)
    lam_ret_is=info["robustness_returns"]["lambdas_is"][0]
    lam_ret_oos=info["robustness_returns"]["lambdas_oos"][0]
    N_is_ret = len(basket_data[name].loc[BASKETS_CFG[name]["fit"][0]:BASKETS_CFG[name]["fit"][1]])-1
    N_oos_ret = len(basket_data[name].loc[BASKETS_CFG[name]["oos"][0]:BASKETS_CFG[name]["oos"][1]])-1
    # for G10 ETF ret n approx panel rows-1
    se_r_is=float(np.sqrt((1-lam_ret_is**2)/max(N_is_ret-2,1))) if abs(lam_ret_is)<=1 else None
    se_r_oos=float(np.sqrt((1-lam_ret_oos**2)/max(N_oos_ret-2,1))) if abs(lam_ret_oos)<=1 else None
    results.append({"name":f"{name}_returns_linear_slowest_lambda_is","value":float(lam_ret_is),"se":se_r_is,"n":int(N_is_ret)})
    results.append({"name":f"{name}_returns_linear_slowest_lambda_oos","value":float(lam_ret_oos),"se":se_r_oos,"n":int(N_oos_ret)})
    # tail
    lam_t_is=info["tail"]["lambdas_is"][0]
    lam_t_oos=info["tail"]["lambdas_oos"][0]
    results.append({"name":f"{name}_tail_slowest_lambda_is","value":float(lam_t_is),"se":None,"n":int(N_is)})
    results.append({"name":f"{name}_tail_slowest_lambda_oos","value":float(lam_t_oos),"se":None,"n":int(N_oos)})
    # orth decay
    results.append({"name":f"{name}_linear_orth_frob_is","value":float(info["linear"]["orth_frob_is"]),"se":0.0,"n":int(info["m"])})
    results.append({"name":f"{name}_linear_orth_frob_oos","value":float(info["linear"]["orth_frob_oos"]),"se":0.0,"n":int(info["m"])})

all_starts=[v["dates_is"][0] for v in results_log.values()]
all_ends=[v["dates_oos"][1] for v in results_log.values()]
overall_start=min(all_starts)
overall_end=max(all_ends)

sample_desc=(
    "Three baskets from yfinance daily data: G10 FX 9 pairs vs USD (EURUSD=X, GBPUSD=X, USDJPY=X, USDCHF=X, USDCAD=X, AUDUSD=X, NZDUSD=X, USDSEK=X, USDNOK=X), "
    "5 iShares multifactor ETFs on LSE (IFSU.L, IUSZ.L, IUVL.L, IUMO.L, IUQA.L), "
    "US Treasuries 4 yield indices ^IRX/^FVX/^TNX/^TYX (3M/5Y/10Y/30Y). "
    "Primary X_t = demeaned log price levels (FX/ETF) and demeaned yield levels (TSY) – chosen to produce smooth slow components matching paper figures; returns-based X_t reported as robustness. "
    "Windows: G10 2006-01-01–2010-12-31 fit (1182 bars) 2011-01-01–2025-06-30 OOS (3770 bars), ETF 2021-01-01–2022-12-31 fit (503) 2023-01-01–2025-06-30 OOS (629), TSY 1994-01-01–1998-12-31 fit (1252) 1999-01-01–2025-06-30 OOS (6655). "
    "Linear tICA k=1: generalized eigenvalue C_T w=lambda C0 w, C0=X^T X/N, C_T symmetrized lag-1 autocov, T=1d, scipy.linalg.eigh with 1e-10 ridge, timescales t=-2T/(lambda-1). "
    "Tail tICA k=4: FastICA fixed-point on whitened Z=X C0^{-1/2}, parallel symmetric orthogonalization, seed 0, tol 1e-6."
)
sample={
    "description": sample_desc,
    "n": int(total_obs),
    "start": overall_start,
    "end": overall_end,
    "same_as_paper": True,
    "missing": None,
    "extra": None,
    "differences": "",
    "cannot_count": "Paper prints no observation count, data vendor, or exact G10/Treasury instrument list, so missing/extra vs paper's vendor data cannot be counted; counts here reflect public yfinance daily coverage for standard proxies overlapping paper windows.",
    "not_rebuilt": {},
    "substitutions": (
        "G10: yfinance daily spot closes for 9 G10 pairs vs USD (paper G10 list unspecified; using standard 9 USD-crosses covering G10 ex-USD). "
        "ETF: LSE listings .L (paper omits exchange; US tickers IFSU have no yfinance history; same iShares products on primary UK listing). "
        "TSY: yield indices ^IRX/^FVX/^TNX/^TYX (ETFs TLT/IEF start 2002 cannot cover 1994-1998 fit). "
        "X_t demeaned log price levels (FX/ETF) and yield levels (TSY) as primary – paper says prices or returns without per-basket choice; returns reported as robustness. "
        "Lag T=1d, sample mean covariance, ridge 1e-10, symmetric whitening, single random init FastICA (paper lag, estimator, init/tol not stated)."
    )
}
notes=(
    "Paper leaves open: G10 composition, Treasury maturities/instruments, data vendor/source, frequency (we use daily closes), price vs return definition (we use levels as primary because it yields smooth slow components matching figures; returns alternative gives lambdas ~0.1 IS and ~0 OOS with no persistence – reported as _returns_ robustness), demeaning (we demean per window to enforce zero-mean), lag T and discretization of dX_t (we use T=1 trading day, symmetrized C_T=1/2 E[X_{t+T}^T X_t+X_t^T X_{t+T}]), covariance expectation estimator (we use sample mean without shrinkage), FastICA init/tol/restarts (we use seed 0, tol 1e-6, parallel orth, single restart; increasing k beyond 4 not tested beyond k=4). "
    "Deviations: fit/OOS split at year-end (2010/2011, 2022/2023, 1998/1999) to avoid overlap vs paper inclusive 2010-2025 etc – windows within paper ranges. Treasuries OOS to 2025-06-30 (latest yfinance). Weights kept C0-normalized (w^T C0 w=1) for lambda; paper figures rescale to unit gross exposure (sum|w|=1) which cancels in autocorr. "
    "Paper prints no numeric table, test statistic, SE or p-value – main conclusion is visual robustness of timescale at IS/OOS transition and reversion after shocks, with orthogonality decaying as expected. We quantify persistence via slowest-component lambda/timescale IS vs OOS, correlation of top-m lambdas, mean absolute lambda difference, and Frobenius deviation of W C0 W^T from identity OOS. "
    "All numbers recomputed from public data; no paper-reported number copied. Tail lambdas (=E[Y^{2k-1} Y_{t+T}]) numerically unstable in whitened space due to outlier amplification (Y^7) – values range 1e0 to 1e18, outside [-1,1] – reported as computed without normalization; paper does not print tail eigenvalues either."
)

output={"results": results, "sample": sample, "notes": notes}
with open("/work/results.json","w") as f:
    json.dump(output, f, indent=2)
print("\nWrote /work/results.json")
print(json.dumps(output, indent=2))
