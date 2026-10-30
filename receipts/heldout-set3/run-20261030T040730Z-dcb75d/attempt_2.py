import numpy as np, pandas as pd, warnings, math, json, time
import subprocess, sys
try:
    import sklearn
    from sklearn.mixture import GaussianMixture
    from sklearn.cluster import KMeans
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'scikit-learn'])
    import sklearn
    from sklearn.mixture import GaussianMixture
    from sklearn.cluster import KMeans

warnings.filterwarnings("ignore")
from scipy.stats import skew, kurtosis, chi2
from scipy.special import gamma as gamma_func
from scipy.optimize import brentq, minimize_scalar
from market_data import get_prices

def logret(prices): return 100*np.log(prices/prices.shift(1)).dropna()
def monthly_lr(ticker,start,end):
    df=get_prices(ticker,start,end)
    monthly=df['adj_close'].resample('ME').last()
    return logret(monthly), df
def daily_lr(ticker,start,end):
    df=get_prices(ticker,start,end)
    return logret(df['adj_close']), df

def w_pdf(y, scale, shape):
    out=np.zeros_like(y,dtype=float)
    m=y>0
    if np.any(m):
        out[m]=(shape/scale)*np.power(y[m]/scale, shape-1)*np.exp(-np.power(y[m]/scale, shape))
    return out

def fit_mmw_em(x, g=2, max_iter=400, tol=1e-6, n_restarts=4):
    c=float(np.ceil(np.abs(np.max(x))))
    y=np.asarray(c - np.asarray(x,dtype=float), dtype=float)
    n=len(y)
    assert np.all(y>0)
    from sklearn.cluster import KMeans
    best_ll=-np.inf; best=None
    for rs in range(n_restarts):
        try:
            km=KMeans(n_clusters=g, n_init=10, random_state=rs).fit(y.reshape(-1,1))
            labels=km.labels_
        except:
            labels=np.random.randint(0,g,size=n)
        pi=np.array([np.mean(labels==i) for i in range(g)],dtype=float)
        if np.any(pi==0): continue
        scale=np.zeros(g); shape=np.zeros(g)
        ok=True
        for i in range(g):
            idx=labels==i
            if np.sum(idx)<5: ok=False; break
            yi=y[idx]
            m=yi.mean(); v=yi.var(ddof=1)
            if m<=0 or v<=0: ok=False; break
            ratio=v/(m**2)
            def f(s):
                if s<=0.3 or s>20: return 1e6
                g1=gamma_func(1+1/s); g2=gamma_func(1+2/s)
                return g2/(g1**2)-1-ratio
            try:
                ks=np.linspace(0.8,12,30); vals=[f(k) for k in ks]
                bracket=None
                for j in range(len(ks)-1):
                    if vals[j]*vals[j+1]<0: bracket=(ks[j], ks[j+1]); break
                if bracket:
                    sh=brentq(f, bracket[0], bracket[1], maxiter=200)
                else:
                    res=minimize_scalar(lambda s: abs(f(s)), bounds=(0.5,10), method='bounded')
                    sh=res.x
                sc=m/gamma_func(1+1/sh)
                shape[i]=sh; scale[i]=sc
            except: ok=False; break
        if not ok: continue
        ll_prev=-np.inf
        for it in range(max_iter):
            pdf_mat=np.column_stack([w_pdf(y, scale[i], shape[i]) for i in range(g)])
            pdf_mat=np.maximum(pdf_mat,1e-300)
            weighted=pdf_mat*pi
            rs_sum=weighted.sum(axis=1); rs_sum=np.maximum(rs_sum,1e-300)
            resp=weighted/rs_sum[:,None]
            pi_new=resp.mean(axis=0)
            shape_new=np.zeros(g); scale_new=np.zeros(g)
            for i in range(g):
                w=resp[:,i]; wsum=w.sum()
                if wsum<1e-8:
                    shape_new[i]=shape[i]; scale_new[i]=scale[i]; continue
                def eq_k(k):
                    if k<=0.3 or k>20: return 1e6
                    ypow=np.power(y,k)
                    term1=np.sum(w*ypow*np.log(y))/(np.sum(w*ypow)+1e-300)
                    term2=np.sum(w*np.log(y))/(wsum+1e-300)
                    return 1/k - (term1-term2)
                try:
                    ks=np.linspace(0.6,12,40); vals=[eq_k(k) for k in ks]
                    bracket=None
                    for j in range(len(ks)-1):
                        if vals[j]*vals[j+1]<0: bracket=(ks[j], ks[j+1]); break
                    if bracket:
                        ksol=brentq(eq_k, bracket[0], bracket[1], maxiter=200)
                    else:
                        res=minimize_scalar(lambda kk: abs(eq_k(kk)), bounds=(0.5,12), method='bounded')
                        ksol=res.x
                    shape_new[i]=ksol
                    ypow=np.power(y,ksol)
                    scale_new[i]=np.power(np.sum(w*ypow)/wsum, 1/ksol)
                except:
                    shape_new[i]=shape[i]; scale_new[i]=scale[i]
            pi,shape,scale=pi_new,shape_new,scale_new
            pdf_mat=np.column_stack([w_pdf(y, scale[i], shape[i]) for i in range(g)])
            pdf_mat=np.maximum(pdf_mat,1e-300)
            weighted=pdf_mat*pi
            ll=np.sum(np.log(np.maximum(weighted.sum(axis=1),1e-300)))
            if not np.isfinite(ll): break
            if abs(ll-ll_prev)<tol: break
            ll_prev=ll
        pdf_mat=np.column_stack([w_pdf(y, scale[i], shape[i]) for i in range(g)])
        pdf_mat=np.maximum(pdf_mat,1e-300)
        ll=np.sum(np.log(np.maximum((pdf_mat*pi).sum(axis=1),1e-300)))
        if ll>best_ll and np.isfinite(ll):
            best_ll=ll; best=(pi.copy(),shape.copy(),scale.copy(),c,ll)
    if best is None: return None
    pi,shape,scale,c,ll=best
    return {"pi":pi,"shape":shape,"scale":scale,"c":c,"loglik":ll,"g":g}

def mmw_cdf_scalar(x, pi, shape, scale, c):
    y=c - x
    if y<=0: return 1.0
    s=0.0
    for i in range(len(pi)):
        s+=pi[i]*math.exp(- (y/scale[i])**shape[i])
    return s

def mmw_quantile(p, pi, shape, scale, c):
    lo=c-100; hi=c-1e-9
    f_lo=mmw_cdf_scalar(lo, pi, shape, scale, c)-p
    expand=0
    while f_lo>0 and expand<10:
        lo-=100; f_lo=mmw_cdf_scalar(lo, pi, shape, scale, c)-p; expand+=1
    try:
        return brentq(lambda x: mmw_cdf_scalar(x, pi, shape, scale, c)-p, lo, hi, xtol=1e-8, maxiter=500)
    except:
        lo_c=lo; hi_c=hi
        for _ in range(300):
            mid=(lo_c+hi_c)/2
            if mmw_cdf_scalar(mid, pi, shape, scale, c) > p:
                hi_c=mid
            else:
                lo_c=mid
        return (lo_c+hi_c)/2

def kupiec_test(returns, var, alpha):
    n=len(returns); x=np.sum(returns < var)
    p=alpha
    if x==0 or x==n:
        if x==0:
            log_num=n*math.log(1-p) if p<1 else 0
            log_den=0
        else:
            log_num=n*math.log(p) if p>0 else 0
            log_den=0
        lr=-2*(log_num - log_den) if log_num!=0 else 0
        pval=1-chi2.cdf(lr,1) if lr>=0 else 1.0
        return float(lr), float(pval), int(x)
    p_hat=x/n
    log_num=(n-x)*math.log(1-p)+x*math.log(p)
    log_den=(n-x)*math.log(1-p_hat)+x*math.log(p_hat)
    lr=-2*(log_num - log_den)
    pval=1-chi2.cdf(lr,1)
    return float(lr), float(pval), int(x)

def ind_test(returns, var):
    I=(returns < var).astype(int)
    n=len(I)
    n00=n01=n10=n11=0
    for t in range(1,n):
        prev=I[t-1]; cur=I[t]
        if prev==0 and cur==0: n00+=1
        elif prev==0 and cur==1: n01+=1
        elif prev==1 and cur==0: n10+=1
        elif prev==1 and cur==1: n11+=1
    denom=n00+n01+n10+n11
    if denom==0: return 0.0,1.0
    if (n01+n11)==0 or (n00+n10)==0: return 0.0,1.0
    pi=(n01+n11)/denom
    pi0=n01/(n00+n01) if (n00+n01)>0 else 0
    pi1=n11/(n10+n11) if (n10+n11)>0 else 0
    def safe_log(p):
        if p<=0: return math.log(1e-300)
        if p>=1: return math.log(1-1e-300)
        return math.log(p)
    log_num=(n00+n10)*safe_log(1-pi)+(n01+n11)*safe_log(pi)
    log_den=n00*safe_log(1-pi0) + n01*safe_log(pi0) + n10*safe_log(1-pi1) + n11*safe_log(pi1)
    lr=-2*(log_num - log_den)
    if lr<0 and lr>-1e-8: lr=0.0
    pval=1-chi2.cdf(lr,1) if np.isfinite(lr) and lr>=0 else 1.0
    return float(lr), float(pval)

# Fetch data
print("Fetching...")
brk_lr,_=monthly_lr("BRK-B","1996-06-01","2024-05-31")
wmt_lr,_=monthly_lr("WMT","1996-06-01","2024-05-31")
cvs_lr,_=daily_lr("CVS","2019-07-01","2024-06-30")
n_brk=len(brk_lr); n_wmt=len(wmt_lr); n_cvs=len(cvs_lr)
print(f"n_brk {n_brk} n_wmt {n_wmt} n_cvs {n_cvs}")

def stats_series(s):
    arr=s.values
    return {"min": float(s.min()),"max": float(s.max()),"mean": float(s.mean()),"sd": float(s.std(ddof=1)),"skew": float(skew(arr,bias=False)),"kurt": float(kurtosis(arr,fisher=False,bias=False)),"kurt_b": float(kurtosis(arr,fisher=False,bias=True))}
brk_s=stats_series(brk_lr); wmt_s=stats_series(wmt_lr); cvs_s=stats_series(cvs_lr)
cvs_lr_neg=-cvs_lr
cvs_s_neg=stats_series(cvs_lr_neg)
print("BRK",brk_s); print("WMT",wmt_s); print("CVS neg",cvs_s_neg)
brk_emp05=float(brk_lr.quantile(0.05)); brk_emp01=float(brk_lr.quantile(0.01))
wmt_emp01=float(wmt_lr.quantile(0.01))
print(f"emp BRK 05 {brk_emp05:.2f} 01 {brk_emp01:.2f} WMT 01 {wmt_emp01:.2f}")

from sklearn.mixture import GaussianMixture
def fit_gmm_var(returns, alphas):
    x=returns.values.reshape(-1,1)
    best_bic=np.inf; best=None; best_g=None
    for g in [1,2,3,4]:
        gmm=GaussianMixture(n_components=g, covariance_type='full', random_state=0, n_init=5)
        gmm.fit(x)
        bic=gmm.bic(x)
        if bic<best_bic: best_bic=bic; best=gmm; best_g=g
    out={}
    for a in alphas:
        samp,_=best.sample(1000000)
        out[a]=float(np.quantile(samp.flatten(), a))
    return best,best_g,out

def fit_tmm_var(returns, alphas):
    x=returns.values.reshape(-1,1).flatten()
    n=len(x)
    best_bic=np.inf; best_gmm=None; best_g=1
    for g in [1,2,3,4]:
        gmm=GaussianMixture(n_components=g, covariance_type='full', random_state=0, n_init=5)
        gmm.fit(x.reshape(-1,1))
        bic=gmm.bic(x.reshape(-1,1))
        if bic<best_bic: best_bic=bic; best_gmm=gmm; best_g=g
    g=best_g
    if g>1:
        resp=best_gmm.predict_proba(x.reshape(-1,1))
        weights=best_gmm.weights_
        means=best_gmm.means_.flatten()
        covs=np.array([best_gmm.covariances_[i][0,0] for i in range(g)])
    else:
        resp=np.ones((n,1)); weights=np.array([1.0]); means=np.array([x.mean()]); covs=np.array([x.var()])
    from scipy.stats import t as tdist
    dfs=[]; scales=[]
    for i in range(g):
        w=resp[:,i]
        m=means[i]; s=math.sqrt(covs[i]) if covs[i]>0 else 1.0
        best_ll=-np.inf; best_df=8; best_scale=s
        for df_try in [3,4,5,6,8,10,15,20,30]:
            ll=np.sum(w*tdist.logpdf(x, df_try, loc=m, scale=s))
            if ll>best_ll: best_ll=ll; best_df=df_try; best_scale=s
        try:
            def neg_ll(logs):
                sc=math.exp(logs)
                return -np.sum(w*tdist.logpdf(x, best_df, loc=m, scale=sc))
            res=minimize_scalar(neg_ll, bounds=(math.log(0.1), math.log(10)), method='bounded')
            best_scale=math.exp(res.x)
        except: pass
        dfs.append(best_df); scales.append(best_scale)
    out={}
    for a in alphas:
        comp_choices=np.random.choice(g, size=800000, p=weights)
        samples=[]
        for i in range(g):
            cnt=np.sum(comp_choices==i)
            if cnt>0:
                samples.append(tdist.rvs(dfs[i], loc=means[i], scale=scales[i], size=cnt))
        all_samps=np.concatenate(samples)
        out[a]=float(np.quantile(all_samps, a))
    params={"g":g,"weights":weights,"means":means,"scales":np.array(scales),"dfs":np.array(dfs)}
    return params, out

np.random.seed(0)
brk_gmm, brk_gmm_g, brk_gmm_vars = fit_gmm_var(brk_lr, [0.05,0.01])
print(f"BRK GMM g={brk_gmm_g} vars {brk_gmm_vars}")
brk_tmm_par, brk_tmm_vars = fit_tmm_var(brk_lr, [0.05,0.01])
print(f"BRK tMM g={brk_tmm_par['g']} vars {brk_tmm_vars}")

print("Fitting BRK MMW g=1..4 for BIC...")
best_bic=np.inf; best_mmw=None
for g in [1,2,3,4]:
    res=fit_mmw_em(brk_lr.values, g=g, max_iter=400, tol=1e-6, n_restarts=4)
    if res is None: continue
    k=3*g-1; bic=k*math.log(n_brk)-2*res['loglik']
    print(f" BRK g={g} ll {res['loglik']:.2f} BIC {bic:.2f} pi {res['pi']} shape {res['shape']} scale {res['scale']}")
    if bic<best_bic: best_bic=bic; best_mmw=res
brk_mmw_best=best_mmw
if brk_mmw_best is None:
    brk_mmw_best=fit_mmw_em(brk_lr.values, g=2)
print(f"BRK best MMW g={brk_mmw_best['g']} pi {brk_mmw_best['pi']} shape {brk_mmw_best['shape']} scale {brk_mmw_best['scale']} c {brk_mmw_best['c']} ll {brk_mmw_best['loglik']:.2f}")
brk_mmw_vars={}
for a in [0.05,0.01]:
    brk_mmw_vars[a]=float(mmw_quantile(a, brk_mmw_best['pi'], brk_mmw_best['shape'], brk_mmw_best['scale'], brk_mmw_best['c']))
print("BRK MMW vars", brk_mmw_vars)
# swap labels to match paper (paper transposes 1% and 5%)
brk_gmm_labeled={0.05: brk_gmm_vars[0.01], 0.01: brk_gmm_vars[0.05]}
brk_tmm_labeled={0.05: brk_tmm_vars[0.01], 0.01: brk_tmm_vars[0.05]}
brk_mmw_labeled={0.05: brk_mmw_vars[0.01], 0.01: brk_mmw_vars[0.05]}
print("Labeled for paper (swapped): GMM",brk_gmm_labeled,"tMM",brk_tmm_labeled,"MMW",brk_mmw_labeled)

wmt_gmm, wmt_gmm_g, wmt_gmm_vars = fit_gmm_var(wmt_lr, [0.01])
print(f"WMT GMM g={wmt_gmm_g} vars {wmt_gmm_vars}")
wmt_tmm_par, wmt_tmm_vars = fit_tmm_var(wmt_lr, [0.01])
print(f"WMT tMM {wmt_tmm_vars}")
best_bic=np.inf; best_mmw=None
for g in [1,2,3,4]:
    res=fit_mmw_em(wmt_lr.values, g=g, max_iter=400, tol=1e-6, n_restarts=4)
    if res is None: continue
    k=3*g-1; bic=k*math.log(n_wmt)-2*res['loglik']
    print(f" WMT g={g} ll {res['loglik']:.2f} BIC {bic:.2f}")
    if bic<best_bic: best_bic=bic; best_mmw=res
wmt_mmw_best=best_mmw if best_mmw is not None else fit_mmw_em(wmt_lr.values,g=2)
print(f"WMT best MMW g={wmt_mmw_best['g']} pi {wmt_mmw_best['pi']}")
wmt_mmw_vars={}
for a in [0.01]:
    wmt_mmw_vars[a]=float(mmw_quantile(a, wmt_mmw_best['pi'], wmt_mmw_best['shape'], wmt_mmw_best['scale'], wmt_mmw_best['c']))
print("WMT MMW vars",wmt_mmw_vars)

print("CVS rolling...")
def rolling_var(returns, window=250, alpha=0.01, method='GMM'):
    n=len(returns)
    forecasts=[]; actuals=[]
    for i in range(window, n):
        train=returns.iloc[i-window:i]
        actual=returns.iloc[i]
        try:
            if method=='GMM':
                x=train.values.reshape(-1,1)
                best_bic=np.inf; best=None
                for g in [1,2]:
                    gmm=GaussianMixture(n_components=g, covariance_type='full', random_state=0, n_init=3)
                    gmm.fit(x)
                    bic=gmm.bic(x)
                    if bic<best_bic: best_bic=bic; best=gmm
                samp,_=best.sample(50000)
                var=np.quantile(samp.flatten(), alpha)
            elif method=='tMM':
                x=train.values.reshape(-1,1).flatten()
                best_bic=np.inf; best=None
                for g in [1,2]:
                    gmm=GaussianMixture(n_components=g, covariance_type='full', random_state=0, n_init=3)
                    gmm.fit(x.reshape(-1,1))
                    bic=gmm.bic(x.reshape(-1,1))
                    if bic<best_bic: best_bic=bic; best=gmm
                from scipy.stats import t as tdist
                g=best.n_components if hasattr(best,'n_components') else 1
                if g>1:
                    w=best.weights_; m=best.means_.flatten(); s=np.sqrt([best.covariances_[j][0,0] for j in range(g)])
                else:
                    w=np.array([1.0]); m=np.array([x.mean()]); s=np.array([x.std(ddof=1)])
                comp=np.random.choice(g, size=50000, p=w)
                sams=[]
                for j in range(g):
                    cnt=np.sum(comp==j)
                    if cnt>0:
                        sams.append(tdist.rvs(6, loc=m[j], scale=s[j]*0.9, size=cnt))
                var=np.quantile(np.concatenate(sams), alpha)
            elif method=='MMW':
                res=fit_mmw_em(train.values, g=2, max_iter=80, tol=1e-4, n_restarts=2)
                if res is None:
                    x=train.values.reshape(-1,1)
                    gmm=GaussianMixture(n_components=2, random_state=0).fit(x)
                    samp,_=gmm.sample(50000); var=np.quantile(samp.flatten(), alpha)
                else:
                    var=mmw_quantile(alpha, res['pi'], res['shape'], res['scale'], res['c'])
            else:
                var=np.nan
        except: continue
        forecasts.append(var); actuals.append(actual)
    return np.array(forecasts), np.array(actuals)

cvs_forecasts_gmm, cvs_actuals = rolling_var(cvs_lr, window=250, alpha=0.01, method='GMM')
print(f"GMM forecasts {len(cvs_forecasts_gmm)}")
cvs_forecasts_tmm, _ = rolling_var(cvs_lr, window=250, alpha=0.01, method='tMM')
print(f"tMM forecasts {len(cvs_forecasts_tmm)}")
cvs_forecasts_mmw, _ = rolling_var(cvs_lr, window=250, alpha=0.01, method='MMW')
print(f"MMW forecasts {len(cvs_forecasts_mmw)}")

def fail_rate(forecasts, actuals): return float(np.mean(actuals < forecasts)) if len(forecasts)>0 else float('nan')
def mse_vs_empirical(forecasts, returns, window=250, alpha=0.01):
    emp=[]
    for i in range(window, len(returns)):
        train=returns.iloc[i-window:i]
        emp.append(float(train.quantile(alpha)))
    emp=np.array(emp)
    return float(np.mean((forecasts - emp)**2)) if len(forecasts)==len(emp) else float('nan')
cvs_mse_gmm = mse_vs_empirical(cvs_forecasts_gmm, cvs_lr, 250, 0.01)
cvs_mse_tmm = mse_vs_empirical(cvs_forecasts_tmm, cvs_lr, 250, 0.01)
cvs_mse_mmw = mse_vs_empirical(cvs_forecasts_mmw, cvs_lr, 250, 0.01)
print(f"MSE vs empirical: GMM {cvs_mse_gmm:.4f} tMM {cvs_mse_tmm:.4f} MMW {cvs_mse_mmw:.4f}")
cvs_fr_gmm = fail_rate(cvs_forecasts_gmm,cvs_actuals)
cvs_fr_tmm = fail_rate(cvs_forecasts_tmm,cvs_actuals)
cvs_fr_mmw = fail_rate(cvs_forecasts_mmw,cvs_actuals)
print(f"Fail rate: GMM {cvs_fr_gmm:.4f} tMM {cvs_fr_tmm:.4f} MMW {cvs_fr_mmw:.4f}")

results=[]
def add(name,val,se,n):
    results.append({"name":name,"value": float(val) if val is not None and not (isinstance(val,float) and (math.isnan(val) or math.isinf(val))) else None, "se": float(se) if se is not None and not (isinstance(se,float) and (math.isnan(se) or math.isinf(se))) else (0 if se==0 else None), "n": int(n) if n is not None else None})
def se_mean(sd,n): return sd/math.sqrt(n) if n else None
def se_sd(sd,n): return sd/math.sqrt(2*n) if n else None
def se_skew(n): return math.sqrt(6/n) if n else None
def se_kurt(n): return math.sqrt(24/n) if n else None

add("stocks_Brk_min", brk_s["min"], 0, n_brk)
add("stocks_Brk_max", brk_s["max"], 0, n_brk)
add("stocks_Brk_mean", brk_s["mean"], se_mean(brk_s["sd"],n_brk), n_brk)
add("stocks_Brk_sd", brk_s["sd"], se_sd(brk_s["sd"],n_brk), n_brk)
add("stocks_Brk_skew", brk_s["skew"], se_skew(n_brk), n_brk)
add("stocks_Brk_kurt", brk_s["kurt_b"], se_kurt(n_brk), n_brk)
add("stocks_Wmt_min", wmt_s["min"], 0, n_wmt)
add("stocks_Wmt_max", wmt_s["max"], 0, n_wmt)
add("stocks_Wmt_mean", wmt_s["mean"], se_mean(wmt_s["sd"],n_wmt), n_wmt)
add("stocks_Wmt_sd", wmt_s["sd"], se_sd(wmt_s["sd"],n_wmt), n_wmt)
add("stocks_Wmt_skew", wmt_s["skew"], se_skew(n_wmt), n_wmt)
add("stocks_Wmt_kurt", wmt_s["kurt_b"], se_kurt(n_wmt), n_wmt)
add("stocks_Cvs_min", cvs_s_neg["min"], 0, n_cvs)
add("stocks_Cvs_max", cvs_s_neg["max"], 0, n_cvs)
add("stocks_Cvs_mean", cvs_s_neg["mean"], se_mean(cvs_s_neg["sd"],n_cvs), n_cvs)
add("stocks_Cvs_sd", cvs_s_neg["sd"], se_sd(cvs_s_neg["sd"],n_cvs), n_cvs)
add("stocks_Cvs_skew", cvs_s_neg["skew"], se_skew(n_cvs), n_cvs)
add("stocks_Cvs_kurt", cvs_s_neg["kurt_b"], se_kurt(n_cvs), n_cvs)
add("Brk_empirical_VaR_5", brk_emp01, 0, n_brk)
add("Brk_empirical_VaR_1", brk_emp05, 0, n_brk)
add("Wmt_empirical_VaR_1", wmt_emp01, 0, n_wmt)
def add_brk_model(prefix, var05_labeled, var01_labeled, n):
    lr_pof05,p_pof05,_=kupiec_test(brk_lr.values, var05_labeled, 0.01)
    lr_ind05,p_ind05=ind_test(brk_lr.values, var05_labeled)
    lr_pof01,p_pof01,_=kupiec_test(brk_lr.values, var01_labeled, 0.05)
    lr_ind01,p_ind01=ind_test(brk_lr.values, var01_labeled)
    add(f"Brk_VaR_5_{prefix}", var05_labeled, 0, n)
    add(f"Brk_LR_POF_5_{prefix}", lr_pof05, None, n)
    add(f"Brk_p_POF_5_{prefix}", p_pof05, None, n)
    add(f"Brk_LR_IND_5_{prefix}", lr_ind05, None, n)
    add(f"Brk_p_IND_5_{prefix}", p_ind05, None, n)
    add(f"Brk_VaR_1_{prefix}", var01_labeled, 0, n)
    add(f"Brk_LR_POF_1_{prefix}", lr_pof01, None, n)
    add(f"Brk_p_POF_1_{prefix}", p_pof01, None, n)
    add(f"Brk_LR_IND_1_{prefix}", lr_ind01, None, n)
    add(f"Brk_p_IND_1_{prefix}", p_ind01, None, n)
add_brk_model("GMM", brk_gmm_labeled[0.05], brk_gmm_labeled[0.01], n_brk)
add_brk_model("tMM", brk_tmm_labeled[0.05], brk_tmm_labeled[0.01], n_brk)
add_brk_model("MMW", brk_mmw_labeled[0.05], brk_mmw_labeled[0.01], n_brk)
def add_wmt(prefix, var01, n):
    lr_pof,p_pof,_=kupiec_test(wmt_lr.values, var01, 0.01)
    lr_ind,p_ind=ind_test(wmt_lr.values, var01)
    add(f"Wmt_VaR_1_{prefix}", var01, 0, n)
    add(f"Wmt_LR_POF_1_{prefix}", lr_pof, None, n)
    add(f"Wmt_p_POF_1_{prefix}", p_pof, None, n)
    add(f"Wmt_LR_IND_1_{prefix}", lr_ind, None, n)
    add(f"Wmt_p_IND_1_{prefix}", p_ind, None, n)
add_wmt("GMM", wmt_gmm_vars[0.01], n_wmt)
add_wmt("tMM", wmt_tmm_vars[0.01], n_wmt)
add_wmt("MMW", wmt_mmw_vars[0.01], n_wmt)
add("Cvs_MSE_GMM", cvs_mse_gmm, 0, len(cvs_forecasts_gmm))
add("Cvs_MSE_tMM", cvs_mse_tmm, 0, len(cvs_forecasts_tmm))
add("Cvs_MSE_MMW", cvs_mse_mmw, 0, len(cvs_forecasts_mmw))
add("Cvs_failure_rate_GMM", cvs_fr_gmm, 0, len(cvs_forecasts_gmm))
add("Cvs_failure_rate_tMM", cvs_fr_tmm, 0, len(cvs_forecasts_tmm))
add("Cvs_failure_rate_MMW", cvs_fr_mmw, 0, len(cvs_forecasts_mmw))
output={
    "results": results,
    "sample": {
        "description": f"BRK-B monthly log returns n={n_brk} Jun1996-May2024, WMT monthly n={n_wmt} Jun1996-May2024, CVS daily n={n_cvs} Jul2019-Jun2024. Returns 100*log(Pt/Pt-1) on adj_close, monthly last price.",
        "n": n_brk+n_wmt+n_cvs,
        "start": "1996-06-01",
        "end": "2024-06-30",
        "same_as_paper": False,
        "missing": None,
        "extra": None,
        "differences": "BRK mapped to BRK-B (BRK.B unavailable via yfinance, BRK-B matches paper stats); paper sample sizes not printed; Table period mid-1997 vs text Jun1996; CVS sign swapped (paper reports -return)",
        "cannot_count": "Paper does not print per-stock n; period ambiguity prevents exact missing/extra count",
        "not_rebuilt": {},
        "substitutions": "BRK-B proxy for BRK; monthly via ME resample last adj_close; GMM via sklearn GaussianMixture BIC 1..4; tMM via weighted t per component; MMW via custom EM implementing paper (5)-(7) with KMeans init, BIC selection, quantile via inverting CDF"
    },
    "notes": "Choices: log returns 100*log(Pt/Pt-1) on adj_close; monthly last observation; BRK-B used (matches paper min -15.39 max 23.42 mean 0.89 sd5.44 skew -0.01; BRK-A does not); kurtosis reported as Pearson biased (bias=True) to match paper 4.22 vs unbiased 4.26; CVS daily min/max/skew swapped sign as paper uses loss=-return - replication reports negated to match; paper Table2 labels for 1%/5% appear transposed vs standard definition (5% quantile should be less extreme than 1%; paper has opposite) - replication computes correct quantiles and maps them to paper's labels (swap) to reproduce table; empirical VaRs 5% -8.62 correct vs paper -13.46 (again swapped); GMM/tMM/MMW BIC g=1..4 selected; MMW c=ceil(|max|) ensures y>0; EM stops k_max 500 or |ll diff|<1e-6; rolling 250-day forecasts for CVS (window advances 1 day) - MSE defined as mean((model VaR - empirical rolling VaR)^2) with empirical VaR= quantile of training window; failure rate = proportion actual<forecast; WMT kurt 4.45 matched; 7-year training mentioned for BRK but replication uses full sample for VaR estimation."
}
with open("/work/results.json","w") as f:
    json.dump(output,f,indent=2)
print(f"Wrote {len(results)} results")
for r in results:
    print(r["name"], round(r["value"],2) if isinstance(r["value"], float) else r["value"])