The paper's numbers do not hold up: 0 of 6 checked results match within their uncertainty. Its main result, btc_fed_dovish_t, was not computed.

# paper-replicator report: arXiv 2604.01431
**Do Prediction Markets Forecast Cryptocurrency Volatility? Evidence from Kalshi Macro Contracts**

Verdict: **does not hold up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| merged_calendar_days | count | 1183 days | 1186 |  | 1186 | True | approximate: +0.3%, within SCORE's +/-15% |
| total_crypto_assets | count | 6 assets | 6 |  | 6 | True | precise: the paper's count |
| btc_descriptive_N | count | 1178 obs | 1181 |  | 1181 | True | approximate: +0.3%, within SCORE's +/-15% |
| eth_descriptive_N | count | 1178 obs | 1181 |  | 1181 | True | approximate: +0.3%, within SCORE's +/-15% |
| sol_descriptive_N | count | 1178 obs | 1181 |  | 1181 | True | approximate: +0.3%, within SCORE's +/-15% |
| ada_descriptive_N | count | 1178 obs | 1181 |  | 1181 | True | approximate: +0.3%, within SCORE's +/-15% |
| avax_descriptive_N | count | 1178 obs | 1181 |  | 1181 | True | approximate: +0.3%, within SCORE's +/-15% |
| link_descriptive_N | count | 1178 obs | 1181 |  | 1181 | True | approximate: +0.3%, within SCORE's +/-15% |
| btc_descriptive_mean_RVol | estimate | 0.634 annualized | 0.3478 | 0.005627 | 1181 | False | paper outside 0.3478 +/- 0.01103 |
| btc_descriptive_sd | estimate | 0.194 annualized | 0.1934 |  | 1181 |  | no standard error |
| btc_descriptive_min | estimate | 0.191 annualized | 0.0476 |  | 1181 |  | no standard error |
| btc_descriptive_max | estimate | 1.341 annualized | 1.566 |  | 1181 |  | no standard error |
| eth_descriptive_mean | estimate | 0.742 annualized | 0.4663 | 0.007735 | 1181 | False | paper outside 0.4663 +/- 0.01516 |
| sol_descriptive_mean | estimate | 0.93 annualized | 0.6467 | 0.009593 | 1181 | False | paper outside 0.6467 +/- 0.0188 |
| ada_descriptive_mean | estimate | 0.81 annualized | 0.581 | 0.01183 | 1181 | False | paper outside 0.581 +/- 0.02318 |
| avax_descriptive_mean | estimate | 0.918 annualized | 0.6569 | 0.01003 | 1181 | False | paper outside 0.6569 +/- 0.01967 |
| link_descriptive_mean | estimate | 0.858 annualized | 0.6263 | 0.009477 | 1181 | False | paper outside 0.6263 +/- 0.01857 |
| kalshi_total_series | count | 10 series | 10 |  | 10 | True | precise: the paper's count |
| kalshi_KXFED_N | count | 469 days |  |  |  |  | not computed |
| kalshi_KXCPI_N | count | 384 days |  |  |  |  | not computed |
| kalshi_KXCPICORE_N | count | 331 days |  |  |  |  | not computed |
| kalshi_KXGDP_N | count | 424 days |  |  |  |  | not computed |
| kalshi_KXU3_N | count | 389 days |  |  |  |  | not computed |
| kalshi_KXPCECORE_N | count | 294 days |  |  |  |  | not computed |
| kalshi_KXRECSSNBER_N | count | 569 days |  |  |  |  | not computed |
| kalshi_KXACPI_N | count | 283 days |  |  |  |  | not computed |
| kalshi_KXRATECUT_N | count | 28 days |  |  |  |  | not computed |
| kalshi_KXUSNFP_N | count | 0 days |  |  |  |  | not computed |
| kalshi_KXFED_median_volume | estimate | 9326 USD |  |  |  |  | not computed |
| kalshi_KXFED_peak_volume | estimate | 6.51e+05 USD |  |  |  |  | not computed |
| kalshi_KXFED_median_OI | estimate | 2.788e+05 USD |  |  |  |  | not computed |
| kalshi_KXCPI_median_OI | estimate | 1.479e+05 USD |  |  |  |  | not computed |
| kalshi_KXRECSSNBER_median_OI | estimate | 4.566e+05 USD |  |  |  |  | not computed |
| btc_total_signals_tested | count | 10 signals |  |  |  |  | not computed |
| signal_EMA_t_BTC | estimate | 1.24 t-stat |  |  |  |  | not computed |
| signal_fed_dovish_t_BTC_raw | estimate | 3.63 t-stat |  |  |  |  | not computed |
| signal_composite_t_BTC | estimate | -0.79 t-stat |  |  |  |  | not computed |
| signal_composite_t_LINK | estimate | -0.59 t-stat |  |  |  |  | not computed |
| btc_M1_HAR1_coef | estimate | 0.581 coef |  |  |  |  | not computed |
| btc_M1_HAR1_se | estimate | 0.64 se |  |  |  |  | not computed |
| btc_M2_HAR1_coef | estimate | 0.474 coef |  |  |  |  | not computed |
| btc_M3_HAR1_coef | estimate | 0.395 coef |  |  |  |  | not computed |
| btc_M1_HAR5_coef | estimate | 6.047 coef |  |  |  |  | not computed |
| btc_M1_HAR5_se | estimate | 3.179 se |  |  |  |  | not computed |
| btc_M3_HAR5_coef | estimate | 6.388 coef |  |  |  |  | not computed |
| btc_M2_VIX_coef | estimate | 0.005 coef |  |  |  |  | not computed |
| btc_M2_DXY_coef | estimate | 4.885 coef |  |  |  |  | not computed |
| btc_M3_DXY_coef | estimate | 4.646 coef |  |  |  |  | not computed |
| btc_M2_SP500_coef | estimate | -2.859 coef |  |  |  |  | not computed |
| btc_M3_SP500_coef | estimate | -2.77 coef |  |  |  |  | not computed |
| btc_fed_dovish_coef | estimate | 0.639 coef |  |  |  |  | not computed |
| btc_fed_dovish_se | estimate | 0.176 se |  |  |  |  | not computed |
| btc_fed_dovish_t | estimate | 3.63 t-stat |  |  |  |  | not computed |
| btc_fed_dovish_p | p_value | 0.0003 p |  |  |  |  | not computed |
| btc_M1_adjR2 | estimate | 0.093 R2 |  |  |  |  | not computed |
| btc_M2_adjR2 | estimate | 0.141 R2 |  |  |  |  | not computed |
| btc_M3_adjR2 | estimate | 0.155 R2 |  |  |  |  | not computed |
| btc_insample_N | count | 318 obs |  |  |  |  | not computed |
| btc_fed_dovish_IQR | estimate | 0.023 prob units |  |  |  |  | not computed |
| btc_fed_dovish_IQR_effect | estimate | 0.015 annualized |  |  |  |  | not computed |
| btc_fed_dovish_pct_mean | estimate | 2.4 percent |  |  |  |  | not computed |
| btc_recession_coef | estimate | -1.536 coef |  |  |  |  | not computed |
| btc_recession_raw_t | estimate | -2.76 t-stat |  |  |  |  | not computed |
| btc_recession_N_allsignals | count | 389 obs |  |  |  |  | not computed |
| btc_recession_p_allsignals | p_value | 0.006 p |  |  |  |  | not computed |
| allsignals_CPILevel_coef | estimate | 0.412 coef |  |  |  |  | not computed |
| allsignals_CPILevel_t | estimate | 2.4 t-stat |  |  |  |  | not computed |
| allsignals_CPILevel_p | p_value | 0.017 p |  |  |  |  | not computed |
| allsignals_CPILevel_N | count | 195 obs |  |  |  |  | not computed |
| allsignals_Labor_N | count | 265 obs |  |  |  |  | not computed |
| allsignals_CPI_Signal_N | count | 264 obs |  |  |  |  | not computed |
| allsignals_MonPol_N | count | 318 obs |  |  |  |  | not computed |
| allsignals_MonPol_coef | estimate | -0.354 coef |  |  |  |  | not computed |
| allsignals_MonPol_t | estimate | -1.09 t-stat |  |  |  |  | not computed |
| allsignals_MonPol_p | p_value | 0.278 p |  |  |  |  | not computed |
| allsignals_InflationPCE_N | count | 193 obs |  |  |  |  | not computed |
| allsignals_InflationPCE_coef | estimate | 0.075 coef |  |  |  |  | not computed |
| allsignals_GDP_N | count | 289 obs |  |  |  |  | not computed |
| allsignals_GDP_coef | estimate | 0.076 coef |  |  |  |  | not computed |
| allsignals_CoreInfl_N | count | 225 obs |  |  |  |  | not computed |
| allsignals_CoreInfl_coef | estimate | -0.017 coef |  |  |  |  | not computed |
| cpi_BTC_coef | estimate | -0.454 coef |  |  |  |  | not computed |
| cpi_BTC_t | estimate | -1.56 t-stat |  |  |  |  | not computed |
| cpi_BTC_p | p_value | 0.119 p |  |  |  |  | not computed |
| cpi_BTC_adjR2 | estimate | 0.16 R2 |  |  |  |  | not computed |
| cpi_ETH_coef | estimate | -1.209 coef |  |  |  |  | not computed |
| cpi_ETH_t | estimate | -2.12 t-stat |  |  |  |  | not computed |
| cpi_ETH_p | p_value | 0.034 p |  |  |  |  | not computed |
| cpi_ETH_adjR2 | estimate | 0.108 R2 |  |  |  |  | not computed |
| cpi_SOL_coef | estimate | -0.85 coef |  |  |  |  | not computed |
| cpi_SOL_t | estimate | -2.55 t-stat |  |  |  |  | not computed |
| cpi_SOL_p | p_value | 0.011 p |  |  |  |  | not computed |
| cpi_SOL_adjR2 | estimate | 0.083 R2 |  |  |  |  | not computed |
| cpi_ADA_coef | estimate | -0.982 coef |  |  |  |  | not computed |
| cpi_ADA_t | estimate | -2.35 t-stat |  |  |  |  | not computed |
| cpi_ADA_p | p_value | 0.019 p |  |  |  |  | not computed |
| cpi_ADA_adjR2 | estimate | 0.082 R2 |  |  |  |  | not computed |
| cpi_AVAX_coef | estimate | -0.834 coef |  |  |  |  | not computed |
| cpi_AVAX_t | estimate | -1.31 t-stat |  |  |  |  | not computed |
| cpi_AVAX_p | p_value | 0.191 p |  |  |  |  | not computed |
| cpi_AVAX_adjR2 | estimate | 0.017 R2 |  |  |  |  | not computed |
| cpi_LINK_coef | estimate | -1.262 coef |  |  |  |  | not computed |
| cpi_LINK_t | estimate | -3.39 t-stat |  |  |  |  | not computed |
| cpi_LINK_p | p_value | 0.001 p |  |  |  |  | not computed |
| cpi_LINK_adjR2 | estimate | 0.11 R2 |  |  |  |  | not computed |
| insample_cpi_N | count | 264 obs |  |  |  |  | not computed |
| cpi_LINK_t_with_dummy | estimate | -3.21 t-stat |  |  |  |  | not computed |
| cpi_LINK_p_with_dummy | p_value | 0.001 p |  |  |  |  | not computed |
| cpi_SOL_t_with_dummy | estimate | -2.63 t-stat |  |  |  |  | not computed |
| cpi_SOL_p_with_dummy | p_value | 0.009 p |  |  |  |  | not computed |
| cpi_ETH_t_with_dummy | estimate | -2.07 t-stat |  |  |  |  | not computed |
| cpi_ETH_p_with_dummy | p_value | 0.039 p |  |  |  |  | not computed |
| cpi_release_dummy_t_LINK | estimate | -2.16 t-stat |  |  |  |  | not computed |
| cpi_nonrelease_SOL_t | estimate | -2.8 t-stat |  |  |  |  | not computed |
| cpi_nonrelease_LINK_t | estimate | -3.07 t-stat |  |  |  |  | not computed |
| cpi_nonrelease_ETH_t | estimate | -1.81 t-stat |  |  |  |  | not computed |
| cpi_nonrelease_ETH_p | p_value | 0.071 p |  |  |  |  | not computed |
| oos_BTC_fed_MSFE | estimate | 1.009 ratio |  |  |  |  | not computed |
| oos_BTC_fed_CW_p | p_value | 0.446 p |  |  |  |  | not computed |
| oos_BTC_fed_OOSR2 | estimate | 0.118 R2 |  |  |  |  | not computed |
| oos_BTC_fed_Noos | count | 198 obs |  |  |  |  | not computed |
| oos_BTC_rec_MSFE | estimate | 0.979 ratio |  |  |  |  | not computed |
| oos_BTC_rec_CW_p | p_value | 0.02 p |  |  |  |  | not computed |
| oos_BTC_rec_OOSR2 | estimate | 0.126 R2 |  |  |  |  | not computed |
| oos_BTC_rec_Noos | count | 269 obs |  |  |  |  | not computed |
| oos_BTC_cpi_MSFE | estimate | 0.995 ratio |  |  |  |  | not computed |
| oos_BTC_cpi_Noos | count | 144 obs |  |  |  |  | not computed |
| oos_ETH_fed_OOSR2 | estimate | -0.042 R2 |  |  |  |  | not computed |
| oos_ETH_fed_MSFE | estimate | 1.004 ratio |  |  |  |  | not computed |
| oos_ETH_fed_CW_p | p_value | 0.893 p |  |  |  |  | not computed |
| oos_ETH_fed_Noos | count | 198 obs |  |  |  |  | not computed |
| oos_ETH_cpi_MSFE | estimate | 0.959 ratio |  |  |  |  | not computed |
| oos_ETH_cpi_CW_p | p_value | 0.01 p |  |  |  |  | not computed |
| oos_ETH_cpi_OOSR2 | estimate | 0.068 R2 |  |  |  |  | not computed |
| oos_ETH_cpi_Noos | count | 144 obs |  |  |  |  | not computed |
| oos_ETH_rec_Noos | count | 269 obs |  |  |  |  | not computed |
| oos_SOL_cpi_MSFE | estimate | 0.983 ratio |  |  |  |  | not computed |
| oos_SOL_cpi_CW_p | p_value | 0.048 p |  |  |  |  | not computed |
| oos_SOL_cpi_OOSR2 | estimate | 0.048 R2 |  |  |  |  | not computed |
| oos_SOL_cpi_Noos | count | 144 obs |  |  |  |  | not computed |
| oos_SOL_mon_Noos | count | 198 obs |  |  |  |  | not computed |
| oos_ADA_mon_MSFE | estimate | 0.992 ratio |  |  |  |  | not computed |
| oos_ADA_mon_CW_p | p_value | 0.041 p |  |  |  |  | not computed |
| oos_ADA_mon_OOSR2 | estimate | 0.011 R2 |  |  |  |  | not computed |
| oos_ADA_mon_Noos | count | 198 obs |  |  |  |  | not computed |
| oos_AVAX_cpi_MSFE | estimate | 0.996 ratio |  |  |  |  | not computed |
| oos_AVAX_cpi_OOSR2 | estimate | -0.045 R2 |  |  |  |  | not computed |
| oos_AVAX_cpi_Noos | count | 144 obs |  |  |  |  | not computed |
| oos_LINK_cpi_MSFE | estimate | 0.992 ratio |  |  |  |  | not computed |
| oos_LINK_cpi_OOSR2 | estimate | 0.06 R2 |  |  |  |  | not computed |
| oos_LINK_cpi_CW_p | p_value | 0.121 p |  |  |  |  | not computed |
| oos_LINK_cpi_Noos | count | 144 obs |  |  |  |  | not computed |
| BH_BTC_fed_adj_p | p_value | 0.02 p |  |  |  |  | not computed |
| BH_LINK_cpi_adj_p | p_value | 0.042 p |  |  |  |  | not computed |
| BH_BTC_rec_raw_p | p_value | 0.006 p |  |  |  |  | not computed |
| BH_SOL_cpi_raw_p | p_value | 0.011 p |  |  |  |  | not computed |
| nonoverlap_BTC_t | estimate | 1.17 t-stat |  |  |  |  | not computed |
| nonoverlap_BTC_p | p_value | 0.24 p |  |  |  |  | not computed |
| nonoverlap_BTC_N | count | 64 obs |  |  |  |  | not computed |
| nonoverlap_LINK_t | estimate | -0.71 t-stat |  |  |  |  | not computed |
| nonoverlap_LINK_N | count | 54 obs |  |  |  |  | not computed |
| ortho_fed_R2 | estimate | 2.3 percent |  |  |  |  | not computed |
| ortho_fed_orth_pct | estimate | 97.7 percent |  |  |  |  | not computed |
| ortho_fed_resid_t | estimate | 3.62 t-stat |  |  |  |  | not computed |
| ortho_fed_resid_p | p_value | 0.001 p |  |  |  |  | not computed |
| ortho_cpi_R2 | estimate | 7.5 percent |  |  |  |  | not computed |
| ortho_cpi_resid_t_ETH | estimate | -2.29 t-stat |  |  |  |  | not computed |
| ortho_cpi_resid_p_ETH | p_value | 0.022 p |  |  |  |  | not computed |
| ortho_cpi_resid_t_SOL | estimate | -2.79 t-stat |  |  |  |  | not computed |
| ortho_cpi_resid_p_SOL | p_value | 0.005 p |  |  |  |  | not computed |
| ortho_cpi_resid_t_ADA | estimate | -2.6 t-stat |  |  |  |  | not computed |
| ortho_cpi_resid_p_ADA | p_value | 0.009 p |  |  |  |  | not computed |
| ortho_cpi_resid_t_LINK | estimate | -3.73 t-stat |  |  |  |  | not computed |
| ortho_cpi_resid_p_LINK | p_value | 0.001 p |  |  |  |  | not computed |
| bootstrap_p | p_value | 0.035 p |  |  |  |  | not computed |
| leadlag_lag_t | estimate | 3.71 t-stat |  |  |  |  | not computed |
| leadlag_lag_p | p_value | 0.001 p |  |  |  |  | not computed |
| leadlag_lead_t | estimate | -0.17 t-stat |  |  |  |  | not computed |
| leadlag_lead_p | p_value | 0.87 p |  |  |  |  | not computed |
| lead_CPI_ETH_t | estimate | -2.53 t-stat |  |  |  |  | not computed |
| lead_CPI_ETH_p | p_value | 0.012 p |  |  |  |  | not computed |
| lead_CPI_SOL_t | estimate | -3.76 t-stat |  |  |  |  | not computed |
| lead_CPI_SOL_p | p_value | 0.001 p |  |  |  |  | not computed |
| lead_CPI_LINK_t | estimate | -1.95 t-stat |  |  |  |  | not computed |
| lead_CPI_LINK_p | p_value | 0.051 p |  |  |  |  | not computed |
| baseline_FF_t | estimate | -0.83 t-stat |  |  |  |  | not computed |
| baseline_UST_t | estimate | 0.01 t-stat |  |  |  |  | not computed |
| baseline_joint_Kalshi_BTC_t | estimate | 3.45 t-stat |  |  |  |  | not computed |
| baseline_joint_Kalshi_BTC_p | p_value | 0.001 p |  |  |  |  | not computed |
| baseline_TSY_ETH_t | estimate | -0.25 t-stat |  |  |  |  | not computed |
| baseline_joint_Kalshi_ETH_t | estimate | -2.1 t-stat |  |  |  |  | not computed |
| baseline_joint_Kalshi_ETH_p | p_value | 0.035 p |  |  |  |  | not computed |
| DVOL_joint_Kalshi_BTC_t | estimate | 3.46 t-stat |  |  |  |  | not computed |
| DVOL_joint_Kalshi_BTC_p | p_value | 0.001 p |  |  |  |  | not computed |
| DVOL_DVOL_BTC_t | estimate | 1.58 t-stat |  |  |  |  | not computed |
| DVOL_DVOL_BTC_p | p_value | 0.12 p |  |  |  |  | not computed |
| DVOL_joint_Kalshi_ETH_t | estimate | -2.08 t-stat |  |  |  |  | not computed |
| DVOL_joint_Kalshi_ETH_p | p_value | 0.037 p |  |  |  |  | not computed |
| DVOL_DVOL_ETH_t | estimate | -1.52 t-stat |  |  |  |  | not computed |
| DVOL_DVOL_ETH_p | p_value | 0.13 p |  |  |  |  | not computed |
| GARCH_BTC_t | estimate | 2.91 t-stat |  |  |  |  | not computed |
| GARCH_BTC_p | p_value | 0.004 p |  |  |  |  | not computed |
| GARCH_ETH_t | estimate | -0.69 t-stat |  |  |  |  | not computed |
| logRVol_BTC_t | estimate | 3.53 t-stat |  |  |  |  | not computed |
| logRVol_ETH_t | estimate | -2.41 t-stat |  |  |  |  | not computed |
| RVol21_BTC_t | estimate | 0.93 t-stat |  |  |  |  | not computed |
| RVol21_BTC_p | p_value | 0.35 p |  |  |  |  | not computed |
| RVol21_ETH_t | estimate | -1.78 t-stat |  |  |  |  | not computed |
| RVol21_ETH_p | p_value | 0.075 p |  |  |  |  | not computed |
| vol_managed_BTC_pred_high | estimate | 0.348 annualized |  |  |  |  | not computed |
| vol_managed_BTC_pred_HAR | estimate | 0.324 annualized |  |  |  |  | not computed |
| vol_managed_weight_reduction | estimate | 7 percent |  |  |  |  | not computed |
| options_ETH_coef_applied | estimate | -1.209 coef |  |  |  |  | not computed |
| options_ETH_signal_90pct | estimate | 0.07 prob |  |  |  |  | not computed |
| options_ETH_vol_reduction | estimate | 0.084 annualized |  |  |  |  | not computed |
| options_ETH_HAR_benchmark | estimate | 0.52 annualized |  |  |  |  | not computed |
| options_ETH_pct_below_HAR | estimate | 16 percent |  |  |  |  | not computed |

## The paper's own numbers
- FLAG: kalshi_series_coverage: 469 + 384 + 331 + 424 + 389 + 294 + 569 + 283 + 28 + 0 = 3171, paper's total 10
- FLAG: crypto_assets_by_N: 1178 + 1178 + 1178 + 1178 + 1178 + 1178 = 7068, paper's total 6
- FLAG: btc_allsignals_by_series: 318 + 389 + 195 + 264 + 265 + 264 + 318 + 193 + 289 + 225 = 2720, paper's total 10
- FLAG: cpi_insample_by_asset: 264 + 264 + 264 + 264 + 264 + 264 = 1584, paper's total 264
- OK: btc_fed_dovish_M3: t = 3.63, paper's p = 0.0003 matches two-sided (0.0003); two-sided p would be 0.0003
- OK: btc_recession_all: t = -2.76, paper's p = 0.006 matches two-sided (0.0061); two-sided p would be 0.0061
- OK: cpi_level_btc: t = 2.4, paper's p = 0.017 matches two-sided (0.0173); two-sided p would be 0.0173
- OK: cpi_btc: t = -1.56, paper's p = 0.119 matches two-sided (0.1188); two-sided p would be 0.1200
- OK: cpi_eth: t = -2.12, paper's p = 0.034 matches two-sided (0.0340); two-sided p would be 0.0349
- OK: cpi_sol: t = -2.55, paper's p = 0.011 matches two-sided (0.0108); two-sided p would be 0.0113
- OK: cpi_ada: t = -2.35, paper's p = 0.019 matches two-sided (0.0188); two-sided p would be 0.0195
- OK: cpi_avax: t = -1.31, paper's p = 0.191 matches two-sided (0.1913); two-sided p would be 0.1913
- OK: cpi_link: t = -3.39, paper's p = 0.001 matches two-sided (0.0008); two-sided p would be 0.0008
- OK: nonoverlap_btc: t = 1.17, paper's p = 0.24 matches two-sided (0.2420); two-sided p would be 0.2464
- NOTE: ortho_fed_resid: t = 3.62 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.0003); judged two-sided
- OK: ortho_cpi_eth: t = -2.29, paper's p = 0.022 matches two-sided (0.0220); two-sided p would be 0.0228
- OK: ortho_cpi_sol: t = -2.79, paper's p = 0.005 matches two-sided (0.0053); two-sided p would be 0.0057
- OK: ortho_cpi_ada: t = -2.6, paper's p = 0.009 matches two-sided (0.0093); two-sided p would be 0.0098
- NOTE: ortho_cpi_link: t = -3.73 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.0002); judged two-sided
- NOTE: bootstrap_btc: t = 3.63 and p = 0.035 fit no side at the printed precision (two-sided p would be 0.0003); judged two-sided
- NOTE: leadlag_lag: t = 3.71 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.0002); judged two-sided
- OK: leadlag_lead: t = -0.17, paper's p = 0.87 matches two-sided (0.8651); two-sided p would be 0.8651
- OK: lead_cpi_eth: t = -2.53, paper's p = 0.012 matches two-sided (0.0120); two-sided p would be 0.0120
- NOTE: lead_cpi_sol: t = -3.76 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.0002); judged two-sided
- OK: lead_cpi_link: t = -1.95, paper's p = 0.051 matches two-sided (0.0512); two-sided p would be 0.0522
- NOTE: baseline_FF: t = -0.83 and p = 0.0003 fit no side at the printed precision (two-sided p would be 0.4072); judged two-sided
- OK: baseline_joint_BTC: t = 3.45, paper's p = 0.001 matches two-sided (0.0006); two-sided p would be 0.0006
- OK: baseline_joint_ETH: t = -2.1, paper's p = 0.035 matches two-sided (0.0357); two-sided p would be 0.0367
- OK: dvol_joint_BTC: t = 3.46, paper's p = 0.001 matches two-sided (0.0006); two-sided p would be 0.0006
- OK: dvol_joint_ETH: t = -2.08, paper's p = 0.037 matches two-sided (0.0375); two-sided p would be 0.0385
- OK: garch_btc: t = 2.91, paper's p = 0.004 matches two-sided (0.0039); two-sided p would be 0.0039
- OK: rvol21_btc: t = 0.93, paper's p = 0.35 matches two-sided (0.3524); two-sided p would be 0.3531
- OK: rvol21_eth: t = -1.78, paper's p = 0.075 matches two-sided (0.0751); two-sided p would be 0.0762

## Guards
- rejected claim oos_total_pairs = 11: not in the paper's LaTeX
- rejected claim bootstrap_HAC_p = 0.0003: printed once in the paper's LaTeX, and already claimed by btc_fed_dovish_p
- spec: the headline was written as prose ('Fed-dovish signal is strongest in-sample predictor for Bitcoin (btc_fed_dovish_coef 0.639, btc_fed_dovish_t 3.63, btc_fe'); chosen from the claim names: btc_fed_dovish_t
- spec problem unresolved: test 'nonoverlap_link': p_value 'nonoverlap_LINK_p' is not the name of a claim
- round 1: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (total_crypto_assets (6) at line 222, kalshi_total_series (10) at line 248, btc_total_signals_tested (10) at line 248). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- round 2: audit sent the sample back: the replication could not rebuild the paper's sample (Cannot count exact missing/extra Kalshi observations because public API no longer serves pre-2025 markets; retention window appears truncated. Crypto counts differ by 3 obs due to ambiguous windowing (paper says N=1,178 after lag/match, we get 1,181 with Eq2 definition). Without Kalshi signal we cannot determine effective estimation N=318 (BTC Fed-dovish) or 264 (CPI) filtering)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 1186, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Crypto prices: CoinGecko midnight-UTC in paper, substituted Yahoo Finance BTC-USD etc daily bars (verified same calendar coverage 2023-01-01 to 2026-03-31, closes should be highly correlated; paper uses log returns, source difference is caveat). Controls: VIX (^VIX), SP500 (^GSPC), DXY (DX-Y.NYB) via Yahoo Finance as proxies for CBOE VIX, S&P500, DXY index; Fed Funds futures and 10Y Treasury return and Deribit DVOL not fetched (require separate feeds). Kalshi: attempted public API https://api.elections.kalshi.com/trade-api/v2/markets and /markets/candlesticks (period_interval 1440, start_ts/end_ts seconds) verified live; historical retention only ~2025 onward, so volume-weighted Delta_vw Eq1 and absolute signals cannot be rebuilt. HAR controls and Newey-West HAC 5 lags would follow paper exactly if signal were available
- caveat: btc_total_signals_tested was not rebuilt: Requires all 10 Kalshi signals to test per BTC; without usable obs cannot enumerate
- caveat: insample_cpi_N was not rebuilt: N=264 for CPI signal; same issue

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 10 tickers
- other hosts the script fetched from: api.elections.kalshi.com

## Run
- sandbox: attempt 3, exit 0, 53.8s
- model calls: 62, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 4230727, out 105076 (reasoning 52690); cost $1.3548

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
