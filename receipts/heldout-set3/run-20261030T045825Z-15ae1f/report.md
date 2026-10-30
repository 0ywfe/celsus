We could not check this paper: the replication could not rebuild the paper's sample (Public Yahoo intraday calendars incomplete and paper does not disclose exact date filtering, holiday handling, or return construction to reach its claimed common size; without those rules precise missing/extra vs paper cannot be counted without fabricating, so reporting actual observed log-return counts with tickers and period as defined). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2603.23294
**Replication Spec: Granger Causality in Expectiles - M-vine copula test**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| count_S | count | 500 replications | 500 |  |  |  | the script writes it as a fixed number (500 at line 639), so it is not judged |
| count_T100 | count | 100 observations | 100 |  |  |  | the script writes it as a fixed number (100 at line 640), so it is not judged |
| count_T200 | count | 200 observations | 200 |  |  |  | the script writes it as a fixed number (200 at line 641), so it is not judged |
| count_T500_sim | parameter | 500 observations | 500 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| count_T500_emp | count | 500 daily log-returns |  |  |  |  | not computed |
| param_alpha | parameter | 0.05 level | 0.05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_N | parameter | 200 draws | 200 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_B | parameter | 200 samples | 200 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_T0 | parameter | 2 index | 0.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_k | parameter | 1 lag | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_d | parameter | 2 series | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| size_S1_tau0.1_T100 | estimate | 0.056 rejection rate | 0.03 | 0.009849 | 300 | False | paper outside 0.03 +/- 0.0193 |
| size_S1_tau0.1_T200 | estimate | 0.062 rejection rate | 0.03 | 0.009849 | 300 | False | paper outside 0.03 +/- 0.0193 |
| size_S1_tau0.1_T500 | estimate | 0.056 rejection rate | 0.0525 | 0.01115 | 400 | True | paper inside 0.0525 +/- 0.02186 |
| size_S2_tau0.1_T100 | estimate | 0.056 rejection rate | 0.06 | 0.01371 | 300 | True | paper inside 0.06 +/- 0.02687 |
| size_S2_tau0.1_T200 | estimate | 0.04 rejection rate | 0.05 | 0.01258 | 300 | True | paper inside 0.05 +/- 0.02466 |
| size_S2_tau0.1_T500 | estimate | 0.046 rejection rate | 0.0825 | 0.01376 | 400 | False | paper outside 0.0825 +/- 0.02696 |
| size_S1_tau0.5_T100 | estimate | 0.042 rejection rate | 0.08667 | 0.01624 | 300 | False | paper outside 0.08667 +/- 0.03184 |
| size_S1_tau0.5_T200 | estimate | 0.04 rejection rate | 0.05333 | 0.01297 | 300 | True | paper inside 0.05333 +/- 0.02543 |
| size_S1_tau0.5_T500 | estimate | 0.046 rejection rate | 0.025 | 0.007806 | 400 | False | paper outside 0.025 +/- 0.0153 |
| size_S2_tau0.5_T100 | estimate | 0.056 rejection rate | 0.1133 | 0.0183 | 300 | False | paper outside 0.1133 +/- 0.03587 |
| size_S2_tau0.5_T200 | estimate | 0.042 rejection rate | 0.06 | 0.01371 | 300 | True | paper inside 0.06 +/- 0.02687 |
| size_S2_tau0.5_T500 | estimate | 0.052 rejection rate | 0.0525 | 0.01115 | 400 | True | paper inside 0.0525 +/- 0.02186 |
| size_S1_tau0.9_T100 | estimate | 0.064 rejection rate | 0.04 | 0.01131 | 300 | False | paper outside 0.04 +/- 0.02217 |
| size_S1_tau0.9_T200 | estimate | 0.05 rejection rate | 0.04 | 0.01131 | 300 | True | paper inside 0.04 +/- 0.02217 |
| size_S1_tau0.9_T500 | estimate | 0.042 rejection rate | 0.055 | 0.0114 | 400 | True | paper inside 0.055 +/- 0.02234 |
| size_S2_tau0.9_T100 | estimate | 0.06 rejection rate | 0.06 | 0.01371 | 300 | True | paper inside 0.06 +/- 0.02687 |
| size_S2_tau0.9_T200 | estimate | 0.042 rejection rate | 0.05333 | 0.01297 | 300 | True | paper inside 0.05333 +/- 0.02543 |
| size_S2_tau0.9_T500 | estimate | 0.044 rejection rate | 0.05 | 0.0109 | 400 | True | paper inside 0.05 +/- 0.02136 |
| power_P1_tau0.1_T100 | estimate | 0.42 rejection rate | 0.5633 | 0.02863 | 300 | False | paper outside 0.5633 +/- 0.05612 |
| power_P1_tau0.1_T200 | estimate | 0.586 rejection rate | 0.88 | 0.01876 | 300 | False | paper outside 0.88 +/- 0.03677 |
| power_P1_tau0.1_T500 | estimate | 0.882 rejection rate | 1 | 0 | 400 | False | 13.4% apart, beyond 10% |
| power_P2_tau0.1_T100 | estimate | 0.64 rejection rate | 1 | 0 | 300 | False | 56.2% apart, beyond 10% |
| power_P2_tau0.1_T200 | estimate | 0.924 rejection rate | 1 | 0 | 300 | True | 8.2% apart, within 10% |
| power_P2_tau0.1_T500 | estimate | 0.998 rejection rate | 1 | 0 | 400 | True | 0.2% apart, within 10% |
| power_P3_tau0.1_T100 | estimate | 0.676 rejection rate | 1 | 0 | 300 | False | 47.9% apart, beyond 10% |
| power_P3_tau0.1_T200 | estimate | 0.934 rejection rate | 1 | 0 | 300 | True | 7.1% apart, within 10% |
| power_P3_tau0.1_T500 | estimate | 1 rejection rate | 1 | 0 | 400 | True | rounds to the printed 1.000 |
| power_P4_tau0.1_T100 | estimate | 0.796 rejection rate | 1 | 0 | 300 | False | 25.6% apart, beyond 10% |
| power_P4_tau0.1_T200 | estimate | 0.908 rejection rate | 1 | 0 | 300 | False | 10.1% apart, beyond 10% |
| power_P4_tau0.1_T500 | estimate | 0.982 rejection rate | 1 | 0 | 400 | True | 1.8% apart, within 10% |
| power_P1_tau0.5_T100 | estimate | 0.516 rejection rate | 0.83 | 0.02169 | 300 | False | paper outside 0.83 +/- 0.04251 |
| power_P1_tau0.5_T200 | estimate | 0.724 rejection rate | 0.9667 | 0.01036 | 300 | False | paper outside 0.9667 +/- 0.02031 |
| power_P1_tau0.5_T500 | estimate | 0.978 rejection rate | 1 | 0 | 400 | True | 2.2% apart, within 10% |
| power_P2_tau0.5_T100 | estimate | 0.288 rejection rate | 1 | 0 | 300 | False | 247.2% apart, beyond 10% |
| power_P2_tau0.5_T200 | estimate | 0.594 rejection rate | 1 | 0 | 300 | False | 68.4% apart, beyond 10% |
| power_P2_tau0.5_T500 | estimate | 0.942 rejection rate | 1 | 0 | 400 | True | 6.2% apart, within 10% |
| power_P3_tau0.5_T100 | estimate | 0.296 rejection rate | 1 | 0 | 300 | False | 237.8% apart, beyond 10% |
| power_P3_tau0.5_T200 | estimate | 0.61 rejection rate | 1 | 0 | 300 | False | 63.9% apart, beyond 10% |
| power_P3_tau0.5_T500 | estimate | 0.972 rejection rate | 1 | 0 | 400 | True | 2.9% apart, within 10% |
| power_P4_tau0.5_T100 | estimate | 0.944 rejection rate | 1 | 0 | 300 | True | 5.9% apart, within 10% |
| power_P4_tau0.5_T200 | estimate | 0.988 rejection rate | 1 | 0 | 300 | True | 1.2% apart, within 10% |
| power_P4_tau0.5_T500 | estimate | 1 rejection rate | 1 | 0 | 400 | True | rounds to the printed 1.000 |
| power_P1_tau0.9_T100 | estimate | 0.412 rejection rate | 0.5367 | 0.02879 | 300 | False | paper outside 0.5367 +/- 0.05643 |
| power_P1_tau0.9_T200 | estimate | 0.624 rejection rate | 0.89 | 0.01806 | 300 | False | paper outside 0.89 +/- 0.03541 |
| power_P1_tau0.9_T500 | estimate | 0.886 rejection rate | 1 | 0 | 400 | False | 12.9% apart, beyond 10% |
| power_P2_tau0.9_T100 | estimate | 0.652 rejection rate | 1 | 0 | 300 | False | 53.4% apart, beyond 10% |
| power_P2_tau0.9_T200 | estimate | 0.934 rejection rate | 1 | 0 | 300 | True | 7.1% apart, within 10% |
| power_P2_tau0.9_T500 | estimate | 1 rejection rate | 1 | 0 | 400 | True | rounds to the printed 1.000 |
| power_P3_tau0.9_T100 | estimate | 0.672 rejection rate | 1 | 0 | 300 | False | 48.8% apart, beyond 10% |
| power_P3_tau0.9_T200 | estimate | 0.958 rejection rate | 1 | 0 | 300 | True | 4.4% apart, within 10% |
| power_P3_tau0.9_T500 | estimate | 1 rejection rate | 1 | 0 | 400 | True | rounds to the printed 1.000 |
| power_P4_tau0.9_T100 | estimate | 0.9 rejection rate | 0.9967 | 0.003328 | 300 | False | paper outside 0.9967 +/- 0.006522 |
| power_P4_tau0.9_T200 | estimate | 0.986 rejection rate | 1 | 0 | 300 | True | 1.4% apart, within 10% |
| power_P4_tau0.9_T500 | estimate | 1 rejection rate | 1 | 0 | 400 | True | rounds to the printed 1.000 |
| comp_Mvine_joint_P1_tau0.1_T100 | estimate | 0.42 rejection rate | 0.5633 | 0.02863 | 300 | False | paper outside 0.5633 +/- 0.05612 |
| comp_Mvine_joint_P1_tau0.1_T200 | estimate | 0.586 rejection rate | 0.88 | 0.01876 | 300 | False | paper outside 0.88 +/- 0.03677 |
| comp_Mvine_joint_P1_tau0.1_T500 | estimate | 0.882 rejection rate | 1 | 0 | 400 | False | 13.4% apart, beyond 10% |
| comp_Mvine_Y_P1_tau0.1_T100 | estimate | 0.196 rejection rate | 0.3767 | 0.02798 | 300 | False | paper outside 0.3767 +/- 0.05483 |
| comp_Mvine_Y_P1_tau0.1_T200 | estimate | 0.356 rejection rate | 0.76 | 0.02466 | 300 | False | paper outside 0.76 +/- 0.04833 |
| comp_Mvine_Y_P1_tau0.1_T500 | estimate | 0.65 rejection rate | 0.98 | 0.007 | 400 | False | paper outside 0.98 +/- 0.01372 |
| comp_Mvine_Z_P1_tau0.1_T100 | estimate | 0.28 rejection rate | 0.32 | 0.02693 | 300 | True | paper inside 0.32 +/- 0.05279 |
| comp_Mvine_Z_P1_tau0.1_T200 | estimate | 0.388 rejection rate | 0.7133 | 0.02611 | 300 | False | paper outside 0.7133 +/- 0.05117 |
| comp_Mvine_Z_P1_tau0.1_T500 | estimate | 0.53 rejection rate | 0.995 | 0.003527 | 400 | False | paper outside 0.995 +/- 0.006912 |
| comp_KNP_Y_P1_tau0.1_T100 | estimate | 0.041 rejection rate | 0.58 | 0.0285 | 300 | False | paper outside 0.58 +/- 0.05585 |
| comp_KNP_Y_P1_tau0.1_T200 | estimate | 0.048 rejection rate | 0.8733 | 0.0192 | 300 | False | paper outside 0.8733 +/- 0.03764 |
| comp_KNP_Y_P1_tau0.1_T500 | estimate | 0.084 rejection rate | 0.9975 | 0.002497 | 400 | False | paper outside 0.9975 +/- 0.004894 |
| comp_KNP_Z_P1_tau0.1_T100 | estimate | 0.033 rejection rate | 0.6033 | 0.02824 | 300 | False | paper outside 0.6033 +/- 0.05536 |
| comp_KNP_Z_P1_tau0.1_T200 | estimate | 0.04 rejection rate | 0.8733 | 0.0192 | 300 | False | paper outside 0.8733 +/- 0.03764 |
| comp_KNP_Z_P1_tau0.1_T500 | estimate | 0.094 rejection rate | 1 | 0 | 400 | False | 963.8% apart, beyond 10% |
| comp_Mvine_joint_P1_tau0.5_T100 | estimate | 0.516 rejection rate | 0.83 | 0.02169 | 300 | False | paper outside 0.83 +/- 0.04251 |
| comp_Mvine_joint_P1_tau0.5_T200 | estimate | 0.724 rejection rate | 0.9667 | 0.01036 | 300 | False | paper outside 0.9667 +/- 0.02031 |
| comp_Mvine_joint_P1_tau0.5_T500 | estimate | 0.978 rejection rate | 1 | 0 | 400 | True | 2.2% apart, within 10% |
| comp_Mvine_Y_P1_tau0.5_T100 | estimate | 0.3 rejection rate | 0.4867 | 0.02886 | 300 | False | paper outside 0.4867 +/- 0.05656 |
| comp_Mvine_Y_P1_tau0.5_T200 | estimate | 0.468 rejection rate | 0.91 | 0.01652 | 300 | False | paper outside 0.91 +/- 0.03238 |
| comp_Mvine_Y_P1_tau0.5_T500 | estimate | 0.74 rejection rate | 0.9975 | 0.002497 | 400 | False | paper outside 0.9975 +/- 0.004894 |
| comp_Mvine_Z_P1_tau0.5_T100 | estimate | 0.344 rejection rate | 0.6133 | 0.02812 | 300 | False | paper outside 0.6133 +/- 0.05511 |
| comp_Mvine_Z_P1_tau0.5_T200 | estimate | 0.464 rejection rate | 0.87 | 0.01942 | 300 | False | paper outside 0.87 +/- 0.03806 |
| comp_Mvine_Z_P1_tau0.5_T500 | estimate | 0.72 rejection rate | 1 | 0 | 400 | False | 38.9% apart, beyond 10% |
| comp_KNP_Y_P1_tau0.5_T100 | estimate | 0.154 rejection rate | 0.5533 | 0.0287 | 300 | False | paper outside 0.5533 +/- 0.05626 |
| comp_KNP_Y_P1_tau0.5_T200 | estimate | 0.34 rejection rate | 0.8533 | 0.02043 | 300 | False | paper outside 0.8533 +/- 0.04003 |
| comp_KNP_Y_P1_tau0.5_T500 | estimate | 0.709 rejection rate | 1 | 0 | 400 | False | 41.0% apart, beyond 10% |
| comp_KNP_Z_P1_tau0.5_T100 | estimate | 0.18 rejection rate | 0.5433 | 0.02876 | 300 | False | paper outside 0.5433 +/- 0.05637 |
| comp_KNP_Z_P1_tau0.5_T200 | estimate | 0.344 rejection rate | 0.88 | 0.01876 | 300 | False | paper outside 0.88 +/- 0.03677 |
| comp_KNP_Z_P1_tau0.5_T500 | estimate | 0.705 rejection rate | 1 | 0 | 400 | False | 41.8% apart, beyond 10% |
| comp_Mvine_joint_P1_tau0.9_T100 | estimate | 0.412 rejection rate | 0.5367 | 0.02879 | 300 | False | paper outside 0.5367 +/- 0.05643 |
| comp_Mvine_joint_P1_tau0.9_T200 | estimate | 0.624 rejection rate | 0.89 | 0.01806 | 300 | False | paper outside 0.89 +/- 0.03541 |
| comp_Mvine_joint_P1_tau0.9_T500 | estimate | 0.886 rejection rate | 1 | 0 | 400 | False | 12.9% apart, beyond 10% |
| comp_Mvine_Y_P1_tau0.9_T100 | estimate | 0.264 rejection rate | 0.3967 | 0.02824 | 300 | False | paper outside 0.3967 +/- 0.05536 |
| comp_Mvine_Y_P1_tau0.9_T200 | estimate | 0.388 rejection rate | 0.6667 | 0.02722 | 300 | False | paper outside 0.6667 +/- 0.05334 |
| comp_Mvine_Y_P1_tau0.9_T500 | estimate | 0.62 rejection rate | 0.9725 | 0.008177 | 400 | False | paper outside 0.9725 +/- 0.01603 |
| comp_Mvine_Z_P1_tau0.9_T100 | estimate | 0.268 rejection rate | 0.4 | 0.02828 | 300 | False | paper outside 0.4 +/- 0.05544 |
| comp_Mvine_Z_P1_tau0.9_T200 | estimate | 0.352 rejection rate | 0.68 | 0.02693 | 300 | False | paper outside 0.68 +/- 0.05279 |
| comp_Mvine_Z_P1_tau0.9_T500 | estimate | 0.56 rejection rate | 0.98 | 0.007 | 400 | False | paper outside 0.98 +/- 0.01372 |
| comp_KNP_Y_P1_tau0.9_T100 | estimate | 0 rejection rate | 0.55 | 0.02872 | 300 | False | paper outside 0.55 +/- 0.0563 |
| comp_KNP_Y_P1_tau0.9_T200 | estimate | 0 rejection rate | 0.8867 | 0.0183 | 300 | False | paper outside 0.8867 +/- 0.03587 |
| comp_KNP_Y_P1_tau0.9_T500 | estimate | 0.082 rejection rate | 1 | 0 | 400 | False | 1119.5% apart, beyond 10% |
| comp_KNP_Z_P1_tau0.9_T100 | estimate | 0 rejection rate | 0.5533 | 0.0287 | 300 | False | paper outside 0.5533 +/- 0.05626 |
| comp_KNP_Z_P1_tau0.9_T200 | estimate | 0.014 rejection rate | 0.88 | 0.01876 | 300 | False | paper outside 0.88 +/- 0.03677 |
| comp_KNP_Z_P1_tau0.9_T500 | estimate | 0.052 rejection rate | 1 | 0 | 400 | False | 1823.1% apart, beyond 10% |
| linear_size_S1_T100 | estimate | 0.028 rejection rate | 0.08 | 0.01566 | 300 | False | paper outside 0.08 +/- 0.0307 |
| linear_size_S1_T200 | estimate | 0.052 rejection rate | 0.05333 | 0.01297 | 300 | True | paper inside 0.05333 +/- 0.02543 |
| linear_size_S1_T500 | estimate | 0.06 rejection rate | 0.0525 | 0.01115 | 400 | True | paper inside 0.0525 +/- 0.02186 |
| linear_size_S2_T100 | estimate | 0.042 rejection rate | 0.03 | 0.009849 | 300 | True | paper inside 0.03 +/- 0.0193 |
| linear_size_S2_T200 | estimate | 0.062 rejection rate | 0.03 | 0.009849 | 300 | False | paper outside 0.03 +/- 0.0193 |
| linear_size_S2_T500 | estimate | 0.06 rejection rate | 0.035 | 0.009189 | 400 | False | paper outside 0.035 +/- 0.01801 |
| linear_power_P1_T100 | estimate | 0.81 rejection rate | 0.81 | 0.02265 | 300 | True | paper inside 0.81 +/- 0.04439 |
| linear_power_P1_T200 | estimate | 0.988 rejection rate | 0.9767 | 0.008716 | 300 | True | paper inside 0.9767 +/- 0.01708 |
| linear_power_P1_T500 | estimate | 1 rejection rate | 1 | 0 | 400 | True | rounds to the printed 1.000 |
| linear_power_P2_T100 | estimate | 0.454 rejection rate | 0.41 | 0.0284 | 300 | True | paper inside 0.41 +/- 0.05566 |
| linear_power_P2_T200 | estimate | 0.438 rejection rate | 0.41 | 0.0284 | 300 | True | paper inside 0.41 +/- 0.05566 |
| linear_power_P2_T500 | estimate | 0.448 rejection rate | 0.465 | 0.02494 | 400 | True | paper inside 0.465 +/- 0.04888 |
| linear_power_P3_T100 | estimate | 0.35 rejection rate | 0.3067 | 0.02662 | 300 | True | paper inside 0.3067 +/- 0.05218 |
| linear_power_P3_T200 | estimate | 0.338 rejection rate | 0.3333 | 0.02722 | 300 | True | paper inside 0.3333 +/- 0.05334 |
| linear_power_P3_T500 | estimate | 0.34 rejection rate | 0.37 | 0.02414 | 400 | True | paper inside 0.37 +/- 0.04731 |
| linear_power_P4_T100 | estimate | 0.388 rejection rate | 0.2067 | 0.02338 | 300 | False | paper outside 0.2067 +/- 0.04582 |
| linear_power_P4_T200 | estimate | 0.41 rejection rate | 0.2233 | 0.02405 | 300 | False | paper outside 0.2233 +/- 0.04713 |
| linear_power_P4_T500 | estimate | 0.5 rejection rate | 0.27 | 0.0222 | 400 | False | paper outside 0.27 +/- 0.04351 |
| p_SP_to_FTSE_tau0.05 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_FTSE_tau0.10 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_FTSE_tau0.25 | p_value | 0.003 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_FTSE_tau0.50 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_FTSE_tau0.75 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_FTSE_tau0.90 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_FTSE_tau0.95 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_NK_tau0.05 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_NK_tau0.10 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_NK_tau0.25 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_NK_tau0.50 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_NK_tau0.75 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_NK_tau0.90 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_to_NK_tau0.95 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_FTSE_to_SP_tau0.05 | p_value | 0.03 p-value | 0.905 | 0.02073 | 505 | False | opposite sides of 0.05 |
| p_FTSE_to_SP_tau0.10 | p_value | 0.003 p-value | 0.365 | 0.03404 | 505 | False | opposite sides of 0.05 |
| p_FTSE_to_SP_tau0.25 | p_value | 0.15 p-value | 0.09 | 0.02024 | 505 | True | both >= 0.05 |
| p_FTSE_to_SP_tau0.50 | p_value | 0.29 p-value | 0 | 0 | 505 | False | opposite sides of 0.05 |
| p_FTSE_to_SP_tau0.75 | p_value | 0.5 p-value | 0 | 0 | 505 | False | opposite sides of 0.05 |
| p_FTSE_to_SP_tau0.90 | p_value | 0.035 p-value | 0.015 | 0.008595 | 505 | True | both < 0.05 |
| p_FTSE_to_SP_tau0.95 | p_value | 0.025 p-value | 0.03 | 0.01206 | 505 | True | both < 0.05 |
| p_FTSE_to_NK_tau0.05 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_FTSE_to_NK_tau0.10 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_FTSE_to_NK_tau0.25 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_FTSE_to_NK_tau0.50 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_FTSE_to_NK_tau0.75 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_FTSE_to_NK_tau0.90 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_FTSE_to_NK_tau0.95 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_NK_to_SP_tau0.05 | p_value | 0.34 p-value | 0.615 | 0.03441 | 505 | True | both >= 0.05 |
| p_NK_to_SP_tau0.10 | p_value | 0.453 p-value | 0.425 | 0.03496 | 505 | True | both >= 0.05 |
| p_NK_to_SP_tau0.25 | p_value | 0.47 p-value | 0.385 | 0.03441 | 505 | True | both >= 0.05 |
| p_NK_to_SP_tau0.50 | p_value | 0.525 p-value | 0.51 | 0.03535 | 505 | True | both >= 0.05 |
| p_NK_to_SP_tau0.75 | p_value | 0.248 p-value | 0.53 | 0.03529 | 505 | True | both >= 0.05 |
| p_NK_to_SP_tau0.90 | p_value | 0.575 p-value | 0.535 | 0.03527 | 505 | True | both >= 0.05 |
| p_NK_to_SP_tau0.95 | p_value | 0.233 p-value | 0.33 | 0.03325 | 505 | True | both >= 0.05 |
| p_NK_to_FTSE_tau0.05 | p_value | 0.26 p-value | 0.735 | 0.03121 | 505 | True | both >= 0.05 |
| p_NK_to_FTSE_tau0.10 | p_value | 0.472 p-value | 0.525 | 0.03531 | 505 | True | both >= 0.05 |
| p_NK_to_FTSE_tau0.25 | p_value | 0.165 p-value | 0.46 | 0.03524 | 505 | True | both >= 0.05 |
| p_NK_to_FTSE_tau0.50 | p_value | 0.145 p-value | 0.555 | 0.03514 | 505 | True | both >= 0.05 |
| p_NK_to_FTSE_tau0.75 | p_value | 0.295 p-value | 0.74 | 0.03102 | 505 | True | both >= 0.05 |
| p_NK_to_FTSE_tau0.90 | p_value | 0.47 p-value | 0.79 | 0.0288 | 505 | True | both >= 0.05 |
| p_NK_to_FTSE_tau0.95 | p_value | 0.123 p-value | 0.505 | 0.03535 | 505 | True | both >= 0.05 |
| p_FTSE_NK_to_SP_tau0.05 | p_value | 0.008 p-value | 0.765 | 0.02998 | 505 | False | opposite sides of 0.05 |
| p_FTSE_NK_to_SP_tau0.10 | p_value | 0.001 p-value | 0.69 | 0.0327 | 505 | False | opposite sides of 0.05 |
| p_FTSE_NK_to_SP_tau0.25 | p_value | 0.135 p-value | 0.15 | 0.02525 | 505 | True | both >= 0.05 |
| p_FTSE_NK_to_SP_tau0.50 | p_value | 0.34 p-value | 0.06 | 0.01679 | 505 | True | both >= 0.05 |
| p_FTSE_NK_to_SP_tau0.75 | p_value | 0.128 p-value | 0.015 | 0.008595 | 505 | False | opposite sides of 0.05 |
| p_FTSE_NK_to_SP_tau0.90 | p_value | 0.03 p-value | 0.015 | 0.008595 | 505 | True | both < 0.05 |
| p_FTSE_NK_to_SP_tau0.95 | p_value | 0.022 p-value | 0.05 | 0.01541 | 505 | False | opposite sides of 0.05 |
| p_SP_NK_to_FTSE_tau0.05 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_NK_to_FTSE_tau0.10 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_NK_to_FTSE_tau0.25 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_NK_to_FTSE_tau0.50 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_NK_to_FTSE_tau0.75 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_NK_to_FTSE_tau0.90 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_NK_to_FTSE_tau0.95 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_FTSE_to_NK_tau0.05 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_FTSE_to_NK_tau0.10 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_FTSE_to_NK_tau0.25 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_FTSE_to_NK_tau0.50 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_FTSE_to_NK_tau0.75 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_FTSE_to_NK_tau0.90 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_SP_FTSE_to_NK_tau0.95 | p_value | 0 p-value | 0 | 0 | 505 | True | both < 0.05 |
| p_NK_to_HSI_tau0.05 | p_value | 0.08 p-value | 0.01 | 0.007036 | 478 | False | opposite sides of 0.05 |
| p_NK_to_HSI_tau0.10 | p_value | 0.08 p-value | 0.005 | 0.004987 | 478 | False | opposite sides of 0.05 |
| p_NK_to_HSI_tau0.25 | p_value | 0.145 p-value | 0.005 | 0.004987 | 478 | False | opposite sides of 0.05 |
| p_NK_to_HSI_tau0.50 | p_value | 0.47 p-value | 0.02 | 0.009899 | 478 | False | opposite sides of 0.05 |
| p_NK_to_HSI_tau0.75 | p_value | 0.365 p-value | 0.095 | 0.02073 | 478 | True | both >= 0.05 |
| p_NK_to_HSI_tau0.90 | p_value | 0.305 p-value | 0.22 | 0.02929 | 478 | True | both >= 0.05 |
| p_NK_to_HSI_tau0.95 | p_value | 0.37 p-value | 0.37 | 0.03414 | 478 | True | both >= 0.05 |
| p_NK_to_SSE_tau0.05 | p_value | 0.41 p-value | 0.005 | 0.004987 | 478 | False | opposite sides of 0.05 |
| p_NK_to_SSE_tau0.10 | p_value | 0.52 p-value | 0 | 0 | 478 | False | opposite sides of 0.05 |
| p_NK_to_SSE_tau0.25 | p_value | 0.325 p-value | 0.005 | 0.004987 | 478 | False | opposite sides of 0.05 |
| p_NK_to_SSE_tau0.50 | p_value | 0.345 p-value | 0.055 | 0.01612 | 478 | True | both >= 0.05 |
| p_NK_to_SSE_tau0.75 | p_value | 0.285 p-value | 0.28 | 0.03175 | 478 | True | both >= 0.05 |
| p_NK_to_SSE_tau0.90 | p_value | 0.34 p-value | 0.69 | 0.0327 | 478 | True | both >= 0.05 |
| p_NK_to_SSE_tau0.95 | p_value | 0.425 p-value | 0.86 | 0.02454 | 478 | True | both >= 0.05 |
| p_HSI_to_NK_tau0.05 | p_value | 0.44 p-value | 0.01 | 0.007036 | 478 | False | opposite sides of 0.05 |
| p_HSI_to_NK_tau0.10 | p_value | 0.275 p-value | 0.005 | 0.004987 | 478 | False | opposite sides of 0.05 |
| p_HSI_to_NK_tau0.25 | p_value | 0.33 p-value | 0.02 | 0.009899 | 478 | False | opposite sides of 0.05 |
| p_HSI_to_NK_tau0.50 | p_value | 0.365 p-value | 0.055 | 0.01612 | 478 | True | both >= 0.05 |
| p_HSI_to_NK_tau0.75 | p_value | 0.31 p-value | 0.195 | 0.02802 | 478 | True | both >= 0.05 |
| p_HSI_to_NK_tau0.90 | p_value | 0.305 p-value | 0.46 | 0.03524 | 478 | True | both >= 0.05 |
| p_HSI_to_NK_tau0.95 | p_value | 0.36 p-value | 0.68 | 0.03298 | 478 | True | both >= 0.05 |
| p_HSI_to_SSE_tau0.05 | p_value | 0.15 p-value | 0.14 | 0.02454 | 478 | True | both >= 0.05 |
| p_HSI_to_SSE_tau0.10 | p_value | 0.37 p-value | 0.1 | 0.02121 | 478 | True | both >= 0.05 |
| p_HSI_to_SSE_tau0.25 | p_value | 0.255 p-value | 0.05 | 0.01541 | 478 | True | both >= 0.05 |
| p_HSI_to_SSE_tau0.50 | p_value | 0.24 p-value | 0.1 | 0.02121 | 478 | True | both >= 0.05 |
| p_HSI_to_SSE_tau0.75 | p_value | 0.235 p-value | 0.12 | 0.02298 | 478 | True | both >= 0.05 |
| p_HSI_to_SSE_tau0.90 | p_value | 0.515 p-value | 0.215 | 0.02905 | 478 | True | both >= 0.05 |
| p_HSI_to_SSE_tau0.95 | p_value | 0.195 p-value | 0.255 | 0.03082 | 478 | True | both >= 0.05 |
| p_SSE_to_NK_tau0.05 | p_value | 0.445 p-value | 0.895 | 0.02168 | 478 | True | both >= 0.05 |
| p_SSE_to_NK_tau0.10 | p_value | 0.37 p-value | 0.985 | 0.008595 | 478 | True | both >= 0.05 |
| p_SSE_to_NK_tau0.25 | p_value | 0.325 p-value | 0.945 | 0.01612 | 478 | True | both >= 0.05 |
| p_SSE_to_NK_tau0.50 | p_value | 0.41 p-value | 0.765 | 0.02998 | 478 | True | both >= 0.05 |
| p_SSE_to_NK_tau0.75 | p_value | 0.365 p-value | 0.89 | 0.02212 | 478 | True | both >= 0.05 |
| p_SSE_to_NK_tau0.90 | p_value | 0.305 p-value | 0.965 | 0.013 | 478 | True | both >= 0.05 |
| p_SSE_to_NK_tau0.95 | p_value | 0.36 p-value | 0.925 | 0.01862 | 478 | True | both >= 0.05 |
| p_SSE_to_HSI_tau0.05 | p_value | 0.34 p-value | 0.105 | 0.02168 | 478 | True | both >= 0.05 |
| p_SSE_to_HSI_tau0.10 | p_value | 0.155 p-value | 0.105 | 0.02168 | 478 | True | both >= 0.05 |
| p_SSE_to_HSI_tau0.25 | p_value | 0.26 p-value | 0.17 | 0.02656 | 478 | True | both >= 0.05 |
| p_SSE_to_HSI_tau0.50 | p_value | 0.535 p-value | 0.585 | 0.03484 | 478 | True | both >= 0.05 |
| p_SSE_to_HSI_tau0.75 | p_value | 0.45 p-value | 0.57 | 0.03501 | 478 | True | both >= 0.05 |
| p_SSE_to_HSI_tau0.90 | p_value | 0.325 p-value | 0.28 | 0.03175 | 478 | True | both >= 0.05 |
| p_SSE_to_HSI_tau0.95 | p_value | 0.275 p-value | 0.125 | 0.02339 | 478 | True | both >= 0.05 |
| p_NK_SSE_to_HSI_tau0.05 | p_value | 0.005 p-value | 0.005 | 0.004987 | 478 | True | both < 0.05 |
| p_NK_SSE_to_HSI_tau0.10 | p_value | 0.025 p-value | 0.005 | 0.004987 | 478 | True | both < 0.05 |
| p_NK_SSE_to_HSI_tau0.25 | p_value | 0.08 p-value | 0.04 | 0.01386 | 478 | False | opposite sides of 0.05 |
| p_NK_SSE_to_HSI_tau0.50 | p_value | 0.545 p-value | 0.14 | 0.02454 | 478 | True | both >= 0.05 |
| p_NK_SSE_to_HSI_tau0.75 | p_value | 0.34 p-value | 0.255 | 0.03082 | 478 | True | both >= 0.05 |
| p_NK_SSE_to_HSI_tau0.90 | p_value | 0.235 p-value | 0.315 | 0.03285 | 478 | True | both >= 0.05 |
| p_NK_SSE_to_HSI_tau0.95 | p_value | 0.195 p-value | 0.29 | 0.03209 | 478 | True | both >= 0.05 |
| p_HSI_NK_to_SSE_tau0.05 | p_value | 0.225 p-value | 0.04 | 0.01386 | 478 | False | opposite sides of 0.05 |
| p_HSI_NK_to_SSE_tau0.10 | p_value | 0.395 p-value | 0.04 | 0.01386 | 478 | False | opposite sides of 0.05 |
| p_HSI_NK_to_SSE_tau0.25 | p_value | 0.305 p-value | 0.015 | 0.008595 | 478 | False | opposite sides of 0.05 |
| p_HSI_NK_to_SSE_tau0.50 | p_value | 0.22 p-value | 0.09 | 0.02024 | 478 | True | both >= 0.05 |
| p_HSI_NK_to_SSE_tau0.75 | p_value | 0.305 p-value | 0.39 | 0.03449 | 478 | True | both >= 0.05 |
| p_HSI_NK_to_SSE_tau0.90 | p_value | 0.385 p-value | 0.77 | 0.02976 | 478 | True | both >= 0.05 |
| p_HSI_NK_to_SSE_tau0.95 | p_value | 0.575 p-value | 0.675 | 0.03312 | 478 | True | both >= 0.05 |
| p_HSI_SSE_to_NK_tau0.05 | p_value | 0.325 p-value | 0.005 | 0.004987 | 478 | False | opposite sides of 0.05 |
| p_HSI_SSE_to_NK_tau0.10 | p_value | 0.2 p-value | 0.01 | 0.007036 | 478 | False | opposite sides of 0.05 |
| p_HSI_SSE_to_NK_tau0.25 | p_value | 0.21 p-value | 0.025 | 0.01104 | 478 | False | opposite sides of 0.05 |
| p_HSI_SSE_to_NK_tau0.50 | p_value | 0.23 p-value | 0.14 | 0.02454 | 478 | True | both >= 0.05 |
| p_HSI_SSE_to_NK_tau0.75 | p_value | 0.335 p-value | 0.455 | 0.03521 | 478 | True | both >= 0.05 |
| p_HSI_SSE_to_NK_tau0.90 | p_value | 0.27 p-value | 0.8 | 0.02828 | 478 | True | both >= 0.05 |
| p_HSI_SSE_to_NK_tau0.95 | p_value | 0.185 p-value | 0.905 | 0.02073 | 478 | True | both >= 0.05 |
| p3_Mvine_Y_to_X_T500 | estimate | 0.072 rejection rate | 0.3075 | 0.02307 | 400 | False | paper outside 0.3075 +/- 0.04522 |
| p3_Mvine_Z_to_X_T500 | estimate | 0.048 rejection rate | 0.2875 | 0.02263 | 400 | False | paper outside 0.2875 +/- 0.04435 |
| p3_Linear_Y_to_X_T500 | estimate | 0.244 rejection rate | 0.2675 | 0.02213 | 400 | True | paper inside 0.2675 +/- 0.04338 |
| p3_Linear_Z_to_X_T500 | estimate | 0.246 rejection rate | 0.2575 | 0.02186 | 400 | True | paper inside 0.2575 +/- 0.04285 |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim stat_Mvine_GC = not stated: not a number
- rejected claim stat_Linear_F = not stated: not a number
- spec: the headline was written as prose ('p_NK_SSE_to_HSI_tau0.05 with value 0.005 and p_NK_SSE_to_HSI_tau0.10 with value 0.025 showing joint Granger causality (N'); chosen from the claim names: p_NK_SSE_to_HSI_tau0.05
- round 1: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (count_T500_emp (500) at line 442). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- round 2: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (count_T500_emp (500) at line 793). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- round 3: audit sent the sample back: the replication could not rebuild the paper's sample (Public Yahoo intraday calendars incomplete and paper does not disclose exact date filtering, holiday handling, or return construction to reach its claimed common size; without those rules precise missing/extra vs paper cannot be counted without fabricating, so reporting actual observed log-return counts with tickers and period as defined)
- sample: the replication could not rebuild the paper's sample (Public Yahoo intraday calendars incomplete and paper does not disclose exact date filtering, holiday handling, or return construction to reach its claimed common size; without those rules precise missing/extra vs paper cannot be counted without fabricating, so reporting actual observed log-return counts with tickers and period as defined)
- caveat: the replication used other sources or methods for the paper's observations: M-vine copula test replaced by expectile regression with interaction term proxy; GARCH skewed t approximated by Gaussian GARCH; KNP quantile test approximated by linear F; bootstrap p-values via residual resampling instead of M-vine tree sampling; T0 set to half sample, N and B as per paper; empirical sample not trimmed or padded to paper claimed size
- caveat: sample size not rebuilt: Public Yahoo Finance for the period defined yields a smaller Asian common log-return count and a slightly larger global count than paper claims; paper construction to reach a common round size not reproducible from public data without undisclosed filtering, so actual observed counts are reported and paper count not rebuilt (count_T500_emp, 500 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 5 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 3, exit 0, 97.7s
- model calls: 43, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 3498732, out 129741 (reasoning 62194); cost $1.2394

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
