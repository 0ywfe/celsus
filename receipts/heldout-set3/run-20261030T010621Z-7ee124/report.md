The paper's numbers partly hold up: 7 of 15 checked results match within their uncertainty. Its main result, wf_gen_ratio_improvement_98pct, is 98% in the paper and 112.9% here (not judged: no standard error).

# paper-replicator report: arXiv 2602.00080
**The GT-Score: A Robust Objective Function for Reducing Overfitting in Data-Driven Trading Strategies**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| n_assets | count | 50 assets | 50 | 0 | 50 | True | precise: the paper's count |
| approx_trading_days_per_asset | count | 3770 days | 3774 |  | 50 | True | approximate: +0.1%, within SCORE's +/-15% |
| n_strategies | count | 3 strategies | 3 | 0 | 3 | True | precise: the paper's count |
| n_walkforward_splits_per_asset | count | 9 splits | 9 | 0 | 9 | True | precise: the paper's count |
| n_monte_carlo_seeds | parameter | 15 seeds | 15 | 0 | 15 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_monte_carlo_trials_total | parameter | 9000 trials | 9000 | 0 | 9000 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_walkforward_trials_total | count | 5340 trials | 5400 | 0 | 5400 | True | approximate: +1.1%, within SCORE's +/-15% |
| mc_gt_n | parameter | 2250 trials | 2250 | 0 | 2250 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| mc_sharpe_n | parameter | 2250 trials | 2250 | 0 | 2250 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| mc_sortino_n | parameter | 2250 trials | 2250 | 0 | 2250 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| mc_simple_n | parameter | 2250 trials | 2250 | 0 | 2250 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| wf_gt_n | count | 1335 trials | 1350 | 0 | 1350 | True | approximate: +1.1%, within SCORE's +/-15% |
| wf_sharpe_n | count | 1335 trials | 1350 | 0 | 1350 | True | approximate: +1.1%, within SCORE's +/-15% |
| wf_sortino_n | count | 1335 trials | 1350 | 0 | 1350 | True | approximate: +1.1%, within SCORE's +/-15% |
| wf_simple_n | count | 1335 trials | 1350 | 0 | 1350 | True | approximate: +1.1%, within SCORE's +/-15% |
| mc_gt_test_mean | estimate | 43.6% | 85.67 | 3.411 | 2250 | False | paper outside 85.67 +/- 6.685 |
| mc_gt_test_std | estimate | 62.6% | 161.8 |  | 2250 |  | no standard error |
| mc_gt_train_mean | estimate | 237.8% | 140.4 |  | 2250 |  | no standard error |
| mc_gt_gen_ratio | estimate | 0.183 ratio | 0.6103 |  | 2250 |  | no standard error |
| mc_sharpe_test_mean | estimate | 46.3% | 111.5 | 5.489 | 2250 | False | paper outside 111.5 +/- 10.76 |
| mc_sharpe_test_std | estimate | 71.7% | 260.4 |  | 2250 |  | no standard error |
| mc_sharpe_train_mean | estimate | 395.6% | 245.7 |  | 2250 |  | no standard error |
| mc_sharpe_gen_ratio | estimate | 0.117 ratio | 0.4539 |  | 2250 |  | no standard error |
| mc_sortino_test_mean | estimate | 49.3% | 101.5 | 5.097 | 2250 | False | paper outside 101.5 +/- 9.99 |
| mc_sortino_test_std | estimate | 76.2% | 241.8 |  | 2250 |  | no standard error |
| mc_sortino_train_mean | estimate | 421.4% | 228.7 |  | 2250 |  | no standard error |
| mc_sortino_gen_ratio | estimate | 0.117 ratio | 0.4438 |  | 2250 |  | no standard error |
| mc_simple_test_mean | estimate | 49.5% | 115.8 | 5.194 | 2250 | False | paper outside 115.8 +/- 10.18 |
| mc_simple_test_std | estimate | 76.2% | 246.4 |  | 2250 |  | no standard error |
| mc_simple_train_mean | estimate | 428% | 256.8 |  | 2250 |  | no standard error |
| mc_simple_gen_ratio | estimate | 0.116 ratio | 0.451 |  | 2250 |  | no standard error |
| mc_gen_ratio_improvement_56pct | estimate | 56% | 35.76 |  |  |  | no standard error |
| wf_gt_val_mean | estimate | 18.5% | 19.37 | 0.7803 | 1350 | True | paper inside 19.37 +/- 1.529 |
| wf_gt_val_std | estimate | 37.1% | 28.67 |  | 1350 |  | no standard error |
| wf_gt_train_mean | estimate | 50.7% | 44.59 |  | 1350 |  | no standard error |
| wf_gt_gen_ratio | estimate | 0.365 ratio | 0.4345 |  | 1350 |  | no standard error |
| wf_sharpe_val_mean | estimate | 17.1% | 19.79 | 0.8421 | 1350 | False | paper outside 19.79 +/- 1.65 |
| wf_sharpe_val_std | estimate | 34.1% | 30.94 |  | 1350 |  | no standard error |
| wf_sharpe_train_mean | estimate | 95.2% | 102 |  | 1350 |  | no standard error |
| wf_sharpe_gen_ratio | estimate | 0.18 ratio | 0.1939 |  | 1350 |  | no standard error |
| wf_sortino_val_mean | estimate | 18.6% | 19.48 | 0.869 | 1350 | True | paper inside 19.48 +/- 1.703 |
| wf_sortino_val_std | estimate | 35% | 31.93 |  | 1350 |  | no standard error |
| wf_sortino_train_mean | estimate | 99.9% | 94.33 |  | 1350 |  | no standard error |
| wf_sortino_gen_ratio | estimate | 0.186 ratio | 0.2065 |  | 1350 |  | no standard error |
| wf_simple_val_mean | estimate | 19% | 22.95 | 0.9164 | 1350 | False | paper outside 22.95 +/- 1.796 |
| wf_simple_val_std | estimate | 35.4% | 33.67 |  | 1350 |  | no standard error |
| wf_simple_train_mean | estimate | 100.9% | 108.2 |  | 1350 |  | no standard error |
| wf_simple_gen_ratio | estimate | 0.188 ratio | 0.212 |  | 1350 |  | no standard error |
| wf_baseline_avg_gen_ratio | estimate | 0.185 ratio | 0.2041 |  |  |  | no standard error |
| wf_gen_ratio_improvement_98pct | estimate | 98% | 112.9 |  |  |  | no standard error |
| ttest_gt_vs_sharpe_mean_diff | estimate | -0.028 proportion | -0.2583 |  | 2250 |  | no standard error |
| ttest_gt_vs_sharpe_tstat | estimate | -2.45 t | -4.659 |  | 2250 |  | no standard error |
| ttest_gt_vs_sharpe_p | p_value | 0.014 p | 3.359e-06 |  | 2250 | True | both < 0.05 |
| ttest_gt_vs_sharpe_d | estimate | -0.041 d | -0.09823 |  | 2250 |  | no standard error |
| ttest_gt_vs_sortino_mean_diff | estimate | -0.058 proportion | -0.1581 |  | 2250 |  | no standard error |
| ttest_gt_vs_sortino_tstat | estimate | -5.05 t | -3.172 |  | 2250 |  | no standard error |
| ttest_gt_vs_sortino_p | p_value | 0.001 p | 0.001535 |  | 2250 | True | both < 0.05 |
| ttest_gt_vs_sortino_d | estimate | -0.083 d | -0.06687 |  | 2250 |  | no standard error |
| ttest_gt_vs_simple_mean_diff | estimate | -0.06 proportion | -0.3012 |  | 2250 |  | no standard error |
| ttest_gt_vs_simple_tstat | estimate | -5.22 t | -6.443 |  | 2250 |  | no standard error |
| ttest_gt_vs_simple_p | p_value | 0.001 p | 1.426e-10 |  | 2250 | True | both < 0.05 |
| ttest_gt_vs_simple_d | estimate | -0.086 d | -0.1358 |  | 2250 |  | no standard error |
| wilcoxon_gt_vs_sharpe_p | p_value | 0.139 p | 7.331e-17 |  | 2250 | False | opposite sides of 0.05 |
| wilcoxon_gt_vs_sortino_p | p_value | 0.001 p | 3.858e-07 |  | 2250 | True | both < 0.05 |
| wilcoxon_gt_vs_simple_p | p_value | 0.001 p | 3.903e-24 |  | 2250 | True | both < 0.05 |
| regime_2014_2016_gt | estimate | 13.2% | 9.516 |  |  |  | no standard error |
| regime_2014_2016_baseline | estimate | 11.7% | 8.299 |  |  |  | no standard error |
| regime_2014_2016_delta | estimate | 1.5 pp | 1.218 |  |  |  | no standard error |
| regime_2015_2017_gt | estimate | 17% | 15.13 |  |  |  | no standard error |
| regime_2015_2017_baseline | estimate | 17.1% | 18.23 |  |  |  | no standard error |
| regime_2015_2017_delta | estimate | -0.1 pp | -3.103 |  |  |  | no standard error |
| regime_2016_2018_gt | estimate | 30.1% | 27.01 |  |  |  | no standard error |
| regime_2016_2018_baseline | estimate | 27.3% | 29.67 |  |  |  | no standard error |
| regime_2016_2018_delta | estimate | 2.8 pp | -2.658 |  |  |  | no standard error |
| regime_2017_2019_gt | estimate | 21% | 14.82 |  |  |  | no standard error |
| regime_2017_2019_baseline | estimate | 15.5% | 15.64 |  |  |  | no standard error |
| regime_2017_2019_delta | estimate | 5.5 pp | -0.813 |  |  |  | no standard error |
| regime_2018_2020_gt | estimate | 21% | 19.14 |  |  |  | no standard error |
| regime_2018_2020_baseline | estimate | 19% | 20.59 |  |  |  | no standard error |
| regime_2018_2020_delta | estimate | 2 pp | -1.456 |  |  |  | no standard error |
| regime_2019_2021_gt | estimate | 24.7% | 27.85 |  |  |  | no standard error |
| regime_2019_2021_baseline | estimate | 24.7% | 26.7 |  |  |  | no standard error |
| regime_2019_2021_delta | estimate | 0 pp | 1.147 |  |  |  | no standard error |
| regime_2020_2022_gt | estimate | 21.4% | 32.02 |  |  |  | no standard error |
| regime_2020_2022_baseline | estimate | 29.3% | 36.75 |  |  |  | no standard error |
| regime_2020_2022_delta | estimate | -7.9 pp | -4.727 |  |  |  | no standard error |
| regime_2021_2023_gt | estimate | 7% | 14.02 |  |  |  | no standard error |
| regime_2021_2023_baseline | estimate | 7.2% | 13.21 |  |  |  | no standard error |
| regime_2021_2023_delta | estimate | -0.2 pp | 0.8149 |  |  |  | no standard error |
| regime_2022_2024_gt | estimate | 10.6% | 14.86 |  |  |  | no standard error |
| regime_2022_2024_baseline | estimate | 11.6% | 17.54 |  |  |  | no standard error |
| regime_2022_2024_delta | estimate | -1 pp | -2.677 |  |  |  | no standard error |
| strat_rsi_gt | estimate | 44% | 81.56 |  |  |  | no standard error |
| strat_rsi_sharpe | estimate | 49.2% | 144.2 |  |  |  | no standard error |
| strat_rsi_sortino | estimate | 59.4% | 123.2 |  |  |  | no standard error |
| strat_rsi_simple | estimate | 59.1% | 165.5 |  |  |  | no standard error |
| strat_macd_gt | estimate | 42.4% | 98.05 |  |  |  | no standard error |
| strat_macd_sharpe | estimate | 43.8% | 104.4 |  |  |  | no standard error |
| strat_macd_sortino | estimate | 43.7% | 100.3 |  |  |  | no standard error |
| strat_macd_simple | estimate | 43.8% | 98.41 |  |  |  | no standard error |
| strat_boll_gt | estimate | 44.2% | 77.41 |  |  |  | no standard error |
| strat_boll_sharpe | estimate | 46% | 85.9 |  |  |  | no standard error |
| strat_boll_sortino | estimate | 45% | 80.89 |  |  |  | no standard error |
| strat_boll_simple | estimate | 45.7% | 83.46 |  |  |  | no standard error |
| mc_mean_trades_gt | estimate | 32.4 trades | 38.29 |  | 2250 |  | no standard error |
| mc_mean_trades_baseline | estimate | 21 trades | 29.46 |  |  |  | no standard error |
| abstract_p_lt_01_sortino_simple | p_value | 0.01 p | 1 |  |  | False | opposite sides of 0.05 |

## The paper's own numbers
- OK: Monte Carlo by objective: 2250 + 2250 + 2250 + 2250 = 9000, paper's total 9000
- OK: Walk-forward by objective: 1335 + 1335 + 1335 + 1335 = 5340, paper's total 5340
- OK: Paired t-test GT-Score vs Sharpe on Monte Carlo test returns (paired across trials): t = -2.45, paper's p = 0.014 matches two-sided (0.0143); two-sided p would be 0.0143
- OK: Paired t-test GT-Score vs Sortino on Monte Carlo test returns (paired across trials): t = -5.05, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000
- OK: Paired t-test GT-Score vs Simple on Monte Carlo test returns (paired across trials): t = -5.22, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000

## Guards
- no claims rejected
- spec: the headline was written as prose ('The paper's central conclusion is the walk-forward 98% generalization-ratio improvement for GT-Score vs baselines. Repli'); chosen from the claim names: wf_gen_ratio_improvement_98pct
- attempt 1: 1 market-data items fetched on the host into data/market
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 50, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Market-cap ranking as of fetch date (proxied top 50 with history). Parameter search spaces not stated in paper – used standard ranges. Monte Carlo split window not stated – used 2010-2018 train, 2019-2024 test with 30d embargo. Bollinger position logic vectorized, RSI smoothed via Wilder EMA, downside deviation target 0, risk-free 0. Standard Sharpe/Sortino annualized sqrt252

## Data sources
- market_cap: yfinance (host) (cache), fetched 2026-10-30, 1 tickers
- market_cap: yfinance (live, sandbox), fetched 2026-10-30, 138 tickers
- prices: yfinance (live, sandbox), fetched 2026-10-30, 87 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 1, exit 0, 191.3s, with the packages the builder installed: llvmlite==0.50.0, numba==0.68.1
- model calls: 21, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 615742, out 101254 (reasoning 69525); cost $0.6648

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
