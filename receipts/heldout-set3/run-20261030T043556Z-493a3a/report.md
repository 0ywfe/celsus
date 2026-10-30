The paper's numbers partly hold up: 10 of 54 checked results match within their uncertainty. Its main result, qqq_vpmacd_total_pnl, is 8.832e+04 USD in the paper and 4.312e+04 USD here (not consistent).

# paper-replicator report: arXiv 2604.26063
**A Volume-Price-Adjusted MACD Trading Strategy with Sensitivity Calibration for U.S. Equity Indices**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| training_observations | count | 1259 trading days per instrument | 1259 |  | 1259 | True | precise: the paper's count |
| testing_observations_per_instrument | count | 791 trading days per instrument | 791 |  | 791 | True | precise: the paper's count |
| initial_capital | parameter | 1e+05 USD | 100000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| transaction_cost_one_way | parameter | 4 bps | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| trading_cost | parameter | 3 bps | 3 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| slippage | parameter | 1 bp | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| round_trip_cost | parameter | 8 bps | 8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ema_fast_window | parameter | 12 days | 12 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ema_slow_window | parameter | 26 days | 26 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| signal_window | parameter | 9 days | 9 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_range_low | parameter | 0.8 | 0.8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_range_high | parameter | 1 | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_step | parameter | 0.02 | 0.02 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_candidates | parameter | 11 | 11 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| bootstrap_resamples | parameter | 1000 | 1000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| bootstrap_block_length | parameter | 5 days | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| sharpe_annualization_factor | parameter | 252 | 252 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_opt_spy_macdpluslambda | parameter | 0.9 | 0.9 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_opt_spy_vpmacd | parameter | 0.88 | 0.88 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_opt_qqq_macdpluslambda | parameter | 0.84 | 0.84 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_opt_qqq_vpmacd | parameter | 0.98 | 0.98 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_opt_dia_macdpluslambda | parameter | 0.92 | 0.92 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_opt_dia_vpmacd | parameter | 0.86 | 0.86 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| spy_baseline_trades | estimate | 40 trades | 38 |  |  |  | no standard error |
| spy_baseline_win_rate | estimate | 50% | 52.63 | 0.081 | 38 | False | paper outside 52.63 +/- 0.1588 |
| spy_baseline_total_pnl | estimate | 1.361e+04 USD | 9698 | 0 | 791 | False | 28.8% apart, beyond 10% |
| spy_baseline_pnl_ratio | estimate | 1.39 | 1.2 | 0 | 38 | False | 13.7% apart, beyond 10% |
| spy_baseline_sharpe | estimate | 0.47 | 0.3849 | 0.03685 | 791 | False | paper outside 0.3849 +/- 0.07222 |
| spy_baseline_max_dd | estimate | -13.78% | 13.01 | 0 | 791 | False | 194.4% apart, beyond 10% |
| spy_baseline_expectancy | estimate | 19.39 USD | 286.9 | 498.6 | 38 | True | paper inside 286.9 +/- 977.1 |
| spy_macdpluslambda_trades | estimate | 36 trades | 29 |  |  |  | no standard error |
| spy_macdpluslambda_win_rate | estimate | 55.56% | 51.72 | 0.09279 | 29 | False | paper outside 51.72 +/- 0.1819 |
| spy_macdpluslambda_total_pnl | estimate | 5.269e+04 USD | 1.53e+04 | 0 | 791 | False | 71.0% apart, beyond 10% |
| spy_macdpluslambda_pnl_ratio | estimate | 2.98 | 1.51 | 0 | 29 | False | 49.3% apart, beyond 10% |
| spy_macdpluslambda_sharpe | estimate | 1.35 | 0.5771 | 0.0384 | 791 | False | paper outside 0.5771 +/- 0.07527 |
| spy_macdpluslambda_max_dd | estimate | -8.17% | 11.21 | 0 | 791 | False | 237.2% apart, beyond 10% |
| spy_macdpluslambda_expectancy | estimate | 121 USD | 571.4 | 678.7 | 29 | True | paper inside 571.4 +/- 1330 |
| spy_vpmacd_trades | estimate | 6 trades | 21 |  |  |  | no standard error |
| spy_vpmacd_win_rate | estimate | 50% | 71.43 | 0.09858 | 21 | False | paper outside 71.43 +/- 0.1932 |
| spy_vpmacd_total_pnl | estimate | 2.754e+04 USD | 3.213e+04 | 0 | 791 | False | 16.6% apart, beyond 10% |
| spy_vpmacd_pnl_ratio | estimate | 8.61 | 1.767 | 0 | 21 | False | 79.5% apart, beyond 10% |
| spy_vpmacd_sharpe | estimate | 0.96 | 0.7907 | 0.04074 | 791 | False | paper outside 0.7907 +/- 0.07984 |
| spy_vpmacd_max_dd | estimate | -6.33% | 9.142 | 0 | 791 | False | 244.4% apart, beyond 10% |
| spy_vpmacd_expectancy | estimate | 365.7 USD | 1486 | 600 | 21 | True | paper inside 1486 +/- 1176 |
| qqq_baseline_trades | estimate | 35 trades | 33 |  |  |  | no standard error |
| qqq_baseline_win_rate | estimate | 45.71% | 48.48 | 0.087 | 33 | False | paper outside 48.48 +/- 0.1705 |
| qqq_baseline_total_pnl | estimate | 1.682e+04 USD | 2.006e+04 | 0 | 791 | False | 19.2% apart, beyond 10% |
| qqq_baseline_pnl_ratio | estimate | 1.56 | 1.524 | 0 | 33 | True | 2.3% apart, within 10% |
| qqq_baseline_sharpe | estimate | 0.45 | 0.5317 | 0.03799 | 791 | False | paper outside 0.5317 +/- 0.07445 |
| qqq_baseline_max_dd | estimate | -22.84% | 22.3 | 0 | 791 | False | 197.6% apart, beyond 10% |
| qqq_baseline_expectancy | estimate | 17.14 USD | 658.8 | 944.3 | 33 | True | paper inside 658.8 +/- 1851 |
| qqq_macdpluslambda_trades | estimate | 31 trades | 24 |  |  |  | no standard error |
| qqq_macdpluslambda_win_rate | estimate | 61.29% | 50 | 0.1021 | 24 | False | paper outside 50 +/- 0.2 |
| qqq_macdpluslambda_total_pnl | estimate | 6.332e+04 USD | 5705 | 0 | 791 | False | 91.0% apart, beyond 10% |
| qqq_macdpluslambda_pnl_ratio | estimate | 1.89 | 1.198 | 0 | 24 | False | 36.6% apart, beyond 10% |
| qqq_macdpluslambda_sharpe | estimate | 1.13 | 0.2058 | 0.03593 | 791 | False | paper outside 0.2058 +/- 0.07042 |
| qqq_macdpluslambda_max_dd | estimate | -11.94% | 17.27 | 0 | 791 | False | 244.6% apart, beyond 10% |
| qqq_macdpluslambda_expectancy | estimate | 76.83 USD | 299.7 | 959.7 | 24 | True | paper inside 299.7 +/- 1881 |
| qqq_vpmacd_trades | estimate | 21 trades | 20 |  |  |  | no standard error |
| qqq_vpmacd_win_rate | estimate | 80.95% | 75 | 0.09682 | 20 | False | paper outside 75 +/- 0.1898 |
| qqq_vpmacd_total_pnl | estimate | 8.832e+04 USD | 4.312e+04 | 0 | 791 | False | 51.2% apart, beyond 10% |
| qqq_vpmacd_pnl_ratio | estimate | 1.72 | 1.235 | 0 | 20 | False | 28.2% apart, beyond 10% |
| qqq_vpmacd_sharpe | estimate | 1.51 | 0.8067 | 0.04093 | 791 | False | paper outside 0.8067 +/- 0.08023 |
| qqq_vpmacd_max_dd | estimate | -7.41% | 15.86 | 0 | 791 | False | 314.1% apart, beyond 10% |
| qqq_vpmacd_expectancy | estimate | 120.3 USD | 2375 | 1317 | 20 | True | paper inside 2375 +/- 2581 |
| dia_baseline_trades | estimate | 40 trades | 38 |  |  |  | no standard error |
| dia_baseline_win_rate | estimate | 40% | 31.58 | 0.07541 | 38 | False | paper outside 31.58 +/- 0.1478 |
| dia_baseline_total_pnl | estimate | 1237 USD | -2369 | 0 | 791 | False | 291.5% apart, beyond 10% |
| dia_baseline_pnl_ratio | estimate | 1.55 | 2.024 | 0 | 38 | False | 30.6% apart, beyond 10% |
| dia_baseline_sharpe | estimate | 0.09 | -0.0542 | 0.03558 | 791 | False | paper outside -0.0542 +/- 0.06974 |
| dia_baseline_max_dd | estimate | -13.95% | 14.6 | 0 | 791 | False | 204.6% apart, beyond 10% |
| dia_baseline_expectancy | estimate | 2.09 USD | -62.33 | 465.5 | 38 | True | paper inside -62.33 +/- 912.3 |
| dia_macdpluslambda_trades | estimate | 34 trades | 33 |  |  |  | no standard error |
| dia_macdpluslambda_win_rate | estimate | 50% | 42.42 | 0.08603 | 33 | False | paper outside 42.42 +/- 0.1686 |
| dia_macdpluslambda_total_pnl | estimate | -6862 USD | 1793 | 0 | 791 | False | 126.1% apart, beyond 10% |
| dia_macdpluslambda_pnl_ratio | estimate | 0.75 | 1.432 | 0 | 33 | False | 90.9% apart, beyond 10% |
| dia_macdpluslambda_sharpe | estimate | -0.2 | 0.1086 | 0.03566 | 791 | False | paper outside 0.1086 +/- 0.06989 |
| dia_macdpluslambda_max_dd | estimate | -14.19% | 13.03 | 0 | 791 | False | 191.9% apart, beyond 10% |
| dia_macdpluslambda_expectancy | estimate | -12.55 USD | 54.33 | 574.9 | 33 | True | paper inside 54.33 +/- 1127 |
| dia_vpmacd_trades | estimate | 13 trades | 22 |  |  |  | no standard error |
| dia_vpmacd_win_rate | estimate | 69.23% | 59.09 | 0.1048 | 22 | False | paper outside 59.09 +/- 0.2055 |
| dia_vpmacd_total_pnl | estimate | 2.959e+04 USD | 1.145e+04 | 0 | 791 | False | 61.3% apart, beyond 10% |
| dia_vpmacd_pnl_ratio | estimate | 3.72 | 1.162 | 0 | 22 | False | 68.8% apart, beyond 10% |
| dia_vpmacd_sharpe | estimate | 1.08 | 0.3892 | 0.03688 | 791 | False | paper outside 0.3892 +/- 0.07228 |
| dia_vpmacd_max_dd | estimate | -6.2% | 9.962 | 0 | 791 | False | 260.7% apart, beyond 10% |
| dia_vpmacd_expectancy | estimate | 226.9 USD | 552.3 | 651.7 | 22 | True | paper inside 552.3 +/- 1277 |
| ttest_pair1_spy_t | estimate | 1.717 | 0.6658 |  | 790 |  | no standard error |
| ttest_pair1_spy_p | estimate | 0.0432 | 0.2529 |  | 790 |  | no standard error |
| ttest_pair1_qqq_t | estimate | 1.665 | -0.8117 |  | 790 |  | no standard error |
| ttest_pair1_qqq_p | estimate | 0.0481 | 0.7914 |  | 790 |  | no standard error |
| ttest_pair1_dia_t | estimate | -0.6313 | 0.4914 |  | 790 |  | no standard error |
| ttest_pair1_dia_p | estimate | 0.0736 | 0.3116 |  | 790 |  | no standard error |
| ttest_pair2_spy_t | estimate | 0.4971 | 0.8587 |  | 790 |  | no standard error |
| ttest_pair2_spy_p | estimate | 0.3096 | 0.1954 |  | 790 |  | no standard error |
| ttest_pair2_qqq_t | estimate | 1.659 | 0.6797 |  | 790 |  | no standard error |
| ttest_pair2_qqq_p | estimate | 0.0488 | 0.2484 |  | 790 |  | no standard error |
| ttest_pair2_dia_t | estimate | 1.28 | 0.7332 |  | 790 |  | no standard error |
| ttest_pair2_dia_p | estimate | 0.1004 | 0.2318 |  | 790 |  | no standard error |
| ttest_pair3_spy_t | estimate | -0.8857 | 0.6295 |  | 790 |  | no standard error |
| ttest_pair3_spy_p | estimate | 0.812 | 0.2646 |  | 790 |  | no standard error |
| ttest_pair3_qqq_t | estimate | 0.3107 | 1.117 |  | 790 |  | no standard error |
| ttest_pair3_qqq_p | estimate | 0.3781 | 0.1323 |  | 790 |  | no standard error |
| ttest_pair3_dia_t | estimate | 1.706 | 0.5107 |  | 790 |  | no standard error |
| ttest_pair3_dia_p | estimate | 0.0442 | 0.3049 |  | 790 |  | no standard error |
| nw_pair1_spy_t | estimate | 1.898 | 0.7167 |  | 790 |  | no standard error |
| nw_pair1_spy_p | estimate | 0.0288 | 0.2368 |  | 790 |  | no standard error |
| nw_pair1_qqq_t | estimate | 1.693 | -0.8258 |  | 790 |  | no standard error |
| nw_pair1_qqq_p | estimate | 0.0452 | 0.7955 |  | 790 |  | no standard error |
| nw_pair1_dia_t | estimate | -0.6593 | 0.5056 |  | 790 |  | no standard error |
| nw_pair1_dia_p | estimate | 0.7452 | 0.3066 |  | 790 |  | no standard error |
| nw_pair2_spy_t | estimate | 0.5307 | 0.9982 |  | 790 |  | no standard error |
| nw_pair2_spy_p | estimate | 0.2978 | 0.1591 |  | 790 |  | no standard error |
| nw_pair2_qqq_t | estimate | 1.723 | 0.6895 |  | 790 |  | no standard error |
| nw_pair2_qqq_p | estimate | 0.0425 | 0.2452 |  | 790 |  | no standard error |
| nw_pair2_dia_t | estimate | 1.296 | 0.709 |  | 790 |  | no standard error |
| nw_pair2_dia_p | estimate | 0.0974 | 0.2392 |  | 790 |  | no standard error |
| nw_pair3_spy_t | estimate | -0.9922 | 0.7433 |  | 790 |  | no standard error |
| nw_pair3_spy_p | estimate | 0.8394 | 0.2287 |  | 790 |  | no standard error |
| nw_pair3_qqq_t | estimate | 0.3487 | 1.125 |  | 790 |  | no standard error |
| nw_pair3_qqq_p | estimate | 0.3637 | 0.1304 |  | 790 |  | no standard error |
| nw_pair3_dia_t | estimate | 1.789 | 0.4923 |  | 790 |  | no standard error |
| nw_pair3_dia_p | estimate | 0.0368 | 0.3112 |  | 790 |  | no standard error |
| bootstrap_pair1_spy_p | estimate | 0.024 | 0.241 |  | 790 |  | no standard error |
| bootstrap_pair2_qqq_p | estimate | 0.039 | 0.219 |  | 790 |  | no standard error |
| bootstrap_pair3_dia_p | estimate | 0.028 | 0.31 |  | 790 |  | no standard error |

## The paper's own numbers
- NOTE: one_sided_t_test Pair1 SPY MACD+lambda vs MACD: t = 1.7171, paper's p = 0.0432 matches one-sided (upper tail) (0.0432); two-sided p would be 0.0864
- NOTE: one_sided_t_test Pair1 QQQ MACD+lambda vs MACD: t = 1.6653, paper's p = 0.0481 matches one-sided (upper tail) (0.0481); two-sided p would be 0.0962
- NOTE: one_sided_t_test Pair1 DIA MACD+lambda vs MACD: t = -0.6313 and p = 0.0736 fit no side at the printed precision (two-sided p would be 0.5280); judged two-sided
- NOTE: one_sided_t_test Pair2 SPY VP-MACD vs MACD: t = 0.4971, paper's p = 0.3096 matches one-sided (upper tail) (0.3096); two-sided p would be 0.6193
- NOTE: one_sided_t_test Pair2 QQQ VP-MACD vs MACD: t = 1.6586, paper's p = 0.0488 matches one-sided (upper tail) (0.0488); two-sided p would be 0.0976
- NOTE: one_sided_t_test Pair2 DIA VP-MACD vs MACD: t = 1.2804, paper's p = 0.1004 matches one-sided (upper tail) (0.1004); two-sided p would be 0.2008
- NOTE: one_sided_t_test Pair3 SPY VP-MACD vs MACD+lambda: t = -0.8857, paper's p = 0.812 matches one-sided (upper tail) (0.8120); two-sided p would be 0.3760
- NOTE: one_sided_t_test Pair3 QQQ VP-MACD vs MACD+lambda: t = 0.3107, paper's p = 0.3781 matches one-sided (upper tail) (0.3781); two-sided p would be 0.7561
- NOTE: one_sided_t_test Pair3 DIA VP-MACD vs MACD+lambda: t = 1.7065, paper's p = 0.0442 matches one-sided (upper tail) (0.0442); two-sided p would be 0.0883
- NOTE: Newey-West HAC t-test Pair1 SPY: t = 1.8983, paper's p = 0.0288 matches one-sided (upper tail) (0.0288); two-sided p would be 0.0580
- NOTE: Newey-West HAC t-test Pair1 QQQ: t = 1.6931, paper's p = 0.0452 matches one-sided (upper tail) (0.0452); two-sided p would be 0.0908
- NOTE: Newey-West HAC t-test Pair1 DIA: t = -0.6593, paper's p = 0.7452 matches one-sided (upper tail) (0.7451); two-sided p would be 0.5099
- NOTE: Newey-West HAC t-test Pair2 SPY: t = 0.5307, paper's p = 0.2978 matches one-sided (upper tail) (0.2978); two-sided p would be 0.5958
- NOTE: Newey-West HAC t-test Pair2 QQQ: t = 1.7229, paper's p = 0.0425 matches one-sided (upper tail) (0.0425); two-sided p would be 0.0853
- NOTE: Newey-West HAC t-test Pair2 DIA: t = 1.2964, paper's p = 0.0974 matches one-sided (upper tail) (0.0974); two-sided p would be 0.1952
- NOTE: Newey-West HAC t-test Pair3 SPY: t = -0.9922, paper's p = 0.8394 matches one-sided (upper tail) (0.8395); two-sided p would be 0.3214
- NOTE: Newey-West HAC t-test Pair3 QQQ: t = 0.3487, paper's p = 0.3637 matches one-sided (upper tail) (0.3637); two-sided p would be 0.7274
- NOTE: Newey-West HAC t-test Pair3 DIA: t = 1.7894, paper's p = 0.0368 matches one-sided (upper tail) (0.0368); two-sided p would be 0.0739

## Guards
- no claims rejected
- spec problem unresolved: test 'circular_block_bootstrap Pair1 SPY MACD+lambda vs MACD': statistic 'not stated' is not the name of a claim
- spec problem unresolved: test 'circular_block_bootstrap Pair2 QQQ VP-MACD vs MACD': statistic 'not stated' is not the name of a claim
- spec problem unresolved: test 'circular_block_bootstrap Pair3 DIA VP-MACD vs MACD+lambda': statistic 'not stated' is not the name of a claim
- round 1: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (training_observations (1,259) at line 491). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 2050, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: ETFs SPY/QQQ/DIA as proxies for S&P 500/NASDAQ-100/DJIA indices; Yahoo Finance vendor; next-day open execution; integer shares with floor(cash/(open*(1+cost))); sigma_i interpreted as (High-Low)/Close because STD of single High-Low undefined without extra window; P* window N chosen as standard trading month (paper leaves N unstated); EMA via pandas ewm adjust=False span; Sharpe sqrt(252); MDD as max peak-to-trough; HAC Newey-West lags=5 Bartlett; block bootstrap length 5 with 1000 resamples

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 3 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 2, exit 0, 53.3s
- model calls: 40, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 2410991, out 145558 (reasoning 76567); cost $1.1646

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
