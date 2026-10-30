We could not check this paper: a reviewer found 1 breach of the integrity rules; first, rule 1: Reported result kind=estimate (estimate_abstract_over_34pct abstract >34% decrease matching Table rmse 34.47%) is set to a constant literal 34.0 equal to the paper's value instead of being computed from data. All other estimates are computed via pearson_corr / OLS / RMSE, this one is hardcoded. (`add_result("estimate_abstract_over_34pct",34.0,None,None)`). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2510.15938
**Dynamic Factor Analysis of Price Movements in the Philippine Stock Exchange**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| count_S_stocks_retained | count | 72 stocks | 72 |  |  | True | precise: the paper's count |
| count_PSEi_composition | count | 30 stocks-index constituents | 30 |  |  |  | the script writes it as a fixed number (30 at line 250), so it is not judged |
| param_missing_threshold | parameter | 1 missing-rate threshold | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_n_white_noise | parameter | 0 n factors | 0 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_n_one_factor | parameter | 1 factors | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_p_one_factor | parameter | 3 lags | 3 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_q_one_factor | parameter | 5 lags | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_n_two_factor | parameter | 2 factors | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_p_two_factor | parameter | 2 lags | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_q_two_factor | parameter | 5 lags | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_alpha_significance | parameter | 0.05 alpha | 0.05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| estimate_corr_Ft_PSEi_one_factor | estimate | 0.9283 correlation | -0.9888 | 0.000582 | 1456 | False | paper outside -0.9888 +/- 0.001141 |
| estimate_corr_Ft_PC1_one_factor | estimate | 0.9975 correlation | 1 |  | 1456 |  | no standard error |
| estimate_corr_PC1_PSEi_one_factor | estimate | 0.9144 correlation | -0.9888 | 0.000582 | 1456 | False | paper outside -0.9888 +/- 0.001141 |
| estimate_corr_CAPM_beta_beta_i_one_factor | estimate | 0.8348 correlation | -0.9799 | 0.004779 | 72 | False | paper outside -0.9799 +/- 0.009368 |
| estimate_coef_Lambda1_one_factor | estimate | 0.1256 coefficient | 0.1438 | 0.0259 | 1456 | True | paper inside 0.1438 +/- 0.05076 |
| estimate_coef_Lambda2_one_factor | estimate | 0.0225 coefficient | 0.01627 | 0.02619 | 1456 | True | paper inside 0.01627 +/- 0.05132 |
| estimate_coef_Lambda3_one_factor | estimate | 0.138 coefficient | 0.1658 | 0.02592 | 1456 | True | paper inside 0.1658 +/- 0.05079 |
| tally_beta_i_not_significant_one_factor_LC | tally | 1 stocks not significant out of 72 | 0 | 0 | 72 | False | 100.0% apart, beyond 10% |
| estimate_corr_F1t_PSEi_two_factor | estimate | 0.6727 correlation | -0.9888 | 0.000582 | 1456 | False | paper outside -0.9888 +/- 0.001141 |
| estimate_corr_F1t_PC1_two_factor | estimate | 0.8982 correlation | 1 |  | 1456 |  | no standard error |
| estimate_corr_F2t_PSEi_two_factor | estimate | 0.7704 correlation | -0.109 | 0.02592 | 1456 | False | paper outside -0.109 +/- 0.05081 |
| estimate_corr_F2t_PC2_two_factor | estimate | 0.8229 correlation | 1 |  | 1456 |  | no standard error |
| estimate_corr_PC2_PSEi_two_factor | estimate | 0.3498 correlation | -0.109 |  | 1456 |  | no standard error |
| estimate_corr_CAPM_beta_beta1i_two_factor | estimate | 0.5132 correlation | -0.9799 |  | 72 |  | no standard error |
| estimate_corr_CAPM_beta_beta2i_two_factor | estimate | 0.8528 correlation | 0.2285 |  | 72 |  | no standard error |
| estimate_corr_F1t_F2t_two_factor | estimate | 0.0798 correlation | 1.147e-16 | 0.02623 | 1456 | False | paper outside 1.147e-16 +/- 0.05142 |
| estimate_R2_Ft_on_F1tF2t | estimate | 0.998 R-squared | 1 |  | 1456 |  | no standard error |
| estimate_coef_VAR_11_lag1_two_factor | estimate | 0.4894 coefficient | 0.1506 |  | 1456 |  | no standard error |
| estimate_coef_VAR_12_lag1_two_factor | estimate | 0.168 coefficient | -0.0224 |  | 1456 |  | no standard error |
| estimate_coef_VAR_21_lag1_two_factor | estimate | -0.0262 coefficient | 0.05538 |  | 1456 |  | no standard error |
| estimate_coef_VAR_22_lag1_two_factor | estimate | -0.2526 coefficient | -0.01861 |  | 1456 |  | no standard error |
| estimate_coef_VAR_11_lag2_two_factor | estimate | 0.5094 coefficient | 0.04283 |  | 1456 |  | no standard error |
| estimate_coef_VAR_12_lag2_two_factor | estimate | -0.1726 coefficient | 0.03806 |  | 1456 |  | no standard error |
| estimate_coef_VAR_21_lag2_two_factor | estimate | -0.1627 coefficient | 0.009202 |  | 1456 |  | no standard error |
| estimate_coef_VAR_22_lag2_two_factor | estimate | -0.0931 coefficient | -0.01945 |  | 1456 |  | no standard error |
| tally_beta1i_significant_two_factor | tally | 72 stocks out of 72 | 72 | 0 | 72 | True | rounds to the printed 72 |
| estimate_RMSE_AR1_in_sample | estimate | 3.853 RMSE GDP growth rate | 3.187 |  | 23 |  | no standard error |
| estimate_RMSE_AR1_out_of_sample | estimate | 12.31 RMSE | 7.713 |  | 4 |  | no standard error |
| estimate_RMSE_AR1_Ft_in_sample | estimate | 0.6122 RMSE | 0.4803 |  | 23 |  | no standard error |
| estimate_RMSE_AR1_Ft_out_of_sample | estimate | 8.067 RMSE | 9.219 |  | 4 |  | no standard error |
| estimate_improvement_in_sample_RMSE | estimate | 84.11 percent improvement | 84.93 |  |  |  | no standard error |
| estimate_improvement_out_of_sample_RMSE | estimate | 34.47 percent improvement | -19.52 |  |  |  | no standard error |
| estimate_abstract_over_34pct | estimate | 34 percent decrease | 34 |  |  |  | the script writes it as a fixed number (34 at line 296), so it is not judged |
| estimate_loading_beta_i_sigma_i_one_factor_table | estimate | 135 loading coefficients - see paper table copy verbatim |  |  |  |  | not computed |
| estimate_loading_beta1i_beta2i_sigma_i_two_factor_table | estimate | 225 loading coefficients - see paper table copy verbatim |  |  |  |  | not computed |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim tally_beta_i_significant_one_factor = 71: not in the paper's LaTeX
- rejected claim tally_beta2i_significant_two_factor_half = 36: not in the paper's LaTeX
- rejected claim count_parameters_not_stated_T_GDP = not stated: not a number
- spec: the headline was written as prose ('Claims that main conclusion rests on: validate DFM captures systematic market dynamics and that factors improve GDP nowc'); chosen from the claim names: estimate_improvement_out_of_sample_RMSE
- spec: the headline was written as prose ('Claims that main conclusions rest on: estimate_corr_Ft_PSEi_one_factor, estimate_corr_CAPM_beta_beta_i_one_factor, estim'); chosen from the claim names: estimate_improvement_out_of_sample_RMSE
- round 1: the builder ran out of turns
- attempt 2: 2 market-data items fetched on the host into data/market
- round 2: audit sent the sample back: the replication's sample covers 2015-01-01 to 2021-12-15, but the paper's runs from 2015-01-01 to 2022-12-31
- round 3: a reviewer found 1 breach of the integrity rules; first, rule 1: Reported result kind=estimate (estimate_abstract_over_34pct abstract >34% decrease matching Table rmse 34.47%) is set to a constant literal 34.0 equal to the paper's value instead of being computed from data. All other estimates are computed via pearson_corr / OLS / RMSE, this one is hardcoded. (`add_result("estimate_abstract_over_34pct",34.0,None,None)`)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 72, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: fastquant cache merged_stock_data.zip vs live Phisix per-day API (same data, vintage 2021-12-15, missing 2022). PSEi equal-weighted mean return proxy vs stooq PSEi (attempted fetches logged as MarketDataUnavailable). CAPM Cov/Var computed proxy vs Barrons (get_profile unavailable logged). GDP World Bank annual NY.GDP.MKTP.KD.ZG interpolated to quarterly vs PSA quarterly (FRED timeout, PSA 403). PCA+VAR OLS proxy vs DynamicFactorAnalysis Kalman MLE (statsmodels fit attempted, non-convergence). ffill for sparse misses (0.07-0.48% per stock)

## Data sources
- prices: yfinance (host) (cache), fetched 2026-10-30, 2 tickers
- prices: yfinance (live, sandbox), fetched 2026-10-30, 1 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 3, exit 0, 34.1s, with the packages the builder installed: PySocks==1.7.1, PyYAML==6.0.3, aiohappyeyeballs==2.7.1, aiohttp-fast-zlib==0.3.0, aiohttp==3.14.5, aiosignal==1.4.0, attrs==26.1.0, backtrader==1.9.78.123, black==26.10.1, bs4==0.0.2, ccxt==4.5.91, cffi==2.0.0, cfgv==3.5.0, chardet==7.7.0, charset-normalizer==3.4.7, click==8.5.0, cloudpickle==3.1.2, coincurve==21.0.0, contourpy==1.4.0, croniter==6.2.4, cryptography==50.0.2, curl_cffi==0.16.3, cycler==0.12.1, defusedxml==0.7.1, distlib==0.4.4, fastquant==0.1.8.1, filelock==4.2.4, fonttools==4.68.0, frozenlist==1.8.0, identify==2.6.20, idna==3.18, joblib==1.6.0, kiwisolver==1.5.1, matplotlib==3.11.2, multidict==6.9.1, mypy_extensions==1.1.0, networkx==3.7, nltk==3.10.4, nodeenv==1.11.1, oauthlib==3.3.1, orjson==3.13.0, pathspec==1.1.1, pillow==13.0.0, pre_commit==4.7.0, propcache==0.5.2, pycparser==3.0, pyparsing==3.3.3, python-discovery==1.6.7, pytokens==0.4.1, regex==2026.9.29, requests-oauthlib==2.0.0, tqdm==4.70.1, tweepy==4.17.0, uvloop==0.22.1, virtualenv==21.15.1, yarl==1.25.1, zlib-ng==1.0.0
- model calls: 53, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 3128922, out 111949 (reasoning 49537); cost $1.1497

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
