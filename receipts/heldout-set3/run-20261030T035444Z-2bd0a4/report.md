We could not check this paper: the replication could not rebuild the paper's sample (79 missing and 0 extra observations: Paper total 202 importer-month observations (monthly, 2009-2023, many months with zero trade omitted). Replication uses annual frequency (one observation per importer-year) from OEC/BACI, giving 123 importer-year rows vs 202 importer-months; per-period counts therefore differ in time granularity but reflect same underlying trade flows. Annual aggregation loses within-year FX variation; period boundaries approximated annually (2013-2016 for P2, 2017-2019 for P3, 2020-2023 for P4) vs paper's exact monthly splits (Jan2013-Apr2017 etc.)); and the replication could not rebuild the paper's sample (n_obs_p1: 25 here, 52 in the paper; n_obs_p4: 27 here, 49 in the paper; n_obs_p2: 45 here, 64 in the paper, and 4 more). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2608.08690
**Price Responses of Rwandan Tungsten Exports under Conflict Minerals Regulation ---Period-by-Period Estimation of Export Demand Elasticity---**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| beta_p1 | estimate | -19.81 log-log coefficient | -3.038 | 12.47 | 25 | True | paper inside -3.038 +/- 24.44 |
| se_beta_p1 | estimate | 4.536 SE | 12.47 |  | 25 |  | no standard error |
| beta_p2 | estimate | 2.814 log-log coefficient | -0.8515 | 16.58 | 45 | True | paper inside -0.8515 +/- 32.5 |
| se_beta_p2 | estimate | 2.315 SE | 16.58 |  | 45 |  | no standard error |
| beta_p3 | estimate | -4.277 log-log coefficient | -0.7465 | 9.302 | 26 | True | paper inside -0.7465 +/- 18.23 |
| se_beta_p3 | estimate | 0.381 SE | 9.302 |  | 26 |  | no standard error |
| se_beta_p4 | estimate | 0.913 SE | 14.91 |  | 27 |  | no standard error |
| gamma_p1 | estimate | 0.307 log-log coefficient | -0.1659 | 0.4565 | 25 | True | paper inside -0.1659 +/- 0.8947 |
| se_gamma_p1 | estimate | 0.159 SE | 0.4565 |  | 25 |  | no standard error |
| gamma_p2 | estimate | 0.354 log-log coefficient | -0.5176 | 1.277 | 45 | True | paper inside -0.5176 +/- 2.503 |
| se_gamma_p2 | estimate | 0.156 SE | 1.277 |  | 45 |  | no standard error |
| gamma_p3 | estimate | -0.697 log-log coefficient | 3.339 | 1.829 | 26 | False | paper outside 3.339 +/- 3.585 |
| se_gamma_p3 | estimate | 1.062 SE | 1.829 |  | 26 |  | no standard error |
| gamma_p4 | estimate | -0.036 log-log coefficient | -1.694 | 2.358 | 27 | True | paper inside -1.694 +/- 4.623 |
| se_gamma_p4 | estimate | 0.182 SE | 2.358 |  | 27 |  | no standard error |
| eta_p1 | estimate | -20.81 elasticity | -4.038 | 12.47 | 25 | True | paper inside -4.038 +/- 24.44 |
| eta_p1_ci_lo | estimate | -29.7 elasticity | -28.48 | 12.47 | 25 | True | paper inside -28.48 +/- 24.44 |
| eta_p1_ci_hi | estimate | -11.92 elasticity | 20.4 | 12.47 | 25 | False | paper outside 20.4 +/- 24.44 |
| eta_p2 | estimate | 1.814 elasticity | -1.851 | 16.58 | 45 | True | paper inside -1.851 +/- 32.5 |
| eta_p2_ci_lo | estimate | -2.723 elasticity | -34.36 | 16.58 | 45 | True | paper inside -34.36 +/- 32.5 |
| eta_p2_ci_hi | estimate | 6.351 elasticity | 30.65 | 16.58 | 45 | True | paper inside 30.65 +/- 32.5 |
| eta_p3 | estimate | -5.277 elasticity | -1.747 | 9.302 | 26 | True | paper inside -1.747 +/- 18.23 |
| eta_p3_ci_lo | estimate | -6.024 elasticity | -19.98 | 9.302 | 26 | True | paper inside -19.98 +/- 18.23 |
| eta_p3_ci_hi | estimate | -4.531 elasticity | 16.49 | 9.302 | 26 | False | paper outside 16.49 +/- 18.23 |
| eta_p4_ci_hi | estimate | 2.229 elasticity | 9.368 | 14.91 | 27 | True | paper inside 9.368 +/- 29.22 |
| n_obs_p1 | count | 52 observations | 25 |  | 25 | False | -51.9%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-14.1), a band no published standard uses |
| n_importers_p1 | count | 4 countries | 10 |  | 25 | False | +150.0%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-3.9), a band no published standard uses |
| n_obs_p2 | count | 64 observations | 45 |  | 45 | False | -29.7%, beyond SCORE's +/-15% |
| n_importers_p2 | count | 7 countries | 19 |  | 45 | False | +171.4%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-5.2), a band no published standard uses |
| n_obs_p3 | count | 37 observations | 26 |  | 26 | True | -29.7%, beyond SCORE's +/-15%, but the difference -11 is within 1.96 sqrt(n) (+/-11.9), a band no published standard uses |
| n_importers_p3 | count | 4 countries | 12 |  | 26 | False | +200.0%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-3.9), a band no published standard uses |
| n_obs_p4 | count | 49 observations | 27 |  | 27 | False | -44.9%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-13.7), a band no published standard uses |
| n_importers_p4 | count | 5 countries | 13 |  | 27 | False | +160.0%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-4.4), a band no published standard uses |
| omega_est | estimate | 0.04384 coefficient | 0.1677 | 0.03568 | 123 | False | paper outside 0.1677 +/- 0.06993 |
| omega_ci_lo | estimate | -0.00829 coefficient | 0.09776 |  | 123 |  | no standard error |
| omega_ci_hi | estimate | 0.09597 coefficient | 0.2376 |  | 123 |  | no standard error |
| p_eta_p1 | p_value | 0.01 p-value threshold | 0.8075 |  | 25 | False | opposite sides of 0.05 |
| p_eta_p2 | p_value | 0.1 p-value threshold | 0.9591 |  | 45 | True | both >= 0.05 |
| p_eta_p3 | p_value | 0.01 p-value threshold | 0.936 |  | 26 | False | opposite sides of 0.05 |
| p_eta_p4 | p_value | 0.1 p-value threshold | 0.2061 |  | 27 | True | both >= 0.05 |
| p_omega | p_value | 0.05 p-value threshold | 2.6e-06 |  | 123 | False | opposite sides of 0.05 |
| diff_p2_p1 | estimate | 22.63 coefficient difference | 2.187 | 22.39 | 70 | True | paper inside 2.187 +/- 43.88 |
| se_diff_p2_p1 | estimate | 5.665 SE | 22.39 |  | 70 |  | no standard error |
| t_diff_p2_p1 | estimate | 3.994 t-statistic | 0.09768 |  | 70 |  | no standard error |
| p_diff_p2_p1 | p_value | 0.0021 p-value | 0.9233 |  | 70 | False | opposite sides of 0.05 |
| diff_p3_p1 | estimate | 15.54 coefficient difference | 2.292 | 15.99 | 51 | True | paper inside 2.292 +/- 31.34 |
| se_diff_p3_p1 | estimate | 4.162 SE | 15.99 |  | 51 |  | no standard error |
| t_diff_p3_p1 | estimate | 3.733 t-statistic | 0.1433 |  | 51 |  | no standard error |
| p_diff_p3_p1 | p_value | 0.0097 p-value | 0.8881 |  | 51 | False | opposite sides of 0.05 |
| diff_p4_p1 | estimate | 21.25 coefficient difference | -15.81 | 21.5 | 52 | True | paper inside -15.81 +/- 42.14 |
| se_diff_p4_p1 | estimate | 4.063 SE | 21.5 |  | 52 |  | no standard error |
| p_diff_p4_p1_table | p_value | 0.0008 p-value | 0.4717 |  | 52 | False | opposite sides of 0.05 |
| p_diff_p4_p1_text | p_value | 0.001 p-value threshold | 0.4717 |  | 52 | False | opposite sides of 0.05 |
| diff_p4_p3 | estimate | 5.717 coefficient difference | -18.1 | 13.81 | 53 | True | paper inside -18.1 +/- 27.06 |
| t_diff_p4_p3 | estimate | 5.955 t-statistic | -1.311 |  | 53 |  | no standard error |
| p_diff_p4_p3_table | p_value | 0.0006 p-value | 0.2084 |  | 53 | False | opposite sides of 0.05 |
| p_diff_p4_p3_text | p_value | 0.001 p-value threshold | 0.2084 |  | 53 | False | opposite sides of 0.05 |

## The paper's own numbers
- OK: Wald/t test H0 beta_P1 = beta_P2 (equiv eta) from pooled importer x period FE clustered at importer level: t = 3.994, paper's p = 0.0021 matches two-sided (0.0001); two-sided p would be 0.0001
- OK: Wald/t test H0 beta_P1 = beta_P3: t = 3.733, paper's p = 0.0097 matches two-sided (0.0002); two-sided p would be 0.0002
- OK: Wald/t test H0 beta_P3 = beta_P4: t = 5.955, paper's p = 0.0006 matches two-sided (0.0000); two-sided p would be 0.0000
- OK: Individual significance beta/eta Period1 clustered at importer level: t = -19.814, paper's p = 0.01 matches two-sided (0.0000); two-sided p would be 0.0000
- NOTE: Individual significance beta/eta Period2: t = 2.814, paper's p = 0.1 matches one-sided (lower tail) (0.9968); two-sided p would be 0.0064
- OK: Individual significance beta/eta Period3: t = -4.277, paper's p = 0.01 matches two-sided (0.0001); two-sided p would be 0.0001
- NOTE: Inverse-supply omega=0 test lnUV on lnX with importer FE clustered: t = 0.04384, paper's p = 0.05 matches one-sided (upper tail) (0.4825); two-sided p would be 0.9650

## Guards
- rejected claim beta_p4 = 1.44: not in the paper's LaTeX
- rejected claim eta_p4 = 0.44: not in the paper's LaTeX
- rejected claim eta_p4_ci_lo = -1.35: not in the paper's LaTeX
- rejected claim n_obs_total = not stated: not a number
- rejected claim n_importers_total = not stated: not a number
- rejected claim omega_se = 0.0266: not in the paper's LaTeX
- rejected claim n_omega = not stated: not a number
- rejected claim t_diff_p4_p1 = 5.23: not in the paper's LaTeX
- rejected claim se_diff_p4_p3 = 0.96: not in the paper's LaTeX
- spec: the headline was written as prose ('Core finding is time-varying price responsiveness: significant negative elasticity in P1 and P3 but not P2/P4, with sign'); chosen from the claim names: p_diff_p2_p1
- spec: the headline was written as prose ('Main conclusion rests on time-varying price responsiveness: statistically significant negative eta in Period1 and Period'); chosen from the claim names: p_diff_p2_p1
- round 1: the builder ran out of turns
- round 2: rejected before the clean run: the code that writes these results contains the number the paper reports for them (beta_p1 (-19.814) at line 377, beta_p2 (2.814) at line 377, beta_p3 (-4.277) at line 377). Compute each result from the data; the paper's value never goes into it.
- round 3: the builder ran out of turns
- attempt 3: 1 market-data items fetched on the host into data/market
- round 3: audit sent the sample back: n_obs_p1: the paper reports 52, your run produced 25
- sample: the replication could not rebuild the paper's sample (79 missing and 0 extra observations: Paper total 202 importer-month observations (monthly, 2009-2023, many months with zero trade omitted). Replication uses annual frequency (one observation per importer-year) from OEC/BACI, giving 123 importer-year rows vs 202 importer-months; per-period counts therefore differ in time granularity but reflect same underlying trade flows. Annual aggregation loses within-year FX variation; period boundaries approximated annually (2013-2016 for P2, 2017-2019 for P3, 2020-2023 for P4) vs paper's exact monthly splits (Jan2013-Apr2017 etc.))
- caveat: the replication used other sources or methods for the paper's observations: UN Comtrade monthly mirror trade (importer-reported HS261100 Jan2009-Dec2023) substituted with OEC/BACI annual bilateral trade (CEPII harmonized, HS 261100 key 5261100) via public api.oec.world/tesseract (trade_i_baci_a_92 and a_12) due to Comtrade preview quota exhaustion (403 Out of call volume quota). FXTOP monthly tables substituted with yfinance daily forex via market_data.get_prices (USDRWF=X,RWF=X,EURRWF=X,USDCNY=X,USDJPY=X,USDINR=X etc.) annual-averaged, CUR per RWF via 1/RWFperCUR or cross CURperUSD/RWFperUSD with nearest-year interpolation. World price PtW = sum_i V_it / sum_i Q_it monthly substituted with same OEC global annual trade value/quantity for HS5261100. HS revision 1992 vs 2012 harmonized by using both cubes and deduplicating overlapping year 2012. Estimation method identical (FE OLS, clustered SE at importer, eta=beta-1, diff tests with importer x period FE and t_{G-1})
- caveat: the sample block's not_rebuilt: n_obs_total is no claim's name, so it excused nothing
- caveat: the sample block's not_rebuilt: n_importers_total is no claim's name, so it excused nothing

## Data sources
- prices: yfinance (host) (cache), fetched 2026-10-30, 1 tickers
- prices: yfinance (live, sandbox), fetched 2026-10-30, 25 tickers
- other hosts the script fetched from: api.oec.world

## Run
- sandbox: attempt 3, exit 0, 40.8s
- model calls: 69, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 4405509, out 120893 (reasoning 50674); cost $1.2888

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
