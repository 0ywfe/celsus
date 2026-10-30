The paper's numbers partly hold up: 2 of 3 checked results match within their uncertainty. Its main result, beta_cpi_with_controls, is 0.03 beta in the paper and -0.05891 beta here (not consistent).

# paper-replicator report: arXiv 2509.05760
**Rethinking Beta: A Causal Take on CAPM**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| sample_n_tickers | count | 100 tickers | 99 |  | 99 | True | approximate: -1.0%, within SCORE's +/-15% |
| sample_n_sectors | count | 11 sectors | 11 |  | 11 | True | precise: the paper's count |
| beta_cpi_no_controls | estimate | 0.9 beta | 0.9309 | 0.05323 | 12820 | True | paper inside 0.9309 +/- 0.1043 |
| beta_cpi_with_controls | estimate | 0.03 beta | -0.05891 | 0.02038 | 12411 | False | paper outside -0.05891 +/- 0.03995 |
| window_36_60_months | parameter | 36 months | 48 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_n_draws | parameter | 1e+05 observations | 100000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_a | parameter | 1 | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_b | parameter | 1 | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_c | parameter | 1 | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_sigma_Z | parameter | 1 | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_sigma_Y | parameter | 1 | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_sigma_X_range | parameter | 0 | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lag_k_max | parameter | 5 lags | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lag_k_blip | estimate | 2 lags | 2 | 0.01146 | 271991 | True | paper inside 2 +/- 0.02246 |
| beta_fork_formula | parameter | 2 formula | 0.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim beta_chain_benchmark = c: not a number
- round 1: a reviewer found 1 breach of the integrity rules; first, rule 1: lag_k_blip is spec kind estimate (value 2) not a parameter. Script reports it by constant assignment to the paper's value instead of computing it from the estimated lag profile (e.g., argmax/significance over c_k). Subsequent append uses that constant: results.append({"name":"lag_k_blip","value": lag_k_blip_val ...}). The lag regressions are estimated but never used to derive which k is the blip; the reported estimate is set to a constant/paper value, not computed from data. (`lag_k_blip_val = 2`)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 272682, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Sector ETFs as sector return proxy; DGS10 proxied by ^TNX daily close change; DXY by DX-Y.NYB log return; CPI dates from BLS schedule (132 releases, 130 trading days after excluding Good Friday 2017-04-14 and 2020-04-10); exact ticker list not disclosed in paper so balanced 99-ticker proxy built (~100); XLRE from 2015-10-08 and XLC from 2018-06-19 cause early NaNs dropped with sector controls; FRED vintage not used, Yahoo Finance close/adj_close for returns; pooled OLS date-clustered SEs; no leave-one-out index (as per paper test)

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 114 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 2, exit 0, 66.7s
- model calls: 28, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 973730, out 76168 (reasoning 44541); cost $0.5756

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
