The paper's numbers partly hold up: 3 of 3 checked results match within their uncertainty. Its main result is none of the numbers checked, so it was not judged. Sample size not rebuilt: exact posterior HMC in rank(K)<=T via 32 chains 300 burn 700 retained not rebuilt - Laplace approximation used, so exact timing/MCSE/Rhat not computed (RevExactDates, 605 in the paper).

# paper-replicator report: arXiv 2602.21173
**Bayesian Parametric Portfolio Policies**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| NOOS_months | count | 605 months | 605 |  |  | True | precise: the paper's count |
| NBurnIn_months | parameter | 121 months | 121 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingWindow_months | parameter | 120 months | 120 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| NAnomaly_portfolios | count | 212 portfolios | 212 |  |  | True | precise: the paper's count |
| NTiming_predictors | count | 30 predictors | 30 |  |  | True | precise: the paper's count |
| NSignals_predictors | count | 242 predictors | 242 |  |  | True | precise: the paper's count |
| NSignalsPolicy_L | parameter | 243 predictors | 243 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| NCoefficientsPolicy | parameter | 1215 coefficients | 1215 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| RiskAversion_gamma | parameter | 5 | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingCap_c | parameter | 0.6 | 0.6 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingLeverage_g | parameter | 1.5 | 1.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingPcaRank | parameter | 10 | 10 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingOmega_median | estimate | 5.8 | 5.919 |  | 605 |  | no standard error |
| BPPP_active_pp | estimate | 7.05 pp | 7.062 |  | 605 |  | no standard error |
| BPPP_static_pp | estimate | 4.97 pp | 5.004 |  | 605 |  | no standard error |
| BPPP_timing_pp | estimate | 2.08 pp | 2.058 | 0.7092 | 605 | True | paper inside 2.058 +/- 1.39 |
| BPPP_timing_t | estimate | 3 t | 2.902 |  | 605 |  | no standard error |
| BPPP_timing_share_pct | estimate | 29.5% | 29.14 |  | 605 |  | no standard error |
| BPPP_gross_SR_total | estimate | 1.242 | 1.243 |  | 605 |  | no standard error |
| BPPP_gross_SR_excess | estimate | 0.96 | 0.9609 |  | 605 |  | no standard error |
| BPPP_net_SR_total | estimate | 1.043 | 1.041 |  | 605 |  | no standard error |
| BPPP_turnover_annual | estimate | 5.01 | 5.059 |  | 605 |  | no standard error |
| BPPP_exposure_avg | estimate | 1.31 | 1.309 |  | 605 |  | no standard error |
| BPPP_CE_gross_pct | estimate | 12.68% | 12.7 |  | 605 |  | no standard error |
| RPPP_timing_pp | estimate | 1.5 pp | 1.458 | 1.009 | 605 | True | paper inside 1.458 +/- 1.978 |
| RPPP_timing_t | estimate | 1.53 t | 1.445 |  | 605 |  | no standard error |
| RPPP_active_pp | estimate | 6.77 pp | 6.754 |  | 605 |  | no standard error |
| RPPP_static_pp | estimate | 5.27 pp | 5.296 |  | 605 |  | no standard error |
| RPPP_timing_share_pct | estimate | 22.1% | 21.59 |  | 605 |  | no standard error |
| RPPP_gross_SR_total | estimate | 1.211 | 1.21 |  | 605 |  | no standard error |
| RPPP_exposure_avg | estimate | 1.49 | 1.495 |  | 605 |  | no standard error |
| Constant_active_pp | estimate | 7.18 pp |  |  |  |  | not computed |
| Constant_static_pp | estimate | 7.1 pp |  |  |  |  | not computed |
| Constant_timing_pp | estimate | 0.08 pp |  |  |  |  | not computed |
| Constant_timing_t | estimate | 0.33 t |  |  |  |  | not computed |
| Constant_gross_SR_total | estimate | 1.193 |  |  |  |  | not computed |
| Constant_gross_SR_excess | estimate | 0.925 |  |  |  |  | not computed |
| Constant_net_SR_total | estimate | 1.136 |  |  |  |  | not computed |
| Constant_CE_gross_pct | estimate | 12.09% |  |  |  |  | not computed |
| Constant_turnover_annual | estimate | 0.15 |  |  |  |  | not computed |
| Constant_exposure_avg | estimate | 1.5 |  |  |  |  | not computed |
| Lasso_timing_pp | estimate | 0.82 pp |  |  |  |  | not computed |
| Lasso_timing_t | estimate | 1 t |  |  |  |  | not computed |
| Lasso_active_pp | estimate | 5.59 pp |  |  |  |  | not computed |
| CMV_timing_pp | estimate | 0.98 pp |  |  |  |  | not computed |
| CMV_timing_t | estimate | 1.15 t |  |  |  |  | not computed |
| MinVar_timing_pp | estimate | 0.11 pp |  |  |  |  | not computed |
| MinVar_timing_t | estimate | 0.15 t |  |  |  |  | not computed |
| InvVar_timing_pp | estimate | -0.12 pp |  |  |  |  | not computed |
| InvVar_timing_t | estimate | -0.72 t |  |  |  |  | not computed |
| RewardToRisk_timing_pp | estimate | -0.06 pp |  |  |  |  | not computed |
| RewardToRisk_timing_t | estimate | -0.1 t |  |  |  |  | not computed |
| ScaledMinVar_timing_pp | estimate | 0.05 pp |  |  |  |  | not computed |
| ScaledMinVar_timing_t | estimate | 0.08 t |  |  |  |  | not computed |
| Market_gross_SR_total | estimate | 0.739 | 0.7393 |  | 605 |  | no standard error |
| Market_excess_SR | estimate | 0.47 | 0.4701 |  | 605 |  | no standard error |
| BPPP_vs_Constant_p_Holm | estimate | 0.953 |  |  |  |  | not computed |
| BPPP_vs_RPPP_p_Holm | estimate | 0.953 |  |  |  |  | not computed |
| Timing_1970s_pp | estimate | -0.14 pp | -0.06533 |  | 77 |  | no standard error |
| Timing_1980s_pp | estimate | 0.79 pp | 0.7705 |  | 120 |  | no standard error |
| Timing_1990s_pp | estimate | 2.93 pp | 2.955 |  | 120 |  | no standard error |
| Timing_2000s_pp | estimate | -0.06 pp | -0.1486 |  | 120 |  | no standard error |
| Timing_2010s_pp | estimate | 0.72 pp | 0.8237 |  | 120 |  | no standard error |
| Timing_2020s_pp | estimate | 1.89 pp | 1.622 |  | 48 |  | no standard error |
| Timing_ex1990s_pp | estimate | 1.73 pp | 1.697 | 0.8341 | 485 | True | paper inside 1.697 +/- 1.635 |
| Timing_ex1990s_t | estimate | 2.13 t | 2.035 |  | 485 |  | no standard error |
| Timing_ex1990s_months | count | 485 months | 485 |  |  | True | precise: the paper's count |
| RevPost_pp | estimate | 1.82 pp | 1.264 |  | 288 |  | no standard error |
| RevPub_pp | estimate | 1.22 pp |  |  |  |  | not computed |
| RevPub_t | estimate | 1.79 t |  |  |  |  | not computed |
| RevPubTwo_pp | estimate | 1.17 pp |  |  |  |  | not computed |
| RevPubTwo_t | estimate | 1.75 t |  |  |  |  | not computed |
| RevPubPost_pp | estimate | 1.75 pp |  |  |  |  | not computed |
| TimingRobustLow_pp | estimate | 1.47 pp |  |  |  |  | not computed |
| TimingRobustHigh_pp | estimate | 3.02 pp |  |  |  |  | not computed |
| TimingRobustTLow | estimate | 2.18 t |  |  |  |  | not computed |
| TimingRobustTHigh | estimate | 4.04 t |  |  |  |  | not computed |
| RevDropAnomaly_pp | estimate | 0.87 pp |  |  |  |  | not computed |
| RevDropAnomaly_t | estimate | 1.13 t |  |  |  |  | not computed |
| RevFamilyMax_pp | estimate | 0.05 pp |  |  |  |  | not computed |
| RevPcaTen_timing_pp | estimate | 4.42 pp |  |  |  |  | not computed |
| RevPcaTen_t | estimate | 4.51 t |  |  |  |  | not computed |
| RevPcaTenExpl_pct | estimate | 53% |  |  |  |  | not computed |
| RevPcaTurnLow | estimate | 10.6 |  |  |  |  | not computed |
| RevPcaTurnHigh | estimate | 15.4 |  |  |  |  | not computed |
| RevPcaNetLow | estimate | 0.56 |  |  |  |  | not computed |
| RevPcaNetHigh | estimate | 0.85 |  |  |  |  | not computed |
| PCA3_timing_pp | estimate | 2.57 pp |  |  |  |  | not computed |
| PCA3_t | estimate | 2.46 t |  |  |  |  | not computed |
| PCA3_var_pct | estimate | 35% |  |  |  |  | not computed |
| PCA5_timing_pp | estimate | 3.98 pp |  |  |  |  | not computed |
| PCA5_t | estimate | 3.67 t |  |  |  |  | not computed |
| PCA5_var_pct | estimate | 43% |  |  |  |  | not computed |
| PCA20_timing_pp | estimate | 4.17 pp |  |  |  |  | not computed |
| PCA20_t | estimate | 4.34 t |  |  |  |  | not computed |
| PCA20_var_pct | estimate | 65% |  |  |  |  | not computed |
| PCA40_timing_pp | estimate | 3.57 pp |  |  |  |  | not computed |
| PCA40_t | estimate | 4.13 t |  |  |  |  | not computed |
| PCA40_var_pct | estimate | 77% |  |  |  |  | not computed |
| RevAtLimitBPPP_pct | estimate | 52.6% | 53.22 |  | 605 |  | no standard error |
| RevAtLimitMap_pct | estimate | 96.4% | 96.69 |  | 605 |  | no standard error |
| RevPreBPPP_exposure | estimate | 1.48 | 1.485 |  | 605 |  | no standard error |
| RevPreMap_exposure | estimate | 2.44 | 2.448 |  | 605 |  | no standard error |
| RevContraction_median | estimate | 0.45 |  |  |  |  | not computed |
| RevContractionLow | estimate | 0.32 |  |  |  |  | not computed |
| RevContractionHigh | estimate | 0.54 |  |  |  |  | not computed |
| RevContractionCorr | estimate | 0.983 |  |  |  |  | not computed |
| RevPostSD | estimate | 1 |  |  |  |  | not computed |
| RevBootSD | estimate | 0.42 |  |  |  |  | not computed |
| RevPeakScaleTiming | estimate | 0.4 |  |  |  |  | not computed |
| RevPeakTiming_pp | estimate | 2.05 pp |  |  |  |  | not computed |
| RevPeakScaleSR | estimate | 0.425 |  |  |  |  | not computed |
| RevPeakSR | estimate | 1.245 |  |  |  |  | not computed |
| RevScaleMatched | estimate | 0.375 |  |  |  |  | not computed |
| RevScaledTiming_pp | estimate | 2.04 pp |  |  |  |  | not computed |
| RevScaledTiming_t | estimate | 2.65 t |  |  |  |  | not computed |
| RevScaledDiffT | estimate | 0.25 t |  |  |  |  | not computed |
| RevMonthlyTiming_pp | estimate | 1.55 pp |  |  |  |  | not computed |
| RevMonthlyTiming_t | estimate | 2.19 t |  |  |  |  | not computed |
| RevBagTiming_pp | estimate | 1.69 pp |  |  |  |  | not computed |
| RevBagTiming_t | estimate | 1.95 t |  |  |  |  | not computed |
| RevBagAtLimit_pct | estimate | 86.6% |  |  |  |  | not computed |
| RevRidgeHalfAtLimit_pct | estimate | 62.5% |  |  |  |  | not computed |
| RevRidgeTimingLow_pp | estimate | 1.47 pp |  |  |  |  | not computed |
| RevRidgeTimingHigh_pp | estimate | 1.69 pp |  |  |  |  | not computed |
| RevRecScaledTiming_pp | estimate | 2 pp |  |  |  |  | not computed |
| RevRecScaledTiming_t | estimate | 2.46 t |  |  |  |  | not computed |
| BPPP_RPPP_diff_pp | estimate | -0.58 pp |  |  |  |  | not computed |
| BPPP_RPPP_diff_t | estimate | -0.98 t |  |  |  |  | not computed |
| TurnoverPenalty_kappa80_timing_pp | estimate | 1.42 pp |  |  |  |  | not computed |
| TurnoverPenalty_kappa80_t | estimate | 2.25 t |  |  |  |  | not computed |
| TurnoverPenalty_kappa80_turnover | estimate | 1.51 |  |  |  |  | not computed |
| TurnoverPenalty_kappa80_net_SR | estimate | 1.118 |  |  |  |  | not computed |
| TurnoverPenalty_kappa80_p_vs_const | estimate | 0.79 |  |  |  |  | not computed |
| RevCostTLow | estimate | 2.03 t |  |  |  |  | not computed |
| RevScaleTwoTiming_pp | estimate | 1.22 pp |  |  |  |  | not computed |
| RevScaleTwo_t | estimate | 1.78 t |  |  |  |  | not computed |
| RevScaleTwo_net_SR | estimate | 1.122 |  |  |  |  | not computed |
| RevScaleTwo_turnover | estimate | 1.09 |  |  |  |  | not computed |
| RevConstNetSR_total | estimate | 1.136 |  |  |  |  | not computed |
| RevRecCostNetSR | estimate | 1.121 |  |  |  |  | not computed |
| RevRecCostT | estimate | 1.93 t |  |  |  |  | not computed |
| RevRecCostP_p | estimate | 0.83 |  |  |  |  | not computed |
| RevRecCostCEDiff_pp | estimate | -0.34 pp |  |  |  |  | not computed |
| RevRecAlpha_pp | estimate | 0.83 pp |  |  |  |  | not computed |
| RevRecAlpha_t | estimate | 0.76 t |  |  |  |  | not computed |
| RevBreakEighty_pct | estimate | 51% |  |  |  |  | not computed |
| RevBreakRec_pct | estimate | 51% |  |  |  |  | not computed |
| RevBlendW_pct | estimate | 40% |  |  |  |  | not computed |
| RevBlendSR | estimate | 1.147 |  |  |  |  | not computed |
| RevMandateTimLow_pp | estimate | 1.38 pp |  |  |  |  | not computed |
| RevMandateTimHigh_pp | estimate | 3.7 pp |  |  |  |  | not computed |
| RevMandateNetLow_SR | estimate | 0.963 |  |  |  |  | not computed |
| RevMandateNetHigh_SR | estimate | 1.107 |  |  |  |  | not computed |
| RevMandateBTLow_t | estimate | 2.19 t |  |  |  |  | not computed |
| RevMandateBTHigh_t | estimate | 3.06 t |  |  |  |  | not computed |
| RevMandateMTLow_t | estimate | 1.39 t |  |  |  |  | not computed |
| RevMandateMTHigh_t | estimate | 2.18 t |  |  |  |  | not computed |
| RevRecTiming_pp | estimate | 1.9 pp |  |  |  |  | not computed |
| RevRecTiming_t | estimate | 2.64 t |  |  |  |  | not computed |
| RevRecModal_pct | estimate | 72% |  |  |  |  | not computed |
| RevExactTiming_pp | estimate | 2.12 pp |  |  |  |  | not computed |
| RevExactTiming_t | estimate | 2.95 t |  |  |  |  | not computed |
| RevExactMeanDiff | estimate | 0.0086 |  |  |  |  | not computed |
| RevExactMaxDiff | estimate | 0.07 |  |  |  |  | not computed |
| RevExactMeanShift | estimate | 0.026 |  |  |  |  | not computed |
| RevExactSdRatio | estimate | 0.996 |  |  |  |  | not computed |
| RevExactRhatMax | estimate | 1.005 |  |  |  |  | not computed |
| RevExactMcseMax | estimate | 0.0037 |  |  |  |  | not computed |
| RevExactMcseMedian | estimate | 0.0014 |  |  |  |  | not computed |
| RevExactMinRank | estimate | 113 |  |  |  |  | not computed |
| RevExactAccept_pct | estimate | 95% |  |  |  |  | not computed |
| RevExactDates | count | 605 months |  |  |  |  | not computed |
| Factor_SMB_timing_pp | estimate | 0.625 pp | 0.598 |  | 605 |  | no standard error |
| Factor_HML_timing_pp | estimate | 0.758 pp | 0.7712 |  | 605 |  | no standard error |
| Factor_CMA_timing_pp | estimate | 0.078 pp | 0.07244 |  | 605 |  | no standard error |
| Factor_RMW_timing_pp | estimate | 0.046 pp | 0.03028 |  | 605 |  | no standard error |
| Factor_UMD_timing_pp | estimate | 0.573 pp | 0.586 |  | 605 |  | no standard error |

## The paper's own numbers
- FLAG: Decade_timing_breakdown: -0.14 + 0.79 + 2.93 + -0.06 + 0.72 + 1.89 = 6.13, paper's total 2.08
- OK: Factor_contribution_to_timing: 0.625 + 0.758 + 0.078 + 0.046 + 0.573 = 2.08, paper's total 2.08
- FLAG: Predictor_set_sensitivity_alternative_timings: 0.87 + 1.22 + 1.17 + 4.42 = 7.68, paper's total 2.08
- FLAG: Mandate_grid_sensitivity_range: 1.38 + 3.7 = 5.08, paper's total 2.08
- NOTE: Constant_timing: t = 0.08 and p = 0.33 fit no side at the printed precision (two-sided p would be 0.9363); judged two-sided
- NOTE: MinVar_timing: t = 0.11 and p = 0.15 fit no side at the printed precision (two-sided p would be 0.9124); judged two-sided
- NOTE: Kappa80_net_Sharpe_vs_constant: t = 1.118 and p = 0.79 fit no side at the printed precision (two-sided p would be 0.2640); judged two-sided
- NOTE: Recursive_penalized_net_Sharpe_vs_constant: t = 1.121 and p = 0.83 fit no side at the printed precision (two-sided p would be 0.2627); judged two-sided
- NOTE: BPPP_vs_Constant_Sharpe_Holm: t = 1.242 and p = 0.953 fit no side at the printed precision (two-sided p would be 0.2147); judged two-sided
- NOTE: BPPP_vs_RPPP_Sharpe_Holm: t = 1.242 and p = 0.953 fit no side at the printed precision (two-sided p would be 0.2147); judged two-sided

## Guards
- no claims rejected
- spec: the headline was written as prose ('BPPP earns 2.08 pp per year from timing (t=3.00, share 29.5% of active 7.05pp, gross SR 1.242) vs constant allocation ti'); chosen from the claim names: BPPP_timing_pp
- spec problem unresolved: headline 'BPPP_timing_pp, BPPP_timing_t' is not the name of a claim
- round 1: the builder ran out of turns
- round 1: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (RevExactDates (605) at line 297). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- round 2: audit sent the sample back: the replication's sample covers 1973-08-31 to 2023-12-31, but the paper's runs from July 1963 to December 2023
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 726, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: French data 202609 CRSP vintage (vs paper 202312 Dec vintage); OSAP PredictorLSretWide.parquet Data-Release-2026.10 CC BY 4.0 (vs earlier release) 212 cols same count; factor-specific predictors built per Appendix with 12m/36m/60m lookbacks; omega calibrated via diagonal trace-matching two-pass Newton on kernel K_ss'=(F'F)(z'Lambda^{-1}z); market_data module not used, direct HTTP fetch used; turnover/holding costs phi 60/25/30/30/70bps h 90/40/45/45/80bps charged at factor level as in paper
- caveat: sample size not rebuilt: exact posterior HMC in rank(K)<=T via 32 chains 300 burn 700 retained not rebuilt - Laplace approximation used, so exact timing/MCSE/Rhat not computed (RevExactDates, 605 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- market data: none used
- other hosts the script fetched from: mba.tuck.dartmouth.edu, huggingface.co, us.aws.cdn.hf.co

## Run
- sandbox: attempt 3, exit 0, 47.5s
- model calls: 45, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 3236649, out 166634 (reasoning 100043); cost $1.5486

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
