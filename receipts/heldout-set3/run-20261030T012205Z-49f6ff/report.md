The paper's numbers partly hold up: 26 of 45 checked results match within their uncertainty. Its main result, QQQ_VPMACD_totalPnL, is 8.832e+04 USD in the paper and 4.312e+04 USD here (not consistent).

# paper-replicator report: arXiv 2604.26063
**A Volume-Price-Adjusted MACD Trading Strategy with Sensitivity Calibration for U.S. Equity Indices**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| training_observations_per_instrument | count | 1259 trading days | 1259 |  |  | True | precise: the paper's count |
| testing_observations_per_instrument | count | 791 trading days | 791 |  |  | True | precise: the paper's count |
| number_of_indices | count | 3 indices | 3 |  |  |  | the script writes it as a fixed number (3 at line 455), so it is not judged |
| strategies_per_index | count | 3 strategies | 3 |  |  |  | the script writes it as a fixed number (3 at line 456), so it is not judged |
| initial_capital | parameter | 1e+05 USD | 100000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| one_way_transaction_cost | parameter | 4 bps | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| round_trip_cost | parameter | 8 bps | 8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| grid_lambda_min | parameter | 0.8 | 0.8 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| grid_lambda_max | parameter | 1 | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| grid_lambda_increment | parameter | 0.02 | 0.02 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| bootstrap_resamples | parameter | 1000 resamples | 1000 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| bootstrap_block_length | parameter | 5 days | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_SPY_MACDplus | parameter | 0.9 | 0.9 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_SPY_VPMACD | parameter | 0.88 | 0.88 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_QQQ_MACDplus | parameter | 0.84 | 0.84 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_QQQ_VPMACD | parameter | 0.98 | 0.98 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_DIA_MACDplus | parameter | 0.92 | 0.92 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_DIA_VPMACD | parameter | 0.86 | 0.86 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| SPY_baseline_trades | estimate | 40 trades | 38 | 0 | 38 | True | 5.0% apart, within 10% |
| SPY_baseline_winrate | estimate | 50% | 52.63 | 8.1 | 38 | True | paper inside 52.63 +/- 15.88 |
| SPY_baseline_totalPnL | estimate | 1.361e+04 USD | 9698 | 3073 | 38 | True | paper inside 9698 +/- 6024 |
| SPY_baseline_PnLratio | estimate | 1.39 | 1.2 |  | 38 |  | no standard error |
| SPY_baseline_sharpe | estimate | 0.47 | 0.3849 |  | 790 |  | no standard error |
| SPY_baseline_MDD | estimate | -13.78% | 13.01 | 0 | 791 | False | 194.4% apart, beyond 10% |
| SPY_baseline_expectancy | estimate | 19.39 USD | 286.9 | 498.6 | 38 | True | paper inside 286.9 +/- 977.1 |
| SPY_MACDlambda_trades | estimate | 36 trades | 29 | 0 | 29 | False | 19.4% apart, beyond 10% |
| SPY_MACDlambda_winrate | estimate | 55.56% | 51.72 | 9.279 | 29 | True | paper inside 51.72 +/- 18.19 |
| SPY_MACDlambda_totalPnL | estimate | 5.269e+04 USD | 1.53e+04 | 3655 | 29 | False | paper outside 1.53e+04 +/- 7164 |
| SPY_MACDlambda_PnLratio | estimate | 2.98 | 1.51 |  | 29 |  | no standard error |
| SPY_MACDlambda_sharpe | estimate | 1.35 | 0.5771 |  | 790 |  | no standard error |
| SPY_MACDlambda_MDD | estimate | -8.17% | 11.21 | 0 | 791 | False | 237.2% apart, beyond 10% |
| SPY_MACDlambda_expectancy | estimate | 121 USD | 571.4 | 678.7 | 29 | True | paper inside 571.4 +/- 1330 |
| SPY_VPMACD_trades | estimate | 6 trades | 21 | 0 | 21 | False | 250.0% apart, beyond 10% |
| SPY_VPMACD_winrate | estimate | 50% | 71.43 | 9.858 | 21 | False | paper outside 71.43 +/- 19.32 |
| SPY_VPMACD_totalPnL | estimate | 2.754e+04 USD | 3.213e+04 | 2749 | 21 | True | paper inside 3.213e+04 +/- 5389 |
| SPY_VPMACD_PnLratio | estimate | 8.61 | 1.767 |  | 21 |  | no standard error |
| SPY_VPMACD_sharpe | estimate | 0.96 | 0.7907 |  | 790 |  | no standard error |
| SPY_VPMACD_MDD | estimate | -6.33% | 9.142 | 0 | 791 | False | 244.4% apart, beyond 10% |
| SPY_VPMACD_expectancy | estimate | 365.7 USD | 1486 | 600 | 21 | True | paper inside 1486 +/- 1176 |
| QQQ_baseline_trades | estimate | 35 trades | 33 | 0 | 33 | True | 5.7% apart, within 10% |
| QQQ_baseline_winrate | estimate | 45.71% | 48.48 | 8.7 | 33 | True | paper inside 48.48 +/- 17.05 |
| QQQ_baseline_totalPnL | estimate | 1.682e+04 USD | 2.006e+04 | 5425 | 33 | True | paper inside 2.006e+04 +/- 1.063e+04 |
| QQQ_baseline_PnLratio | estimate | 1.56 | 1.524 |  | 33 |  | no standard error |
| QQQ_baseline_sharpe | estimate | 0.45 | 0.5317 |  | 790 |  | no standard error |
| QQQ_baseline_MDD | estimate | -22.84% | 22.3 | 0 | 791 | False | 197.6% apart, beyond 10% |
| QQQ_baseline_expectancy | estimate | 17.14 USD | 658.8 | 944.3 | 33 | True | paper inside 658.8 +/- 1851 |
| QQQ_MACDlambda_trades | estimate | 31 trades | 24 | 0 | 24 | False | 22.6% apart, beyond 10% |
| QQQ_MACDlambda_winrate | estimate | 61.29% | 50 | 10.21 | 24 | True | paper inside 50 +/- 20 |
| QQQ_MACDlambda_totalPnL | estimate | 6.332e+04 USD | 5705 | 4702 | 24 | False | paper outside 5705 +/- 9215 |
| QQQ_MACDlambda_PnLratio | estimate | 1.89 | 1.198 |  | 24 |  | no standard error |
| QQQ_MACDlambda_sharpe | estimate | 1.13 | 0.2058 |  | 790 |  | no standard error |
| QQQ_MACDlambda_MDD | estimate | -11.94% | 17.27 | 0 | 791 | False | 244.6% apart, beyond 10% |
| QQQ_MACDlambda_expectancy | estimate | 76.83 USD | 299.7 | 959.7 | 24 | True | paper inside 299.7 +/- 1881 |
| QQQ_VPMACD_trades | estimate | 21 trades | 20 | 0 | 20 | True | 4.8% apart, within 10% |
| QQQ_VPMACD_winrate | estimate | 80.95% | 75 | 9.682 | 20 | True | paper inside 75 +/- 18.98 |
| QQQ_VPMACD_totalPnL | estimate | 8.832e+04 USD | 4.312e+04 | 5888 | 20 | False | paper outside 4.312e+04 +/- 1.154e+04 |
| QQQ_VPMACD_PnLratio | estimate | 1.72 | 1.235 |  | 20 |  | no standard error |
| QQQ_VPMACD_sharpe | estimate | 1.51 | 0.8067 |  | 790 |  | no standard error |
| QQQ_VPMACD_MDD | estimate | -7.41% | 15.86 | 0 | 791 | False | 314.1% apart, beyond 10% |
| QQQ_VPMACD_expectancy | estimate | 120.3 USD | 2375 | 1317 | 20 | True | paper inside 2375 +/- 2581 |
| DIA_baseline_trades | estimate | 40 trades | 38 | 0 | 38 | True | 5.0% apart, within 10% |
| DIA_baseline_winrate | estimate | 40% | 31.58 | 7.541 | 38 | True | paper inside 31.58 +/- 14.78 |
| DIA_baseline_totalPnL | estimate | 1237 USD | -2369 | 2869 | 38 | True | paper inside -2369 +/- 5624 |
| DIA_baseline_PnLratio | estimate | 1.55 | 2.024 |  | 38 |  | no standard error |
| DIA_baseline_sharpe | estimate | 0.09 | -0.0542 |  | 790 |  | no standard error |
| DIA_baseline_MDD | estimate | -13.95% | 14.6 | 0 | 791 | False | 204.6% apart, beyond 10% |
| DIA_baseline_expectancy | estimate | 2.09 USD | -62.33 | 465.5 | 38 | True | paper inside -62.33 +/- 912.3 |
| DIA_MACDlambda_trades | estimate | 34 trades | 33 | 0 | 33 | True | 2.9% apart, within 10% |
| DIA_MACDlambda_winrate | estimate | 50% | 42.42 | 8.603 | 33 | True | paper inside 42.42 +/- 16.86 |
| DIA_MACDlambda_totalPnL | estimate | -6862 USD | 1793 | 3302 | 33 | False | paper outside 1793 +/- 6473 |
| DIA_MACDlambda_PnLratio | estimate | 0.75 | 1.432 |  | 33 |  | no standard error |
| DIA_MACDlambda_sharpe | estimate | -0.2 | 0.1086 |  | 790 |  | no standard error |
| DIA_MACDlambda_MDD | estimate | -14.19% | 13.03 | 0 | 791 | False | 191.9% apart, beyond 10% |
| DIA_MACDlambda_expectancy | estimate | -12.55 USD | 54.33 | 574.9 | 33 | True | paper inside 54.33 +/- 1127 |
| DIA_VPMACD_trades | estimate | 13 trades | 22 | 0 | 22 | False | 69.2% apart, beyond 10% |
| DIA_VPMACD_winrate | estimate | 69.23% | 59.09 | 10.48 | 22 | True | paper inside 59.09 +/- 20.55 |
| DIA_VPMACD_totalPnL | estimate | 2.959e+04 USD | 1.145e+04 | 3057 | 22 | False | paper outside 1.145e+04 +/- 5991 |
| DIA_VPMACD_PnLratio | estimate | 3.72 | 1.162 |  | 22 |  | no standard error |
| DIA_VPMACD_sharpe | estimate | 1.08 | 0.3892 |  | 790 |  | no standard error |
| DIA_VPMACD_MDD | estimate | -6.2% | 9.962 | 0 | 791 | False | 260.7% apart, beyond 10% |
| DIA_VPMACD_expectancy | estimate | 226.9 USD | 552.3 | 651.7 | 22 | True | paper inside 552.3 +/- 1277 |
| ttest_pair1_SPY_t | estimate | 1.717 | 0.6658 |  | 790 |  | no standard error |
| ttest_pair1_SPY_p | estimate | 0.0432 | 0.2529 |  | 790 |  | no standard error |
| ttest_pair1_QQQ_t | estimate | 1.665 | -0.8117 |  | 790 |  | no standard error |
| ttest_pair1_QQQ_p | estimate | 0.0481 | 0.7914 |  | 790 |  | no standard error |
| ttest_pair1_DIA_t | estimate | -0.6313 | 0.4914 |  | 790 |  | no standard error |
| ttest_pair1_DIA_p | estimate | 0.0736 | 0.3116 |  | 790 |  | no standard error |
| ttest_pair2_SPY_t | estimate | 0.4971 | 0.8587 |  | 790 |  | no standard error |
| ttest_pair2_SPY_p | estimate | 0.3096 | 0.1954 |  | 790 |  | no standard error |
| ttest_pair2_QQQ_t | estimate | 1.659 | 0.6797 |  | 790 |  | no standard error |
| ttest_pair2_QQQ_p | estimate | 0.0488 | 0.2484 |  | 790 |  | no standard error |
| ttest_pair2_DIA_t | estimate | 1.28 | 0.7332 |  | 790 |  | no standard error |
| ttest_pair2_DIA_p | estimate | 0.1004 | 0.2318 |  | 790 |  | no standard error |
| ttest_pair3_SPY_t | estimate | -0.8857 | 0.6295 |  | 790 |  | no standard error |
| ttest_pair3_SPY_p | estimate | 0.812 | 0.2646 |  | 790 |  | no standard error |
| ttest_pair3_QQQ_t | estimate | 0.3107 | 1.117 |  | 790 |  | no standard error |
| ttest_pair3_QQQ_p | estimate | 0.3781 | 0.1323 |  | 790 |  | no standard error |
| ttest_pair3_DIA_t | estimate | 1.706 | 0.5107 |  | 790 |  | no standard error |
| ttest_pair3_DIA_p | estimate | 0.0442 | 0.3049 |  | 790 |  | no standard error |
| nwttest_pair1_SPY_t | estimate | 1.898 | 0.7308 |  | 790 |  | no standard error |
| nwttest_pair1_SPY_p | estimate | 0.0288 | 0.2324 |  | 790 |  | no standard error |
| nwttest_pair1_QQQ_t | estimate | 1.693 | -0.8378 |  | 790 |  | no standard error |
| nwttest_pair1_QQQ_p | estimate | 0.0452 | 0.7989 |  | 790 |  | no standard error |
| nwttest_pair1_DIA_t | estimate | -0.6593 | 0.5066 |  | 790 |  | no standard error |
| nwttest_pair1_DIA_p | estimate | 0.7452 | 0.3062 |  | 790 |  | no standard error |
| nwttest_pair2_SPY_t | estimate | 0.5307 | 1.002 |  | 790 |  | no standard error |
| nwttest_pair2_SPY_p | estimate | 0.2978 | 0.1583 |  | 790 |  | no standard error |
| nwttest_pair2_QQQ_t | estimate | 1.723 | 0.686 |  | 790 |  | no standard error |
| nwttest_pair2_QQQ_p | estimate | 0.0425 | 0.2464 |  | 790 |  | no standard error |
| nwttest_pair2_DIA_t | estimate | 1.296 | 0.7013 |  | 790 |  | no standard error |
| nwttest_pair2_DIA_p | estimate | 0.0974 | 0.2415 |  | 790 |  | no standard error |
| nwttest_pair3_SPY_t | estimate | -0.9922 | 0.7456 |  | 790 |  | no standard error |
| nwttest_pair3_SPY_p | estimate | 0.8394 | 0.2279 |  | 790 |  | no standard error |
| nwttest_pair3_QQQ_t | estimate | 0.3487 | 1.126 |  | 790 |  | no standard error |
| nwttest_pair3_QQQ_p | estimate | 0.3637 | 0.1301 |  | 790 |  | no standard error |
| nwttest_pair3_DIA_t | estimate | 1.789 | 0.4911 |  | 790 |  | no standard error |
| nwttest_pair3_DIA_p | estimate | 0.0368 | 0.3117 |  | 790 |  | no standard error |
| bootstrap_pair1_SPY_p | estimate | 0.024 | 0.264 |  | 1000 |  | no standard error |
| bootstrap_pair2_QQQ_p | estimate | 0.039 | 0.222 |  | 1000 |  | no standard error |
| bootstrap_pair3_DIA_p | estimate | 0.028 | 0.326 |  | 1000 |  | no standard error |

## The paper's own numbers
- NOTE: Pair1 MACD+lambda vs Baseline MACD SPY one-sided t mean return >0: t = 1.7171, paper's p = 0.0432 matches one-sided (upper tail) (0.0432); two-sided p would be 0.0864
- NOTE: Pair1 QQQ one-sided t: t = 1.6653, paper's p = 0.0481 matches one-sided (upper tail) (0.0481); two-sided p would be 0.0962
- NOTE: Pair1 DIA one-sided t: t = -0.6313 and p = 0.0736 fit no side at the printed precision (two-sided p would be 0.5280); judged two-sided
- NOTE: Pair2 VP-MACD vs Baseline MACD SPY one-sided t: t = 0.4971, paper's p = 0.3096 matches one-sided (upper tail) (0.3096); two-sided p would be 0.6193
- NOTE: Pair2 QQQ one-sided t: t = 1.6586, paper's p = 0.0488 matches one-sided (upper tail) (0.0488); two-sided p would be 0.0976
- NOTE: Pair2 DIA one-sided t: t = 1.2804, paper's p = 0.1004 matches one-sided (upper tail) (0.1004); two-sided p would be 0.2008
- NOTE: Pair3 VP-MACD vs MACD+lambda SPY one-sided t: t = -0.8857, paper's p = 0.812 matches one-sided (upper tail) (0.8120); two-sided p would be 0.3760
- NOTE: Pair3 QQQ one-sided t: t = 0.3107, paper's p = 0.3781 matches one-sided (upper tail) (0.3781); two-sided p would be 0.7561
- NOTE: Pair3 DIA one-sided t: t = 1.7065, paper's p = 0.0442 matches one-sided (upper tail) (0.0442); two-sided p would be 0.0883
- NOTE: Newey-West HAC Pair1 SPY: t = 1.8983, paper's p = 0.0288 matches one-sided (upper tail) (0.0288); two-sided p would be 0.0580
- NOTE: Newey-West Pair1 QQQ: t = 1.6931, paper's p = 0.0452 matches one-sided (upper tail) (0.0452); two-sided p would be 0.0908
- NOTE: Newey-West Pair1 DIA: t = -0.6593, paper's p = 0.7452 matches one-sided (upper tail) (0.7451); two-sided p would be 0.5099
- NOTE: Newey-West Pair2 SPY: t = 0.5307, paper's p = 0.2978 matches one-sided (upper tail) (0.2978); two-sided p would be 0.5958
- NOTE: Newey-West Pair2 QQQ: t = 1.7229, paper's p = 0.0425 matches one-sided (upper tail) (0.0425); two-sided p would be 0.0853
- NOTE: Newey-West Pair2 DIA: t = 1.2964, paper's p = 0.0974 matches one-sided (upper tail) (0.0974); two-sided p would be 0.1952
- NOTE: Newey-West Pair3 SPY: t = -0.9922, paper's p = 0.8394 matches one-sided (upper tail) (0.8395); two-sided p would be 0.3214
- NOTE: Newey-West Pair3 QQQ: t = 0.3487, paper's p = 0.3637 matches one-sided (upper tail) (0.3637); two-sided p would be 0.7274
- NOTE: Newey-West Pair3 DIA: t = 1.7894, paper's p = 0.0368 matches one-sided (upper tail) (0.0368); two-sided p would be 0.0739

## Guards
- no claims rejected
- spec: the headline was written as prose ('SPY_VPMACD_totalPnL, QQQ_VPMACD_totalPnL, DIA_VPMACD_totalPnL, SPY_VPMACD_sharpe, QQQ_VPMACD_sharpe, DIA_VPMACD_sharpe, '); chosen from the claim names: ttest_pair2_QQQ_p
- spec problem unresolved: test 'Circular block bootstrap Pair1 SPY 1000 resamples block5': statistic 'not stated' is not the name of a claim
- spec problem unresolved: test 'Circular block bootstrap Pair2 QQQ': statistic 'not stated' is not the name of a claim
- spec problem unresolved: test 'Circular block bootstrap Pair3 DIA': statistic 'not stated' is not the name of a claim
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 791, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: VP-MACD rolling window N=20 (paper states N past days but no value; 20 chosen as standard volatility window). Sigma interpreted as (High-Low)/Close (paper writes STD(High-Low)/Close; single-day STD undefined, so taken as range/Close). r as |Close-Open|/(High-Low). P* = sum P*Vol*sigma*r / sum Vol = VW body. No leverage, integer shares next-open execution, cost 4bps one-way as paper. Sharpe uses portfolio daily returns over testing period, annualized sqrt252. Newey-West HAC lag = floor(4*(n/100)^(2/9)), normal p-value. Bootstrap circular block 1000 resamples block 5, p = proportion means <=0

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 3 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 1, exit 0, 52.7s
- model calls: 27, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 1225517, out 91002 (reasoning 45188); cost $0.7172

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
