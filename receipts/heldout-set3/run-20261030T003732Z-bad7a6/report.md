The paper's numbers partly hold up: 13 of 26 checked results match within their uncertainty. Its main result, abstract_hat_theta_mean, is 0.91 in the paper and 0.9097 here (consistent). Sample size not rebuilt: requires 90k fBm paths T=2^16 via Davies-Harte exact circulant embedding (N=10k per H x9) ~5.9e8 timesteps, infeasible in 20min sandbox (fBm_N_per_H, 10,000 in the paper).

# paper-replicator report: arXiv 2512.02352
**First-passage horizons in HVG: rank-invariant path-roughness estimator verified from first-passage persistence and HVG; rough Bergomi H=0.1, verification via fBm/RB numeric experiments; deployment on 20plus years VIX rolling W1024 step126 with overlapping-window iid Monte Carlo nulls (single-window 95% envelope and rolling-mean/count Monte Carlo p) and block bootstrap CIs; sensitivity for ties/censoring/additive noise/thinning; control processes i.i.d./BM/GBM/OU and benchmark vol models Heston/GARCH/FIGARCH.**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| fBm_N_per_H | count | 1e+04 paths |  |  |  |  | not computed |
| fBm_T_validation | parameter | 2 timesteps |  |  |  |  | not computed |
| fBm_H01_hat_theta | estimate | 0.9 Hill-CSN cross-replicate mean at T=2^16 N=10,000 fBm H=0.1 predicted 0.90 vs bias -0.0003 etc. |  |  |  |  | not computed |
| fBm_H01_sigma | estimate | 0.013 |  |  |  |  | not computed |
| fBm_H01_predicted | parameter | 0.9 |  |  |  |  | not computed |
| fBm_H01_bias | estimate | -0.0003 |  |  |  |  | not computed |
| fBm_H01_ell0star_bar | parameter | 20 |  |  |  |  | not computed |
| fBm_H02_hat | estimate | 0.81 |  |  |  |  | not computed |
| fBm_H02_sigma | estimate | 0.013 |  |  |  |  | not computed |
| fBm_H02_pred | parameter | 0.8 |  |  |  |  | not computed |
| fBm_H02_bias | estimate | 0.01 |  |  |  |  | not computed |
| fBm_H02_ell | parameter | 20 |  |  |  |  | not computed |
| fBm_H03_hat | estimate | 0.728 |  |  |  |  | not computed |
| fBm_H03_sigma | estimate | 0.015 |  |  |  |  | not computed |
| fBm_H03_pred | parameter | 0.7 |  |  |  |  | not computed |
| fBm_H03_bias | estimate | 0.028 |  |  |  |  | not computed |
| fBm_H03_ell | parameter | 20 |  |  |  |  | not computed |
| fBm_H04_hat | estimate | 0.65 |  |  |  |  | not computed |
| fBm_H04_sigma | estimate | 0.019 |  |  |  |  | not computed |
| fBm_H04_pred | parameter | 0.6 |  |  |  |  | not computed |
| fBm_H04_bias | estimate | 0.05 |  |  |  |  | not computed |
| fBm_H04_ell | parameter | 20 |  |  |  |  | not computed |
| fBm_H05_hat | estimate | 0.575 |  |  |  |  | not computed |
| fBm_H05_sigma | estimate | 0.024 |  |  |  |  | not computed |
| fBm_H05_pred | parameter | 0.5 |  |  |  |  | not computed |
| fBm_H05_bias | estimate | 0.075 |  |  |  |  | not computed |
| fBm_H05_ell | parameter | 19 |  |  |  |  | not computed |
| fBm_H06_hat | estimate | 0.505 |  |  |  |  | not computed |
| fBm_H06_sigma | estimate | 0.032 |  |  |  |  | not computed |
| fBm_H06_pred | parameter | 0.4 |  |  |  |  | not computed |
| fBm_H06_bias | estimate | 0.105 |  |  |  |  | not computed |
| fBm_H06_ell | parameter | 14 |  |  |  |  | not computed |
| fBm_H07_hat | estimate | 0.445 |  |  |  |  | not computed |
| fBm_H07_sigma | estimate | 0.046 |  |  |  |  | not computed |
| fBm_H07_pred | parameter | 0.3 |  |  |  |  | not computed |
| fBm_H07_bias | estimate | 0.145 |  |  |  |  | not computed |
| fBm_H07_ell | parameter | 9 |  |  |  |  | not computed |
| fBm_H08_hat | estimate | 0.405 |  |  |  |  | not computed |
| fBm_H08_sigma | estimate | 0.075 |  |  |  |  | not computed |
| fBm_H08_pred | parameter | 0.2 |  |  |  |  | not computed |
| fBm_H08_bias | estimate | 0.205 |  |  |  |  | not computed |
| fBm_H08_ell | parameter | 7 |  |  |  |  | not computed |
| fBm_H09_hat | estimate | 0.423 |  |  |  |  | not computed |
| fBm_H09_sigma | estimate | 0.183 |  |  |  |  | not computed |
| fBm_H09_pred | parameter | 0.1 |  |  |  |  | not computed |
| fBm_H09_bias | estimate | 0.323 |  |  |  |  | not computed |
| fBm_H09_ell | parameter | 15 |  |  |  |  | not computed |
| control_iid_uniform_hat | estimate | 1.021 theta_hat |  |  |  |  | not computed |
| control_iid_uniform_SE | estimate | 0.002 |  |  |  |  | not computed |
| control_iid_uniform_sigma | estimate | 0.012 |  |  |  |  | not computed |
| control_iid_uniform_pred | parameter | 1 |  |  |  |  | not computed |
| control_iid_gaussian_hat | estimate | 1.024 |  |  |  |  | not computed |
| control_iid_gaussian_SE | estimate | 0.002 |  |  |  |  | not computed |
| control_iid_gaussian_sigma | estimate | 0.014 |  |  |  |  | not computed |
| control_iid_gaussian_pred | parameter | 1 |  |  |  |  | not computed |
| control_BM_hat | estimate | 0.569 |  |  |  |  | not computed |
| control_BM_SE | estimate | 0.004 |  |  |  |  | not computed |
| control_BM_sigma | estimate | 0.025 |  |  |  |  | not computed |
| control_BM_pred | parameter | 0.5 |  |  |  |  | not computed |
| control_OU_001_hat | estimate | 0.653 |  |  |  |  | not computed |
| control_OU_001_SE | estimate | 0.002 |  |  |  |  | not computed |
| control_OU_001_sigma | estimate | 0.014 |  |  |  |  | not computed |
| control_OU_10_hat | estimate | 1.052 |  |  |  |  | not computed |
| control_OU_10_SE | estimate | 0.002 |  |  |  |  | not computed |
| control_OU_10_sigma | estimate | 0.011 |  |  |  |  | not computed |
| control_OU_10_pred | parameter | 1 |  |  |  |  | not computed |
| control_GBM_hat | estimate | 0.57 |  |  |  |  | not computed |
| control_GBM_SE | estimate | 0.004 |  |  |  |  | not computed |
| control_GBM_sigma | estimate | 0.025 |  |  |  |  | not computed |
| control_GBM_pred | parameter | 0.5 |  |  |  |  | not computed |
| iid_uniform_decay_T14 | estimate | 1.041 | 1.045 | 0.002325 | 50 | True | paper inside 1.045 +/- 0.004558 |
| iid_uniform_decay_T16 | estimate | 1.024 | 1.034 | 0.0007156 | 50 | False | paper outside 1.034 +/- 0.001403 |
| iid_uniform_decay_T18 | estimate | 1.016 | 1.03 | 0.0004151 | 50 | False | paper outside 1.03 +/- 0.0008135 |
| iid_uniform_decay_T20 | estimate | 1.014 | 1.028 | 0.0002879 | 50 | False | paper outside 1.028 +/- 0.0005644 |
| rb_heatmap_max_eta_diff | estimate | 0.00048 |  |  |  |  | not computed |
| rb_heatmap_H015_match | estimate | 0.003 |  |  |  |  | not computed |
| rb_heatmap_H02_match | estimate | 0.01 |  |  |  |  | not computed |
| cmp_rBergomi_hat | estimate | 0.8989 |  |  |  |  | not computed |
| cmp_rBergomi_SE | estimate | 0.0001 |  |  |  |  | not computed |
| cmp_rBergomi_95lo | estimate | 0.874 |  |  |  |  | not computed |
| cmp_rBergomi_95hi | estimate | 0.924 |  |  |  |  | not computed |
| cmp_FIGARCH_hat | estimate | 0.8409 |  |  |  |  | not computed |
| cmp_FIGARCH_SE | estimate | 0.0002 |  |  |  |  | not computed |
| cmp_FIGARCH_95lo | estimate | 0.81 |  |  |  |  | not computed |
| cmp_FIGARCH_95hi | estimate | 0.87 |  |  |  |  | not computed |
| cmp_GARCH_hat | estimate | 0.7234 |  |  |  |  | not computed |
| cmp_GARCH_SE | estimate | 0.0007 |  |  |  |  | not computed |
| cmp_GARCH_95lo | estimate | 0.64 |  |  |  |  | not computed |
| cmp_GARCH_95hi | estimate | 0.838 |  |  |  |  | not computed |
| cmp_Heston_hat | estimate | 0.5635 |  |  |  |  | not computed |
| cmp_Heston_SE | estimate | 0.0002 |  |  |  |  | not computed |
| cmp_Heston_95lo | estimate | 0.528 |  |  |  |  | not computed |
| cmp_Heston_95hi | estimate | 0.606 |  |  |  |  | not computed |
| cmp_diff_rB_Heston | estimate | 0.3355 |  |  |  |  | not computed |
| cmp_diff_rB_Heston_SE | estimate | 0.00024 |  |  |  |  | not computed |
| cmp_diff_rB_FIGARCH | estimate | 0.058 |  |  |  |  | not computed |
| cmp_diff_rB_FIGARCH_SE | estimate | 0.0002 |  |  |  |  | not computed |
| VIX_n_days | count | 6651 days | 6621 |  | 6621 | True | approximate: -0.5%, within SCORE's +/-15% |
| VIX_windows_count | count | 45 windows | 45 | 0 | 45 | True | precise: the paper's count |
| VIX_W_length | parameter | 1024 days | 1024 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| VIX_step_length | parameter | 126 days | 126 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| VIX_rolling_mean_complete | estimate | 0.91 theta | 0.9097 | 0.02837 | 45 | True | paper inside 0.9097 +/- 0.05561 |
| VIX_rolling_sigma_complete | estimate | 0.19 | 0.1903 |  | 45 |  | no standard error |
| VIX_rolling_range_lo_complete | estimate | 0.723 | 0.7233 |  | 45 |  | no standard error |
| VIX_rolling_range_hi_complete | estimate | 1.506 | 1.508 |  | 45 |  | no standard error |
| VIX_rolling_range_lo_text | estimate | 0.72 | 0.72 |  | 45 |  | no standard error |
| VIX_rolling_range_hi_text | estimate | 1.51 | 1.51 |  | 45 |  | no standard error |
| VIX_windows_total_45 | count | 45 windows | 45 |  | 45 | True | precise: the paper's count |
| VIX_censored_mean_per_window | estimate | 24.4 horizons | 25.18 | 1.885 | 45 | True | paper inside 25.18 +/- 3.694 |
| VIX_censored_above_threshold | estimate | 21.8 horizons | 21.31 | 1.881 | 45 | True | paper inside 21.31 +/- 3.686 |
| VIX_tie_break_shift | estimate | 0.003 theta | 0.005632 |  | 45 |  | no standard error |
| censor_complete_mean | estimate | 0.91 | 0.9097 | 0.02837 | 45 | True | paper inside 0.9097 +/- 0.05561 |
| censor_complete_sigma | estimate | 0.19 | 0.1903 |  | 45 |  | no standard error |
| censor_censored_mean | estimate | 0.674 | 0.676 | 0.01555 | 45 | True | paper inside 0.676 +/- 0.03047 |
| censor_censored_sigma | estimate | 0.102 | 0.1043 |  | 45 |  | no standard error |
| censor_censored_lo | estimate | 0.507 | 0.5068 |  | 45 |  | no standard error |
| censor_censored_hi | estimate | 0.985 | 0.9902 |  | 45 |  | no standard error |
| censor_lower_mean | estimate | 0.757 | 0.7586 | 0.01431 | 45 | True | paper inside 0.7586 +/- 0.02804 |
| censor_lower_sigma | estimate | 0.099 | 0.09597 |  | 45 |  | no standard error |
| censor_lower_lo | estimate | 0.603 | 0.6047 |  | 45 |  | no standard error |
| censor_lower_hi | estimate | 1.03 | 1.035 |  | 45 |  | no standard error |
| iid_null_W1024_mean | estimate | 1.166 | 1.138 | 0.00253 | 1000 | False | paper outside 1.138 +/- 0.00496 |
| iid_null_W1024_sigma | estimate | 0.091 | 0.08002 |  | 1000 |  | no standard error |
| iid_null_W1024_95lo | estimate | 1.017 | 0.9963 |  | 1000 |  | no standard error |
| iid_null_W1024_95hi | estimate | 1.376 | 1.319 |  | 1000 |  | no standard error |
| iid_null_W1024_N | count | 1000 replicates | 1000 |  | 1000 | True | precise: the paper's count |
| overlap_null_windows_below_tally | tally | 35 windows | 35 |  | 45 |  | a tally of what the analysis found, with no uncertainty, so it is not judged |
| overlap_null_threshold | parameter | 1.017 | 1.017 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| overlap_null_count_mean | estimate | 1.35 windows | 1.888 | 0.06876 | 1000 | False | paper outside 1.888 +/- 0.1348 |
| overlap_null_count_99q | estimate | 7 | 9 |  | 1000 |  | no standard error |
| overlap_null_count_max | estimate | 10 | 11 |  | 1000 |  | no standard error |
| overlap_null_count_p | p_value | 0.001 | 0.000999 |  | 1000 | True | both < 0.05 |
| overlap_null_rolling_mean | estimate | 1.16 | 1.14 | 0.000749 | 1000 | False | paper outside 1.14 +/- 0.001468 |
| overlap_null_rolling_sigma | estimate | 0.026 | 0.02368 |  | 1000 |  | no standard error |
| VIX_overall_mean_091_vs_null | estimate | 0.91 | 0.9097 | 0.02837 | 45 | True | paper inside 0.9097 +/- 0.05561 |
| overlap_rollmean_p | p_value | 0.001 | 0.000999 |  | 1000 | True | both < 0.05 |
| abstract_hat_theta_mean | estimate | 0.91 | 0.9097 | 0.02837 | 45 | True | paper inside 0.9097 +/- 0.05561 |
| abstract_hat_theta_sigma | estimate | 0.19 | 0.1903 |  | 45 |  | no standard error |
| abstract_p_lt_001 | p_value | 0.001 | 0.000999 |  | 1000 | True | both < 0.05 |
| null_table_W512_mean | estimate | 1.211 | 1.204 | 0.00347 | 1000 | True | paper inside 1.204 +/- 0.0068 |
| null_table_W512_sigma | estimate | 0.118 | 0.1097 |  | 1000 |  | no standard error |
| null_table_W512_25 | estimate | 1.01 | 1.017 |  | 1000 |  | no standard error |
| null_table_W512_975 | estimate | 1.465 | 1.435 |  | 1000 |  | no standard error |
| null_table_W512_median | estimate | 1.198 | 1.196 |  | 1000 |  | no standard error |
| null_table_W512_N | count | 1000 | 1000 |  | 1000 | True | precise: the paper's count |
| null_table_W1024_mean2 | estimate | 1.166 | 1.138 | 0.00253 | 1000 | False | paper outside 1.138 +/- 0.00496 |
| null_table_W1024_sigma2 | estimate | 0.091 | 0.08002 |  | 1000 |  | no standard error |
| null_table_W1024_25 | estimate | 1.017 | 0.9963 |  | 1000 |  | no standard error |
| null_table_W1024_975 | estimate | 1.376 | 1.319 |  | 1000 |  | no standard error |
| null_table_W1024_med | estimate | 1.157 | 1.133 |  | 1000 |  | no standard error |
| null_table_W1024_N2 | count | 1000 | 1000 |  | 1000 | True | precise: the paper's count |
| null_table_W2048_mean | estimate | 1.136 | 1.1 | 0.001654 | 1000 | False | paper outside 1.1 +/- 0.003241 |
| null_table_W2048_sigma | estimate | 0.084 | 0.0523 |  | 1000 |  | no standard error |
| null_table_W2048_25 | estimate | 0.994 | 1 |  | 1000 |  | no standard error |
| null_table_W2048_975 | estimate | 1.31 | 1.204 |  | 1000 |  | no standard error |
| null_table_W2048_med | estimate | 1.13 | 1.1 |  | 1000 |  | no standard error |
| null_table_W2048_N | count | 1000 | 1000 |  | 1000 | True | precise: the paper's count |
| null_table_W4096_mean | estimate | 1.09 | 1.073 | 0.001085 | 1000 | False | paper outside 1.073 +/- 0.002126 |
| null_table_W4096_sigma | estimate | 0.056 | 0.0343 |  | 1000 |  | no standard error |
| null_table_W4096_25 | estimate | 0.985 | 1.006 |  | 1000 |  | no standard error |
| null_table_W4096_975 | estimate | 1.201 | 1.138 |  | 1000 |  | no standard error |
| null_table_W4096_med | estimate | 1.087 | 1.072 |  | 1000 |  | no standard error |
| null_table_W4096_N | count | 1000 | 1000 |  | 1000 | True | precise: the paper's count |
| null_table_W8192_mean | estimate | 1.06 | 1.054 | 0.0007543 | 1000 | False | paper outside 1.054 +/- 0.001478 |
| null_table_W8192_sigma | estimate | 0.039 | 0.02385 |  | 1000 |  | no standard error |
| null_table_W8192_25 | estimate | 0.988 | 1.009 |  | 1000 |  | no standard error |
| null_table_W8192_975 | estimate | 1.136 | 1.103 |  | 1000 |  | no standard error |
| null_table_W8192_med | estimate | 1.058 | 1.054 |  | 1000 |  | no standard error |
| null_table_W8192_N | count | 1000 | 1000 |  | 1000 | True | precise: the paper's count |
| null_table_W16384_mean | estimate | 1.042 | 1.045 | 0.0005105 | 1000 | False | paper outside 1.045 +/- 0.001 |
| null_table_W16384_sigma | estimate | 0.025 | 0.01614 |  | 1000 |  | no standard error |
| null_table_W16384_25 | estimate | 0.994 | 1.014 |  | 1000 |  | no standard error |
| null_table_W16384_975 | estimate | 1.092 | 1.075 |  | 1000 |  | no standard error |
| null_table_W16384_med | estimate | 1.042 | 1.045 |  | 1000 |  | no standard error |
| null_table_W16384_N | count | 1000 | 1000 |  | 1000 | True | precise: the paper's count |
| null_table_W32768_mean | estimate | 1.03 | 1.038 | 0.0005097 | 500 | False | paper outside 1.038 +/- 0.000999 |
| null_table_W32768_sigma | estimate | 0.016 | 0.0114 |  | 500 |  | no standard error |
| null_table_W32768_25 | estimate | 0.999 | 1.016 |  | 500 |  | no standard error |
| null_table_W32768_975 | estimate | 1.062 | 1.061 |  | 500 |  | no standard error |
| null_table_W32768_med | estimate | 1.03 | 1.038 |  | 500 |  | no standard error |
| null_table_W32768_N | count | 500 | 500 |  | 500 | True | precise: the paper's count |
| null_table_W65536_mean | estimate | 1.023 | 1.034 | 0.0003671 | 500 | False | paper outside 1.034 +/- 0.0007196 |
| null_table_W65536_sigma | estimate | 0.012 | 0.008209 |  | 500 |  | no standard error |
| null_table_W65536_25 | estimate | 1 | 1.018 |  | 500 |  | no standard error |
| null_table_W65536_975 | estimate | 1.048 | 1.05 |  | 500 |  | no standard error |
| null_table_W65536_med | estimate | 1.023 | 1.034 |  | 500 |  | no standard error |
| null_table_W65536_N | count | 500 | 500 |  | 500 | True | precise: the paper's count |
| sens_bias_H01_T12 | estimate | 0.078 |  |  |  |  | not computed |
| sens_bias_H01_T18 | estimate | -0.01 |  |  |  |  | not computed |
| sens_bias_H05_T12 | estimate | 0.2 |  |  |  |  | not computed |
| sens_bias_H05_T18 | estimate | 0.046 |  |  |  |  | not computed |
| sens_Hill_plateau_range | parameter | 10 |  |  |  |  | not computed |
| sens_Hill_plateau_range_hi | parameter | 60 |  |  |  |  | not computed |
| sens_Hill_move | estimate | 0.02 |  |  |  |  | not computed |
| sens_noise_sigma10_hat | estimate | 0.984 |  |  |  |  | not computed |
| sens_noise_bias_thresh | parameter | 0.3 relative scale |  |  |  |  | not computed |
| sens_noise_bias_limit | estimate | 0.02 |  |  |  |  | not computed |
| sens_thinning_rate | parameter | 50 |  |  |  |  | not computed |
| rb_s_star_lower | parameter | 1 |  |  |  |  | not computed |
| rb_r_max | estimate | 0.28 |  |  |  |  | not computed |
| rb_r_small_scale | estimate | 0.001 |  |  |  |  | not computed |
| rb_micro_scale | parameter | 0.0003 |  |  |  |  | not computed |
| theory_survival_iid | parameter | 1 | 1 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| theory_theta_iid | parameter | 1 | 1 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| theory_theta_H | parameter | 1 | 1 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| block_B | parameter | 200 resamples |  |  |  |  | not computed |
| block_b_formula | parameter | 1 days |  |  |  |  | not computed |

## The paper's own numbers
- NOTE: VIX rolling mean vs overlapping-window iid null: t = 0.91 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.3628); judged two-sided
- OK: VIX count of windows below single-window 2.5% quantile vs overlapping-window iid null: t = 35, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000

## Guards
- rejected claim VIX_windows_above07_tally = 43: not in the paper's LaTeX
- rejected claim censor_complete_range_lo = 0.723: printed once in the paper's LaTeX, and already claimed by VIX_rolling_range_lo_complete
- rejected claim censor_complete_range_hi = 1.506: printed once in the paper's LaTeX, and already claimed by VIX_rolling_range_hi_complete
- spec: the headline was written as prose ('github/hubspot/cms-content/pull/12345" }, '); chosen from the claim names: VIX_rolling_mean_complete
- sample: the sample differs from the paper's by 30 missing and 0 extra observations (0.5% of the paper's 6651, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: FRED VIXCLS proxied by Yahoo ^VIX daily close (same CBOE VIX level, rank-invariant statistic on level so close vs VIXCLS level immaterial). FRED HTTP timed out in sandbox (no curl, requests timeout to fred.stlouisfed.org), so market_data.get_prices served cached Yahoo ^VIX. Ties handled by deterministic time-order (later equal = crossing) as per paper Sec3, stricter convention shift 0.003-0.006. Hill-MLE and CSN threshold implemented exactly as described (candidate set 1..min(19,floor(q0.9)) +30 log-spaced 20..q0.9, KS distance sup|empirical-Pareto|). iid nulls are Monte Carlo uniform replicates; overlapping-window null 1000 iid uniform paths length 6621 same W/step. VIX rolling windows W=1024 step126
- caveat: sample size not rebuilt: requires 90k fBm paths T=2^16 via Davies-Harte exact circulant embedding (N=10k per H x9) ~5.9e8 timesteps, infeasible in 20min sandbox (fBm_N_per_H, 10,000 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 1 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 1, exit 0, 143.0s
- model calls: 30, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 1568245, out 96830 (reasoning 39090); cost $0.8294

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
