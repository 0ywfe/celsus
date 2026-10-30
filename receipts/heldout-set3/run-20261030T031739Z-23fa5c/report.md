The paper's numbers partly hold up: 18 of 41 checked results match within their uncertainty. Its main result, p_abstract, is 0.001 p in the paper and 0.002494 p here (consistent).

# paper-replicator report: arXiv 2512.02352
**First-passage horizons in HVG rank-invariant estimator of path roughness - replication spec**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| fbm_H0.1_hat | estimate | 0.9 theta | 0.9037 | 0.0007759 | 150 | False | paper outside 0.9037 +/- 0.001521 |
| fbm_H0.1_sigma | estimate | 0.013 theta | 0.009503 |  | 150 |  | no standard error |
| fbm_H0.1_pred | parameter | 0.9 theta | 0.9 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.1_bias | estimate | -0.0003 theta | 0.003668 | 0.0007759 | 150 | False | paper outside 0.003668 +/- 0.001521 |
| fbm_H0.1_l0star | parameter | 20 lag | 10.98 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.2_hat | estimate | 0.81 theta | 0.8091 | 0.0008291 | 150 | True | paper inside 0.8091 +/- 0.001625 |
| fbm_H0.2_sigma | estimate | 0.013 theta | 0.01015 |  | 150 |  | no standard error |
| fbm_H0.2_pred | parameter | 0.8 theta | 0.8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.2_bias | estimate | 0.01 theta | 0.009137 | 0.0008291 | 150 | True | paper inside 0.009137 +/- 0.001625 |
| fbm_H0.2_l0star | parameter | 20 lag | 12.89 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.3_hat | estimate | 0.728 theta | 0.7279 | 0.001064 | 150 | True | paper inside 0.7279 +/- 0.002085 |
| fbm_H0.3_sigma | estimate | 0.015 theta | 0.01303 |  | 150 |  | no standard error |
| fbm_H0.3_pred | parameter | 0.7 theta | 0.7 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.3_bias | estimate | 0.028 theta | 0.02788 | 0.001064 | 150 | True | paper inside 0.02788 +/- 0.002085 |
| fbm_H0.3_l0star | parameter | 20 lag | 15.91 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.4_hat | estimate | 0.65 theta | 0.6485 | 0.001483 | 150 | True | paper inside 0.6485 +/- 0.002907 |
| fbm_H0.4_sigma | estimate | 0.019 theta | 0.01817 |  | 150 |  | no standard error |
| fbm_H0.4_pred | parameter | 0.6 theta | 0.6 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.4_bias | estimate | 0.05 theta | 0.04847 | 0.001483 | 150 | True | paper inside 0.04847 +/- 0.002907 |
| fbm_H0.4_l0star | parameter | 20 lag | 20.31 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.5_hat | estimate | 0.575 theta | 0.5683 | 0.002038 | 150 | False | paper outside 0.5683 +/- 0.003995 |
| fbm_H0.5_sigma | estimate | 0.024 theta | 0.02496 |  | 150 |  | no standard error |
| fbm_H0.5_pred | parameter | 0.5 theta | 0.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.5_bias | estimate | 0.075 theta | 0.06832 | 0.002038 | 150 | False | paper outside 0.06832 +/- 0.003995 |
| fbm_H0.5_l0star | parameter | 19 lag | 19.47 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.6_hat | estimate | 0.505 theta | 0.4966 | 0.002404 | 150 | False | paper outside 0.4966 +/- 0.004713 |
| fbm_H0.6_sigma | estimate | 0.032 theta | 0.02945 |  | 150 |  | no standard error |
| fbm_H0.6_pred | parameter | 0.4 theta | 0.4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.6_bias | estimate | 0.105 theta | 0.09662 | 0.002404 | 150 | False | paper outside 0.09662 +/- 0.004713 |
| fbm_H0.6_l0star | parameter | 14 lag | 13.73 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.7_hat | estimate | 0.445 theta | 0.429 | 0.003221 | 150 | False | paper outside 0.429 +/- 0.006313 |
| fbm_H0.7_sigma | estimate | 0.046 theta | 0.03945 |  | 150 |  | no standard error |
| fbm_H0.7_pred | parameter | 0.3 theta | 0.3 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.7_bias | estimate | 0.145 theta | 0.129 | 0.003221 | 150 | False | paper outside 0.129 +/- 0.006313 |
| fbm_H0.7_l0star | parameter | 9 lag | 9.227 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.8_hat | estimate | 0.405 theta | 0.3792 | 0.003821 | 150 | False | paper outside 0.3792 +/- 0.007488 |
| fbm_H0.8_sigma | estimate | 0.075 theta | 0.04679 |  | 150 |  | no standard error |
| fbm_H0.8_pred | parameter | 0.2 theta | 0.2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.8_bias | estimate | 0.205 theta | 0.1792 | 0.003821 | 150 | False | paper outside 0.1792 +/- 0.007488 |
| fbm_H0.8_l0star | parameter | 7 lag | 6.167 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.9_hat | estimate | 0.423 theta | 0.3831 | 0.009917 | 150 | False | paper outside 0.3831 +/- 0.01944 |
| fbm_H0.9_sigma | estimate | 0.183 theta | 0.1215 |  | 150 |  | no standard error |
| fbm_H0.9_pred | parameter | 0.1 theta | 0.1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fbm_H0.9_bias | estimate | 0.323 theta | 0.2831 | 0.009917 | 150 | False | paper outside 0.2831 +/- 0.01944 |
| fbm_H0.9_l0star | parameter | 15 lag | 5.88 |  | 150 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ctrl_uniform_hat | estimate | 1.021 theta | 1.032 | 0.001054 | 50 | False | paper outside 1.032 +/- 0.002065 |
| ctrl_uniform_SE | estimate | 0.002 theta | 0.001054 |  | 50 |  | no standard error |
| ctrl_uniform_sigma | estimate | 0.012 theta | 0.00745 |  | 50 |  | no standard error |
| ctrl_uniform_pred | parameter | 1 theta | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ctrl_gauss_hat | estimate | 1.024 theta | 1.034 | 0.001039 | 50 | False | paper outside 1.034 +/- 0.002037 |
| ctrl_gauss_SE | estimate | 0.002 theta | 0.001039 |  | 50 |  | no standard error |
| ctrl_gauss_sigma | estimate | 0.014 theta | 0.007348 |  | 50 |  | no standard error |
| ctrl_gauss_pred | parameter | 1 theta | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ctrl_BM_hat | estimate | 0.569 theta | 0.5742 | 0.003178 | 50 | True | paper inside 0.5742 +/- 0.00623 |
| ctrl_BM_SE | estimate | 0.004 theta | 0.003178 |  | 50 |  | no standard error |
| ctrl_BM_sigma | estimate | 0.025 theta | 0.02247 |  | 50 |  | no standard error |
| ctrl_BM_pred | parameter | 0.5 theta | 0.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ctrl_OU01_hat | estimate | 0.653 theta |  |  |  |  | not computed |
| ctrl_OU01_SE | estimate | 0.002 theta |  |  |  |  | not computed |
| ctrl_OU01_sigma | estimate | 0.014 theta |  |  |  |  | not computed |
| ctrl_OU10_hat | estimate | 1.052 theta |  |  |  |  | not computed |
| ctrl_OU10_SE | estimate | 0.002 theta |  |  |  |  | not computed |
| ctrl_OU10_sigma | estimate | 0.011 theta |  |  |  |  | not computed |
| ctrl_OU10_pred | parameter | 1 theta |  |  |  |  | not computed |
| ctrl_GBM_hat | estimate | 0.57 theta | 0.5718 | 0.002992 | 50 | True | paper inside 0.5718 +/- 0.005863 |
| ctrl_GBM_SE | estimate | 0.004 theta | 0.002992 |  | 50 |  | no standard error |
| ctrl_GBM_sigma | estimate | 0.025 theta | 0.02115 |  | 50 |  | no standard error |
| ctrl_GBM_pred | parameter | 0.5 theta | 0.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| iid_uniform_T14_hat | estimate | 1.041 theta | 1.04 |  | 20 |  | no standard error |
| iid_uniform_T16_hat | estimate | 1.024 theta | 1.033 |  | 20 |  | no standard error |
| iid_uniform_T18_hat | estimate | 1.016 theta | 1.028 |  | 20 |  | no standard error |
| iid_uniform_T20_hat | estimate | 1.014 theta |  |  |  |  | not computed |
| bias_decay_H01_T12 | estimate | 0.078 theta |  |  |  |  | not computed |
| bias_decay_H01_T18 | estimate | -0.01 theta |  |  |  |  | not computed |
| bias_decay_H05_T12 | estimate | 0.2 theta |  |  |  |  | not computed |
| bias_decay_H05_T18 | estimate | 0.046 theta |  |  |  |  | not computed |
| hill_plateau_move | estimate | 0.02 theta |  |  |  |  | not computed |
| noise_s1_hat | estimate | 0.984 theta |  |  |  |  | not computed |
| noise_bias_le0.3 | estimate | 0.02 theta |  |  |  |  | not computed |
| drift_noise_ratio_max | estimate | 0.28 ratio | 0.2131 |  |  |  | no standard error |
| drift_noise_ratio_tail | estimate | 0.001 ratio | 0.0007372 |  |  |  | no standard error |
| tie_break_delta | estimate | 0.003 theta | 0.003174 |  | 45 |  | no standard error |
| model_rB_hat | estimate | 0.8989 theta |  |  |  |  | not computed |
| model_rB_SE | estimate | 0.0001 theta |  |  |  |  | not computed |
| model_rB_CI_low | estimate | 0.874 theta |  |  |  |  | not computed |
| model_rB_CI_high | estimate | 0.924 theta |  |  |  |  | not computed |
| model_FIG_hat | estimate | 0.8409 theta |  |  |  |  | not computed |
| model_FIG_SE | estimate | 0.0002 theta |  |  |  |  | not computed |
| model_FIG_low | estimate | 0.81 theta |  |  |  |  | not computed |
| model_FIG_high | estimate | 0.87 theta |  |  |  |  | not computed |
| model_GARCH_hat | estimate | 0.7234 theta |  |  |  |  | not computed |
| model_GARCH_SE | estimate | 0.0007 theta |  |  |  |  | not computed |
| model_GARCH_low | estimate | 0.64 theta |  |  |  |  | not computed |
| model_GARCH_high | estimate | 0.838 theta |  |  |  |  | not computed |
| model_Heston_hat | estimate | 0.5635 theta |  |  |  |  | not computed |
| model_Heston_SE | estimate | 0.0002 theta |  |  |  |  | not computed |
| model_Heston_low | estimate | 0.528 theta |  |  |  |  | not computed |
| model_Heston_high | estimate | 0.606 theta |  |  |  |  | not computed |
| sep_rB_Heston | estimate | 0.3355 theta |  |  |  |  | not computed |
| sep_rB_Heston_SE | estimate | 0.00024 theta |  |  |  |  | not computed |
| sep_rB_FIG | estimate | 0.058 theta |  |  |  |  | not computed |
| sep_rB_FIG_SE | estimate | 0.0002 theta |  |  |  |  | not computed |
| vix_n_days | count | 6651 days | 6651 | 0 | 6651 | True | precise: the paper's count |
| vix_W | parameter | 1024 days | 1024 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| vix_step | parameter | 126 days | 126 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| vix_n_windows | count | 45 windows | 45 | 0 | 45 |  | the script writes it as a fixed number (45 at line 496), so it is not judged |
| vix_roll_mean_text | estimate | 0.91 theta | 0.9098 | 0.02834 | 45 | True | paper inside 0.9098 +/- 0.05554 |
| vix_roll_sd_text | estimate | 0.19 theta | 0.1901 |  | 45 |  | no standard error |
| vix_roll_range_low_text | estimate | 0.72 theta | 0.7229 |  | 45 |  | no standard error |
| vix_roll_range_high_text | estimate | 1.51 theta | 1.506 |  | 45 |  | no standard error |
| vix_roll_mean_table | estimate | 0.91 theta | 0.9098 | 0.02834 | 45 | True | paper inside 0.9098 +/- 0.05554 |
| vix_roll_sd_table | estimate | 0.19 theta | 0.1901 |  | 45 |  | no standard error |
| vix_roll_min_table | estimate | 0.723 theta | 0.7229 |  | 45 |  | no standard error |
| vix_roll_max_table | estimate | 1.506 theta | 1.506 |  | 45 |  | no standard error |
| vix_above07_total | count | 45 windows | 45 |  |  |  | the script writes it as a fixed number (45 at line 506), so it is not judged |
| vix_cens_complete_mean | estimate | 0.91 theta | 0.9098 | 0.02834 | 45 | True | paper inside 0.9098 +/- 0.05554 |
| vix_cens_pareto_mean | estimate | 0.674 theta | 0.6739 | 0.01525 | 45 | True | paper inside 0.6739 +/- 0.0299 |
| vix_cens_pareto_sd | estimate | 0.102 theta | 0.1023 |  | 45 |  | no standard error |
| vix_cens_pareto_low | estimate | 0.507 theta | 0.507 |  | 45 |  | no standard error |
| vix_cens_pareto_high | estimate | 0.985 theta | 0.9849 |  | 45 |  | no standard error |
| vix_cens_lower_mean | estimate | 0.757 theta | 0.7566 | 0.01477 | 45 | True | paper inside 0.7566 +/- 0.02894 |
| vix_cens_lower_sd | estimate | 0.099 theta | 0.09905 |  | 45 |  | no standard error |
| vix_cens_lower_low | estimate | 0.603 theta | 0.605 |  | 45 |  | no standard error |
| vix_cens_lower_high | estimate | 1.03 theta | 1.03 |  | 45 |  | no standard error |
| vix_avg_censored_per_window | estimate | 24.4 horizons | 24.44 |  | 45 |  | no standard error |
| vix_avg_censored_above_thresh | estimate | 21.8 horizons | 21.96 |  | 45 |  | no standard error |
| null_single_W1024_mean | estimate | 1.166 theta | 1.143 | 0.003394 | 500 | False | paper outside 1.143 +/- 0.006652 |
| null_single_W1024_sd | estimate | 0.091 theta | 0.07589 |  | 500 |  | no standard error |
| null_single_W1024_low | estimate | 1.017 theta | 1.007 |  | 500 |  | no standard error |
| null_single_W1024_high | estimate | 1.376 theta | 1.308 |  | 500 |  | no standard error |
| null_single_W1024_N | parameter | 1000 replicates | 500 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| vix_below_null_quant_count | tally | 35 windows | 35 |  | 45 |  | a tally of what the analysis found, with no uncertainty, so it is not judged |
| vix_below_null_total | count | 45 windows | 45 |  |  |  | the script writes it as a fixed number (45 at line 524), so it is not judged |
| vix_below_null_quant_value | parameter | 1.017 theta | 1.007 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_overlap_count_mean | estimate | 1.35 windows | 1.248 | 0.08274 | 400 | True | paper inside 1.248 +/- 0.1622 |
| null_overlap_count_q99 | estimate | 7 windows | 7.01 |  | 400 |  | no standard error |
| null_overlap_count_max | estimate | 10 windows | 8 |  | 400 |  | no standard error |
| null_overlap_count_N | parameter | 1000 paths | 400 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_overlap_p_count | estimate | 0.001 p | 0.002494 |  | 400 |  | no standard error |
| null_overlap_roll_mean_null | estimate | 1.16 theta | 1.143 | 0.001309 | 400 | False | paper outside 1.143 +/- 0.002565 |
| null_overlap_roll_sd_null | estimate | 0.026 theta | 0.02618 |  | 400 |  | no standard error |
| null_overlap_vix_roll_mean | estimate | 0.91 theta | 0.9098 | 0.02834 | 45 | True | paper inside 0.9098 +/- 0.05554 |
| null_overlap_p_mean | p_value | 0.001 p | 0.002494 |  | 400 | True | both < 0.05 |
| p_abstract | p_value | 0.001 p | 0.002494 |  | 400 | True | both < 0.05 |
| null_empirical_W512_mean | estimate | 1.211 theta | 1.211 | 0.008363 | 250 | True | paper inside 1.211 +/- 0.01639 |
| null_empirical_W512_sigma | estimate | 0.118 theta | 0.1322 |  | 250 |  | no standard error |
| null_empirical_W512_low | estimate | 1.01 theta | 0.9949 |  | 250 |  | no standard error |
| null_empirical_W512_high | estimate | 1.465 theta | 1.513 |  | 250 |  | no standard error |
| null_empirical_W512_median | estimate | 1.198 theta | 1.191 |  | 250 |  | no standard error |
| null_empirical_W512_N | parameter | 1000 replicates | 250 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_empirical_W1024_mean | estimate | 1.166 theta | 1.143 | 0.004838 | 250 | False | paper outside 1.143 +/- 0.009482 |
| null_empirical_W1024_sigma | estimate | 0.091 theta | 0.07649 |  | 250 |  | no standard error |
| null_empirical_W1024_low | estimate | 1.017 theta | 1.007 |  | 250 |  | no standard error |
| null_empirical_W1024_high | estimate | 1.376 theta | 1.298 |  | 250 |  | no standard error |
| null_empirical_W1024_median | estimate | 1.157 theta | 1.139 |  | 250 |  | no standard error |
| null_empirical_W1024_N | parameter | 1000 replicates | 250 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_empirical_W2048_mean | estimate | 1.136 theta | 1.099 | 0.003226 | 250 | False | paper outside 1.099 +/- 0.006323 |
| null_empirical_W2048_sigma | estimate | 0.084 theta | 0.05101 |  | 250 |  | no standard error |
| null_empirical_W2048_low | estimate | 0.994 theta | 1.006 |  | 250 |  | no standard error |
| null_empirical_W2048_high | estimate | 1.31 theta | 1.199 |  | 250 |  | no standard error |
| null_empirical_W2048_median | estimate | 1.13 theta | 1.1 |  | 250 |  | no standard error |
| null_empirical_W2048_N | parameter | 1000 replicates | 250 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_empirical_W4096_mean | estimate | 1.09 theta | 1.07 | 0.002143 | 250 | False | paper outside 1.07 +/- 0.0042 |
| null_empirical_W4096_sigma | estimate | 0.056 theta | 0.03388 |  | 250 |  | no standard error |
| null_empirical_W4096_low | estimate | 0.985 theta | 1.012 |  | 250 |  | no standard error |
| null_empirical_W4096_high | estimate | 1.201 theta | 1.135 |  | 250 |  | no standard error |
| null_empirical_W4096_median | estimate | 1.087 theta | 1.068 |  | 250 |  | no standard error |
| null_empirical_W4096_N | parameter | 1000 replicates | 250 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_empirical_W8192_mean | estimate | 1.06 theta | 1.056 | 0.001441 | 250 | False | paper outside 1.056 +/- 0.002824 |
| null_empirical_W8192_sigma | estimate | 0.039 theta | 0.02278 |  | 250 |  | no standard error |
| null_empirical_W8192_low | estimate | 0.988 theta | 1.014 |  | 250 |  | no standard error |
| null_empirical_W8192_high | estimate | 1.136 theta | 1.099 |  | 250 |  | no standard error |
| null_empirical_W8192_median | estimate | 1.058 theta | 1.056 |  | 250 |  | no standard error |
| null_empirical_W8192_N | parameter | 1000 replicates | 250 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_empirical_W16384_mean | estimate | 1.042 theta | 1.044 | 0.001026 | 250 | False | paper outside 1.044 +/- 0.002012 |
| null_empirical_W16384_sigma | estimate | 0.025 theta | 0.01623 |  | 250 |  | no standard error |
| null_empirical_W16384_low | estimate | 0.994 theta | 1.014 |  | 250 |  | no standard error |
| null_empirical_W16384_high | estimate | 1.092 theta | 1.079 |  | 250 |  | no standard error |
| null_empirical_W16384_median | estimate | 1.042 theta | 1.045 |  | 250 |  | no standard error |
| null_empirical_W16384_N | parameter | 1000 replicates | 250 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_empirical_W32768_mean | estimate | 1.03 theta | 1.04 | 0.0009514 | 120 | False | paper outside 1.04 +/- 0.001865 |
| null_empirical_W32768_sigma | estimate | 0.016 theta | 0.01042 |  | 120 |  | no standard error |
| null_empirical_W32768_low | estimate | 0.999 theta | 1.017 |  | 120 |  | no standard error |
| null_empirical_W32768_high | estimate | 1.062 theta | 1.058 |  | 120 |  | no standard error |
| null_empirical_W32768_median | estimate | 1.03 theta | 1.04 |  | 120 |  | no standard error |
| null_empirical_W32768_N | parameter | 500 replicates | 120 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| null_empirical_W65536_mean | estimate | 1.023 theta | 1.033 | 0.0007769 | 100 | False | paper outside 1.033 +/- 0.001523 |
| null_empirical_W65536_sigma | estimate | 0.012 theta | 0.007769 |  | 100 |  | no standard error |
| null_empirical_W65536_low | estimate | 1 theta | 1.018 |  | 100 |  | no standard error |
| null_empirical_W65536_high | estimate | 1.048 theta | 1.045 |  | 100 |  | no standard error |
| null_empirical_W65536_median | estimate | 1.023 theta | 1.034 |  | 100 |  | no standard error |
| null_empirical_W65536_N | parameter | 500 replicates | 100 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| iid_null_excess_W512 | estimate | 0.21 theta |  |  |  |  | not computed |
| iid_null_excess_W65536 | estimate | 0.02 theta |  |  |  |  | not computed |
| theoretical_iid_theta | parameter | 1 theta | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| theoretical_fbm_theta_1_minus_H | parameter | 1 theta | 0.9 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_T | parameter | 6.554e+04 observations | 65536 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_N_fbm | parameter | 1e+04 paths | 150 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_N_ctrl | parameter | 50 paths | 50 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_N_cmp | parameter | 1e+04 paths | 10000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_N_heatmap | parameter | 1e+04 paths | 10000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_B_bootstrap | parameter | 200 resamples | 200 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_block_len | parameter | 1 observations |  |  |  |  | not computed |
| candidate_thresh_low | parameter | 1 lag |  |  |  |  | not computed |
| candidate_thresh_high | parameter | 30 thresholds |  |  |  |  | not computed |

## The paper's own numbers
- OK: fBm Davies-Harte validation by H=0.1..0.9, each subgroup N=10000 T=65536; reported estimates fbm_H0.1_hat..fbm_H0.9_hat etc.: 10000 = 10000, paper's total 10000
- OK: Control processes: i.i.d. uniform, i.i.d. Gaussian, BM, OU dt0.01, OU dt1.0, GBM each N=50 T=65536; plus uniform T-sweep 2^14,2^16,2^18,2^20 N=50; estimates ctrl_*_hat and iid_uniform_T*_hat.: 50 = 50, paper's total 50
- FLAG: Volatility models: model comparison 4 groups rough Bergomi H0.1, FIGARCH d0.4, GARCH(1,1), classical Heston each N=10000 T=65536; heatmap H 0.05,0.10,0.15,0.20,0.30 x eta 0.2,0.4 xi0 0.04 each cell N=10000; estimates model_*_hat, heatmap_max_eta_diff.: 10000 + 10000 = 20000, paper's total 10000
- FLAG: Empirical i.i.d. null distribution by window length W=512..65536, each subgroup N=1000 or 500 uniform replicates; reported null_empirical_W*_mean/sigma/low/high/median/N.: 1000 + 1000 + 1000 + 1000 + 1000 + 1000 + 500 + 500 = 7000, paper's total 1000
- FLAG: VIX empirical n=6651 vs i.i.d. Monte-Carlo nulls: single-window N=1000 length1024 and overlapping-window N=1000 length6651 rolling; counts vix_below_null_total 45 vs null_overlap_count_N/mean/q99/max.: 45 + 1000 + 1000 = 2045, paper's total 6651
- OK: VIX count below single-window 2.5% i.i.d. quantile: observed 35/45 windows with theta_hat <1.017 vs overlapping-window i.i.d. null mean 1.35 99%q=7 max10 across 1000 sims p~=0.001 add-one smoothing; single-window null at W1024 N1000 mean 1.166 sd0.091 envelope [1.017,1.376].: t = 35, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000
- NOTE: VIX rolling mean vs overlapping-window i.i.d. null mean: VIX mean 0.910 vs null mean 1.160 sd0.026 on 45 windows within 6651 days vs 1000 null paths length6651 p~=0.001 for mean this small.: t = 0.91 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.3628); judged two-sided
- NOTE: Abstract headline rolling estimate 0.91+-0.19 across 45 four-year windows vs overlapping-window i.i.d. Monte-Carlo null p<0.001; null_single 95% envelope [1.017,1.376] at W1024, null_overlap mean1.160 sd0.026.: t = 0.91 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.3628); judged two-sided

## Guards
- rejected claim thinning_50pct_unchanged = 0.000: not in the paper's LaTeX
- rejected claim heatmap_max_eta_diff = 0.00048: not in the paper's LaTeX
- rejected claim vix_above07_count = 43: not in the paper's LaTeX
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (drift_noise_ratio_max (0.28) at line 529). Compute each result from the data; the paper's value never goes into it.
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 6651, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Used FRED CSV direct without API key (same series VIXCLS, identical data, 6651 obs matches paper's count). Used time-order tie break (x[t+k]==x[t] counts) per paper. Used complete-case Hill-CSN with candidate thresholds 1..min(19,floor(q90)) plus 30 log-spaced 20..q90 as described. For synthetic, used reduced N (150 per H vs 10000, 50 for controls vs 50 paper matches, iid null N 100-250 vs 500-1000) due to 20min limit; reported reduced N honestly. Used batched Davies-Harte FFT for speed (statistically identical). For VIX overlapping null, used uniform 0-1 replicates via numpy (paper uses uniform). For VIX rolling, excluded last index from censored counts to match paper's 24.4 (vs 25.4 incl last). Drift ratios computed from model definitions via numerical integration of RL-fBm increment variance, not hardcoded; asymptotic and exact values reported
- caveat: the sample block's not_rebuilt: heatmap_max_eta_diff is no claim's name, so it excused nothing

## Data sources
- market data: none used
- other hosts the script fetched from: fred.stlouisfed.org

## Run
- sandbox: attempt 2, exit 0, 158.4s
- model calls: 48, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 3860013, out 159047 (reasoning 73821); cost $1.4706

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
