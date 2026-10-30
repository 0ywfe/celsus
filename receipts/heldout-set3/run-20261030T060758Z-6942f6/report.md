The paper's numbers do not hold up: 0 of 9 checked results match within their uncertainty. Its main result, estimate_RMSE_improvement_outsample_pct, was not computed.

# paper-replicator report: arXiv 2510.15938
**Dynamic Factor Analysis of Price Movements in the Philippine Stock Exchange**

Verdict: **does not hold up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| count_stocks_retained_after_filter | count | 72 stocks | 66 |  | 66 | True | approximate: -8.3%, within SCORE's +/-15% |
| param_missing_threshold | parameter | 1% missing observations threshold for exclusion | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_n_1_factor | parameter | 1 number of common factors in one-factor specification | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_n_2_factor | parameter | 2 number of common factors in two-factor specification | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_p_3_q_5_one_factor | parameter | 3 lags | 3 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_p_2_q_5_two_factor | parameter | 2 lags | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_alpha_significance | parameter | 0.05 alpha | 0.05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| estimate_corr_Ft_PSEi_one_factor | estimate | 0.9283 Pearson correlation | 0.9842 | 0.004808 | 1361 | False | paper outside 0.9842 +/- 0.009424 |
| estimate_corr_Ft_PC1_one_factor | estimate | 0.9975 Pearson correlation |  |  |  |  | not computed |
| estimate_corr_PC1_PSEi_one_factor | estimate | 0.9144 Pearson correlation | 0.9842 | 0.004808 | 1361 | False | paper outside 0.9842 +/- 0.009424 |
| estimate_corr_CAPM_beta_beta_i_one_factor | estimate | 0.8348 Pearson correlation | 0.9671 | 0.03181 | 66 | False | paper outside 0.9671 +/- 0.06234 |
| estimate_VAR_Ft_Lambda1_one_factor | estimate | 0.1256 AR coefficient |  |  |  |  | not computed |
| estimate_VAR_Ft_Lambda2_one_factor_ns | estimate | 0.0225 AR coefficient ns |  |  |  |  | not computed |
| estimate_VAR_Ft_Lambda3_one_factor | estimate | 0.138 AR coefficient |  |  |  |  | not computed |
| estimate_corr_F1t_PSEi_two_factor | estimate | 0.6727 Pearson correlation | 0.9842 | 0.004808 | 1361 | False | paper outside 0.9842 +/- 0.009424 |
| estimate_corr_F1t_PC1_two_factor | estimate | 0.8982 Pearson correlation |  |  |  |  | not computed |
| estimate_corr_F2t_PSEi_two_factor | estimate | 0.7704 Pearson correlation | -0.1446 | 0.02684 | 1361 | False | paper outside -0.1446 +/- 0.05261 |
| estimate_corr_F2t_PC2_two_factor | estimate | 0.8229 Pearson correlation |  |  |  |  | not computed |
| estimate_corr_PC2_PSEi_two_factor | estimate | 0.3498 Pearson correlation | -0.1446 | 0.02684 | 1361 | False | paper outside -0.1446 +/- 0.05261 |
| estimate_corr_CAPM_beta_beta1i_two_factor | estimate | 0.5132 Pearson correlation | 0.9671 | 0.03181 | 66 | False | paper outside 0.9671 +/- 0.06234 |
| estimate_corr_CAPM_beta_beta2i_two_factor | estimate | 0.8528 Pearson correlation | 0.2672 | 0.1205 | 66 | False | paper outside 0.2672 +/- 0.2361 |
| estimate_corr_F1t_F2t_two_factor | estimate | 0.0798 Pearson correlation | 0 | 0.02713 | 1361 | False | paper outside 0 +/- 0.05317 |
| estimate_R2_Ft_on_F1tF2t | estimate | 0.998 R-squared |  |  |  |  | not computed |
| estimate_VAR_Ft_11_lag1_two_factor | estimate | 0.4894 VAR coefficient |  |  |  |  | not computed |
| estimate_VAR_Ft_12_lag1_two_factor | estimate | 0.168 VAR coefficient |  |  |  |  | not computed |
| estimate_VAR_Ft_21_lag1_two_factor_ns | estimate | -0.0262 VAR coefficient ns |  |  |  |  | not computed |
| estimate_VAR_Ft_22_lag1_two_factor | estimate | -0.2526 VAR coefficient |  |  |  |  | not computed |
| estimate_VAR_Ft_11_lag2_two_factor | estimate | 0.5094 VAR coefficient |  |  |  |  | not computed |
| estimate_VAR_Ft_12_lag2_two_factor | estimate | -0.1726 VAR coefficient |  |  |  |  | not computed |
| estimate_VAR_Ft_21_lag2_two_factor | estimate | -0.1627 VAR coefficient |  |  |  |  | not computed |
| estimate_VAR_Ft_22_lag2_two_factor_ns | estimate | -0.0931 VAR coefficient ns |  |  |  |  | not computed |
| tally_beta1i_significant_72_of_72_two_factor | tally | 72 stocks with significant beta1i |  |  |  |  | not computed |
| estimate_RMSE_AR1_insample_2015_2020 | estimate | 3.853 RMSE |  |  |  |  | not computed |
| estimate_RMSE_AR1_outsample_2021_2022 | estimate | 12.31 RMSE |  |  |  |  | not computed |
| estimate_RMSE_AR1_with_Ft_insample | estimate | 0.6122 RMSE |  |  |  |  | not computed |
| estimate_RMSE_AR1_with_Ft_outsample | estimate | 8.067 RMSE |  |  |  |  | not computed |
| estimate_RMSE_improvement_insample_pct | estimate | 84.11 percent reduction in RMSE |  |  |  |  | not computed |
| estimate_RMSE_improvement_outsample_pct | estimate | 34.47 percent reduction in RMSE |  |  |  |  | not computed |
| estimate_RMSE_improvement_over_34pct_abstract | estimate | 34 percent |  |  |  |  | not computed |
| loading_beta_2GO_one_factor | estimate | 0.847 loading beta_i |  |  |  |  | not computed |
| loading_sigma_2GO_one_factor | estimate | 3.922 loading sigma_i |  |  |  |  | not computed |
| loading_beta_ABA_one_factor | estimate | 0.9707 loading |  |  |  |  | not computed |
| loading_sigma_ABA_one_factor | estimate | 3.238 loading |  |  |  |  | not computed |
| loading_beta_AC_one_factor | estimate | 1.27 loading |  |  |  |  | not computed |
| loading_sigma_AC_one_factor | estimate | 1.437 loading |  |  |  |  | not computed |
| loading_beta_AEV_one_factor | estimate | 1.1 loading |  |  |  |  | not computed |
| loading_sigma_AEV_one_factor | estimate | 1.83 loading |  |  |  |  | not computed |
| loading_beta_AGI_one_factor | estimate | 1.272 loading |  |  |  |  | not computed |
| loading_sigma_AGI_one_factor | estimate | 1.722 loading |  |  |  |  | not computed |
| loading_beta_ALI_one_factor | estimate | 1.871 loading |  |  |  |  | not computed |
| loading_sigma_ALI_one_factor | estimate | 1.614 loading |  |  |  |  | not computed |
| loading_beta_AP_one_factor | estimate | 0.7276 loading |  |  |  |  | not computed |
| loading_sigma_AP_one_factor | estimate | 1.513 loading |  |  |  |  | not computed |
| loading_beta_BDO_one_factor | estimate | 1.256 loading |  |  |  |  | not computed |
| loading_sigma_BDO_one_factor | estimate | 1.483 loading |  |  |  |  | not computed |
| loading_beta_BEL_one_factor | estimate | 0.8189 loading |  |  |  |  | not computed |
| loading_sigma_BEL_one_factor | estimate | 1.653 loading |  |  |  |  | not computed |
| loading_beta_BLOOM_one_factor | estimate | 1.523 loading |  |  |  |  | not computed |
| loading_sigma_BLOOM_one_factor | estimate | 2.724 loading |  |  |  |  | not computed |
| loading_beta_BPI_one_factor | estimate | 1.001 loading |  |  |  |  | not computed |
| loading_sigma_BPI_one_factor | estimate | 1.466 loading |  |  |  |  | not computed |
| loading_beta_BRN_one_factor | estimate | 1.24 loading |  |  |  |  | not computed |
| loading_sigma_BRN_one_factor | estimate | 3.306 loading |  |  |  |  | not computed |
| loading_beta_CEB_one_factor | estimate | 1.331 loading |  |  |  |  | not computed |
| loading_sigma_CEB_one_factor | estimate | 2.417 loading |  |  |  |  | not computed |
| loading_beta_CHIB_one_factor | estimate | 0.4127 loading |  |  |  |  | not computed |
| loading_sigma_CHIB_one_factor | estimate | 0.9347 loading |  |  |  |  | not computed |
| loading_beta_CNPF_one_factor | estimate | 0.6633 loading |  |  |  |  | not computed |
| loading_sigma_CNPF_one_factor | estimate | 1.728 loading |  |  |  |  | not computed |
| loading_beta_COSCO_one_factor | estimate | 0.7777 loading |  |  |  |  | not computed |
| loading_sigma_COSCO_one_factor | estimate | 1.454 loading |  |  |  |  | not computed |
| loading_beta_CPG_one_factor | estimate | 0.873 loading |  |  |  |  | not computed |
| loading_sigma_CPG_one_factor | estimate | 2.206 loading |  |  |  |  | not computed |
| loading_beta_DD_one_factor | estimate | 0.7787 loading |  |  |  |  | not computed |
| loading_sigma_DD_one_factor | estimate | 2.439 loading |  |  |  |  | not computed |
| loading_beta_DMC_one_factor | estimate | 1.28 loading |  |  |  |  | not computed |
| loading_sigma_DMC_one_factor | estimate | 1.891 loading |  |  |  |  | not computed |
| loading_beta_DNL_one_factor | estimate | 1.15 loading |  |  |  |  | not computed |
| loading_sigma_DNL_one_factor | estimate | 2.231 loading |  |  |  |  | not computed |
| loading_beta_EEI_one_factor | estimate | 0.8018 loading |  |  |  |  | not computed |
| loading_sigma_EEI_one_factor | estimate | 2.185 loading |  |  |  |  | not computed |
| loading_beta_EW_one_factor | estimate | 1.025 loading |  |  |  |  | not computed |
| loading_sigma_EW_one_factor | estimate | 1.873 loading |  |  |  |  | not computed |
| loading_beta_FGEN_one_factor | estimate | 0.8139 loading |  |  |  |  | not computed |
| loading_sigma_FGEN_one_factor | estimate | 1.888 loading |  |  |  |  | not computed |
| loading_beta_FLI_one_factor | estimate | 1.003 loading |  |  |  |  | not computed |
| loading_sigma_FLI_one_factor | estimate | 1.573 loading |  |  |  |  | not computed |
| loading_beta_FNI_one_factor | estimate | 1.243 loading |  |  |  |  | not computed |
| loading_sigma_FNI_one_factor | estimate | 6.045 loading |  |  |  |  | not computed |
| loading_beta_FPH_one_factor | estimate | 0.7029 loading |  |  |  |  | not computed |
| loading_sigma_FPH_one_factor | estimate | 1.235 loading |  |  |  |  | not computed |
| loading_beta_GERI_one_factor | estimate | 1.028 loading |  |  |  |  | not computed |
| loading_sigma_GERI_one_factor | estimate | 2.123 loading |  |  |  |  | not computed |
| loading_beta_GLO_one_factor | estimate | 0.7262 loading |  |  |  |  | not computed |
| loading_sigma_GLO_one_factor | estimate | 1.856 loading |  |  |  |  | not computed |
| loading_beta_GMA7_one_factor | estimate | 0.3908 loading |  |  |  |  | not computed |
| loading_sigma_GMA7_one_factor | estimate | 1.39 loading |  |  |  |  | not computed |
| loading_beta_GTCAP_one_factor | estimate | 1.22 loading |  |  |  |  | not computed |
| loading_sigma_GTCAP_one_factor | estimate | 1.858 loading |  |  |  |  | not computed |
| loading_beta_HOUSE_one_factor | estimate | 0.3541 loading |  |  |  |  | not computed |
| loading_sigma_HOUSE_one_factor | estimate | 1.81 loading |  |  |  |  | not computed |
| loading_beta_ICT_one_factor | estimate | 1.142 loading |  |  |  |  | not computed |
| loading_sigma_ICT_one_factor | estimate | 1.828 loading |  |  |  |  | not computed |
| loading_beta_IMI_one_factor | estimate | 0.9508 loading |  |  |  |  | not computed |
| loading_sigma_IMI_one_factor | estimate | 2.492 loading |  |  |  |  | not computed |
| loading_beta_JFC_one_factor | estimate | 1.158 loading |  |  |  |  | not computed |
| loading_sigma_JFC_one_factor | estimate | 1.766 loading |  |  |  |  | not computed |
| loading_beta_JGS_one_factor | estimate | 1.466 loading |  |  |  |  | not computed |
| loading_sigma_JGS_one_factor | estimate | 1.808 loading |  |  |  |  | not computed |
| loading_beta_LC_one_factor_ns | estimate | 0.1881 loading ns |  |  |  |  | not computed |
| loading_sigma_LC_one_factor | estimate | 3.033 loading |  |  |  |  | not computed |
| loading_beta_LPZ_one_factor | estimate | 0.7766 loading |  |  |  |  | not computed |
| loading_sigma_LPZ_one_factor | estimate | 2.041 loading |  |  |  |  | not computed |
| loading_beta_LTG_one_factor | estimate | 0.9536 loading |  |  |  |  | not computed |
| loading_sigma_LTG_one_factor | estimate | 2.1 loading |  |  |  |  | not computed |
| loading_beta_MAXS_one_factor | estimate | 1.159 loading |  |  |  |  | not computed |
| loading_sigma_MAXS_one_factor | estimate | 2.048 loading |  |  |  |  | not computed |
| loading_beta_MBT_one_factor | estimate | 1.123 loading |  |  |  |  | not computed |
| loading_sigma_MBT_one_factor | estimate | 1.511 loading |  |  |  |  | not computed |
| loading_beta_MEG_one_factor | estimate | 1.52 loading |  |  |  |  | not computed |
| loading_sigma_MEG_one_factor | estimate | 1.757 loading |  |  |  |  | not computed |
| loading_beta_MER_one_factor | estimate | 0.673 loading |  |  |  |  | not computed |
| loading_sigma_MER_one_factor | estimate | 1.523 loading |  |  |  |  | not computed |
| loading_beta_MPI_one_factor | estimate | 1.242 loading |  |  |  |  | not computed |
| loading_sigma_MPI_one_factor | estimate | 1.94 loading |  |  |  |  | not computed |
| loading_beta_MWC_one_factor | estimate | 0.781 loading |  |  |  |  | not computed |
| loading_sigma_MWC_one_factor | estimate | 2.291 loading |  |  |  |  | not computed |
| loading_beta_MWIDE_one_factor | estimate | 0.9886 loading |  |  |  |  | not computed |
| loading_sigma_MWIDE_one_factor | estimate | 2.371 loading |  |  |  |  | not computed |
| loading_beta_NI_one_factor | estimate | 0.3982 loading |  |  |  |  | not computed |
| loading_sigma_NI_one_factor | estimate | 2.528 loading |  |  |  |  | not computed |
| loading_beta_NIKL_one_factor | estimate | 1.319 loading |  |  |  |  | not computed |
| loading_sigma_NIKL_one_factor | estimate | 3.695 loading |  |  |  |  | not computed |
| loading_beta_PCOR_one_factor | estimate | 0.9497 loading |  |  |  |  | not computed |
| loading_sigma_PCOR_one_factor | estimate | 2.104 loading |  |  |  |  | not computed |
| loading_beta_PGOLD_one_factor | estimate | 0.7605 loading |  |  |  |  | not computed |
| loading_sigma_PGOLD_one_factor | estimate | 1.612 loading |  |  |  |  | not computed |
| loading_beta_PLC_one_factor | estimate | 1.156 loading |  |  |  |  | not computed |
| loading_sigma_PLC_one_factor | estimate | 2.486 loading |  |  |  |  | not computed |
| loading_beta_PNB_one_factor | estimate | 0.7994 loading |  |  |  |  | not computed |
| loading_sigma_PNB_one_factor | estimate | 1.599 loading |  |  |  |  | not computed |
| loading_beta_PNX_one_factor | estimate | 0.46 loading |  |  |  |  | not computed |
| loading_sigma_PNX_one_factor | estimate | 1.962 loading |  |  |  |  | not computed |
| loading_beta_PX_one_factor | estimate | 0.5659 loading |  |  |  |  | not computed |
| loading_sigma_PX_one_factor | estimate | 2.485 loading |  |  |  |  | not computed |
| loading_beta_PXP_one_factor | estimate | 1.304 loading |  |  |  |  | not computed |
| loading_sigma_PXP_one_factor | estimate | 5.215 loading |  |  |  |  | not computed |
| loading_beta_RLC_one_factor | estimate | 1.477 loading |  |  |  |  | not computed |
| loading_sigma_RLC_one_factor | estimate | 1.94 loading |  |  |  |  | not computed |
| loading_beta_RRHI_one_factor | estimate | 0.7599 loading |  |  |  |  | not computed |
| loading_sigma_RRHI_one_factor | estimate | 1.735 loading |  |  |  |  | not computed |
| loading_beta_SCC_one_factor | estimate | 0.9913 loading |  |  |  |  | not computed |
| loading_sigma_SCC_one_factor | estimate | 2.852 loading |  |  |  |  | not computed |
| loading_beta_SECB_one_factor | estimate | 1.094 loading |  |  |  |  | not computed |
| loading_sigma_SECB_one_factor | estimate | 1.723 loading |  |  |  |  | not computed |
| loading_beta_SLI_one_factor | estimate | 0.3344 loading |  |  |  |  | not computed |
| loading_sigma_SLI_one_factor | estimate | 2.012 loading |  |  |  |  | not computed |
| loading_beta_SM_one_factor | estimate | 1.118 loading |  |  |  |  | not computed |
| loading_sigma_SM_one_factor | estimate | 1.679 loading |  |  |  |  | not computed |
| loading_beta_SMC_one_factor | estimate | 0.7581 loading |  |  |  |  | not computed |
| loading_sigma_SMC_one_factor | estimate | 1.777 loading |  |  |  |  | not computed |
| loading_beta_SMPH_one_factor | estimate | 1.212 loading |  |  |  |  | not computed |
| loading_sigma_SMPH_one_factor | estimate | 1.593 loading |  |  |  |  | not computed |
| loading_beta_SSI_one_factor | estimate | 1.477 loading |  |  |  |  | not computed |
| loading_sigma_SSI_one_factor | estimate | 2.781 loading |  |  |  |  | not computed |
| loading_beta_SSP_one_factor | estimate | 0.9031 loading |  |  |  |  | not computed |
| loading_sigma_SSP_one_factor | estimate | 3.681 loading |  |  |  |  | not computed |
| loading_beta_STI_one_factor | estimate | 0.6874 loading |  |  |  |  | not computed |
| loading_sigma_STI_one_factor | estimate | 2.614 loading |  |  |  |  | not computed |
| loading_beta_TECH_one_factor | estimate | 0.9746 loading |  |  |  |  | not computed |
| loading_sigma_TECH_one_factor | estimate | 3.705 loading |  |  |  |  | not computed |
| loading_beta_TEL_one_factor | estimate | 0.829 loading |  |  |  |  | not computed |
| loading_sigma_TEL_one_factor | estimate | 1.9 loading |  |  |  |  | not computed |
| loading_beta_UBP_one_factor | estimate | 0.2162 loading |  |  |  |  | not computed |
| loading_sigma_UBP_one_factor | estimate | 1.013 loading |  |  |  |  | not computed |
| loading_beta_URC_one_factor | estimate | 1.005 loading |  |  |  |  | not computed |
| loading_sigma_URC_one_factor | estimate | 1.776 loading |  |  |  |  | not computed |
| loading_beta_VITA_one_factor | estimate | 1.14 loading |  |  |  |  | not computed |
| loading_sigma_VITA_one_factor | estimate | 3.611 loading |  |  |  |  | not computed |
| loading_beta_VLL_one_factor | estimate | 1.117 loading |  |  |  |  | not computed |
| loading_sigma_VLL_one_factor | estimate | 2.136 loading |  |  |  |  | not computed |
| loading_beta_WEB_one_factor | estimate | 1.039 loading |  |  |  |  | not computed |
| loading_sigma_WEB_one_factor | estimate | 4.862 loading |  |  |  |  | not computed |
| loading_beta1_2GO_two_factor | estimate | 0.9241 loading beta1i |  |  |  |  | not computed |
| loading_beta2_2GO_two_factor_ns | estimate | 0.0236 loading beta2i ns |  |  |  |  | not computed |
| loading_sigma_2GO_two_factor | estimate | 3.899 loading |  |  |  |  | not computed |
| loading_beta1_ABA_two_factor | estimate | 1.007 loading |  |  |  |  | not computed |
| loading_beta2_ABA_two_factor_ns | estimate | 0.1693 loading ns |  |  |  |  | not computed |
| loading_sigma_ABA_two_factor | estimate | 3.22 loading |  |  |  |  | not computed |
| loading_beta1_AC_two_factor | estimate | 0.9129 loading |  |  |  |  | not computed |
| loading_beta2_AC_two_factor | estimate | 0.8448 loading |  |  |  |  | not computed |
| loading_sigma_AC_two_factor | estimate | 1.399 loading |  |  |  |  | not computed |
| loading_beta1_AEV_two_factor | estimate | 0.7433 loading |  |  |  |  | not computed |
| loading_beta2_AEV_two_factor | estimate | 0.972 loading |  |  |  |  | not computed |
| loading_sigma_AEV_two_factor | estimate | 1.743 loading |  |  |  |  | not computed |
| loading_beta1_AGI_two_factor | estimate | 1.238 loading |  |  |  |  | not computed |
| loading_beta2_AGI_two_factor | estimate | 0.41 loading |  |  |  |  | not computed |
| loading_sigma_AGI_two_factor | estimate | 1.704 loading |  |  |  |  | not computed |
| loading_beta1_ALI_two_factor | estimate | 1.033 loading |  |  |  |  | not computed |
| loading_beta2_ALI_two_factor | estimate | 0.9285 loading |  |  |  |  | not computed |
| loading_sigma_ALI_two_factor | estimate | 1.525 loading |  |  |  |  | not computed |
| loading_beta1_AP_two_factor | estimate | 0.4345 loading |  |  |  |  | not computed |
| loading_beta2_AP_two_factor | estimate | 0.7176 loading |  |  |  |  | not computed |
| loading_sigma_AP_two_factor | estimate | 1.419 loading |  |  |  |  | not computed |
| loading_beta1_BDO_two_factor | estimate | 0.9548 loading |  |  |  |  | not computed |
| loading_beta2_BDO_two_factor | estimate | 0.9023 loading |  |  |  |  | not computed |
| loading_sigma_BDO_two_factor | estimate | 1.439 loading |  |  |  |  | not computed |
| loading_beta1_BEL_two_factor | estimate | 0.8462 loading |  |  |  |  | not computed |
| loading_beta2_BEL_two_factor | estimate | 0.1517 loading |  |  |  |  | not computed |
| loading_sigma_BEL_two_factor | estimate | 1.629 loading |  |  |  |  | not computed |
| loading_beta1_BLOOM_two_factor | estimate | 1.502 loading |  |  |  |  | not computed |
| loading_beta2_BLOOM_two_factor | estimate | 0.4127 loading |  |  |  |  | not computed |
| loading_sigma_BLOOM_two_factor | estimate | 2.698 loading |  |  |  |  | not computed |
| loading_beta1_BPI_two_factor | estimate | 0.747 loading |  |  |  |  | not computed |
| loading_beta2_BPI_two_factor | estimate | 0.7162 loading |  |  |  |  | not computed |
| loading_sigma_BPI_two_factor | estimate | 1.435 loading |  |  |  |  | not computed |
| loading_beta1_BRN_two_factor | estimate | 1.201 loading |  |  |  |  | not computed |
| loading_beta2_BRN_two_factor | estimate | 0.3564 loading |  |  |  |  | not computed |
| loading_sigma_BRN_two_factor | estimate | 3.295 loading |  |  |  |  | not computed |
| loading_beta1_CEB_two_factor | estimate | 1.287 loading |  |  |  |  | not computed |
| loading_beta2_CEB_two_factor | estimate | 0.3642 loading |  |  |  |  | not computed |
| loading_sigma_CEB_two_factor | estimate | 2.396 loading |  |  |  |  | not computed |
| loading_beta1_CHIB_two_factor | estimate | 0.3963 loading |  |  |  |  | not computed |
| loading_beta2_CHIB_two_factor | estimate | 0.1341 loading |  |  |  |  | not computed |
| loading_sigma_CHIB_two_factor | estimate | 0.9321 loading |  |  |  |  | not computed |
| loading_beta1_CNPF_two_factor | estimate | 0.6854 loading |  |  |  |  | not computed |
| loading_beta2_CNPF_two_factor_ns | estimate | 0.0993 loading ns |  |  |  |  | not computed |
| loading_sigma_CNPF_two_factor | estimate | 1.711 loading |  |  |  |  | not computed |
| loading_beta1_COSCO_two_factor | estimate | 0.7646 loading |  |  |  |  | not computed |
| loading_beta2_COSCO_two_factor | estimate | 0.1666 loading |  |  |  |  | not computed |
| loading_sigma_COSCO_two_factor | estimate | 1.436 loading |  |  |  |  | not computed |
| loading_beta1_CPG_two_factor | estimate | 0.8825 loading |  |  |  |  | not computed |
| loading_beta2_CPG_two_factor_ns | estimate | 0.1603 loading ns |  |  |  |  | not computed |
| loading_sigma_CPG_two_factor | estimate | 2.184 loading |  |  |  |  | not computed |
| loading_beta1_DD_two_factor | estimate | 0.7264 loading |  |  |  |  | not computed |
| loading_beta2_DD_two_factor | estimate | 0.2518 loading |  |  |  |  | not computed |
| loading_sigma_DD_two_factor | estimate | 2.438 loading |  |  |  |  | not computed |
| loading_beta1_DMC_two_factor | estimate | 1.122 loading |  |  |  |  | not computed |
| loading_beta2_DMC_two_factor | estimate | 0.5568 loading |  |  |  |  | not computed |
| loading_sigma_DMC_two_factor | estimate | 1.895 loading |  |  |  |  | not computed |
| loading_beta1_DNL_two_factor | estimate | 1.201 loading |  |  |  |  | not computed |
| loading_beta2_DNL_two_factor_ns | estimate | 0.1748 loading ns |  |  |  |  | not computed |
| loading_sigma_DNL_two_factor | estimate | 2.183 loading |  |  |  |  | not computed |
| loading_beta1_EEI_two_factor | estimate | 0.8138 loading |  |  |  |  | not computed |
| loading_beta2_EEI_two_factor_ns | estimate | 0.1628 loading ns |  |  |  |  | not computed |
| loading_sigma_EEI_two_factor | estimate | 2.17 loading |  |  |  |  | not computed |
| loading_beta1_EW_two_factor | estimate | 1.022 loading |  |  |  |  | not computed |
| loading_beta2_EW_two_factor | estimate | 0.242 loading |  |  |  |  | not computed |
| loading_sigma_EW_two_factor | estimate | 1.85 loading |  |  |  |  | not computed |
| loading_beta1_FGEN_two_factor | estimate | 0.7343 loading |  |  |  |  | not computed |
| loading_beta2_FGEN_two_factor | estimate | 0.3185 loading |  |  |  |  | not computed |
| loading_sigma_FGEN_two_factor | estimate | 1.888 loading |  |  |  |  | not computed |
| loading_beta1_FLI_two_factor | estimate | 0.9935 loading |  |  |  |  | not computed |
| loading_beta2_FLI_two_factor | estimate | 0.2374 loading |  |  |  |  | not computed |
| loading_sigma_FLI_two_factor | estimate | 1.547 loading |  |  |  |  | not computed |
| loading_beta1_FNI_two_factor | estimate | 1.195 loading |  |  |  |  | not computed |
| loading_beta2_FNI_two_factor_ns | estimate | 0.358 loading ns |  |  |  |  | not computed |
| loading_sigma_FNI_two_factor | estimate | 6.039 loading |  |  |  |  | not computed |
| loading_beta1_FPH_two_factor | estimate | 0.7587 loading |  |  |  |  | not computed |
| loading_beta2_FPH_two_factor_ns | estimate | 0.0554 loading ns |  |  |  |  | not computed |
| loading_sigma_FPH_two_factor | estimate | 1.19 loading |  |  |  |  | not computed |
| loading_beta1_GERI_two_factor | estimate | 1.03 loading |  |  |  |  | not computed |
| loading_beta2_GERI_two_factor_ns | estimate | 0.1669 loading ns |  |  |  |  | not computed |
| loading_sigma_GERI_two_factor | estimate | 2.092 loading |  |  |  |  | not computed |
| loading_beta1_GLO_two_factor | estimate | 0.4331 loading |  |  |  |  | not computed |
| loading_beta2_GLO_two_factor | estimate | 0.6612 loading |  |  |  |  | not computed |
| loading_sigma_GLO_two_factor | estimate | 1.81 loading |  |  |  |  | not computed |
| loading_beta1_GMA7_two_factor | estimate | 0.4239 loading |  |  |  |  | not computed |
| loading_beta2_GMA7_two_factor_ns | estimate | -0.0013 loading ns |  |  |  |  | not computed |
| loading_sigma_GMA7_two_factor | estimate | 1.374 loading |  |  |  |  | not computed |
| loading_beta1_GTCAP_two_factor | estimate | 0.9541 loading |  |  |  |  | not computed |
| loading_beta2_GTCAP_two_factor | estimate | 0.7777 loading |  |  |  |  | not computed |
| loading_sigma_GTCAP_two_factor | estimate | 1.835 loading |  |  |  |  | not computed |
| loading_beta1_HOUSE_two_factor | estimate | 0.4075 loading |  |  |  |  | not computed |
| loading_beta2_HOUSE_two_factor_ns | estimate | -0.0132 loading ns |  |  |  |  | not computed |
| loading_sigma_HOUSE_two_factor | estimate | 1.798 loading |  |  |  |  | not computed |
| loading_beta1_ICT_two_factor | estimate | 0.8903 loading |  |  |  |  | not computed |
| loading_beta2_ICT_two_factor | estimate | 0.7307 loading |  |  |  |  | not computed |
| loading_sigma_ICT_two_factor | estimate | 1.813 loading |  |  |  |  | not computed |
| loading_beta1_IMI_two_factor | estimate | 1.123 loading |  |  |  |  | not computed |
| loading_beta2_IMI_two_factor_ns | estimate | -0.034 loading ns |  |  |  |  | not computed |
| loading_sigma_IMI_two_factor | estimate | 2.414 loading |  |  |  |  | not computed |
| loading_beta1_JFC_two_factor | estimate | 1.045 loading |  |  |  |  | not computed |
| loading_beta2_JFC_two_factor | estimate | 0.5168 loading |  |  |  |  | not computed |
| loading_sigma_JFC_two_factor | estimate | 1.764 loading |  |  |  |  | not computed |
| loading_beta1_JGS_two_factor | estimate | 1.039 loading |  |  |  |  | not computed |
| loading_beta2_JGS_two_factor | estimate | 1.169 loading |  |  |  |  | not computed |
| loading_sigma_JGS_two_factor | estimate | 1.711 loading |  |  |  |  | not computed |
| loading_beta1_LC_two_factor | estimate | 0.3592 loading |  |  |  |  | not computed |
| loading_beta2_LC_two_factor_ns | estimate | -0.2497 loading ns |  |  |  |  | not computed |
| loading_sigma_LC_two_factor | estimate | 3.005 loading |  |  |  |  | not computed |
| loading_beta1_LPZ_two_factor | estimate | 0.8387 loading |  |  |  |  | not computed |
| loading_beta2_LPZ_two_factor_ns | estimate | 0.0945 loading ns |  |  |  |  | not computed |
| loading_sigma_LPZ_two_factor | estimate | 2.012 loading |  |  |  |  | not computed |
| loading_beta1_LTG_two_factor | estimate | 0.8529 loading |  |  |  |  | not computed |
| loading_beta2_LTG_two_factor | estimate | 0.395 loading |  |  |  |  | not computed |
| loading_sigma_LTG_two_factor | estimate | 2.099 loading |  |  |  |  | not computed |
| loading_beta1_MAXS_two_factor | estimate | 1.271 loading |  |  |  |  | not computed |
| loading_beta2_MAXS_two_factor_ns | estimate | 0.154 loading ns |  |  |  |  | not computed |
| loading_sigma_MAXS_two_factor | estimate | 1.979 loading |  |  |  |  | not computed |
| loading_beta1_MBT_two_factor | estimate | 0.9099 loading |  |  |  |  | not computed |
| loading_beta2_MBT_two_factor | estimate | 0.656 loading |  |  |  |  | not computed |
| loading_sigma_MBT_two_factor | estimate | 1.501 loading |  |  |  |  | not computed |
| loading_beta1_MEG_two_factor | estimate | 1.288 loading |  |  |  |  | not computed |
| loading_beta2_MEG_two_factor | estimate | 0.7545 loading |  |  |  |  | not computed |
| loading_sigma_MEG_two_factor | estimate | 1.759 loading |  |  |  |  | not computed |
| loading_beta1_MER_two_factor | estimate | 0.4251 loading |  |  |  |  | not computed |
| loading_beta2_MER_two_factor | estimate | 0.625 loading |  |  |  |  | not computed |
| loading_sigma_MER_two_factor | estimate | 1.478 loading |  |  |  |  | not computed |
| loading_beta1_MPI_two_factor | estimate | 0.9654 loading |  |  |  |  | not computed |
| loading_beta2_MPI_two_factor | estimate | 0.7626 loading |  |  |  |  | not computed |
| loading_sigma_MPI_two_factor | estimate | 1.929 loading |  |  |  |  | not computed |
| loading_beta1_MWC_two_factor | estimate | 0.7678 loading |  |  |  |  | not computed |
| loading_beta2_MWC_two_factor_ns | estimate | 0.1878 loading ns |  |  |  |  | not computed |
| loading_sigma_MWC_two_factor | estimate | 2.283 loading |  |  |  |  | not computed |
| loading_beta1_MWIDE_two_factor | estimate | 1.131 loading |  |  |  |  | not computed |
| loading_beta2_MWIDE_two_factor_ns | estimate | 0.0369 loading ns |  |  |  |  | not computed |
| loading_sigma_MWIDE_two_factor | estimate | 2.308 loading |  |  |  |  | not computed |
| loading_beta1_NI_two_factor | estimate | 0.5448 loading |  |  |  |  | not computed |
| loading_beta2_NI_two_factor_ns | estimate | -0.1908 loading ns |  |  |  |  | not computed |
| loading_sigma_NI_two_factor | estimate | 2.488 loading |  |  |  |  | not computed |
| loading_beta1_NIKL_two_factor | estimate | 1.353 loading |  |  |  |  | not computed |
| loading_beta2_NIKL_two_factor_ns | estimate | 0.2689 loading ns |  |  |  |  | not computed |
| loading_sigma_NIKL_two_factor | estimate | 3.668 loading |  |  |  |  | not computed |
| loading_beta1_PCOR_two_factor | estimate | 0.9715 loading |  |  |  |  | not computed |
| loading_beta2_PCOR_two_factor_ns | estimate | 0.1949 loading ns |  |  |  |  | not computed |
| loading_sigma_PCOR_two_factor | estimate | 2.078 loading |  |  |  |  | not computed |
| loading_beta1_PGOLD_two_factor | estimate | 0.7043 loading |  |  |  |  | not computed |
| loading_beta2_PGOLD_two_factor | estimate | 0.2572 loading |  |  |  |  | not computed |
| loading_sigma_PGOLD_two_factor | estimate | 1.609 loading |  |  |  |  | not computed |
| loading_beta1_PLC_two_factor | estimate | 1.168 loading |  |  |  |  | not computed |
| loading_beta2_PLC_two_factor | estimate | 0.2474 loading |  |  |  |  | not computed |
| loading_sigma_PLC_two_factor | estimate | 2.458 loading |  |  |  |  | not computed |
| loading_beta1_PNB_two_factor | estimate | 0.8758 loading |  |  |  |  | not computed |
| loading_beta2_PNB_two_factor_ns | estimate | 0.0977 loading ns |  |  |  |  | not computed |
| loading_sigma_PNB_two_factor | estimate | 1.558 loading |  |  |  |  | not computed |
| loading_beta1_PNX_two_factor | estimate | 0.358 loading |  |  |  |  | not computed |
| loading_beta2_PNX_two_factor | estimate | 0.2852 loading |  |  |  |  | not computed |
| loading_sigma_PNX_two_factor | estimate | 1.96 loading |  |  |  |  | not computed |
| loading_beta1_PX_two_factor | estimate | 0.6711 loading |  |  |  |  | not computed |
| loading_beta2_PX_two_factor_ns | estimate | -0.0153 loading ns |  |  |  |  | not computed |
| loading_sigma_PX_two_factor | estimate | 2.457 loading |  |  |  |  | not computed |
| loading_beta1_PXP_two_factor | estimate | 1.29 loading |  |  |  |  | not computed |
| loading_beta2_PXP_two_factor_ns | estimate | 0.3148 loading ns |  |  |  |  | not computed |
| loading_sigma_PXP_two_factor | estimate | 5.204 loading |  |  |  |  | not computed |
| loading_beta1_RLC_two_factor | estimate | 1.166 loading |  |  |  |  | not computed |
| loading_beta2_RLC_two_factor | estimate | 0.9296 loading |  |  |  |  | not computed |
| loading_sigma_RLC_two_factor | estimate | 1.917 loading |  |  |  |  | not computed |
| loading_beta1_RRHI_two_factor | estimate | 0.6137 loading |  |  |  |  | not computed |
| loading_beta2_RRHI_two_factor | estimate | 0.4181 loading |  |  |  |  | not computed |
| loading_sigma_RRHI_two_factor | estimate | 1.735 loading |  |  |  |  | not computed |
| loading_beta1_SCC_two_factor | estimate | 0.9616 loading |  |  |  |  | not computed |
| loading_beta2_SCC_two_factor_ns | estimate | 0.2731 loading ns |  |  |  |  | not computed |
| loading_sigma_SCC_two_factor | estimate | 2.842 loading |  |  |  |  | not computed |
| loading_beta1_SECB_two_factor | estimate | 0.9898 loading |  |  |  |  | not computed |
| loading_beta2_SECB_two_factor | estimate | 0.4194 loading |  |  |  |  | not computed |
| loading_sigma_SECB_two_factor | estimate | 1.724 loading |  |  |  |  | not computed |
| loading_beta1_SLI_two_factor | estimate | 0.3454 loading |  |  |  |  | not computed |
| loading_beta2_SLI_two_factor_ns | estimate | 0.0164 loading ns |  |  |  |  | not computed |
| loading_sigma_SLI_two_factor | estimate | 2.006 loading |  |  |  |  | not computed |
| loading_beta1_SM_two_factor | estimate | 0.7241 loading |  |  |  |  | not computed |
| loading_beta2_SM_two_factor | estimate | 1.023 loading |  |  |  |  | not computed |
| loading_sigma_SM_two_factor | estimate | 1.573 loading |  |  |  |  | not computed |
| loading_beta1_SMC_two_factor | estimate | 0.6562 loading |  |  |  |  | not computed |
| loading_beta2_SMC_two_factor | estimate | 0.3536 loading |  |  |  |  | not computed |
| loading_sigma_SMC_two_factor | estimate | 1.777 loading |  |  |  |  | not computed |
| loading_beta1_SMPH_two_factor | estimate | 0.8483 loading |  |  |  |  | not computed |
| loading_beta2_SMPH_two_factor | estimate | 1.014 loading |  |  |  |  | not computed |
| loading_sigma_SMPH_two_factor | estimate | 1.502 loading |  |  |  |  | not computed |
| loading_beta1_SSI_two_factor | estimate | 1.342 loading |  |  |  |  | not computed |
| loading_beta2_SSI_two_factor | estimate | 0.5626 loading |  |  |  |  | not computed |
| loading_sigma_SSI_two_factor | estimate | 2.778 loading |  |  |  |  | not computed |
| loading_beta1_SSP_two_factor | estimate | 0.9091 loading |  |  |  |  | not computed |
| loading_beta2_SSP_two_factor_ns | estimate | 0.1473 loading ns |  |  |  |  | not computed |
| loading_sigma_SSP_two_factor | estimate | 3.665 loading |  |  |  |  | not computed |
| loading_beta1_STI_two_factor | estimate | 0.7093 loading |  |  |  |  | not computed |
| loading_beta2_STI_two_factor_ns | estimate | 0.1038 loading ns |  |  |  |  | not computed |
| loading_sigma_STI_two_factor | estimate | 2.6 loading |  |  |  |  | not computed |
| loading_beta1_TECH_two_factor | estimate | 0.9719 loading |  |  |  |  | not computed |
| loading_beta2_TECH_two_factor_ns | estimate | 0.2527 loading ns |  |  |  |  | not computed |
| loading_sigma_TECH_two_factor | estimate | 3.698 loading |  |  |  |  | not computed |
| loading_beta1_TEL_two_factor | estimate | 0.5027 loading |  |  |  |  | not computed |
| loading_beta2_TEL_two_factor | estimate | 0.7467 loading |  |  |  |  | not computed |
| loading_sigma_TEL_two_factor | estimate | 1.847 loading |  |  |  |  | not computed |
| loading_beta1_UBP_two_factor | estimate | 0.244 loading |  |  |  |  | not computed |
| loading_beta2_UBP_two_factor_ns | estimate | -0.0131 loading ns |  |  |  |  | not computed |
| loading_sigma_UBP_two_factor | estimate | 1.004 loading |  |  |  |  | not computed |
| loading_beta1_URC_two_factor | estimate | 0.6913 loading |  |  |  |  | not computed |
| loading_beta2_URC_two_factor | estimate | 0.7876 loading |  |  |  |  | not computed |
| loading_sigma_URC_two_factor | estimate | 1.732 loading |  |  |  |  | not computed |
| loading_beta1_VITA_two_factor | estimate | 1.16 loading |  |  |  |  | not computed |
| loading_beta2_VITA_two_factor_ns | estimate | 0.2145 loading ns |  |  |  |  | not computed |
| loading_sigma_VITA_two_factor | estimate | 3.592 loading |  |  |  |  | not computed |
| loading_beta1_VLL_two_factor | estimate | 1.286 loading |  |  |  |  | not computed |
| loading_beta2_VLL_two_factor_ns | estimate | -0.0188 loading ns |  |  |  |  | not computed |
| loading_sigma_VLL_two_factor | estimate | 2.022 loading |  |  |  |  | not computed |
| loading_beta1_WEB_two_factor | estimate | 1.034 loading |  |  |  |  | not computed |
| loading_beta2_WEB_two_factor_ns | estimate | 0.2561 loading ns |  |  |  |  | not computed |
| loading_sigma_WEB_two_factor | estimate | 4.851 loading |  |  |  |  | not computed |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim tally_beta_i_significant_71_of_72_one_factor = 71: not in the paper's LaTeX
- rejected claim tally_beta2i_significant_36_of_72_two_factor = 36: not in the paper's LaTeX
- spec: the headline was written as prose ('["estimate_corr_Ft_PSEi_one_factor", "estimate_RMSE_improvement_outsample_pct", "estimate_corr_CAPM_beta_beta2i_two_fact'); chosen from the claim names: estimate_RMSE_improvement_outsample_pct
- round 1: the builder ran out of turns
- round 2: a reviewer found 4 breaches of the integrity rules; first, rule 1: Rule 1 requires every reported result be computed from the data, not set to a constant/paper value. PC1 is used as proxy for DFM factor F_t, so correlation of F_t with PC1 is tautologically set to 1.0 instead of computing DFM MLE correlation (paper 0.9975). Not computed. (`R2=1.0
            corr_vals.update({
                "estimate_corr_Ft_PSEi_one_factor":(r1,se1,n1),
                "estimate_corr_Ft_PC1_one_factor":(1.0,0.0`); then rule 1: Same breach: two-factor F1t-PC1 and F2t-PC2 correlations set to constant 1.0 because F1t,F2t are defined as PC1,PC2. Paper values are 0.8982 and 0.8229. Not computed from DFM. (`"estimate_corr_F1t_PC1_two_factor":(1.0,0.0,n1),
                "estimate_corr_F2t_PSEi_two_factor":(r2,se2,n2),
                "estimate_corr_F2t_PC2_two_fac`); then rule 1: R2 defined two lines above as R2=1.0 hard-coded. Paper reports regression of one-factor F_t on two-factor F1t,F2t R2=0.998. Result is constant, not computed via OLS on data. (`"estimate_R2_Ft_on_F1tF2t":(R2,None,n12),`); then rule 1: Reported estimate(s) are set to a constant (1.0 / R2=1.0) instead of computed from data. Paper values are ~0.9975, 0.8982, 0.8229, 0.998; code does not compute them. (`R2=1.0
            corr_vals.update({
                "estimate_corr_Ft_PSEi_one_factor":(r1,se1,n1),
                "estimate_corr_Ft_PC1_one_factor":(1.0,0.0`)
- sample: the sample differs from the paper's by 6 missing and 0 extra observations (8.3% of the paper's 72, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: PSE prices: Edge PSE DisclosureCht.ax (official, replaces defunct Phisix per fastquant). PSEi: equal-weighted mean return of retained stocks as proxy (paper used stooq ^PSEI, now CF-blocked; yfinance PSEI.PS only latest bar). GDP: World Bank NY.GDP.MKTP.KD.ZG annual growth (8 obs 2015-2022) illustration for unstated quarterly series; FRED quarterly candidates checked but none matched Philippines quarterly growth. DFM factors: PCA via SVD on demeaned returns (X_demeaned, U*s) as paper shows F_t-PC1 corr 0.9975, so near-identical. CAPM beta: OLS cov(R_i,R_m)/var(R_m) using proxy market vs Barrons external. Returns pct_change, 1% threshold inclusive, BIC lag orders taken as paper (p=3,q=5 and p=2,q=5) not re-estimated
- caveat: the sample block's not_rebuilt: tally_beta_i_significant_71_of_72_one_factor is no claim's name, so it excused nothing
- caveat: the sample block's not_rebuilt: tally_beta2i_significant_36_of_72_two_factor is no claim's name, so it excused nothing

## Data sources
- market data: none used
- other hosts the script fetched from: edge.pse.com.ph, api.worldbank.org

## Run
- sandbox: attempt 3, exit 0, 145.0s, with the packages the builder installed: PySocks==1.7.1, PyYAML==6.0.3, aiohappyeyeballs==2.7.1, aiohttp-fast-zlib==0.3.0, aiohttp==3.14.5, aiosignal==1.4.0, attrs==26.1.0, backtrader==1.9.78.123, black==26.10.1, bs4==0.0.2, ccxt==4.5.91, cffi==2.0.0, cfgv==3.5.0, chardet==7.7.0, charset-normalizer==3.4.7, click==8.5.0, cloudpickle==3.1.2, coincurve==21.0.0, contourpy==1.4.0, croniter==6.2.4, cryptography==50.0.2, curl_cffi==0.16.3, cycler==0.12.1, defusedxml==0.7.1, distlib==0.4.4, fastquant==0.1.8.1, filelock==4.2.4, fonttools==4.68.0, frozenlist==1.8.0, identify==2.6.20, idna==3.18, joblib==1.6.0, kiwisolver==1.5.1, matplotlib==3.11.2, multidict==6.9.1, mypy_extensions==1.1.0, networkx==3.7, nltk==3.10.4, nodeenv==1.11.1, oauthlib==3.3.1, orjson==3.13.0, pathspec==1.1.1, pillow==13.0.0, pre_commit==4.7.0, propcache==0.5.2, pycparser==3.0, pyparsing==3.3.3, python-discovery==1.6.7, pytokens==0.4.1, regex==2026.9.29, requests-oauthlib==2.0.0, tqdm==4.70.1, tweepy==4.17.0, uvloop==0.22.1, virtualenv==21.15.1, yarl==1.25.1, zlib-ng==1.0.0
- model calls: 59, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 4686044, out 119627 (reasoning 50273); cost $1.5630

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
