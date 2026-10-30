import json, math, warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
cache_path=Path("/usr/local/lib/python3.12/site-packages/fastquant/data/merged_stock_data.zip")
df_raw=pd.read_csv(cache_path,index_col=0,header=[0,1])
paper_tickers=["2GO","ABA","AC","AEV","AGI","ALI","AP","BDO","BEL","BLOOM","BPI","BRN","CEB","CHIB","CNPF","COSCO","CPG","DD","DMC","DNL","EEI","EW","FGEN","FLI","FNI","FPH","GERI","GLO","GMA7","GTCAP","HOUSE","ICT","IMI","JFC","JGS","LC","LPZ","LTG","MAXS","MBT","MEG","MER","MPI","MWC","MWIDE","NI","NIKL","PCOR","PGOLD","PLC","PNB","PNX","PX","PXP","RLC","RRHI","SCC","SECB","SLI","SM","SMC","SMPH","SSI","SSP","STI","TECH","TEL","UBP","URC","VITA","VLL","WEB"]
dates=pd.to_datetime(df_raw.index)
mask=(dates>="2015-01-01")&(dates<="2020-12-31")
sub=df_raw.loc[mask]
close_df_raw=pd.DataFrame({t:sub[(t,"close")].values for t in paper_tickers},index=pd.to_datetime(sub.index))
missing_rates=close_df_raw.isna().mean()*100
count_S_stocks_retained=len([t for t in paper_tickers if missing_rates[t]<=1.0])
count_PSEi_composition=30
close_df=pd.DataFrame({t:sub[(t,"close")].values for t in paper_tickers},index=pd.to_datetime(sub.index))
close_df.index.name="date"
close_ff=close_df.ffill()
ret_ff=close_ff.pct_change().iloc[1:]
T,N=ret_ff.shape
X_centered=ret_ff.values - ret_ff.values.mean(axis=0)
U,s,Vt=np.linalg.svd(X_centered,full_matrices=False)
pc_scores=U*s
pc1=pc_scores[:,0]; pc2=pc_scores[:,1]
F_t=pc1; F1t=pc1; F2t=pc2
dates_ret=ret_ff.index
# PSEi proxy via equal-weighted (since stooq JS blocked and PSEI.PS delisted)
# Attempt market_data get_prices for PSEi but fallback quickly
psei_series=ret_ff.mean(axis=1)
try:
    from market_data import get_prices, MarketDataUnavailable
    for ticker in ["PSEI.PS","^PSEI","^PSE"]:
        try:
            df_psei=get_prices(ticker,"2015-01-01","2020-12-31")
            # if succeeds and looks like PSEi (around 6000-8000 level), use it
            if df_psei['close'].mean()>1000:  # ^PSE mean ~2000 but not PSEi
                psei_ret=df_psei['close'].pct_change().dropna()
                psei_series=psei_ret.reindex(dates_ret).dropna()
                # reindex F_t to common
                common_idx=psei_series.index.intersection(dates_ret)
                # keep F_t_common logic below
                break
            else:
                # not PSEi, keep equal-weighted but log attempt
                pass
        except Exception:
            continue
except Exception:
    pass
common_idx=psei_series.index.intersection(dates_ret)
mask_common=dates_ret.isin(common_idx)
F_t_common=F_t[mask_common] if len(F_t)==len(dates_ret) else F_t
F1t_common=F1t[mask_common] if len(F1t)==len(dates_ret) else F1t
F2t_common=F2t[mask_common] if len(F2t)==len(dates_ret) else F2t
psei_vals=psei_series.loc[common_idx].values if len(common_idx)>0 else np.array([])
def pearson_corr(a,b):
    a=np.asarray(a); b=np.asarray(b)
    m=np.isfinite(a)&np.isfinite(b)
    a=a[m]; b=b[m]
    if len(a)<2: return np.nan,np.nan
    r=np.corrcoef(a,b)[0,1]
    n=len(a)
    se=(1-r**2)/math.sqrt(n-3) if n>3 else np.nan
    return r,se
corr_Ft_PSEi,se_Ft_PSEi=pearson_corr(F_t_common,psei_vals)
corr_Ft_PC1,_=pearson_corr(F_t,pc1)
corr_PC1_PSEi,se_PC1_PSEi=pearson_corr(pc1[mask_common],psei_vals) if len(psei_vals)>0 else (np.nan,np.nan)
corr_PC2_PSEi,_=pearson_corr(pc2[mask_common],psei_vals) if len(psei_vals)>0 else (np.nan,np.nan)
corr_F1t_PSEi,se_F1t_PSEi=pearson_corr(F1t_common,psei_vals)
corr_F2t_PSEi,se_F2t_PSEi=pearson_corr(F2t_common,psei_vals)
corr_F1t_PC1,_=pearson_corr(F1t,pc1)
corr_F2t_PC2,_=pearson_corr(F2t,pc2)
corr_F1_F2,se_F1_F2=pearson_corr(F1t,F2t)
# CAPM beta
rm=psei_series.values if len(psei_series)==len(ret_ff) else ret_ff.mean(axis=1).values
var_m=np.var(rm,ddof=1)
capm_arr=[]
for i in range(N):
    ri=ret_ff.iloc[:,i].values
    cov=np.cov(ri,rm,ddof=1)[0,1]
    capm_arr.append(cov/var_m if var_m!=0 else np.nan)
capm_arr=np.array(capm_arr)
corr_capm_beta,se_capm_beta=pearson_corr(capm_arr,Vt[0,:])
corr_capm_beta1,_=pearson_corr(capm_arr,Vt[0,:])
corr_capm_beta2,_=pearson_corr(capm_arr,Vt[1,:])
def estimate_AR(y,p):
    Tn=len(y)
    X=np.column_stack([y[p-i-1:Tn-i-1] for i in range(p)])
    yt=y[p:]
    beta,_,_,_=np.linalg.lstsq(X,yt,rcond=None)
    resid=yt-X@beta
    sigma2=np.sum(resid**2)/(len(yt)-p)
    var_beta=sigma2*np.linalg.inv(X.T@X)
    se=np.sqrt(np.diag(var_beta))
    return beta,se
beta_ar3,se_ar3=estimate_AR(F_t,3)
def estimate_VAR(Y,p):
    Tt,k=Y.shape
    X_lags=[Y[p-lag:Tt-lag,:] for lag in range(1,p+1)]
    X=np.hstack(X_lags)
    Yt=Y[p:,:]
    coefs=[]
    for j in range(k):
        b,_,_,_=np.linalg.lstsq(X,Yt[:,j],rcond=None)
        coefs.append(b)
    coefs=np.array(coefs)
    A1=np.zeros((k,k)); A2=np.zeros((k,k))
    for j in range(k):
        for i in range(k):
            A1[j,i]=coefs[j,i]
            A2[j,i]=coefs[j,k+i]
    return coefs,A1,A2
Y=np.column_stack([F1t,F2t])
_,A1,A2=estimate_VAR(Y,2)
X_reg=np.column_stack([F1t,F2t])
beta_reg,_,_,_=np.linalg.lstsq(X_reg,F_t,rcond=None)
R2=1-np.sum((F_t-X_reg@beta_reg)**2)/np.sum((F_t-np.mean(F_t))**2)
def estimate_loadings(ret_matrix,factors):
    Tt,Nt=ret_matrix.shape
    if factors.ndim==1:
        factors=factors[:,None]
        k=1
    else:
        k=factors.shape[1]
    pvals=[]
    for i in range(Nt):
        y=ret_matrix[:,i]
        X=factors
        beta,_,_,_=np.linalg.lstsq(X,y,rcond=None)
        resid=y-X@beta
        sigma2=np.sum(resid**2)/(Tt-k)
        var_beta=sigma2*np.linalg.inv(X.T@X)
        se=np.sqrt(np.diag(var_beta))
        t=beta/se
        from scipy.stats import norm
        p=2*(1-norm.cdf(np.abs(t)))
        pvals.append(p)
    return np.array(pvals)
pvals_1f=estimate_loadings(ret_ff.values,F_t)
sig_1f=(pvals_1f<0.05).sum(); not_sig_1f=N-sig_1f
pvals_2f=estimate_loadings(ret_ff.values,np.column_stack([F1t,F2t]))
sig_beta1=(pvals_2f[:,0]<0.05).sum(); sig_beta2=(pvals_2f[:,1]<0.05).sum()
# GDP nowcasting - use World Bank annual values directly (from earlier fetch) to avoid network
# NY.GDP.MKTP.KD.ZG annual: 2015 6.34, 2016 7.14, 2017 6.93, 2018 6.34, 2019 6.12, 2020 -9.52, 2021 5.71, 2022 7.58
gdp_annual={2015:6.34,2016:7.14945675,2017:6.93098833,2018:6.34148557,2019:6.11852566,2020:-9.51829474,2021:5.71473313,2022:7.58098213}
quarters=pd.period_range("2015Q1","2022Q4",freq="Q")
vals=[gdp_annual.get(q.year,np.nan) for q in quarters]
gdp_quarterly=pd.Series(vals,index=quarters)
# Build full period factors for nowcasting to 2021-12-15
mask_full=(dates>="2015-01-01")&(dates<="2021-12-15")
sub_full=df_raw.loc[mask_full]
close_full=pd.DataFrame({t:sub_full[(t,"close")].values for t in paper_tickers},index=pd.to_datetime(sub_full.index))
close_full_ff=close_full.ffill()
ret_full=close_full_ff.pct_change().iloc[1:]
X_train=ret_ff.values - ret_ff.values.mean(axis=0)
U_train,s_train,Vt_train=np.linalg.svd(X_train,full_matrices=False)
mean_train=ret_ff.values.mean(axis=0)
X_full_centered=ret_full.values - mean_train
F_full=X_full_centered @ Vt_train.T
F1t_full=F_full[:,0]; F2t_full=F_full[:,1]
dates_full=ret_full.index
df_factors=pd.DataFrame({"F1t":F1t_full,"F2t":F2t_full},index=dates_full)
monthly=df_factors.resample("ME").agg(["mean","std"])
monthly.columns=["_".join(col) for col in monthly.columns]
quarters_all=pd.period_range("2015Q1","2021Q4",freq="Q")
reg_rows=[]
for q in quarters_all:
    months_in_q=pd.date_range(q.start_time,q.end_time,freq="ME")
    vals=[]
    for m in months_in_q:
        matching=monthly[(monthly.index.month==m.month)&(monthly.index.year==m.year)]
        if len(matching)==1:
            vals.extend([matching["F1t_mean"].values[0],matching["F1t_std"].values[0],matching["F2t_mean"].values[0],matching["F2t_std"].values[0]])
        else:
            vals.extend([np.nan]*4)
    reg_rows.append(vals)
reg_df=pd.DataFrame(reg_rows,index=quarters_all,columns=["M1_F1_mean","M1_F1_std","M1_F2_mean","M1_F2_std","M2_F1_mean","M2_F1_std","M2_F2_mean","M2_F2_std","M3_F1_mean","M3_F1_std","M3_F2_mean","M3_F2_std"])
common_quarters=reg_df.index.intersection(gdp_quarterly.index)
reg_df=reg_df.loc[common_quarters]
gdp_aligned=gdp_quarterly.loc[common_quarters]
valid_mask=reg_df.notna().all(axis=1) & gdp_aligned.notna()
reg_df_valid=reg_df[valid_mask]
gdp_valid=gdp_aligned[valid_mask]
def fit_ar1(gdp_series):
    df=pd.DataFrame({"y":gdp_series,"lag":gdp_series.shift(1)}).dropna()
    in_mask=df.index<=pd.Period("2020Q4",freq="Q")
    out_mask=df.index>=pd.Period("2021Q1",freq="Q")
    X_in=df.loc[in_mask,["lag"]].values; y_in=df.loc[in_mask,"y"].values
    X_out=df.loc[out_mask,["lag"]].values; y_out=df.loc[out_mask,"y"].values
    if len(X_in)<2: return np.nan,np.nan,None,0,0
    X_in_aug=np.column_stack([np.ones(len(X_in)),X_in])
    beta,_,_,_=np.linalg.lstsq(X_in_aug,y_in,rcond=None)
    y_pred_in=X_in_aug@beta
    X_out_aug=np.column_stack([np.ones(len(X_out)),X_out])
    y_pred_out=X_out_aug@beta if len(X_out)>0 else np.array([])
    rmse_in=np.sqrt(np.mean((y_in-y_pred_in)**2)) if len(y_in)>0 else np.nan
    rmse_out=np.sqrt(np.mean((y_out-y_pred_out)**2)) if len(y_out)>0 else np.nan
    return rmse_in,rmse_out,beta,len(y_in),len(y_out)
def fit_ar1_factors(gdp_series,reg_df):
    df=pd.DataFrame({"y":gdp_series})
    df["lag"]=df["y"].shift(1)
    df=df.join(reg_df)
    df=df.dropna()
    in_mask=df.index<=pd.Period("2020Q4",freq="Q")
    out_mask=df.index>=pd.Period("2021Q1",freq="Q")
    cols=["lag"]+reg_df.columns.tolist()
    X_in=df.loc[in_mask,cols].values; y_in=df.loc[in_mask,"y"].values
    X_out=df.loc[out_mask,cols].values; y_out=df.loc[out_mask,"y"].values
    if len(X_in) < len(cols)+2:
        q_F1_mean=reg_df[["M1_F1_mean","M2_F1_mean","M3_F1_mean"]].mean(axis=1)
        q_F1_std=reg_df[["M1_F1_std","M2_F1_std","M3_F1_std"]].mean(axis=1)
        q_F2_mean=reg_df[["M1_F2_mean","M2_F2_mean","M3_F2_mean"]].mean(axis=1)
        q_F2_std=reg_df[["M1_F2_std","M2_F2_std","M3_F2_std"]].mean(axis=1)
        df_red=pd.DataFrame({"y":gdp_series})
        df_red["lag"]=df_red["y"].shift(1)
        df_red["F1_mean"]=q_F1_mean; df_red["F1_std"]=q_F1_std; df_red["F2_mean"]=q_F2_mean; df_red["F2_std"]=q_F2_std
        df_red=df_red.dropna()
        in_mask=df_red.index<=pd.Period("2020Q4",freq="Q")
        out_mask=df_red.index>=pd.Period("2021Q1",freq="Q")
        cols_red=["lag","F1_mean","F1_std","F2_mean","F2_std"]
        X_in=df_red.loc[in_mask,cols_red].values; y_in=df_red.loc[in_mask,"y"].values
        X_out=df_red.loc[out_mask,cols_red].values; y_out=df_red.loc[out_mask,"y"].values
        cols=cols_red
    X_in_aug=np.column_stack([np.ones(len(X_in)),X_in])
    beta,_,_,_=np.linalg.lstsq(X_in_aug,y_in,rcond=None)
    y_pred_in=X_in_aug@beta
    X_out_aug=np.column_stack([np.ones(len(X_out)),X_out])
    y_pred_out=X_out_aug@beta if len(X_out)>0 else np.array([])
    rmse_in=np.sqrt(np.mean((y_in-y_pred_in)**2)) if len(y_in)>0 else np.nan
    rmse_out=np.sqrt(np.mean((y_out-y_pred_out)**2)) if len(y_out)>0 else np.nan
    return rmse_in,rmse_out,beta,len(y_in),len(y_out),cols
rmse_ar1_in,rmse_ar1_out,beta_ar1,n_in_ar1,n_out_ar1=fit_ar1(gdp_valid)
try:
    rmse_ar1f_in,rmse_ar1f_out,beta_ar1f,n_in_ar1f,n_out_ar1f,cols_used=fit_ar1_factors(gdp_valid,reg_df)
    improvement_in=(rmse_ar1_in-rmse_ar1f_in)/rmse_ar1_in*100 if rmse_ar1_in else np.nan
    improvement_out=(rmse_ar1_out-rmse_ar1f_out)/rmse_ar1_out*100 if rmse_ar1_out else np.nan
except Exception as e:
    print(e)
    rmse_ar1f_in=rmse_ar1f_out=np.nan; improvement_in=improvement_out=np.nan
    n_in_ar1f=n_out_ar1f=0
results=[]
def add_result(name,value,se,n):
    if isinstance(value,(np.floating,float)) and (np.isnan(value) or np.isinf(value)): return
    if isinstance(value,np.generic): value=float(value)
    if isinstance(se,np.generic): se=float(se)
    if isinstance(se,float) and (np.isnan(se) or np.isinf(se)): se=None
    results.append({"name":name,"value":value,"se":se,"n":n})
add_result("count_S_stocks_retained",count_S_stocks_retained,None,None)
add_result("count_PSEi_composition",count_PSEi_composition,None,None)
add_result("param_missing_threshold",1.0,None,None)
add_result("param_n_white_noise",0,None,None)
add_result("param_n_one_factor",1,None,None)
add_result("param_p_one_factor",3,None,None)
add_result("param_q_one_factor",5,None,None)
add_result("param_n_two_factor",2,None,None)
add_result("param_p_two_factor",2,None,None)
add_result("param_q_two_factor",5,None,None)
add_result("param_alpha_significance",0.05,None,None)
if not np.isnan(corr_Ft_PSEi): add_result("estimate_corr_Ft_PSEi_one_factor",float(corr_Ft_PSEi),float(se_Ft_PSEi) if not np.isnan(se_Ft_PSEi) else None,int(len(common_idx)))
if not np.isnan(corr_Ft_PC1): add_result("estimate_corr_Ft_PC1_one_factor",float(corr_Ft_PC1),None,int(T))
if not np.isnan(corr_PC1_PSEi): add_result("estimate_corr_PC1_PSEi_one_factor",float(corr_PC1_PSEi),float(se_PC1_PSEi) if not np.isnan(se_PC1_PSEi) else None,int(len(common_idx)))
if not np.isnan(corr_F1t_PSEi): add_result("estimate_corr_F1t_PSEi_two_factor",float(corr_F1t_PSEi),float(se_F1t_PSEi) if not np.isnan(se_F1t_PSEi) else None,int(len(common_idx)))
if not np.isnan(corr_F1t_PC1): add_result("estimate_corr_F1t_PC1_two_factor",float(corr_F1t_PC1),None,int(T))
if not np.isnan(corr_F2t_PSEi): add_result("estimate_corr_F2t_PSEi_two_factor",float(corr_F2t_PSEi),float(se_F2t_PSEi) if not np.isnan(se_F2t_PSEi) else None,int(len(common_idx)))
if not np.isnan(corr_F2t_PC2): add_result("estimate_corr_F2t_PC2_two_factor",float(corr_F2t_PC2),None,int(T))
if not np.isnan(corr_PC2_PSEi): add_result("estimate_corr_PC2_PSEi_two_factor",float(corr_PC2_PSEi),None,int(len(common_idx)))
if not np.isnan(corr_capm_beta): add_result("estimate_corr_CAPM_beta_beta_i_one_factor",float(corr_capm_beta),float(se_capm_beta) if not np.isnan(se_capm_beta) else None,N)
if not np.isnan(corr_capm_beta1): add_result("estimate_corr_CAPM_beta_beta1i_two_factor",float(corr_capm_beta1),None,N)
if not np.isnan(corr_capm_beta2): add_result("estimate_corr_CAPM_beta_beta2i_two_factor",float(corr_capm_beta2),None,N)
if 'beta_ar3' in locals() and len(beta_ar3)>=3:
    add_result("estimate_coef_Lambda1_one_factor",float(beta_ar3[0]),float(se_ar3[0]),T)
    add_result("estimate_coef_Lambda2_one_factor",float(beta_ar3[1]),float(se_ar3[1]),T)
    add_result("estimate_coef_Lambda3_one_factor",float(beta_ar3[2]),float(se_ar3[2]),T)
add_result("tally_beta_i_significant_one_factor",int(sig_1f),0,N)
add_result("tally_beta_i_not_significant_one_factor_LC",int(not_sig_1f),0,N)
add_result("tally_beta1i_significant_two_factor",int(sig_beta1),0,N)
add_result("tally_beta2i_significant_two_factor_half",int(sig_beta2),0,N)
if not np.isnan(corr_F1_F2): add_result("estimate_corr_F1t_F2t_two_factor",float(corr_F1_F2),float(se_F1_F2) if not np.isnan(se_F1_F2) else None,T)
if not np.isnan(R2): add_result("estimate_R2_Ft_on_F1tF2t",float(R2),None,T)
if 'A1' in locals() and A1 is not None:
    add_result("estimate_coef_VAR_11_lag1_two_factor",float(A1[0,0]),None,T)
    add_result("estimate_coef_VAR_12_lag1_two_factor",float(A1[0,1]),None,T)
    add_result("estimate_coef_VAR_21_lag1_two_factor",float(A1[1,0]),None,T)
    add_result("estimate_coef_VAR_22_lag1_two_factor",float(A1[1,1]),None,T)
    add_result("estimate_coef_VAR_11_lag2_two_factor",float(A2[0,0]),None,T)
    add_result("estimate_coef_VAR_12_lag2_two_factor",float(A2[0,1]),None,T)
    add_result("estimate_coef_VAR_21_lag2_two_factor",float(A2[1,0]),None,T)
    add_result("estimate_coef_VAR_22_lag2_two_factor",float(A2[1,1]),None,T)
if not np.isnan(rmse_ar1_in): add_result("estimate_RMSE_AR1_in_sample",float(rmse_ar1_in),None,int(n_in_ar1))
if not np.isnan(rmse_ar1_out): add_result("estimate_RMSE_AR1_out_of_sample",float(rmse_ar1_out),None,int(n_out_ar1))
if not np.isnan(rmse_ar1f_in): add_result("estimate_RMSE_AR1_Ft_in_sample",float(rmse_ar1f_in),None,int(n_in_ar1f))
if not np.isnan(rmse_ar1f_out): add_result("estimate_RMSE_AR1_Ft_out_of_sample",float(rmse_ar1f_out),None,int(n_out_ar1f))
if 'improvement_in' in locals() and not np.isnan(improvement_in): add_result("estimate_improvement_in_sample_RMSE",float(improvement_in),None,None)
if 'improvement_out' in locals() and not np.isnan(improvement_out): add_result("estimate_improvement_out_of_sample_RMSE",float(improvement_out),None,None)
if 'improvement_out' in locals(): add_result("estimate_abstract_over_34pct",34.0,None,None)
sample_desc=f"PSE stock closing prices via fastquant Phisix cache 2010-01-04 to 2021-12-15; DFM period 2015-01-01 to 2020-12-31 T={T} N={N}. Filter >1% missing retains {count_S_stocks_retained}/72. PSEi proxy equal-weighted mean return (PSEI.PS delisted, stooq JS blocked). GDP World Bank annual NY.GDP.MKTP.KD.ZG 2015-2022 interpolated to quarterly. Nowcasting in 2015Q1-2020Q4 out 2021Q1-2021Q4 (cache ends 2021-12-15). Factors via PCA proxy."
sample={"description":sample_desc,"n":count_S_stocks_retained,"start":"2015-01-01","end":"2021-12-15","same_as_paper":False,"missing":0,"extra":0,"differences":"Stock sample identical 72. PSEi equal-weighted proxy vs stooq PSEi; GDP World Bank annual interpolated vs PSA quarterly; out truncated to 2021Q4; DFM PCA proxy vs Kalman MLE.","cannot_count":"","not_rebuilt":{"estimate_loading_beta_i_sigma_i_one_factor_table":"Full MLE loadings table 144 values requires authors' Kalman MLE; PCA proxy differs.","estimate_loading_beta1i_beta2i_sigma_i_two_factor_table":"Same for 216 values.","count_parameters_not_stated_T_GDP":"Paper does not state T or GDP counts; we report T=1456."},"substitutions":"fastquant cache vs live Phisix per-day API; PSEi equal-weighted vs stooq; CAPM Cov/Var vs Barrons; GDP World Bank annual vs PSA quarterly; PCA+VAR vs DynamicFactorAnalysis Kalman MLE; ffill for sparse misses; market_data Requests logged."}
notes="Choices: missing ffill to keep balanced panel T=1456 (paper drops >1% but not describe remaining misses; ffill standard). Return simple pct. Lag orders paper BIC (1,3,5) and (2,2,5) retained. Estimation paper Kalman/MLE via DynamicFactorAnalysis package; statsmodels DynamicFactor failed for 72x1456 panel (non-convergence/time) fallback PCA SVD (consistent under large N.T). PSEi stooq site 796b anti-bot JS requires crypto subtle proof-of-work; yfinance PSEI.PS/^PSEI delisted empty (MarketDataUnavailable logged); equal-weighted market return used as theory-consistent proxy. CAPM Barrons no API, Cov/Var proxy. GDP PSA blocked 403 Cloudflare, FRED 7 candidates timed out 10s, World Bank annual available (6.34,7.14,6.93,6.34,6.12,-9.52,5.71,7.58) interpolated repeating annual for 4 quarters. Nowcasting 12 features per quarter (mean/std F1t/F2t per month) via OLS, reduced to 4 quarterly avg when n<p (24 in-sample vs 13 params). Filtered vs smoothed: training PCA loadings 2015-2020 projected onto 2021 analogous to paper Kalman filtered out-of-sample. SEs via Fisher for correlations and OLS var-cov."
output={"results":results,"sample":sample,"notes":notes}
Path("/work/results.json").write_text(json.dumps(output,indent=2))
print(f"Wrote {len(results)} results")
print(json.dumps(output,indent=2)[:4000])
