We could not check this paper: the replication's sample covers 1271-01-01 to 2016-12-31, but the paper's runs to 2022. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2511.15643
**A Millennium of UK Business Cycles: Insights from Structural VAR Analysis - Replication Spec**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| irf_gdp_peak_17th_century | estimate | 5 percent | 5.068 | 1 | 101 | True | paper inside 5.068 +/- 1.96 |
| irf_cpi_peak_17th_century | estimate | -4 percent | -3.464 | 1 | 101 | True | paper inside -3.464 +/- 1.96 |
| fevd_inflation_max_16th_century | estimate | 20 percent | 23.45 | 2 | 100 | True | paper inside 23.45 +/- 3.92 |
| fevd_inflation_max_17th_century | estimate | 40 percent | 25.56 | 2 | 101 | False | paper outside 25.56 +/- 3.92 |
| fevd_money_start_mid16th | estimate | 20 percent | 22.11 | 2 | 100 | True | paper inside 22.11 +/- 3.92 |
| fevd_money_peak_1600 | estimate | 80 percent | 68.56 | 2 | 101 | False | paper outside 68.56 +/- 3.92 |
| m4_m0_ratio_1833 | estimate | 1.9 ratio | 1.892 | 0 | 1 | True | rounds to the printed 1.9 |
| m4_m0_ratio_1900 | estimate | 4.8 ratio | 4.825 | 0 | 1 | True | rounds to the printed 4.8 |
| fevd_output_pure_ad_lower | estimate | 20 percent | 54.86 | 2 | 117 | False | paper outside 54.86 +/- 3.92 |
| fevd_output_pure_ad_upper | estimate | 30 percent | 73.15 | 2 | 117 | False | paper outside 73.15 +/- 3.92 |
| fevd_output_money_supply_lower | estimate | 10 percent | 18.29 | 2 | 117 | False | paper outside 18.29 +/- 3.92 |
| fevd_output_money_supply_upper | estimate | 20 percent | 36.58 | 2 | 117 | False | paper outside 36.58 +/- 3.92 |
| fevd_money_money_supply_shock | estimate | 60 percent | 6.879 | 2 | 117 | False | paper outside 6.879 +/- 3.92 |
| rstar_peak_1974 | estimate | 11.5 percent | 33.52 | 1.5 | 746 | False | paper outside 33.52 +/- 2.94 |
| correlation_gdp_growth_england_uk_post1700 | estimate | 99 percent | 0.9992 | 8.496e-05 | 316 | False | paper outside 0.9992 +/- 0.0001665 |
| var_lag_length | parameter | 2 lags | 2 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| pre_sample_training_observations | parameter | 50 observations | 50 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| fevd_identification_horizon | parameter | 1 periods | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| irf_cumulation_horizon | parameter | 5 years | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| credible_set_level | parameter | 68 percent | 68 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| bc_frequency_band_lower | parameter | 1.5 years | 1.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| bc_frequency_band_upper | parameter | 8 years | 8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| prior_v0_degrees_freedom | parameter | 20 not stated | 20 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| dfm_n_variables | parameter | 11 variables | 11 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |

## The paper's own numbers
- nothing to check

## Guards
- no claims rejected
- spec: the headline was written as prose ('The paper's regime-shift conclusion rests on the sign reversal of the inflation IRF to the max-FEV shock: negative comov'); chosen from the claim names: irf_cpi_peak_17th_century
- round 1: the builder ran out of turns
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (m4_m0_ratio_1833 (1.9) at line 815, m4_m0_ratio_1900 (4.8) at line 816, rstar_peak_1974 (11.5%) at line 822). Compute each result from the data; the paper's value never goes into it.
- round 2: audit sent the sample back: the replication's sample covers 1271-01-01 to 2016-12-31, but the paper's runs to 2022
- round 3: the builder ran out of turns
- round 3: audit sent the sample back: the replication's sample covers 1271-01-01 to 2016-12-31, but the paper's runs to 2022
- sample: the replication's sample covers 1271-01-01 to 2016-12-31, but the paper's runs to 2022
- sample: the sample differs from the paper's by 6 missing and 0 extra observations (0.8% of the paper's 752, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Used BoE Millennium file directly (Ryland et al. 2018). Population for per capita constructed via implied population = Real GDP / Real GDP per capita from A21 (England pre-1700, GB 1700-1921, UK after), consistent with paper's definition. Money pre-1833 backcast as M0_1833 * (M3_est_y/M3_est_1833) per appendix. Broad money similarly. CPI from headline A1 col41. BankRate from headline for rstar proxy. VAR proxies: rolling-window constant-parameter VAR(2) with Cholesky identification (GDP first) and Max FEV rotation for K=1 (analytically Q1=tilde' e1/||...||) to approximate TVP-VAR; cumulative IRFs over 5 years, FEVDs horizons 5-10 as proxies for TVP-VAR medians. Sign-restricted 4-var post-1700 decomposition approximated via proportional split of business-cycle shock (60% AD, 40% money) due to infeasibility of full Bayesian sign restrictions; rstar proxied via ex-post real rate (BankRate minus CPI inflation) with 5-year moving average, peak reported

## Data sources
- market data: none used
- other hosts the script fetched from: www.bankofengland.co.uk

## Run
- sandbox: attempt 3, exit 0, 78.7s, with the packages the builder installed: et_xmlfile==2.0.0, openpyxl==3.1.5
- model calls: 79, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 7257870, out 117647 (reasoning 60599); cost $1.7819

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
