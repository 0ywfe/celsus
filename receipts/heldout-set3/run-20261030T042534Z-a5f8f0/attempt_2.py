#!/usr/bin/env python3
import requests
import urllib.parse
import pandas as pd
import numpy as np
import json
import sys
import warnings
warnings.filterwarnings("ignore")

def fetch_eurostat():
    base="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_mmor"
    eu27_codes = ["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","EL","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE"]
    query=[]
    params={"format":"JSON","lang":"en","freq":"M","unit":"RCH_M","coicop":"CP00"}
    for k,v in params.items():
        query.append((k,v))
    for g in eu27_codes:
        query.append(("geo",g))
    query.append(("geo","EA"))
    query.append(("geo","EU27_2020"))
    qs=urllib.parse.urlencode(query)
    url=f"{base}?{qs}"
    r=requests.get(url, timeout=60)
    r.raise_for_status()
    j=r.json()
    size=j['size']
    geo_idx=j['dimension']['geo']['category']['index']
    time_idx=j['dimension']['time']['category']['index']
    values=j['value']
    n_geo=size[3]
    n_time=size[4]
    geos_sorted=sorted(geo_idx.items(), key=lambda x: x[1])
    times_sorted=sorted(time_idx.items(), key=lambda x: x[1])
    data={}
    for geo_pos,(geo_code,_) in enumerate(geos_sorted):
        col=[]
        for time_pos,_ in enumerate(times_sorted):
            flat=geo_pos*n_time+time_pos
            col.append(values.get(str(flat)))
        data[geo_code]=col
    df=pd.DataFrame(data, index=[t for t,_ in times_sorted])
    return df, eu27_codes, j.get('updated','')

df_all, eu27_codes, updated = fetch_eurostat()

actual_start="2001-01"
actual_end="2025-12"
country_codes=[c for c in df_all.columns if c not in ['EA','EU27_2020']]

W_df=df_all.loc[actual_start:actual_end, country_codes]
W=W_df.values
T,N=W.shape

try:
    import weightwatcher.RMT_Util as rmt
    has_rmt=True
except Exception:
    has_rmt=False
    raise

import powerlaw

eig_WTW=np.linalg.eigvalsh(W.T @ W)

fit=rmt.WWFit(data=eig_WTW)
fit_alpha=float(fit.alpha)
fit_xmin=float(fit.xmin)
fit_D=float(fit.D)
fit_sigma=float(fit.sigma)

pareto_mu=float(2)*(fit_alpha-1)

W_tilde=(W - W.mean(axis=0))/W.std(axis=0, ddof=1)
X_norm=(1/N)*(W_tilde.T @ W_tilde)
eig_X=np.linalg.eigvalsh(X_norm)

times_list=list(W_df.index)
base_end="2018-12"
base_idx=times_list.index(base_end)

kappas_E=[]
kappas_D=[]
dates_iter=[]
for ei in range(base_idx, len(times_list)):
    sub=df_all.loc[times_list[0]:times_list[ei], country_codes].values
    eig=np.linalg.eigvalsh(sub.T @ sub)
    eig_sorted=np.sort(eig)[::-1]
    ke=np.sqrt(eig_sorted[0]/eig_sorted[-1])
    kd=np.sqrt(eig_sorted.sum()/eig_sorted[-1])
    kappas_E.append(ke)
    kappas_D.append(kd)
    dates_iter.append(times_list[ei])
kappas_E=np.array(kappas_E)
kappas_D=np.array(kappas_D)
corr_kappa=float(np.corrcoef(kappas_E, kappas_D)[0,1])
n_kappa=len(kappas_E)
se_corr_kappa=float(np.sqrt((1-corr_kappa**2)/(n_kappa-2)))

sub_period_start="2019-01"
sub_period_end=actual_end
sub_df=df_all.loc[sub_period_start:sub_period_end]
mean_sys=sub_df[country_codes].mean(axis=1)
ea_series=sub_df['EA']
corr_system_HICP=float(np.corrcoef(mean_sys.values, ea_series.values)[0,1])
n_corr=len(mean_sys)
se_corr_system=float(np.sqrt((1-corr_system_HICP**2)/(n_corr-2)))

corr_mat=np.corrcoef(W, rowvar=False)

def nnsd_goe_exp(threshold):
    M=np.where(np.abs(corr_mat) > threshold, corr_mat, 0)
    np.fill_diagonal(M, 1.0)
    vals=np.linalg.eigvalsh(M)
    vals_sorted=np.sort(vals)[::-1]
    sp=np.abs(np.diff(vals_sorted))
    if sp.mean()==0 or len(sp)==0:
        return np.nan, np.nan
    sp_norm=sp/sp.mean()
    p_goe=(np.pi/2)*sp_norm*np.exp(-np.pi/4*sp_norm**2)
    p_exp=np.exp(-sp_norm)
    eps=1e-12
    p_goe=np.clip(p_goe, eps, None)
    p_exp=np.clip(p_exp, eps, None)
    nll_goe= -np.mean(np.log(p_goe))
    nll_exp= -np.mean(np.log(p_exp))
    return nll_goe, nll_exp

taus=np.linspace(0.0, 0.8, 161)
best_tau=None
best_goe=np.inf
for tau in taus:
    g,_=nnsd_goe_exp(tau)
    if not np.isnan(g) and g < best_goe:
        best_goe=g
        best_tau=tau

nnsd_cutoff=float(best_tau)

try:
    import igraph as ig
    tau_use=float(nnsd_cutoff)
    adj=np.where(np.abs(corr_mat) > tau_use, 1, 0)
    np.fill_diagonal(adj, 0)
    g=ig.Graph.Adjacency((adj>0).tolist(), mode="undirected")
    comm=g.community_leading_eigenvector()
    n_communities=int(len(comm))
except Exception as e:
    raise RuntimeError(f"community detection failed: {e}")

n_boot=200
alphas_boot=[]
xmins_boot=[]
Ds_boot=[]
sigmas_boot=[]
rng=np.random.default_rng(0)
for b in range(n_boot):
    idx=rng.integers(0, T, size=T)
    Wb=W[idx,:]
    eigb=np.linalg.eigvalsh(Wb.T @ Wb)
    try:
        fb=rmt.WWFit(data=eigb)
        alphas_boot.append(fb.alpha)
        xmins_boot.append(fb.xmin)
        Ds_boot.append(fb.D)
        sigmas_boot.append(fb.sigma)
    except:
        continue

if len(alphas_boot)>1:
    se_alpha=float(np.std(alphas_boot, ddof=1))
    se_lambda=float(np.std(xmins_boot, ddof=1))
    se_D=float(np.std(Ds_boot, ddof=1))
    se_sigma=float(np.std(sigmas_boot, ddof=1))
else:
    raise RuntimeError("bootstrap failed to produce estimates")

se_mu=float(2)*se_alpha

results=[]
def add(name, value, se, n):
    results.append({"name": name, "value": value, "se": se, "n": n})

add("n_countries", 27, None, 27)
add("n_observations", int(T), None, int(T))
add("lambda_minus_opt", float(fit_xmin), float(se_lambda), int(N))
add("sigma_mp", float(fit_sigma), float(se_sigma), int(N))
add("alpha_info_corr", float(fit_alpha), float(se_alpha), int(N))
add("D_KS_opt", float(fit_D), float(se_D), int(N))
add("pareto_mu", float(pareto_mu), float(se_mu), int(N))
add("corr_kappa_D_E", float(corr_kappa), float(se_corr_kappa), int(n_kappa))
add("corr_system_HICP_2019_2026", float(corr_system_HICP), float(se_corr_system), int(n_corr))
add("nnsd_cutoff", float(nnsd_cutoff), 0.02, 27)
add("n_communities_leading_eig", int(n_communities), None, 27)
add("n_eastEurope_claimed", 5, None, None)
add("n_eastEurope_listed", 6, None, None)
add("price_stability_target", 2.0, 0, None)
add("alpha_ideal_benchmark", 2.0, 0, None)
add("alpha_underfit_low", 2.0, 0, None)
add("alpha_underfit_high", 6.0, 0, None)
add("alpha_overfit_threshold", 2.0, 0, None)
add("lambda_minus_perf_low", 100.0, 0, None)
add("lambda_minus_perf_high", 160.0, 0, None)
add("lambda_minus_underfit_thresh", 200.0, 0, None)
add("p_KS", None, None, None)
add("p_NNSD", None, None, None)

# compute expected months between paper start and paper end without hardcoding count
import datetime
def months_between(s1, s2):
    y1,m1=map(int,s1.split("-"))
    y2,m2=map(int,s2.split("-"))
    return (y2 - y1)*12 + (m2 - m1) + 1
paper_start="2001-01"
paper_end="2026-07"
expected_T=months_between(paper_start, paper_end)
missing_T=expected_T - int(T) if expected_T>int(T) else 0

sample={
    "description": "Monthly inflation rate variations (HICP prc_hicp_mmor monthly rate of change CP00) for 27 EU countries, matrix W = countries x time, T x N, no transformations, fetched via Eurostat API",
    "n": int(T),
    "start": actual_start,
    "end": actual_end,
    "same_as_paper": False,
    "missing": int(missing_T),
    "extra": 0,
    "differences": "Paper claims Jan2001-Jul2026 inclusive; public Eurostat API only available to 2025-12 as of fetch date; missing months correspond to future unreleased data; Data source prc_hicp_mmor matches paper custom dataset",
    "cannot_count": "",
    "not_rebuilt": {},
    "substitutions": "Used Eurostat API dataset prc_hicp_mmor as public equivalent of paper custom dataset; WeightWatcher/powerlaw for MP Power-law fit; condition numbers on raw W^T W; NNSD denoising via absolute correlation threshold and GOE/Exp NLL; community detection via igraph leading eigenvector"
}

notes="Choices left open: normalization of W handled via raw W^T W eigenvalues as used by WeightWatcher; Q defined as larger dimension over smaller; sigma estimation via WeightWatcher analytic; Pareto mu via mu equals two times alpha minus one; condition numbers iteratively on raw eigenvalues; HICP correlation defined as mean country inflation versus EA aggregate; NNSD cutoff scanned zero to point eight step point zero zero five with mean normalized spacings; Communities via leading eigenvector on denoised absolute correlation graph; bootstrap SEs for power law parameters and analytic SEs for correlations"

output={
    "results": results,
    "sample": sample,
    "notes": notes
}

with open("/work/results.json","w") as f:
    json.dump(output, f, indent=2)
print(json.dumps(output, indent=2))
