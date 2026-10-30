The paper's numbers partly hold up: 6 of 6 checked results match within their uncertainty. Its main result, period3_A00, is 1.161 . in the paper and -0.1045 . here (not judged: no standard error).

# paper-replicator report: arXiv 2512.08000
**Replication Spec - Analysis of Contagion in China's Stock Market: A Hawkes Process Perspective**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| shanghai_count | count | 2452 observations | 2456 |  |  | True | approximate: +0.2%, within SCORE's +/-15% |
| shanghai_mean | estimate | 0.021% | 0.02319 | 0.02653 | 2456 | True | paper inside 0.02319 +/- 0.05199 |
| shanghai_std | estimate | 1.32% | 1.315 |  | 2456 |  | no standard error |
| shanghai_min | estimate | -8.491% | -8.491 |  | 2456 |  | no standard error |
| shanghai_median | estimate | 0.051% | 0.05077 |  | 2456 |  | no standard error |
| shanghai_max | estimate | 5.764% | 5.764 |  | 2456 |  | no standard error |
| shanghai_skew | estimate | -0.927 . | -0.9185 |  | 2456 |  | no standard error |
| shanghai_kurtosis | estimate | 6.71 . | 6.766 |  | 2456 |  | no standard error |
| shenzhen_count | count | 2452 observations | 2456 |  |  | True | approximate: +0.2%, within SCORE's +/-15% |
| shenzhen_mean | estimate | 0.02% | 0.0227 | 0.03224 | 2456 | True | paper inside 0.0227 +/- 0.06318 |
| shenzhen_std | estimate | 1.601% | 1.598 |  | 2456 |  | no standard error |
| shenzhen_min | estimate | -8.446% | -8.446 |  | 2456 |  | no standard error |
| shenzhen_median | estimate | 0.036% | 0.03775 |  | 2456 |  | no standard error |
| shenzhen_max | estimate | 6.454% | 6.454 |  | 2456 |  | no standard error |
| shenzhen_skew | estimate | -0.683 . | -0.6832 |  | 2456 |  | no standard error |
| shenzhen_kurtosis | estimate | 3.727 . | 3.763 |  | 2456 |  | no standard error |
| chinext_count | count | 2452 observations | 2456 |  |  | True | approximate: +0.2%, within SCORE's +/-15% |
| chinext_mean | estimate | 0.06% | 0.06117 | 0.0392 | 2456 | True | paper inside 0.06117 +/- 0.07684 |
| chinext_std | estimate | 1.944% | 1.943 |  | 2456 |  | no standard error |
| chinext_min | estimate | -8.91% | -8.91 |  | 2456 |  | no standard error |
| chinext_median | estimate | 0.045% | 0.05539 |  | 2456 |  | no standard error |
| chinext_max | estimate | 7.159% | 7.159 |  | 2456 |  | no standard error |
| chinext_skew | estimate | -0.378 . | -0.3805 |  | 2456 |  | no standard error |
| chinext_kurtosis | estimate | 2.034 . | 2.042 |  | 2456 |  | no standard error |
| train_size | count | 2084 observations | 2087 |  |  | True | approximate: +0.1%, within SCORE's +/-15% |
| val_size | count | 368 observations | 369 |  |  | True | approximate: +0.3%, within SCORE's +/-15% |
| shanghai_quant10 | parameter | -1.285% | -1.257 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| shanghai_quant90 | parameter | 1.481% | 1.401 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| shenzhen_quant10 | parameter | -1.701% | -1.662 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| shenzhen_quant90 | parameter | 1.891% | 1.818 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| chinext_quant10 | parameter | -2.105% | -2.092 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| chinext_quant90 | parameter | 2.502% | 2.384 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| omega_shanghai | parameter | 0.1 . | 0.05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| omega_shenzhen | parameter | 0.1 . | 0.05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| omega_chinext | parameter | 0.1 . | 0.05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| shanghai_mu0 | estimate | 0.024 . | 0.0107 |  | 492 |  | no standard error |
| shanghai_mu1 | estimate | 0.044 . | 0.03176 |  | 492 |  | no standard error |
| shanghai_A00 | estimate | 0.382 . | 0.474 |  | 492 |  | no standard error |
| shanghai_A01 | estimate | 0.387 . | 0.4206 |  | 492 |  | no standard error |
| shanghai_A10 | estimate | 0.218 . | 0.249 |  | 492 |  | no standard error |
| shanghai_A11 | estimate | 0.343 . | 0.435 |  | 492 |  | no standard error |
| shenzhen_mu0 | estimate | 0.038 . | 0.0175 |  | 492 |  | no standard error |
| shenzhen_mu1 | estimate | 0.047 . | 0.03223 |  | 492 |  | no standard error |
| shenzhen_A00 | estimate | 0.175 . | 0.3808 |  | 492 |  | no standard error |
| shenzhen_A01 | estimate | 0.451 . | 0.4457 |  | 492 |  | no standard error |
| shenzhen_A10 | estimate | 0.155 . | 0.24 |  | 492 |  | no standard error |
| shenzhen_A11 | estimate | 0.381 . | 0.4393 |  | 492 |  | no standard error |
| chinext_mu0 | estimate | 0.034 . | 0.01142 |  | 492 |  | no standard error |
| chinext_mu1 | estimate | 0.05 . | 0.03158 |  | 492 |  | no standard error |
| chinext_A00 | estimate | 0.28 . | 0.4321 |  | 492 |  | no standard error |
| chinext_A01 | estimate | 0.385 . | 0.4544 |  | 492 |  | no standard error |
| chinext_A10 | estimate | 0.154 . | 0.3203 |  | 492 |  | no standard error |
| chinext_A11 | estimate | 0.348 . | 0.3649 |  | 492 |  | no standard error |
| csi_consumer_count | count | 2452 observations | 2456 |  |  | True | approximate: +0.2%, within SCORE's +/-15% |
| csi_consumer_mean | estimate | 0.067% | 0.06905 | 0.03321 | 2456 | True | paper inside 0.06905 +/- 0.06509 |
| csi_consumer_std | estimate | 1.648% | 1.646 |  | 2456 |  | no standard error |
| csi_consumer_min | estimate | -8.325% | -8.325 |  | 2456 |  | no standard error |
| csi_consumer_median | estimate | 0.061% | 0.06297 |  | 2456 |  | no standard error |
| csi_consumer_max | estimate | 7.214% | 7.214 |  | 2456 |  | no standard error |
| csi_consumer_skew | estimate | -0.361 . | -0.3642 |  | 2456 |  | no standard error |
| csi_consumer_kurtosis | estimate | 2.753 . | 2.77 |  | 2456 |  | no standard error |
| csi_healthcare_count | count | 2452 observations | 2456 |  |  | True | approximate: +0.2%, within SCORE's +/-15% |
| csi_healthcare_mean | estimate | 0.035% | 0.03517 | 0.03345 | 2456 | True | paper inside 0.03517 +/- 0.06556 |
| csi_healthcare_std | estimate | 1.659% | 1.658 |  | 2456 |  | no standard error |
| csi_healthcare_min | estimate | -8.484% | -8.484 |  | 2456 |  | no standard error |
| csi_healthcare_median | estimate | 0.067% | 0.06682 |  | 2456 |  | no standard error |
| csi_healthcare_max | estimate | 7.909% | 7.909 |  | 2456 |  | no standard error |
| csi_healthcare_skew | estimate | -0.395 . | -0.3948 |  | 2456 |  | no standard error |
| csi_healthcare_kurtosis | estimate | 2.67 . | 2.675 |  | 2456 |  | no standard error |
| csi_finre_count | count | 2452 observations | 2456 |  |  | True | approximate: +0.2%, within SCORE's +/-15% |
| csi_finre_mean | estimate | 0.023% | 0.02167 | 0.03138 | 2456 | True | paper inside 0.02167 +/- 0.0615 |
| csi_finre_std | estimate | 1.557% | 1.555 |  | 2456 |  | no standard error |
| csi_finre_min | estimate | -9.363% | -9.363 |  | 2456 |  | no standard error |
| csi_finre_median | estimate | -0.034% | -0.03559 |  | 2456 |  | no standard error |
| csi_finre_max | estimate | 8.918% | 8.918 |  | 2456 |  | no standard error |
| csi_finre_skew | estimate | -0.086 . | -0.08458 |  | 2456 |  | no standard error |
| csi_finre_kurtosis | estimate | 5.173 . | 5.19 |  | 2456 |  | no standard error |
| num_periods | parameter | 15 periods | 15 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| trading_days_per_period | parameter | 150 days | 150 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| link_threshold | parameter | 0.01 . | 0.01 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| period3_mu0 | estimate | -0.226 . | 0.4212 |  | 172 |  | no standard error |
| period3_mu1 | estimate | -0.2 . | 0.3265 |  | 172 |  | no standard error |
| period3_mu2 | estimate | -0.341 . | 0.6293 |  | 172 |  | no standard error |
| period3_mu3 | estimate | -0.079 . | 0.113 |  | 172 |  | no standard error |
| period3_mu4 | estimate | -0.024 . | 0.192 |  | 172 |  | no standard error |
| period3_mu5 | estimate | -0.095 . | 0.5047 |  | 172 |  | no standard error |
| period3_omega | estimate | 0.702 . | 0.1538 |  | 172 |  | no standard error |
| period5_mu0 | estimate | 0.089 . | 0.1048 |  | 45 |  | no standard error |
| period5_mu1 | estimate | 0.093 . | 0.09628 |  | 45 |  | no standard error |
| period5_mu2 | estimate | 0.058 . | 0.06722 |  | 45 |  | no standard error |
| period5_mu3 | estimate | 0.091 . | 0.09945 |  | 45 |  | no standard error |
| period5_mu4 | estimate | 0.091 . | 0.09289 |  | 45 |  | no standard error |
| period5_mu5 | estimate | 0.061 . | 0.01006 |  | 45 |  | no standard error |
| period5_omega | estimate | 0.004 . | 0.2637 |  | 45 |  | no standard error |
| period3_A00 | estimate | 1.161 . | -0.1045 |  | 172 |  | no standard error |
| period3_A01 | estimate | 0.24 . | 0.4943 |  | 172 |  | no standard error |
| period3_A02 | estimate | 0.253 . | -1.269 |  | 172 |  | no standard error |
| period3_A03 | estimate | -0.335 . | 0.08626 |  | 172 |  | no standard error |
| period3_A04 | estimate | -0.469 . | 0.6328 |  | 172 |  | no standard error |
| period3_A05 | estimate | -0.154 . | -0.6635 |  | 172 |  | no standard error |
| period3_A10 | estimate | 0.157 . | 0.2354 |  | 172 |  | no standard error |
| period3_A11 | estimate | 1.143 . | 0.1708 |  | 172 |  | no standard error |
| period3_A12 | estimate | -0.238 . | -0.5491 |  | 172 |  | no standard error |
| period3_A13 | estimate | -0.23 . | 0.7522 |  | 172 |  | no standard error |
| period3_A14 | estimate | -0.173 . | -0.1388 |  | 172 |  | no standard error |
| period3_A15 | estimate | -0.208 . | -0.7032 |  | 172 |  | no standard error |
| period3_A20 | estimate | -0.105 . | 0.006649 |  | 172 |  | no standard error |
| period3_A21 | estimate | -0.298 . | 0.1917 |  | 172 |  | no standard error |
| period3_A22 | estimate | 1.313 . | -1.616 |  | 172 |  | no standard error |
| period3_A23 | estimate | -0.371 . | -2.37 |  | 172 |  | no standard error |
| period3_A24 | estimate | -0.474 . | 2.906 |  | 172 |  | no standard error |
| period3_A25 | estimate | -0.425 . | -1.05 |  | 172 |  | no standard error |
| period3_A30 | estimate | 0.109 . | -0.5635 |  | 172 |  | no standard error |
| period3_A31 | estimate | 0.093 . | 0.6853 |  | 172 |  | no standard error |
| period3_A32 | estimate | 0.002 . | -0.3848 |  | 172 |  | no standard error |
| period3_A33 | estimate | 0.671 . | -0.9615 |  | 172 |  | no standard error |
| period3_A34 | estimate | 0.42 . | 1.757 |  | 172 |  | no standard error |
| period3_A35 | estimate | -0.067 . | -0.343 |  | 172 |  | no standard error |
| period3_A40 | estimate | 0.037 . | -0.8477 |  | 172 |  | no standard error |
| period3_A41 | estimate | -0.191 . | 1.025 |  | 172 |  | no standard error |
| period3_A42 | estimate | -0.005 . | -0.6043 |  | 172 |  | no standard error |
| period3_A43 | estimate | 0.46 . | -0.7031 |  | 172 |  | no standard error |
| period3_A44 | estimate | 0.831 . | 1.575 |  | 172 |  | no standard error |
| period3_A45 | estimate | 0.078 . | -0.4866 |  | 172 |  | no standard error |
| period3_A50 | estimate | -0.366 . | 0.1886 |  | 172 |  | no standard error |
| period3_A51 | estimate | -0.1 . | -0.147 |  | 172 |  | no standard error |
| period3_A52 | estimate | -0.136 . | -0.9742 |  | 172 |  | no standard error |
| period3_A53 | estimate | 0.071 . | 0.6154 |  | 172 |  | no standard error |
| period3_A54 | estimate | 0.033 . | 0.2333 |  | 172 |  | no standard error |
| period3_A55 | estimate | 1.092 . | -0.9937 |  | 172 |  | no standard error |
| period5_A00 | estimate | -0.317 . | -0.1127 |  | 45 |  | no standard error |
| period5_A01 | estimate | -0.536 . | -0.2023 |  | 45 |  | no standard error |
| period5_A02 | estimate | -0.323 . | -0.1797 |  | 45 |  | no standard error |
| period5_A03 | estimate | -0.34 . | -0.3261 |  | 45 |  | no standard error |
| period5_A04 | estimate | -0.424 . | -0.1264 |  | 45 |  | no standard error |
| period5_A05 | estimate | -0.452 . | 0.4167 |  | 45 |  | no standard error |
| period5_A10 | estimate | -0.375 . | -0.1299 |  | 45 |  | no standard error |
| period5_A11 | estimate | -0.437 . | 0.1789 |  | 45 |  | no standard error |
| period5_A12 | estimate | -0.315 . | -0.3852 |  | 45 |  | no standard error |
| period5_A13 | estimate | -0.478 . | -0.3895 |  | 45 |  | no standard error |
| period5_A14 | estimate | -0.379 . | 0.1255 |  | 45 |  | no standard error |
| period5_A15 | estimate | -0.6 . | -0.9786 |  | 45 |  | no standard error |
| period5_A20 | estimate | -0.564 . | 0.5248 |  | 45 |  | no standard error |
| period5_A21 | estimate | -0.314 . | -1.981 |  | 45 |  | no standard error |
| period5_A22 | estimate | -0.136 . | 0.1615 |  | 45 |  | no standard error |
| period5_A23 | estimate | -0.408 . | -1.508 |  | 45 |  | no standard error |
| period5_A24 | estimate | -0.574 . | 1.154 |  | 45 |  | no standard error |
| period5_A25 | estimate | -0.577 . | -1.205 |  | 45 |  | no standard error |
| period5_A30 | estimate | -0.576 . | 0.738 |  | 45 |  | no standard error |
| period5_A31 | estimate | -0.452 . | -0.06921 |  | 45 |  | no standard error |
| period5_A32 | estimate | -0.427 . | -1.267 |  | 45 |  | no standard error |
| period5_A33 | estimate | -0.265 . | -0.5695 |  | 45 |  | no standard error |
| period5_A34 | estimate | -0.47 . | 0.02792 |  | 45 |  | no standard error |
| period5_A35 | estimate | -0.517 . | -0.9281 |  | 45 |  | no standard error |
| period5_A40 | estimate | -0.405 . | 0.9018 |  | 45 |  | no standard error |
| period5_A41 | estimate | -0.505 . | -0.5945 |  | 45 |  | no standard error |
| period5_A42 | estimate | -0.396 . | -2.494 |  | 45 |  | no standard error |
| period5_A43 | estimate | -0.406 . | 0.3101 |  | 45 |  | no standard error |
| period5_A44 | estimate | -0.346 . | -1.044 |  | 45 |  | no standard error |
| period5_A45 | estimate | -0.401 . | 0.6751 |  | 45 |  | no standard error |
| period5_A50 | estimate | -0.203 . | 0.6093 |  | 45 |  | no standard error |
| period5_A51 | estimate | -0.535 . | -0.1297 |  | 45 |  | no standard error |
| period5_A52 | estimate | -0.418 . | -0.8424 |  | 45 |  | no standard error |
| period5_A53 | estimate | -0.334 . | 0.03623 |  | 45 |  | no standard error |
| period5_A54 | estimate | -0.403 . | -0.574 |  | 45 |  | no standard error |
| period5_A55 | estimate | -0.338 . | 0.6943 |  | 45 |  | no standard error |
| lambda_train_type0 | estimate | 0.1 . | 0.1035 |  | 454 |  | no standard error |
| lambda_train_type1 | estimate | 0.101 . | 0.1017 |  | 454 |  | no standard error |
| lambda_test_type0 | estimate | 0.067 . | 0.07143 |  | 44 |  | no standard error |
| lambda_test_type1 | estimate | 0.082 . | 0.09398 |  | 44 |  | no standard error |

## The paper's own numbers
- OK: train_validation_split_experiment1: 2084 + 368 = 2452, paper's total 2452

## Guards
- no claims rejected
- spec: the headline was written as prose ('During active market Period 3, diagonal continuation is evidenced by period3_A00 = 1.161, period3_A11 = 1.143, period3_A'); chosen from the claim names: period3_A00
- spec problem unresolved: partition 'market_indices_by_type': total 'not stated' is not the name of a claim
- spec problem unresolved: partition 'sector_indices_by_type': total 'not stated' is not the name of a claim
- round 1: the builder ran out of turns
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (shanghai_mu0 (0.024) at line 611, shanghai_mu1 (0.044) at line 612, shanghai_A00 (0.382) at line 613, shanghai_A01 (0.387) at line 614, shanghai_A10 (0.218) at line 615, shanghai_A11 (0.343) at line 616, shenzhen_mu0 (0.038) at line 627, shenzhen_mu1 (0.047) at line 628, shenzhen_A00 (0.175) at line 629, shenzhen_A01 (0.451) at line 630, shenzhen_A10 (0.155) at line 631, shenzhen_A11 (0.381) at line 632, chinext_mu0 (0.034) at line 643, chinext_A00 (0.28) at line 645, chinext_A01 (0.385) at line 646, chinext_A10 (0.154) at line 647, chinext_A11 (0.348) at line 648, period3_omega (0.702) at line 685). Compute each result from the data; the paper's value never goes into it.
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 2456, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Data source: East Money API http://push2his.eastmoney.com for all indices (secid 1.000001,0.399001,0.399006,1.000932,1.000933,1.000934). Returns (close/prev_close-1)*100 simple. Descriptive stats pandas. Hawkes bivariate MLE via scipy L-BFGS-B, omega chosen by grid search over [0.05,0.08,0.1,0.2,0.5] maximizing likelihood. 6-dim nonlinear Hawkes with link g=max(x,0.01), integral via Monte Carlo 60 uniform samples, L-BFGS-B from generic init. Poisson lambda = n/T

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 3 tickers
- other hosts the script fetched from: push2his.eastmoney.com

## Run
- sandbox: attempt 2, exit 0, 141.6s
- model calls: 48, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 2848987, out 136703 (reasoning 63197); cost $1.2502

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
