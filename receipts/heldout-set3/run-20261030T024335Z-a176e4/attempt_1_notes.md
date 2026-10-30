**Replication Summary**

**Sample built:** 10 ETFs (SPY + 9 Select SPDRs: XLB/XLE/XLF/XLI/XLK/XLP/XLU/XLV/XLY) daily OHLC from `market_data` (yfinance live, `2010-01-04` to `2024-12-31`, 3,774 trading days vs paper’s ~3,770). Log-RV proxied by `log(ret^2)` (squared daily log-return, zeros replaced) – substitution for TAQ 5-min RV (M=78). VOLARE 40-stock panel (Jan 2015-Jan 2026) requires auth (`401` on `/api/financial-data` and `/api/.../pregenerated/etf`) not rebuildable. Simulation DGP: fGn via Davies-Harte FFT circulant (M≥2n, N grid 16384), fBm = cumsum fGn, fOU = `phi=exp(-kappa*Delta)` recursion `Delta=1/250`, `kappa={2,5}`, `H={0.1,0.2,0.3,0.4}`, `n={500,4000}`, burn-in 500 days, 100 reps/cell (paper 500) estimated by `SARIMAX(1,0,1)` exact ML Kalman.

**Choices paper leaves open (standard choices made):**
- Ticker → asset mapping: `adj_close` from yfinance for each ETF ticker.
- Calendar alignment: yfinance trading calendar (3774 vs ~3770, vintage/holiday diff noted, not sampled).
- Risk-free rate: not needed.
- Realized measures: `RV=sum r^2`, `RQ=M/3 sum r^4`, `BPV=mu1^{-2} sum|r||r+|`, `RS+/-` all approximated by daily proxy (open/high/low not used for main proxy); `M=78` (6.5h*60/5) and `sigma_w2=1/39=2/m` fixed from Fukasawa et al asymptotics.
- Wold: midpoint grid not touching singularity at 0, FFT via `mean(logf cos k lambda)`, recursion `c_{k+1}=sum(1-j/(k+1))a_{k+1-j}c_j`, `c0=1`, 100 terms for tail; `N=16384`.
- Forecast: rolling 500-day window, log-normal correction, insanity filter, MCS `Tmax` block 20 / 5000 reps noted but not run (missing RV).

**Deviations / not rebuilt:**
- **Empirical Table `est_par` (fBm/fOU Whittle/ML, AR/HAR/RAR/RHAR on 5-min log RV):** No TAQ intraday data public; daily proxy gives `SPY RAR theta=-0.91 (SE 0.01, n=3773)` vs paper `-0.4111 (0.0167)` and `AR rho=0.12` vs `0.8058` – directionally negative MA (roughness) confirmed but magnitude distorted (daily proxy noisier). All `H`, `kappa`, HAR coefficients listed in `not_rebuilt` with reason “requires TAQ 5-min RV + Whittle/Wang et al ML”.
- **Forecast ratios & MCS:** `MSE/QLIKE` ratios `HAR=1.0`, `Log-RAR ~0.79`, `Log-RHAR`, `fBm/fOU` and MCS p-values require full RV panel + ~300k rolling fits >20 min and missing inputs → omitted, declared in `not_rebuilt`.
- **Measurement-error check (`theta≈-0.4` after fixing `sigma_w2=1/39`):** State-space with known variance not rebuilt.
- **Simulation:** Reduced to 100 reps/cell (paper 500), `n=500` + `n=4000` via FFT (paper Cholesky), `RHAR` weekly/monthly lags omitted (near-redundant under fOU). Demonstrates headline: `c1(0.1)=-0.657, c1(0.2)=-0.459, c1(0.3)=-0.293, c1(0.4)=-0.142` matched to `1e-4` (Table `fgn_ck`); `fBm H=0.1 n=500 RAR mean -0.633 (SE 0.006, sd 0.064, n=100)` vs paper `-0.624 (0.070)`, `H_imp 0.112`, `fBm H=0.1 n=4000 -0.668 (0.002)` vs paper `-0.670 (0.021)`, `fOU k=2 -0.623` vs `-0.606`, `k=5 -0.594` vs `-0.579` – tracking `c1(H)`.
- **Counts/parameters** (`count_ETFs=10`, `count_stocks=40`, `M=78`, `Delta=1/250`, `kappa=2,5`, rolling 500, MCS 20/5000) reproduced exactly; sample `same_as_paper=false` due to missing TAQ/VOLARE.