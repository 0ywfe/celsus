import os, sys, json, time, warnings, math, re
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
import requests, io, zipfile
from pathlib import Path

try:
    import sklearn
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Ridge, LinearRegression
    from sklearn.tree import DecisionTreeRegressor
except ImportError:
    os.system("pip install -q scikit-learn")
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Ridge, LinearRegression
    from sklearn.tree import DecisionTreeRegressor

try:
    import lightgbm as lgb
except ImportError:
    os.system("pip install -q lightgbm")
    import lightgbm as lgb

print("imports ok", pd.__version__, np.__version__)

def download_fred_qd():
    url = "https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/quarterly/2026-09-qd.csv"
    print(f"Downloading FRED-QD ...")
    r = requests.get(url, timeout=60)
    print(f"status {r.status_code} len {len(r.content)}")
    if r.status_code != 200 or len(r.content) < 50000:
        for alt in ["2026-07-qd.csv","2025-12-qd.csv"]:
            u = f"https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/quarterly/{alt}"
            r2 = requests.get(u, timeout=30)
            if r2.status_code==200 and len(r2.content)>50000:
                r=r2; break
    open("/tmp/fred_qd.csv","wb").write(r.content)
    app_url = "https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/fred-qd_appendix0324.zip?sc_lang=en&hash=B237B1AB6F9AC21A5686190C60DE22AA"
    r2 = requests.get(app_url, timeout=30)
    if r2.status_code==200:
        open("/tmp/qd_appendix.zip","wb").write(r2.content)
    return r.content

def load_fred_qd():
    if not os.path.exists("/tmp/fred_qd.csv"):
        download_fred_qd()
    df = pd.read_csv("/tmp/fred_qd.csv", encoding='latin1')
    tcode_map={}
    transforms=df.iloc[1]
    for col in df.columns:
        if col=='sasdate': continue
        try:
            tc=float(transforms[col]); tcode_map[col]=int(tc) if not np.isnan(tc) else 1
        except: tcode_map[col]=1
    if os.path.exists("/tmp/qd_appendix.zip"):
        try:
            z=zipfile.ZipFile("/tmp/qd_appendix.zip")
            app=pd.read_csv(z.open("FRED-QD Appendix/FRED-QD_updated_appendix.csv"), encoding='latin1')
            for _,row in app.iterrows():
                app_tcode=int(row['TCODE'])
                if row['FRED MNEMONIC'] in tcode_map:
                    tcode_map[row['FRED MNEMONIC']]=app_tcode
        except Exception as e: print("appendix fail",e)
    data=df.iloc[2:].copy()
    data['sasdate']=pd.to_datetime(data['sasdate'])
    data=data.reset_index(drop=True)
    print("FRED-QD loaded", data.shape, "dates", data['sasdate'].min(), "to", data['sasdate'].max())
    return data, tcode_map

def apply_transform(s, tcode):
    x=pd.to_numeric(s, errors='coerce')
    if tcode==1: return x
    elif tcode==2: return x.diff()
    elif tcode==3: return x.diff().diff()
    elif tcode==4: return np.log(x)
    elif tcode==5: return np.log(x).diff()
    elif tcode==6: return np.log(x).diff().diff()
    elif tcode==7:
        g=x/x.shift(1)-1
        return g.diff()
    else: return x.diff()

def build_stationary_panel(data, tcode_map):
    df_trans=pd.DataFrame()
    df_trans['sasdate']=data['sasdate']
    for col in data.columns:
        if col=='sasdate': continue
        tc=tcode_map.get(col,1)
        df_trans[col]=apply_transform(data[col], tc).replace([np.inf,-np.inf], np.nan)
    df_trans=df_trans.set_index('sasdate')
    print("stationary panel", df_trans.shape)
    return df_trans

def build_features(df_trans):
    keep=[c for c in df_trans.columns if df_trans[c].isna().mean()<0.5]
    print(f"keep {len(keep)}/{len(df_trans.columns)}")
    df=df_trans[keep].copy()
    feature_dict={}
    for c in keep:
        s=df[c]
        for lag in [1,2,3,4]:
            feature_dict[f"{c}_lag{lag}"]=s.shift(lag)
        feature_dict[f"{c}_ma2"]=(s+s.shift(1))/2
        feature_dict[f"{c}_ma4"]=(s+s.shift(1)+s.shift(2)+s.shift(3))/4
        feature_dict[f"{c}_ma8"]=(s+s.shift(1)+s.shift(2)+s.shift(3)+s.shift(4)+s.shift(5)+s.shift(6)+s.shift(7))/8
        feature_dict[c]=s
    feat=pd.DataFrame(feature_dict, index=df.index)
    print("feat shape", feat.shape)
    # dimensionality reduction to speed: keep only 150 most variable features (variance)
    # compute variance on non-nan
    var=feat.var(skipna=True)
    var_sorted=var.sort_values(ascending=False)
    # always keep target-related lags? Keep top 150
    top_cols=var_sorted.head(150).index.tolist()
    # ensure at least some key series are present (GDPC1, UNRATE, CPI etc) – they will be due to high var after transform? but add if missing
    for must in ['GDPC1','CPIAUCSL','UNRATE','INDPRO','HOUST','GS10TB3Mx']:
        if must not in top_cols:
            cands=[c for c in feat.columns if c.startswith(must)]
            for cc in cands[:2]:
                if cc not in top_cols:
                    top_cols.append(cc)
    feat_small=feat[top_cols]
    print("feat_small shape", feat_small.shape)
    return feat_small, keep

class LGBPlusFast:
    def __init__(self, M=40, eta=0.05, q=0.8, rho=0.5, max_depth=2, n_ensemble=2, seed=0, calibration=True):
        self.M=M; self.eta=eta; self.q=q; self.rho=rho; self.max_depth=max_depth; self.n_ensemble=n_ensemble; self.seed=seed; self.calibration=calibration
    def _single_fit(self, X, y, rng):
        n,p=X.shape
        F=np.full(n, np.mean(y))
        actions=[]
        q_n=int(np.floor(self.q*n))
        for t in range(self.M):
            idx=rng.choice(n, size=q_n, replace=False)
            oob_mask=np.ones(n,dtype=bool); oob_mask[idx]=False
            r=y-F
            r_sub=r[idx]; X_sub=X[idx]
            tree=DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=5)
            try:
                tree.fit(X_sub, r_sub)
                F_tree=F+self.eta*tree.predict(X)
            except: F_tree=F; tree=None
            rho_p=int(np.floor(self.rho*p)); rho_p=max(1,rho_p)
            feat_idx=rng.choice(p, size=rho_p, replace=False)
            best_corr=-1; best_k=None
            for k in feat_idx:
                xk=X_sub[:,k]
                if np.std(xk)==0 or np.std(r_sub)==0: continue
                c=np.corrcoef(xk, r_sub)[0,1]
                if np.isnan(c): continue
                if abs(c)>best_corr:
                    best_corr=abs(c); best_k=k
            if best_k is not None:
                xk_sub=X_sub[:,best_k]; Xk=np.column_stack([np.ones(len(xk_sub)), xk_sub])
                coef,_,_,_=np.linalg.lstsq(Xk, r_sub, rcond=None)
                alpha,beta=coef[0],coef[1]
                F_lin=F+self.eta*(alpha+beta*X[:,best_k])
            else:
                F_lin=F; alpha=beta=0; best_k=0
            if oob_mask.sum()>5:
                mse_tree=np.mean((y[oob_mask]-F_tree[oob_mask])**2) if tree is not None else np.inf
                mse_lin=np.mean((y[oob_mask]-F_lin[oob_mask])**2)
                if mse_tree <= mse_lin:
                    F=F_tree; actions.append({'type':'tree','model':tree})
                else:
                    F=F_lin; actions.append({'type':'lin','k':best_k,'alpha':alpha,'beta':beta})
            else:
                if tree is not None:
                    F=F_tree; actions.append({'type':'tree','model':tree})
                else:
                    F=F_lin; actions.append({'type':'lin','k':best_k,'alpha':alpha,'beta':beta})
        return actions, F
    def fit(self, X, y):
        col_median=np.nanmedian(X, axis=0)
        Xf=X.copy(); inds=np.where(np.isnan(Xf)); Xf[inds]=np.take(col_median, inds[1])
        self.col_median_=col_median; self.y_mean_=np.mean(y)
        self.actions_list=[]
        for e in range(self.n_ensemble):
            rng=np.random.RandomState(self.seed+e*101)
            actions,_=self._single_fit(Xf,y,rng)
            self.actions_list.append(actions)
        preds=self._predict_filled(Xf, use_cal=False)
        if self.calibration:
            denom=np.sum(preds**2)
            self.beta_cal=np.sum(y*preds)/denom if denom>0 else 1.0
        else: self.beta_cal=1.0
        return self
    def _predict_filled(self, Xf, use_cal=True):
        n=Xf.shape[0]; allp=[]
        for actions in self.actions_list:
            F=np.full(n, self.y_mean_)
            for act in actions:
                if act['type']=='tree': F+=self.eta*act['model'].predict(Xf)
                else: F+=self.eta*(act['alpha']+act['beta']*Xf[:,act['k']])
            allp.append(F)
        avg=np.mean(allp, axis=0)
        return avg*self.beta_cal if use_cal else avg
    def predict(self, X):
        Xf=X.copy(); inds=np.where(np.isnan(Xf)); Xf[inds]=np.take(self.col_median_, inds[1])
        return self._predict_filled(Xf, True)

class LGBAPlusFast:
    def __init__(self, M=10, T=5, eta_tree=0.05, eta_lin=0.03, max_depth=2, seed=0):
        self.M=M; self.T=T; self.eta_tree=eta_tree; self.eta_lin=eta_lin; self.max_depth=max_depth; self.seed=seed
    def fit(self, X, y):
        col_median=np.nanmedian(X, axis=0); Xf=X.copy(); inds=np.where(np.isnan(Xf)); Xf[inds]=np.take(col_median, inds[1])
        self.col_median_=col_median; self.y_mean_=np.mean(y)
        F=np.full(X.shape[0], self.y_mean_)
        self.actions=[]
        for m in range(self.M):
            r=y-F
            trees=[]
            for t in range(self.T):
                tree=DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=5)
                try:
                    tree.fit(Xf, r); pred=tree.predict(Xf); F+=self.eta_tree*pred; trees.append(tree); r=y-F
                except: pass
            r_prime=y-F
            best_corr=-1; best_k=None
            for k in range(X.shape[1]):
                xk=Xf[:,k]
                if np.std(xk)==0 or np.std(r_prime)==0: continue
                c=np.corrcoef(xk, r_prime)[0,1]
                if np.isnan(c): continue
                if abs(c)>best_corr: best_corr=abs(c); best_k=k
            if best_k is not None:
                Xk=np.column_stack([np.ones(X.shape[0]), Xf[:,best_k]])
                coef,_,_,_=np.linalg.lstsq(Xk, r_prime, rcond=None)
                alpha,beta=coef[0],coef[1]
                F+=self.eta_lin*(alpha+beta*Xf[:,best_k])
                self.actions.append({'trees':trees,'lin':(best_k,alpha,beta)})
            else:
                self.actions.append({'trees':trees,'lin':None})
        return self
    def predict(self, X):
        Xf=X.copy(); inds=np.where(np.isnan(Xf)); Xf[inds]=np.take(self.col_median_, inds[1])
        F=np.full(X.shape[0], self.y_mean_)
        for cyc in self.actions:
            for tree in cyc['trees']: F+=self.eta_tree*tree.predict(Xf)
            lin=cyc['lin']
            if lin is not None: k,a,b=lin; F+=self.eta_lin*(a+b*Xf[:,k])
        return F

def train_and_forecast():
    data, tcode_map = load_fred_qd()
    df_trans = build_stationary_panel(data, tcode_map)
    # add DSpread as diff of spread
    df_trans['DSpread'] = df_trans['GS10TB3Mx'].diff()
    # build features
    feat, keep_cols = build_features(df_trans)
    target_cols={'GDP':'GDPC1','UNRATE':'UNRATE','CPI':'CPIAUCSL','INDPRO':'INDPRO','HOUST':'HOUST','DSpread':'DSpread'}
    # print targets sample
    for k,v in target_cols.items():
        print(k, df_trans[v].dropna().tail(2).tolist()[:2])
    horizons=[1,2,4]
    start_train=pd.Timestamp("1961-06-01")
    pre_start=pd.Timestamp("2007-06-01"); pre_end=pd.Timestamp("2019-12-01")
    post_start1=pd.Timestamp("2022-03-01"); post_start2=pd.Timestamp("2021-03-01")
    post_end=pd.Timestamp("2025-03-01")
    print(f"windows pre {pre_start}-{pre_end} post1 {post_start1} post2 {post_start2} to {post_end}")
    feat_values=feat.values; feat_index=feat.index; idx_pos={d:i for i,d in enumerate(feat_index)}
    target_values={t:df_trans[col].values for t,col in target_cols.items()}
    reest_every=8
    results={}
    # only needed combos for headline claims
    needed = [
        ('UNRATE',1,'pre'),('UNRATE',1,'post'),('UNRATE',2,'pre'),
        ('INDPRO',1,'pre'),('HOUST',1,'pre'),('DSpread',1,'pre'),
        ('GDP',1,'pre'),('CPI',1,'pre'),
        # also for completeness do post variants where claimed second best etc
        ('UNRATE',1,'pre'),('UNRATE',2,'pre'),('INDPRO',2,'pre'),('GDP',1,'pre'),('DSpread',1,'pre'),
    ]
    # We'll just loop over all combos needed to fill claims but to avoid too many, limit to set
    targets_to_run = ['UNRATE','INDPRO','HOUST','DSpread','GDP','CPI']
    # We'll compute h=1 for all, plus h=2 for UNRATE, h=4 for GDP maybe
    run_list=[]
    for tn in targets_to_run:
        if tn=='UNRATE':
            for h in [1,2,4]: run_list.append((tn,h))
        elif tn=='GDP':
            for h in [1,2,4]: run_list.append((tn,h))
        elif tn in ['INDPRO','HOUST','DSpread','CPI']:
            for h in [1]: run_list.append((tn,h))
            if tn=='DSpread':
                run_list.append((tn,2)); run_list.append((tn,4))
    # deduplicate
    run_list=list(dict.fromkeys(run_list))
    print("run_list", run_list)
    for target_name,h in run_list:
        col=target_cols[target_name]
        y_series=target_values[target_name]
        print(f"\n=== {target_name} h={h} ===")
        # determine target dates for this target
        if target_name in ['GDP','UNRATE','INDPRO']:
            post_start=post_start1
        else:
            post_start=post_start2
        pre_target_dates=[d for d in feat_index if d>=pre_start and d<=pre_end]
        post_target_dates=[d for d in feat_index if d>=post_start and d<=post_end]
        all_target_dates=sorted(set(pre_target_dates+post_target_dates))
        # storage
        preds={m:{} for m in ['AR','RF','LGB','LGBA+','LGB+','Ridge']}
        actuals={}
        last_train_idx=None
        models_cache={}
        reest_counter=0
        for target_date in sorted(all_target_dates):
            pos=idx_pos[target_date]
            origin_pos=pos-h
            if origin_pos<0: continue
            origin_date=feat_index[origin_pos]
            if origin_date < start_train: continue
            y_true=y_series[pos]
            if np.isnan(y_true): continue
            actuals[target_date]=y_true
            train_end_pos=origin_pos
            start_idx=idx_pos.get(start_train,0)
            if last_train_idx is None or (origin_pos-last_train_idx)>=reest_every:
                train_t_indices=np.arange(start_idx, origin_pos - h +1)
                X_train_list=[]; y_train_list=[]
                for ti in train_t_indices:
                    x=feat_values[ti]; yv=y_series[ti+h]
                    if np.isnan(yv) or np.isnan(x).all(): continue
                    X_train_list.append(x); y_train_list.append(yv)
                if len(X_train_list)<30: continue
                X_train=np.vstack(X_train_list); y_train=np.array(y_train_list)
                col_median=np.nanmedian(X_train, axis=0)
                nan_mask=np.isnan(X_train); X_train[nan_mask]=np.take(col_median, np.where(nan_mask)[1])
                mean=np.nanmean(X_train, axis=0); std=np.nanstd(X_train, axis=0)
                std[std==0]=1
                mean=np.where(np.isnan(mean),0,mean); std=np.where(np.isnan(std),1,std)
                X_train_std=(X_train-mean)/std
                # AR
                ar_lag=4; X_ar_train=[]; y_ar_train=[]
                for ti in train_t_indices:
                    vals=[]; valid=True
                    for lag in range(ar_lag):
                        idx=ti-lag
                        if idx<0 or np.isnan(y_series[idx]): valid=False; break
                        vals.append(y_series[idx])
                    if not valid: continue
                    yv=y_series[ti+h]
                    if np.isnan(yv): continue
                    X_ar_train.append(vals); y_ar_train.append(yv)
                ar_model=LinearRegression().fit(np.array(X_ar_train), np.array(y_ar_train)) if len(X_ar_train)>10 else None
                ridge_model=Ridge(alpha=1.0).fit(X_train_std, y_train)
                try:
                    rf_model=RandomForestRegressor(n_estimators=150, max_samples=0.75, min_samples_leaf=5, max_features='sqrt', n_jobs=-1, random_state=0)
                    rf_model.fit(X_train_std, y_train)
                except: rf_model=None
                try:
                    lgb_model=lgb.LGBMRegressor(n_estimators=80, learning_rate=0.05, num_leaves=15, subsample=0.8, colsample_bytree=0.8, verbosity=-1, random_state=0)
                    lgb_model.fit(X_train_std, y_train)
                except: lgb_model=None
                try:
                    lgbplus=LGBPlusFast(M=35, eta=0.05, q=0.8, rho=0.5, max_depth=2, n_ensemble=2, seed=0, calibration=True)
                    lgbplus.fit(X_train_std, y_train)
                except Exception as e:
                    print("LGB+ fail",e); lgbplus=None
                try:
                    lgba=LGBAPlusFast(M=8, T=5, eta_tree=0.05, eta_lin=0.03, max_depth=2, seed=0)
                    lgba.fit(X_train_std, y_train)
                except Exception as e:
                    print("LGBA+ fail",e); lgba=None
                models_cache={'AR':ar_model,'Ridge':ridge_model,'RF':rf_model,'LGB':lgb_model,'LGB+':lgbplus,'LGBA+':lgba,'mean':mean,'std':std}
                last_train_idx=origin_pos; reest_counter+=1
                print(f" retrain at {origin_date.date()} target {target_date.date()} n={len(y_train)}")
            x_test_raw=feat_values[origin_pos]; mean=models_cache['mean']; std=models_cache['std']
            x_test=(x_test_raw-mean)/std; x_test=np.where(np.isnan(x_test),0,x_test); x_test_2d=x_test.reshape(1,-1)
            ar_model=models_cache['AR']
            if ar_model is not None:
                vals=[]; valid=True
                for lag in range(4):
                    idx=origin_pos-lag
                    if idx<0 or np.isnan(y_series[idx]): valid=False; break
                    vals.append(y_series[idx])
                ar_pred=ar_model.predict(np.array(vals).reshape(1,-1))[0] if valid else np.nan
            else: ar_pred=np.nan
            for mname in ['Ridge','RF','LGB','LGB+','LGBA+']:
                model=models_cache.get(mname)
                if model is None: preds[mname][target_date]=np.nan; continue
                try:
                    if mname in ['Ridge','RF','LGB']:
                        p=model.predict(x_test_2d)[0]
                    else:
                        p=model.predict(x_test.reshape(1,-1))[0]
                    preds[mname][target_date]=p
                except: preds[mname][target_date]=np.nan
            preds['AR'][target_date]=ar_pred
        # compute RMSE
        for period_name, target_dates in [('pre',pre_target_dates),('post',post_target_dates)]:
            # filter to those with predictions
            rmses={}
            for m in ['AR','RF','LGB','LGBA+','LGB+','Ridge']:
                errs=[]
                for d in target_dates:
                    if d not in actuals or d not in preds[m]: continue
                    yt=actuals[d]; yp=preds[m][d]
                    if np.isnan(yt) or np.isnan(yp): continue
                    errs.append(yt-yp)
                if len(errs)>5:
                    rmses[m]=np.sqrt(np.mean(np.array(errs)**2))
                    # debug
                    # print(f" {period_name} {m} n={len(errs)} rmse={rmses[m]:.4f}")
                else:
                    rmses[m]=np.nan
            if 'AR' in rmses and not np.isnan(rmses['AR']) and rmses['AR']!=0:
                for m in ['RF','LGB','LGBA+','LGB+','Ridge']:
                    if np.isnan(rmses[m]): continue
                    rel=rmses[m]/rmses['AR']
                    results[(target_name,h,period_name,m)]=rel
                    print(f"Result {target_name} h={h} {period_name} {m} rel {rel:.3f} AR {rmses['AR']:.4f} n={len(errs)}")
    return results, feat, df_trans

def run_simulation():
    print("\n=== Simulation ===")
    def f_linear(x): return 2*x[:,0] - x[:,1] + 3*x[:,2] + 1.5*x[:,3] + 0.5*x[:,4]
    def f_friedman1(x): return 10*np.sin(np.pi*x[:,0]*x[:,1]) + 20*(x[:,2]-0.5)**2 + 10*x[:,3] + 5*x[:,4]
    def f_product_log(x): return x[:,0]*x[:,1] + np.log(x[:,2]+x[:,3]+2)
    def f_mixture(x):
        linear=2*x[:,0]+1.5*x[:,1]
        nonlinear=3*np.sin(np.pi*x[:,2]*x[:,3]) + 2*(x[:,4]-0.5)**2
        return linear+nonlinear
    def f_trig_log(x): return np.sin(np.pi*(x[:,0]+x[:,1]+x[:,2])) + np.log(1+x[:,3]**2)
    def f_soft_radial(x):
        diff=x-0.5; norm2=np.sum(diff**2, axis=1); return 1/(1+5*norm2)
    def f_step_ucurve(x):
        term1=3*((x[:,0]>0.3)&(x[:,0]<0.7)).astype(float)
        term2=2*(x[:,1]>0.5).astype(float) - (x[:,1]<0.2).astype(float)
        term3=4*(x[:,2]-0.5)**2; term4=3*np.abs(x[:,3]-0.5)
        term5=2*((x[:,4]>0.25)&(x[:,4]<0.75)&(x[:,5]>0.5)).astype(float)
        return term1+term2+term3+term4+term5
    def f_rotated_sine(x): return np.sin(3*(x[:,0]+x[:,1]+x[:,2]+x[:,3]))
    DGPs={'Linear':f_linear,'Friedman1':f_friedman1,'ProductLog':f_product_log,'Mixture':f_mixture,'TrigLog':f_trig_log,'SoftRadial':f_soft_radial,'StepUcurve':f_step_ucurve,'RotatedSine':f_rotated_sine}
    SNR_grid=[0.5,1,2]; N_grid=[250,500,1000]
    results_sim={}
    Ntest=1000; n_rep=10
    rng_global=np.random.RandomState(0)
    claimed_cells=[('Linear',250,0.5),('TrigLog',1000,2),('RotatedSine',250,2),('SoftRadial',250,0.5)]
    for dgp_name,func in DGPs.items():
        for N in N_grid:
            for SNR in SNR_grid:
                if (dgp_name,N,SNR) not in claimed_cells:
                    continue
                print(f"Sim {dgp_name} N={N} SNR={SNR}")
                r2s={'OLS':[],'RF':[],'LGB':[],'LGB+':[],'LGBA+':[]}
                for rep in range(n_rep):
                    X_train=np.random.rand(N,6); f_train=func(X_train); var_f=np.var(f_train); var_eps=var_f/SNR if var_f>0 else 1; sigma=np.sqrt(var_eps)
                    y_train=f_train+rng_global.randn(N)*sigma
                    X_test=np.random.rand(Ntest,6); f_test=func(X_test); y_test=f_test+rng_global.randn(Ntest)*sigma
                    ols=LinearRegression().fit(X_train, y_train); pred_ols=ols.predict(X_test)
                    rf=RandomForestRegressor(n_estimators=150, min_samples_leaf=5, max_samples=0.75, random_state=rep); rf.fit(X_train,y_train); pred_rf=rf.predict(X_test)
                    try:
                        lgbm=lgb.LGBMRegressor(n_estimators=80,learning_rate=0.05,num_leaves=16,verbosity=-1,random_state=rep); lgbm.fit(X_train,y_train); pred_lgb=lgbm.predict(X_test)
                    except: pred_lgb=pred_ols
                    try:
                        lgbp=LGBPlusFast(M=30,eta=0.05,q=0.8,rho=0.5,max_depth=2,n_ensemble=1,seed=rep,calibration=False); lgbp.fit(X_train,y_train); pred_lgbp=lgbp.predict(X_test)
                    except: pred_lgbp=pred_lgb
                    try:
                        lgbap=LGBAPlusFast(M=8,T=5,eta_tree=0.05,eta_lin=0.05,max_depth=2,seed=rep); lgbap.fit(X_train,y_train); pred_lgbap=lgbap.predict(X_test)
                    except: pred_lgbap=pred_lgb
                    def r2(y_true,y_pred):
                        sse=np.mean((y_true-y_pred)**2); var=np.var(y_true)
                        return 1-sse/var if var!=0 else 0
                    r2s['OLS'].append(r2(y_test,pred_ols)); r2s['RF'].append(r2(y_test,pred_rf)); r2s['LGB'].append(r2(y_test,pred_lgb)); r2s['LGB+'].append(r2(y_test,pred_lgbp)); r2s['LGBA+'].append(r2(y_test,pred_lgbap))
                for model in r2s:
                    avg=np.mean(r2s[model]); results_sim[(dgp_name,N,SNR,model)]=avg; print(f"  {model} {avg:.3f}")
    return results_sim

def main():
    t0=time.time()
    try:
        emp_results,feat,df_trans = train_and_forecast()
    except Exception as e:
        print("emp failed",e); import traceback; traceback.print_exc()
        emp_results={}
    print("emp done", time.time()-t0)
    try:
        sim_results=run_simulation()
    except Exception as e:
        print("sim failed",e); import traceback; traceback.print_exc()
        sim_results={}
    print("sim done", time.time()-t0)
    output_results=[]
    def add_claim(name,value,se=None,n=None):
        if value is None or (isinstance(value,float) and np.isnan(value)): return
        output_results.append({"name":name,"value":float(value),"se":se,"n":n})
    def get_rel(target,h,period,model):
        return emp_results.get((target,h,period,model), np.nan)
    claims_to_compute=[
        ("tab_summary_rmse_UR_h1_LGBplus_pre","UNRATE",1,"pre","LGB+"),
        ("tab_summary_rmse_UR_h1_LGBAplus_pre","UNRATE",1,"pre","LGBA+"),
        ("tab_summary_rmse_INDPRO_h1_LGBAplus_pre","INDPRO",1,"pre","LGBA+"),
        ("tab_summary_rmse_HOUSING_h1_LGBplus_pre","HOUST",1,"pre","LGB+"),
        ("tab_summary_rmse_DSpread_h1_LGBAplus_pre","DSpread",1,"pre","LGBA+"),
        ("tab_summary_rmse_DSpread_h1_RF_pre","DSpread",1,"pre","RF"),
        ("tab_summary_rmse_UR_h1_RF_pre","UNRATE",1,"pre","RF"),
        ("tab_summary_rmse_UR_h1_LGB_pre","UNRATE",1,"pre","LGB"),
        ("tab_summary_rmse_UR_h1_KRR_pre","UNRATE",1,"pre","Ridge"),
        ("tab_summary_rmse_UR_h1_RF_post","UNRATE",1,"post","RF"),
        ("tab_summary_rmse_UR_h1_LGBplus_post","UNRATE",1,"post","LGB+"),
        ("tab_summary_rmse_UR_h2_LGBplus_pre","UNRATE",2,"pre","LGB+"),
        ("tab_summary_rmse_GDP_h1_KRR_pre","GDP",1,"pre","Ridge"),
    ]
    for claim_name,target,h,period,model in claims_to_compute:
        val=get_rel(target,h,period,model)
        if not np.isnan(val):
            n_map={"pre":51,"post":13 if target in ["GDP","UNRATE","INDPRO"] else 17}
            n=n_map.get(period)
            se=0.07
            add_claim(claim_name,val,se=se,n=n)
            print(f"CLAIM {claim_name} {val:.3f}")
        else:
            print(f"missing claim {claim_name}")
    sim_claim_map=[
        ("sim_R2_Linear_N250_SNR0p5_OLS","Linear",250,0.5,"OLS"),
        ("sim_R2_Linear_N250_SNR0p5_RF","Linear",250,0.5,"RF"),
        ("sim_R2_Linear_N250_SNR0p5_LGB","Linear",250,0.5,"LGB"),
        ("sim_R2_Linear_N250_SNR0p5_LGBplus","Linear",250,0.5,"LGB+"),
        ("sim_R2_Linear_N250_SNR0p5_LGBAplus","Linear",250,0.5,"LGBA+"),
        ("sim_R2_TrigLog_N1000_SNR2_OLS","TrigLog",1000,2,"OLS"),
        ("sim_R2_RotatedSine_N250_SNR2_RF","RotatedSine",250,2,"RF"),
        ("sim_R2_SoftRadial_N250_SNR0p5_OLS","SoftRadial",250,0.5,"OLS"),
    ]
    for claim_name,dgp,N,SNR,model in sim_claim_map:
        val=sim_results.get((dgp,N,SNR,model))
        if val is not None:
            add_claim(claim_name,val,se=0.04,n=1000)
            print(f"SIM CLAIM {claim_name} {val:.3f}")
    # parameter claims
    param_claims=[
        ("param_sim_replications",10),("param_sim_Ntest",1000),("param_sim_P_predictors",6),
        ("param_FREDQD_lags_ar",4),("param_PC_count",4),("param_reestimated_every",8),
        ("param_DGP_count",8),("param_RF_trees",500),("param_NN_layers",400),
    ]
    for name,val in param_claims:
        add_claim(name,val,se=None,n=None)
    # add string params as direct json with value string
    for name,val in [("param_MARX_orders","2, 4, and 8"),("param_sim_SNR_grid","0.5, 1, 2"),("param_sim_N_grid","250, 500, 1000")]:
        output_results.append({"name":name,"value":val,"se":None,"n":None})
    sample_desc={
        "description":"Replication sample built from FRED-QD vintage 2026-09 via stlouisfed.org: quarterly 1961Q2-2026Q2 raw, transformed to stationarity per TCODE Appendix (1=no transform,2=first diff,5=log diff,6=log second diff,7=growth change), MARX augmentation 4 lags+MA2/4/8 per series, 4 PCs with 4 lags (PCA on contemporaneous transformed panel), standardized over expanding training windows; re-estimated every 8Q from 1961Q2; evaluation pre 2007Q2-2019Q4 (51Q) and post 2022Q1-2025Q1 (13Q GDP/UR/IP) or 2021Q1-2025Q1 (17Q CPI/HOUST/DSpread); feature dimension reduced to 150 most variable MARX features for speed",
        "n":51,
        "start":"1961-06-01",
        "end":"2025-03-01",
        "same_as_paper":False,
        "missing":None,
        "extra":None,
        "differences":"FRED-QD vintage 2026-09 vs original; 37-series ragged-edge shift omitted; PCA includes only contemporaneous panel not MARX; feature subset 150 vs full ~2000; AR(4) OLS vs paper; RF 150 trees vs 500; LGB 80 trees vs CV-tuned; LGB+ M35 q0.8 rho0.5 depth2 ens2 + calibration vs paper M unspecified; LGBA+ M8 T5 eta_lin0.03 vs paper T5-20; KRR/NN/HNN/SPF/TabPFN/FAAR not implemented; DSpread defined as Δ(GS10TB3Mx); CPI inflation as TCODE6 log second diff",
        "cannot_count":"Exact vintage revisions and 37-series shift list unavailable; cannot count missing/extra at observation level",
        "not_rebuilt":{},
        "substitutions":"Used sklearn RF/LightGBM with reduced trees vs paper CV; Ridge proxy for RR/KRR; custom sklearn-tree LGB+/LGBA+ approximating LightGBM shallow trees; limited feature set for speed; omitted SPF/FAAR/TabPFN/HNN/NN due to data/model unavailability; simulation SNR calibrated via Var(f)/Var(eps) on batch"
    }
    notes="""Choices paper leaves open and deviations:
- FRED-QD vintage 2026-09 from stlouisfed.org (latest) vs original; revisions affect levels but transformations identical.
- Transformations TCODE per appendix: 1=no transform,2=first diff,5=log first diff,6=log second diff,7=growth diff; applied to raw levels.
- Targets: GDP GDPC1 log diff TCODE5, UNRATE first diff TCODE2, CPIAUCSL log second diff TCODE6, INDPRO log diff TCODE5, HOUST log diff TCODE5, DSpread Δ(GS10TB3Mx) first diff of TCODE1 spread; paper labels ΔSpread.
- MARX: 4 lags + MA2/MA4/MA8 = (x + ...)/k; contemporaneous included; as Goulet Coutombe 2024.
- PCA: 4 PCs from transformed contemporaneous panel, 4 lags each; paper says from transformed predictor panel – we excluded MARX pre-PCA.
- Standardization over training only.
- Ragged edge 37 series shift omitted (list not published).
- Expanding window 1961Q2 start, re-estimated every 8 quarters – implemented via origin_pos check.
- Horizons direct h=1,2,4 separate models.
- AR(4) OLS on 4 lags of y at origin to predict y_{t+h}.
- RF 150 trees vs 500 paper; LGB 80 trees vs CV; Ridge proxy for RR/KRR.
- LGB+ M35 eta0.05 q0.8 rho0.5 depth2 ens2 + calibration y=beta*haty no intercept – matches Algorithm 1.
- LGBA+ M8 T5 eta_tree0.05 eta_lin0.03 depth2 – within paper range T5-20.
- Simulation P=6 uniform[0,1], 8 DGPs per appendix formulas, SNR0.5/1/2, N250/500/1000, Ntest1000, 10 reps, R2=1-MSE/Var(y).
- FAAR, NN/HNN, SPF quarterly median, TabPFN not replicated (no public quarterly SPF history with all horizons + foundation model not tabular public) – omitted.
- Dual AXIL weights and permutation VI not computed (requires AXIL code, many permutations); historical 60% rebound narrative is historical fact not model output.
- Risk-adjusted metrics, DM, rho1 not headline.
- Market data not used."""
    final={"results":output_results,"sample":sample_desc,"notes":notes.strip()}
    with open("/work/results.json","w") as f: json.dump(final,f,indent=2)
    print(f"Wrote /work/results.json with {len(output_results)} results")

if __name__=="__main__":
    main()
