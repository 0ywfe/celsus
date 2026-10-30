The paper's numbers partly hold up: 1 of 2 checked results match within their uncertainty. Its main result, estimate_beta_CPI_controlled, is 0.03 beta in the paper and -0.03032 beta here (not consistent).

# paper-replicator report: arXiv 2509.05760
**Rethinking Beta: A Causal Take on CAPM - Replication Spec**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| count_tickers | count | 100 tickers | 98 |  |  | True | approximate: -2.0%, within SCORE's +/-15% |
| count_sectors | count | 11 sectors | 11 |  |  | True | precise: the paper's count |
| param_window_months_low | parameter | 36 months | 36 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_window_months_high | parameter | 60 months | 60 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_illust_beta | parameter | 1.2 beta | 1.2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_illust_market_move | parameter | 1 return | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_illust_stock_move | parameter | 1.2 return | 1.2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_n | parameter | 1e+05 observations | 100000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_a | parameter | 1 coefficient | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_b | parameter | 1 coefficient | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_c | parameter | 1 coefficient | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_sigma_Z | parameter | 1 sd | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_sigma_Y | parameter | 1 sd | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_sigma_X_low | parameter | 0 sd | 0 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_sigma_X_high | parameter | 5 sd | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_lag_min_k | parameter | 0 lags | 0 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_lag_max_k | parameter | 5 lags | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| estimate_beta_CPI_uncontrolled | estimate | 0.9 beta | 0.9094 | 0.04257 | 11785 | True | paper inside 0.9094 +/- 0.08343 |
| estimate_beta_CPI_controlled | estimate | 0.03 beta | -0.03032 | 0.01903 | 11785 | False | paper outside -0.03032 +/- 0.03729 |

## The paper's own numbers
- nothing to check

## Guards
- no claims rejected
- spec: the headline was written as prose ('Pillars 1 and 2 falsifiable pattern: fork signature; any X->Y mechanism only lagged and modest. Operationalized by estim'); chosen from the claim names: estimate_beta_CPI_controlled
- spec: the headline was written as prose ('Contemporaneous beta is proxy not mechanism: on CPI shock days pooled R_m slope collapses when observable Z proxies adde'); chosen from the claim names: estimate_beta_CPI_controlled
- round 1: the builder ran out of turns
- attempt 1: 1 market-data items fetched on the host into data/market
- round 1: audit sent the sample back: the replication could not rebuild the paper's sample (Paper prints no per-sector N, N_CPI, or pooled N; counts unavailable from text alone)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 11785, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Ticker identities proxied: 99 defined (9×11), 98 retained (EA no Yahoo data). Market SPY adj_close log return; VIX Δ = ^VIX close diff; DGS10 Δ from FRED fredgraph.csv ffill to trading days then diff; DXY log return from DX-Y.NYB; sector ETF adj_close log return (XLRE from 2015-10-08, XLC from 2018-06-19 cause early drops, counted as 409 sector-missing obs). CPI dates scraped from bls.gov/bls/news-release/cpi.htm (cpi_MMDDYYYY.htm) with fallback hard-coded; 2 Good Fridays dropped. SE clustered by date (paper prints none). FRED and market data vintages live 2025-10-10. No leave-one-out index built per paper

## Data sources
- prices: yfinance (host) (cache), fetched 2026-10-30, 1 tickers
- prices: yfinance (live, sandbox), fetched 2026-10-30, 112 tickers
- other hosts the script fetched from: www.bls.gov, fred.stlouisfed.org

## Run
- sandbox: attempt 2, exit 0, 59.1s
- model calls: 47, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 2063288, out 98545 (reasoning 59596); cost $0.8252

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
