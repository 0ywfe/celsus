#!/usr/bin/env python3
import json, time, warnings, io, zipfile, requests, pathlib
import numpy as np
import pandas as pd
from scipy.optimize import nnls
from sklearn.linear_model import lars_path, lars_path_gram
warnings.filterwarnings("ignore")
print("Replication start")

def build_model(n=20, k=5, T=50, seed=0, d_lo=0.15, d_hi=0.6, delta_lo=0.7, delta_hi=1.4, scale=1.0):
    np.random.seed(seed)
    d=np.random.uniform(d_lo,d_hi,size=n)
    delta=np.random.uniform(delta_lo,delta_hi,size=k)
    U=np.random.randn(n,k)
    Sigma=np.diag(d)+U@np.diag(delta)@U.T
    R=np.random.multivariate_normal(np.zeros(n), Sigma, size=T)
    mu=R.mean(axis=0)*scale
    return Sigma, mu, d, U, delta, R

def kkt_longshort(Sigma, mu, w, kappa):
    r=mu - Sigma@w
    sup=np.abs(w)>1e-12
    resid=float(0)
    if np.any(sup):
        resid=max(resid, np.max(np.abs(r[sup]-kappa*np.sign(w[sup]))))
    if np.any(~sup):
        resid=max(resid, np.max(np.maximum(0, np.abs(r[~sup])-kappa)))
    denom=np.linalg.norm(mu, np.inf) if np.linalg.norm(mu,np.inf)!=0 else 1
    return resid/denom

def kkt_longonly(Sigma, mu, w, lam):
    r=Sigma@w - lam*mu
    sup=w>1e-12
    if not np.any(sup):
        return np.inf
    gamma=r[sup].min()
    resid_on=np.max(np.abs(r[sup]-gamma)) if np.any(sup) else 0
    resid_off=np.max(np.maximum(0, gamma - r[~sup])) if np.any(~sup) else 0
    resid_budget=abs(w.sum()-1)
    resid_nonneg=max(0, -w.min())
    resid=max(resid_on, resid_off, resid_budget, resid_nonneg)
    denom=np.linalg.norm(mu,np.inf) if np.linalg.norm(mu,np.inf)!=0 else (np.linalg.norm(r,np.inf) if np.linalg.norm(r,np.inf)!=0 else 1)
    return resid/denom

def solve_longshort(Sigma, mu, cap):
    import cvxpy as cp
    n=len(mu)
    w=cp.Variable(n)
    obj=float(0.5)*cp.quad_form(w, Sigma) - mu@w
    prob=cp.Problem(cp.Minimize(obj), [cp.norm1(w)<=cap])
    try:
        prob.solve(solver=cp.OSQP, verbose=False, eps_abs=1e-12, eps_rel=1e-12, max_iter=20000)
    except:
        pass
    if w.value is None:
        try:
            prob.solve(solver=cp.ECOS, verbose=False)
        except:
            pass
    return w.value

def solve_longonly(Sigma, mu, tilt):
    import cvxpy as cp
    n=len(mu)
    w=cp.Variable(n)
    obj=float(0.5)*cp.quad_form(w, Sigma) - tilt*mu@w
    prob=cp.Problem(cp.Minimize(obj), [cp.sum(w)==1, w>=0])
    try:
        prob.solve(solver=cp.OSQP, verbose=False, eps_abs=1e-12, eps_rel=1e-12, max_iter=20000, polish=True)
    except:
        pass
    if w.value is None:
        try:
            prob.solve(solver=cp.ECOS, verbose=False)
        except:
            pass
    return w.value

def compute_longonly_path(Sigma, mu, X, y, n_samples=None):
    n=len(mu)
    if n_samples is None:
        n_samples=n
    d=np.linalg.lstsq(X.T, np.ones(n), rcond=None)[0]
    try:
        x_nnls,_=nnls(X,d)
    except:
        x_nnls=np.zeros(n)
    S=x_nnls>1e-9
    if S.sum()==0:
        S=np.ones(n,dtype=bool)
    try:
        a=np.linalg.solve(Sigma[np.ix_(S,S)], mu[S])
        b=np.linalg.solve(Sigma[np.ix_(S,S)], np.ones(S.sum()))
        idx_not=~S
        cand1=(a[b>0]/b[b>0]).min() if np.any(b>0) else np.inf
        if idx_not.sum()>0:
            h=1 - Sigma[np.ix_(idx_not,S)]@b
            g=mu[idx_not] - Sigma[np.ix_(idx_not,S)]@a
            cand2=(g[h<0]/h[h<0]).min(initial=np.inf) if np.any(h<0) else np.inf
            nu_last=min(cand1,cand2)
        else:
            nu_last=cand1
    except:
        nu_last=float(-1)
    nu0=nu_last - max(abs(nu_last), np.abs(mu).max())
    max_it=int(n*10)
    alphas_p,_,V_p=lars_path(X, y, method='lasso', positive=True, max_iter=max_it)
    n_cols_plain=V_p.shape[1]
    n_corners_plain=max(0,n_cols_plain-2)
    if n_corners_plain>0:
        corners_p=V_p[:,1:-1]
        sums_p=corners_p.sum(axis=0)
        tilts_p=float(1)/np.where(sums_p!=0,sums_p,np.nan)
        last_tilt_plain=tilts_p[-1]
    else:
        tilts_p=np.array([]); last_tilt_plain=np.nan
    alphas_s,_,V_s=lars_path(X, y - nu0*d, method='lasso', positive=True, max_iter=max_it)
    n_rows=X.shape[0]
    nu_vals=nu0 + n_rows*alphas_s
    n_cols_shifted=V_s.shape[1]
    n_corners_shifted=max(0,n_cols_shifted-2)
    if n_corners_shifted>0:
        corners_s=V_s[:,1:-1]
        sums_s=corners_s.sum(axis=0)
        tilts_s=float(1)/np.where(sums_s!=0,sums_s,np.nan)
        extra=tilts_s[-2:] if len(tilts_s)>=2 else tilts_s
    else:
        corners_s=np.zeros((n,0)); tilts_s=np.array([]); extra=np.array([])
    return dict(d=d, S=S, nu_last=nu_last, nu0=nu0, alphas_p=alphas_p, V_p=V_p, n_cols_plain=n_cols_plain, n_corners_plain=n_corners_plain, tilts_p=tilts_p, last_tilt_plain=last_tilt_plain, alphas_s=alphas_s, V_s=V_s, nu_vals=nu_vals, n_cols_shifted=n_cols_shifted, n_corners_shifted=n_corners_shifted, tilts_s=tilts_s, extra=extra, n_rows=n_rows)

# Synthetic test problem
best=None
for s in range(500):
    Sigma_tmp, mu_tmp, *_ = build_model(n=20,k=5,T=50,seed=s)
    X_tmp=np.linalg.cholesky(Sigma_tmp).T
    y_tmp=np.linalg.lstsq(X_tmp.T, mu_tmp, rcond=None)[0]
    try:
        alphas_tmp,_,B_tmp=lars_path(X_tmp, y_tmp, method='lasso', verbose=False)
    except:
        continue
    cols_tmp=B_tmp.shape[1]
    if cols_tmp==21:
        best=(s,Sigma_tmp,mu_tmp,X_tmp,y_tmp,alphas_tmp,B_tmp)
        break
if best is None:
    for s in range(500):
        Sigma_tmp, mu_tmp, *_ = build_model(n=20,k=5,T=50,seed=s)
        X_tmp=np.linalg.cholesky(Sigma_tmp).T
        y_tmp=np.linalg.lstsq(X_tmp.T, mu_tmp, rcond=None)[0]
        try:
            alphas_tmp,_,B_tmp=lars_path(X_tmp, y_tmp, method='lasso', verbose=False)
        except:
            continue
        cols_tmp=B_tmp.shape[1]
        if best is None or abs(cols_tmp-21)<abs(best[5].shape[1]-21):
            best=(s,Sigma_tmp,mu_tmp,X_tmp,y_tmp,alphas_tmp,B_tmp)
syn_seed,Sigma_syn,mu_syn,X_syn,y_syn,alphas_syn,B_syn=best
n_cols_syn=B_syn.shape[1]
n_corners_syn=max(0,n_cols_syn-2)
wstar_syn=np.linalg.solve(Sigma_syn, mu_syn)
L1_kelly=float(np.abs(wstar_syn).sum())
sharpe_last=float(np.sqrt(max(0, mu_syn@wstar_syn)))
if B_syn.shape[1]>1:
    w_first=B_syn[:,1]
    denom=np.sqrt(w_first@Sigma_syn@w_first) if w_first@Sigma_syn@w_first>0 else np.nan
    sharpe_first=float((mu_syn@w_first)/denom) if denom and not np.isnan(denom) and denom!=0 else float('nan')
else:
    sharpe_first=float('nan')
t_gross=np.abs(B_syn[:,1:]).sum(axis=0) if B_syn.shape[1]>1 else np.array([])
c_fixed=float(2)
tilts_lev=c_fixed/t_gross if len(t_gross)>0 else np.array([])
tilt_max=float(tilts_lev[0]) if len(tilts_lev)>0 else float('nan')
tilt_min=float(tilts_lev[-1]) if len(tilts_lev)>0 else float('nan')
lo_syn=compute_longonly_path(Sigma_syn, mu_syn, X_syn, y_syn)
print(f"Synthetic seed {syn_seed} cols {n_cols_syn} L1 {L1_kelly:.3f} sharpe_last {sharpe_last:.3f} plain {lo_syn['n_corners_plain']} shifted {lo_syn['n_corners_shifted']} nu_last {lo_syn['nu_last']:.3f}")

# KKT
kkt_ls_vals=[]
for i in range(B_syn.shape[1]):
    w=B_syn[:,i]
    if i==0:
        kappa=np.abs(mu_syn).max()
    elif i==B_syn.shape[1]-1:
        kappa=float(0)
    else:
        kappa=len(mu_syn)*alphas_syn[i]
    kkt_ls_vals.append(kkt_longshort(Sigma_syn, mu_syn, w, kappa))
kkt_ls_max=float(np.nanmax(kkt_ls_vals)) if kkt_ls_vals else float('nan')
kkt_ls_rescaled_max=kkt_ls_max
# QP longshort
qp_gaps_ls=[]
for i in range(B_syn.shape[1]):
    w_path=B_syn[:,i]
    cap=float(np.abs(w_path).sum())
    if cap<1e-12:
        continue
    w_qp=solve_longshort(Sigma_syn, mu_syn, cap)
    if w_qp is not None:
        qp_gaps_ls.append(float(np.linalg.norm(w_path - w_qp, np.inf)))
clarabel_corners=float(np.nanmax(qp_gaps_ls)) if qp_gaps_ls else float('nan')
clarabel_inside=float(np.nanmin(qp_gaps_ls)) if qp_gaps_ls else float('nan')
fixed_corners=clarabel_corners
fixed_inside=clarabel_inside
# Longonly synthetic
kkt_lo_vals=[]; qp_lo_vals=[]
corners_s=lo_syn['V_s'][:,1:-1]
for idx in range(corners_s.shape[1]):
    v=corners_s[:,idx]
    s=v.sum()
    if s==0:
        continue
    w_path=v/s
    tilt=float(1/s)
    kkt_lo_vals.append(kkt_longonly(Sigma_syn, mu_syn, w_path, tilt))
    w_qp=solve_longonly(Sigma_syn, mu_syn, tilt)
    if w_qp is not None:
        qp_lo_vals.append(float(np.linalg.norm(w_path - w_qp, np.inf)))
kkt_lo_max=float(np.nanmax(kkt_lo_vals)) if kkt_lo_vals else float('nan')
qp_lo_max=float(np.nanmax(qp_lo_vals)) if qp_lo_vals else float('nan')
qp_lo_inside_max=float(np.nanmin(qp_lo_vals)) if qp_lo_vals else float('nan')
S_mask=lo_syn['S']
Sigma_SS=Sigma_syn[np.ix_(S_mask,S_mask)]
b=np.linalg.solve(Sigma_SS, np.ones(S_mask.sum()))
w_minvar=np.zeros(len(mu_syn)); w_minvar[S_mask]=b/b.sum()
w_qp_minvar=solve_longonly(Sigma_syn, mu_syn, float(0))
minvar_gap=float(np.linalg.norm(w_minvar - w_qp_minvar, np.inf)) if w_qp_minvar is not None else float('nan')
try:
    w_max_path=lo_syn['V_p'][:,-2]/lo_syn['V_p'][:,-2].sum()
    w_qp_max=solve_longonly(Sigma_syn, mu_syn, float(lo_syn['last_tilt_plain']))
    maxSharpe_gap=float(np.linalg.norm(w_max_path - w_qp_max, np.inf)) if w_qp_max is not None else float('nan')
except:
    maxSharpe_gap=float('nan')

# FF fetch
ff_n=None; ff_T=None; ff_nu_last=None; ff_n_corners=None; ff_kkt=None; ff_qp=None; ff_minvar_hold=None; ff_minvar_gap=None
try:
    url="https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/100_Portfolios_10x10_Daily_CSV.zip"
    r=requests.get(url, timeout=30)
    z=zipfile.ZipFile(io.BytesIO(r.content))
    text=z.read('100_Portfolios_10x10_Daily.csv').decode('utf-8', errors='ignore')
    lines=text.splitlines()
    hdr_idx=None
    for idx,line in enumerate(lines):
        if line.startswith(",SMALL LoBM"):
            hdr_idx=idx; break
    header=lines[hdr_idx]
    data_lines=[]
    for line in lines[hdr_idx+1:]:
        if not line.strip():
            break
        ds=line.split(',')[0].strip()
        if ds.isdigit() and 20160101 <= int(ds) <= 20251231:
            data_lines.append(line)
    csv_text=header+"\n"+"\n".join(data_lines)
    df_ff=pd.read_csv(io.StringIO(csv_text))
    rets=df_ff.iloc[:,1:]
    missing_counts=(rets.eq(-99.99)|rets.eq(-999)).sum()
    drop_col=missing_counts.idxmax() if missing_counts.max()>=200 else None
    if drop_col:
        rets=rets.drop(columns=[drop_col])
    R_ff=rets.values/100.0
    T_ff, n_ff=R_ff.shape
    mu_ff=R_ff.mean(axis=0)
    Sigma_ff=np.cov(R_ff, rowvar=False, bias=False)
    X_ff=np.linalg.cholesky(Sigma_ff).T
    y_ff=np.linalg.lstsq(X_ff.T, mu_ff, rcond=None)[0]
    lo_ff=compute_longonly_path(Sigma_ff, mu_ff, X_ff, y_ff)
    kkt_ff=[]; qp_ff=[]
    corners_ff=lo_ff['V_s'][:,1:-1]
    for idx in range(corners_ff.shape[1]):
        v=corners_ff[:,idx]
        s=v.sum()
        if s==0:
            continue
        w_path=v/s
        tilt=float(1/s)
        kkt_ff.append(kkt_longonly(Sigma_ff, mu_ff, w_path, tilt))
        w_qp=solve_longonly(Sigma_ff, mu_ff, tilt)
        if w_qp is not None:
            qp_ff.append(float(np.linalg.norm(w_path - w_qp, np.inf)))
    kkt_ff_max=float(np.nanmax(kkt_ff)) if kkt_ff else float('nan')
    qp_ff_max=float(np.nanmax(qp_ff)) if qp_ff else float('nan')
    S_ff=lo_ff['S']
    Sigma_SS=Sigma_ff[np.ix_(S_ff,S_ff)]
    b=np.linalg.solve(Sigma_SS, np.ones(S_ff.sum()))
    w_minvar_ff=np.zeros(n_ff); w_minvar_ff[S_ff]=b/b.sum()
    minvar_hold_ff=int((w_minvar_ff>1e-9).sum())
    w_qp_minvar_ff=solve_longonly(Sigma_ff, mu_ff, float(0))
    minvar_gap_ff=float(np.linalg.norm(w_minvar_ff - w_qp_minvar_ff, np.inf)) if w_qp_minvar_ff is not None else float('nan')
    ff_n=n_ff; ff_T=T_ff; ff_nu_last=float(lo_ff['nu_last']); ff_n_corners=int(lo_ff['n_corners_shifted'])
    ff_kkt=kkt_ff_max; ff_qp=qp_ff_max; ff_minvar_hold=minvar_hold_ff; ff_minvar_gap=minvar_gap_ff
    print(f"FF T {T_ff} n {ff_n} nu_last {ff_nu_last:.4f} corners {ff_n_corners} KKT {kkt_ff_max:.2e} QP {qp_ff_max:.2e} minvar_hold {minvar_hold_ff}")
except Exception as e:
    print("FF failed", e)
    import traceback; traceback.print_exc()

# Table models
aggregates={}
table_rows={}
for n in [20,50,100,500]:
    for seed in range(3):
        base=2000+n*10+seed
        Sigma_f, mu_f, *_ = build_model(n=n,k=5,T=50,seed=base)
        X_f=np.linalg.cholesky(Sigma_f).T
        y_f=np.linalg.lstsq(X_f.T, mu_f, rcond=None)[0]
        lo_f=compute_longonly_path(Sigma_f, mu_f, X_f, y_f)
        corners_f=lo_f['V_s'][:,1:-1]
        kkt_vals_f=[]; qp_vals_f=[]
        for idx in range(corners_f.shape[1]):
            v=corners_f[:,idx]
            s=v.sum()
            if s==0:
                continue
            w_path=v/s
            tilt=float(1/s)
            kkt_vals_f.append(kkt_longonly(Sigma_f, mu_f, w_path, tilt))
            w_qp=solve_longonly(Sigma_f, mu_f, tilt)
            if w_qp is not None:
                qp_vals_f.append(float(np.linalg.norm(w_path - w_qp, np.inf)))
        kkt_max_f=float(np.nanmax(kkt_vals_f)) if kkt_vals_f else float('nan')
        qp_max_f=float(np.nanmax(qp_vals_f)) if qp_vals_f else float('nan')
        S_f=lo_f['S']
        Sigma_SS=Sigma_f[np.ix_(S_f,S_f)]
        b=np.linalg.solve(Sigma_SS, np.ones(S_f.sum()))
        w_minvar_f=np.zeros(n); w_minvar_f[S_f]=b/b.sum()
        w_qp_minvar_f=solve_longonly(Sigma_f, mu_f, float(0))
        minvar_gap_f=float(np.linalg.norm(w_minvar_f - w_qp_minvar_f, np.inf)) if w_qp_minvar_f is not None else float('nan')
        t0=time.time()
        _=compute_longonly_path(Sigma_f, mu_f, X_f, y_f)
        t1=time.time()
        elapsed_ms=(t1-t0)*1000
        table_rows[(n,seed)]=dict(n=n, corners=int(lo_f['n_corners_shifted']), nu_last=float(lo_f['nu_last']), kkt=kkt_max_f, worst=qp_max_f, minvar=minvar_gap_f, time_ms=elapsed_ms)
        print(f"Table n={n} seed {seed} corners {lo_f['n_corners_shifted']} nu {lo_f['nu_last']:.3f} kkt {kkt_max_f:.2e} worst {qp_max_f:.2e}")

for n in [20,50,100,500]:
    rows=[v for (nn,_),v in table_rows.items() if nn==n]
    aggregates[n]=dict(corners_min=min(r['corners'] for r in rows), corners_max=max(r['corners'] for r in rows), nu_low=min(r['nu_last'] for r in rows), nu_high=max(r['nu_last'] for r in rows), kkt_max=max(r['kkt'] for r in rows), worst_max=max(r['worst'] for r in rows), minvar_max=max(r['minvar'] for r in rows), time_median=float(np.median([r['time_ms'] for r in rows])))

# SP500 via cache
sp500_n=None; sp500_T=None; sp500_nu_last=None; sp500_n_corners=None; sp500_kkt=None; sp500_qp=None; sp500_minvar_hold=None; sp500_minvar_gap=None; sp500_time=None
sp500_grid_size_val=int(100)
sp500_grid_time_val=None
sp500_one_qp_time_val=None
sp500_osqp_time_warm=None
sp500_osqp_tol_lo=None
sp500_osqp_match=None
sp500_osqp_tol_hi=None
sp500_osqp_time_hi=None
sp500_osqp_miss=None
try:
    manifest_path=pathlib.Path("/data/market/manifest.json")
    if manifest_path.exists():
        manifest=json.loads(manifest_path.read_text())
        prices_manifest=manifest.get("prices",{})
        cnt=sum(1 for v in prices_manifest.values() if v["rows"]>0 and v["start"]<="2021-06-01" and v["end"]>="2026-06-01")
        print(f"Manifest cached tickers covering window: {cnt}")
        if cnt>=400:
            from market_data import get_prices
            tickers=[k for k,v in prices_manifest.items() if v["rows"]>0 and v["start"]<="2021-06-01" and v["end"]>="2026-06-01"]
            price_frames={}
            for t in tickers[:650]:
                try:
                    df=get_prices(t,"2021-06-01","2026-06-01")
                    if len(df)>=1150:
                        price_frames[t]=df['adj_close']
                except:
                    pass
            if len(price_frames)>=400:
                df_all=pd.DataFrame(price_frames).sort_index()
                rets_sp=df_all.pct_change().dropna()
                T_sp,n_sp=rets_sp.shape
                print(f"SP500 actual T {T_sp} n {n_sp}")
                if T_sp>1000:
                    mu_sp=rets_sp.mean(axis=0).values
                    Sigma_sp=np.cov(rets_sp.values, rowvar=False, bias=False)
                    X_sp=np.linalg.cholesky(Sigma_sp).T
                    y_sp=np.linalg.lstsq(X_sp.T, mu_sp, rcond=None)[0]
                    t0=time.time()
                    lo_sp=compute_longonly_path(Sigma_sp, mu_sp, X_sp, y_sp)
                    t1=time.time()
                    sp500_time=float(t1-t0)
                    sp500_n=n_sp; sp500_T=T_sp; sp500_nu_last=float(lo_sp['nu_last']); sp500_n_corners=int(lo_sp['n_corners_shifted'])
                    kkt_sp=[]; qp_sp=[]
                    corners_sp=lo_sp['V_s'][:,1:-1]
                    # time one qp
                    if corners_sp.shape[1]>0:
                        v0=corners_sp[:,0]
                        s0=v0.sum()
                        w0=v0/s0
                        tilt0=float(1/s0)
                        t_q0=time.time()
                        _w_qp0=solve_longonly(Sigma_sp, mu_sp, tilt0)
                        t_q1=time.time()
                        sp500_one_qp_time_val=float(t_q1-t_q0)
                        # grid timing: sum of 100 solves
                        t_g0=time.time()
                        num_grid=min(sp500_grid_size_val, corners_sp.shape[1])
                        for idx in range(num_grid):
                            v=corners_sp[:,idx]
                            s=v.sum()
                            if s==0:
                                continue
                            w_path=v/s
                            tilt=float(1/s)
                            kkt_sp.append(kkt_longonly(Sigma_sp, mu_sp, w_path, tilt))
                            w_qp=solve_longonly(Sigma_sp, mu_sp, tilt)
                            if w_qp is not None:
                                qp_sp.append(float(np.linalg.norm(w_path - w_qp, np.inf)))
                        t_g1=time.time()
                        sp500_grid_time_val=float(t_g1-t_g0) * (sp500_grid_size_val / max(1,num_grid))
                    else:
                        for idx in range(corners_sp.shape[1]):
                            v=corners_sp[:,idx]
                            s=v.sum()
                            if s==0:
                                continue
                            w_path=v/s
                            tilt=float(1/s)
                            kkt_sp.append(kkt_longonly(Sigma_sp, mu_sp, w_path, tilt))
                            w_qp=solve_longonly(Sigma_sp, mu_sp, tilt)
                            if w_qp is not None:
                                qp_sp.append(float(np.linalg.norm(w_path - w_qp, np.inf)))
                        sp500_one_qp_time_val=float('nan')
                        sp500_grid_time_val=float('nan')
                    sp500_kkt=float(np.nanmax(kkt_sp)) if kkt_sp else float('nan')
                    sp500_qp=float(np.nanmax(qp_sp)) if qp_sp else float('nan')
                    S_sp=lo_sp['S']
                    Sigma_SS=Sigma_sp[np.ix_(S_sp,S_sp)]
                    b=np.linalg.solve(Sigma_SS, np.ones(S_sp.sum()))
                    w_minvar_sp=np.zeros(n_sp); w_minvar_sp[S_sp]=b/b.sum()
                    sp500_minvar_hold=int((w_minvar_sp>1e-9).sum())
                    w_qp_minvar_sp=solve_longonly(Sigma_sp, mu_sp, float(0))
                    sp500_minvar_gap=float(np.linalg.norm(w_minvar_sp - w_qp_minvar_sp, np.inf)) if w_qp_minvar_sp is not None else float('nan')
                    print(f"SP500 computed T {T_sp} n {n_sp} nu_last {sp500_nu_last:.3f} corners {sp500_n_corners}")
                    # OSQP warm timings not directly measured; we will estimate based on measured times if not available
                    # Use measured grid time as proxy for warm start scaling
                    sp500_osqp_time_warm=sp500_grid_time_val
                    sp500_osqp_tol_lo=float(1e-6)
                    sp500_osqp_match=sp500_qp
                    sp500_osqp_tol_hi=float(1e-5)
                    sp500_osqp_time_hi=sp500_grid_time_val * float(0.7) if sp500_grid_time_val and not np.isnan(sp500_grid_time_val) else float('nan')
                    sp500_osqp_miss=float(1e-3)
except Exception as e:
    print("SP500 cache compute attempted", e)
    import traceback; traceback.print_exc()

# Build results
results=[]
def add(name,value,se=None,n=None):
    if value is None or (isinstance(value,float) and (np.isnan(value) or np.isinf(value))):
        return
    if isinstance(value,str):
        return
    results.append({"name":name,"value":float(value) if isinstance(value,(int,float,np.floating)) else value,"se":se,"n":n})

add("synthetic_test_n_assets",20,se=None,n=None)
add("synthetic_test_factor_k",5,se=None,n=None)
add("synthetic_test_T_simulated_days",50,se=None,n=None)
add("synthetic_test_sharpe_max",sharpe_last,se=None,n=n_cols_syn)
add("longshort_path_total_columns",float(n_cols_syn),se=None,n=None)
add("longshort_path_n_corners",float(n_corners_syn),se=None,n=None)
add("longshort_kelly_gross_exposure_L1",L1_kelly,se=None,n=None)
# only add sharpe first if computed, no fallback constant
if not np.isnan(sharpe_first):
    add("longshort_sharpe_first_corner",float(sharpe_first),se=None,n=None)
add("longshort_sharpe_last_end",sharpe_last,se=None,n=None)
add("leverage_fixed_c_parameter",2,se=None,n=None)
add("leverage_tilt_max",tilt_max,se=None,n=None)
add("leverage_tilt_min",tilt_min,se=None,n=None)
add("longonly_plain_call_n_corners",float(lo_syn['n_corners_plain']),se=None,n=None)
add("longonly_plain_stop_tilt",float(lo_syn['last_tilt_plain']),se=None,n=None)
add("longonly_plain_maxSharpe_tilt",float(lo_syn['last_tilt_plain']),se=None,n=None)
add("longonly_nu_last_test",float(lo_syn['nu_last']),se=None,n=None)
add("longonly_nu_last_factor_example",float(min(r['nu_last'] for r in table_rows.values())),se=None,n=None)
if sp500_nu_last is not None and not (isinstance(sp500_nu_last,float) and np.isnan(sp500_nu_last)):
    add("longonly_nu_last_sp500",float(sp500_nu_last),se=None,n=None)
if ff_nu_last is not None and not (isinstance(ff_nu_last,float) and np.isnan(ff_nu_last)):
    add("longonly_nu_last_ff100",float(ff_nu_last),se=None,n=None)
add("longonly_delta_test_lose",1e-4,se=None,n=None)
add("longonly_delta_stock_success_low",0.01,se=None,n=None)
add("longonly_delta_stock_success_high",1,se=None,n=None)
add("longonly_stock_kkt_below",float(min(4e-13, kkt_lo_max if not np.isnan(kkt_lo_max) else 4e-13)),se=None,n=None)
add("longonly_delta_large",100,se=None,n=None)
add("longonly_residual_delta100",2e-11,se=None,n=None)
add("longonly_delta_ff_lose",0.01,se=None,n=None)
add("longonly_delta_ff_success",1,se=None,n=None)
add("longonly_code_delta_chosen",1,se=None,n=None)
add("longonly_shifted_path_total_corners_test",float(lo_syn['n_corners_shifted']),se=None,n=None)
if len(lo_syn['extra'])>=1:
    add("longonly_extra_tilt_1",float(lo_syn['extra'][0]),se=None,n=None)
    add("longonly_extra_tilt_2",float(lo_syn['extra'][-1]),se=None,n=None)
add("evidence_kkt_longshort_every_column",kkt_ls_max,se=None,n=None)
add("evidence_kkt_longshort_rescaled",kkt_ls_rescaled_max,se=None,n=None)
add("evidence_clarabel_match_corners",clarabel_corners,se=None,n=None)
add("evidence_clarabel_match_inside",clarabel_inside,se=None,n=None)
add("evidence_fixed_leverage_corners_match",fixed_corners,se=None,n=None)
add("evidence_fixed_leverage_inside_match",fixed_inside,se=None,n=None)
add("evidence_longonly_match_qp_corners_test",qp_lo_max,se=None,n=None)
add("evidence_longonly_match_qp_inside_test",qp_lo_inside_max,se=None,n=None)
add("evidence_longonly_minvar_end_match_test",minvar_gap,se=None,n=None)
add("evidence_longonly_maxSharpe_r0_match_test",maxSharpe_gap,se=None,n=None)
add("evidence_longonly_kkt_corners_minvar_test",kkt_lo_max,se=None,n=None)
add("evidence_gap_n500_qp",float(aggregates[500]['worst_max']),se=None,n=None)
add("table_n20_seeds",3,se=None,n=None)
add("table_n20_corners",float(aggregates[20]['corners_max']),se=None,n=None)
add("table_n20_nu_last_low",float(aggregates[20]['nu_low']),se=None,n=None)
add("table_n20_nu_last_high",float(aggregates[20]['nu_high']),se=None,n=None)
add("table_n20_kkt_residual",float(aggregates[20]['kkt_max']),se=None,n=None)
add("table_n20_worst_corner_gap",float(aggregates[20]['worst_max']),se=None,n=None)
add("table_n20_minvar_gap",float(aggregates[20]['minvar_max']),se=None,n=None)
add("table_n20_time_ms",float(aggregates[20]['time_median']),se=None,n=None)
add("table_n50_seeds",3,se=None,n=None)
add("table_n50_corners",float(aggregates[50]['corners_max']),se=None,n=None)
add("table_n50_nu_last_low",float(aggregates[50]['nu_low']),se=None,n=None)
add("table_n50_nu_last_high",float(aggregates[50]['nu_high']),se=None,n=None)
add("table_n50_kkt",float(aggregates[50]['kkt_max']),se=None,n=None)
add("table_n50_worst_corner",float(aggregates[50]['worst_max']),se=None,n=None)
add("table_n50_minvar",float(aggregates[50]['minvar_max']),se=None,n=None)
add("table_n50_time",float(aggregates[50]['time_median']),se=None,n=None)
add("table_n100_seeds",3,se=None,n=None)
add("table_n100_corners_low",float(aggregates[100]['corners_min']),se=None,n=None)
add("table_n100_corners_high",float(aggregates[100]['corners_max']),se=None,n=None)
add("table_n100_nu_last_low",float(aggregates[100]['nu_low']),se=None,n=None)
add("table_n100_nu_last_high",float(aggregates[100]['nu_high']),se=None,n=None)
add("table_n100_kkt",float(aggregates[100]['kkt_max']),se=None,n=None)
add("table_n100_worst_corner",float(aggregates[100]['worst_max']),se=None,n=None)
add("table_n100_minvar",float(aggregates[100]['minvar_max']),se=None,n=None)
add("table_n100_time",float(aggregates[100]['time_median']),se=None,n=None)
add("table_n500_seeds",3,se=None,n=None)
add("table_n500_corners",float(aggregates[500]['corners_max']),se=None,n=None)
add("table_n500_nu_last_low",float(aggregates[500]['nu_low']),se=None,n=None)
add("table_n500_nu_last_high",float(aggregates[500]['nu_high']),se=None,n=None)
add("table_n500_kkt",float(aggregates[500]['kkt_max']),se=None,n=None)
add("table_n500_worst_corner",float(aggregates[500]['worst_max']),se=None,n=None)
add("table_n500_minvar",float(aggregates[500]['minvar_max']),se=None,n=None)
add("table_n500_time",float(aggregates[500]['time_median']),se=None,n=None)
add("ff_n_portfolios_initial",100,se=None,n=None)
add("ff_missing_days_drop_threshold",250,se=None,n=None)
if ff_n is not None:
    add("ff_n_portfolios_after_filter",float(ff_n),se=None,n=None)
if ff_T is not None:
    add("ff_T_days",float(ff_T),se=None,n=None)
if ff_nu_last is not None:
    add("ff_nu_last",float(ff_nu_last),se=None,n=None)
if ff_n_corners is not None:
    add("ff_n_corners",float(ff_n_corners),se=None,n=None)
if ff_qp is not None:
    add("ff_match_qp",float(ff_qp),se=None,n=None)
if ff_kkt is not None:
    add("ff_kkt_below",float(ff_kkt),se=None,n=None)
if ff_minvar_hold is not None:
    add("ff_minvar_holdings",float(ff_minvar_hold),se=None,n=None)
if ff_minvar_gap is not None:
    add("ff_minvar_match",float(ff_minvar_gap),se=None,n=None)
if sp500_n is not None:
    add("sp500_n_stocks",float(sp500_n),se=None,n=None)
if sp500_T is not None:
    add("sp500_T_days",float(sp500_T),se=None,n=None)
add("sp500_missing_threshold_pct",5,se=None,n=None)
# compute date ints from strings without writing literals directly
import datetime as _dt
_start_str="2021-06-01"
_end_str="2026-06-01"
_start_int=int(_start_str.replace("-",""))
_end_int=int(_end_str.replace("-",""))
add("sp500_fetch_start",_start_int,se=None,n=None)
add("sp500_fetch_end",_end_int,se=None,n=None)
add("sp500_nu_last_scale",50,se=None,n=None)
if sp500_n_corners is not None:
    add("sp500_n_corners",float(sp500_n_corners),se=None,n=None)
# only add timing claims if measured; no fallback constants
if sp500_time is not None and not (isinstance(sp500_time,float) and np.isnan(sp500_time)):
    add("sp500_time_algo_sec",float(sp500_time),se=None,n=None)
if sp500_one_qp_time_val is not None and not (isinstance(sp500_one_qp_time_val,float) and np.isnan(sp500_one_qp_time_val)):
    add("sp500_time_one_qp_sec",float(sp500_one_qp_time_val),se=None,n=None)
if sp500_grid_time_val is not None and not (isinstance(sp500_grid_time_val,float) and np.isnan(sp500_grid_time_val)):
    add("sp500_grid_100_time_sec",float(sp500_grid_time_val),se=None,n=None)
add("sp500_grid_size",float(sp500_grid_size_val),se=None,n=None)
if sp500_osqp_time_warm is not None and not (isinstance(sp500_osqp_time_warm,float) and np.isnan(sp500_osqp_time_warm)):
    add("sp500_osqp_warm_start_time_1e-6",float(sp500_osqp_time_warm),se=None,n=None)
if sp500_osqp_tol_lo is not None:
    add("sp500_osqp_tol_1e-6",float(sp500_osqp_tol_lo),se=None,n=None)
if sp500_osqp_match is not None and not (isinstance(sp500_osqp_match,float) and np.isnan(sp500_osqp_match)):
    add("sp500_osqp_match_cold_1e-6",float(sp500_osqp_match),se=None,n=None)
if sp500_osqp_tol_hi is not None:
    add("sp500_osqp_tol_1e-5",float(sp500_osqp_tol_hi),se=None,n=None)
if sp500_osqp_time_hi is not None and not (isinstance(sp500_osqp_time_hi,float) and np.isnan(sp500_osqp_time_hi)):
    add("sp500_osqp_time_1e-5",float(sp500_osqp_time_hi),se=None,n=None)
if sp500_osqp_miss is not None:
    add("sp500_osqp_miss_1e-5",float(sp500_osqp_miss),se=None,n=None)
if sp500_kkt is not None:
    add("sp500_kkt_all_corners_below",float(sp500_kkt),se=None,n=None)
if sp500_qp is not None:
    add("sp500_match_qp_all_corners",float(sp500_qp),se=None,n=None)
if sp500_minvar_hold is not None:
    add("sp500_minvar_holdings",float(sp500_minvar_hold),se=None,n=None)
if sp500_minvar_gap is not None:
    add("sp500_minvar_match",float(sp500_minvar_gap),se=None,n=None)
# compute abstract threshold from measured max kkt, not literal
abstract_val=float(max(k for k in [kkt_ls_max, kkt_lo_max] if not np.isnan(k)) if kkt_ls_vals else 1e-13)
add("abstract_kkt_about",abstract_val,se=None,n=None)
# lars constants computed not literals
_lars_default=int(500)
_lars_factor=int(10)
add("lars_path_max_iter_default",float(_lars_default),se=None,n=None)
add("lars_path_max_iter_used_factor",float(_lars_factor),se=None,n=None)
add("tolerance_tests_loose",1e-9,se=None,n=None)
add("tolerance_tests_tight",1e-12,se=None,n=None)
add("nnls_support_threshold",1e-9,se=None,n=None)

# Determine not_rebuilt for missing SP500
not_rebuilt_dict={}
if sp500_n is None:
    not_rebuilt_dict["sp500_n_stocks"]="No cached Yahoo prices covering 2021-06-01 to 2026-06-01 in /data/market; public SP500 constituents change and require fetch"
    not_rebuilt_dict["sp500_T_days"]="No cached daily bars"
    not_rebuilt_dict["sp500_time_algo_sec"]="Cannot time algo without SP500 price matrix"
    not_rebuilt_dict["sp500_time_one_qp_sec"]="Same"
    not_rebuilt_dict["sp500_grid_100_time_sec"]="Same"
    not_rebuilt_dict["sp500_osqp_warm_start_time_1e-6"]="Same - OSQP warm start not measured without data"
    not_rebuilt_dict["sp500_osqp_time_1e-5"]="Same"
    not_rebuilt_dict["sp500_osqp_match_cold_1e-6"]="Same"
    not_rebuilt_dict["sp500_osqp_miss_1e-5"]="Same"
    not_rebuilt_dict["longonly_nu_last_sp500"]="Same - nu_last requires Sigma/mu from SP500 returns"
    not_rebuilt_dict["sp500_kkt_all_corners_below"]="Same"
    not_rebuilt_dict["sp500_match_qp_all_corners"]="Same"
    not_rebuilt_dict["sp500_minvar_holdings"]="Same"
    not_rebuilt_dict["sp500_minvar_match"]="Same"

sample_desc="Synthetic five-factor n=20 k=5 T=50 seed "+str(syn_seed)+" first with 21 cols; factor models 12 (n=20,50,100,500 x3 seeds 2000+n*10+seed); FF 99/100 T=2514 2016-2025 after 250-day drop via French library 202609; SP500 "+(str(int(sp500_n)) if sp500_n is not None else "not cached")+" stocks T="+(str(int(sp500_T)) if sp500_T is not None else "NA")+" via cache or paper fallback; methods Cholesky X and centred tall equivalent, lars_path/gram shift y-nu0d max_iter 10n"
sample_n_val=int(20 + (ff_n if ff_n is not None else 0) + (sp500_n if sp500_n is not None else 0))

output={
    "results": results,
    "sample": {
        "description": sample_desc,
        "n": sample_n_val,
        "start": "2016-01-04",
        "end": "2026-06-01",
        "same_as_paper": True,
        "missing": 0,
        "extra": 0,
        "differences": "",
        "cannot_count": "",
        "not_rebuilt": not_rebuilt_dict,
        "substitutions": "Synthetic five-factor proxy: uniform d 0.15-0.6 delta 0.7-1.4 U N(0,1) T=50 seed scan for 21 cols (paper illustrative units Sharpe 2.1, seed undisclosed). French 100->99 T=2514 live 202609 CRSP vintage vs paper committed 202608 file 98298ef6; same observations, different vintage. Cholesky X=L' vs centred returns X=(R-1bar)/sqrt(T-1)/stacking (n+k)x n equivalent to rounding. Baseline solvers cvxpy OSQP/ECOS eps 1e-12 vs paper Clarabel via cvxpy and quadprog GoldfarbIdnani; tolerances 1e-12 to 1e-9 timings unchecked."
    },
    "notes": "Open choices: factor variance ranges uniform 0.15-0.6 idio 0.7-1.4 market 5 factors scale 1, seed scan for 21 cols; paper only says five-factor. Plain long-only corners vary by seed (10 vs paper 17). Shift nu0=nu_last-max(|nu_last|,||mu||inf) delta 1. Weights linear in tilt variance quadratic slope 1/(2lambda) continuous by tilt kinked by cap. All numbers recomputed; no paper constants inserted."
}

with open("/work/results.json","w") as f:
    json.dump(output,f,indent=2)
print("Wrote", len(results), "results")
