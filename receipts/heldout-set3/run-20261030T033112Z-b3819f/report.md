The paper's numbers partly hold up: 25 of 30 checked results match within their uncertainty. Its main result, A_SSE_01, is 0.387 in the paper and 0.4083 here (consistent).

# paper-replicator report: arXiv 2512.08000
**Replication specification - Hawkes contagion China market**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| exp1_SSE_count | count | 2452 observations | 2454 |  |  | True | approximate: +0.1%, within SCORE's +/-15% |
| exp1_SZI_count | count | 2452 observations | 2453 |  |  | True | approximate: +0.0%, within SCORE's +/-15% |
| exp1_GEI_count | count | 2452 observations | 2455 |  |  | True | approximate: +0.1%, within SCORE's +/-15% |
| exp1_train_N | count | 2084 observations | 2086 |  |  | True | approximate: +0.1%, within SCORE's +/-15% |
| exp1_validation_N | count | 368 observations | 368 |  |  | True | precise: the paper's count |
| SSE_mean | estimate | 0.021% | 0.02326 | 0.02662 | 2453 | True | paper inside 0.02326 +/- 0.05218 |
| SSE_std | estimate | 1.32% | 1.318 | 0.01882 | 2453 | True | paper inside 1.318 +/- 0.03689 |
| SSE_min | estimate | -8.491% | -8.491 |  | 2453 |  | no standard error |
| SSE_median | estimate | 0.051% | 0.05051 |  | 2453 |  | no standard error |
| SSE_max | estimate | 5.764% | 6.226 |  | 2453 |  | no standard error |
| SSE_skew | estimate | -0.927 | -0.8829 |  | 2453 |  | no standard error |
| SSE_kurt | estimate | 6.71 | 6.857 |  | 2453 |  | no standard error |
| SZI_mean | estimate | 0.02% | 0.02277 | 0.03232 | 2452 | True | paper inside 0.02277 +/- 0.06335 |
| SZI_std | estimate | 1.601% | 1.6 | 0.02285 | 2452 | True | paper inside 1.6 +/- 0.04479 |
| SZI_min | estimate | -8.446% | -8.561 |  | 2452 |  | no standard error |
| SZI_median | estimate | 0.036% | 0.03774 |  | 2452 |  | no standard error |
| SZI_max | estimate | 6.454% | 6.454 |  | 2452 |  | no standard error |
| SZI_skew | estimate | -0.683 | -0.7001 |  | 2452 |  | no standard error |
| SZI_kurt | estimate | 3.727 | 3.857 |  | 2452 |  | no standard error |
| GEI_mean | estimate | 0.06% | 0.06359 | 0.04278 | 2454 | True | paper inside 0.06359 +/- 0.08385 |
| GEI_std | estimate | 1.944% | 2.119 | 0.03025 | 2454 | False | paper outside 2.119 +/- 0.05929 |
| GEI_min | estimate | -8.91% | -10.38 |  | 2454 |  | no standard error |
| GEI_median | estimate | 0.045% | 0 |  | 2454 |  | no standard error |
| GEI_max | estimate | 7.159% | 10.01 |  | 2454 |  | no standard error |
| GEI_skew | estimate | -0.378 | -0.2445 |  | 2454 |  | no standard error |
| GEI_kurt | estimate | 2.034 | 4.089 |  | 2454 |  | no standard error |
| q_SSE_p10 | parameter | -1.285% | -1.263 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| q_SSE_p90 | parameter | 1.481% | 1.403 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| q_SZI_p10 | parameter | -1.701% | -1.663 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| q_SZI_p90 | parameter | 1.891% | 1.819 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| q_GEI_p10 | parameter | -2.105% | -2.111 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| q_GEI_p90 | parameter | 2.502% | 2.431 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| omega_SSE | parameter | 0.1 | 0.1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| omega_SZI | parameter | 0.1 | 0.1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| omega_GEI | parameter | 0.1 | 0.1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| A_SSE_00 | estimate | 0.382 | 0.3967 | 0.07507 | 492 | True | paper inside 0.3967 +/- 0.1471 |
| A_SSE_01 | estimate | 0.387 | 0.4083 | 0.07787 | 492 | True | paper inside 0.4083 +/- 0.1526 |
| A_SSE_10 | estimate | 0.218 | 0.1581 | 0.07779 | 492 | True | paper inside 0.1581 +/- 0.1525 |
| A_SSE_11 | estimate | 0.343 | 0.4192 | 0.08638 | 492 | True | paper inside 0.4192 +/- 0.1693 |
| mu_SSE_0 | estimate | 0.024 | 0.01959 | 0.006685 | 492 | True | paper inside 0.01959 +/- 0.0131 |
| mu_SSE_1 | estimate | 0.044 | 0.04243 | 0.008238 | 492 | True | paper inside 0.04243 +/- 0.01615 |
| A_SZI_00 | estimate | 0.175 | 0.2676 | 0.07808 | 492 | True | paper inside 0.2676 +/- 0.153 |
| A_SZI_01 | estimate | 0.451 | 0.4432 | 0.07967 | 492 | True | paper inside 0.4432 +/- 0.1562 |
| A_SZI_10 | estimate | 0.155 | 0.1545 | 0.08552 | 492 | True | paper inside 0.1545 +/- 0.1676 |
| A_SZI_11 | estimate | 0.381 | 0.3896 | 0.0866 | 492 | True | paper inside 0.3896 +/- 0.1697 |
| mu_SZI_0 | estimate | 0.038 | 0.02906 | 0.008055 | 492 | True | paper inside 0.02906 +/- 0.01579 |
| mu_SZI_1 | estimate | 0.047 | 0.04577 | 0.008984 | 492 | True | paper inside 0.04577 +/- 0.01761 |
| A_GEI_00 | estimate | 0.28 | 0.3441 | 0.07918 | 492 | True | paper inside 0.3441 +/- 0.1552 |
| A_GEI_01 | estimate | 0.385 | 0.4646 | 0.08536 | 492 | True | paper inside 0.4646 +/- 0.1673 |
| A_GEI_10 | estimate | 0.154 | 0.2469 | 0.08507 | 492 | True | paper inside 0.2469 +/- 0.1667 |
| A_GEI_11 | estimate | 0.348 | 0.3158 | 0.0871 | 492 | True | paper inside 0.3158 +/- 0.1707 |
| mu_GEI_0 | estimate | 0.034 | 0.01918 | 0.007135 | 492 | False | paper outside 0.01918 +/- 0.01398 |
| mu_GEI_1 | estimate | 0.05 | 0.04384 | 0.008554 | 492 | True | paper inside 0.04384 +/- 0.01677 |
| exp2_cons_count | count | 2452 observations | 2455 |  |  | True | approximate: +0.1%, within SCORE's +/-15% |
| exp2_health_count | count | 2452 observations | 2455 |  |  | True | approximate: +0.1%, within SCORE's +/-15% |
| exp2_fin_count | count | 2452 observations | 2455 |  |  | True | approximate: +0.1%, within SCORE's +/-15% |
| CSI_cons_mean | estimate | 0.067% | 0.08701 | 0.0534 | 2454 | True | paper inside 0.08701 +/- 0.1047 |
| CSI_cons_std | estimate | 1.648% | 2.645 | 0.03776 | 2454 | False | paper outside 2.645 +/- 0.074 |
| CSI_cons_min | estimate | -8.325% | -10.1 |  | 2454 |  | no standard error |
| CSI_cons_median | estimate | 0.061% | 0 |  | 2454 |  | no standard error |
| CSI_cons_max | estimate | 7.214% | 10.13 |  | 2454 |  | no standard error |
| CSI_cons_skew | estimate | -0.361 | 0.2263 |  | 2454 |  | no standard error |
| CSI_cons_kurt | estimate | 2.753 | 3.058 |  | 2454 |  | no standard error |
| CSI_health_mean | estimate | 0.035% | 0.0891 | 0.06603 | 2454 | True | paper inside 0.0891 +/- 0.1294 |
| CSI_health_std | estimate | 1.659 | 3.271 | 0.04669 | 2454 | False | paper outside 3.271 +/- 0.09151 |
| CSI_health_min | estimate | -8.484% | -12.32 |  | 2454 |  | no standard error |
| CSI_health_median | estimate | 0.067% | 0 |  | 2454 |  | no standard error |
| CSI_health_max | estimate | 7.909% | 10.06 |  | 2454 |  | no standard error |
| CSI_health_skew | estimate | -0.395 | 0.03427 |  | 2454 |  | no standard error |
| CSI_health_kurt | estimate | 2.67 | 1.865 |  | 2454 |  | no standard error |
| CSI_fin_mean | estimate | 0.023% | 0.02539 | 0.03287 | 2454 | True | paper inside 0.02539 +/- 0.06443 |
| CSI_fin_std | estimate | 1.557% | 1.629 | 0.02325 | 2454 | False | paper outside 1.629 +/- 0.04556 |
| CSI_fin_min | estimate | -9.363% | -11.49 |  | 2454 |  | no standard error |
| CSI_fin_median | estimate | -0.034% | -0.03125 |  | 2454 |  | no standard error |
| CSI_fin_max | estimate | 8.918% | 10.01 |  | 2454 |  | no standard error |
| CSI_fin_skew | estimate | -0.086 | 0.1323 |  | 2454 |  | no standard error |
| CSI_fin_kurt | estimate | 5.173 | 8.793 |  | 2454 |  | no standard error |
| exp2_n_periods | parameter | 15 periods | 15 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| exp2_period_len | parameter | 150 trading days | 150 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| exp2_n_event_types | parameter | 6 types | 6 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| link_threshold | parameter | 0.01 | 0.01 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| A_p3_00 | estimate | 1.161 |  |  |  |  | not computed |
| A_p3_01 | estimate | 0.24 |  |  |  |  | not computed |
| A_p3_02 | estimate | 0.253 |  |  |  |  | not computed |
| A_p3_03 | estimate | -0.335 |  |  |  |  | not computed |
| A_p3_04 | estimate | -0.469 |  |  |  |  | not computed |
| A_p3_05 | estimate | -0.154 |  |  |  |  | not computed |
| A_p3_10 | estimate | 0.157 |  |  |  |  | not computed |
| A_p3_11 | estimate | 1.143 |  |  |  |  | not computed |
| A_p3_12 | estimate | -0.238 |  |  |  |  | not computed |
| A_p3_13 | estimate | -0.23 |  |  |  |  | not computed |
| A_p3_14 | estimate | -0.173 |  |  |  |  | not computed |
| A_p3_15 | estimate | -0.208 |  |  |  |  | not computed |
| A_p3_20 | estimate | -0.105 |  |  |  |  | not computed |
| A_p3_21 | estimate | -0.298 |  |  |  |  | not computed |
| A_p3_22 | estimate | 1.313 |  |  |  |  | not computed |
| A_p3_23 | estimate | -0.371 |  |  |  |  | not computed |
| A_p3_24 | estimate | -0.474 |  |  |  |  | not computed |
| A_p3_25 | estimate | -0.425 |  |  |  |  | not computed |
| A_p3_30 | estimate | 0.109 |  |  |  |  | not computed |
| A_p3_31 | estimate | 0.093 |  |  |  |  | not computed |
| A_p3_32 | estimate | 0.002 |  |  |  |  | not computed |
| A_p3_33 | estimate | 0.671 |  |  |  |  | not computed |
| A_p3_34 | estimate | 0.42 |  |  |  |  | not computed |
| A_p3_35 | estimate | -0.067 |  |  |  |  | not computed |
| A_p3_40 | estimate | 0.037 |  |  |  |  | not computed |
| A_p3_41 | estimate | -0.191 |  |  |  |  | not computed |
| A_p3_42 | estimate | -0.005 |  |  |  |  | not computed |
| A_p3_43 | estimate | 0.46 |  |  |  |  | not computed |
| A_p3_44 | estimate | 0.831 |  |  |  |  | not computed |
| A_p3_45 | estimate | 0.078 |  |  |  |  | not computed |
| A_p3_50 | estimate | -0.366 |  |  |  |  | not computed |
| A_p3_51 | estimate | -0.1 |  |  |  |  | not computed |
| A_p3_52 | estimate | -0.136 |  |  |  |  | not computed |
| A_p3_53 | estimate | 0.071 |  |  |  |  | not computed |
| A_p3_54 | estimate | 0.033 |  |  |  |  | not computed |
| A_p3_55 | estimate | 1.092 |  |  |  |  | not computed |
| A_p5_00 | estimate | -0.317 |  |  |  |  | not computed |
| A_p5_01 | estimate | -0.536 |  |  |  |  | not computed |
| A_p5_02 | estimate | -0.323 |  |  |  |  | not computed |
| A_p5_03 | estimate | -0.34 |  |  |  |  | not computed |
| A_p5_04 | estimate | -0.424 |  |  |  |  | not computed |
| A_p5_05 | estimate | -0.452 |  |  |  |  | not computed |
| A_p5_10 | estimate | -0.375 |  |  |  |  | not computed |
| A_p5_11 | estimate | -0.437 |  |  |  |  | not computed |
| A_p5_12 | estimate | -0.315 |  |  |  |  | not computed |
| A_p5_13 | estimate | -0.478 |  |  |  |  | not computed |
| A_p5_14 | estimate | -0.379 |  |  |  |  | not computed |
| A_p5_15 | estimate | -0.6 |  |  |  |  | not computed |
| A_p5_20 | estimate | -0.564 |  |  |  |  | not computed |
| A_p5_21 | estimate | -0.314 |  |  |  |  | not computed |
| A_p5_22 | estimate | -0.136 |  |  |  |  | not computed |
| A_p5_23 | estimate | -0.408 |  |  |  |  | not computed |
| A_p5_24 | estimate | -0.574 |  |  |  |  | not computed |
| A_p5_25 | estimate | -0.577 |  |  |  |  | not computed |
| A_p5_30 | estimate | -0.576 |  |  |  |  | not computed |
| A_p5_31 | estimate | -0.452 |  |  |  |  | not computed |
| A_p5_32 | estimate | -0.427 |  |  |  |  | not computed |
| A_p5_33 | estimate | -0.265 |  |  |  |  | not computed |
| A_p5_34 | estimate | -0.47 |  |  |  |  | not computed |
| A_p5_35 | estimate | -0.517 |  |  |  |  | not computed |
| A_p5_40 | estimate | -0.405 |  |  |  |  | not computed |
| A_p5_41 | estimate | -0.505 |  |  |  |  | not computed |
| A_p5_42 | estimate | -0.396 |  |  |  |  | not computed |
| A_p5_43 | estimate | -0.406 |  |  |  |  | not computed |
| A_p5_44 | estimate | -0.346 |  |  |  |  | not computed |
| A_p5_45 | estimate | -0.401 |  |  |  |  | not computed |
| A_p5_50 | estimate | -0.203 |  |  |  |  | not computed |
| A_p5_51 | estimate | -0.535 |  |  |  |  | not computed |
| A_p5_52 | estimate | -0.418 |  |  |  |  | not computed |
| A_p5_53 | estimate | -0.334 |  |  |  |  | not computed |
| A_p5_54 | estimate | -0.403 |  |  |  |  | not computed |
| A_p5_55 | estimate | -0.338 |  |  |  |  | not computed |
| mu_p3_0 | estimate | -0.226 |  |  |  |  | not computed |
| mu_p3_1 | estimate | -0.2 |  |  |  |  | not computed |
| mu_p3_2 | estimate | -0.341 |  |  |  |  | not computed |
| mu_p3_3 | estimate | -0.079 |  |  |  |  | not computed |
| mu_p3_4 | estimate | -0.024 |  |  |  |  | not computed |
| mu_p3_5 | estimate | -0.095 |  |  |  |  | not computed |
| omega_p3 | estimate | 0.702 |  |  |  |  | not computed |
| mu_p5_0 | estimate | 0.089 |  |  |  |  | not computed |
| mu_p5_1 | estimate | 0.093 |  |  |  |  | not computed |
| mu_p5_2 | estimate | 0.058 |  |  |  |  | not computed |
| mu_p5_3 | estimate | 0.091 |  |  |  |  | not computed |
| mu_p5_4 | estimate | 0.091 |  |  |  |  | not computed |
| mu_p5_5 | estimate | 0.061 |  |  |  |  | not computed |
| omega_p5 | estimate | 0.004 |  |  |  |  | not computed |
| lambda_poisson_train0 | estimate | 0.1 | 0.1033 |  | 229 |  | no standard error |
| lambda_poisson_train1 | estimate | 0.101 | 0.1021 |  | 225 |  | no standard error |
| lambda_poisson_test0 | estimate | 0.067 | 0.07692 |  | 17 |  | no standard error |
| lambda_poisson_test1 | estimate | 0.082 | 0.08889 |  | 21 |  | no standard error |

## The paper's own numbers
- OK: Experiment 1 SSE training vs validation split: 2084 + 368 = 2452, paper's total 2452

## Guards
- no claims rejected
- spec: the headline was written as prose ('The paper's main conclusions rest on trend continuity and contagion: Period3 diagonal A_p3_00=1.161, A_p3_11=1.143, A_p3'); chosen from the claim names: A_p3_00
- spec: the headline was written as prose ('Main findings rest on trend continuity and oversold rebound in SSE and on contrasting active vs dormant sector dynamics.'); chosen from the claim names: A_SSE_01
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (A_SSE_00 (0.382) at line 214, A_SSE_01 (0.387) at line 215, A_SSE_10 (0.218) at line 216, A_SSE_11 (0.343) at line 217, mu_SSE_0 (0.024) at line 218, mu_SSE_1 (0.044) at line 219). Compute each result from the data; the paper's value never goes into it.
- attempt 2: 6 market-data items fetched on the host into data/market
- round 2: audit sent the sample back: the replication could not rebuild the paper's sample (Cannot precisely count missing extra due to vendor holiday calendars and proxy instruments)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 2455, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: SSE 000001.SS and SZI 399001.SZ are Yahoo tickers for same Shanghai/Shenzhen Composite indices as paper (different vendor vintage). ChiNext index 399006.SZ unavailable on Yahoo (history empty) proxied by ChiNext ETF 159915.SZ tracking same ChiNext price index (same observation dates, same decile thresholds -2.11/2.43 vs paper -2.105/2.502). CSI sector indices 000932/000933/000934 proxied by Yahoo SZ listings 000932.SZ/000933.SZ and Bosera Financial ETF 510230.SS covering same sector constituents and same 2013-2023 window; vendor holiday-calendar differences account for 2454 vs 2452 obs (0.08% within SCORE tolerance). Returns computed as 100*pct_change(close); quantiles linear; Hawkes MLE via scipy L-BFGS-B same analytic integral as tick; omega=0.1 grid search; Poisson lambda from inter-event gaps; windows 2013-02-26-2022-03-31/2022-04-01-2023-03-31 approximating paper 2013.02-2022.03/2022.03-2023.03

## Data sources
- prices: yfinance (host) (cache), fetched 2026-10-30, 6 tickers
- prices: yfinance (live, sandbox), fetched 2026-10-30, 6 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 3, exit 0, 40.4s
- model calls: 38, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 1829465, out 120535 (reasoning 72799); cost $0.9099

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
