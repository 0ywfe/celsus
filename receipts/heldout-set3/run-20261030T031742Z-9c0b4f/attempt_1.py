#!/usr/bin/env python3
"""
Replicate CEE panel LRVC results from public Eurostat + World Bank data.
"""
import requests, json, time, itertools, datetime, sys
import numpy as np, pandas as pd
from scipy import stats

CEE = ['BG','CZ','EE','HR','LV','LT','HU','PL','RO','SI','SK']
CEE_ISO = {'BG':'BG','CZ':'CZ','EE':'EE','HR':'HR','LV':'LV','LT':'LT','HU':'HU','PL':'PL','RO':'RO','SI':'SI','SK':'SK'}
YEARS_REGR = list(range(1995,2024)) # 1995-2023 inclusive 29 years
YEARS_DELTA = list(range(1996,2025)) # 1996-2024 inclusive 29 intervals

def fetch_eurostat_prc():
    url='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_ppp_ind?format=JSON&lang=en'
    r=requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def fetch_eurostat_gov():
    url='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10dd_edpt1?format=JSON&lang=en'
    r=requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def fetch_eurostat_priv():
    url='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tipspd20?format=JSON&lang=en'
    r=requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def wb_fetch(country, indicator):
    url=f'https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=100&date=1990:2024'
    for attempt in range(3):
        try:
            r=requests.get(url, timeout=30)
            if r.status_code!=200:
                time.sleep(1)
                continue
            j=r.json()
            if len(j)<2 or j[1] is None:
                return {}
            return {int(e['date']): float(e['value']) for e in j[1] if e['value'] is not None}
        except Exception as e:
            time.sleep(1)
    return {}

def build_panel():
    print("Fetching Eurostat prc_ppp_ind...")
    prc = fetch_eurostat_prc()
    vals_prc = prc['value']
    sizes_prc = prc['size']
    strides_prc=[1]*len(sizes_prc)
    for i in range(len(sizes_prc)-2,-1,-1):
        strides_prc[i]=strides_prc[i+1]*sizes_prc[i+1]
    def flat_prc(dims):
        return sum(dims[i]*strides_prc[i] for i in range(len(sizes_prc)))
    # dimensions order: freq, na_item, ppp_cat, geo, time
    geo_idx_prc = prc['dimension']['geo']['category']['index']
    time_idx_prc = prc['dimension']['time']['category']['index']
    # na_item 20 = VI_PPS_EU27_2020_HAB, 4 = PLI_EU27_2020
    na_vi = prc['dimension']['na_item']['category']['index']['VI_PPS_EU27_2020_HAB']
    na_pli = prc['dimension']['na_item']['category']['index']['PLI_EU27_2020']

    print("Fetching World Bank indicators...")
    fdi_map, trade_map, gcf_map = {}, {}, {}
    for c in CEE:
        fdi = wb_fetch(c, 'BX.KLT.DINV.WD.GD.ZS')
        tr = wb_fetch(c, 'NE.TRD.GNFS.ZS')
        gcf = wb_fetch(c, 'NE.GDI.TOTL.ZS')
        fdi_map[c]=fdi; trade_map[c]=tr; gcf_map[c]=gcf
        # sanity check
        missing_fdi=[y for y in YEARS_REGR if y not in fdi]
        missing_tr=[y for y in YEARS_REGR if y not in tr]
        missing_gcf=[y for y in YEARS_REGR if y not in gcf]
        if missing_fdi: print(f"  WB FDI missing {c} {missing_fdi}")
        if missing_tr:  print(f"  WB Trade missing {c} {missing_tr}")
        if missing_gcf: print(f"  WB GCF missing {c} {missing_gcf}")
        time.sleep(0.2)

    # also need 2024 for Delta calculation (GDP X1 2024)
    # and for cumulative FDI up to 2024 etc but regressors only 1995-2023
    # For deltas we need X1 up to 2024
    for c in CEE:
        # ensure 2024 WB available (Trade etc not needed beyond 2023, but check)
        pass

    print("Fetching Eurostat gov debt...")
    gov = fetch_eurostat_gov()
    vals_gov = gov['value']; sizes_gov=gov['size']
    strides_gov=[1]*len(sizes_gov)
    for i in range(len(sizes_gov)-2,-1,-1): strides_gov[i]=strides_gov[i+1]*sizes_gov[i+1]
    def flat_gov(dims): return sum(dims[i]*strides_gov[i] for i in range(len(sizes_gov)))
    geo_idx_gov = gov['dimension']['geo']['category']['index']
    time_idx_gov = gov['dimension']['time']['category']['index']
    unit_gov = gov['dimension']['unit']['category']['index']['PC_GDP']
    sec_gov = gov['dimension']['sector']['category']['index']['S13'] # general gov (matches most)
    gd_gov = gov['dimension']['na_item']['category']['index']['GD']

    print("Fetching Eurostat private debt...")
    priv = fetch_eurostat_priv()
    vals_priv = priv['value']; sizes_priv=priv['size']
    strides_priv=[1]*len(sizes_priv)
    for i in range(len(sizes_priv)-2,-1,-1): strides_priv[i]=strides_priv[i+1]*sizes_priv[i+1]
    def flat_priv(dims): return sum(dims[i]*strides_priv[i] for i in range(len(sizes_priv)))
    geo_idx_priv = priv['dimension']['geo']['category']['index']
    time_idx_priv = priv['dimension']['time']['category']['index']
    unit_priv = priv['dimension']['unit']['category']['index']['PC_GDP']

    # Build arrays
    # X matrix for 1995-2023 regressors (319 rows)
    NT = len(CEE)*len(YEARS_REGR) # 319
    X = np.zeros((NT,7))
    # also need X1_1995..2024 for Δy (330 values)
    X1_by_ctry = {c:{} for c in CEE}
    X2_by_ctry = {c:{} for c in CEE}

    row=0
    for c in CEE:
        # cumulative trackers per country
        fdi_cum=0.0
        gcf_cum=0.0
        for yr in YEARS_REGR:
            t_prc = time_idx_prc[str(yr)]
            g_prc = geo_idx_prc[c]
            x1 = vals_prc[str(flat_prc([0, na_vi, 0, g_prc, t_prc]))]
            x2 = vals_prc[str(flat_prc([0, na_pli, 0, g_prc, t_prc]))]
            X1_by_ctry[c][yr]=x1
            X2_by_ctry[c][yr]=x2
            fdi_cum += fdi_map[c][yr]
            x4 = trade_map[c][yr]
            gcf_cum += gcf_map[c][yr]
            t_gov = time_idx_gov[str(yr)]
            g_gov = geo_idx_gov[c]
            x6 = vals_gov[str(flat_gov([0, unit_gov, sec_gov, gd_gov, g_gov, t_gov]))]
            t_priv = time_idx_priv[str(yr)]
            g_priv = geo_idx_priv[c]
            x7 = vals_priv[str(flat_priv([0, unit_priv,0,0,0,0,g_priv, t_priv]))]
            X[row,0]=x1
            X[row,1]=x2
            X[row,2]=fdi_cum
            X[row,3]=x4
            X[row,4]=gcf_cum
            X[row,5]=x6
            X[row,6]=x7
            row+=1
        # also need 2024 for X1 to compute Δy last year
        yr=2024
        t_prc = time_idx_prc[str(yr)]
        g_prc = geo_idx_prc[c]
        x1_2024 = vals_prc[str(flat_prc([0, na_vi, 0, g_prc, t_prc]))]
        X1_by_ctry[c][yr]=x1_2024
        # X2 2024 not needed as regressor but fetch for completeness
        try:
            x2_2024 = vals_prc[str(flat_prc([0, na_pli, 0, g_prc, t_prc]))]
            X2_by_ctry[c][yr]=x2_2024
        except:
            pass

    print(f"Built X matrix {X.shape}, any NaN? {np.isnan(X).any()}")
    # Check means quickly
    mu = X.mean(axis=0)
    sigma = X.std(axis=0, ddof=1)
    print("mu", mu)
    print("sigma", sigma)
    return X, X1_by_ctry, mu, sigma, fdi_map, trade_map, gcf_map, prc, gov, priv

def descriptive_block(X):
    cols=['X1','X2','X3','X4','X5','X6','X7']
    res={}
    for j in range(7):
        col=X[:,j]
        res[f'{cols[j]}_mean']=float(np.mean(col))
        res[f'{cols[j]}_SD']=float(np.std(col, ddof=1))
        res[f'{cols[j]}_Min']=float(np.min(col))
        res[f'{cols[j]}_Max']=float(np.max(col))
        res[f'{cols[j]}_Median']=float(np.median(col))
        res[f'{cols[j]}_Skew']=float(stats.skew(col, bias=False))
        res[f'{cols[j]}_Kurt']=float(stats.kurtosis(col, fisher=False, bias=False)) # Pearson kurt (3 for normal)
    return res

def correlation_matrix(X):
    mu=X.mean(axis=0); sigma=X.std(axis=0, ddof=1)
    Z=(X-mu)/sigma
    corr=np.corrcoef(Z, rowvar=False)
    return corr, mu, sigma, Z

def compute_VIF(Z):
    # Z standardized, correlation matrix
    # VIF_j = 1/(1 - R2_j) where R2_j is regression of Z_j on other Zs
    vif=[]
    for j in range(Z.shape[1]):
        y=Z[:,j]
        X_other=np.delete(Z, j, axis=1)
        # add intercept?
        # For standardized, no intercept needed (mean zero). Regress without intercept.
        # Solve least squares
        beta, res, _, _ = np.linalg.lstsq(X_other, y, rcond=None)
        yhat=X_other @ beta
        ss_res=np.sum((y-yhat)**2)
        ss_tot=np.sum((y - y.mean())**2)
        r2=1-ss_res/ss_tot if ss_tot!=0 else 0
        vif_j=1/(1-r2) if r2<0.9999 else 999
        vif.append(vif_j)
    return vif

def run_LRVC(X, X1_by_ctry, mu, sigma):
    # Build orthogonal basis W
    NT=X.shape[0]
    mu_pooled=mu
    sigma_pooled=sigma
    Z=(X - mu_pooled)/sigma_pooled
    Omega = (Z.T @ Z)/(NT-1) # correlation
    # eigh
    lambdas, W = np.linalg.eigh(Omega) # ascending
    # Sort descending for consistency? Paper uses W Lambda W^T with diag lambda1..d. Order matters but final beta invariant if consistent.
    # Use descending order: largest eigenvalue first
    idx_sort=np.argsort(lambdas)[::-1]
    lambdas=lambdas[idx_sort]
    W=W[:, idx_sort]
    print("Omega eigenvalues", lambdas)
    print("W shape", W.shape)
    # P = Z @ W
    P = Z @ W
    # Verify orthogonality: P'P/(NT-1) should be diag(lambdas)
    PP = (P.T @ P)/(NT-1)
    print("P orthogonal check diag", np.diag(PP)[:3], "off diag max", np.max(np.abs(PP - np.diag(np.diag(PP)))))
    # For each year t=1996..2024, we need lagged X (1995..2023)
    years = list(range(1996,2025)) # 29 years
    N=11
    d=7
    # Map row index to (country, year) for X: row = c_idx*29 + y_idx where y_idx 0..28 for 1995..2023
    c_list=CEE
    year_to_idx={yr:i for i,yr in enumerate(YEARS_REGR)}
    # Build per-year results
    results_per_year={}
    residuals_all=[]
    sigma2_per_year=[]
    R2_list=[]
    adjR2_list=[]
    residSD_list=[]
    Fstat_list=[]
    # For later kappa calculation we need per-country per-year alpha/beta
    betas={} # t -> beta vector length7
    alphas={} # t -> alpha

    for t in years:
        lag_yr=t-1
        # Build y vector length N, P_lagged matrix N x d
        y=np.zeros(N)
        P_lag=np.zeros((N,d))
        X_lag=np.zeros((N,d))
        for ci,c in enumerate(c_list):
            # y = X1_t - X1_{t-1}
            y[ci]= X1_by_ctry[c][t] - X1_by_ctry[c][t-1]
            # X_lagged for this country-year = row for c, lag_yr
            row_idx = ci*len(YEARS_REGR) + year_to_idx[lag_yr]
            X_lag[ci,:]= X[row_idx,:]
            # Z_lag and P_lag
            z_lag = (X_lag[ci,:] - mu_pooled)/sigma_pooled
            P_lag[ci,:]= z_lag @ W
        # OLS in P-space: design Xp = [1, P_lag]
        Xp=np.column_stack([np.ones(N), P_lag])
        # least squares
        coef, residuals, rank, svals = np.linalg.lstsq(Xp, y, rcond=None)
        alphaP=coef[0]; gamma=coef[1:]
        yhat = Xp @ coef
        e = y - yhat
        residuals_all.extend(e.tolist())
        # metrics
        ss_res=np.sum(e**2)
        ss_tot=np.sum((y - y.mean())**2)
        R2=1-ss_res/ss_tot if ss_tot!=0 else 0
        adjR2=1-(1-R2)*(N-1)/(N-d-1) if N-d-1!=0 else np.nan
        residSD=np.sqrt(ss_res/(N-d-1)) if N-d-1>0 else np.nan
        # F-stat: (R2/d) / ((1-R2)/(N-d-1))
        Fstat=(R2/d)/((1-R2)/(N-d-1)) if (1-R2)!=0 and N-d-1!=0 else np.nan
        R2_list.append(R2); adjR2_list.append(adjR2); residSD_list.append(residSD); Fstat_list.append(Fstat)
        sigma2_per_year.append(np.mean(e**2)) # as paper: 1/N sum e^2
        # Recover beta and alpha
        # beta_j = 1/sigma_j * sum_k W_{j,k} gamma_k
        beta = (W @ gamma) / sigma_pooled  # elementwise division by sigma? Wait D^{-1} W gamma : Diag(sigma)^{-1} @ W @ gamma
        # Check: beta_j = (1/sigma_j) * sum_k W_{j,k} gamma_k -> this is row-wise
        # Our vectorized: (W @ gamma) is length7 where element j = sum_k W_{j,k} gamma_k . Then divide by sigma_j
        # That's what we did but need elementwise: W @ gamma gives sum over k for each j, then / sigma
        # Actually (W @ gamma)/sigma elementwise correct because sigma is vector
        alpha = alphaP - np.dot(mu_pooled, beta)
        betas[t]=beta
        alphas[t]=alpha
        results_per_year[t]={'alphaP':alphaP,'gamma':gamma,'beta':beta,'alpha':alpha,'e':e,'R2':R2,'adjR2':adjR2,'residSD':residSD,'F':Fstat,'y':y,'yhat':yhat}
        # compute SE via delta method
        # cov_gamma = sigma2_resid * (P_lag_centered? But include intercept)
        # For OLS, cov(coef) = s2 * inv(Xp'Xp)
        s2 = ss_res/(N-d-1) if N-d-1>0 else 0
        try:
            inv = np.linalg.inv(Xp.T @ Xp)
            cov_coef = s2 * inv
            cov_gamma = cov_coef[1:,1:] # d x d
            # cov_beta = D^{-1} W cov_gamma W^T D^{-1}
            Dinv=np.diag(1/sigma_pooled)
            cov_beta = Dinv @ W @ cov_gamma @ W.T @ Dinv
            se_beta = np.sqrt(np.diag(cov_beta))
            # se_alpha: var(alpha) = var(alphaP) + mu^T cov_beta mu -2 cov(alphaP,beta)^T mu
            # cov(alphaP, beta) = D^{-1} W cov(alphaP,gamma)
            cov_alphaP_gamma = cov_coef[0,1:] # length d
            cov_alphaP_beta = Dinv @ W @ cov_alphaP_gamma # length d? Actually W (7x7) @ cov_alphaP_gamma (7) => 7
            var_alphaP = cov_coef[0,0]
            var_alpha = var_alphaP + mu_pooled @ cov_beta @ mu_pooled -2 * mu_pooled @ cov_alphaP_beta
            se_alpha = np.sqrt(max(var_alpha,0))
        except:
            se_beta=np.zeros(d)
            se_alpha=0
        results_per_year[t]['se_beta']=se_beta
        results_per_year[t]['se_alpha']=se_alpha

    residuals_arr=np.array(residuals_all)
    return {'residuals':residuals_arr, 'per_year':results_per_year, 'W':W, 'lambdas':lambdas,
            'Omega':Omega, 'P':P,'Z':Z,'sigma2_per_year':np.array(sigma2_per_year),
            'R2':R2_list,'adjR2':adjR2_list,'residSD':residSD_list,'Fstat':Fstat_list,
            'betas':betas,'alphas':alphas,'mu':mu,'sigma':sigma}

def main():
    X, X1_by_ctry, mu, sigma, fdi_map, trade_map, gcf_map, prc, gov, priv = build_panel()

    # Descriptive stats
    desc=descriptive_block(X)
    print("Descriptive X1 mean", desc['X1_mean'], "paper 62.492")
    print("X1 SD", desc['X1_SD'], "paper 17.035")
    print("X2 mean", desc['X2_mean'], "paper 59.906")
    print("X3 mean", desc['X3_mean'], "paper 77.057? our 78.408")

    # Correlations
    corr, mu2, sigma2, Z = correlation_matrix(X)
    print("Corr X1X2", corr[0,1], "paper 0.801")

    # VIF
    vif=compute_VIF(Z)
    print("VIF", vif, "paper 1.1-4.0 mean 2.6")

    # LRVC
    lrvc=run_LRVC(X, X1_by_ctry, mu, sigma)
    residuals=lrvc['residuals']
    # pooled residual stats
    mean_res=np.mean(residuals)
    sd_res=np.std(residuals, ddof=1)
    median_res=np.median(residuals)
    skew_res=stats.skew(residuals, bias=False)
    kurt_res=stats.kurtosis(residuals, fisher=False, bias=False)
    q25=np.percentile(residuals,25); q75=np.percentile(residuals,75)
    iqr=q75-q25
    iqr_sd=iqr/sd_res if sd_res!=0 else 0
    # RMSE/MAE
    rmse=np.sqrt(np.mean(residuals**2))
    mae=np.mean(np.abs(residuals))
    rmse_mae=rmse/mae if mae!=0 else 0
    # JB test
    jb_stat, jb_p = stats.jarque_bera(residuals)
    print(f"Residual pooled mean {mean_res:.4f} sd {sd_res:.4f} median {median_res:.4f} skew {skew_res:.4f} kurt {kurt_res:.4f} IQR {iqr:.4f} IQR/SD {iqr_sd:.4f} RMSE/MAE {rmse_mae:.4f} JB p {jb_p:.4f}")

    # Per-country residuals (need to map residuals per year per country)
    # residuals_all is ordered by year? Actually our loop is year-major, residuals_all extend per year (11 per year) in CEE order
    # So per country: collect every 11 slice
    years=list(range(1996,2025))
    per_country_res={c:[] for c in CEE}
    idx=0
    for t in years:
        for ci,c in enumerate(CEE):
            e=lrvc['per_year'][t]['e'][ci]
            per_country_res[c].append(e)

    # Bartlett test
    # per-year variances s_i^2 = unbiased (ddof1)
    variances=[]
    for t in years:
        e=lrvc['per_year'][t]['e']
        variances.append(np.var(e, ddof=1))
    N_per=11
    k=len(years)
    n_i=np.array([N_per]*k)
    s2=np.array(variances)
    # pooled variance
    sp2=np.sum((n_i-1)*s2)/np.sum(n_i-1)
    # Bartlett statistic
    num = (np.sum(n_i-1))*np.log(sp2) - np.sum((n_i-1)*np.log(s2))
    denom = 1 + (1/(3*(k-1))) * (np.sum(1/(n_i-1)) - 1/np.sum(n_i-1))
    B=num/denom
    p_bartlett=1-stats.chi2.cdf(B, k-1)
    print(f"Bartlett B {B:.2f} df {k-1} p {p_bartlett:.4g}")
    # variance ratio
    # country SDs
    country_sds={}
    for c in CEE:
        sd=np.std(per_country_res[c], ddof=1)
        country_sds[c]=sd
    max_sd=max(country_sds.values()); min_sd=min(country_sds.values())
    var_ratio=(max_sd/min_sd)**2
    print(f"var ratio {var_ratio:.2f} max {max_sd:.3f} min {min_sd:.3f}")
    print(country_sds)

    # Per-year selected coefficients for table
    selected=[1997,2002,2009,2013,2018,2021,2024]
    for yr in selected:
        info=lrvc['per_year'][yr]
        print(f"YR{yr} alpha {info['alpha']:.3f} SE {info['se_alpha']:.3f} R2 {info['R2']:.3f} adj {info['adjR2']:.3f} sd {info['residSD']:.3f} F {info['F']:.3f}")
        for j in range(7):
            print(f"  beta X{j+1} {info['beta'][j]:.3f} SE {info['se_beta'][j]:.3f}")

    # Build kappa contributions for 2024
    # kappa_{i,t,j}= GDP1995/d + sum_{tau=1996}^t Delta y_{i,tau,j}
    # Delta y_{i,t,j}= alpha_t/d + beta_{t-1,j} x_{i,t-1,j}
    # For each country, compute GDP1995 = X1_1995 (since that's base)
    d=7
    kappas={}
    total_kappa={}
    accum_error={}
    for c in CEE:
        GDP1995=X1_by_ctry[c][1995]
        # initialize kappa_j = GDP1995/d
        kappa_j=np.full(d, GDP1995/d)
        cum_e=0
        for t in years:
            alpha=lrvc['per_year'][t]['alpha']
            beta=lrvc['per_year'][t]['beta']
            # need x_{t-1} for this country
            yi=t-1
            # get X_lagged for this country
            # X row for c, yi
            row_idx = CEE.index(c)*len(YEARS_REGR) + YEARS_REGR.index(yi)
            X_lag = X[row_idx,:]
            delta_j = alpha/d + beta*X_lag  # elementwise 7
            kappa_j += delta_j
            cum_e += lrvc['per_year'][t]['e'][CEE.index(c)]
        kappas[c]=kappa_j
        total_kappa[c]=kappa_j.sum()
        accum_error[c]=cum_e
        print(f"{c} kappa Total {total_kappa[c]:.1f} X1 {kappa_j[0]:.1f} X2 {kappa_j[1]:.1f} X3 {kappa_j[2]:.1f} X4 {kappa_j[3]:.1f} X5 {kappa_j[4]:.1f} X6 {kappa_j[5]:.1f} X7 {kappa_j[6]:.1f} e_acc {cum_e:.1f}")

    # Now build results.json entries
    results=[]
    def se_for_mean(sd,n):
        return float(sd/np.sqrt(n)) if n>0 else 0.0
    NT=319; N=11; T=29; d=7

    # Helper to add results
    def add(name, value, se, n):
        results.append({"name":name,"value":float(value) if isinstance(value,(int,float,np.floating)) else value,"se":float(se) if se is not None else None,"n":int(n) if n is not None else None})

    # Counts
    add("count_total_pooled_n", NT, 0, NT)
    add("count_N_countries", N, None, N)
    add("count_T_years", T, None, T)
    add("count_d_regressors", d, None, d)
    add("param_df", 3, None, None)
    add("VIF_threshold", 5, None, None)
    add("resid_normal_IQR_SD_benchmark", 1.35, None, None)
    add("resid_normal_RMSE_MAE_benchmark", 1.25, None, None)
    add("bartlett_df", 28, None, None)

    # Descriptive raw X1-X7 etc - we will map names as per spec
    # Provide means
    add("desc_raw_X1_mean", desc['X1_mean'], se_for_mean(desc['X1_SD'],NT), NT)
    add("desc_raw_X1_SD", desc['X1_SD'], None, NT)
    add("desc_raw_X1_Min", desc['X1_Min'], None, NT)
    add("desc_raw_X1_Median", desc['X1_Median'], None, NT)
    add("desc_raw_X1_Max", desc['X1_Max'], None, NT)
    add("desc_raw_X1_Skew", desc['X1_Skew'], None, NT)
    add("desc_raw_X1_Kurt", desc['X1_Kurt'], None, NT)
    add("desc_raw_X2_mean", desc['X2_mean'], se_for_mean(desc['X2_SD'],NT), NT)
    add("desc_raw_X2_SD", desc['X2_SD'], None, NT)
    add("desc_raw_X2_Min", desc['X2_Min'], None, NT)
    add("desc_raw_X2_Median", desc['X2_Median'], None, NT)
    add("desc_raw_X2_Max", desc['X2_Max'], None, NT)
    # X3
    add("desc_raw_X3_mean", desc['X3_mean'], se_for_mean(desc['X3_SD'],NT), NT)
    add("desc_raw_X3_SD", desc['X3_SD'], None, NT)
    # X4
    add("desc_raw_X4_mean", desc['X4_mean'], se_for_mean(desc['X4_SD'],NT), NT)
    add("desc_raw_X4_SD", desc['X4_SD'], None, NT)
    # X5
    add("desc_raw_X5_mean", desc['X5_mean'], se_for_mean(desc['X5_SD'],NT), NT)
    add("desc_raw_X5_SD", desc['X5_SD'], None, NT)
    # X6
    add("desc_raw_X6_mean", desc['X6_mean'], se_for_mean(desc['X6_SD'],NT), NT)
    add("desc_raw_X6_SD", desc['X6_SD'], None, NT)
    # X7
    add("desc_raw_X7_mean", desc['X7_mean'], se_for_mean(desc['X7_SD'],NT), NT)
    add("desc_raw_X7_SD", desc['X7_SD'], None, NT)

    # country-specific examples
    # For Bulgaria X1 mean, compute per-country mean over 29 years (1995-2023)
    # Use X rows per country
    for ci,c in enumerate(CEE):
        rows=X[ci*len(YEARS_REGR):(ci+1)*len(YEARS_REGR),:]
        country_means=rows.mean(axis=0)
        country_sds=rows.std(axis=0, ddof=1)
        # Delta y per country mean
        deltas=[X1_by_ctry[c][t]-X1_by_ctry[c][t-1] for t in years]
        delta_mean=np.mean(deltas); delta_sd=np.std(deltas, ddof=1)
        # Only add requested ones to avoid too many
        if c=='BG':
            add("country_Bulgaria_X1_mean", country_means[0], se_for_mean(country_sds[0],T), T)
            add("country_Bulgaria_X1_SD", country_sds[0], None, T)
        if c=='CZ':
            add("country_Czechia_X1_mean", country_means[0], se_for_mean(country_sds[0],T), T)
        if c=='EE':
            add("country_Estonia_X1_mean", country_means[0], se_for_mean(country_sds[0],T), T)
        if c=='LT':
            add("country_Lithuania_Delta_y_mean", delta_mean, se_for_mean(delta_sd,T), T)
        if c=='PL':
            add("country_Poland_Delta_y_mean", delta_mean, se_for_mean(delta_sd,T), T)

    # correlations
    add("corr_X1_X2", corr[0,1], None, NT)
    add("corr_X1_X3", corr[0,2], None, NT)
    add("corr_X4_X5", corr[3,4], None, NT)
    add("corr_X6_X7", corr[5,6], None, NT)

    # VIF
    add("VIF_low", min(vif), None, None)
    add("VIF_high", max(vif), None, None)
    add("VIF_mean", float(np.mean(vif)), None, None)

    # residual pooled
    add("resid_pooled_mean", mean_res, se_for_mean(sd_res,NT), NT)
    add("resid_pooled_SD", sd_res, None, NT)
    add("resid_pooled_median", median_res, None, NT)
    add("resid_pooled_skew", skew_res, None, NT)
    add("resid_pooled_kurt", kurt_res, None, NT)
    add("resid_pooled_Q25", q25, None, NT)
    add("resid_pooled_Q75", q75, None, NT)
    add("resid_pooled_IQR", iqr, None, NT)
    add("resid_pooled_RMSE_MAE", rmse_mae, None, NT)
    add("resid_pooled_IQR_SD_ratio", iqr_sd, None, NT)
    add("JB_pvalue", jb_p, None, NT)
    add("median_deviation_percent_SD", abs(median_res)/sd_res*100 if sd_res!=0 else 0, None, NT)

    # country residual stats
    # Use precomputed per_country_res
    for c in ['Czechia','Latvia','Poland','Hungary','Bulgaria']:
        # map name to code
        code_map={'Czechia':'CZ','Latvia':'LV','Poland':'PL','Hungary':'HU','Bulgaria':'BG'}
        code=code_map[c]
        vals=np.array(per_country_res[code])
        if c=='Czechia':
            add("resid_Czechia_mean", float(np.mean(vals)), se_for_mean(np.std(vals,ddof=1),T), T)
            add("resid_Czechia_SD", float(np.std(vals,ddof=1)), None, T)
        if c=='Latvia':
            add("resid_Latvia_mean", float(np.mean(vals)), se_for_mean(np.std(vals,ddof=1),T), T)
            add("resid_Latvia_SD", float(np.std(vals,ddof=1)), None, T)
        if c=='Poland':
            add("resid_Poland_SD", float(np.std(vals,ddof=1)), None, T)
        if c=='Hungary':
            add("resid_Hungary_SD", float(np.std(vals,ddof=1)), None, T)

    add("resid_variance_ratio", var_ratio, None, None)
    add("bartlett_B", B, None, NT)
    add("bartlett_p", float(p_bartlett), None, None) # spec expects "< 0.001" but we give numeric
    # but spec expects value "< 0.001" string? We'll try numeric
    # Actually spec says bartlett_p value "< 0.001" - we should put that string if needed, but JSON value must be number? We'll give 0.0005 as proxy
    # We'll handle: if p<0.001 we can still give numeric p
    # Keep numeric

    # alpha and beta selected years
    for yr in selected:
        info=lrvc['per_year'][yr]
        add(f"alpha_{yr}", float(info['alpha']), float(info['se_alpha']), N)
        add(f"alpha_{yr}_SE", float(info['se_alpha']), None, N)
    # Beta X1 selected
    mapping={1997:'beta_X1_1997',2002:'beta_X1_2002',2009:'beta_X1_2009',2013:'beta_X1_2013'}
    for yr,name in mapping.items():
        info=lrvc['per_year'][yr]
        add(name, float(info['beta'][0]), float(info['se_beta'][0]), N)
    # X2
    for yr,name in [(1997,'beta_X2_1997'),(2009,'beta_X2_2009'),(2013,'beta_X2_2013')]:
        info=lrvc['per_year'][yr]
        # find index 1
        add(name, float(info['beta'][1]), float(info['se_beta'][1]), N)
    # X7
    for yr,name in [(1997,'beta_X7_1997'),(2002,'beta_X7_2002'),(2013,'beta_X7_2013'),(2018,'beta_X7_2018'),(2024,'beta_X7_2024')]:
        info=lrvc['per_year'][yr]
        add(name, float(info['beta'][6]), float(info['se_beta'][6]), N)

    # R2 etc
    for yr,name in [(1997,'R2_1997'),(2009,'R2_2009'),(2024,'R2_2024')]:
        info=lrvc['per_year'][yr]
        add(name, float(info['R2']), None, N)
        # also adj
        if yr==1997:
            add("AdjR2_1997", float(info['adjR2']), None, N)
        if yr==2024:
            add("AdjR2_2024", float(info['adjR2']), None, N)
        # residSD
        if yr==1997:
            add("ResidSD_1997", float(info['residSD']), None, N)
        if yr==2009:
            add("ResidSD_2009", float(info['residSD']), None, N)
        if yr==2024:
            add("ResidSD_2024", float(info['residSD']), None, N)
        # F
        if yr==1997:
            add("Fstat_1997", float(info['F']), None, N)
        if yr==2009:
            add("Fstat_2009", float(info['F']), None, N)
        if yr==2024:
            add("Fstat_2024", float(info['F']), None, N)

    # kappa contributions 2024
    # Use order as per Table1: columns X2, Total, X3, X4, X5, X6, X7, X1, e_acc
    # We'll provide the ones requested in spec
    # For Bulgaria
    ck=kappas['BG']
    add("kappa_Total_Bulgaria_2024", float(total_kappa['BG']), None, None)
    add("kappa_X2_Bulgaria_2024", float(ck[1]), None, None)
    add("kappa_X7_Bulgaria_2024", float(ck[6]), None, None)
    add("kappa_X1_Bulgaria_2024", float(ck[0]), None, None)
    # Czechia
    add("kappa_X7_Czechia_2024", float(kappas['CZ'][6]), None, None)
    add("kappa_X7_Estonia_2024", float(kappas['EE'][6]), None, None)
    add("kappa_X7_Latvia_2024", float(kappas['LV'][6]), None, None)
    add("kappa_X7_Lithuania_2024", float(kappas['LT'][6]), None, None)
    add("kappa_X7_Poland_2024", float(kappas['PL'][6]), None, None)
    add("kappa_X7_Romania_2024", float(kappas['RO'][6]), None, None)
    add("kappa_X7_Slovenia_2024", float(kappas['SI'][6]), None, None)
    add("kappa_X7_Slovakia_2024", float(kappas['SK'][6]), None, None)
    add("kappa_Total_Lithuania_2024", float(total_kappa['LT']), None, None)
    add("kappa_Total_Estonia_2024", float(total_kappa['EE']), None, None)
    # accum errors
    add("accum_error_Bulgaria_2024", float(accum_error['BG']), None, None)
    add("accum_error_Czechia_2024", float(accum_error['CZ']), None, None)
    add("accum_error_Latvia_2024", float(accum_error['LV']), None, None)
    add("accum_error_Lithuania_2024", float(accum_error['LT']), None, None)

    # Build sample description
    sample={
        "description": f"Panel of 11 CEE countries {', '.join(CEE)} observed 1995-2024; regressors X1-X7 levels lagged t-1 for 1995-2023 (NT=319); Δy 1996-2024; orthogonalized via pooled W; yearly OLS N=11",
        "n": NT,
        "start": "1995-01-01",
        "end": "2024-12-31",
        "same_as_paper": False, # due to vintage differences
        "missing": 0,
        "extra": 0,
        "differences": "Gov debt vintage BG 1996 outlier 244.5 vs paper 99 max; X3 FDI SK vintage difference; pooled X3 mean 78.4 vs 77.06; X6 pooled mean 38.76 vs 38.37 due to outlier",
        "cannot_count": "",
        "not_rebuilt": {},
        "substitutions": "Eurostat prc_ppp_ind for X1 X2; World Bank BX.KLT.DINV.WD.GD.ZS cumulated for X3, NE.TRD.GNFS.ZS for X4, NE.GDI.TOTL.ZS cumulated for X5; Eurostat gov_10dd_edpt1 S13 general gov debt for X6 (paper says central but S13 matches most means); Eurostat tipspd20 for X7. Current Eurostat vintage has BG gov outlier; SK FDI revision."
    }
    notes="Choices: Eurostat prc_ppp_ind API used; X3 cumulated net FDI inflows %GDP from 1995 start (paper accumulated FDI cum. %GDP); X5 cumulated GCF %GDP; X6 used general gov debt S13 because central S1311 sparse and S13 means match paper except BG outlier - noted as vintage difference; World Bank data vintage 2025-2026 may differ slightly from paper's 2024 vintage affecting SK FDI; orthogonalization via eigendecomp of pooled correlation with descending eigenvalues; yearly OLS N=11 d=7 df=3; SE via delta method D^{-1}W cov(gamma) W^T D^{-1}; Bartlett heteroskedasticity test as defined; JB test via scipy; kappa contributions via alpha/d + beta*x and cumulative sum from GDP1995/d."

    output={"results":results,"sample":sample,"notes":notes}
    with open("/work/results.json","w") as f:
        json.dump(output,f,indent=2)
    print("Wrote /work/results.json with",len(results),"results")

if __name__=="__main__":
    main()
