**Sample built**

* **Overall calendar:** `1994-01-03` → `2025-12-31` (latest year printed in paper). Total `14 197` daily trading-days summed over 3 independent baskets.
* **G10 FX – 10 series** (paper only says “G10”, no tickers): `EURUSD=X,GBPUSD=X,AUDUSD=X,NZDUSD=X,USDCAD=X,USDJPY=X,USDCHF=X,USDNOK=X,USDSEK=X,DX-Y.NYB` (9 majors vs USD + `DX-Y.NYB` as USD proxy). Train `2006-01-03–2009-12-31` =891 days (inner-join truncates `2006-01–2006-05-16` because `AUDUSD=X` starts 2006-05-16, –87 days), Test `2010-01-04–2025-12-31`=4016 days.
* **Factor ETFs – 5 series:** `IFSU.L,IUSZ.L,IUVL.L,IUMO.L,IUQA.L` (paper lists tickers without exchange; LSE listings from ISIN). Train `2021-01-04–2022-12-30`=502 days, Test `2023-01-03–2025-12-31`=757 days.
* **US Treasuries – 4 series** (paper: basket size & tenors not stated, Fig 3 shows 5 lines): `^IRX(13W),^FVX(5Y),^TNX(10Y),^TYX(30Y)` – longest-history yfinance yields. Train `1994-01-03–1998-12-31`=1251 days, Test `1999-01-04–2025-12-31`=6782 days.

Every series fetched via `market_data.get_prices` (cache → yfinance live). `X_t` = daily log-returns (FX/ETF) and daily yield *changes* (TSY). Lag `T=1` day, demeaned sample `C0` (`N-1`) and symmetrised `C(T)=½(E[X_{t+T}X_t^T]+E[X_t X_{t+T}^T])`, `scipy.linalg.eigh` (=LAPACK `gvd`). Five slowest = largest `λ∈[-1,1]`, `t_i=-2T/(λ_i-1)`. Non-linear `k=4`: `g(u)=u^7, g'=7u^6`, whitened symmetric FastICA `1000 iter tol1e-6 seed0` SVD orthogonalisation.

**Choices paper leaves open**

* Vendor `yfinance` (paper: none), frequency daily `close` (paper: not stated), transform log-return/change vs “prices or returns”, lag `T=1d`, covariance estimator, demeaning, solver, normalisation `W^TC0W=I` (plot rescaled to unit gross only), FastICA init/tolerance, training windows to trading-day boundaries (paper labels overlap `2010` etc).

**Deviations / proxies**

* G10 exact 10 not stated → 9 crosses + DXY; `AUDUSD` start 2006-05-16 forces inner-join loss. Treasuries `n` not stated → 4 yields vs Fig-5. ETF `.L` suffix omitted. Levels alternative (`log-price` G10 corr 0.987, TSY level corr 0.965) reported alongside returns because `λ≈1` (paper’s timescale formula) only occurs for levels; return version still positive `0.447/0.645/0.835`.
* Paper’s headline is purely visual (no `λ,t_i,p`). Operationalised: Pearson `corr(λ_IS,λ_OOS)` G10 10-comp 0.447±0.253, ETF 0.645±0.261, TSY 0.835±0.151; slowest `λ_IS→OOS` G10 0.162→-0.340 (2.4→1.5 d), ETF 0.137→-0.021, TSY 0.590→0.030; mean `Δλ` –0.10/–0.06/+0.05. Orthogonality `‖off(W^TC0W)‖_F` IS 0 → OOS 3.88/1.13/0.83 (decays as expected). Non-linear tail `λ_tail=E[Y_t^{7}Y_{t+T}]` corr `k=4`: –0.18/–0.11/0.97.
* `same_as_paper:false` – counts/filters/tickers/frequency not printed → `missing/extra:null`, `cannot_count` explained. No `not_rebuilt`.

**Flash-crash background:** paper `9%`; `SPY` low-vs-prev-close –10.1 %, `^GSPC` –8.6 % intraday (–8.7 % high-low), close-close –3.2 % – consistent within range.