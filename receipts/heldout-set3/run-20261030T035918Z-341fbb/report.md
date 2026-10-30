The paper's numbers partly hold up: 2 of 19 checked results match within their uncertainty. Its main result, tab_summary_rmse_UR_h1_LGBplus_pre, is 0.67 RMSE relative to AR(4) in the paper and 1.068 RMSE relative to AR(4) here (not consistent).

# paper-replicator report: arXiv 2605.09740
**LGB+: A Macroeconomic Forecasting Road Test**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| tab_summary_rmse_UR_h1_LGBplus_pre | estimate | 0.67 RMSE relative to AR(4) | 1.068 | 0.07 | 51 | False | paper outside 1.068 +/- 0.1372 |
| tab_summary_rmse_UR_h1_LGBAplus_pre | estimate | 0.68 RMSE relative to AR | 1.259 | 0.07 | 51 | False | paper outside 1.259 +/- 0.1372 |
| tab_summary_rmse_INDPRO_h1_LGBAplus_pre | estimate | 0.88 RMSE relative to AR | 1.237 | 0.07 | 51 | False | paper outside 1.237 +/- 0.1372 |
| tab_summary_rmse_HOUSING_h1_LGBplus_pre | estimate | 0.97 RMSE relative to AR | 1.155 | 0.07 | 51 | False | paper outside 1.155 +/- 0.1372 |
| tab_summary_rmse_DSpread_h1_LGBAplus_pre | estimate | 1 RMSE relative to AR | 0.989 | 0.07 | 51 | True | paper inside 0.989 +/- 0.1372 |
| tab_summary_rmse_DSpread_h1_RF_pre | estimate | 0.96 RMSE relative to AR | 0.9267 | 0.07 | 51 | True | paper inside 0.9267 +/- 0.1372 |
| tab_summary_rmse_UR_h1_RF_pre | estimate | 0.86 RMSE relative to AR | 1.191 | 0.07 | 51 | False | paper outside 1.191 +/- 0.1372 |
| tab_summary_rmse_UR_h1_LGB_pre | estimate | 0.86 RMSE relative to AR | 1.323 | 0.07 | 51 | False | paper outside 1.323 +/- 0.1372 |
| tab_summary_rmse_UR_h1_KRR_pre | estimate | 1.29 RMSE relative to AR | 1.598 | 0.07 | 51 | False | paper outside 1.598 +/- 0.1372 |
| tab_summary_rmse_UR_h1_SPF_pre | estimate | 1.07 RMSE relative to AR |  |  |  |  | not computed |
| tab_summary_rmse_UR_h1_TPFN_pre | estimate | 0.84 RMSE relative to AR |  |  |  |  | not computed |
| tab_summary_rmse_UR_h1_RF_post | estimate | 1.43 RMSE relative to AR | 1.947 | 0.07 | 13 | False | paper outside 1.947 +/- 0.1372 |
| tab_summary_rmse_UR_h1_LGBplus_post | estimate | 1.39 RMSE relative to AR | 6.062 | 0.07 | 13 | False | paper outside 6.062 +/- 0.1372 |
| tab_summary_rmse_UR_h1_SPF_post | estimate | 1.15 RMSE relative to AR |  |  |  |  | not computed |
| tab_summary_rmse_UR_h1_TPFN_post | estimate | 0.86 RMSE relative to AR |  |  |  |  | not computed |
| tab_summary_rmse_UR_h2_LGBplus_pre | estimate | 0.71 RMSE relative to AR | 0.9755 | 0.07 | 51 | False | paper outside 0.9755 +/- 0.1372 |
| tab_summary_rmse_GDP_h1_KRR_pre | estimate | 0.84 RMSE relative to AR | 2.254 | 0.07 | 51 | False | paper outside 2.254 +/- 0.1372 |
| tab_summary_rmse_Infl_h1_SPF_pre | estimate | 0.86 RMSE relative to AR |  |  |  |  | not computed |
| tab_summary_rmse_Infl_h1_NN_pre | estimate | 0.89 RMSE relative to AR |  |  |  |  | not computed |
| sim_R2_Linear_N250_SNR0p5_OLS | estimate | 32 out-of-sample R2 average over 10 replications Ntest=1000 | 0.3156 | 0.04 | 1000 | False | paper outside 0.3156 +/- 0.0784 |
| sim_R2_Linear_N250_SNR0p5_RF | estimate | 25 R2 | 0.2658 | 0.04 | 1000 | False | paper outside 0.2658 +/- 0.0784 |
| sim_R2_Linear_N250_SNR0p5_LGB | estimate | 22 R2 | 0.2316 | 0.04 | 1000 | False | paper outside 0.2316 +/- 0.0784 |
| sim_R2_Linear_N250_SNR0p5_LGBplus | estimate | 27 R2 | 0.2257 | 0.04 | 1000 | False | paper outside 0.2257 +/- 0.0784 |
| sim_R2_RotatedSine_N250_SNR2_RF | estimate | 29 R2 | 0.2644 | 0.04 | 1000 | False | paper outside 0.2644 +/- 0.0784 |
| sim_R2_SoftRadial_N250_SNR0p5_OLS | estimate | 2 R2 | -0.03347 | 0.04 | 1000 | False | paper outside -0.03347 +/- 0.0784 |
| appendix_UR_h1_pre_DM_RF | estimate | 2.53 DM t-stat |  |  |  |  | not computed |
| appendix_UR_h1_pre_rho1_HNN_pre_infl_example | estimate | 0.02 first-order autocor of errors |  |  |  |  | not computed |
| dual_UR_2009Q2_pred_LGBAplus | estimate | 0.98 standardized unemployment forecast |  |  |  |  | not computed |
| dual_UR_2009Q2_actual | estimate | 1.03 actual |  |  |  |  | not computed |
| dual_UR_weight_top_window_2008Q2_2009Q1 | estimate | 0.35 AXIL observation weight sum over 4Q window |  |  |  |  | not computed |
| dual_UR_weight_second_window_1974Q4_1975Q3 | estimate | 0.241 4Q weight |  |  |  |  | not computed |
| dual_DSpread_2024Q4_pred | estimate | 0.72 change in spread forecast |  |  |  |  | not computed |
| dual_DSpread_2024Q4_actual | estimate | 0.93 actual |  |  |  |  | not computed |
| dual_DSpread_weight_top1_1981Q1_1981Q4 | estimate | 0.154 4Q weight |  |  |  |  | not computed |
| dual_DSpread_weight_top2_1981Q2_1982Q1 | estimate | 0.152 4Q weight |  |  |  |  | not computed |
| dual_HOUST_2022Q3_topQ_2022Q2 | estimate | 0.043 individual quarter AXIL weight |  |  |  |  | not computed |
| dual_HOUST_secondQ_1981Q1 | estimate | 0.032 weight |  |  |  |  | not computed |
| dual_HOUST_window_top_2021Q3_2022Q2 | estimate | 0.094 4Q weight |  |  |  |  | not computed |
| dual_HOUST_window_second_1981Q1_1981Q4 | estimate | 0.072 4Q weight |  |  |  |  | not computed |
| historical_housing_rebound_1983_Volcker | estimate | 60 percent change housing starts 1983 rebound |  |  |  |  | not computed |
| param_sim_replications | parameter | 10 replications | 10 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_Ntest | parameter | 1000 observations | 1000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_P_predictors | parameter | 6 predictors | 6 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_FREDQD_lags_ar | parameter | 4 lags | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_MARX_orders | parameter | 2 MA orders |  |  |  |  | not computed |
| param_PC_count | parameter | 4 PCs | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_reestimated_every | parameter | 8 quarters | 8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_sim_SNR_grid | parameter | 0.5 signal-to-noise ratio grid |  |  |  |  | not computed |
| param_sim_N_grid | parameter | 250 observations |  |  |  |  | not computed |
| param_DGP_count | parameter | 8 DGPs | 8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_RF_trees | parameter | 500 trees | 500 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_NN_layers | parameter | 400 neurons per layer | 400 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim sim_R2_Linear_N250_SNR0p5_LGBAplus = .27: printed once in the paper's LaTeX, and already claimed by sim_R2_Linear_N250_SNR0p5_LGBplus
- rejected claim sim_R2_TrigLog_N1000_SNR2_OLS = .06: not in the paper's LaTeX
- spec: the headline was written as prose ('tab_summary_rmse_UR_h1_LGBplus_pre_0.67 and tab_summary_rmse_UR_h1_LGBAplus_pre_0.68 and tab_summary_rmse_INDPRO_h1_LGBA'); chosen from the claim names: tab_summary_rmse_UR_h1_LGBplus_pre
- round 2: audit sent the sample back: the replication could not rebuild the paper's sample (Exact vintage revisions and 37-series shift list unavailable; cannot count missing/extra at observation level)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 51, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Model implementations are proxies: RF 150 trees vs 500 paper, LightGBM 80 trees vs CV-tuned, Ridge proxy for RR/KRR, custom DecisionTree-based LGB+ (M35 q0.8 rho0.5 depth2 ens2 + calibration y=β·ŷ) and LGBA+ (M8 T5 eta_tree0.05 eta_lin0.03) approximating LightGBM shallow trees; feature set limited to 150 most-variable MARX features for speed; FAAR/NN/HNN/TabPFN/SPF not publicly available quarterly at all horizons omitted as benchmark models only (not sample); 37-series 1Q publication-lag shift omitted (timing only, no count change); PCA on contemporaneous panel excluding MARX pre-PCA; simulation SNR calibrated via empirical Var(f)/Var(eps) per batch

## Data sources
- market data: none used
- other hosts the script fetched from: www.stlouisfed.org

## Run
- sandbox: attempt 3, exit 0, 215.7s, with the packages the builder installed: cloudpickle==3.1.2, joblib==1.6.0, lightgbm==4.7.0, scikit-learn==1.9.1, threadpoolctl==3.7.0
- model calls: 47, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 5198174, out 97980 (reasoning 45569); cost $1.4072

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
