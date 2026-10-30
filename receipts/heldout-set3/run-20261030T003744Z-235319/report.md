The paper's numbers do not hold up: 0 of 9 checked results match within their uncertainty. Its main result, summary_preCOVID_UR_h1_LGBplus_RMSE, was not computed. Sample size not rebuilt: the script writes it as a fixed number (37 at line 337), not counted from the data (emp_ragged_shift_count, 37 in the paper).

# paper-replicator report: arXiv 2605.09740
**LGB+: A Macroeconomic Forecasting Road Test**

Verdict: **does not hold up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| sim_P | parameter | 6 predictors | 6 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_N_250 | parameter | 250 observations | 250 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_N_500 | parameter | 500 observations | 500 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_N_1000 | parameter | 1000 observations | 1000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_SNR_0p5 | parameter | 0.5 ratio | 0.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_SNR_1 | parameter | 1 ratio | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_SNR_2 | parameter | 2 ratio | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_Ntest | parameter | 1000 observations | 1000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sim_replications | parameter | 10 replications | 10 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_ragged_shift_count | count | 37 variables | 37 |  |  |  | the script writes it as a fixed number (37 at line 337), so it is not judged |
| emp_AR_lags | parameter | 4 lags | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_FAAR_target_lags | parameter | 4 lags | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_FAAR_PC_lags | parameter | 2 lags | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_MARX_lags | parameter | 4 lags | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_MARX_MA_orders | parameter | 2 orders | 8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_PCs | parameter | 4 components | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_PC_lags | parameter | 4 lags | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_reestimate_freq | parameter | 8 quarters | 8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_RF_trees | parameter | 500 trees | 500 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_RF_min_node | parameter | 5 observations | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_NN_layers | parameter | 3 layers | 3 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_NN_neurons | parameter | 400 neurons | 400 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_NN_dropout | parameter | 0.2 rate | 0.2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_LGBplus_T_low | parameter | 5 trees per cycle | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| emp_LGBplus_T_high | parameter | 20 trees per cycle | 20 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| dual_ur_2009Q2_pred | estimate | 0.98 standardized units |  |  |  |  | not computed |
| dual_ur_2009Q2_actual | estimate | 1.03 standardized units |  |  |  |  | not computed |
| dual_ur_window_2008Q2_2009Q1_weight | estimate | 0.35 weight |  |  |  |  | not computed |
| dual_ur_window_1974Q4_1975Q3_weight | estimate | 0.241 weight |  |  |  |  | not computed |
| dual_dSpread_2024Q4_pred | estimate | 0.72 standardized units |  |  |  |  | not computed |
| dual_dSpread_2024Q4_actual | estimate | 0.93 standardized units |  |  |  |  | not computed |
| dual_dSpread_window_1981Q1_1981Q4_weight | estimate | 0.154 weight |  |  |  |  | not computed |
| dual_dSpread_window_1981Q2_1982Q1_weight | estimate | 0.152 weight |  |  |  |  | not computed |
| dual_houst_2022Q3_topQ_2022Q2_weight | estimate | 0.043 weight |  |  |  |  | not computed |
| dual_houst_2022Q3_secondQ_1981Q1_weight | estimate | 0.032 weight |  |  |  |  | not computed |
| dual_houst_2022Q3_top4Q_2021Q3_2022Q2_weight | estimate | 0.094 weight |  |  |  |  | not computed |
| dual_houst_2022Q3_second4Q_1981Q1_1981Q4_weight | estimate | 0.072 weight |  |  |  |  | not computed |
| sim_Linear_N250_SNR0p5_OLS_R2 | estimate | 32 R2 | 0.3132 | 0.008917 | 1000 | False | paper outside 0.3132 +/- 0.01748 |
| sim_Linear_N250_SNR0p5_RF_R2 | estimate | 25 R2 | 0.2606 | 0.008208 | 1000 | False | paper outside 0.2606 +/- 0.01609 |
| sim_Linear_N250_SNR0p5_LGB_R2 | estimate | 22 R2 | 0.2283 | 0.01315 | 1000 | False | paper outside 0.2283 +/- 0.02578 |
| sim_Linear_N250_SNR0p5_LGBplus_R2 | estimate | 27 R2 | 0.2914 | 0.01013 | 1000 | False | paper outside 0.2914 +/- 0.01986 |
| sim_TrigLog_N250_SNR0p5_RF_R2 | estimate | 11 R2 | 0.09825 | 0.00767 | 1000 | False | paper outside 0.09825 +/- 0.01503 |
| sim_TrigLog_N250_SNR0p5_LGBAplus_R2 | estimate | 13 R2 | 0.06595 | 0.01433 | 1000 | False | paper outside 0.06595 +/- 0.02809 |
| sim_SoftRadial_N250_SNR0p5_OLS_R2 | estimate | 2 R2 | -0.0299 | 0.007041 | 1000 | False | paper outside -0.0299 +/- 0.0138 |
| sim_SoftRadial_N250_SNR0p5_LGBAplus_R2 | estimate | 20 R2 | 0.1529 | 0.005643 | 1000 | False | paper outside 0.1529 +/- 0.01106 |
| sim_RotatedSine_N250_SNR0p5_RF_R2 | estimate | 10 R2 | 0.1057 | 0.007428 | 1000 | False | paper outside 0.1057 +/- 0.01456 |
| summary_preCOVID_UR_h1_RF_RMSE | estimate | 0.86 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_UR_h1_LGB_RMSE | estimate | 0.86 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_UR_h1_LGBAplus_RMSE | estimate | 0.68 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_UR_h1_LGBplus_RMSE | estimate | 0.67 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_UR_h1_KRR_RMSE | estimate | 1.29 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_UR_h2_LGBplus_RMSE | estimate | 0.71 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_INDPRO_h1_LGBAplus_RMSE | estimate | 0.88 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_INDPRO_h1_LGBplus_RMSE | estimate | 1.01 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_HOUST_h1_LGBplus_RMSE | estimate | 0.97 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_GDP_h1_KRR_RMSE | estimate | 0.84 relative RMSE |  |  |  |  | not computed |
| summary_preCOVID_INFL_h2_SPF_RMSE | estimate | 0.76 relative RMSE |  |  |  |  | not computed |
| summary_postCOVID_UR_h1_SPF_RMSE | estimate | 1.15 relative RMSE |  |  |  |  | not computed |
| summary_postCOVID_UR_h1_TABPFN_RMSE | estimate | 0.86 relative RMSE |  |  |  |  | not computed |
| summary_postCOVID_HOUST_h1_LGBAplus_RMSE | estimate | 0.83 relative RMSE |  |  |  |  | not computed |
| summary_postCOVID_DSpread_h1_LGBplus_RMSE | estimate | 0.8 relative RMSE |  |  |  |  | not computed |
| detailed_GDP_h1_preCOVID_KRR_Return_SE | estimate | 0.29 return |  |  |  |  | not computed |
| detailed_GDP_h1_preCOVID_KRR_DM_tstat | estimate | 1.41 t-stat |  |  |  |  | not computed |
| detailed_UR_h1_preCOVID_LGBplus_Sharpe_SE | estimate | 0.69 Sharpe |  |  |  |  | not computed |
| detailed_UR_h1_preCOVID_RF_rho1 | estimate | 0.27 autocorrelation |  |  |  |  | not computed |
| detailed_UR_h1_postCOVID_TABPFN_DM | estimate | 0.66 t-stat |  |  |  |  | not computed |
| detailed_DSpread_h1_preCOVID_RF_RMSE | estimate | 0.96 relative RMSE |  |  |  |  | not computed |
| interpret_IP_YLag_share | estimate | 60 percent |  |  |  |  | not computed |
| housing_rebound_1983 | estimate | 60 percent |  |  |  |  | not computed |
| mortgage_rate_1981_approx | estimate | 18 percent |  |  |  |  | not computed |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim sim_Linear_N250_SNR0p5_LGBAplus_R2 = .27: printed once in the paper's LaTeX, and already claimed by sim_Linear_N250_SNR0p5_LGBplus_R2
- rejected claim sim_Linear_N250_SNR1_OLS_R2 = .49: not in the paper's LaTeX
- rejected claim sim_Linear_N250_SNR1_LGBAplus_R2 = .45: not in the paper's LaTeX
- rejected claim sim_TrigLog_N250_SNR0p5_OLS_R2 = .00: not in the paper's LaTeX
- round 1: audit sent the sample back: the replication could not rebuild the paper's sample (Empirical missing/extra counts depend on exact vintage and on hyperparameter-dependent model selection (early stopping) which is stochastic; simulation stochastic variation makes exact N match probabilistic)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 1000, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: FRED-QD 2026-09 vintage (529kB, 246 series, 3/1/1959-6/1/2026) from https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/quarterly/2026-09-qd.csv used in place of paper's 2025Q1 vintage (same observations, later vintage, same series definitions); SPF single-series verified via fredgraph csv; simulation proxy base learners: sklearn DecisionTreeRegressor(max_depth=2 min_samples_leaf=5) for tree candidate, LightGBM LGBMRegressor(n_estimators=100 lr=0.07 max_depth=3 subsample 0.8 colsample 0.8) fallback to GradientBoostingRegressor, RF 200 trees (paper 500) same 75% subsampling min 5 for speed, LGB+ M=80 eta=0.08 q=0.7 rho=0.8 OOB winner, LGBA+ cycles12 T8 eta_tree0.07 eta_lin0.05 depth2, SNR calibrated on 100k draws, test set fixed per DGP hash seed, Mixture equal-variance raw sum (second-order)
- caveat: sample size not rebuilt: the script writes it as a fixed number (37 at line 337), not counted from the data (emp_ragged_shift_count, 37 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- market data: none used
- other hosts the script fetched from: www.stlouisfed.org, fred.stlouisfed.org

## Run
- sandbox: attempt 2, exit 0, 51.7s, with the packages the builder installed: cloudpickle==3.1.2, joblib==1.6.0, lightgbm==4.7.0, scikit-learn==1.9.1, threadpoolctl==3.7.0
- model calls: 48, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 5084590, out 98185 (reasoning 54576); cost $1.5309

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
