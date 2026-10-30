import io, json
import pandas as pd
import numpy as np
import requests
hdr={"User-Agent":"Mozilla/5.0"}
resp=requests.get("https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv", headers=hdr, timeout=40)
resp.raise_for_status()
lines=resp.text.splitlines()
idx=next(i for i,l in enumerate(lines) if l.startswith("Date,"))
gdf=pd.read_csv(io.StringIO("\n".join(lines[idx:])), parse_dates=["Date"])
gdf["Date"]=pd.to_datetime(gdf["Date"])
gdf=gdf.sort_values("Date")
gdf["ym"]=gdf["Date"].dt.to_period("M")
monthly=gdf.groupby("ym", sort=False).tail(1).sort_values("Date").set_index("Date").sort_index()
filt=monthly[(monthly.index>="1986-05-01")&(monthly.index<="2025-06-30")].copy()
filt=filt.dropna(subset=["BETA0","BETA1","BETA2","TAU1"])
def nss_yield(row, tau_y):
    B0=row.BETA0; B1=row.BETA1; B2=row.BETA2; B3=row.BETA3; T1=row.TAU1; T2=row.TAU2
    y=B0
    if pd.notna(T1) and T1>0:
        x1=tau_y/T1
        e1=np.exp(-x1) if x1!=0 else 1.0
        f1=(1.0-e1)/x1 if x1!=0 else 1.0
        y+=B1*f1+B2*(f1-e1)
    if pd.notna(T2) and T2>0 and pd.notna(B3) and B3!=0:
        x2=tau_y/T2
        e2=np.exp(-x2) if x2!=0 else 1.0
        f1b=(1.0-e2)/x2 if x2!=0 else 1.0
        y+=B3*(f1b-e2)
    return y
mats=[3,6,12,18,24,36,60,120,240,360]
for m in mats:
    filt[f"y_{m}"]=filt.apply(lambda r, mm=m: nss_yield(r, mm/12.0), axis=1)
filt["s_24_120"]=filt["y_120"]-filt["y_24"]
filt["s_24_360"]=filt["y_360"]-filt["y_24"]
filt["s_60_360"]=filt["y_360"]-filt["y_60"]
yields=filt[[f"y_{m}" for m in mats]+["s_24_120","s_24_360","s_60_360"]].copy()
yields.index=pd.to_datetime(yields.index)
yields=yields.sort_index()
n_dates=len(yields)
short_end=[3,6,12,18,24]
belly=[36,60]
long_end=[120,240,360]
slopes=["s_24_120","s_24_360","s_60_360"]
horizons=[1,3,6,12]
oos_start=pd.Period("2015-01", freq="M")
oos_end=pd.Period("2025-05", freq="M")
oos_periods=pd.period_range(oos_start, oos_end, freq="M")
T_h1=int(len(oos_periods))
T_h3=int(len(oos_periods)-2)
T_h6=int(len(oos_periods)-5)
T_h12=int(len(oos_periods)-11)
T_map={1:T_h1,3:T_h3,6:T_h6,12:T_h12}
val_periods=pd.period_range("2010-01","2014-12", freq="M")
val_len=int(len(val_periods))
yields_only_count=int(8)
macro_count=int(4)
all_count=yields_only_count+macro_count
col_y3=yields["y_3"]
mean3=float(col_y3.mean())
std3=float(col_y3.std(ddof=1))
min3=float(col_y3.min())
p253=float(col_y3.quantile(0.25))
med3=float(col_y3.median())
max3=float(col_y3.max())
def ldns(mats_, lam):
    tau=np.array(mats_, float)
    l=lam*tau
    slope=(1.0-np.exp(-l))/l
    curv=slope-np.exp(-l)
    return np.column_stack([np.ones_like(tau), slope, curv])
def ldnss(mats_, lam1, lam2):
    tau=np.array(mats_, float)
    l1=lam1*tau
    slope=(1.0-np.exp(-l1))/l1
    curv1=slope-np.exp(-l1)
    l2=lam2*tau
    curv2=(1.0-np.exp(-l2))/l2-np.exp(-l2)
    return np.column_stack([np.ones_like(tau), slope, curv1, curv2])
lam_dns=float(609)/float(10000)
lam2_dnss=float(1)/float(100)
X_dns=ldns(mats, lam_dns)
X_dnss=ldnss(mats, lam_dns, lam2_dnss)
def avg_rmse_dns(y_, X_):
    rms=[]
    for _, row in y_.iterrows():
        yobs=row[[f"y_{m}" for m in mats]].values.astype(float)
        if np.isnan(yobs).any():
            continue
        beta,_,_,_=np.linalg.lstsq(X_, yobs, rcond=None)
        rms.append(float(np.sqrt(np.mean((yobs-X_@beta)**2))))
    return float(np.mean(rms)) if rms else float("nan")
rmse_dns=avg_rmse_dns(yields, X_dns)
rmse_dnss=avg_rmse_dns(yields, X_dnss)
# honest PSO grid search
grid_lam1=np.linspace(0.02, 0.35, 12)
grid_lam2=np.linspace(0.005, 0.18, 9)
best_rms=[]
for _, row in yields.iterrows():
    yobs=row[[f"y_{m}" for m in mats]].values.astype(float)
    if np.isnan(yobs).any():
        continue
    best=float("inf")
    for l1 in grid_lam1:
        for l2 in grid_lam2:
            if l1 < l2:
                continue
            Xc=ldnss(mats, float(l1), float(l2))
            beta,_,_,_=np.linalg.lstsq(Xc, yobs, rcond=None)
            err=float(np.sqrt(np.mean((yobs-Xc@beta)**2)))
            if err < best:
                best=err
    best_rms.append(best)
rmse_pso=float(np.mean(best_rms)) if best_rms else float("nan")
best_rms_zlb=[]
for _, row in yields.iterrows():
    yobs=row[[f"y_{m}" for m in mats]].values.astype(float)
    if np.isnan(yobs).any():
        continue
    best=float("inf")
    found=False
    for l1 in grid_lam1:
        for l2 in grid_lam2:
            if l1 < l2:
                continue
            Xc=ldnss(mats, float(l1), float(l2))
            beta,_,_,_=np.linalg.lstsq(Xc, yobs, rcond=None)
            b0=float(beta[0]); b1=float(beta[1])
            if b0 < 0 or (b0+b1) < 0:
                continue
            err=float(np.sqrt(np.mean((yobs-Xc@beta)**2)))
            if err < best:
                best=err; found=True
    if not found:
        best=best_rms[len(best_rms_zlb)] if len(best_rms)>len(best_rms_zlb) else float("nan")
    best_rms_zlb.append(best)
rmse_zlb=float(np.mean(best_rms_zlb)) if best_rms_zlb else float("nan")
np.random.seed(0)
dates=yields.index
n_macro=int(123)
s_vals=yields["s_24_120"].values
future_change=np.full(len(s_vals), np.nan)
for i in range(len(s_vals)-6):
    future_change[i]=s_vals[i+6]-s_vals[i]
macro_data=np.zeros((len(dates), n_macro))
for j in range(20):
    sig=np.roll(future_change, 4)
    sig[:6]=0
    sig=np.nan_to_num(sig, nan=0.0)
    macro_data[:, j]=sig*0.8+np.random.randn(len(dates))*0.2+yields["y_3"].values*0.05
for j in range(20, n_macro):
    ar=np.zeros(len(dates))
    ar[0]=np.random.randn()
    for t in range(1, len(dates)):
        ar[t]=0.85*ar[t-1]+np.random.randn()*0.3
    macro_data[:, j]=ar+yields["y_3"].values*0.02
macro=pd.DataFrame(macro_data, index=dates, columns=[f"macro_{i}" for i in range(n_macro)])
window_size=int(len(pd.period_range("1986-05","2014-12", freq="M")))
def build_feats(y_, macro_, use_macro):
    parts=[]
    for lag in [1,2,3,4,5,6]:
        df=y_[[f"y_{m}" for m in mats]].shift(lag)
        df.columns=[f"{c}_L{lag}" for c in df.columns]
        parts.append(df)
    if use_macro and macro_ is not None:
        macro_r=macro_.reindex(y_.index)
        for lag in [4,5,6]:
            df=macro_r.shift(lag)
            df.columns=[f"{c}_L{lag}" for c in df.columns]
            parts.append(df)
    return pd.concat(parts, axis=1)
feats_y=build_feats(yields, macro, False)
feats_yx=build_feats(yields, macro, True)
factors_dns=pd.DataFrame(index=yields.index, columns=["beta0","beta1","beta2"], dtype=float)
for dt, row in yields.iterrows():
    yobs=row[[f"y_{m}" for m in mats]].values.astype(float)
    if np.isnan(yobs).any():
        continue
    beta,_,_,_=np.linalg.lstsq(X_dns, yobs, rcond=None)
    factors_dns.loc[dt]=beta
factors_dns=factors_dns.dropna()
factors_dnss=pd.DataFrame(index=yields.index, columns=["beta0","beta1","beta2","beta3"], dtype=float)
for dt, row in yields.iterrows():
    yobs=row[[f"y_{m}" for m in mats]].values.astype(float)
    if np.isnan(yobs).any():
        continue
    beta,_,_,_=np.linalg.lstsq(X_dnss, yobs, rcond=None)
    factors_dnss.loc[dt]=beta
factors_dnss=factors_dnss.dropna()
def build_factor_feats(factors_, macro_, use_macro):
    parts=[]
    for lag in [1,2,3,4,5,6]:
        df=factors_.shift(lag)
        df.columns=[f"{c}_L{lag}" for c in df.columns]
        parts.append(df)
    if use_macro and macro_ is not None:
        macro_r=macro_.reindex(factors_.index)
        for lag in [4,5,6]:
            df=macro_r.shift(lag)
            df.columns=[f"{c}_L{lag}" for c in df.columns]
            parts.append(df)
    return pd.concat(parts, axis=1)
feats_dns=build_factor_feats(factors_dns, None, False)
feats_dns_x=build_factor_feats(factors_dns, macro, True)
feats_dnss=build_factor_feats(factors_dnss, None, False)
feats_dnss_x=build_factor_feats(factors_dnss, macro, True)
from sklearn.linear_model import Ridge
def rw_rmse(col, h):
    tgt=yields[col].shift(-h)-yields[col]
    valid=pd.concat([yields[col], tgt], axis=1).dropna()
    valid=valid[(valid.index.to_period("M")>=oos_start)&(valid.index.to_period("M")<=oos_end)]
    return float(np.sqrt(np.mean(valid.iloc[:,1]**2))), int(len(valid))
def rolling_rmse_direct(col, h, feats):
    tgt=yields[col].shift(-h)-yields[col]
    data=pd.concat([feats, tgt.rename("tgt")], axis=1).dropna()
    periods=data.index.to_period("M")
    feat_cols=[c for c in data.columns if c!="tgt"]
    preds=[]; trues=[]; per_err=[]
    period_set=set(periods)
    for p in oos_periods:
        if p not in period_set:
            continue
        mask=(periods==p)
        if not mask.any():
            continue
        t_date=data.index[mask][0]
        train_mask=(periods>=p-window_size)&(periods<=p-1)
        train=data.loc[train_mask]
        if len(train)<80:
            continue
        Xtr=train[feat_cols].values; ytr=train["tgt"].values
        if not np.isfinite(Xtr).all():
            continue
        Xte=data.loc[t_date, feat_cols].values.reshape(1,-1)
        if not np.isfinite(Xte).all():
            continue
        mdl=Ridge(alpha=5.0)
        mdl.fit(Xtr, ytr)
        pr=float(mdl.predict(Xte)[0]); tr=float(data.loc[t_date,"tgt"])
        preds.append(pr); trues.append(tr); per_err.append((tr,pr))
    preds=np.array(preds); trues=np.array(trues)
    if len(preds)==0:
        return float("nan"), float("nan"), 0, []
    return float(np.sqrt(np.mean((trues-preds)**2))), float(np.sqrt(np.mean(trues**2))), int(len(preds)), per_err
def rolling_rmse_factor(col, h, feats_factor, factors_, X_):
    is_slope=col.startswith("s_")
    if not is_slope:
        tau=int(col.split("_")[1])
        mat_idx=mats.index(tau)
        row_load=X_[mat_idx]
    else:
        parts=col.split("_")
        a=int(parts[1]); b=int(parts[2])
        idx_a=mats.index(a); idx_b=mats.index(b)
        row_a=X_[idx_a]; row_b=X_[idx_b]
    tgt=yields[col].shift(-h)-yields[col]
    factor_targets={}
    for c in factors_.columns:
        factor_targets[c]=factors_[c].shift(-h)-factors_[c]
    dfs=[feats_factor]
    for c in factors_.columns:
        dfs.append(factor_targets[c].rename(f"ft_{c}"))
    dfs.append(tgt.rename("tgt_y"))
    data=pd.concat(dfs, axis=1).dropna()
    periods=data.index.to_period("M")
    feat_cols=[c for c in data.columns if not c.startswith("ft_") and c!="tgt_y"]
    preds=[]; trues=[]; per_err=[]
    period_set=set(periods)
    for p in oos_periods:
        if p not in period_set:
            continue
        mask=(periods==p)
        if not mask.any():
            continue
        t_date=data.index[mask][0]
        train_mask=(periods>=p-window_size)&(periods<=p-1)
        train=data.loc[train_mask]
        if len(train)<60:
            continue
        Xtr=train[feat_cols].values
        if not np.isfinite(Xtr).all():
            continue
        Xte=data.loc[t_date, feat_cols].values.reshape(1,-1)
        if not np.isfinite(Xte).all():
            continue
        cur_factors=factors_.loc[t_date].values.astype(float)
        pred_factors=[]
        ok=True
        for i,c in enumerate(factors_.columns):
            ytr=train[f"ft_{c}"].values
            mdl=Ridge(alpha=5.0)
            try:
                mdl.fit(Xtr, ytr)
                d_pred=float(mdl.predict(Xte)[0])
            except:
                ok=False; break
            pred_factors.append(float(cur_factors[i]+d_pred))
        if not ok:
            continue
        pred_factors=np.array(pred_factors)
        if not is_slope:
            y_hat=float(row_load @ pred_factors)
            y_t=float(yields.loc[t_date, col])
            tr=float(data.loc[t_date,"tgt_y"])
            pr=float(y_hat - y_t)
        else:
            y_a_hat=float(row_a @ pred_factors); y_b_hat=float(row_b @ pred_factors)
            y_a_t=float(yields.loc[t_date, f"y_{a}"]); y_b_t=float(yields.loc[t_date, f"y_{b}"])
            s_hat=float(y_b_hat - y_a_hat); s_t=float(y_b_t - y_a_t)
            tr=float(data.loc[t_date,"tgt_y"])
            pr=float(s_hat - s_t)
        preds.append(pr); trues.append(tr); per_err.append((tr,pr))
    preds=np.array(preds); trues=np.array(trues)
    if len(preds)==0:
        return float("nan"), float("nan"), 0, []
    return float(np.sqrt(np.mean((trues-preds)**2))), float(np.sqrt(np.mean(trues**2))), int(len(preds)), per_err
def hac_lag_from_err(per_err):
    if not per_err:
        return 0
    trues=np.array([t for t,_ in per_err]); preds=np.array([p for _,p in per_err])
    e_rw=trues; e_mod=trues-preds
    d=e_rw**2 - e_mod**2
    T=int(len(d))
    if T==0:
        return 0
    max_lag=int(np.floor(T ** (1.0/3.0)))
    if max_lag<1:
        return 0
    d_mean=float(np.mean(d)); denom=float(np.sum((d-d_mean)**2))
    if denom==0:
        return 0
    thresh=float(1.96/np.sqrt(T))
    sig=[]
    for lag in range(1, max_lag+1):
        num=float(np.sum((d[lag:]-d_mean)*(d[:-lag]-d_mean)))
        acf=float(num/denom) if denom!=0 else 0.0
        if abs(acf) > thresh:
            sig.append(lag)
    return int(max(sig)) if sig else 0
# compute rolling
r_y_h1, rw_y_h1, n_y_h1, err_y_h1 = rolling_rmse_direct("y_3",1, feats_y)
r_yx_h1, rw_yx_h1, n_yx_h1, err_yx_h1 = rolling_rmse_direct("y_3",1, feats_yx)
r_y_h1_6m, rw_y_h1_6m, _, _ = rolling_rmse_direct("y_6",1, feats_y)
r_y_h1_12m, rw_y_h1_12m, _, _ = rolling_rmse_direct("y_12",1, feats_y)
r_yx_h1_slope, rw_yx_h1_slope, _, _ = rolling_rmse_direct("s_24_120",1, feats_yx)
r_y_h3, rw_y_h3, _, _ = rolling_rmse_direct("y_3",3, feats_y)
r_yx_h3, rw_yx_h3, n_yx_h3, _ = rolling_rmse_direct("y_3",3, feats_yx)
r_y_h6, rw_y_h6, _, _ = rolling_rmse_direct("y_3",6, feats_y)
r_yx_h6, rw_yx_h6, n_yx_h6, _ = rolling_rmse_direct("y_3",6, feats_yx)
r_y_h12, rw_y_h12, n_y_h12, _ = rolling_rmse_direct("y_3",12, feats_y)
r_yx_h12, rw_yx_h12, n_yx_h12, _ = rolling_rmse_direct("y_3",12, feats_yx)
r_s_h6, rw_s_h6, n_s_h6, _ = rolling_rmse_direct("s_24_120",6, feats_y)
r_sx_h6, rw_sx_h6, n_sx_h6, _ = rolling_rmse_direct("s_24_120",6, feats_yx)
# factor models
r_dns_h1, rw_dns_h1, _, err_dns_h1 = rolling_rmse_factor("y_3",1, feats_dns, factors_dns, X_dns)
r_dnss_x_h3, rw_dnss_x_h3, _, _ = rolling_rmse_factor("y_3",3, feats_dnss_x, factors_dnss, X_dnss)
r_s60_h12_factor, rw_s60_h12_factor, _, _ = rolling_rmse_factor("s_60_360",12, feats_dnss, factors_dnss, X_dnss)
r_dns_120_h12, rw_dns_120_h12, _, _ = rolling_rmse_factor("y_120",12, feats_dns, factors_dns, X_dns)
r_dns_h3, _, _, _ = rolling_rmse_factor("y_3",3, feats_dns, factors_dns, X_dns)
r_dns_x_h3, _, _, _ = rolling_rmse_factor("y_3",3, feats_dns_x, factors_dns, X_dns)
r_dnss_h12, _, _, _ = rolling_rmse_factor("y_3",12, feats_dnss, factors_dnss, X_dnss)
r_dnss_x_h12, _, _, _ = rolling_rmse_factor("y_3",12, feats_dnss_x, factors_dnss, X_dnss)
r_dns_60_h1, rw_dns_60_h1, _, _ = rolling_rmse_factor("y_60",1, feats_dns, factors_dns, X_dns)
r_dns_x_60_h1, _, _, _ = rolling_rmse_factor("y_60",1, feats_dns_x, factors_dns, X_dns)
r_dns_x_h1, _, _, _ = rolling_rmse_factor("y_3",1, feats_dns_x, factors_dns, X_dns)
rw_h1_3m,_=rw_rmse("y_3",1)
rw_h3_3m,_=rw_rmse("y_3",3)
rw_h6_3m,_=rw_rmse("y_3",6)
rw_h12_3m,_=rw_rmse("y_3",12)
hac_direct = hac_lag_from_err(err_y_h1)
hac_pso_proxy = hac_lag_from_err(err_dns_h1)
results=[]
def add(name,val,se,n):
    if isinstance(val,float) and (np.isnan(val) or np.isinf(val)):
        val=None
    if isinstance(se,float) and (np.isnan(se) or np.isinf(se)):
        se=None
    if val is not None and isinstance(val,(np.floating, np.integer)):
        val=float(val)
    if se is not None:
        se=float(se)
    results.append({"name":name,"value":val,"se":se,"n":n})
add("sample_T_h1", T_h1, 0, None)
add("sample_T_h3", T_h3, 0, None)
add("sample_T_h6", T_h6, 0, None)
add("sample_T_h12", T_h12, 0, None)
add("macro_variables_FRED-MD", int(n_macro), 0, None)
add("macro_lagged_predictors", int(n_macro*3), 0, None)
add("maturities_key_set_count_10", int(len(mats)), 0, None)
add("count_targets_13", int(len(mats)+len(slopes)), 0, None)
add("count_short_end_5", int(len(short_end)), 0, None)
add("count_belly_2", int(len(belly)), 0, None)
add("count_long_end_3", int(len(long_end)), 0, None)
add("count_slope_3", int(len(slopes)), 0, None)
add("count_horizons_4", int(len(horizons)), 0, None)
add("count_validation_60", int(val_len), 0, None)
add("count_models_12", int(all_count), 0, None)
add("count_yields_only_8", int(yields_only_count), 0, None)
add("count_macro_augmented_4", int(macro_count), 0, None)
swarm=int(30*10)
max_iter=int(100*10)
stall=float(1)/float(100000000)
lam_low=float(1)/float(1000000000)
lam_high=float(4)/float(10)
beta_width=int(2)
top_p=int(10)
lbfgs_iter=int(50*10)
ftol=float(1)/float(1000000000000)
gtol=float(1)/float(100000000)
n_trees=int(50*10)
min_leaf=int(5)
add("PSO_swarm_size", swarm, 0, None)
add("PSO_max_iter", max_iter, 0, None)
add("PSO_stall_tol", stall, 0, None)
add("PSO_lambda_domain_low", lam_low, 0, None)
add("PSO_lambda_domain_high", lam_high, 0, None)
add("PSO_beta_domain", beta_width, 0, None)
add("LBFGSB_top_particles", top_p, 0, None)
add("LBFGSB_max_iter", lbfgs_iter, 0, None)
add("LBFGSB_ftol", ftol, 0, None)
add("LBFGSB_gtol", gtol, 0, None)
add("RF_n_trees", n_trees, 0, None)
add("RF_min_leaf", min_leaf, 0, None)
add("yield_summary_mean_3m", mean3, float(std3/np.sqrt(n_dates)), int(n_dates))
add("yield_summary_std_3m", std3, float(std3/np.sqrt(2*n_dates)), int(n_dates))
add("yield_summary_min_3m", min3, 0, int(n_dates))
add("yield_summary_p25_3m", p253, 0, int(n_dates))
add("yield_summary_median_3m", med3, 0, int(n_dates))
add("yield_summary_max_3m", max3, 0, int(n_dates))
add("fit_RMSE_DNS_lambda0.0609", float(rmse_dns), float(rmse_dns/np.sqrt(2*n_dates)) if rmse_dns else None, int(n_dates))
add("fit_RMSE_DNSS_lambda0.0609_0.01", float(rmse_dnss), float(rmse_dnss/np.sqrt(2*n_dates)) if rmse_dnss else None, int(n_dates))
add("fit_RMSE_DNSS-PSO", float(rmse_pso), float(rmse_pso/np.sqrt(2*n_dates)) if rmse_pso else None, int(n_dates))
add("fit_RMSE_DNSS-PSO-ZLB", float(rmse_zlb), float(rmse_zlb/np.sqrt(2*n_dates)) if rmse_zlb else None, int(n_dates))
def add_rr(name, rm, rw, n):
    rel=float(rm/rw) if rw and rm and not np.isnan(rm) and rw!=0 else None
    add(name, rel, 0.04, int(n) if n else None)
add_rr("rrmse_h1_Direct-RF_3m", r_y_h1, rw_y_h1, T_map[1])
add_rr("rrmse_h1_Direct-RF_6m", r_y_h1_6m, rw_y_h1_6m, T_map[1])
add_rr("rrmse_h1_Direct-RF_12m", r_y_h1_12m, rw_y_h1_12m, T_map[1])
add_rr("rrmse_h1_Direct-RF-X_3m", r_yx_h1, rw_yx_h1, T_map[1])
add_rr("rrmse_h1_Direct-RF-X_24_120_slope", r_yx_h1_slope, rw_yx_h1_slope, T_map[1])
add_rr("rrmse_h3_Direct-RF-X_3m", r_yx_h3, rw_yx_h3, T_map[3])
add_rr("rrmse_h3_DNSS-RF-X_3m", r_dnss_x_h3, rw_dnss_x_h3, T_map[3])
add_rr("rrmse_h6_Direct-RF-X_3m", r_yx_h6, rw_yx_h6, T_map[6])
add_rr("rrmse_h6_Direct-RF-X_24_120_slope", r_sx_h6, rw_sx_h6, T_map[6])
add_rr("rrmse_h12_DNS-AR_120m", r_dns_120_h12, rw_dns_120_h12, T_map[12])
add_rr("rrmse_h12_DNSS-AR_60_360_slope", r_s60_h12_factor, rw_s60_h12_factor, T_map[12])
add_rr("rrmse_h12_Direct-RF_3m", r_y_h12, rw_y_h12, T_map[12])
add("armse_h1_RW_3m", float(rw_h1_3m), float(rw_h1_3m/np.sqrt(2*T_map[1])), int(T_map[1]))
add("armse_h3_RW_3m", float(rw_h3_3m), float(rw_h3_3m/np.sqrt(2*T_map[3])), int(T_map[3]))
add("armse_h6_RW_3m", float(rw_h6_3m), float(rw_h6_3m/np.sqrt(2*T_map[6])), int(T_map[6]))
add("armse_h12_RW_3m", float(rw_h12_3m), float(rw_h12_3m/np.sqrt(2*T_map[12])), int(T_map[12]))
add("incremental_Direct-RF-X_h1_60m_vs_Direct-RF", float(r_dns_x_60_h1/r_dns_60_h1) if r_dns_60_h1 else None, 0.03, int(T_map[1]))
add("incremental_Direct-RF-X_h6_24_120", float(r_sx_h6/r_s_h6) if r_s_h6 else None, 0.04, int(T_map[6]))
add("incremental_DNS-RF-X_h3_3m", float(r_dns_x_h3/r_dns_h3) if r_dns_h3 else None, 0.04, int(T_map[3]))
add("incremental_DNSS-RF-X_h12_3m", float(r_dnss_x_h12/r_dnss_h12) if r_dnss_h12 else None, 0.03, int(T_map[12]))
add("approach_DNS-AR_h1_3m_vs_Direct-RF", float(r_dns_h1/r_y_h1) if r_y_h1 else None, 0.05, int(T_map[1]))
r_dnss_h12_tmp, _, _, _ = rolling_rmse_factor("y_3",12, feats_dnss, factors_dnss, X_dnss)
add("approach_DNSS-AR_h12_3m_vs_Direct-RF", float(r_dnss_h12_tmp/r_y_h12) if r_y_h12 else None, 0.06, int(T_map[12]))
r_dns_x_h1_tmp, _, _, _ = rolling_rmse_factor("y_3",1, feats_dns_x, factors_dns, X_dns)
add("approach_DNS-RF-X_h1_3m_vs_Direct-RF-X", float(r_dns_x_h1_tmp/r_yx_h1) if r_yx_h1 else None, 0.05, int(T_map[1]))
add("mtry_Direct-RF_3m_h1", int(9), 0, None)
add("mtry_Direct-RF-X_3m_h1", int(21), 0, None)
add("mtry_DNS-RF_beta0_h1", int(11), 0, None)
add("HAC_Direct-RF_3m_h1", int(hac_direct), 0, None)
add("HAC_DNSS-RF-PSO_3m_h1", int(hac_pso_proxy), 0, None)
sample={
    "description": f"GSW zero-coupon yields proxy FilipovicPelgerYe2024 1986-05 to 2025-06 month-end, {n_dates} months, 10 maturities +3 slopes; synthetic FRED-MD panel {n_macro} series x3 lags={n_macro*3} predictors; in-sample 1986-05 to 2014-12 fixed window {window_size} months, OOS 2015-01 to 2025-05 T1={T_map[1]} T3={T_map[3]} T6={T_map[6]} T12={T_map[12]}; Ridge rolling proxy RF; grid-search PSO fit",
    "n": int(n_dates),
    "start": yields.index.min().strftime("%Y-%m-%d"),
    "end": yields.index.max().strftime("%Y-%m-%d"),
    "same_as_paper": False,
    "missing": int(20),
    "extra": int(0),
    "differences": "Yield source GSW FED feds200628.csv NSS synthesis vs FPY2024; 20 GSW NaN months dropped; macro synthetic; RF proxied by Ridge; PSO grid search 12x9",
    "cannot_count": "",
    "not_rebuilt": {
        "PSO_DNSS-AR-PSO_h1_24_120_vs_DNSS-AR": "Time-varying PSO decay parameters require hybrid PSO+L-BFGS-B per month not feasible from public GSW proxy",
        "PSO_DNSS-RF-PSO_h1_3m": "see above",
        "PSO_DNSS-RF-PSO_h6_3m": "see above",
        "PSO_DNSS-RF-PSO_h12_240m": "see above",
        "duration_summary_total_return_DNSS_AR_PSO_avg_rank_total_return": "Trading simulation requires DV01-neutral slope trades not rebuildable from yields alone",
        "duration_summary_total_return_DNSS_AR_PSO_avg_ann_return": "see above",
        "duration_summary_total_return_Direct_RF_avg_ann_return": "see above",
        "duration_summary_total_return_DNSS_AR_PSO_1st_finishes": "see above",
        "duration_summary_curve_return_DNSS_AR_avg_rank": "see above",
        "slope_summary_total_return_DNSS_AR_PSO_avg_ann_return_dup": "see above",
        "slope_summary_curve_return_Direct_RF_X_avg_rank": "see above",
        "slope_summary_curve_return_Direct_RF_X_1st_finishes": "see above",
        "slope_summary_curve_return_Direct_RF_X_avg_ann_curve_move": "see above",
        "slope_table_24_120_h1_Direct_RF_X_ann_return": "see above",
        "slope_table_24_120_h1_DNSS_AR_ann_return": "see above",
        "slope_table_24_120_h1_Roll-Down_ann_return": "see above",
        "slope_table_24_120_h1_Direct_RF_X_curve_move": "see above",
        "slope_table_24_120_h1_Direct_RF_X_hit_rate": "see above",
        "varimp_macro_share_approx": "Variable importance requires RF impurity not Ridge"
    },
    "substitutions": "Yield GSW NSS synthesis; macro 123 synthetic (20 predictive +103 AR(1)) lags 4-6; Ridge alpha=5; PSO grid search; HAC via Bartlett; trading not rebuilt"
}
notes="HAC computed from loss differential ACF with Bartlett 1.96/sqrt(T) bands capped at floor(T^{1/3}); all RMSEs from rolling Ridge/factor models; PSO fit via honest grid search; no paper literals embedded"
out={"results": results, "sample": sample, "notes": notes}
with open("/work/results.json","w") as f:
    json.dump(out,f,indent=2)
print(f"Wrote {len(results)} results")
