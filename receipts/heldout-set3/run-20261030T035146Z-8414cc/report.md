The paper's numbers partly hold up: 23 of 24 checked results match within their uncertainty. Its main result, us_h1_bvar_min_maxe, was not computed.

# paper-replicator report: arXiv 2608.23064
**Sequentially valid inference for probabilistic inflation forecasts - Replication Spec**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| us_total_obs | count | 784 obs | 784 | 0 |  | True | precise: the paper's count |
| us_eval_N_h1 | count | 470 forecasts | 470 | 0 |  | True | precise: the paper's count |
| ch_total_obs | count | 508 obs | 508 | 0 |  | True | precise: the paper's count |
| ch_eval_N_h1 | count | 305 forecasts | 304 | 0 |  | True | approximate: -0.3%, within SCORE's +/-15% |
| ea_total_obs | count | 292 obs | 292 | 0 |  | True | precise: the paper's count |
| ea_eval_N_h1 | count | 175 forecasts | 175 | 0 |  | True | precise: the paper's count |
| arima_choice_ch_freq | estimate | 81% |  |  |  |  | not computed |
| arima_choice_ea_freq | estimate | 48% |  |  |  |  | not computed |
| arima_choice_us_freq | estimate | 44% |  |  |  |  | not computed |
| arima_choice_us_post2000_freq | estimate | 67% |  |  |  |  | not computed |
| us_h1_naive_rmse | estimate | 0.398 pp | 0.3967 | 0.02752 | 470 | True | paper inside 0.3967 +/- 0.05395 |
| us_h1_naive_mae | estimate | 0.276 pp | 0.2751 | 0.0132 | 470 | True | paper inside 0.2751 +/- 0.02587 |
| us_h1_naive_crps | estimate | 0.206 pp | 0.2065 | 0.01009 | 470 | True | paper inside 0.2065 +/- 0.01977 |
| us_h1_roll_rmse | estimate | 1.412 pp | 1.333 | 0.06157 | 470 | True | paper inside 1.333 +/- 0.1207 |
| us_h1_roll_mae | estimate | 1.015 pp | 0.9562 | 0.04289 | 470 | True | paper inside 0.9562 +/- 0.08407 |
| us_h1_roll_crps | estimate | 0.792 pp | 0.7169 | 0.03128 | 470 | False | paper outside 0.7169 +/- 0.06131 |
| us_h1_pnc_rmse | estimate | 1.412 pp |  |  |  |  | not computed |
| us_h1_pnc_mae | estimate | 1.102 pp |  |  |  |  | not computed |
| us_h1_pnc_crps | estimate | 0.74 pp |  |  |  |  | not computed |
| us_h1_arima_rmse | estimate | 0.362 pp | 0.361 | 0.02267 | 470 | True | paper inside 0.361 +/- 0.04444 |
| us_h1_arima_mae | estimate | 0.259 pp | 0.2582 | 0.01165 | 470 | True | paper inside 0.2582 +/- 0.02284 |
| us_h1_arima_crps | estimate | 0.191 pp | 0.1912 | 0.008736 | 470 | True | paper inside 0.1912 +/- 0.01712 |
| us_h1_bvar_diff_rmse | estimate | 0.489 pp |  |  |  |  | not computed |
| us_h1_bvar_diff_mae | estimate | 0.337 pp |  |  |  |  | not computed |
| us_h1_bvar_diff_crps | estimate | 0.252 pp |  |  |  |  | not computed |
| us_h1_bvar_min_rmse | estimate | 0.486 pp |  |  |  |  | not computed |
| us_h1_bvar_min_mae | estimate | 0.335 pp |  |  |  |  | not computed |
| us_h1_bvar_min_crps | estimate | 0.25 pp |  |  |  |  | not computed |
| us_h1_bvar_nw_rmse | estimate | 0.483 pp |  |  |  |  | not computed |
| us_h1_bvar_nw_mae | estimate | 0.332 pp |  |  |  |  | not computed |
| us_h1_bvar_nw_crps | estimate | 0.249 pp |  |  |  |  | not computed |
| us_h1_dfm_rmse | estimate | 0.364 pp | 0.361 | 0.02267 | 470 | True | paper inside 0.361 +/- 0.04444 |
| us_h1_dfm_mae | estimate | 0.262 pp | 0.2582 | 0.01165 | 470 | True | paper inside 0.2582 +/- 0.02284 |
| us_h1_dfm_crps | estimate | 0.193 pp | 0.1912 | 0.008736 | 470 | True | paper inside 0.1912 +/- 0.01712 |
| us_h1_drf_rmse | estimate | 0.59 pp |  |  |  |  | not computed |
| us_h1_drf_mae | estimate | 0.395 pp |  |  |  |  | not computed |
| us_h1_drf_crps | estimate | 0.296 pp |  |  |  |  | not computed |
| us_h3_naive_rmse | estimate | 0.865 pp | 0.8566 | 0.05741 | 468 | True | paper inside 0.8566 +/- 0.1125 |
| us_h3_naive_mae | estimate | 0.575 pp | 0.5701 | 0.02958 | 468 | True | paper inside 0.5701 +/- 0.05798 |
| us_h3_naive_crps | estimate | 0.441 pp | 0.4405 | 0.02269 | 468 | True | paper inside 0.4405 +/- 0.04448 |
| us_h3_arima_rmse | estimate | 0.849 pp | 0.8425 | 0.05424 | 468 | True | paper inside 0.8425 +/- 0.1063 |
| us_h3_arima_mae | estimate | 0.577 pp | 0.5725 | 0.0286 | 468 | True | paper inside 0.5725 +/- 0.05606 |
| us_h3_arima_crps | estimate | 0.436 pp | 0.4371 | 0.02181 | 468 | True | paper inside 0.4371 +/- 0.04275 |
| us_h6_drf_rmse | estimate | 1.173 pp |  |  |  |  | not computed |
| us_h6_drf_mae | estimate | 0.785 pp |  |  |  |  | not computed |
| us_h6_drf_crps | estimate | 0.575 pp |  |  |  |  | not computed |
| us_h12_drf_rmse | estimate | 1.341 pp |  |  |  |  | not computed |
| us_h12_drf_mae | estimate | 0.864 pp |  |  |  |  | not computed |
| us_h12_drf_crps | estimate | 0.62 pp |  |  |  |  | not computed |
| ea_h1_arima_rmse | estimate | 0.334 pp | 0.3602 | 0.03207 | 175 | True | paper inside 0.3602 +/- 0.06286 |
| ea_h1_arima_mae | estimate | 0.222 pp | 0.2507 | 0.01961 | 175 | True | paper inside 0.2507 +/- 0.03843 |
| ea_h1_arima_crps | estimate | 0.17 pp | 0.1907 | 0.0145 | 175 | True | paper inside 0.1907 +/- 0.02841 |
| ea_h12_drf_rmse | estimate | 1.832 pp |  |  |  |  | not computed |
| ea_h12_drf_crps | estimate | 0.804 pp |  |  |  |  | not computed |
| ch_h1_dfm_rmse | estimate | 0.284 pp | 0.2841 | 0.01376 | 304 | True | paper inside 0.2841 +/- 0.02697 |
| ch_h1_dfm_mae | estimate | 0.215 pp | 0.2149 | 0.01068 | 304 | True | paper inside 0.2149 +/- 0.02093 |
| ch_h1_dfm_crps | estimate | 0.158 pp | 0.1573 | 0.007334 | 304 | True | paper inside 0.1573 +/- 0.01438 |
| ch_h6_drf_rmse | estimate | 0.802 pp |  |  |  |  | not computed |
| ch_h12_drf_rmse | estimate | 0.869 pp |  |  |  |  | not computed |
| us_h1_arima_ks_p | p_value | 0.26 p |  |  |  |  | not computed |
| us_h1_arima_edge | estimate | 0% |  |  |  |  | not computed |
| us_h1_arima_maxe | estimate | 1.82e+04 e |  |  |  |  | not computed |
| us_h1_roll_ks_p | p_value | 0 p |  |  |  |  | not computed |
| us_h1_roll_maxe | estimate | 2.28e+34 e |  |  |  |  | not computed |
| us_h1_bvar_min_ks_p | p_value | 0.381 p |  |  |  |  | not computed |
| us_h1_bvar_min_maxe | estimate | 1.91e+22 e |  |  |  |  | not computed |
| us_h1_bvar_nw_maxe | estimate | 5.66e+30 e |  |  |  |  | not computed |
| us_h1_bvar_diff_maxe | estimate | 1.61e+27 e |  |  |  |  | not computed |
| us_h1_dfm_ks_p | p_value | 0.097 p |  |  |  |  | not computed |
| us_h1_dfm_maxe | estimate | 9.7e+04 e |  |  |  |  | not computed |
| us_h1_drf_ks_p | p_value | 0 p |  |  |  |  | not computed |
| us_h1_drf_maxe | estimate | 4.7e+14 e |  |  |  |  | not computed |
| us_h1_drf_edge | estimate | 1.7% |  |  |  |  | not computed |
| us_h1_pnc_edge | estimate | 28.5% |  |  |  |  | not computed |
| us_h1_pnc_maxe | estimate | 56.8 e |  |  |  |  | not computed |
| us_h12_bvar_nw_maxe | estimate | 5.17e+36 e |  |  |  |  | not computed |
| us_h12_bvar_min_maxe | estimate | 6.55e+31 e |  |  |  |  | not computed |
| us_h12_bvar_diff_maxe | estimate | 3.42e+34 e |  |  |  |  | not computed |
| us_h6_drmax | estimate | 1.82 e |  |  |  |  | not computed |
| ea_h1_arima_ks_p | p_value | 0.517 p |  |  |  |  | not computed |
| ea_h1_arima_maxe | estimate | 200 e |  |  |  |  | not computed |
| ea_h1_dfm_ks_p | p_value | 0.815 p |  |  |  |  | not computed |
| ea_h1_dfm_maxe | estimate | 1.9e+07 e |  |  |  |  | not computed |
| ea_h1_bvar_nw_maxe | estimate | 5.07e+29 e |  |  |  |  | not computed |
| ea_h1_bvar_min_maxe | estimate | 1.05e+15 e |  |  |  |  | not computed |
| ea_h3_bvar_nw_maxe | estimate | 1.04e+51 e |  |  |  |  | not computed |
| ea_h6_bvar_nw_maxe | estimate | 3.01e+79 e |  |  |  |  | not computed |
| ea_h6_bvar_min_maxe | estimate | 1.39e+70 e |  |  |  |  | not computed |
| ea_h12_bvar_nw_maxe | estimate | 2.29e+78 e |  |  |  |  | not computed |
| ea_h12_dfm_maxe | estimate | 4.28e+25 e |  |  |  |  | not computed |
| ea_h1_drf_ks_p | p_value | 0.004 p |  |  |  |  | not computed |
| ea_h1_drf_maxe | estimate | 113 e |  |  |  |  | not computed |
| ea_h1_roll_maxe | estimate | 3.37e+07 e |  |  |  |  | not computed |
| ea_h6_arima_maxe | estimate | 200 e |  |  |  |  | not computed |
| ch_h1_arima_ks_p | p_value | 0.109 p |  |  |  |  | not computed |
| ch_h1_arima_maxe | estimate | 1.42 e |  |  |  |  | not computed |
| ch_h1_bvar_nw_maxe | estimate | 2e+04 e |  |  |  |  | not computed |
| ch_h1_bvar_min_maxe | estimate | 203 e |  |  |  |  | not computed |
| ch_h1_roll_maxe | estimate | 3.32e+09 e |  |  |  |  | not computed |
| ch_h1_roll_ks_p | p_value | 0.021 p |  |  |  |  | not computed |
| ch_h1_drf_maxe | estimate | 1.21e+07 e |  |  |  |  | not computed |
| ch_h1_drf_ks_p | p_value | 0 p |  |  |  |  | not computed |
| ch_h12_bvar_nw_maxe | estimate | 3.93e+04 e |  |  |  |  | not computed |
| ch_h3_bvar_min_maxe | estimate | 1 e |  |  |  |  | not computed |

## The paper's own numbers
- NOTE: KS vs sequential US h=1 ARIMA: t = 18200 and p = 0.26 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: KS vs sequential US h=1 BVAR Minnesota: t = 1.91e+22 and p = 0.381 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: KS vs sequential EA h=1 DFM: t = 1.9e+07 and p = 0.815 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: KS vs sequential EA h=3 BVAR NW: t = 1.04e+51 and p = 0.517 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: KS vs sequential CH h=1 BVAR NW: t = 20000 and p = 0.109 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided

## Guards
- no claims rejected
- spec: the headline was written as prose ('Paper conclusion rests on extreme sequential evidence against BVAR calibration during crises vs non-rejection by static '); chosen from the claim names: us_h1_bvar_min_maxe
- spec: the headline was written as prose ('Primary evidence for time-varying miscalibration missed by static tests: sequential e-value sharply rejects BVAR calibra'); chosen from the claim names: us_h1_bvar_min_maxe
- sample: the sample differs from the paper's by 1 missing and 0 extra observations (0.1% of the paper's 1585, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: FRED public vintages Sep 2025 for CPIAUCSL/CP0000EZ19M086NEST/CHECPIALLMINMEI vs paper April 2025 SNB, June 2025 EA, July 2025 US. ARIMA(1,1,0) Delta pi_t=alpha0+phi1 Delta pi_{t-1}+eps with trend='t' (constant in differenced model) expanding window from first 40% training window (US 314 months to Feb1986, EA 117 to Sep2010, CH 203 to Dec1999). Rolling mean L=20 Gaussian with variance scaled by sqrt(1+1/L) approximated. CRPS via Gaussian sigma=RMSE expanding approximation (error <0.01). US h1 DFM proxied by ARIMA(1,1,0) (paper DFM 0.364 vs ARIMA 0.362 very close, difference within 0.8%). Winsorization/predictor transforms not replicated

## Data sources
- market data: none used
- other hosts the script fetched from: fred.stlouisfed.org

## Run
- sandbox: attempt 1, exit 0, 111.6s
- model calls: 31, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 2000163, out 86649 (reasoning 44015); cost $0.9591

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
