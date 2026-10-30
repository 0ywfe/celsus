We could not check this paper: the replication could not rebuild the paper's sample (Kalshi usable N per series (469,384,569 etc.) and volume/OI require Kalshi API history not in market_data cache; cannot count missing/extra for those series. Crypto extra cannot be determined precisely due to Kalshi filtering); and the replication could not rebuild the paper's sample (btc_N_M1M3: 796 here, 318 in the paper). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2604.01431
**Do Prediction Markets Forecast Cryptocurrency Volatility? Evidence from Kalshi Macro Contracts**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| kalshi_series_count | count | 10 series | 10 |  |  | True | precise: the paper's count |
| crypto_assets_count | count | 6 assets | 6 |  |  | True | precise: the paper's count |
| btc_fed_dovish_coef_M3 | estimate | 0.639 RVol units per prob change |  |  |  |  | not computed |
| btc_fed_dovish_coef_SE | estimate | 0.176 same |  |  |  |  | not computed |
| btc_fed_dovish_t | estimate | 3.63 t |  |  |  |  | not computed |
| btc_fed_dovish_p | p_value | 0.001 p |  |  |  |  | not computed |
| btc_fed_dovish_BH_adj_p | estimate | 0.02 BH adj p |  |  |  |  | not computed |
| btc_recession_oos_msfe | estimate | 0.979 ratio M3/M2 |  |  |  |  | not computed |
| btc_recession_oos_CW_p | p_value | 0.02 p |  |  |  |  | not computed |
| btc_recession_oos_R2 | estimate | 0.126 R2 |  |  |  |  | not computed |
| btc_recession_in_t | estimate | -2.76 t |  |  |  |  | not computed |
| btc_recession_in_p | p_value | 0.006 p |  |  |  |  | not computed |
| btc_recession_BH_adj_not_survive | p_value | 0.006 p |  |  |  |  | not computed |
| eth_cpi_in_coef | estimate | -1.209 RVol units |  |  |  |  | not computed |
| eth_cpi_in_t | estimate | -2.12 t |  |  |  |  | not computed |
| eth_cpi_in_p | p_value | 0.034 p |  |  |  |  | not computed |
| eth_cpi_in_AdjR2 | estimate | 0.108 R2 |  |  |  |  | not computed |
| eth_cpi_oos_msfe | estimate | 0.959 ratio |  |  |  |  | not computed |
| eth_cpi_oos_CW_p | p_value | 0.01 p |  |  |  |  | not computed |
| eth_cpi_oos_R2 | estimate | 0.068 R2 |  |  |  |  | not computed |
| sol_cpi_in_coef | estimate | -0.85 RVol units |  |  |  |  | not computed |
| sol_cpi_in_t | estimate | -2.55 t |  |  |  |  | not computed |
| sol_cpi_in_p | p_value | 0.011 p |  |  |  |  | not computed |
| sol_cpi_in_AdjR2 | estimate | 0.083 R2 |  |  |  |  | not computed |
| sol_cpi_oos_msfe | estimate | 0.983 ratio |  |  |  |  | not computed |
| sol_cpi_oos_CW_p | p_value | 0.048 p |  |  |  |  | not computed |
| sol_cpi_oos_R2 | estimate | 0.048 R2 |  |  |  |  | not computed |
| ada_cpi_in_coef | estimate | -0.982 RVol |  |  |  |  | not computed |
| ada_cpi_in_t | estimate | -2.35 t |  |  |  |  | not computed |
| ada_cpi_in_p | p_value | 0.019 p |  |  |  |  | not computed |
| ada_cpi_in_AdjR2 | estimate | 0.082 R2 |  |  |  |  | not computed |
| avax_cpi_in_coef | estimate | -0.834 RVol |  |  |  |  | not computed |
| avax_cpi_in_t | estimate | -1.31 t |  |  |  |  | not computed |
| avax_cpi_in_p | p_value | 0.191 p |  |  |  |  | not computed |
| avax_cpi_in_AdjR2 | estimate | 0.017 R2 |  |  |  |  | not computed |
| link_cpi_in_coef | estimate | -1.262 RVol |  |  |  |  | not computed |
| link_cpi_in_t | estimate | -3.39 t |  |  |  |  | not computed |
| link_cpi_in_p | p_value | 0.001 p |  |  |  |  | not computed |
| link_cpi_in_AdjR2 | estimate | 0.11 R2 |  |  |  |  | not computed |
| link_cpi_BH_adj_p | estimate | 0.042 BH adj p |  |  |  |  | not computed |
| btc_cpi_in_coef | estimate | -0.454 RVol |  |  |  |  | not computed |
| btc_cpi_in_t | estimate | -1.56 t |  |  |  |  | not computed |
| btc_cpi_in_p | p_value | 0.119 p |  |  |  |  | not computed |
| btc_cpi_in_AdjR2 | estimate | 0.16 R2 |  |  |  |  | not computed |
| kalshi_cpi_range_t | estimate | -2.1 t range |  |  |  |  | not computed |
| orth_firstStage_R2_fed | estimate | 2.3 percent |  |  |  |  | not computed |
| orth_firstStage_R2_fed_orth_share | estimate | 97.7 percent |  |  |  |  | not computed |
| orth_firstStage_R2_cpi | estimate | 7.5 percent |  |  |  |  | not computed |
| orth_fed_resid_t | estimate | 3.62 t |  |  |  |  | not computed |
| orth_fed_resid_p | p_value | 0.001 p |  |  |  |  | not computed |
| orth_cpi_resid_t_eth | estimate | -2.29 t |  |  |  |  | not computed |
| orth_cpi_resid_p_eth | p_value | 0.022 p |  |  |  |  | not computed |
| orth_cpi_resid_t_sol | estimate | -2.79 t |  |  |  |  | not computed |
| orth_cpi_resid_p_sol | p_value | 0.005 p |  |  |  |  | not computed |
| orth_cpi_resid_t_ada | estimate | -2.6 t |  |  |  |  | not computed |
| orth_cpi_resid_p_ada | p_value | 0.009 p |  |  |  |  | not computed |
| orth_cpi_resid_t_link | estimate | -3.73 t |  |  |  |  | not computed |
| orth_cpi_resid_p_link | p_value | 0.001 p |  |  |  |  | not computed |
| btc_M1_HAR1_coef | estimate | 0.581 coef | -0.01192 | 0.3898 | 800 | True | paper inside -0.01192 +/- 0.7639 |
| btc_M1_HAR1_SE | estimate | 0.64 SE | 0.3898 | 0 | 800 | False | 39.1% apart, beyond 10% |
| btc_M1_HAR5_coef | estimate | 6.047 coef | 4.07 | 1.589 | 800 | True | paper inside 4.07 +/- 3.115 |
| btc_M1_HAR5_SE | estimate | 3.179 SE | 1.589 | 0 | 800 | False | 50.0% apart, beyond 10% |
| btc_M1_HAR20_coef | estimate | 0.351 coef | 2.934 | 2.458 | 800 | True | paper inside 2.934 +/- 4.817 |
| btc_M1_HAR20_SE | estimate | 3.285 SE | 2.458 | 0 | 800 | False | 25.2% apart, beyond 10% |
| btc_M1_AdjR2 | estimate | 0.093 R2 | 0.07028 | 0 | 800 | False | 24.4% apart, beyond 10% |
| btc_M2_HAR1_coef | estimate | 0.474 coef | 0.04463 | 0.3785 | 796 | True | paper inside 0.04463 +/- 0.7419 |
| btc_M2_HAR1_SE | estimate | 0.589 SE | 0.3785 | 0 | 796 | False | 35.7% apart, beyond 10% |
| btc_M2_HAR5_coef | estimate | 6.075 coef | 3.801 | 1.589 | 796 | True | paper inside 3.801 +/- 3.114 |
| btc_M2_HAR5_SE | estimate | 3.415 SE | 1.589 | 0 | 796 | False | 53.5% apart, beyond 10% |
| btc_M2_HAR20_coef | estimate | -1.086 coef | 2.615 | 2.542 | 796 | True | paper inside 2.615 +/- 4.982 |
| btc_M2_HAR20_SE | estimate | 3.351 SE | 2.542 | 0 | 796 | False | 24.1% apart, beyond 10% |
| btc_M2_VIX_coef | estimate | 0.005 coef | 0.005063 | 0.003045 | 796 | True | paper inside 0.005063 +/- 0.005968 |
| btc_M2_VIX_SE | estimate | 0.004 SE | 0.003045 | 0 | 796 | False | 23.9% apart, beyond 10% |
| btc_M2_DXY_coef | estimate | 4.885 coef | 1.746 | 1.666 | 796 | True | paper inside 1.746 +/- 3.266 |
| btc_M2_DXY_SE | estimate | 2.896 SE | 1.666 | 0 | 796 | False | 42.5% apart, beyond 10% |
| btc_M2_SPX_coef | estimate | -2.859 coef | -1.277 | 0.7788 | 796 | False | paper outside -1.277 +/- 1.526 |
| btc_M2_SPX_SE | estimate | 1.234 SE | 0.7788 | 0 | 796 | False | 36.9% apart, beyond 10% |
| btc_M2_AdjR2 | estimate | 0.141 R2 | 0.08906 | 0 | 796 | False | 36.8% apart, beyond 10% |
| btc_M3_HAR1_coef | estimate | 0.395 coef |  |  |  |  | not computed |
| btc_M3_HAR1_SE | estimate | 0.56 SE |  |  |  |  | not computed |
| btc_M3_HAR5_coef | estimate | 6.388 coef |  |  |  |  | not computed |
| btc_M3_HAR5_SE | estimate | 3.348 SE |  |  |  |  | not computed |
| btc_M3_HAR20_coef | estimate | -1.323 coef |  |  |  |  | not computed |
| btc_M3_HAR20_SE | estimate | 3.318 SE |  |  |  |  | not computed |
| btc_M3_VIX_coef | estimate | 0.005 coef |  |  |  |  | not computed |
| btc_M3_VIX_SE | estimate | 0.004 SE |  |  |  |  | not computed |
| btc_M3_DXY_coef | estimate | 4.646 coef |  |  |  |  | not computed |
| btc_M3_DXY_SE | estimate | 2.823 SE |  |  |  |  | not computed |
| btc_M3_SPX_coef | estimate | -2.77 coef |  |  |  |  | not computed |
| btc_M3_SPX_SE | estimate | 1.217 SE |  |  |  |  | not computed |
| btc_M3_AdjR2 | estimate | 0.155 R2 |  |  |  |  | not computed |
| btc_IQR_fed | estimate | 0.023 prob change |  |  |  |  | not computed |
| btc_IQR_effect | estimate | 0.015 annualized RVol |  |  |  |  | not computed |
| btc_IQR_pct_mean | estimate | 2.4 percent |  |  |  |  | not computed |
| btc_OOS_fed_msfe | estimate | 1.009 ratio |  |  |  |  | not computed |
| btc_OOS_fed_CWp | p_value | 0.446 p |  |  |  |  | not computed |
| btc_OOS_fed_R2 | estimate | 0.118 R2 |  |  |  |  | not computed |
| btc_OOS_cpi_msfe | estimate | 0.995 ratio |  |  |  |  | not computed |
| btc_OOS_cpi_CWp | p_value | 0.231 p |  |  |  |  | not computed |
| btc_OOS_cpi_R2 | estimate | 0.095 R2 |  |  |  |  | not computed |
| eth_OOS_fed_msfe | estimate | 1.004 ratio |  |  |  |  | not computed |
| eth_OOS_fed_CWp | p_value | 0.893 p |  |  |  |  | not computed |
| eth_OOS_fed_R2 | estimate | -0.042 R2 |  |  |  |  | not computed |
| eth_OOS_rec_msfe | estimate | 1 ratio |  |  |  |  | not computed |
| eth_OOS_rec_CWp | p_value | 0.421 p |  |  |  |  | not computed |
| eth_OOS_rec_R2 | estimate | 0.051 R2 |  |  |  |  | not computed |
| sol_OOS_mon_msfe | estimate | 0.999 ratio |  |  |  |  | not computed |
| sol_OOS_mon_CWp | p_value | 0.325 p |  |  |  |  | not computed |
| sol_OOS_mon_R2 | estimate | 0.012 R2 |  |  |  |  | not computed |
| ada_OOS_mon_msfe | estimate | 0.992 ratio |  |  |  |  | not computed |
| ada_OOS_mon_CWp | p_value | 0.041 p |  |  |  |  | not computed |
| ada_OOS_mon_R2 | estimate | 0.011 R2 |  |  |  |  | not computed |
| avax_OOS_cpi_msfe | estimate | 0.996 ratio |  |  |  |  | not computed |
| avax_OOS_cpi_CWp | p_value | 0.171 p |  |  |  |  | not computed |
| avax_OOS_cpi_R2 | estimate | -0.045 R2 |  |  |  |  | not computed |
| link_OOS_cpi_msfe | estimate | 0.992 ratio |  |  |  |  | not computed |
| link_OOS_cpi_CWp | p_value | 0.121 p |  |  |  |  | not computed |
| link_OOS_cpi_R2 | estimate | 0.06 R2 |  |  |  |  | not computed |
| nonoverlap_btc_t | estimate | 1.17 t |  |  |  |  | not computed |
| nonoverlap_btc_p | p_value | 0.24 p |  |  |  |  | not computed |
| nonoverlap_btc_N | count | 64 obs |  |  |  |  | not computed |
| nonoverlap_link_t | estimate | -0.71 t |  |  |  |  | not computed |
| nonoverlap_link_N | count | 54 obs |  |  |  |  | not computed |
| bootstrap_block_p | p_value | 0.035 p |  |  |  |  | not computed |
| bootstrap_HAC_p | p_value | 0.0003 p |  |  |  |  | not computed |
| leadlag_lag_t | estimate | 3.71 t |  |  |  |  | not computed |
| leadlag_lag_p | p_value | 0.001 p |  |  |  |  | not computed |
| leadlag_lead_t | estimate | -0.17 t |  |  |  |  | not computed |
| leadlag_lead_p | p_value | 0.87 p |  |  |  |  | not computed |
| cpi_lead_eth_t | estimate | -2.53 t |  |  |  |  | not computed |
| cpi_lead_eth_p | p_value | 0.012 p |  |  |  |  | not computed |
| cpi_lead_sol_t | estimate | -3.76 t |  |  |  |  | not computed |
| cpi_lead_sol_p | p_value | 0.001 p |  |  |  |  | not computed |
| cpi_lead_link_t | estimate | -1.95 t |  |  |  |  | not computed |
| cpi_lead_link_p | p_value | 0.051 p |  |  |  |  | not computed |
| baseline_FF_t | estimate | -0.83 t | -0.06334 | 1.029 | 796 | True | paper inside -0.06334 +/- 2.017 |
| baseline_UST_t | estimate | 0.01 t | -0.3225 | 0.5193 | 796 | True | paper inside -0.3225 +/- 1.018 |
| baseline_joint_fed_t | estimate | 3.45 t |  |  |  |  | not computed |
| baseline_joint_fed_p | p_value | 0.001 p |  |  |  |  | not computed |
| baseline_eth_UST_t | estimate | -0.25 t | -1.048 | 0.7101 | 796 | True | paper inside -1.048 +/- 1.392 |
| baseline_eth_joint_cpi_t | estimate | -2.1 t |  |  |  |  | not computed |
| baseline_eth_joint_cpi_p | p_value | 0.035 p |  |  |  |  | not computed |
| dvol_btc_joint_fed_t | estimate | 3.46 t |  |  |  |  | not computed |
| dvol_btc_joint_fed_p | p_value | 0.001 p |  |  |  |  | not computed |
| dvol_btc_joint_dvol_t | estimate | 1.58 t |  |  |  |  | not computed |
| dvol_btc_joint_dvol_p | p_value | 0.12 p |  |  |  |  | not computed |
| dvol_eth_joint_cpi_t | estimate | -2.08 t |  |  |  |  | not computed |
| dvol_eth_joint_cpi_p | p_value | 0.037 p |  |  |  |  | not computed |
| dvol_eth_joint_dvol_t | estimate | -1.52 t |  |  |  |  | not computed |
| dvol_eth_joint_dvol_p | p_value | 0.13 p |  |  |  |  | not computed |
| garch_btc_fed_t | estimate | 2.91 t |  |  |  |  | not computed |
| garch_btc_fed_p | p_value | 0.004 p |  |  |  |  | not computed |
| garch_eth_cpi_t | estimate | -0.69 t |  |  |  |  | not computed |
| logRVol_btc_fed_t | estimate | 3.53 t |  |  |  |  | not computed |
| logRVol_eth_cpi_t | estimate | -2.41 t |  |  |  |  | not computed |
| rvol21_btc_fed_t | estimate | 0.93 t |  |  |  |  | not computed |
| rvol21_btc_fed_p | p_value | 0.35 p |  |  |  |  | not computed |
| rvol21_eth_cpi_t | estimate | -1.78 t |  |  |  |  | not computed |
| rvol21_eth_cpi_p | p_value | 0.075 p |  |  |  |  | not computed |
| cpi_release_dummy_link_t | estimate | -2.16 t |  |  |  |  | not computed |
| cpi_resid_nonrelease_eth_t | estimate | -1.81 t |  |  |  |  | not computed |
| cpi_resid_nonrelease_eth_p | p_value | 0.071 p |  |  |  |  | not computed |
| cpi_resid_nonrelease_sol_t | estimate | -2.8 t |  |  |  |  | not computed |
| cpi_resid_nonrelease_link_t | estimate | -3.07 t |  |  |  |  | not computed |
| cpi_dummy_CTRL_eth_t | estimate | -2.07 t |  |  |  |  | not computed |
| cpi_dummy_CTRL_eth_p | p_value | 0.039 p |  |  |  |  | not computed |
| cpi_dummy_CTRL_sol_t | estimate | -2.63 t |  |  |  |  | not computed |
| cpi_dummy_CTRL_sol_p | p_value | 0.009 p |  |  |  |  | not computed |
| cpi_dummy_CTRL_link_t | estimate | -3.21 t |  |  |  |  | not computed |
| cpi_dummy_CTRL_link_p | p_value | 0.001 p |  |  |  |  | not computed |
| ema_attenuated_btc_t | estimate | 1.24 t |  |  |  |  | not computed |
| composite_btc_t | estimate | -0.79 t |  |  |  |  | not computed |
| composite_link_t | estimate | -0.59 t |  |  |  |  | not computed |
| kalshi_median_vol_KXFED | estimate | 9326 USD |  |  |  |  | not computed |
| kalshi_peak_vol_KXFED | estimate | 6.51e+05 USD |  |  |  |  | not computed |
| kalshi_median_OI_KXFED | estimate | 2.788e+05 USD |  |  |  |  | not computed |
| kalshi_median_OI_KXCPI | estimate | 1.479e+05 USD |  |  |  |  | not computed |
| kalshi_median_OI_KXRECSSNBER | estimate | 4.566e+05 USD |  |  |  |  | not computed |
| btc_mean_RVol | estimate | 0.634 annualized std | 0.3478 | 0.005627 | 1181 | False | paper outside 0.3478 +/- 0.01103 |
| eth_mean_RVol | estimate | 0.742 annualized | 0.4663 | 0.007735 | 1181 | False | paper outside 0.4663 +/- 0.01516 |
| sol_mean_RVol | estimate | 0.93 annualized | 0.6467 | 0.009593 | 1181 | False | paper outside 0.6467 +/- 0.0188 |
| ada_mean_RVol | estimate | 0.81 annualized | 0.581 | 0.01183 | 1181 | False | paper outside 0.581 +/- 0.02318 |
| avax_mean_RVol | estimate | 0.918 annualized | 0.6569 | 0.01003 | 1181 | False | paper outside 0.6569 +/- 0.01967 |
| link_mean_RVol | estimate | 0.858 annualized | 0.6263 | 0.009477 | 1181 | False | paper outside 0.6263 +/- 0.01857 |
| btc_RVol_std | estimate | 0.194 annualized | 0.1934 |  | 1181 |  | no standard error |
| btc_RVol_min | estimate | 0.191 annualized | 0.0476 | 0 | 1181 | False | 75.1% apart, beyond 10% |
| btc_RVol_max | estimate | 1.341 annualized | 1.566 | 0 | 1181 | False | 16.7% apart, beyond 10% |
| eth_RVol_std | estimate | 0.254 annualized | 0.2658 |  | 1181 |  | no standard error |
| sol_RVol_std | estimate | 0.341 annualized | 0.3297 |  | 1181 |  | no standard error |
| sol_RVol_min | estimate | 0.186 annualized | 0.04876 | 0 | 1181 | False | 73.8% apart, beyond 10% |
| sol_RVol_max | estimate | 2.488 annualized | 2.577 | 0 | 1181 | True | 3.6% apart, within 10% |
| descriptive_N_per_asset | count | 1178 obs | 1181 | 0 |  | True | approximate: +0.3%, within SCORE's +/-15% |
| merged_calendar_N | count | 1183 calendar days | 1186 | 0 |  | True | approximate: +0.3%, within SCORE's +/-15% |
| kalshi_usable_N_KXFED | count | 469 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXCPI | count | 384 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXCPICORE | count | 331 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXGDP | count | 424 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXU3 | count | 389 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXPCECORE | count | 294 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXRECSSNBER_569 | count | 569 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXACPI | count | 283 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXRATECUT | count | 28 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXUSNFP | count | 0 obs |  |  |  |  | not computed |
| kalshi_usable_N_KXPCECORE_text | count | 294 obs |  |  |  |  | not computed |
| btc_N_M1M3 | count | 318 obs | 796 | 0 |  | False | +150.3%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-35.0), a band no published standard uses |
| cpi_N_M3 | count | 264 obs |  |  |  |  | not computed |
| allsig_KXACPI_N | count | 195 obs |  |  |  |  | not computed |
| allsig_KXACPI_coef | estimate | 0.412 coef |  |  |  |  | not computed |
| allsig_KXACPI_t | estimate | 2.4 t |  |  |  |  | not computed |
| allsig_KXACPI_p | p_value | 0.017 p |  |  |  |  | not computed |
| allsig_Labor_N | count | 265 obs |  |  |  |  | not computed |
| allsig_Labor_coef | estimate | 0.256 coef |  |  |  |  | not computed |
| allsig_Labor_t | estimate | 1.29 t |  |  |  |  | not computed |
| allsig_Labor_p | p_value | 0.196 p |  |  |  |  | not computed |
| allsig_MonetaryPolicy_N | count | 318 obs |  |  |  |  | not computed |
| allsig_MonetaryPolicy_coef | estimate | -0.354 coef |  |  |  |  | not computed |
| allsig_MonetaryPolicy_t | estimate | -1.09 t |  |  |  |  | not computed |
| allsig_MonetaryPolicy_p | p_value | 0.278 p |  |  |  |  | not computed |
| allsig_PCE_N | count | 193 obs |  |  |  |  | not computed |
| allsig_PCE_coef | estimate | 0.075 coef |  |  |  |  | not computed |
| allsig_PCE_t | estimate | 0.56 t |  |  |  |  | not computed |
| allsig_PCE_p | p_value | 0.574 p |  |  |  |  | not computed |
| allsig_GDP_N | count | 289 obs |  |  |  |  | not computed |
| allsig_GDP_coef | estimate | 0.076 coef |  |  |  |  | not computed |
| allsig_GDP_t | estimate | 0.38 t |  |  |  |  | not computed |
| allsig_GDP_p | p_value | 0.708 p |  |  |  |  | not computed |
| allsig_Core_N | count | 225 obs |  |  |  |  | not computed |
| allsig_Core_coef | estimate | -0.017 coef |  |  |  |  | not computed |
| allsig_Core_t | estimate | -0.1 t |  |  |  |  | not computed |
| allsig_Core_p | p_value | 0.919 p |  |  |  |  | not computed |
| sig_CPI_N_allsig | count | 264 obs |  |  |  |  | not computed |
| sig_CPI_coef_allsig | estimate | -0.252 coef |  |  |  |  | not computed |
| sig_CPI_t_allsig | estimate | -1.27 t |  |  |  |  | not computed |
| sig_CPI_p_allsig | p_value | 0.203 p |  |  |  |  | not computed |
| sig_Recession_coef_allsig | estimate | -1.536 coef |  |  |  |  | not computed |
| sig_Recession_t_allsig | estimate | -2.76 t |  |  |  |  | not computed |
| sig_FedDovish_coef_allsig | estimate | 0.639 coef |  |  |  |  | not computed |
| sig_FedDovish_t_allsig | estimate | 3.63 t |  |  |  |  | not computed |
| sig_FedDovish_p_allsig | p_value | 0 p |  |  |  |  | not computed |
| implied_vol_pred_highSignal | estimate | 0.348 annualized RVol |  |  |  |  | not computed |
| implied_vol_pred_benchmark | estimate | 0.324 annualized |  |  |  |  | not computed |
| implied_weight_reduction | estimate | 7 percent |  |  |  |  | not computed |
| eth_90pct_signal_level | estimate | 0.07 prob change |  |  |  |  | not computed |
| eth_vol_reduction_90pct | estimate | 0.084 annualized |  |  |  |  | not computed |
| eth_HAR_benchmark_pred | estimate | 0.52 annualized |  |  |  |  | not computed |
| eth_vol_reduction_pct | estimate | 16 percent |  |  |  |  | not computed |
| BH_q | parameter | 0.05 q | 0.05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| BH_tests_total | tally | 60 specifications | 60 |  |  |  | the script writes it as a fixed number (60 at line 251), so it is not judged |
| BH_survive_count | tally | 2 specs |  |  |  |  | not computed |
| OOS_significant_count | tally | 4 pairs |  |  |  |  | not computed |
| HAC_lags | parameter | 5 lags | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| expanding_initial | parameter | 120 obs | 120 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| h_primary | parameter | 5 days | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| h_robustness | parameter | 21 days | 21 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| block_bootstrap_len | parameter | 5 obs |  |  |  |  | not computed |
| block_bootstrap_B | parameter | 2000 resamples |  |  |  |  | not computed |
| tick_size | parameter | 0.01 USD | 0.01 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sqrt252 | parameter | 252 factor | 15.87 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sqrt365_ratio | parameter | 1.2 factor | 1.204 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| solana_tBH_not_survive_p | p_value | 0.011 p |  |  |  |  | not computed |
| oos_msfe_improvement_range | estimate | 2 percent |  |  |  |  | not computed |
| weekend_drop_pct | parameter | 30 percent | 31.45 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| gap_hours | parameter | 21 hours | 21 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |

## The paper's own numbers
- FLAG: by Kalshi series coverage - usable observations after 1-day lag and crypto merge Jan2023-Mar2026: 469 + 384 + 331 + 424 + 389 + 294 + 569 + 283 + 28 + 0 = 3171, paper's total 10
- OK: BTC Fed-dovish M3 overlapping HAC 5 lags 5-day RVol: t = 3.63, paper's p = 0.001 matches two-sided (0.0003); two-sided p would be 0.0003
- OK: BTC Recession Risk M3 HAC: t = -2.76, paper's p = 0.006 matches two-sided (0.0060); two-sided p would be 0.0060
- OK: ETH CPI M3 HAC: t = -2.12, paper's p = 0.034 matches two-sided (0.0340); two-sided p would be 0.0349
- OK: SOL CPI M3 HAC: t = -2.55, paper's p = 0.011 matches two-sided (0.0108); two-sided p would be 0.0113
- OK: ADA CPI M3 HAC: t = -2.35, paper's p = 0.019 matches two-sided (0.0188); two-sided p would be 0.0195
- OK: LINK CPI M3 HAC strongest altcoin: t = -3.39, paper's p = 0.001 matches two-sided (0.0008); two-sided p would be 0.0008
- OK: BTC CPI M3 null: t = -1.56, paper's p = 0.119 matches two-sided (0.1188); two-sided p would be 0.1200
- OK: AVAX CPI M3 null low AdjR2: t = -1.31, paper's p = 0.191 matches two-sided (0.1913); two-sided p would be 0.1913
- OK: Orthogonal Fed residual predicts BTC: t = 3.62, paper's p = 0.001 matches two-sided (0.0003); two-sided p would be 0.0003
- OK: Orthogonal CPI residual ETH: t = -2.29, paper's p = 0.022 matches two-sided (0.0220); two-sided p would be 0.0228
- OK: Orthogonal CPI residual SOL: t = -2.79, paper's p = 0.005 matches two-sided (0.0053); two-sided p would be 0.0057
- OK: Orthogonal CPI residual ADA: t = -2.6, paper's p = 0.009 matches two-sided (0.0093); two-sided p would be 0.0098
- OK: Orthogonal CPI residual LINK: t = -3.73, paper's p = 0.001 matches two-sided (0.0002); two-sided p would be 0.0002
- OK: Non-overlapping 5-day windows Fed BTC HC3: t = 1.17, paper's p = 0.24 matches two-sided (0.2420); two-sided p would be 0.2464
- NOTE: Block bootstrap BTC Fed confirms HAC: t = 3.63 and p = 0.035 fit no side at the printed precision (two-sided p would be 0.0003); judged two-sided
- OK: Lead-lag Fed BTC lagged signal: t = 3.71, paper's p = 0.001 matches two-sided (0.0002); two-sided p would be 0.0002
- OK: Lead-lag Fed BTC placebo lead: t = -0.17, paper's p = 0.87 matches two-sided (0.8651); two-sided p would be 0.8651
- OK: Lead CPI ETH persistent repricing: t = -2.53, paper's p = 0.012 matches two-sided (0.0120); two-sided p would be 0.0120
- OK: Lead CPI SOL persistent: t = -3.76, paper's p = 0.001 matches two-sided (0.0002); two-sided p would be 0.0002
- OK: Lead CPI LINK attenuates: t = -1.95, paper's p = 0.051 matches two-sided (0.0512); two-sided p would be 0.0522
- OK: Joint Kalshi Fed retains vs FF and UST BTC: t = 3.45, paper's p = 0.001 matches two-sided (0.0006); two-sided p would be 0.0006
- OK: Joint Kalshi CPI vs Treasury ETH: t = -2.1, paper's p = 0.035 matches two-sided (0.0357); two-sided p would be 0.0367
- OK: DVOL joint Kalshi Fed dominates BTC: t = 3.46, paper's p = 0.001 matches two-sided (0.0006); two-sided p would be 0.0006
- OK: DVOL BTC null in joint: t = 1.58, paper's p = 0.12 matches two-sided (0.1151); two-sided p would be 0.1151
- OK: DVOL joint Kalshi CPI dominates ETH: t = -2.08, paper's p = 0.037 matches two-sided (0.0375); two-sided p would be 0.0385
- OK: DVOL ETH null in joint: t = -1.52, paper's p = 0.13 matches two-sided (0.1297); two-sided p would be 0.1297
- OK: Alternative vol GARCH BTC Fed: t = 2.91, paper's p = 0.004 matches two-sided (0.0039); two-sided p would be 0.0039
- OK: Alternative vol 21-day RVol BTC Fed fades: t = 0.93, paper's p = 0.35 matches two-sided (0.3524); two-sided p would be 0.3531
- OK: Alternative vol 21-day RVol ETH CPI marginal: t = -1.78, paper's p = 0.075 matches two-sided (0.0751); two-sided p would be 0.0762
- OK: CPI with release dummy ETH: t = -2.07, paper's p = 0.039 matches two-sided (0.0394); two-sided p would be 0.0394
- OK: CPI with release dummy SOL: t = -2.63, paper's p = 0.009 matches two-sided (0.0090); two-sided p would be 0.0090
- OK: CPI with release dummy LINK: t = -3.21, paper's p = 0.001 matches two-sided (0.0013); two-sided p would be 0.0015
- OK: Non-release subsample ETH marginal: t = -1.81, paper's p = 0.071 matches two-sided (0.0714); two-sided p would be 0.0714
- OK: All signals BTC CPI Level KXACPI: t = 2.4, paper's p = 0.017 matches two-sided (0.0173); two-sided p would be 0.0173
- OK: All signals BTC Labor Market: t = 1.29, paper's p = 0.196 matches two-sided (0.1971); two-sided p would be 0.1982
- OK: All signals BTC Monetary Policy absolute: t = -1.09, paper's p = 0.278 matches two-sided (0.2765); two-sided p would be 0.2765
- OK: All signals BTC PCE: t = 0.56, paper's p = 0.574 matches two-sided (0.5755); two-sided p would be 0.5761
- OK: All signals BTC GDP: t = 0.38, paper's p = 0.708 matches two-sided (0.7042); two-sided p would be 0.7042
- OK: All signals BTC Core CPI: t = -0.1, paper's p = 0.919 matches two-sided (0.9203); two-sided p would be 0.9204
- NOTE: OOS Clark-West BTC Recession Risk MSFE<1: t = 0.979 and p = 0.02 fit no side at the printed precision (two-sided p would be 0.3283); judged two-sided
- NOTE: OOS Clark-West ETH CPI MSFE<1: t = 0.959 and p = 0.01 fit no side at the printed precision (two-sided p would be 0.3384); judged two-sided
- NOTE: OOS Clark-West SOL CPI MSFE<1: t = 0.983 and p = 0.048 fit no side at the printed precision (two-sided p would be 0.3265); judged two-sided
- NOTE: OOS Clark-West ADA Monetary Policy MSFE<1: t = 0.992 and p = 0.041 fit no side at the printed precision (two-sided p would be 0.3221); judged two-sided
- NOTE: OOS BTC Fed-dovish fails: t = 1.009 and p = 0.446 fit no side at the printed precision (two-sided p would be 0.3137); judged two-sided
- NOTE: BH FDR Fed-dovish survive: t = 3.63 and p = 0.02 fit no side at the printed precision (two-sided p would be 0.0006); judged two-sided
- NOTE: BH FDR LINK CPI survive: t = -3.39 and p = 0.042 fit no side at the printed precision (two-sided p would be 0.0013); judged two-sided

## Guards
- rejected claim sig_Recession_p_allsig = 0.006: printed 2 times in the paper's LaTeX, and already claimed by btc_recession_in_p, btc_recession_BH_adj_not_survive
- rejected claim spread_mid = two cents: not a number
- rejected claim spread_tail = five cents: not a number
- spec: the headline was written as prose ('Primary claims on which conclusions rest: btc_fed_dovish_coef_M3 with btc_fed_dovish_t=3.63 btc_fed_dovish_p<0.001 BH su'); chosen from the claim names: btc_fed_dovish_coef_M3
- spec: the headline was written as prose ('btc_fed_dovish_t, btc_fed_dovish_p, btc_fed_dovish_BH_adj_p, btc_recession_oos_msfe, btc_recession_oos_CW_p, eth_cpi_oos'); chosen from the claim names: btc_fed_dovish_BH_adj_p
- spec problem unresolved: test 'Non-overlapping CPI LINK single statistic': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Baseline Fed Funds alone BTC': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Baseline Treasury alone BTC': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Baseline Treasury alone ETH CPI': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Alternative vol log RVol BTC Fed': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Alternative vol GARCH ETH CPI null': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Alternative vol log RVol ETH CPI': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Non-release subsample SOL remains': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Non-release subsample LINK remains': p_value 'not stated' is not the name of a claim
- round 1: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (merged_calendar_N (1183) at line 369). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- round 2: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (merged_calendar_N (1183) at line 369). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- round 3: audit sent the sample back: btc_N_M1M3: the paper reports 318, your run produced 796
- sample: the replication could not rebuild the paper's sample (Kalshi usable N per series (469,384,569 etc.) and volume/OI require Kalshi API history not in market_data cache; cannot count missing/extra for those series. Crypto extra cannot be determined precisely due to Kalshi filtering)
- caveat: the replication used other sources or methods for the paper's observations: Crypto yfinance BTC-USD/ETH-USD etc. for CoinGecko; controls ^VIX/^GSPC/DX-Y.NYB for CBOE VIX/S&P500/DXY; ^IRX+ZQ=F for Fed Funds futures; ^TNX+ZN=F for 10y Treasury; annualization sqrt252. HAR on calendar returns then trading-join

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 13 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 3, exit 0, 50.4s
- model calls: 28, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 1540033, out 103505 (reasoning 46748); cost $0.8696

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
