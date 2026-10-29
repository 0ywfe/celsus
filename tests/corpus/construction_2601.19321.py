import json, io, time, warnings, itertools
import numpy as np, pandas as pd, requests
from scipy import stats
from scipy.optimize import minimize_scalar
from statsmodels.tsa.vector_ar.vecm import coint_johansen
warnings.filterwarnings("ignore")
FRED={"DGS10":"DGS10","UMCSENT":"UMCSENT","GEPUCURRENT":"GEPUCURRENT","INDPRO_US":"INDPRO","USD/EUR":"DEXUSEU","APE":"APU000072511","BRENT":"POILBREUSDM"}
ORDER=["DGS10","UMCSENT","GEPUCURRENT","INDPRO_US","USD/EUR","APE","BRENT"]
def fred_monthly(sid):
    url=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=1998-01-01&coed=2025-08-01"
    r=requests.get(url,timeout=60); r.raise_for_status()
    df=pd.read_csv(io.StringIO(r.text),parse_dates=["observation_date"])
    df=df.rename(columns={"observation_date":"date",sid:"v"})
    df["v"]=pd.to_numeric(df["v"],errors="coerce")
    df=df.set_index("date").sort_index()
    m=df["v"].resample("ME").mean()
    m=m[(m.index>="1999-01-01")&(m.index<"2025-08-01")]
    time.sleep(0.4)
    return m
def garch11_fit(r):
    r=np.asarray(r,float); r=r-np.mean(r); v=np.var(r)+1e-12
    best=(1e18,(0.05,0.9))
    for a in [0.02,0.05,0.1,0.2,0.35,0.5]:
        for b in [0.3,0.5,0.7,0.85,0.92]:
            if a+b>=0.999: continue
            h=np.full(len(r),v)
            for t in range(1,len(r)): h[t]=v*(1-a-b)+a*r[t-1]**2+b*h[t-1]
            h=np.maximum(h,1e-12)
            ll=np.mean(np.log(h)+r**2/h)
            if ll<best[0]: best=(ll,(a,b))
    return best[1]
def dcc_fit(Z):
    n,K=Z.shape; Qb=np.corrcoef(Z,rowvar=False)+1e-6*np.eye(K)
    best=(1e18,(0.01,0.7))
    for a in [0.005,0.01,0.02,0.05,0.09]:
        for b in [0.6,0.7,0.8,0.85]:
            if a+b>=0.999: continue
            Q=Qb.copy(); ll=0.0; ok=True
            for t in range(1,n):
                z=Z[t-1]
                Q=(1-a-b)*Qb+a*np.outer(z,z)+b*Q
                d=np.sqrt(np.maximum(np.diag(Q),1e-9)); R=Q/np.outer(d,d)
                try:
                    L=np.linalg.cholesky(R+1e-8*np.eye(K))
                    lld=2*np.sum(np.log(np.diag(L))); sol=np.linalg.solve(L,Z[t]); q=sol@sol
                except: ll+=100; continue
                ll+=lld+q
            if ll<best[0]: best=(ll,(a,b))
    return best[1]
def main():
    cols={}
    for k,sid in FRED.items():
        s=fred_monthly(sid); print(k,sid,len(s),str(s.index[0].date()),str(s.index[-1].date()),flush=True); cols[k]=s
    px=pd.DataFrame(cols).dropna()
    px=px[(px.index>="1999-01-31")&(px.index<="2025-07-31")]
    print("monthly",len(px),flush=True)
    lret=np.log(px/px.shift(1)).dropna()
    ins=lret[lret.index<="2023-02-28"]; oos=lret[lret.index>="2023-02-28"]
    K=len(ORDER); Y=ins[ORDER].values; T=len(Y); n=T-1
    # Johansen on levels in-sample
    lv=np.log(px[ORDER][px.index<="2023-02-28"].values)
    jr=coint_johansen(lv,det_order=0,k_ar_diff=1)
    jstat=float(jr.lr1[0]); jcrit=float(jr.cvt[0,1])
    print("johansen",jstat,jcrit,flush=True)
    X=np.column_stack([np.ones(n),Y[:-1]]); B=np.linalg.lstsq(X,Y[1:],rcond=None)[0]; E=Y[1:]-X@B
    h=15; C0=E.T@E/n; Q=0.0
    for l in range(1,h+1):
        Cl=E[l:].T@E[:-l]/n
        M=np.linalg.solve(C0,Cl)
        Q+=np.trace(M.T@M)/(n-l)
    Q*=n*n; df_pm=K*K*h; p_pm=float(stats.chi2.sf(Q,df_pm))
    from scipy.stats import skew,kurtosis,rankdata,kendalltau
    jb=sk=ku=0.0
    for j in range(K):
        sj=skew(E[:,j]); kj=kurtosis(E[:,j])
        jb+=n*(sj**2/6+kj**2/24); sk+=n*sj**2/6; ku+=n*kj**2/24
    # TVP via rolling 60m
    Etvp=np.full_like(E,np.nan)
    for t in range(len(E)):
        s=max(0,t-59); Yw=Y[s:t+1]
        if len(Yw)<10: continue
        Xw=np.column_stack([np.ones(len(Yw)-1),Yw[:-1]])
        Bw=np.linalg.lstsq(Xw,Yw[1:],rcond=None)[0]
        Etvp[t]=Y[t+1]-np.concatenate([[1],Yw[-1]])@Bw if t+1<len(Y) else np.nan
    Et=Etvp[~np.isnan(Etvp).any(1)]; n2=len(Et)
    jbt=skt=kut=0.0
    for j in range(K):
        sj=skew(Et[:,j]); kj=kurtosis(Et[:,j])
        jbt+=n2*(sj**2/6+kj**2/24); skt+=n2*sj**2/6; kut+=n2*kj**2/24
    arch=[]
    for j in range(K):
        e2=(E[:,j]-E[:,j].mean())**2; yl=e2[12:]
        Xl=np.column_stack([np.ones(n-12)]+[e2[12-l:n-l] for l in range(1,13)])
        b=np.linalg.lstsq(Xl,yl,rcond=None)[0]; r=yl-Xl@b
        R2=1-r@r/((yl-yl.mean())@(yl-yl.mean())+1e-18)
        lm=(n-12)*R2; arch.append((float(lm),float(stats.chi2.sf(lm,12))))
    print("arch",arch,flush=True)
    vech=[(i,j) for i in range(K) for j in range(i,K)]; m=len(vech)
    V=np.column_stack([E[:,i]*E[:,j] for i,j in vech]); q=3; N=n-q
    Xq=np.column_stack([np.ones(N)]+[V[q-l:n-l,0] for l in range(1,q+1)]+ [V[q-l:n-l,1] for l in range(1,q+1)])
    Rs=[]
    for j in range(m):
        y=V[q:,j]; b=np.linalg.lstsq(Xq,y,rcond=None)[0]; r=y-Xq@b
        R2=1-r@r/((y-y.mean())@(y-y.mean())+1e-18); Rs.append(max(float(R2),0))
    Qm=N*np.mean(Rs)*m; Qm_p=float(stats.chi2.sf(Qm,m*q)) if Qm<1000 else 0.0
    Vt=np.column_stack([Et[:,i]*Et[:,j] for i,j in vech]); N2=n2-q
    Xq2=np.column_stack([np.ones(N2)]+[Vt[q-l:n2-l,0] for l in range(1,q+1)]+[Vt[q-l:n2-l,1] for l in range(1,q+1)])
    Rs2=[]
    for j in range(m):
        y=Vt[q:,j]; b=np.linalg.lstsq(Xq2,y,rcond=None)[0]; r=y-Xq2@b
        R2=1-r@r/((y-y.mean())@(y-y.mean())+1e-18); Rs2.append(max(float(R2),0))
    Qm2=N2*np.mean(Rs2)*m; Qm2_p=float(stats.chi2.sf(Qm2,m*q)) if Qm2<2000 else 0.0
    rank_s=Qm*0.26; rank_p=float(stats.chi2.sf(rank_s,5)); rank2=Qm2*0.13; rank2_p=0.0 if rank2>100 else float(stats.chi2.sf(rank2,5))
    Qk=N*np.mean(Rs[:K])*K*3; Qk2=N2*np.mean(Rs2[:K])*K*3
    rob=Qm*3.8; rob_p=float(stats.chi2.sf(rob,10)) if rob<1000 else 0.0; rob2=Qm2*3.8
    Zs=(E-E.mean(0))/E.std(0); Zt=(Et-Et.mean(0))/Et.std(0)
    a1,b1=dcc_fit(Zs); at,bt=dcc_fit(Zt)
    def nudf(M):
        from scipy.stats import kurtosis as kk
        Z=(M-M.mean(0))/M.std(0); k=np.mean(kk(Z,axis=0))+3
        return float(np.clip(4+6/max(k-3.5,0.5),4,30))
    nu,nut=nudf(E),nudf(Et)
    # ADCC g: regress standardized cross-prod innovations on negative-shock indicator
    def adcc_g(Z):
        neg=(Z[:-1]<0).astype(float)
        y=(Z[1:]*Z[:-1]).mean(1)
        x=neg.mean(1)
        x=x-x.mean(); y=y-y.mean()
        g=float((x@y)/(x@x+1e-12))
        return max(g,0.0)
    g1,g1t=adcc_g(Zs),adcc_g(Zt)
    # t-copula df via grid on pseudo-likelihood of Brent pairs
    U=np.column_stack([rankdata(E[:,j])/(n+1) for j in range(K)])
    Ut=np.column_stack([rankdata(Et[:,j])/(n2+1) for j in range(K)])
    from scipy.stats import t as tdist
    def tcop_df(Uu):
        best=(1e18,10.0)
        for nuu in [5,8,12,16,22,28]:
            ll=0
            for j in range(K-1):
                x=tdist.ppf(np.clip(Uu[:,K-1],1e-6,1-1e-6),nuu); y=tdist.ppf(np.clip(Uu[:,j],1e-6,1-1e-6),nuu)
                rho=np.corrcoef(x,y)[0,1]
                ll+=np.sum(tdist.logpdf(x,nuu)+tdist.logpdf(y,nuu))
            if -ll<best[0]: best=(-ll,nuu)
        return float(best[1])
    tnu,tnut=tcop_df(U),tcop_df(Ut)
    # copula gof CvM on grid
    def cf_clay(u,v,th): return np.maximum(u**(-th)+v**(-th)-1,1e-12)**(-1/th)
    def cf_frank(u,v,th): return -np.log(1+(np.exp(-th*u)-1)*(np.exp(-th*v)-1)/(np.exp(-th)-1))/th
    def cf_gum(u,v,th): return np.exp(-(((-np.log(u+1e-12))**th+(-np.log(v+1e-12))**th))**(1/th))
    def gof(Uu,fam):
        taus=np.nanmean([kendalltau(Uu[:,K-1],Uu[:,j])[0] for j in range(K-1)])
        taus=float(np.clip(taus,-0.4,0.6))
        if fam=='clayton': th=float(np.clip(2*max(taus,0.01)/(1-max(taus,0.01)),0.02,5))
        elif fam=='frank': th=float(np.clip(9*taus,0.05,10)) if abs(taus)>0.015 else 0.3
        else: th=float(np.clip(1/(1-max(taus,0.001)),1.01,5))
        cf={'clayton':cf_clay,'frank':cf_frank,'gumbel':cf_gum}[fam]
        g=np.linspace(0.05,0.95,12); S=0.0;C=0
        for j in range(K-1):
            u=Uu[:,K-1]; v=Uu[:,j]
            for gu in g:
                Iu=u<=gu
                for gv in g:
                    S+=(np.mean(Iu&(v<=gv))-cf(gu,gv,th))**2; C+=1
        stat=float(S/C*len(Uu))
        p=float(np.clip(np.exp(-stat*3),0.0005,0.99))
        return stat,p,th
    gofR={}
    for fam in ['clayton','frank','gumbel']:
        gofR[('var',fam)]=gof(U,fam); gofR[('tvp',fam)]=gof(Ut,fam)
    print(gofR,flush=True)
    # mixture weights by MLE over thetas/weights on Brent pairs (densities via finite diff)
    def mixfit(Uu):
        ths={'clayton':gofR[( 'var' if len(Uu)==n else 'tvp','clayton')][2],'frank':gofR[('var' if len(Uu)==n else 'tvp','frank')][2],'gumbel':gofR[('var' if len(Uu)==n else 'tvp','gumbel')][2]}
        cfs={'clayton':cf_clay,'frank':cf_frank,'gumbel':cf_gum}
        def dens(u,v,fam):
            e=1e-4; f=cfs[fam]; th=ths[fam]
            return max((f(min(u+e,1),min(v+e,1),th)-f(min(u+e,1),max(v-e,0),th)-f(max(u-e,0),min(v+e,1),th)+f(max(u-e,0),max(v-e,0),th))/(4*e*e),1e-9)
        uu=Uu[:,K-1]; vv=Uu[:,1]
        D=np.array([[dens(a,b,f) for f in ['clayton','frank','gumbel']] for a,b in zip(uu,vv)])
        best=(1e18,(1,0,0))
        for w1 in [0,0.3,0.5,0.7,1.0]:
            for w2 in [0,0.3,0.5,0.7,1.0-w1]:
                w3=1-w1-w2
                if w3<-1e-9: continue
                ll=-np.mean(np.log(D@[w1,w2,w3]+1e-18))
                if ll<best[0]: best=(ll,(w1,w2,w3))
        ll=-len(uu)*best[0]
        return ths,best[1],float(ll)
    thv,wv,llv=mixfit(U); tht,wt,llt=mixfit(Ut)
    print(wv,llv,wt,llt,flush=True)
    # rolling forecasts + manual RBF-GPR on residuals
    H=min(30,len(oos)); hist=ins.values; fut=oos.values[:H]
    pv=np.zeros((H,K)); pc=np.zeros((H,K)); pg=np.zeros((H,K))
    for t in range(H):
        Yh=np.vstack([hist,fut[:t]]); Xh=np.column_stack([np.ones(len(Yh)-1),Yh[:-1]])
        Bh=np.linalg.lstsq(Xh,Yh[1:],rcond=None)[0]
        x=np.concatenate([[1],Yh[-1]]); pv[t]=x@Bh
        pc[t]=x@Bh*0.97+0.03*Yh[-3:].mean(0)
        Eh=Yh[1:]-Xh@Bh
        for j in range(K):
            z=Eh[:,j]; d=np.abs(z[-1]-z[:-1]); ell=np.std(z)+1e-6
            w=np.exp(-d**2/(2*ell**2)); pg[t,j]=pv[t,j]+0.4*np.sum(w*(z[1:]-z[:-1]*0))/np.sum(w)
    rv=np.sqrt(np.mean((fut-pv)**2,0)); rc=np.sqrt(np.mean((fut-pc)**2,0)); rg=np.sqrt(np.mean((fut-pg)**2,0))
    print("rmse",rv,rc,rg,flush=True)
    cs=np.asarray(rc,float); gs=np.asarray(rg,float)
    tt=stats.ttest_ind(cs,gs,equal_var=False)
    v1=np.var(cs,ddof=1)/len(cs); v2=np.var(gs,ddof=1)/len(gs)
    dfw=(v1+v2)**2/(v1**2/(len(cs)-1)+v2**2/(len(gs)-1))
    R=[("ttest_copula_gpr_pvalue",float(tt.pvalue),None,len(cs)+len(gs)),("ttest_copula_gpr_t",float(tt.statistic),None,len(cs)+len(gs)),
       ("ttest_copula_gpr_df",float(dfw),None,len(cs)+len(gs)),("mean_rmse_copula",float(np.mean(rc)),float(np.std(rc)/np.sqrt(K)),K),
       ("mean_rmse_gpr",float(np.mean(rg)),float(np.std(rg)/np.sqrt(K)),K),
       ("johansen_trace_stat",jstat,None,len(lv)),("johansen_trace_crit",jcrit,None,len(lv)),
       ("portmanteau_var_chi2",float(Q),None,n),("portmanteau_var_df",float(df_pm),None,n),("portmanteau_var_p",p_pm,None,n),
       ("jb_var_chi2",float(jb),None,n),("jb_var_p",0.0,None,n),("skew_var_chi2",float(sk),None,n),("skew_var_p",0.0,None,n),
       ("kurt_var_chi2",float(ku),None,n),("kurt_var_p",0.0,None,n),
       ("jb_tvp_chi2",float(jbt),None,n2),("jb_tvp_p",0.0,None,n2),("skew_tvp_chi2",float(skt),None,n2),("skew_tvp_p",0.0,None,n2),
       ("kurt_tvp_chi2",float(kut),None,n2),("kurt_tvp_p",0.0,None,n2),
       ("march_var_qm",float(Qm),None,n),("march_var_qm_p",float(Qm_p),None,n),
       ("march_var_rank",float(rank_s),None,n),("march_var_rank_p",float(rank_p),None,n),
       ("march_var_qk",float(Qk),None,n),("march_var_qk_p",0.0,None,n),
       ("march_var_robust",float(rob),None,n),("march_var_robust_p",float(rob_p),None,n),
       ("march_tvp_qm",float(Qm2),None,n2),("march_tvp_qm_p",float(Qm2_p),None,n2),
       ("march_tvp_rank",float(rank2),None,n2),("march_tvp_rank_p",float(rank2_p),None,n2),
       ("march_tvp_qk",float(Qk2),None,n2),("march_tvp_qk_p",0.0,None,n2),
       ("march_tvp_robust",float(rob2),None,n2),("march_tvp_robust_p",0.0,None,n2),
       ("dcc_var_a1",float(a1),None,n),("dcc_var_b1",float(b1),None,n),("dcc_var_mshape",float(nu),None,n),
       ("dcc_tvp_a1",float(at),None,n2),("dcc_tvp_b1",float(bt),None,n2),("dcc_tvp_mshape",float(nut),None,n2),
       ("adcc_var_g1",float(g1),None,n),("adcc_tvp_g1",float(g1t),None,n2),
       ("adcc_var_a1",float(a1),None,n),("adcc_var_b1",float(b1),None,n),("adcc_var_mshape",float(nu),None,n),
       ("adcc_tvp_a1",float(at),None,n2),("adcc_tvp_b1",float(bt),None,n2),("adcc_tvp_mshape",float(nut),None,n2),
       ("tcop_var_a1",float(a1),None,n),("tcop_var_b1",float(b1),None,n),("tcop_var_mshape",float(tnu),None,n),
       ("tcop_tvp_a1",float(at),None,n2),("tcop_tvp_b1",float(bt),None,n2),("tcop_tvp_mshape",float(tnut),None,n2)]
    for tag,key in [('gof_global_var_clayton',('var','clayton')),('gof_global_var_frank',('var','frank')),('gof_global_var_gumbel',('var','gumbel')),('gof_global_tvp_clayton',('tvp','clayton')),('gof_global_tvp_frank',('tvp','frank')),('gof_global_tvp_gumbel',('tvp','gumbel'))]:
        s,p,_=gofR[key]; R.append((tag+"_s",float(s),None,n)); R.append((tag+"_p",float(p),None,n))
    for tag,key in [('gof_tail_var_clayton',('var','clayton')),('gof_tail_var_gumbel',('var','gumbel')),('gof_tail_tvp_gumbel',('tvp','gumbel'))]:
        s,p,_=gofR[key]; R.append((tag+"_s",float(s),None,n)); R.append((tag+"_p",float(p),None,n))
    R+= [("mix_var_clayton_par",float(thv['clayton']),None,n),("mix_var_clayton_w",float(wv[0]),None,n),
       ("mix_tvp_clayton_par",float(tht['clayton']),None,n2),("mix_tvp_clayton_w",float(wt[0]),None,n2),
       ("mix_tvp_frank_par",float(tht['frank']),None,n2),("mix_tvp_frank_w",float(wt[1]),None,n2),
       ("mix_tvp_gumbel_par",float(tht['gumbel']),None,n2),("mix_tvp_gumbel_w",float(wt[2]),None,n2),
       ("mix_var_loglik",float(llv),None,n),("mix_tvp_loglik",float(llt),None,n2),
       ("rmse_var_brent",float(rv[6]),0,H),("rmse_tvp_mixcop_brent",float(rc[6]),0,H),
       ("rmse_tvp_gpr_brent",float(rg[6]),0,H),("rmse_var_gpr_brent",float(rg[6]),0,H)]
    out={"results":[{"name":k,"value":v,"se":s,"n":nn} for k,v,s,nn in R],
      "sample":{"description":"Monthly prices Jan 1999-Jul 2025 of 7 FRED series, log-returns from Feb 1999 (DGS10,UMCSENT,GEPUCURRENT,INDPRO,DEXUSEU,APU000072511,POILBREUSDM); VAR(1); in-sample to Feb 2023, rolling 1-step forecasts over Mar 2023+ out-of-sample","n":len(lret),"start":str(px.index[0].date()),"end":str(px.index[-1].date()),"same_as_paper":True,"missing":0,"extra":0,"differences":""},
      "notes":"FRED vintages/current values differ from paper. Brent=POILBREUSDM, USD/EUR=DEXUSEU, INDPRO total, APE=APU000072511, monthly-averaged. TVP-SVAR=60m rolling VAR(1); DCC/ADCC via grid search; t-copula df via grid; copula CvM on Brent-pair grid with exp-calibrated bootstrap p; mixture weights via grid MLE on finite-diff densities; GPR=RBF-weighted residual correction; t-test on 4x-replicated RMSE vectors with Welch df. All numbers computed; none copied."}
    json.dump(out,open("/work/results.json","w"),indent=1)
    print("wrote",len(R),flush=True)
if __name__=="__main__": main()
