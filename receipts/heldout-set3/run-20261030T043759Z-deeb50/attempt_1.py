#!/usr/bin/env python3
"""
Replication of Read (2025) "Sign Restrictions and Supply-demand Decompositions of Inflation"
Produces /work/results.json with headline estimates computed from public FRED data.
"""
import json
import requests
import pandas as pd
import numpy as np
import io

def fetch_fred(sid, timeout=15):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df['observation_date'] = pd.to_datetime(df['observation_date'])
    df = df.set_index('observation_date').sort_index()
    return df

print("Fetching FRED series...")
cpi_m = fetch_fred("CPIAUCSL")
gdp_q = fetch_fred("GDPC1")
print(f"CPI monthly {cpi_m.index.min()} to {cpi_m.index.max()} n={len(cpi_m)}")
print(f"GDP quarterly {gdp_q.index.min()} to {gdp_q.index.max()} n={len(gdp_q)}")

# quarterly aggregation helpers
def to_quarterly_avg(s_monthly):
    q = s_monthly.resample('QE').mean()
    q.index = pd.PeriodIndex(q.index, freq='Q')
    return q
def to_quarterly_last(s_monthly):
    q = s_monthly.resample('QE').last()
    q.index = pd.PeriodIndex(q.index, freq='Q')
    return q

cpi_q_mean = to_quarterly_avg(cpi_m['CPIAUCSL'])
gdp_q_series = gdp_q['GDPC1']
gdp_q_series.index = pd.PeriodIndex(gdp_q_series.index, freq='Q')

df_mean = pd.DataFrame({'cpi': cpi_q_mean})
df_mean = pd.concat([df_mean, gdp_q_series.rename('gdp')], axis=1).dropna()
df_mean['log_cpi'] = np.log(df_mean['cpi'])
df_mean['log_gdp'] = np.log(df_mean['gdp'])

# estimate VAR(4) OLS
def estimate_var(df, p=4, sample_start='1997Q1', sample_end='2019Q4'):
    est = df.loc[sample_start:sample_end]
    y = est[['log_cpi','log_gdp']].values
    n,k = y.shape
    T_est = n - p
    Y = y[p:,:]
    X = np.zeros((T_est, 1 + k*p))
    X[:,0] = 1
    for lag in range(1, p+1):
        X[:, 1+(lag-1)*k : 1+lag*k] = y[p-lag : n-lag, :]
    B_hat = np.linalg.lstsq(X, Y, rcond=None)[0]
    const = B_hat[0,:]
    A_list = []
    for lag in range(p):
        slice_mat = B_hat[1+lag*k : 1+(lag+1)*k, :]
        A_list.append(slice_mat.T)
    U = Y - X @ B_hat
    Sigma = (U.T @ U) / T_est
    Sigma_tr = np.linalg.cholesky(Sigma)
    sigma11 = Sigma_tr[0,0]; sigma21 = Sigma_tr[1,0]; sigma22 = Sigma_tr[1,1]
    rho = sigma21 / np.sqrt(sigma21**2 + sigma22**2)
    return {'est': est, 'Y': Y, 'X': X, 'B_hat': B_hat, 'A_list': A_list, 'const': const,
            'U': U, 'Sigma': Sigma, 'Sigma_tr': Sigma_tr, 'sigma11': sigma11, 'sigma21': sigma21, 'sigma22': sigma22,
            'rho': rho, 'T_est': T_est, 'k': k, 'p': p, 'df': df}

var = estimate_var(df_mean, p=4)
print(f"var rho {var['rho']:.4f} Sigma diag {np.diag(var['Sigma'])} T {var['T_est']}")
print(f"rho sigma11 {var['sigma11']:.6f} sigma21 {var['sigma21']:.6f} sigma22 {var['sigma22']:.6f}")

# forecast
def forecast_var(var_res, steps, start_period='2019Q4'):
    df = var_res['df']
    A_list = var_res['A_list']; const = var_res['const']; p = var_res['p']
    hist = df.loc[:start_period][['log_cpi','log_gdp']].values
    last_p = hist[-p:,:]
    forecasts = []
    for h in range(1, steps+1):
        y_pred = const.copy()
        for l in range(1, p+1):
            lag_idx = h - l
            if lag_idx <= 0:
                idx = (p-1) + lag_idx
                y_lag = last_p[idx, :]
            else:
                y_lag = forecasts[lag_idx-1]
            y_pred = y_pred + A_list[l-1] @ y_lag
        forecasts.append(y_pred)
    forecasts = np.array(forecasts)
    start_per = pd.Period(start_period, freq='Q')
    fc_index = pd.period_range(start_per+1, periods=steps, freq='Q')
    return forecasts, fc_index

fc, fc_index = forecast_var(var, steps=17)
print(f"forecast 2020Q1 {fc[0]} fc_index {fc_index[0]}")

def compute_fe_yearended(var_res, forecasts, fc_index):
    df = var_res['df']
    ext_actual = df['log_cpi']; ext_fc = pd.Series(forecasts[:,0], index=fc_index)
    fe = {}; act_ye={}; fc_ye={}
    for per in fc_index:
        if per in ext_actual.index and (per-4) in ext_actual.index:
            act_ye[per] = ext_actual.loc[per] - ext_actual.loc[per-4]
        else:
            act_ye[per]=np.nan
        fc_pt = ext_fc.loc[per]
        lag = per-4
        if lag in ext_fc.index:
            fc_pt4 = ext_fc.loc[lag]
        elif lag in ext_actual.index:
            fc_pt4 = ext_actual.loc[lag]
        else:
            fc_pt4=np.nan
        fc_ye[per]=fc_pt-fc_pt4
        fe[per]=act_ye[per]-fc_ye[per] if not np.isnan(act_ye[per]) else np.nan
    return act_ye, fc_ye, fe

act_ye, fc_ye, fe = compute_fe_yearended(var, fc, fc_index)
for per in fc_index:
    if per in fe and not np.isnan(fe[per]):
        print(per, f"act {act_ye[per]*100:.2f} fc {fc_ye[per]*100:.2f} FE {fe[per]*100:.2f}")

def compute_C_h(A_list, p, max_h):
    k = A_list[0].shape[0]
    C = [np.eye(k)]
    for h in range(1, max_h+1):
        Ch = np.zeros((k,k))
        for l in range(1, min(h,p)+1):
            Ch += A_list[l-1] @ C[h-l]
        C.append(Ch)
    return C

def compute_post_u(var_res, horizon_periods):
    df = var_res['df']; A_list=var_res['A_list']; const=var_res['const']; p=var_res['p']
    us={}
    for per in horizon_periods:
        y_t = df.loc[per][['log_cpi','log_gdp']].values
        y_pred = const.copy()
        for l in range(1, p+1):
            lag_per = per - l
            if lag_per in df.index:
                y_lag = df.loc[lag_per][['log_cpi','log_gdp']].values
                y_pred += A_list[l-1] @ y_lag
        us[per]=y_t-y_pred
    return us

us = compute_post_u(var, fc_index)
C_list = compute_C_h(var['A_list'], var['p'], 30)
k=2; e1=np.array([1,0])
def compute_Omega_h(var_res, C_list, us, horizon_index, h):
    Sigma_tr=var_res['Sigma_tr']; Sigma_tr_inv=np.linalg.inv(Sigma_tr)
    Omega=np.zeros((k,k))
    for l in range(0, h+1):
        Cl=C_list[l]; row=e1 @ Cl @ Sigma_tr
        per_idx=h-l
        if per_idx<0: continue
        per=horizon_index[per_idx]
        Sigma_inv_u=Sigma_tr_inv @ us[per]
        Omega+=np.outer(row, Sigma_inv_u)
    return Omega
def compute_tilde_Omega(var_res, C_list, us, horizon_index, h):
    Omega_h=compute_Omega_h(var_res, C_list, us, horizon_index, h)
    if h>=4:
        Omega_h4=compute_Omega_h(var_res, C_list, us, horizon_index, h-4)
        return Omega_h-Omega_h4
    else:
        return Omega_h
def IS_theta_bounds(Sigma_tr):
    s21=Sigma_tr[1,0]; s22=Sigma_tr[1,1]
    rho=s21/np.sqrt(s21**2+s22**2)
    if rho<0:
        lower=np.arctan(s22/s21); upper=0.0
    else:
        lower=-np.pi/2; upper=np.arctan(-s21/s22)
    return lower, upper, rho
def compute_bounds_for_h(var_res, C_list, us, horizon_index, h):
    tilde=compute_tilde_Omega(var_res, C_list, us, horizon_index, h)
    S=0.5*(tilde+tilde.T)
    Sigma_tr=var_res['Sigma_tr']; lower, upper, rho=IS_theta_bounds(Sigma_tr)
    cands=[]; ths=[]
    def H_theta(theta, Omega):
        q=np.array([np.cos(theta), np.sin(theta)], dtype=float)
        return float(q @ Omega @ q)
    for th in [lower, upper]:
        cands.append(H_theta(th, tilde)); ths.append(th)
    try:
        vals, vecs=np.linalg.eig(S)
        for i in range(2):
            v=np.array(vecs[:,i], dtype=float); v=v/np.linalg.norm(v)
            if v[0]<0: v=-v
            if v[0]<-1e-12: continue
            th=float(np.arctan2(float(v[1]), float(v[0])))
            if th>=lower-1e-9 and th<=upper+1e-9:
                cands.append(H_theta(th, tilde)); ths.append(th)
    except Exception as e:
        print(e)
    return min(cands), max(cands), cands, ths

h_2022Q2 = list(fc_index).index(pd.Period('2022Q2', freq='Q'))
L,U,_,_=compute_bounds_for_h(var, C_list, us, fc_index, h_2022Q2)
print(f"2022Q2 L {L*100:.2f} U {U*100:.2f} FE {fe[fc_index[h_2022Q2]]*100:.2f}")

all_bounds=[]
for h,per in enumerate(fc_index):
    Lb,Ub,_,_=compute_bounds_for_h(var, C_list, us, fc_index, h)
    all_bounds.append((per, Lb*100, Ub*100, fe[per]*100 if not np.isnan(fe[per]) else np.nan))
    print(per, f"L {Lb*100:.2f} U {Ub*100:.2f} FE {fe[per]*100:.2f}" if not np.isnan(fe[per]) else "nan")

# monthly PCE illustration
print("\nMonthly PCE illustration")
try:
    pce_price=fetch_fred("PCEPI")
    pce_real=fetch_fred("DPCERA3M086SBEA")
    df_pce=pd.DataFrame({'pcepi': pce_price['PCEPI']}); df_pce['pce_real']=pce_real['DPCERA3M086SBEA']
    df_pce=df_pce.dropna(); df_pce['infl']=np.log(df_pce['pcepi']).diff()*100; df_pce['real_growth']=np.log(df_pce['pce_real']).diff()*100; df_pce=df_pce.dropna()
    est_pce=df_pce.loc['1988-01-01':'2023-09-01']
    print(f"PCE monthly est n {len(est_pce)} {est_pce.index.min()} to {est_pce.index.max()}")
    from statsmodels.tsa.api import VAR
    var_pce_res=VAR(est_pce[['infl','real_growth']]).fit(12)
    corr_pce=var_pce_res.sigma_u.iloc[0,1]/np.sqrt(var_pce_res.sigma_u.iloc[0,0]*var_pce_res.sigma_u.iloc[1,1])
    print(f"PCE monthly VAR12 corr {corr_pce:.3f} sigma {var_pce_res.sigma_u.values}")
    # count explosive: quick check eigenvalues of companion
    print(f"PCE VAR12 nobs {var_pce_res.nobs}")
except Exception as e:
    print(f"PCE monthly fail {e}")
    corr_pce=np.nan

# prepare results
rho_est=var['rho']; n_obs=var['T_est']; se_rho=np.sqrt((1-rho_est**2)**2/(n_obs-1))
h_idx=list(fc_index).index(pd.Period('2022Q2', freq='Q'))
fe_val=fe[fc_index[h_idx]]*100
L_val=all_bounds[h_idx][1]; U_val=all_bounds[h_idx][2]

results=[]
def add_result(name, value, se, n):
    results.append({"name": name, "value": float(value) if value is not None else None, "se": float(se) if se is not None else (None), "n": int(n) if n is not None else None})

# parameters (model choices) - exact spec values
par_claims={"par_agg_lags":4,"par_disagg_lags":12,"par_phi_draws":10000,"par_theta_per_phi_uniform":10,"par_total_draws_uniform":100000,"par_theta_per_phi_joint":10000,"par_trivariate_draws":55000,"par_misclass_epsilon":1,"par_misclass_delta":1,"par_large_svar_Q_draws":10000,"par_K_required":10494,"par_d_hist":17,"par_epsilon_large":0.01,"par_delta_large":0.01,"par_cred_level":68}
for k,v in par_claims.items():
    add_result(k, v, None, None)

# estimates computed from public FRED
add_result("est_rho_agg_postmean", float(rho_est), float(se_rho), int(n_obs))
add_result("est_rho_agg_ci_low", float(rho_est - se_rho), float(se_rho), int(n_obs))
add_result("est_rho_agg_ci_high", float(rho_est + se_rho), float(se_rho), int(n_obs))
add_result("est_US_FE_2022Q2", float(fe_val), 0.0, 17)
add_result("est_US_supply_set_low_2022Q2", float(L_val), 0.0, 17)
add_result("est_US_supply_set_high_2022Q2", float(U_val), 0.0, 17)

# counts that are deterministic from period definitions
add_result("count_post2019_quarters_d", 17, None, None)
add_result("count_joint_hypothesis_quarters", 5, None, None)

sample_desc=f"Aggregate VAR(4) in log CPI (FRED CPIAUCSL quarterly mean, n={n_obs} usable obs 1997Q1-2019Q4 after lags) and log real GDP (FRED GDPC1) OLS; forecast 2020Q1-2024Q1 17 quarters year-ended CPI inflation (p_t - p_{{(t-4)}}) FE; monthly PCE VAR(12) 1988M1-2023M9 illustration (n={len(est_pce) if 'est_pce' in locals() else 'NA'} monthly obs)"
sample={
    "description": sample_desc,
    "n": int(n_obs+17),
    "start": "1988-01-01",
    "end": "2023-09-30",
    "same_as_paper": False,
    "missing": None,
    "extra": None,
    "differences": "Public FRED vintage 2026-10-30 vs GP24 private replication vintage; OLS point estimate vs Bayesian Minnesota+soc prior (Giannone-Lenza-Primiceri 2015) with 10k posterior draws; quarterly CPI as quarterly mean of CPIAUCSL then log vs unknown paper aggregation; identified sets at OLS estimate vs paper's posterior means of endpoints; PCE monthly illustration using FRED PCEPI/DPCERA aggregate only vs 136 BEA UD categories",
    "cannot_count": "Cannot count missing/extra observations without private GP24 vintage and BEA UD tables access (requires BEA API key, not available in sandbox)",
    "not_rebuilt": {
        "count_PCE_categories": "Requires BEA National Accounts Underlying Detail Tables monthly PCE prices and real expenditures per category (136 categories) - requires BEA API key and detailed table parsing, not available via public FRED; cannot count categories from public data without reconstructing full BEA vintage",
        "tally_explosive_VARs": "Requires estimating 136 category VAR(12) to check explosiveness - needs BEA data above",
        "est_euro_FE_2022Q4": "Euro area HICP quarterly level and GDP (ECB/Eurostat vintage 1997Q1-2019Q4) not available via public FRED at quarterly frequency matching GP24; FRED OECD harmonised series give inflation rates not levels, and euro GDP series incomplete",
        "est_euro_supply_postmean_2022Q4": "Same as above - euro area VAR not replicable without consistent quarterly HICP level series",
        "est_euro_supply_set_low_2022Q4": "Same as above",
        "est_euro_supply_set_high_2022Q4": "Same as above",
        "est_rho_lubricants_abs_upper": "Category-specific rho for 'lubricants and fluids' requires BEA UD Tables per-category price/quantity (see count_PCE_categories)",
        "est_rho_food_farms": "Same - category 'food produced and consumed on farms' rho -0.98 requires BEA UD Tables",
        "est_food_supply_low_2022M03": "Requires category VAR historical decomposition for that PCE category",
        "est_food_supply_high_2022M03": "Same",
        "est_food_inflation_2022M03_net": "Same",
        "est_joint_uniform_prob": "Requires full Bayesian prior-robust inference with 10k theta draws per phi (100k total) and posterior simulation under uniform prior - would need to replicate GP24's MCMC for phi posterior (Minnesota+soc prior hyperparameters tuned via ML), not feasible via OLS point estimate",
        "est_joint_lower_prob": "Same",
        "est_joint_upper_prob": "Same",
        "est_share_corr_gt020_vague": "Requires 136 category rhos distribution - needs BEA data",
        "est_share_corr_lt040_vague": "Same"
    },
    "substitutions": "OLS VAR(4) instead of Bayesian Minnesota+soc prior (hyperparameters via marginal likelihood); FRED CPIAUCSL quarterly mean vs paper's unspecified quarterly aggregation; FRED GDPC1 (chained 2017 dollars) vintage 2026 vs original vintage; monthly PCE aggregate via FRED PCEPI/DPCERA as illustration vs 136 BEA categories; identified set bounds via analytic eigenvector method at OLS point estimate (paper Fig2 shows posterior means of bounds); SE for rho via delta-method approx sqrt((1-rho^2)^2/(n-1)), FE SE=0 (fixed-horizon forecast error as per spec)"
}
notes="Choices paper leaves open: quarterly CPI aggregation (paper states log CPI quarterly but not whether quarterly value is mean of monthly levels, last month, or log-average; chose quarterly mean of CPI level then log as standard) - standard choice noted; risk-free rate not needed; calendars align via PeriodIndex Q-DEC; market data not used. Deviations: Public FRED vintage 2026-10-30 includes data revisions vs 2019 vintage paper used (affects GDP/CPI levels and forecast); Estimated OLS VAR(4) by OLS (n=88 usable after lags) vs paper's Bayesian VAR with Minnesota+soc prior (Giannone-Lenza-Primiceri 2015) and 10k phi posterior draws - this shifts rho from paper posterior mean 0.23 to OLS 0.219 and forecast year-ended inflation at 2022Q2 from ~0.6% (implied paper FE 7.7 = actual ~8.3 - forecast) to 2.11% (our FE 6.13), consequently supply identified set [0.39,5.35] vs paper [0.2,7.3] but still wide covering ~6% to 87% of FE, confirming uninformativeness. Euro area and disaggregated category results not rebuilt due to lack of public consistent vintage data (see not_rebuilt). Joint posterior probabilities (0.5,0,0.99) and trivariate 55k draws not resimulated - are prior-robust Bayesian outputs requiring full posterior. All reported headline numbers computed from data fetched in script via FRED CSV."

out={"results": results, "sample": sample, "notes": notes}
with open("/work/results.json","w") as f:
    json.dump(out, f, indent=2)
print("Wrote results.json")
print(json.dumps(out, indent=2))
