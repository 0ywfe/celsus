All 170 claims recomputed from public data; no paper-reported number is hard-coded. `python /work/replicate.py` fetches daily closes from East Money (`secid 1.000001,0.399001,0.399006,1.000932,1.000933,1.000934` — the only public vendor with continuous 2013-2023 CSI/ChiNext history; `market_data` yfinance is probed for `000001.SS/399001.SZ/159915.SZ` and logged in `market_data_log.json` but has only 1-day future prices for CSI/ChiNext) and via `requests`, computes simple returns `(close/prev-1)*100`.

**Sample built:** 2013-02-26 – 2023-03-31, 2456 trading-day returns (2457 klines). Paper: 2452 returns Feb 2013-Mar 2023 (end-date ambiguous). `same_as_paper=false`, extra 4 trading days due to inclusive Mar-31 end; vendor difference causes minor shifts (SSE mean 0.023 vs paper 0.021, q10 -1.257 vs -1.285, etc.). Train/val 85/15 = `floor(0.85*2456)=2087/369` vs paper 2084/368.

**Open choices made standard:**
- Return = simple percent; time = trading-day index; `ω` per trading-day.
- Quantiles = `pandas.DataFrame.quantile(0.10/0.90)` linear interpolation.
- `ω` chosen by grid-search maximising likelihood over `[0.05,0.08,0.1,0.2,0.5]` (paper: grid-search, value 0.1 – our data selects 0.05).
- Bivariate Hawkes `λ_k=μ_k+∑α_{kj}ωexp(-ωΔt)`, `μ>0,α≥0`, MLE `L=∏λ_{d_i}exp(-∑∫λ)`, `∫=μT+∑α(1-exp(-ω(T-t_i)))`, optimised with `scipy.optimize.minimize L-BFGS-B` (paper: `tick` module, optimiser/initi undocumented).
- Sector 6-dim: `λ=g(μ̅)`, `μ̅=μ+αωexp(-ωt)`, `g=max(x,0.01)` (`link_threshold=0.01`), `∫` via Monte-Carlo `N=60` uniform samples (paper algorithm 1, `N`/lr/init/epochs not stated), `L-BFGS-B` from baseline-derived init; 15 periods of 150 returns (`available=16`).
- Homogeneous Poisson `λ̂=n/T`.

**Deviation:** East Money substitution required; descriptive/Hawkes/6-dim numeric values differ from paper due to vendor/end-date/optimiser stochasticity but are fully data-computed. Period-3/5 `A,μ,ω` are best-effort replications (paper SGD path irreproducible).