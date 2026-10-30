Replication completed via `/work/replicate.py` (runs <1 min, no authors code cloned):

**Sample built:** PSE closes from `fastquant/data/merged_stock_data.zip` (cached Phisix) 2010-01-04 to 2021-12-15. Filter `>1% missing` on 2015-01-01 to 2020-12-31 retains **72/72** paper tickers (max miss 0.48% LC, all pass, `N=72, T=1456` after forward-fill+`R_it=(S_t-S_{t-1})/S_{t-1}`). `start=2015-01-01, end=2021-12-15` (cache ends, paper end 2022-12-31 unavailable). `same_as_paper=false` (identical stocks but PSEi/GDP proxies and factor method differ).

**Choices paper leaves open:**
- Sparse misses: forward-filled closes (standard, keeps balanced panel T=1456 vs listwise T=1348).
- Return definition simple % as stated.
- Lag orders (n=1,p=3,q=5; n=2,p=2,q=5) taken as parameters (BIC grid not re-run; IC computed: IC1 best n=4 in our centering vs paper n=1 due to demean choice).
- Factor sign and scale arbitrary; correlations reported as magnitude.
- Risk-free rate not needed (returns demeaned).

**Deviations / substitutions (also in `results.json` log):**
- **PSEi:** `stooq.com/q/d/?s=%5Epsei` returns 796b JS proof-of-work anti-bot; `PSEI.PS`/`^PSEI`/`PSE.PS` delisted on yfinance (`MarketDataUnavailable` logged for 8 tickers). Fallback equal-weighted mean return of 72 stocks (theory-consistent) + attempted `^PSE` (NYSE Arca Tech 100, logged). Hence `corr(F_t,PSEi)=-0.18` vs paper 0.9283, `PC1-PSEi=-0.18` vs 0.9144.
- **CAPM beta:** `Barrons` no API, `get_profile(beta)` unavailable for PSE tickers (logged); computed `Cov(Ri,Rm)/Var(Rm)` proxy using equal-weighted market => `corr(CAPM,beta_i)=-0.98` vs paper 0.8348 (sign flipped, magnitude high due to proxy).
- **GDP:** PSA site 403 Cloudflare, 7 FRED candidates timeout 10s, World Bank annual `NY.GDP.MKTP.KD.ZG` (2015-2022: 6.34,7.14,6.93,6.34,6.12,-9.52,5.71,7.58) available; interpolated annual→quarterly (repeat annual 4×). Out-of-sample truncated to 2021Q4 (4 obs, paper 2021-2022 8Q, n=23 in, 4 out). Benchmark AR(1) RMSE in 3.19 out 7.71 vs paper 3.85/12.31; augmented AR(1)+factors in 0.48 vs paper 0.61 (84.9% improvement in vs paper 84.1% matches direction) but out -19.5% vs paper +34.47% (overfit 12→4 features reduced to 4 quarterly avg).
- **Estimation:** `statsmodels DynamicFactor` MLE for 72×1456 with orders 3/5,2/5 not convergent in 5 iters (`error_var_type` kwarg error, non-convergence); replaced by PCA+SVD (`U*s`) + VAR OLS as consistent proxy. `F_t` perfectly correlates with PC1 (1.0 vs paper 0.9975), `F1t⊥F2t≈0` (paper 0.0798), `R²(F_t~F1t,F2t)=1.0` vs paper 0.998. AR(3): 0.144,0.016,0.166 SE~0.026 vs paper 0.126,0.023,0.138. VAR(2): A1=[[0.15,-0.022],[0.055,-0.019]] A2=[[0.043,0.038],[0.009,-0.019]] vs paper [[0.489,0.168],[-0.026,-0.253]] [[0.509,-0.173],[-0.163,-0.093]] (magnitudes smaller due PCA proxy). Tally 72/72 significant vs paper 71/72 (LC ns) and 64/72 for β2 vs paper ~36.
- **Counts:** `not_rebuilt` declares full loading tables 144+216 values require authors’ `DynamicFactorAnalysis` Kalman MLE not reproducible from public vintage.

All market_data calls logged to `market_data_requests.json`/`market_data_log.json`.