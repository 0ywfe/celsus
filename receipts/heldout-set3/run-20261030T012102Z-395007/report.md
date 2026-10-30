We could not check this paper: the replication could not rebuild the paper's sample (Exact paper NASDAQ-100 vintage (wiki_nasdaq) not archived and quarterly rebalancing means nominal 100 list changes; fetched 98 vs union 101 vs nominal 100 differences cannot be precisely counted against unknown vintage); and the replication could not rebuild the paper's sample (N_NASDAQ100_nominal: 98 here, 100 in the paper). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2510.15942
**Intrinsic Geometry of Stock Market from Graph Ricci Flow Replication Spec**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| N_NASDAQ100_nominal | count | 100 stocks | 98 | 0 | 98 | False | 98 outside the paper's bound > 100 |
| window_years | parameter | 5 years | 4.884 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| alpha_idleness | parameter | 1 | 0.5 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_complete_equal_theoretical | parameter | 0.505 | 0.5052 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_complete_equal_formula | parameter | 1 | 0.5052 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| LLY_curvature_limit | parameter | -1 | 1.01 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| eigen_laplacian_complete_0 | parameter | 0 | 0 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| eigen_laplacian_complete_n_over_n1 | parameter | -1 | 1.01 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| eigen_multiplicity_n1 | parameter | -1 | 97 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ORC_global_lower_bound | parameter | -2 | -2 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ORC_global_upper_bound | parameter | 1 | 1 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_lower_bound_formula | parameter | 2 | -1.959 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_lower_bound_equal_weight_formula | parameter | 2 | -1.959 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_min_NASDAQ100_theoretical | parameter | -1.96 | -1.959 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| d_ij_theoretical_at_lower_bound | parameter | 2.96 | 2.959 | 0 | 98 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| corr_avg_empirical | estimate | 38% | 37.99 | 0.2165 | 4753 | True | paper inside 37.99 +/- 0.4244 |
| avg_edge_weight_empirical | estimate | 1.11 distance | 1.105 | 0.002023 | 4753 | False | 1.105 +/- 0.003964 outside the paper's bound > 1.11 |
| median_edge_weight_empirical | estimate | 1.11 distance | 1.111 | 0.002534 | 4753 | True | 1.111 +/- 0.004967 within the paper's bound > 1.11 |
| surgery_curvature_threshold | parameter | 0 kappa | 0 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| surgery_edge_weight_around | estimate | 3 distance | 1.516e-06 | 2.202e-09 | 4753 | False | 1.516e-06 +/- 4.316e-09 outside the paper's bound > 3 |
| flow_iteration_5 | parameter | 5 iterations | 5 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| flow_iteration_10 | parameter | 10 iterations | 10 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| flow_iteration_20 | parameter | 20 iterations | 20 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| L1_cluster_A_66 | tally | 66 stocks |  |  |  |  | not computed |
| L1_cluster_B_35 | tally | 35 stocks |  |  |  |  | not computed |
| L2_semicon_basket_16 | tally | 16 stocks |  |  |  |  | not computed |
| L2_semicond_parent_remainder_50 | tally | 50 stocks |  |  |  |  | not computed |
| L3_outlier_10 | tally | 10 stocks |  |  |  |  | not computed |
| L4_remaining_40 | tally | 40 stocks |  |  |  |  | not computed |
| L4_biotech_4 | tally | 4 stocks |  |  |  |  | not computed |
| L4_supermicro_1 | tally | 1 stocks |  |  |  |  | not computed |
| L4_remainder_35_for_L5 | tally | 35 stocks |  |  |  |  | not computed |
| L5_bigtech_17 | tally | 17 stocks |  |  |  |  | not computed |
| L5_tesla_group_18 | tally | 18 stocks |  |  |  |  | not computed |
| L2_health_staples_10_alt_branch | tally | 10 stocks |  |  |  |  | not computed |
| L3_industrials_17_alt_branch | tally | 17 stocks |  |  |  |  | not computed |

## The paper's own numbers
- FLAG: Level1 first Ricci flow + zero-curvature surgery: 66-stock tech-driven vs 35-stock non-cyclicals - total nominal 100 papers prints 66+35=101 discrepancy reproduced as printed - see note: 66 + 35 = 101, paper's total 100
- OK: Level2 within 66-stock tech cluster: 16 semiconductors vs remainder 50: 16 + 50 = 66, paper's total 66
- OK: Level3 within 50-stock cluster: 10 outlier vs remainder 40: 10 + 40 = 50, paper's total 50
- OK: Level4 within 40-stock cluster: 4 biotech +1 SMCI +35 remainder for next level: 4 + 1 + 35 = 40, paper's total 40
- OK: Level5 within that 35 remainder: 17 Big Tech vs 18 Tesla group: 17 + 18 = 35, paper's total 35

## Guards
- rejected claim L3_staples_energy_8 = >8: not in the paper's LaTeX
- spec: the headline was written as prose ('<L1_cluster_A_66, L1_cluster_B_35, L2_semicon_basket_16, avg_edge_weight_empirical, corr_avg_empirical, kappa_complete_e'); chosen from the claim names: avg_edge_weight_empirical
- spec: the headline was written as prose (':['); chosen from the claim names: surgery_edge_weight_around
- round 1: the builder ran out of turns
- round 2: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (N_NASDAQ100_nominal (>100) at line 161). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- attempt 3: 3 market-data items fetched on the host into data/market
- round 3: audit sent the sample back: N_NASDAQ100_nominal: the paper reports 100, your run produced 98
- sample: the replication could not rebuild the paper's sample (Exact paper NASDAQ-100 vintage (wiki_nasdaq) not archived and quarterly rebalancing means nominal 100 list changes; fetched 98 vs union 101 vs nominal 100 differences cannot be precisely counted against unknown vintage)
- caveat: the replication used other sources or methods for the paper's observations: Yahoo Finance via market_data live (same source yahoo_fin). Log returns (paper says r_i unspecified; log vs simple <1% corr diff). Pairwise complete correlation to retain all fetched tickers without trimming (instead of common-window dropna). GraphRicciCurvature OllivierRicci alpha=0.5 base=e exp_power=2 (Ni et al. 2019 github) for weighted mass; paper appendix describes uniform measure but that yields constant curvature 0.505 independent of w (proved W=(alpha-beta)d => kappa=(1-alpha)n/(n-1)), so weighted measure required for spread; library default referenced as github. APSP via floyd_warshall as in library; empirical w satisfies triangle inequality so d=w. Flow w^{(l+1)}=(1-kappa)d per paper. Window years computed from actual data dates, not printed 5
- caveat: the sample block's not_rebuilt: L3_staples_energy_8 is no claim's name, so it excused nothing

## Data sources
- prices: yfinance (host) (cache), fetched 2026-10-29, 1 tickers
- prices: yfinance (host) (cache), fetched 2026-10-30, 3 tickers
- prices: yfinance (live, sandbox), fetched 2026-10-30, 97 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 3, exit 0, 63.3s, with the packages the builder installed: Cython==3.3.0, GraphRicciCurvature==0.6.1, POT==0.9.7.post1, networkit==11.2.2, networkx==3.7, numpy==2.2.6, python-louvain==0.16, scipy==1.13.1, tabulate==0.10.0
- model calls: 46, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 1910688, out 133153 (reasoning 87716); cost $0.9721

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
